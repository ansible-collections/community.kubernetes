#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r'''
module: k8s_expose

short_description: Expose a resource as a new Kubernetes service. Roughly equivalent to kubectl expose.

version_added: "1.1.0"

author: "Fabian von Feilitzsch (@fabianvf)"

description:
  - Looks up a resource and creates a new service based on its selector.
  - Supported resources are deployments, services, replicasets, replication controllers and pods. (TODO: Investigate daemonsets/statefulsets)
  - Analogous to `kubectl expose`

extends_documentation_fragment:
  - community.kubernetes.k8s_auth_options
  - community.kubernetes.k8s_wait_options

requirements:
  - "python >= 2.7"
  - "openshift >= 0.11.0"
  - "PyYAML >= 3.11"

options:
  deployment:
    description:
      - The name of the deployment to expose.
      - Mutually exclusive with I(service), I(replicaset), I(replication_controller), I(pod)
    type: str
    aliases: ['deploy']
  service:
    description:
      - The name of the service to expose.
      - Mutually exclusive with I(deployment), I(replicaset), I(replication_controller), I(pod)
    type: str
    aliases: ['svc']
  replicaset:
    description:
      - The name of the replicaset to expose.
      - Mutually exclusive with I(deployment), I(service), I(replication_controller), I(pod)
    type: str
    aliases: ['rs']
  replication_controller:
    description:
      - The name of the replication controller to expose.
      - Mutually exclusive with I(deployment), I(service), I(replicaset), I(pod)
    type: str
    aliases: ['rc']
  pod:
    description:
      - The name of the pod to expose.
      - Mutually exclusive with I(deployment), I(service), I(replicaset), I(replication_controller)
    type: str
    aliases: ['po']
  namespace:
    description:
      - The namespace of the resource being targeted.
      - The Service will be created in this namespace as well.
    required: yes
    type: str
  cluster_ip:
    description:
      - Specify ClusterIP to be assigned to the service.
      - Leave empty to auto-allocate.
      - Set to `nil` to create a headless service.
    type: str
  external_ip:
    description:
      - Specify an external IP not managed by Kubernetes to accept for the service.
    type: str
  labels:
    description:
      - Specify the labels to apply to the created service.
      - A set of key: value pairs.
    type: dict
  load_balancer_ip:
    description:
      - Specify the IP to be assigned to the LoadBalancer service.
      - If I(type) is LoadBalancer and this field is not provided, an ephemeral IP will be created and used.
    type: str
  name:
    description:
      - The desired name of the Service to be created.
    type: str
  port:
    description:
      - The port that the Service will serve on.
      - Copied from the resource being exposed if unspecified
    type: str
  protocol:
    description:
      - The network protocol for the Service being created
    type: str
    default: TCP
    choices:
      - TCP
      - UDP
  selector:
    description:
      - A label selector to be used for this service.
      - Only equality-based selectors are supported.
      - If empty, selector will be inferred from the resource being exposed.
    type: str
  target_port:
    description:
      - Name or number for the port on the container that the Service should target.
    type: str
  type:
    description:
      - The type of Service to create.
    type: str
    default: ClusterIP
    choices:
      - ClusterIP
      - NodePort
      - LoadBalancer
      - ExternalName
'''

EXAMPLES = r'''
- name: Create a Service for an nginx deployment that connects port 80 to port 8000 in the container
  community.kubernetes.k8s_expose:
    deployment: nginx
    namespace: default
    port: '80'
    target_port: '8000'
  register: nginx_service

- name: Create a second service based on the above service, that connects port 443 to port 8443 in the container
  community.kubernetes.k8s_expose:
    service: '{{ nginx_service.result.metadata.name }}'
    namespace: default
    port: '443'
    target_port: '8443'
    name: nginx-https

- name: Create a service for a pod
  community.kubernetes.k8s_expose:
    pod: hello-world
    namespace: default
    name: hello-world
'''

RETURN = r'''
result:
  description:
  - The Service object that was created or updated
  returned: success
  type: complex
  contains:
    metadata:
      type: complex
    spec:
      type: complex
    status:
      type: complex
'''

import copy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.kubernetes.plugins.module_utils.common import (
    K8sAnsibleMixin, AUTH_ARG_SPEC, WAIT_ARG_SPEC
)


class KubernetesExpose(K8sAnsibleMixin):

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=self.argspec,
            supports_check_mode=True,
        )
        self.params = self.module.params
        self.fail_json = self.module.fail_json
        super(KubernetesExpose, self).__init__()

    @property
    def argspec(self):
        spec = copy.deepcopy(AUTH_ARG_SPEC)
        spec.update(copy.deepcopy(WAIT_ARG_SPEC))

        spec['deployment'] = dict(type='str', aliases=['deploy'])
        spec['service'] = dict(type='str', aliases=['svc'])
        spec['replicaset'] = dict(type='str', aliases=['rs'])
        spec['replication_controller'] = dict(type='str', aliases=['rc'])
        spec['pod'] = dict(type='str', aliases=['po'])

        spec['name'] = dict(type='str')
        spec['namespace'] = dict(required=True, type='str')
        spec['labels'] = dict(type='dict')
        spec['selector'] = dict(type='str')
        spec['type'] = dict(type='str', default='ClusterIP', choices=['ClusterIP', 'NodePort', 'LoadBalancer', 'ExternalName'])

        spec['cluster_ip'] = dict(type='str')
        spec['external_ip'] = dict(type='str')
        spec['load_balancer_ip'] = dict(type='str')

        spec['port'] = dict(type='str')
        spec['target_port'] = dict(type='str')
        spec['protocol'] = dict(type='str', default='TCP', choices=['TCP', 'UDP'])
        return spec

    def execute_module(self):
        raise NotImplementedError


def main():
    KubernetesExpose().execute_module()


if __name__ == '__main__':
    main()
