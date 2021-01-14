#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: helm_repository

short_description: Manage Helm repositories.

version_added: "0.11.0"

author:
  - Lucas Boisserie (@LucasBoisserie)

requirements:
  - "helm (https://github.com/helm/helm/releases)"
  - "yaml (https://pypi.org/project/PyYAML/)"

description:
  -  Manage Helm repositories.

options:
  binary_path:
    description:
      - The path of a helm binary to use.
    required: false
    type: path
  repo_name:
    description:
      - Chart repository name.
    required: true
    type: str
    aliases: [ name ]
  repo_url:
    description:
      - Chart repository url
    type: str
    aliases: [ url ]
  repo_username:
    description:
      - Chart repository username for repository with basic auth.
      - Required if chart_repo_password is specified.
    required: false
    type: str
    aliases: [ username ]
  repo_password:
    description:
      - Chart repository password for repository with basic auth.
      - Required if chart_repo_username is specified.
    required: false
    type: str
    aliases: [ password ]
  repo_state:
    choices: ['present', 'absent']
    description:
      - Desired state of repository.
    required: false
    default: present
    aliases: [ state ]
    type: str
'''

EXAMPLES = r'''
- name: Add a repository
  community.kubernetes.helm_repository:
    name: stable
    repo_url: https://kubernetes.github.io/ingress-nginx

- name: Add Red Hat Helm charts repository
  community.kubernetes.helm_repository:
    name: redhat-charts
    repo_url: https://redhat-developer.github.com/redhat-helm-charts
'''

RETURN = r'''
stdout:
  type: str
  description: Full `helm` command stdout, in case you want to display it or examine the event log
  returned: always
  sample: '"bitnami" has been added to your repositories'
stdout_lines:
  type: list
  description: Full `helm` command stdout in list, in case you want to display it or examine the event log
  returned: always
  sample: ["\"bitnami\" has been added to your repositories"]
stderr:
  type: str
  description: Full `helm` command stderr, in case you want to display it or examine the event log
  returned: always
  sample: ''
stderr_lines:
  type: list
  description: Full `helm` command stderr in list, in case you want to display it or examine the event log
  returned: always
  sample: [""]
command:
  type: str
  description: Full `helm` command built by this module, in case you want to re-run the command outside the module or debug a problem.
  returned: always
  sample: '/usr/local/bin/helm repo add bitnami https://charts.bitnami.com/bitnami'
msg:
  type: str
  description: Error message returned by `helm` command
  returned: on failure
  sample: 'Repository already have a repository named bitnami'
'''

import traceback

try:
    import yaml
    IMP_YAML = True
except ImportError:
    IMP_YAML_ERR = traceback.format_exc()
    IMP_YAML = False

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.community.kubernetes.plugins.module_utils.helm import run_helm


# Get repository from all repositories added
def get_repository(state, repo_name):
    if state is not None:
        for repository in state:
            if repository['name'] == repo_name:
                return repository
    return None


# Get repository status
def get_repository_status(module, command, repository_name):
    list_command = command + " repo list --output=yaml"

    rc, out, err = run_helm(module, list_command, fails_on_error=False)

    # no repo => rc=1 and 'no repositories to show' in output
    if rc == 1 and "no repositories to show" in err:
        return None
    elif rc != 0:
        module.fail_json(
            msg="Failure when executing Helm command. Exited {0}.\nstdout: {1}\nstderr: {2}".format(rc, out, err),
            command=list_command
        )

    return get_repository(yaml.safe_load(out), repository_name)


# Install repository
def install_repository(command, repository_name, repository_url, repository_username, repository_password):
    install_command = command + " repo add " + repository_name + " " + repository_url

    if repository_username is not None and repository_password is not None:
        install_command += " --username=" + repository_username
        install_command += " --password=" + repository_password

    return install_command


# Delete repository
def delete_repository(command, repository_name):
    remove_command = command + " repo rm " + repository_name

    return remove_command


def main():
    global module

    module = AnsibleModule(
        argument_spec=dict(
            binary_path=dict(type='path'),
            repo_name=dict(type='str', aliases=['name'], required=True),
            repo_url=dict(type='str', aliases=['url']),
            repo_username=dict(type='str', aliases=['username']),
            repo_password=dict(type='str', aliases=['password'], no_log=True),
            repo_state=dict(default='present', choices=['present', 'absent'], aliases=['state']),
        ),
        required_together=[
            ['repo_username', 'repo_password']
        ],
        required_if=[
            ('repo_state', 'present', ['repo_url']),
        ],
        supports_check_mode=True,
    )

    if not IMP_YAML:
        module.fail_json(msg=missing_required_lib("yaml"), exception=IMP_YAML_ERR)

    changed = False

    bin_path = module.params.get('binary_path')
    repo_name = module.params.get('repo_name')
    repo_url = module.params.get('repo_url')
    repo_username = module.params.get('repo_username')
    repo_password = module.params.get('repo_password')
    repo_state = module.params.get('repo_state')

    if bin_path is not None:
        helm_cmd = bin_path
    else:
        helm_cmd = module.get_bin_path('helm', required=True)

    repository_status = get_repository_status(module, helm_cmd, repo_name)

    if repo_state == "absent" and repository_status is not None:
        helm_cmd = delete_repository(helm_cmd, repo_name)
        changed = True
    elif repo_state == "present":
        if repository_status is None:
            helm_cmd = install_repository(helm_cmd, repo_name, repo_url, repo_username, repo_password)
            changed = True
        elif repository_status['url'] != repo_url:
            module.fail_json(msg="Repository already have a repository named {0}".format(repo_name))

    if module.check_mode:
        module.exit_json(changed=changed)
    elif not changed:
        module.exit_json(changed=False, repo_name=repo_name, repo_url=repo_url)

    rc, out, err = run_helm(module, helm_cmd)

    if repo_password is not None:
        helm_cmd = helm_cmd.replace(repo_password, '******')

    if rc != 0:
        module.fail_json(
            msg="Failure when executing Helm command. Exited {0}.\nstdout: {1}\nstderr: {2}".format(rc, out, err),
            command=helm_cmd
        )

    module.exit_json(changed=changed, stdout=out, stderr=err, command=helm_cmd)


if __name__ == '__main__':
    main()
