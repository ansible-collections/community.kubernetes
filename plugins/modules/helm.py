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
module: helm

short_description: Manages Kubernetes packages with the Helm package manager

author:
  - Lucas Boisserie (@LucasBoisserie)
  - Matthieu Diehr (@d-matt)

requirements:
  - "helm (https://github.com/helm/helm/releases)"
  - "yaml (https://pypi.org/project/PyYAML/)"

description:
  - Install, upgrade, delete packages with the Helm package manager.

options:
  binary_path:
    description:
      - The path of a helm binary to use.
    required: false
    type: path
  chart_ref:
    description:
      - chart_reference on chart repository.
      - path to a packaged chart.
      - path to an unpacked chart directory.
      - absolute URL.
      - Required when I(release_state) is set to C(present).
    required: false
    type: path
  chart_repo_url:
    description:
      - Chart repository URL where to locate the requested chart.
    required: false
    type: str
  chart_version:
    description:
      - Chart version to install. If this is not specified, the latest version is installed.
    required: false
    type: str
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
  release_state:
    choices: ['present', 'absent']
    description:
      - Desirated state of release.
    required: false
    default: present
    aliases: [ state ]
    type: str
  release_values:
    description:
        - Value to pass to chart.
    required: false
    default: {}
    aliases: [ values ]
    type: dict
  update_repo_cache:
    description:
      - Run C(helm repo update) before the operation. Can be run as part of the package installation or as a separate step.
    default: false
    type: bool

#Helm options
  disable_hook:
    description:
      - Helm option to disable hook on install/upgrade/delete.
    default: False
    type: bool
  force:
    description:
      - Helm option to force reinstall, ignore on new install.
    default: False
    type: bool
  kube_context:
    description:
      - Helm option to specify which kubeconfig context to use.
    type: str
  kubeconfig_path:
    description:
      - Helm option to specify kubeconfig path to use.
    type: path
    aliases: [ kubeconfig ]
  purge:
    description:
      - Remove the release from the store and make its name free for later use.
    default: True
    type: bool
  wait:
    description:
      - Wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment are in a ready state before marking the release as successful.
    default: False
    type: bool
  wait_timeout:
    description:
      - Timeout when wait option is enabled (helm2 is a number of seconds, helm3 is a duration).
    type: str
'''

EXAMPLES = '''
- name: Create helm namespace as HELM 3 doesn't create it automatically
  k8s:
    api_version: v1
    kind: Namespace
    name: "monitoring"
    wait: true

# From repository
- name: Add stable chart repo
  helm_repository:
    name: stable
    repo_url: "https://kubernetes-charts.storage.googleapis.com"

- name: Deploy latest version of Grafana chart inside monitoring namespace with values
  helm:
    name: test
    chart_ref: stable/grafana
    release_namespace: monitoring
    values:
      replicas: 2

- name: Deploy Grafana chart on 5.0.12 with values loaded from template
  helm:
    name: test
    chart_ref: stable/grafana
    chart_version: 5.0.12
    values: "{{ lookup('template', 'somefile.yaml') | from_yaml }}"

- name: Remove test release and waiting suppression ending
  helm:
    name: test
    state: absent
    wait: true

# From git
- name: Git clone stable repo on HEAD
  git:
    repo: "http://github.com/helm/charts.git"
    dest: /tmp/helm_repo

- name: Deploy Grafana chart from local path
  helm:
    name: test
    chart_ref: /tmp/helm_repo/stable/grafana
    release_namespace: monitoring

# From url
- name: Deploy Grafana chart on 5.0.12 from url
  helm:
    name: test
    chart_ref: "https://kubernetes-charts.storage.googleapis.com/grafana-5.0.12.tgz"
    release_namespace: monitoring
