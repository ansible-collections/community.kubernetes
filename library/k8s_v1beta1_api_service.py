#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.k8s_common import KubernetesAnsibleModule, KubernetesAnsibleException

DOCUMENTATION = '''
module: k8s_v1beta1_api_service
short_description: Kubernetes APIService
description:
- Manage the lifecycle of a api_service object. Supports check mode, and attempts
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
  spec_ca_bundle:
    description:
    - CABundle is a PEM encoded CA bundle which will be used to validate an API server's
      serving certificate.
    aliases:
    - ca_bundle
  spec_group:
    description:
    - Group is the API group name this server hosts
    aliases:
    - group
  spec_group_priority_minimum:
    description:
    - "GroupPriorityMininum is the priority this group should have at least. Higher\
      \ priority means that the group is prefered by clients over lower priority ones.\
      \ Note that other versions of this group might specify even higher GroupPriorityMininum\
      \ values such that the whole group gets a higher priority. The primary sort\
      \ is based on GroupPriorityMinimum, ordered highest number to lowest (20 before\
      \ 10). The secondary sort is based on the alphabetical comparison of the name\
      \ of the object. (v1.bar before v1.foo) We'd recommend something like: *.k8s.io\
      \ (except extensions) at 18000 and PaaSes (OpenShift, Deis) are recommended\
      \ to be in the 2000s"
    aliases:
    - group_priority_minimum
    type: int
  spec_insecure_skip_tls_verify:
    description:
    - InsecureSkipTLSVerify disables TLS certificate verification when communicating
      with this server. This is strongly discouraged. You should use the CABundle
      instead.
    aliases:
    - insecure_skip_tls_verify
    type: bool
  spec_service_name:
    description:
    - Name is the name of the service
    aliases:
    - service_name
  spec_service_namespace:
    description:
    - Namespace is the namespace of the service
    aliases:
    - service_namespace
  spec_version:
    description:
    - Version is the API version this server hosts. For example, "v1"
    aliases:
    - version
  spec_version_priority:
    description:
    - VersionPriority controls the ordering of this API version inside of its group.
      Must be greater than zero. The primary sort is based on VersionPriority, ordered
      highest to lowest (20 before 10). The secondary sort is based on the alphabetical
      comparison of the name of the object. (v1.bar before v1.foo) Since it's inside
      of a group, the number can be small, probably in the 10s.
    aliases:
    - version_priority
    type: int
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
api_service:
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
      description: []
      type: complex
    spec:
      description:
      - Spec contains information for locating and communicating with a server
      type: complex
    status:
      description:
      - Status contains derived information about an API server
      type: complex
'''


def main():
    try:
        module = KubernetesAnsibleModule('api_service', 'v1beta1')
    except KubernetesAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except KubernetesAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
