#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: helm_info

short_description: Get information from Helm package deployed inside the cluster

version_added: "0.11.0"

author:
  - Lucas Boisserie (@LucasBoisserie)

requirements:
  - "helm (https://github.com/helm/helm/releases)"
  - "yaml (https://pypi.org/project/PyYAML/)"

description:
  -  Get information (values, states, ...) from Helm package deployed inside the cluster.

options:
  release_name:
    description:
      - Release name to manage.
    required: true
    type: str
    aliases: [ name ]
  release_namespace:
    description:
      - Kubernetes namespace where the chart should be installed.
    required: true
    type: str
    aliases: [ namespace ]
extends_documentation_fragment:
  - community.kubernetes.helm_common_options
'''

EXAMPLES = r'''
- name: Deploy latest version of Grafana chart inside monitoring namespace
  community.kubernetes.helm_info:
    name: test
    release_namespace: monitoring
'''

RETURN = r'''
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
'''

import traceback

try:
    import yaml
    IMP_YAML = True
except ImportError:
    IMP_YAML_ERR = traceback.format_exc()
    IMP_YAML = False

from ansible.module_utils.basic import AnsibleModule, missing_required_lib, env_fallback

module = None


# Get Values from deployed release
def get_values(command, release_name):
    get_command = command + " get values --output=yaml " + release_name

    rc, out, err = module.run_command(get_command)

    if rc != 0:
        module.fail_json(
            msg="Failure when executing Helm command. Exited {0}.\nstdout: {1}\nstderr: {2}".format(rc, out, err),
            command=get_command
        )

    # Helm 3 return "null" string when no values are set
    if out.rstrip("\n") == "null":
        return {}
    else:
        return yaml.safe_load(out)


# Get Release from all deployed releases
def get_release(state, release_name):
    if state is not None:
        for release in state:
            if release['name'] == release_name:
                return release
    return None


# Get Release state from deployed release
def get_release_status(command, release_name):
    list_command = command + " list --output=yaml --filter " + release_name

    rc, out, err = module.run_command(list_command)

    if rc != 0:
        module.fail_json(
            msg="Failure when executing Helm command. Exited {0}.\nstdout: {1}\nstderr: {2}".format(rc, out, err),
            command=list_command
        )

    release = get_release(yaml.safe_load(out), release_name)

    if release is None:  # not install
        return None

    release['values'] = get_values(command, release_name)

    return release


def main():
    global module

    module = AnsibleModule(
        argument_spec=dict(
            binary_path=dict(type='path'),
            release_name=dict(type='str', required=True, aliases=['name']),
            release_namespace=dict(type='str', required=True, aliases=['namespace']),

            # Helm options
            kube_context=dict(type='str', aliases=['context'], fallback=(env_fallback, ['K8S_AUTH_CONTEXT'])),
            kubeconfig_path=dict(type='path', aliases=['kubeconfig'], fallback=(env_fallback, ['K8S_AUTH_KUBECONFIG'])),
        ),
        supports_check_mode=True,
    )

    if not IMP_YAML:
        module.fail_json(msg=missing_required_lib("yaml"), exception=IMP_YAML_ERR)

    bin_path = module.params.get('binary_path')
    release_name = module.params.get('release_name')
    release_namespace = module.params.get('release_namespace')

    # Helm options
    kube_context = module.params.get('kube_context')
    kubeconfig_path = module.params.get('kubeconfig_path')

    if bin_path is not None:
        helm_cmd_common = bin_path
    else:
        helm_cmd_common = module.get_bin_path('helm', required=True)

    if kube_context is not None:
        helm_cmd_common += " --kube-context " + kube_context

    if kubeconfig_path is not None:
        helm_cmd_common += " --kubeconfig " + kubeconfig_path

    helm_cmd_common += " --namespace=" + release_namespace

    release_status = get_release_status(helm_cmd_common, release_name)

    if release_status is not None:
        module.exit_json(changed=False, status=release_status)

    module.exit_json(changed=False)


if __name__ == '__main__':
    main()