'''

RETURN = """
status:
  type: complex
  description: A dictionary of status output
  returned: on success Creation/Upgrade/Already deploy
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
  sample: helm upgrade ...
"""

import traceback

try:
    import yaml
    IMP_YAML = True
except ImportError:
    IMP_YAML_ERR = traceback.format_exc()
    IMP_YAML = False

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

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


# Run Repo update
def run_repo_update(command):
    repo_update_command = command + " repo update"

    rc, out, err = module.run_command(repo_update_command)
    if rc != 0:
        module.fail_json(
            msg="Failure when executing Helm command. Exited {0}.\nstdout: {1}\nstderr: {2}".format(rc, out, err),
            command=repo_update_command
        )


# Get chart info
def fetch_chart_info(command, chart_ref):
    inspect_command = command + " show chart " + chart_ref

    rc, out, err = module.run_command(inspect_command)
    if rc != 0:
        module.fail_json(
            msg="Failure when executing Helm command. Exited {0}.\nstdout: {1}\nstderr: {2}".format(rc, out, err),
            command=inspect_command
        )

    return yaml.safe_load(out)


# Install/upgrade/rollback release chart
def deploy(command, release_name, release_values, chart_name, wait, wait_timeout, disable_hook, force):
    deploy_command = command + " upgrade -i"  # install/upgrade

    # Always reset values to keep release_values equal to values released
    deploy_command += " --reset-values"

    if wait:
        deploy_command += " --wait"
        if wait_timeout is not None:
            deploy_command += " --timeout " + wait_timeout

    if force:
        deploy_command += " --force"

    if disable_hook:
        deploy_command += " --no-hooks"

    if release_values != {}:
        try:
            import tempfile
        except ImportError:
            module.fail_json(msg=missing_required_lib("tempfile"), exception=traceback.format_exc())

        fd, path = tempfile.mkstemp(suffix='.yml')
        with open(path, 'w') as yaml_file:
            yaml.dump(release_values, yaml_file, default_flow_style=False)
        deploy_command += " -f=" + path

    deploy_command += " " + release_name + " " + chart_name

    return deploy_command


# Delete release chart
def delete(command, release_name, purge, disable_hook):
    delete_command = command + " uninstall "

    if not purge:
        delete_command += " --keep-history"

    if disable_hook:
        delete_command += " --no-hooks"

    delete_command += " " + release_name

    return delete_command


def main():
    global module
    module = AnsibleModule(
        argument_spec=dict(
            binary_path=dict(type='path'),
            chart_ref=dict(type='path'),
            chart_repo_url=dict(type='str'),
            chart_version=dict(type='str'),
            release_name=dict(type='str', required=True, aliases=['name']),
            release_namespace=dict(type='str', required=True, aliases=['namespace']),
            release_state=dict(default='present', choices=['present', 'absent'], aliases=['state']),
            release_values=dict(type='dict', default={}, aliases=['values']),
            update_repo_cache=dict(type='bool', default=False),

            # Helm options
            disable_hook=dict(type='bool', default=False),
            force=dict(type='bool', default=False),
            kube_context=dict(type='str'),
            kubeconfig_path=dict(type='path', aliases=['kubeconfig']),
            purge=dict(type='bool', default=True),
            wait=dict(type='bool', default=False),
            wait_timeout=dict(type='str'),
        ),
        required_if=[
            ('release_state', 'present', ['release_name', 'chart_ref']),
            ('release_state', 'absent', ['release_name'])
        ],
        supports_check_mode=True,
    )

    if not IMP_YAML:
        module.fail_json(msg=missing_required_lib("yaml"), exception=IMP_YAML_ERR)

    changed = False

    bin_path = module.params.get('binary_path')
    chart_ref = module.params.get('chart_ref')
    chart_repo_url = module.params.get('chart_repo_url')
    chart_version = module.params.get('chart_version')
    release_name = module.params.get('release_name')
    release_namespace = module.params.get('release_namespace')
    release_state = module.params.get('release_state')
    release_values = module.params.get('release_values')
    update_repo_cache = module.params.get('update_repo_cache')

    # Helm options
    disable_hook = module.params.get('disable_hook')
    force = module.params.get('force')
    kube_context = module.params.get('kube_context')
    kubeconfig_path = module.params.get('kubeconfig_path')
    purge = module.params.get('purge')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    if bin_path is not None:
        helm_cmd_common = bin_path
    else:
        helm_cmd_common = module.get_bin_path('helm', required=True)

    if kube_context is not None:
        helm_cmd_common += " --kube-context " + kube_context

    if kubeconfig_path is not None:
        helm_cmd_common += " --kubeconfig " + kubeconfig_path

    if update_repo_cache:
        run_repo_update(helm_cmd_common)

    helm_cmd_common += " --namespace=" + release_namespace

    # Get real/deployed release status
    release_status = get_release_status(helm_cmd_common, release_name)

    # keep helm_cmd_common for get_release_status in module_exit_json
    helm_cmd = helm_cmd_common
    if release_state == "absent" and release_status is not None:
        helm_cmd = delete(helm_cmd, release_name, purge, disable_hook)
        changed = True
    elif release_state == "present":

        if chart_version is not None:
            helm_cmd += " --version=" + chart_version

        if chart_repo_url is not None:
            helm_cmd += " --repo=" + chart_repo_url

        # Fetch chart info to have real version and real name for chart_ref from archive, folder or url
        chart_info = fetch_chart_info(helm_cmd, chart_ref)

        if release_status is None:  # Not installed
            helm_cmd = deploy(helm_cmd, release_name, release_values, chart_ref, wait, wait_timeout,
                              disable_hook, False)
            changed = True

        elif force or release_values != release_status['values'] \
                or (chart_info['name'] + '-' + chart_info['version']) != release_status["chart"]:
            helm_cmd = deploy(helm_cmd, release_name, release_values, chart_ref, wait, wait_timeout,
                              disable_hook, force)
            changed = True

    if module.check_mode:
        module.exit_json(changed=changed)
    elif not changed:
        module.exit_json(changed=False, status=release_status)

    rc, out, err = module.run_command(helm_cmd)

    if rc != 0:
        module.fail_json(
            msg="Failure when executing Helm command. Exited {0}.\nstdout: {1}\nstderr: {2}".format(rc, out, err),
            command=helm_cmd
        )

    module.exit_json(changed=changed, stdout=out, stderr=err,
                     status=get_release_status(helm_cmd_common, release_name), command=helm_cmd)


if __name__ == '__main__':
    main()
