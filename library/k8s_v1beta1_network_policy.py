#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.k8s_common import KubernetesAnsibleModule, KubernetesAnsibleException

DOCUMENTATION = '''
module: k8s_v1beta1_network_policy
short_description: Kubernetes NetworkPolicy
description:
- Manage the lifecycle of a network_policy object. Supports check mode, and attempts
  to to be idempotent.
version_added: 2.3.0
author: OpenShift (@openshift)
options:
  annotations:
    description:
    - Annotations is an unstructured key value map stored with a resource that may
      be set by external tools to store and retrieve arbitrary metadata. They are
      not queryable and should be preserved when modifying objects.
    type: dict
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
  labels:
    description:
    - Map of string keys and values that can be used to organize and categorize (scope
      and select) objects. May match selectors of replication controllers and services.
    type: dict
  name:
    description:
    - Name must be unique within a namespace. Is required when creating resources,
      although some resources may allow a client to request the generation of an appropriate
      name automatically. Name is primarily intended for creation idempotence and
      configuration definition. Cannot be updated.
  namespace:
    description:
    - Namespace defines the space within each name must be unique. An empty namespace
      is equivalent to the "default" namespace, but "default" is the canonical representation.
      Not all objects are required to be scoped to a namespace - the value of this
      field for those objects will be empty. Must be a DNS_LABEL. Cannot be updated.
  password:
    description:
    - Provide a password for connecting to the API. Use in conjunction with I(username).
  resource_definition:
    description:
    - Provide the YAML definition for the object, bypassing any modules parameters
      intended to define object attributes.
    type: dict
  spec_egress:
    description:
    - List of egress rules to be applied to the selected pods. Outgoing traffic is
      allowed if there are no NetworkPolicies selecting the pod (and cluster policy
      otherwise allows the traffic), OR if the traffic matches at least one egress
      rule across all of the NetworkPolicy objects whose podSelector matches the pod.
      If this field is empty then this NetworkPolicy limits all outgoing traffic (and
      serves solely to ensure that the pods it selects are isolated by default). This
      field is beta-level in 1.8
    aliases:
    - egress
    type: list
  spec_ingress:
    description:
    - List of ingress rules to be applied to the selected pods. Traffic is allowed
      to a pod if there are no NetworkPolicies selecting the pod OR if the traffic
      source is the pod's local node, OR if the traffic matches at least one ingress
      rule across all of the NetworkPolicy objects whose podSelector matches the pod.
      If this field is empty then this NetworkPolicy does not allow any traffic (and
      serves solely to ensure that the pods it selects are isolated by default).
    aliases:
    - ingress
    type: list
  spec_pod_selector_match_expressions:
    description:
    - matchExpressions is a list of label selector requirements. The requirements
      are ANDed.
    aliases:
    - pod_selector_match_expressions
    type: list
  spec_pod_selector_match_labels:
    description:
    - matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels
      map is equivalent to an element of matchExpressions, whose key field is "key",
      the operator is "In", and the values array contains only "value". The requirements
      are ANDed.
    aliases:
    - pod_selector_match_labels
    type: dict
  spec_policy_types:
    description:
    - List of rule types that the NetworkPolicy relates to. Valid options are Ingress,
      Egress, or Ingress,Egress. If this field is not specified, it will default based
      on the existence of Ingress or Egress rules; policies that contain an Egress
      section are assumed to affect Egress, and all policies (whether or not they
      contain an Ingress section) are assumed to affect Ingress. If you want to write
      an egress-only policy, you must explicitly specify policyTypes [ "Egress" ].
      Likewise, if you want to write a policy that specifies that no egress is allowed,
      you must specify a policyTypes value that include "Egress" (since such a policy
      would not include an Egress section and would otherwise default to just [ "Ingress"
      ]). This field is beta-level in 1.8
    aliases:
    - policy_types
    type: list
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
network_policy:
  type: complex
  returned: when I(state) = C(present)
  contains:
    api_version:
      description:
      - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values.
      type: str
    kind:
      description:
      - Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to. Cannot
        be updated. In CamelCase.
      type: str
    metadata:
      description:
      - Standard object's metadata.
      type: complex
    spec:
      description:
      - Specification of the desired behavior for this NetworkPolicy.
      type: complex
'''


def main():
    try:
        module = KubernetesAnsibleModule('network_policy', 'v1beta1')
    except KubernetesAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except KubernetesAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
