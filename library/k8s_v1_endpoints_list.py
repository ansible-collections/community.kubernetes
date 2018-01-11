#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.k8s_common import KubernetesAnsibleModule, KubernetesAnsibleException

DOCUMENTATION = '''
module: k8s_v1_endpoints_list
short_description: Kubernetes EndpointsList
description:
- Retrieve a list of endpoints. List operations provide a snapshot read of the underlying
  objects, returning a resource_version representing a consistent version of the listed
  objects.
version_added: 2.3.0
author: OpenShift (@openshift)
options:
  api_key:
    description:
    - Token used to connect to the API.
  cert_file:
    description:
    - Path to a certificate used to authenticate with the API.
    type: path
  context:
    description:
    - The name of a context found in the Kubernetes config file.
  debug:
    description:
    - Enable debug output from the OpenShift helper. Logging info is written to KubeObjHelper.log
    default: false
    type: bool
  force:
    description:
    - If set to C(True), and I(state) is C(present), an existing object will updated,
      and lists will be replaced, rather than merged.
    default: false
    type: bool
  host:
    description:
    - Provide a URL for acessing the Kubernetes API.
  key_file:
    description:
    - Path to a key file used to authenticate with the API.
    type: path
  kubeconfig:
    description:
    - Path to an existing Kubernetes config file. If not provided, and no other connection
      options are provided, the openshift client will attempt to load the default
      configuration file from I(~/.kube/config.json).
    type: path
  password:
    description:
    - Provide a password for connecting to the API. Use in conjunction with I(username).
  resource_definition:
    description:
    - Provide the YAML definition for the object, bypassing any modules parameters
      intended to define object attributes.
    type: dict
  src:
    description:
    - Provide a path to a file containing the YAML definition of the object. Mutually
      exclusive with I(resource_definition).
    type: path
  ssl_ca_cert:
    description:
    - Path to a CA certificate used to authenticate with the API.
    type: path
  state:
    description:
    - Determines if an object should be created, patched, or deleted. When set to
      C(present), the object will be created, if it does not exist, or patched, if
      parameter values differ from the existing object's attributes, and deleted,
      if set to C(absent). A patch operation results in merging lists and updating
      dictionaries, with lists being merged into a unique set of values. If a list
      contains a dictionary with a I(name) or I(type) attribute, a strategic merge
      is performed, where individual elements with a matching I(name_) or I(type)
      are merged. To force the replacement of lists, set the I(force) option to C(True).
    default: present
    choices:
    - present
    - absent
  username:
    description:
    - Provide a username for connecting to the API.
  verify_ssl:
    description:
    - Whether or not to verify the API server's SSL certificates.
    type: bool
requirements:
- kubernetes == 4.0.0
'''

EXAMPLES = '''
'''

RETURN = '''
api_version:
  description: Requested API version
  type: string
endpoints_list:
  type: complex
  returned: when I(state) = C(present)
  contains:
    api_version:
      description:
      - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values.
      type: str
    items:
      description:
      - List of endpoints.
      type: list
      contains:
        api_version:
          description:
          - APIVersion defines the versioned schema of this representation of an object.
            Servers should convert recognized schemas to the latest internal value,
            and may reject unrecognized values.
          type: str
        kind:
          description:
          - Kind is a string value representing the REST resource this object represents.
            Servers may infer this from the endpoint the client submits requests to.
            Cannot be updated. In CamelCase.
          type: str
        metadata:
          description:
          - Standard object's metadata.
          type: complex
        subsets:
          description:
          - The set of all endpoints is the union of all subsets. Addresses are placed
            into subsets according to the IPs they share. A single address with multiple
            ports, some of which are ready and some of which are not (because they
            come from different containers) will result in the address being displayed
            in different subsets for the different ports. No address will appear in
            both Addresses and NotReadyAddresses in the same subset. Sets of addresses
            and ports that comprise a service.
          type: list
          contains:
            addresses:
              description:
              - IP addresses which offer the related ports that are marked as ready.
                These endpoints should be considered safe for load balancers and clients
                to utilize.
              type: list
              contains:
                hostname:
                  description:
                  - The Hostname of this endpoint
                  type: str
                ip:
                  description:
                  - The IP of this endpoint. May not be loopback (127.0.0.0/8), link-local
                    (169.254.0.0/16), or link-local multicast ((224.0.0.0/24). IPv6
                    is also accepted but not fully supported on all platforms. Also,
                    certain kubernetes components, like kube-proxy, are not IPv6 ready.
                  type: str
                node_name:
                  description:
                  - 'Optional: Node hosting this endpoint. This can be used to determine
                    endpoints local to a node.'
                  type: str
                target_ref:
                  description:
                  - Reference to object providing the endpoint.
                  type: complex
            not_ready_addresses:
              description:
              - IP addresses which offer the related ports but are not currently marked
                as ready because they have not yet finished starting, have recently
                failed a readiness check, or have recently failed a liveness check.
              type: list
              contains:
                hostname:
                  description:
                  - The Hostname of this endpoint
                  type: str
                ip:
                  description:
                  - The IP of this endpoint. May not be loopback (127.0.0.0/8), link-local
                    (169.254.0.0/16), or link-local multicast ((224.0.0.0/24). IPv6
                    is also accepted but not fully supported on all platforms. Also,
                    certain kubernetes components, like kube-proxy, are not IPv6 ready.
                  type: str
                node_name:
                  description:
                  - 'Optional: Node hosting this endpoint. This can be used to determine
                    endpoints local to a node.'
                  type: str
                target_ref:
                  description:
                  - Reference to object providing the endpoint.
                  type: complex
            ports:
              description:
              - Port numbers available on the related IP addresses.
              type: list
              contains:
                name:
                  description:
                  - The name of this port (corresponds to ServicePort.Name). Must
                    be a DNS_LABEL. Optional only if one port is defined.
                  type: str
                port:
                  description:
                  - The port number of the endpoint.
                  type: int
                protocol:
                  description:
                  - The IP protocol for this port. Must be UDP or TCP. Default is
                    TCP.
                  type: str
    kind:
      description:
      - Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to. Cannot
        be updated. In CamelCase.
      type: str
    metadata:
      description:
      - Standard list metadata.
      type: complex
'''


def main():
    try:
        module = KubernetesAnsibleModule('endpoints_list', 'v1')
    except KubernetesAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except KubernetesAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
