#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.openshift_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: openshift_v1beta1_event
short_description: OpenShift Event
description:
- Manage the lifecycle of a event object. Supports check mode, and attempts to to
  be idempotent.
version_added: 2.3.0
author: OpenShift (@openshift)
options:
  action:
    description:
    - What action was taken/failed regarding to the regarding object.
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
  deprecated_count:
    description:
    - Deprecated field assuring backward compatibility with core.v1 Event type
    type: int
  deprecated_first_timestamp:
    description:
    - Deprecated field assuring backward compatibility with core.v1 Event type
  deprecated_last_timestamp:
    description:
    - Deprecated field assuring backward compatibility with core.v1 Event type
  deprecated_source_component:
    description:
    - Component from which the event is generated.
    aliases:
    - component
  deprecated_source_host:
    description:
    - Node name on which the event is generated.
  event_time:
    description:
    - Required. Time when this Event was first observed.
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
  note:
    description:
    - Optional. A human-readable description of the status of this operation. Maximal
      length of the note is 1kB, but libraries should be prepared to handle values
      up to 64kB.
  password:
    description:
    - Provide a password for connecting to the API. Use in conjunction with I(username).
  reason:
    description:
    - Why the action was taken.
  regarding_api_version:
    description:
    - API version of the referent.
    aliases:
    - api_version
  regarding_field_path:
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
  regarding_kind:
    description:
    - Kind of the referent.
    aliases:
    - kind
  regarding_name:
    description:
    - Name of the referent.
  regarding_namespace:
    description:
    - Namespace of the referent.
  regarding_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - resource_version
  regarding_uid:
    description:
    - UID of the referent.
    aliases:
    - uid
  related_api_version:
    description:
    - API version of the referent.
  related_field_path:
    description:
    - 'If referring to a piece of an object instead of an entire object, this string
      should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2].
      For example, if the object reference is to a container within a pod, this would
      take on a value like: "spec.containers{name}" (where "name" refers to the name
      of the container that triggered the event) or if no container name is specified
      "spec.containers[2]" (container with index 2 in this pod). This syntax is chosen
      only to have some well-defined way of referencing a part of an object.'
  related_kind:
    description:
    - Kind of the referent.
  related_name:
    description:
    - Name of the referent.
  related_namespace:
    description:
    - Namespace of the referent.
  related_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
  related_uid:
    description:
    - UID of the referent.
  reporting_controller:
    description:
    - Name of the controller that emitted this Event, e.g. `kubernetes.io/kubelet`.
  reporting_instance:
    description:
    - ID of the controller instance, e.g. `kubelet-xyzf`.
  resource_definition:
    description:
    - Provide the YAML definition for the object, bypassing any modules parameters
      intended to define object attributes.
    type: dict
  series_count:
    description:
    - Number of occurrences in this series up to the last heartbeat time
    aliases:
    - count
    type: int
  series_last_observed_time:
    description:
    - Time when last Event from the series was seen before last heartbeat.
    aliases:
    - last_observed_time
  series_state:
    description:
    - Information whether this series is ongoing or finished.
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
    - Type of this event (Normal, Warning), new types could be added in the future.
  username:
    description:
    - Provide a username for connecting to the API.
  verify_ssl:
    description:
    - Whether or not to verify the API server's SSL certificates.
    type: bool
requirements:
- openshift == 0.4.0.a1
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
    action:
      description:
      - What action was taken/failed regarding to the regarding object.
      type: str
    api_version:
      description:
      - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values.
      type: str
    deprecated_count:
      description:
      - Deprecated field assuring backward compatibility with core.v1 Event type
      type: int
    deprecated_first_timestamp:
      description:
      - Deprecated field assuring backward compatibility with core.v1 Event type
      type: complex
      contains: {}
    deprecated_last_timestamp:
      description:
      - Deprecated field assuring backward compatibility with core.v1 Event type
      type: complex
      contains: {}
    deprecated_source:
      description:
      - Deprecated field assuring backward compatibility with core.v1 Event type
      type: complex
    event_time:
      description:
      - Required. Time when this Event was first observed.
      type: complex
      contains: {}
    kind:
      description:
      - Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to. Cannot
        be updated. In CamelCase.
      type: str
    metadata:
      description: []
      type: complex
    note:
      description:
      - Optional. A human-readable description of the status of this operation. Maximal
        length of the note is 1kB, but libraries should be prepared to handle values
        up to 64kB.
      type: str
    reason:
      description:
      - Why the action was taken.
      type: str
    regarding:
      description:
      - The object this Event is about. In most cases it's an Object reporting controller
        implements. E.g. ReplicaSetController implements ReplicaSets and this event
        is emitted because it acts on some changes in a ReplicaSet object.
      type: complex
    related:
      description:
      - Optional secondary object for more complex actions. E.g. when regarding object
        triggers a creation or deletion of related object.
      type: complex
    reporting_controller:
      description:
      - Name of the controller that emitted this Event, e.g. `kubernetes.io/kubelet`.
      type: str
    reporting_instance:
      description:
      - ID of the controller instance, e.g. `kubelet-xyzf`.
      type: str
    series:
      description:
      - Data about the Event series this event represents or nil if it's a singleton
        Event.
      type: complex
    type:
      description:
      - Type of this event (Normal, Warning), new types could be added in the future.
      type: str
'''


def main():
    try:
        module = OpenShiftAnsibleModule('event', 'v1beta1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
