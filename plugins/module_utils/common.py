# Copyright 2018 Red Hat | Ansible
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import copy
from datetime import datetime
import time
import os
import traceback


from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible.module_utils.six import iteritems, string_types
from ansible.module_utils._text import to_native

K8S_IMP_ERR = None
try:
    import kubernetes
    import openshift
    from openshift.dynamic import DynamicClient
    from openshift.dynamic.exceptions import ResourceNotFoundError, ResourceNotUniqueError, NotFoundError
    HAS_K8S_MODULE_HELPER = True
    k8s_import_exception = None
except ImportError as e:
    HAS_K8S_MODULE_HELPER = False
    k8s_import_exception = e
    K8S_IMP_ERR = traceback.format_exc()

YAML_IMP_ERR = None
try:
    import yaml
    HAS_YAML = True
except ImportError:
    YAML_IMP_ERR = traceback.format_exc()
    HAS_YAML = False

try:
    import urllib3
    urllib3.disable_warnings()
except ImportError:
    pass

try:
    from openshift.dynamic.apply import recursive_diff
except ImportError:
    from ansible.module_utils.common.dict_transformations import recursive_diff


def list_dict_str(value):
    if isinstance(value, list):
        return value
    elif isinstance(value, dict):
        return value
    elif isinstance(value, string_types):
        return value
    raise TypeError


ARG_ATTRIBUTES_BLACKLIST = ('property_path',)

COMMON_ARG_SPEC = {
    'state': {
        'default': 'present',
        'choices': ['present', 'absent'],
    },
    'force': {
        'type': 'bool',
        'default': False,
    },
    'resource_definition': {
        'type': list_dict_str,
        'aliases': ['definition', 'inline']
    },
    'src': {
        'type': 'path',
    },
    'kind': {},
    'name': {},
    'namespace': {},
    'api_version': {
        'default': 'v1',
        'aliases': ['api', 'version'],
    },
}

AUTH_ARG_SPEC = {
    'kubeconfig': {
        'type': 'path',
    },
    'context': {},
    'host': {},
    'api_key': {
        'no_log': True,
    },
    'username': {},
    'password': {
        'no_log': True,
    },
    'validate_certs': {
        'type': 'bool',
        'aliases': ['verify_ssl'],
    },
    'ca_cert': {
        'type': 'path',
        'aliases': ['ssl_ca_cert'],
    },
    'client_cert': {
        'type': 'path',
        'aliases': ['cert_file'],
    },
    'client_key': {
        'type': 'path',
        'aliases': ['key_file'],
    },
    'proxy': {
        'type': 'str',
    },
    'persist_config': {
        'type': 'bool',
    },
}

# Map kubernetes-client parameters to ansible parameters
AUTH_ARG_MAP = {
    'kubeconfig': 'kubeconfig',
    'context': 'context',
    'host': 'host',
    'api_key': 'api_key',
    'username': 'username',
    'password': 'password',
    'verify_ssl': 'validate_certs',
    'ssl_ca_cert': 'ca_cert',
    'cert_file': 'client_cert',
    'key_file': 'client_key',
    'proxy': 'proxy',
    'persist_config': 'persist_config',
}


