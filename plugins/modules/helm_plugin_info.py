#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: helm_plugin_info
short_description: Gather information about Helm plugins
version_added: "1.0.0"
author:
  - Abhijeet Kasurde (@Akasurde)
requirements:
  - "helm (https://github.com/helm/helm/releases)"
description:
  -  Gather information about Helm plugins installed in namespace.
options:
  release_namespace:
    description:
      - Kubernetes namespace where the helm plugins are installed.
    required: true
    type: str
    aliases: [ namespace ]

#Helm options
  plugin_name:
    description:
      - Name of Helm plugin, to gather particular plugin info.
    type: str
extends_documentation_fragment:
  - community.kubernetes.helm_common_options
'''

EXAMPLES = r'''
- name: Gather Helm plugin info
  community.kubernetes.helm_plugin_info:

- name: Gather Helm env plugin info
  community.kubernetes.helm_plugin_info:
    plugin_name: env
'''

RETURN = r'''
stdout:
  type: str
  description: Full `helm` command stdout, in case you want to display it or examine the event log
  returned: always
  sample: ''
stderr:
  type: str
  description: Full `helm` command stderr, in case you want to display it or examine the event log
  returned: always
  sample: ''
command:
  type: str
  description: Full `helm` command built by this module, in case you want to re-run the command outside the module or debug a problem.
  returned: always
  sample: helm plugin list ...
plugin_list:
  type: list
  description: Helm plugin dict inside a list
  returned: always
  sample: {
      "name": "env",
      "version": "0.1.0",
      "description": "Print out the helm environment."
  }
rc:
  type: int
  description: Helm plugin command return code
  returned: always
  sample: 1
'''

from ansible.module_utils.basic import AnsibleModule, env_fallback


def main():
    module = AnsibleModule(
        argument_spec=dict(
            binary_path=dict(type='path'),
            release_namespace=dict(type='str', required=True, aliases=['namespace']),
            plugin_name=dict(type='str',),
            # Helm options
            context=dict(type='str', aliases=['kube_context'], fallback=(env_fallback, ['K8S_AUTH_CONTEXT'])),
            kubeconfig=dict(type='path', aliases=['kubeconfig_path'], fallback=(env_fallback, ['K8S_AUTH_KUBECONFIG'])),
        ),
        supports_check_mode=True,
    )

    bin_path = module.params.get('binary_path')
    release_namespace = module.params.get('release_namespace')

    # Helm options
    kube_context = module.params.get('context')
    kubeconfig_path = module.params.get('kubeconfig')

    if bin_path is not None:
        helm_cmd_common = bin_path
    else:
        helm_cmd_common = 'helm'

    helm_cmd_common = module.get_bin_path(helm_cmd_common, required=True)

    helm_cmd_common += " plugin"

    if kube_context is not None:
        helm_cmd_common += " --kube-context " + kube_context

    if kubeconfig_path is not None:
        helm_cmd_common += " --kubeconfig " + kubeconfig_path

    helm_cmd_common += " --namespace=" + release_namespace

    plugin_name = module.params.get('plugin_name')
    helm_plugin_list = helm_cmd_common + " list"
    rc, out, err = module.run_command(helm_plugin_list)
    if rc != 0 or (out == '' and err == ''):
        module.fail_json(
            msg="Failed to get Helm plugin info",
            command=helm_plugin_list,
            stdout=out,
            stderr=err,
            rc=rc,
        )

    plugin_list = []
    if out:
        for line in out.splitlines():
            if line.startswith("NAME"):
                continue
            name, version, description = line.split('\t', 3)
            name = name.strip()
            version = version.strip()
            description = description.strip()
            if plugin_name is None:
                plugin_list.append({
                    'name': name,
                    'version': version,
                    'description': description,
                })
                continue

            if plugin_name == name:
                plugin_list.append({
                    'name': name,
                    'version': version,
                    'description': description,
                })
                break

    module.exit_json(
        changed=True,
        command=helm_plugin_list,
        stdout=out,
        stderr=err,
        rc=rc,
        plugin_list=plugin_list,
    )


if __name__ == '__main__':
    main()
