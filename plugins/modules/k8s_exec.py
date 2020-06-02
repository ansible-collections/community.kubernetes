#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r'''

module: k8s_exec

short_description: Execute command in Pod

version_added: "0.10.0"

author: "Tristan de Cacqueray (@tristanC)"

description:
  - Use the Kubernetes Python client to execute command on K8s pods.

extends_documentation_fragment:
  - community.kubernetes.k8s_auth_options

requirements:
  - "python >= 2.7"
  - "openshift == 0.4.3"
  - "PyYAML >= 3.11"

options:
  proxy:
    description:
    - The URL of an HTTP proxy to use for the connection. Can also be specified via K8S_AUTH_PROXY environment variable.
    - Please note that this module does not pick up typical proxy settings from the environment (e.g. HTTP_PROXY).
    type: str
  namespace:
    description:
    - The pod namespace name
    type: str
    required: yes
  pod:
    description:
    - The pod name
    type: str
    required: yes
  container:
    description:
    - The name of the container in the pod to connect to. Defaults to only container if there is only one container in the pod.
    type: str
    required: no
  command:
    description:
    - The command to execute
    type: str
    required: yes
'''

EXAMPLES = r'''
- name: Execute a command
  community.kubernetes.k8s_exec:
    namespace: myproject
    pod: zuul-scheduler
    command: zuul-scheduler full-reconfigure
'''

RETURN = r'''
result:
  description:
  - The command object
  returned: success
  type: complex
  contains:
     stdout:
       description: The command stdout
       type: str
     stdout_lines:
       description: The command stdout
       type: str
     stderr:
       description: The command stderr
       type: str
     stderr_lines:
       description: The command stderr
       type: str
'''

import copy
import shlex
from ansible_collections.community.kubernetes.plugins.module_utils.common import KubernetesAnsibleModule
from ansible_collections.community.kubernetes.plugins.module_utils.common import AUTH_ARG_SPEC

try:
    from kubernetes.client.apis import core_v1_api
    from kubernetes.stream import stream
except ImportError:
    # ImportError are managed by the common module already.
    pass


class KubernetesExecCommand(KubernetesAnsibleModule):
    @property
    def argspec(self):
        spec = copy.deepcopy(AUTH_ARG_SPEC)
        spec['namespace'] = dict(type='str', required=True)
        spec['pod'] = dict(type='str', required=True)
        spec['container'] = dict(type='str')
        spec['command'] = dict(type='str', required=True)
        return spec


def main():
    module = KubernetesExecCommand()
    # Load kubernetes.client.Configuration
    module.get_api_client()
    api = core_v1_api.CoreV1Api()

    # hack because passing the container as None breaks things
    optional_kwargs = {}
    if module.params.get('container'):
        optional_kwargs['container'] = module.params['container']
    resp = stream(
        api.connect_get_namespaced_pod_exec,
        module.params["pod"],
        module.params["namespace"],
        command=shlex.split(module.params["command"]),
        stdout=True,
        stderr=True,
        stdin=False,
        tty=False,
        _preload_content=False, **optional_kwargs)
    stdout, stderr = [], []
    while resp.is_open():
        resp.update(timeout=1)
        if resp.peek_stdout():
            stdout.append(resp.read_stdout())
        if resp.peek_stderr():
            stderr.append(resp.read_stderr())
    module.exit_json(
        changed=True, stdout="".join(stdout), stderr="".join(stderr))


if __name__ == '__main__':
    main()
