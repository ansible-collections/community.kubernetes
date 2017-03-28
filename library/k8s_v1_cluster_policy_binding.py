#!/usr/bin/env python

from ansible.module_utils.k8s_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: k8s_v1_cluster_policy_binding
short_description: Kubernetes ClusterPolicyBinding
description:
- Manage the lifecycle of a cluster_policy_binding object. Supports check mode, and
  attempts to to be idempotent.
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
  policy_ref_api_version:
    description:
    - API version of the referent.
    aliases:
    - api_version
  policy_ref_field_path:
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
  policy_ref_kind:
    description:
    - Kind of the referent.
    aliases:
    - kind
  policy_ref_name:
    description:
    - Name of the referent.
    aliases:
    - name
  policy_ref_namespace:
    description:
    - Namespace of the referent.
    aliases:
    - namespace
  policy_ref_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - resource_version
  policy_ref_uid:
    description:
    - UID of the referent.
    aliases:
    - uid
  resource_definition:
    description:
    - Provide the YAML definition for the object, bypassing any modules parameters
      intended to define object attributes.
    type: dict
  role_bindings:
    description:
    - RoleBindings holds all the ClusterRoleBindings held by this ClusterPolicyBinding,
      mapped by ClusterRoleBinding.Name
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
- openshift == 1.0.0-snapshot
'''

EXAMPLES = '''
'''

RETURN = '''
api_version:
  type: string
  description: Requested API version
