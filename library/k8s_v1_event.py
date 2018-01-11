#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.k8s_common import KubernetesAnsibleModule, KubernetesAnsibleException

DOCUMENTATION = '''
module: k8s_v1_event
short_description: Kubernetes Event
description:
- Manage the lifecycle of a event object. Supports check mode, and attempts to to
  be idempotent.
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
  count:
    description:
    - The number of times this event has occurred.
    type: int
  debug:
    description:
    - Enable debug output from the OpenShift helper. Logging info is written to KubeObjHelper.log
    default: false
    type: bool
  first_timestamp:
    description:
    - The time at which the event was first recorded. (Time of server receipt is in
      TypeMeta.)
  force:
    description:
    - If set to C(True), and I(state) is C(present), an existing object will updated,
      and lists will be replaced, rather than merged.
    default: false
    type: bool
  host:
    description:
    - Provide a URL for acessing the Kubernetes API.
  involved_object_api_version:
    description:
    - API version of the referent.
    aliases:
    - api_version
  involved_object_field_path:
    description:
    - 'If referring to a piece of an object instead of an entire object, this string
      should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2].
      For example, if the object reference is to a container within a pod, this would
      take on a value like: "spec.containers{name}" (where "name" refers to the name
      of the container that triggered the event) or if no container name is specified
      "spec.containers[2]" (container with index 2 in this pod). This syntax is chosen
      only to have some well-defined way of referencing a part of an object.'
    aliases:
    - field_path
  involved_object_kind:
    description:
    - Kind of the referent.
    aliases:
    - kind
  involved_object_name:
    description:
    - Name of the referent.
  involved_object_namespace:
    description:
    - Namespace of the referent.
  involved_object_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - resource_version
  involved_object_uid:
    description:
    - UID of the referent.
    aliases:
    - uid
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
  last_timestamp:
    description:
    - The time at which the most recent occurrence of this event was recorded.
  message:
    description:
    - A human-readable description of the status of this operation.
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
  reason:
    description:
    - This should be a short, machine understandable string that gives the reason
      for the transition into the object's current status.
  resource_definition:
    description:
    - Provide the YAML definition for the object, bypassing any modules parameters
      intended to define object attributes.
    type: dict
  source_component:
    description:
    - Component from which the event is generated.
    aliases:
    - component
  source_host:
    description:
    - Node name on which the event is generated.
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
  type:
    description:
    - Type of this event (Normal, Warning), new types could be added in the future
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
event:
  type: complex
  returned: when I(state) = C(present)
  contains:
    api_version:
      description:
      - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values.
      type: str
    count:
      description:
      - The number of times this event has occurred.
      type: int
    first_timestamp:
      description:
      - The time at which the event was first recorded. (Time of server receipt is
        in TypeMeta.)
      type: complex
      contains: {}
    involved_object:
      description:
      - The object that this event is about.
      type: complex
    kind:
      description:
      - Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to. Cannot
        be updated. In CamelCase.
      type: str
    last_timestamp:
      description:
      - The time at which the most recent occurrence of this event was recorded.
      type: complex
      contains: {}
    message:
      description:
      - A human-readable description of the status of this operation.
      type: str
    metadata:
      description:
      - Standard object's metadata.
      type: complex
    reason:
      description:
      - This should be a short, machine understandable string that gives the reason
        for the transition into the object's current status.
      type: str
    source:
      description:
      - The component reporting this event. Should be a short machine understandable
        string.
      type: complex
    type:
      description:
      - Type of this event (Normal, Warning), new types could be added in the future
      type: str
'''


def main():
    try:
        module = KubernetesAnsibleModule('event', 'v1')
    except KubernetesAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except KubernetesAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
