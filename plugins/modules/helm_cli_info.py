#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: helm_cli_info
short_description: Get informations from Helm package deployed inside the cluster
description:
  -  Get informations (values, states, ...) from Helm package deployed inside the cluster
version_added: "2.10"
author:
  - Lucas Boisserie (@LucasBoisserie)
requirements:
  - "helm (https://github.com/helm/helm/releases)"
  - "yaml (https://pypi.org/project/PyYAML/)"
options:
  binary_path:
    description:
      - The path of a helm binary to use.
    required: false
    type: path
  release_name:
    description:
      - Release name to manage
    required: true
    type: str
    aliases: [ name ]
  release_namespace:
    description:
      - Kubernetes namespace where the chart should be installed
      - Can't be changed with helm 2
    default: "default"
    required: false
    type: str
    aliases: [ namespace ]
  tiller_host:
    description:
      - Address of Tiller
      - Ignored when is helm 3
    type: str
  tiller_namespace:
    description:
      - Namespace of Tiller
      - Ignored when is helm 3
    default: "kube-system"
    type: str

#Helm options
  kube_context:
    description:
      - Helm option to specify which kubeconfig context to use
    type: str
  kubeconfig_path:
    description:
      - Helm option to specify kubeconfig path to use
    type: path
    aliases: [ kubeconfig ]
'''

EXAMPLES = '''
# With Helm 2
- name: Get grafana deployment
  helm_cli_info:
    name: test
    tiller_namespace: helm

# With Helm 3
- name: Deploy latest version of Grafana chart inside monitoring namespace
  helm_cli_info:
    name: test
    release_namespace: monitoring
'''

RETURN = """
status:
  type: complex
  description: A dictionary of status output
  returned: only when release exists
  contains:
    appversion:
      type: str
      returned: always
      description: Version of app deployed
    chart:
      type: str
      returned: always
      description: Chart name and chart version
    name:
      type: str
      returned: always
      description: Name of the release
    namespace:
      type: str
      returned: always
      description: Namespace where the release is deployed
    revision:
      type: str
      returned: always
      description: Number of time where the release has been updated
    status:
      type: str
      returned: always
      description: Status of release (can be DEPLOYED, FAILED, ...)
    updated:
      type: str
      returned: always
      description: The Date of last update
    values:
      type: str
      returned: always
      description: Dict of Values used to deploy
"""

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from ansible.module_utils.basic import AnsibleModule

module = None
is_helm_2 = True


# get Helm Version
def get_helm_client_version(command):
    is_helm_2_local = True
    version_command = command + " version --client --short"
    rc, out, err = module.run_command(version_command)

    if not out.startswith('Client: v2'):
        is_helm_2_local = False
        # Fallback on Helm 3
        version_command = command + " version --short"
        rc, out, err = module.run_command(version_command)

        if rc != 0:
            module.fail_json(
                msg="Failure when executing Helm command. Exited {0}.\nstdout: {1}\nstderr: {2}".format(rc, out, err),
                command=version_command
            )

    elif rc != 0:
        module.fail_json(
            msg="Failure when executing Helm command. Exited {0}.\nstdout: {1}\nstderr: {2}".format(rc, out, err),
            command=version_command
        )

    return is_helm_2_local


# Get Values from deployed release
def get_values(command, release_name, release_namespace):
    get_command = command + " get values --output=yaml " + release_name

    if not is_helm_2:
        get_command += " --namespace=" + release_namespace

    rc, out, err = module.run_command(get_command)

    if rc != 0:
        module.fail_json(
            msg="Failure when executing Helm command. Exited {0}.\nstdout: {1}\nstderr: {2}".format(rc, out, err),
            command=get_command
        )

    # Helm 3 return "null" string when no values are set
    if not is_helm_2 and out.rstrip("\n") == "null":
        return yaml.safe_load('{}')
    else:
        return yaml.safe_load(out)


# Get Release from all deployed releases
def get_release(state, release_name, release_namespace):
    if state is not None:
        if is_helm_2:
            for release in state['Releases']:
                # release = {k.lower(): v for k, v in release.items()} # NOT WORKING wit python 2.6
                release_lower = dict()
                for k, v in release.items():
                    release_lower[k.lower()] = v
                release = release_lower
                if release['name'] == release_name and release['namespace'] == release_namespace:
                    return release
        else:
            for release in state:
                if release['name'] == release_name and release['namespace'] == release_namespace:
                    return release
    return None


# Get Release state from deployed release
def get_release_status(command, release_name, release_namespace):
    list_command = command + " list --output=yaml "

    if not is_helm_2:
        list_command += " --namespace=" + release_namespace
        list_command += " --filter "

    list_command += release_name

    rc, out, err = module.run_command(list_command)

    if rc != 0:
        module.fail_json(
            msg="Failure when executing Helm command. Exited {0}.\nstdout: {1}\nstderr: {2}".format(rc, out, err),
            command=list_command
        )

    release = get_release(yaml.safe_load(out), release_name, release_namespace)

    if release is None:  # not install
        return None

    release['values'] = get_values(command, release_name, release_namespace)

    return release


def main():
    global module, is_helm_2

    module = AnsibleModule(
        argument_spec=dict(
            binary_path=dict(type='path'),
            release_name=dict(type='str', required=True, aliases=['name']),
            release_namespace=dict(type='str', default='default', aliases=['namespace']),
            tiller_host=dict(type='str'),
            tiller_namespace=dict(type='str', default='kube-system'),

            # Helm options
            kube_context=dict(type='str'),
            kubeconfig_path=dict(type='path', aliases=['kubeconfig']),
        ),
        supports_check_mode=True,
    )
    if not HAS_YAML:
        module.fail_json(msg="Could not import the yaml python module. Please install `yaml` package.")

    bin_path = module.params.get('binary_path')
    release_name = module.params.get('release_name')
    release_namespace = module.params.get('release_namespace')
    tiller_host = module.params.get('tiller_host')
    tiller_namespace = module.params.get('tiller_namespace')

    # Helm options
    kube_context = module.params.get('kube_context')
    kubeconfig_path = module.params.get('kubeconfig_path')

    if bin_path is not None:
        helm_cmd_common = bin_path
    else:
        helm_cmd_common = module.get_bin_path('helm', required=True)

    is_helm_2 = get_helm_client_version(helm_cmd_common)

    # Helm 2 need tiller, Helm 3 and higher doesn't
    if is_helm_2:
        if tiller_host is not None:
            helm_cmd_common += " --host=" + tiller_namespace
        else:
            helm_cmd_common += " --tiller-namespace=" + tiller_namespace

    if kube_context is not None:
        helm_cmd_common += " --kube-context " + kube_context

    if kubeconfig_path is not None:
        helm_cmd_common += " --kubeconfig " + kubeconfig_path

    # Get real/deployed release status
    release_status = get_release_status(helm_cmd_common, release_name, release_namespace)
    if release_status is not None:
        module.exit_json(changed=False, status=release_status)
    else:
        module.exit_json(changed=False)


if __name__ == '__main__':
    main()