cluster_policy_binding:
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
    last_modified:
      description:
      - LastModified is the last time that any part of the ClusterPolicyBinding was
        created, updated, or deleted
      type: complex
      contains: {}
    metadata:
      description:
      - Standard object's metadata.
      type: complex
      contains:
        annotations:
          description:
          - Annotations is an unstructured key value map stored with a resource that
            may be set by external tools to store and retrieve arbitrary metadata.
            They are not queryable and should be preserved when modifying objects.
          type: complex
          contains: str, str
        cluster_name:
          description:
          - The name of the cluster which the object belongs to. This is used to distinguish
            resources with same name and namespace in different clusters. This field
            is not set anywhere right now and apiserver is going to ignore it if set
            in create or update request.
          type: str
        creation_timestamp:
          description:
          - CreationTimestamp is a timestamp representing the server time when this
            object was created. It is not guaranteed to be set in happens-before order
            across separate operations. Clients may not set this value. It is represented
            in RFC3339 form and is in UTC. Populated by the system. Read-only. Null
            for lists.
          type: complex
          contains: {}
        deletion_grace_period_seconds:
          description:
          - Number of seconds allowed for this object to gracefully terminate before
            it will be removed from the system. Only set when deletionTimestamp is
            also set. May only be shortened. Read-only.
          type: int
        deletion_timestamp:
          description:
          - DeletionTimestamp is RFC 3339 date and time at which this resource will
            be deleted. This field is set by the server when a graceful deletion is
            requested by the user, and is not directly settable by a client. The resource
            is expected to be deleted (no longer visible from resource lists, and
            not reachable by name) after the time in this field. Once set, this value
            may not be unset or be set further into the future, although it may be
            shortened or the resource may be deleted prior to this time. For example,
            a user may request that a pod is deleted in 30 seconds. The Kubelet will
            react by sending a graceful termination signal to the containers in the
            pod. After that 30 seconds, the Kubelet will send a hard termination signal
            (SIGKILL) to the container and after cleanup, remove the pod from the
            API. In the presence of network partitions, this object may still exist
            after this timestamp, until an administrator or automated process can
            determine the resource is fully terminated. If not set, graceful deletion
            of the object has not been requested. Populated by the system when a graceful
            deletion is requested. Read-only.
          type: complex
          contains: {}
        finalizers:
          description:
          - Must be empty before the object is deleted from the registry. Each entry
            is an identifier for the responsible component that will remove the entry
            from the list. If the deletionTimestamp of the object is non-nil, entries
            in this list can only be removed.
          type: list
          contains: str
        generate_name:
          description:
          - GenerateName is an optional prefix, used by the server, to generate a
            unique name ONLY IF the Name field has not been provided. If this field
            is used, the name returned to the client will be different than the name
            passed. This value will also be combined with a unique suffix. The provided
            value has the same validation rules as the Name field, and may be truncated
            by the length of the suffix required to make the value unique on the server.
            If this field is specified and the generated name exists, the server will
            NOT return a 409 - instead, it will either return 201 Created or 500 with
            Reason ServerTimeout indicating a unique name could not be found in the
            time allotted, and the client should retry (optionally after the time
            indicated in the Retry-After header). Applied only if Name is not specified.
          type: str
        generation:
          description:
          - A sequence number representing a specific generation of the desired state.
            Populated by the system. Read-only.
          type: int
        labels:
          description:
          - Map of string keys and values that can be used to organize and categorize
            (scope and select) objects. May match selectors of replication controllers
            and services.
          type: complex
          contains: str, str
        name:
          description:
          - Name must be unique within a namespace. Is required when creating resources,
            although some resources may allow a client to request the generation of
            an appropriate name automatically. Name is primarily intended for creation
            idempotence and configuration definition. Cannot be updated.
          type: str
        namespace:
          description:
          - Namespace defines the space within each name must be unique. An empty
            namespace is equivalent to the "default" namespace, but "default" is the
            canonical representation. Not all objects are required to be scoped to
            a namespace - the value of this field for those objects will be empty.
            Must be a DNS_LABEL. Cannot be updated.
          type: str
        owner_references:
          description:
          - List of objects depended by this object. If ALL objects in the list have
            been deleted, this object will be garbage collected. If this object is
            managed by a controller, then an entry in this list will point to this
            controller, with the controller field set to true. There cannot be more
            than one managing controller.
          type: list
          contains:
            api_version:
              description:
              - API version of the referent.
              type: str
            controller:
              description:
              - If true, this reference points to the managing controller.
              type: bool
            kind:
              description:
              - Kind of the referent.
              type: str
            name:
              description:
              - Name of the referent.
              type: str
            uid:
              description:
              - UID of the referent.
              type: str
        resource_version:
          description:
          - An opaque value that represents the internal version of this object that
            can be used by clients to determine when objects have changed. May be
            used for optimistic concurrency, change detection, and the watch operation
            on a resource or set of resources. Clients must treat these values as
            opaque and passed unmodified back to the server. They may only be valid
            for a particular resource or set of resources. Populated by the system.
            Read-only. Value must be treated as opaque by clients and .
          type: str
        self_link:
          description:
          - SelfLink is a URL representing this object. Populated by the system. Read-only.
          type: str
        uid:
          description:
          - UID is the unique in time and space value for this object. It is typically
            generated by the server on successful creation of a resource and is not
            allowed to change on PUT operations. Populated by the system. Read-only.
          type: str
    policy_ref:
      description:
      - PolicyRef is a reference to the ClusterPolicy that contains all the ClusterRoles
        that this ClusterPolicyBinding's RoleBindings may reference
      type: complex
      contains:
        api_version:
          description:
          - API version of the referent.
          type: str
        field_path:
          description:
          - 'If referring to a piece of an object instead of an entire object, this
            string should contain a valid JSON/Go field access statement, such as
            desiredState.manifest.containers[2]. For example, if the object reference
            is to a container within a pod, this would take on a value like: "spec.containers{name}"
            (where "name" refers to the name of the container that triggered the event)
            or if no container name is specified "spec.containers[2]" (container with
            index 2 in this pod). This syntax is chosen only to have some well-defined
            way of referencing a part of an object.'
          type: str
        kind:
          description:
          - Kind of the referent.
          type: str
        name:
          description:
          - Name of the referent.
          type: str
        namespace:
          description:
          - Namespace of the referent.
          type: str
        resource_version:
          description:
          - Specific resourceVersion to which this reference is made, if any.
          type: str
        uid:
          description:
          - UID of the referent.
          type: str
    role_bindings:
      description:
      - RoleBindings holds all the ClusterRoleBindings held by this ClusterPolicyBinding,
        mapped by ClusterRoleBinding.Name
      type: list
      contains:
        name:
          description:
          - Name is the name of the cluster role binding
          type: str
        role_binding:
          description:
          - RoleBinding is the cluster role binding being named
          type: complex
          contains:
            api_version:
              description:
              - APIVersion defines the versioned schema of this representation of
                an object. Servers should convert recognized schemas to the latest
                internal value, and may reject unrecognized values.
              type: str
            group_names:
              description:
              - GroupNames holds all the groups directly bound to the role. This field
                should only be specified when supporting legacy clients and servers.
                See Subjects for further details.
              type: list
              contains: str
            kind:
              description:
              - Kind is a string value representing the REST resource this object
                represents. Servers may infer this from the endpoint the client submits
                requests to. Cannot be updated. In CamelCase.
              type: str
            metadata:
              description:
              - Standard object's metadata.
              type: complex
              contains:
                annotations:
                  description:
                  - Annotations is an unstructured key value map stored with a resource
                    that may be set by external tools to store and retrieve arbitrary
                    metadata. They are not queryable and should be preserved when
                    modifying objects.
                  type: complex
                  contains: str, str
                cluster_name:
                  description:
                  - The name of the cluster which the object belongs to. This is used
                    to distinguish resources with same name and namespace in different
                    clusters. This field is not set anywhere right now and apiserver
                    is going to ignore it if set in create or update request.
                  type: str
                creation_timestamp:
                  description:
                  - CreationTimestamp is a timestamp representing the server time
                    when this object was created. It is not guaranteed to be set in
                    happens-before order across separate operations. Clients may not
                    set this value. It is represented in RFC3339 form and is in UTC.
                    Populated by the system. Read-only. Null for lists.
                  type: complex
                  contains: {}
                deletion_grace_period_seconds:
                  description:
                  - Number of seconds allowed for this object to gracefully terminate
                    before it will be removed from the system. Only set when deletionTimestamp
                    is also set. May only be shortened. Read-only.
                  type: int
                deletion_timestamp:
                  description:
                  - DeletionTimestamp is RFC 3339 date and time at which this resource
                    will be deleted. This field is set by the server when a graceful
                    deletion is requested by the user, and is not directly settable
                    by a client. The resource is expected to be deleted (no longer
                    visible from resource lists, and not reachable by name) after
                    the time in this field. Once set, this value may not be unset
                    or be set further into the future, although it may be shortened
                    or the resource may be deleted prior to this time. For example,
                    a user may request that a pod is deleted in 30 seconds. The Kubelet
                    will react by sending a graceful termination signal to the containers
                    in the pod. After that 30 seconds, the Kubelet will send a hard
                    termination signal (SIGKILL) to the container and after cleanup,
                    remove the pod from the API. In the presence of network partitions,
                    this object may still exist after this timestamp, until an administrator
                    or automated process can determine the resource is fully terminated.
                    If not set, graceful deletion of the object has not been requested.
                    Populated by the system when a graceful deletion is requested.
                    Read-only.
                  type: complex
                  contains: {}
                finalizers:
                  description:
                  - Must be empty before the object is deleted from the registry.
                    Each entry is an identifier for the responsible component that
                    will remove the entry from the list. If the deletionTimestamp
                    of the object is non-nil, entries in this list can only be removed.
                  type: list
                  contains: str
                generate_name:
                  description:
                  - GenerateName is an optional prefix, used by the server, to generate
                    a unique name ONLY IF the Name field has not been provided. If
                    this field is used, the name returned to the client will be different
                    than the name passed. This value will also be combined with a
                    unique suffix. The provided value has the same validation rules
                    as the Name field, and may be truncated by the length of the suffix
                    required to make the value unique on the server. If this field
                    is specified and the generated name exists, the server will NOT
                    return a 409 - instead, it will either return 201 Created or 500
                    with Reason ServerTimeout indicating a unique name could not be
                    found in the time allotted, and the client should retry (optionally
                    after the time indicated in the Retry-After header). Applied only
                    if Name is not specified.
                  type: str
                generation:
                  description:
                  - A sequence number representing a specific generation of the desired
                    state. Populated by the system. Read-only.
                  type: int
                labels:
                  description:
                  - Map of string keys and values that can be used to organize and
                    categorize (scope and select) objects. May match selectors of
                    replication controllers and services.
                  type: complex
                  contains: str, str
                name:
                  description:
                  - Name must be unique within a namespace. Is required when creating
                    resources, although some resources may allow a client to request
                    the generation of an appropriate name automatically. Name is primarily
                    intended for creation idempotence and configuration definition.
                    Cannot be updated.
                  type: str
                namespace:
                  description:
                  - Namespace defines the space within each name must be unique. An
                    empty namespace is equivalent to the "default" namespace, but
                    "default" is the canonical representation. Not all objects are
                    required to be scoped to a namespace - the value of this field
                    for those objects will be empty. Must be a DNS_LABEL. Cannot be
                    updated.
                  type: str
                owner_references:
                  description:
                  - List of objects depended by this object. If ALL objects in the
                    list have been deleted, this object will be garbage collected.
                    If this object is managed by a controller, then an entry in this
                    list will point to this controller, with the controller field
                    set to true. There cannot be more than one managing controller.
                  type: list
                  contains:
                    api_version:
                      description:
                      - API version of the referent.
                      type: str
                    controller:
                      description:
                      - If true, this reference points to the managing controller.
                      type: bool
                    kind:
                      description:
                      - Kind of the referent.
                      type: str
                    name:
                      description:
                      - Name of the referent.
                      type: str
                    uid:
                      description:
                      - UID of the referent.
                      type: str
                resource_version:
                  description:
                  - An opaque value that represents the internal version of this object
                    that can be used by clients to determine when objects have changed.
                    May be used for optimistic concurrency, change detection, and
                    the watch operation on a resource or set of resources. Clients
                    must treat these values as opaque and passed unmodified back to
                    the server. They may only be valid for a particular resource or
                    set of resources. Populated by the system. Read-only. Value must
                    be treated as opaque by clients and .
                  type: str
                self_link:
                  description:
                  - SelfLink is a URL representing this object. Populated by the system.
                    Read-only.
                  type: str
                uid:
                  description:
                  - UID is the unique in time and space value for this object. It
                    is typically generated by the server on successful creation of
                    a resource and is not allowed to change on PUT operations. Populated
                    by the system. Read-only.
                  type: str
            role_ref:
              description:
              - RoleRef can only reference the current namespace and the global namespace.
                If the ClusterRoleRef cannot be resolved, the Authorizer must return
                an error. Since Policy is a singleton, this is sufficient knowledge
                to locate a role.
              type: complex
              contains:
                api_version:
                  description:
                  - API version of the referent.
                  type: str
                field_path:
                  description:
                  - 'If referring to a piece of an object instead of an entire object,
                    this string should contain a valid JSON/Go field access statement,
                    such as desiredState.manifest.containers[2]. For example, if the
                    object reference is to a container within a pod, this would take
                    on a value like: "spec.containers{name}" (where "name" refers
                    to the name of the container that triggered the event) or if no
                    container name is specified "spec.containers[2]" (container with
                    index 2 in this pod). This syntax is chosen only to have some
                    well-defined way of referencing a part of an object.'
                  type: str
                kind:
                  description:
                  - Kind of the referent.
                  type: str
                name:
                  description:
                  - Name of the referent.
                  type: str
                namespace:
                  description:
                  - Namespace of the referent.
                  type: str
                resource_version:
                  description:
                  - Specific resourceVersion to which this reference is made, if any.
                  type: str
                uid:
                  description:
                  - UID of the referent.
                  type: str
            subjects:
              description:
              - Subjects hold object references to authorize with this rule. This
                field is ignored if UserNames or GroupNames are specified to support
                legacy clients and servers. Thus newer clients that do not need to
                support backwards compatibility should send only fully qualified Subjects
                and should omit the UserNames and GroupNames fields. Clients that
                need to support backwards compatibility can use this field to build
                the UserNames and GroupNames.
              type: list
              contains:
                api_version:
                  description:
                  - API version of the referent.
                  type: str
                field_path:
                  description:
                  - 'If referring to a piece of an object instead of an entire object,
                    this string should contain a valid JSON/Go field access statement,
                    such as desiredState.manifest.containers[2]. For example, if the
                    object reference is to a container within a pod, this would take
                    on a value like: "spec.containers{name}" (where "name" refers
                    to the name of the container that triggered the event) or if no
                    container name is specified "spec.containers[2]" (container with
                    index 2 in this pod). This syntax is chosen only to have some
                    well-defined way of referencing a part of an object.'
                  type: str
                kind:
                  description:
                  - Kind of the referent.
                  type: str
                name:
                  description:
                  - Name of the referent.
                  type: str
                namespace:
                  description:
                  - Namespace of the referent.
                  type: str
                resource_version:
                  description:
                  - Specific resourceVersion to which this reference is made, if any.
                  type: str
                uid:
                  description:
                  - UID of the referent.
                  type: str
            user_names:
              description:
              - UserNames holds all the usernames directly bound to the role. This
                field should only be specified when supporting legacy clients and
                servers. See Subjects for further details.
              type: list
              contains: str
'''


def main():
    try:
        module = OpenShiftAnsibleModule('cluster_policy_binding', 'V1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()