class K8sAnsibleMixin(object):
    _argspec_cache = None

    @property
    def argspec(self):
        """
        Introspect the model properties, and return an Ansible module arg_spec dict.
        :return: dict
        """
        if self._argspec_cache:
            return self._argspec_cache
        argument_spec = copy.deepcopy(COMMON_ARG_SPEC)
        argument_spec.update(copy.deepcopy(AUTH_ARG_SPEC))
        self._argspec_cache = argument_spec
        return self._argspec_cache

    def get_api_client(self, **auth_params):
        auth_params = auth_params or getattr(self, 'params', {})
        auth = {}

        # If authorization variables aren't defined, look for them in environment variables
        for true_name, arg_name in AUTH_ARG_MAP.items():
            if auth_params.get(arg_name) is None:
                env_value = os.getenv('K8S_AUTH_{0}'.format(arg_name.upper()), None) or os.getenv('K8S_AUTH_{0}'.format(true_name.upper()), None)
                if env_value is not None:
                    if AUTH_ARG_SPEC[arg_name].get('type') == 'bool':
                        env_value = env_value.lower() not in ['0', 'false', 'no']
                    auth[true_name] = env_value
            else:
                auth[true_name] = auth_params[arg_name]

        def auth_set(*names):
            return all([auth.get(name) for name in names])

        if auth_set('username', 'password', 'host') or auth_set('api_key', 'host'):
            # We have enough in the parameters to authenticate, no need to load incluster or kubeconfig
            pass
        elif auth_set('kubeconfig') or auth_set('context'):
            try:
                kubernetes.config.load_kube_config(auth.get('kubeconfig'), auth.get('context'), persist_config=auth.get('persist_config'))
            except Exception as err:
                self.fail(msg='Failed to load kubeconfig due to %s' % to_native(err))
        else:
            # First try to do incluster config, then kubeconfig
            try:
                kubernetes.config.load_incluster_config()
            except kubernetes.config.ConfigException:
                try:
                    kubernetes.config.load_kube_config(auth.get('kubeconfig'), auth.get('context'), persist_config=auth.get('persist_config'))
                except Exception as err:
                    self.fail(msg='Failed to load kubeconfig due to %s' % to_native(err))

        # Override any values in the default configuration with Ansible parameters
        configuration = kubernetes.client.Configuration()
        for key, value in iteritems(auth):
            if key in AUTH_ARG_MAP.keys() and value is not None:
                if key == 'api_key':
                    setattr(configuration, key, {'authorization': "Bearer {0}".format(value)})
                else:
                    setattr(configuration, key, value)

        kubernetes.client.Configuration.set_default(configuration)
        return DynamicClient(kubernetes.client.ApiClient(configuration))

    def find_resource(self, kind, api_version, fail=False):
        for attribute in ['kind', 'name', 'singular_name']:
            try:
                return self.client.resources.get(**{'api_version': api_version, attribute: kind})
            except (ResourceNotFoundError, ResourceNotUniqueError):
                pass
        try:
            return self.client.resources.get(api_version=api_version, short_names=[kind])
        except (ResourceNotFoundError, ResourceNotUniqueError):
            if fail:
                self.fail(msg='Failed to find exact match for {0}.{1} by [kind, name, singularName, shortNames]'.format(api_version, kind))

    def kubernetes_facts(self, kind, api_version, name=None, namespace=None, label_selectors=None, field_selectors=None):
        resource = self.find_resource(kind, api_version)
        if not resource:
            return dict(resources=[])
        try:
            result = resource.get(name=name,
                                  namespace=namespace,
                                  label_selector=','.join(label_selectors),
                                  field_selector=','.join(field_selectors)).to_dict()
        except openshift.dynamic.exceptions.NotFoundError:
            return dict(resources=[])

        if 'items' in result:
            return dict(resources=result['items'])
        else:
            return dict(resources=[result])

    def remove_aliases(self):
        """
        The helper doesn't know what to do with aliased keys
        """
        for k, v in iteritems(self.argspec):
            if 'aliases' in v:
                for alias in v['aliases']:
                    if alias in self.params:
                        self.params.pop(alias)

    def load_resource_definitions(self, src):
        """ Load the requested src path """
        result = None
        path = os.path.normpath(src)
        if not os.path.exists(path):
            self.fail(msg="Error accessing {0}. Does the file exist?".format(path))
        try:
            with open(path, 'r') as f:
                result = list(yaml.safe_load_all(f))
        except (IOError, yaml.YAMLError) as exc:
            self.fail(msg="Error loading resource_definition: {0}".format(exc))
        return result

    @staticmethod
    def diff_objects(existing, new):
        result = dict()
        diff = recursive_diff(existing, new)
        if diff:
            result['before'] = diff[0]
            result['after'] = diff[1]
        return not diff, result


