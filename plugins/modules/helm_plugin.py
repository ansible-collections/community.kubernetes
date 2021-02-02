#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: helm_plugin
short_description: Manage Helm plugins
version_added: "1.0.0"
author:
  - Abhijeet Kasurde (@Akasurde)
requirements:
  - "helm (https://github.com/helm/helm/releases)"
description:
  -  Manages Helm plugins.
options:
  # TODO: (akasurde) Remove this in version 2.0
  release_namespace:
    description:
      - Kubernetes namespace where the helm plugin should be installed.
    type: str
    aliases: [ namespace ]

#Helm options
  state:
    description:
      - If C(state=present) the Helm plugin will be installed.
      - If C(state=absent) the Helm plugin will be removed.
    choices: [ absent, present ]
    default: present
    type: str
  plugin_name:
    description:
      - Name of Helm plugin.
      - Required only if C(state=absent).
    type: str
  plugin_path:
    description:
      - Plugin path to a plugin on your local file system or a url of a remote VCS repo.
      - If plugin path from file system is provided, make sure that tar is present on remote
        machine and not on Ansible controller.
      - Required only if C(state=present).
    type: str
extends_documentation_fragment:
  - community.kubernetes.helm_common_options
'''

EXAMPLES = r'''
- name: Install Helm env plugin
  community.kubernetes.helm_plugin:
    plugin_path: https://github.com/adamreese/helm-env
    state: present

- name: Install Helm plugin from local filesystem
  community.kubernetes.helm_plugin:
    plugin_path: https://domain/path/to/plugin.tar.gz
    state: present

- name: Remove Helm env plugin
  community.kubernetes.helm_plugin:
    plugin_name: env
    state: absent
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
msg:
  type: str
  description: Info about successful command
  returned: always
  sample: "Plugin installed successfully"
rc:
  type: int
  description: Helm plugin command return code
  returned: always
  sample: 1
'''

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible_collections.community.kubernetes.plugins.module_utils.helm import run_helm


def main():
    module = AnsibleModule(
        argument_spec=dict(
            binary_path=dict(type='path'),
            release_namespace=dict(type='str', aliases=['namespace']),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            plugin_path=dict(type='str',),
            plugin_name=dict(type='str',),
            # Helm options
            context=dict(type='str', aliases=['kube_context'], fallback=(env_fallback, ['K8S_AUTH_CONTEXT'])),
            kubeconfig=dict(type='path', aliases=['kubeconfig_path'], fallback=(env_fallback, ['K8S_AUTH_KUBECONFIG'])),

            # Generic auth key
            host=dict(type='str', fallback=(env_fallback, ['K8S_AUTH_HOST'])),
            ca_cert=dict(type='path', aliases=['ssl_ca_cert'], fallback=(env_fallback, ['K8S_AUTH_SSL_CA_CERT'])),
            validate_certs=dict(type='bool', default=True, aliases=['verify_ssl'], fallback=(env_fallback, ['K8S_AUTH_VERIFY_SSL'])),
            api_key=dict(type='str', no_log=True, fallback=(env_fallback, ['K8S_AUTH_API_KEY']))
        ),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("plugin_path",)),
            ("state", "absent", ("plugin_name",)),
        ],
        mutually_exclusive=[
            ('plugin_name', 'plugin_path'),
            ("context", "ca_cert"),
            ("context", "validate_certs"),
            ("kubeconfig", "ca_cert"),
            ("kubeconfig", "validate_certs")
        ],
    )

    bin_path = module.params.get('binary_path')
    state = module.params.get('state')

    if bin_path is not None:
        helm_cmd_common = bin_path
    else:
        helm_cmd_common = 'helm'

    helm_cmd_common = module.get_bin_path(helm_cmd_common, required=True)

    helm_cmd_common += " plugin"

    if state == 'present':
        helm_cmd_common += " install %s" % module.params.get('plugin_path')
        if not module.check_mode:
            rc, out, err = run_helm(module, helm_cmd_common, fails_on_error=False)
        else:
            rc, out, err = (0, '', '')

        if rc == 1 and 'plugin already exists' in err:
            module.exit_json(
                failed=False,
                changed=False,
                msg="Plugin already exists",
                command=helm_cmd_common,
                stdout=out,
                stderr=err,
                rc=rc
            )
        elif rc == 0:
            module.exit_json(
                failed=False,
                changed=True,
                msg="Plugin installed successfully",
                command=helm_cmd_common,
                stdout=out,
                stderr=err,
                rc=rc,
            )
        else:
            module.fail_json(
                msg="Failure when executing Helm command.",
                command=helm_cmd_common,
                stdout=out,
                stderr=err,
                rc=rc,
            )
    elif state == 'absent':
        plugin_name = module.params.get('plugin_name')
        helm_plugin_list = helm_cmd_common + " list"
        rc, out, err = run_helm(module, helm_plugin_list)
        if rc != 0 or (out == '' and err == ''):
            module.fail_json(
                msg="Failed to get Helm plugin info",
                command=helm_plugin_list,
                stdout=out,
                stderr=err,
                rc=rc,
            )

        if out:
            found = False
            for line in out.splitlines():
                if line.startswith("NAME"):
                    continue
                name, dummy, dummy = line.split('\t', 3)
                name = name.strip()
                if name == plugin_name:
                    found = True
                    break
            if found:
                helm_uninstall_cmd = "%s uninstall %s" % (helm_cmd_common, plugin_name)
                if not module.check_mode:
                    rc, out, err = run_helm(module, helm_uninstall_cmd, fails_on_error=False)
                else:
                    rc, out, err = (0, '', '')

                if rc == 0:
                    module.exit_json(
                        changed=True,
                        msg="Plugin uninstalled successfully",
                        command=helm_uninstall_cmd,
                        stdout=out,
                        stderr=err,
                        rc=rc
                    )
                module.fail_json(
                    msg="Failed to get Helm plugin uninstall",
                    command=helm_uninstall_cmd,
                    stdout=out,
                    stderr=err,
                    rc=rc,
                )
            else:
                module.exit_json(
                    failed=False,
                    changed=False,
                    msg="Plugin not found or is already uninstalled",
                    command=helm_plugin_list,
                    stdout=out,
                    stderr=err,
                    rc=rc
                )


if __name__ == '__main__':
    main()