class KubernetesAnsibleModule(AnsibleModule, K8sAnsibleMixin):
    resource_definition = None
    api_version = None
    kind = None

    def __init__(self, *args, **kwargs):

        kwargs['argument_spec'] = self.argspec
        AnsibleModule.__init__(self, *args, **kwargs)

        if not HAS_K8S_MODULE_HELPER:
            self.fail_json(msg=missing_required_lib('openshift'), exception=K8S_IMP_ERR,
                           error=to_native(k8s_import_exception))
        self.openshift_version = openshift.__version__

        if not HAS_YAML:
            self.fail_json(msg=missing_required_lib("PyYAML"), exception=YAML_IMP_ERR)

    def execute_module(self):
        raise NotImplementedError()

    def fail(self, msg=None):
        self.fail_json(msg=msg)

    def _wait_for(self, resource, name, namespace, predicate, sleep, timeout, state):
        start = datetime.now()

        def _wait_for_elapsed():
            return (datetime.now() - start).seconds

        response = None
        while _wait_for_elapsed() < timeout:
            try:
                response = resource.get(name=name, namespace=namespace)
                if predicate(response):
                    if response:
                        return True, response.to_dict(), _wait_for_elapsed()
                    else:
                        return True, {}, _wait_for_elapsed()
                time.sleep(sleep)
            except NotFoundError:
                if state == 'absent':
                    return True, {}, _wait_for_elapsed()
        if response:
            response = response.to_dict()
        return False, response, _wait_for_elapsed()

    def wait(self, resource, definition, sleep, timeout, state='present', condition=None):

        def _deployment_ready(deployment):
            # FIXME: frustratingly bool(deployment.status) is True even if status is empty
            # Furthermore deployment.status.availableReplicas == deployment.status.replicas == None if status is empty
            # deployment.status.replicas is None is perfectly ok if desired replicas == 0
            # Scaling up means that we also need to check that we're not in a
            # situation where status.replicas == status.availableReplicas
            # but spec.replicas != status.replicas
            return (deployment.status
                    and deployment.spec.replicas == (deployment.status.replicas or 0)
                    and deployment.status.availableReplicas == deployment.status.replicas
                    and deployment.status.observedGeneration == deployment.metadata.generation
                    and not deployment.status.unavailableReplicas)

        def _pod_ready(pod):
            return (pod.status and pod.status.containerStatuses is not None
                    and all([container.ready for container in pod.status.containerStatuses]))

        def _daemonset_ready(daemonset):
            return (daemonset.status and daemonset.status.desiredNumberScheduled is not None
                    and daemonset.status.numberReady == daemonset.status.desiredNumberScheduled
                    and daemonset.status.observedGeneration == daemonset.metadata.generation
                    and not daemonset.status.unavailableReplicas)

        def _custom_condition(resource):
            if not resource.status or not resource.status.conditions:
                return False
            match = [x for x in resource.status.conditions if x.type == condition['type']]
            if not match:
                return False
            # There should never be more than one condition of a specific type
            match = match[0]
            if match.status == 'Unknown':
                if match.status == condition['status']:
                    if 'reason' not in condition:
                        return True
                    if condition['reason']:
                        return match.reason == condition['reason']
                return False
            status = True if match.status == 'True' else False
            if status == condition['status']:
                if condition.get('reason'):
                    return match.reason == condition['reason']
                return True
            return False

        def _resource_absent(resource):
            return not resource

        waiter = dict(
            Deployment=_deployment_ready,
            DaemonSet=_daemonset_ready,
            Pod=_pod_ready
        )
        kind = definition['kind']
        if state == 'present' and not condition:
            predicate = waiter.get(kind, lambda x: x)
        elif state == 'present' and condition:
            predicate = _custom_condition
        else:
            predicate = _resource_absent
        return self._wait_for(resource, definition['metadata']['name'], definition['metadata'].get('namespace'), predicate, sleep, timeout, state)
