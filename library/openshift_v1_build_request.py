#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.openshift_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: openshift_v1_build_request
short_description: OpenShift BuildRequest
description:
- Manage the lifecycle of a build_request object. Supports check mode, and attempts
  to to be idempotent.
version_added: 2.3.0
author: OpenShift (@openshift)
options:
  _from_api_version:
    description:
    - API version of the referent.
    aliases:
    - api_version
  _from_field_path:
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
  _from_kind:
    description:
    - Kind of the referent.
    aliases:
    - kind
  _from_name:
    description:
    - Name of the referent.
    aliases:
    - name
  _from_namespace:
    description:
    - Namespace of the referent.
    aliases:
    - namespace
  _from_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - resource_version
  _from_uid:
    description:
    - UID of the referent.
    aliases:
    - uid
  annotations:
    description:
    - Annotations is an unstructured key value map stored with a resource that may
      be set by external tools to store and retrieve arbitrary metadata. They are
      not queryable and should be preserved when modifying objects.
    type: dict
  api_key:
    description:
    - Token used to connect to the API.
  binary_as_file:
    description:
    - asFile indicates that the provided binary input should be considered a single
      file within the build input. For example, specifying "webapp.war" would place
      the provided binary as `/webapp.war` for the builder. If left empty, the Docker
      and Source build strategies assume this file is a zip, tar, or tar.gz file and
      extract it as the source. The custom strategy receives this binary as standard
      input. This filename may not contain slashes or be '..' or '.'.
    aliases:
    - as_file
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
  docker_strategy_options_build_args:
    description:
    - Args contains any build arguments that are to be passed to Docker. See
    aliases:
    - build_args
    type: list
  docker_strategy_options_no_cache:
    description:
    - noCache overrides the docker-strategy noCache option in the build config
    aliases:
    - no_cache
    type: bool
  env:
    description:
    - env contains additional environment variables you want to pass into a builder
      container.
    type: list
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
  last_version:
    description:
    - lastVersion (optional) is the LastVersion of the BuildConfig that was used to
      generate the build. If the BuildConfig in the generator doesn't match, a build
      will not be generated.
    type: int
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
  revision_git_author_email:
    description:
    - email of the source control user
    aliases:
    - email
  revision_git_author_name:
    description:
    - name of the source control user
    aliases:
    - name
  revision_git_commit:
    description:
    - commit is the commit hash identifying a specific commit
    aliases:
    - commit
  revision_git_committer_email:
    description:
    - email of the source control user
    aliases:
    - email
  revision_git_committer_name:
    description:
    - name of the source control user
    aliases:
    - name
  revision_git_message:
    description:
    - message is the description of a specific commit
    aliases:
    - message
  revision_type:
    description:
    - type of the build source, may be one of 'Source', 'Dockerfile', 'Binary', or
      'Images'
    aliases:
    - type
  source_strategy_options_incremental:
    description:
    - incremental overrides the source-strategy incremental option in the build config
    aliases:
    - incremental
    type: bool
  ssl_ca_cert:
    description:
    - Path to a CA certificate used to authenticate with the API.
    type: path
  triggered_by:
    description:
    - triggeredBy describes which triggers started the most recent update to the build
      configuration and contains information about those triggers.
    type: list
  triggered_by_image_api_version:
    description:
    - API version of the referent.
    aliases:
    - api_version
  triggered_by_image_field_path:
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
  triggered_by_image_kind:
    description:
    - Kind of the referent.
    aliases:
    - kind
  triggered_by_image_name:
    description:
    - Name of the referent.
    aliases:
    - name
  triggered_by_image_namespace:
    description:
    - Namespace of the referent.
    aliases:
    - namespace
  triggered_by_image_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - resource_version
  triggered_by_image_uid:
    description:
    - UID of the referent.
    aliases:
    - uid
  username:
    description:
    - Provide a username for connecting to the API.
  verify_ssl:
    description:
    - Whether or not to verify the API server's SSL certificates.
    type: bool
requirements:
- openshift == 0.3.3
'''

EXAMPLES = '''
'''

RETURN = '''
api_version:
  type: string
  description: Requested API version
build_request:
  type: complex
  returned: on success
  contains:
    _from:
      description:
      - from is the reference to the ImageStreamTag that triggered the build.
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
    api_version:
      description:
      - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values.
      type: str
    binary:
      description:
      - binary indicates a request to build from a binary provided to the builder
      type: complex
      contains:
        as_file:
          description:
          - asFile indicates that the provided binary input should be considered a
            single file within the build input. For example, specifying "webapp.war"
            would place the provided binary as `/webapp.war` for the builder. If left
            empty, the Docker and Source build strategies assume this file is a zip,
            tar, or tar.gz file and extract it as the source. The custom strategy
            receives this binary as standard input. This filename may not contain
            slashes or be '..' or '.'.
          type: str
    docker_strategy_options:
      description:
      - DockerStrategyOptions contains additional docker-strategy specific options
        for the build
      type: complex
      contains:
        build_args:
          description:
          - Args contains any build arguments that are to be passed to Docker. See
          type: list
          contains:
            name:
              description:
              - Name of the environment variable. Must be a C_IDENTIFIER.
              type: str
            value:
              description:
              - 'Variable references $(VAR_NAME) are expanded using the previous defined
                environment variables in the container and any service environment
                variables. If a variable cannot be resolved, the reference in the
                input string will be unchanged. The $(VAR_NAME) syntax can be escaped
                with a double $$, ie: $$(VAR_NAME). Escaped references will never
                be expanded, regardless of whether the variable exists or not. Defaults
                to "".'
              type: str
            value_from:
              description:
              - Source for the environment variable's value. Cannot be used if value
                is not empty.
              type: complex
              contains:
                config_map_key_ref:
                  description:
                  - Selects a key of a ConfigMap.
                  type: complex
                  contains:
                    key:
                      description:
                      - The key to select.
                      type: str
                    name:
                      description:
                      - Name of the referent.
                      type: str
                    optional:
                      description:
                      - Specify whether the ConfigMap or it's key must be defined
                      type: bool
                field_ref:
                  description:
                  - 'Selects a field of the pod: supports metadata.name, metadata.namespace,
                    metadata.labels, metadata.annotations, spec.nodeName, spec.serviceAccountName,
                    status.hostIP, status.podIP.'
                  type: complex
                  contains:
                    api_version:
                      description:
                      - Version of the schema the FieldPath is written in terms of,
                        defaults to "v1".
                      type: str
                    field_path:
                      description:
                      - Path of the field to select in the specified API version.
                      type: str
                resource_field_ref:
                  description:
                  - 'Selects a resource of the container: only resources limits and
                    requests (limits.cpu, limits.memory, requests.cpu and requests.memory)
                    are currently supported.'
                  type: complex
                  contains:
                    container_name:
                      description:
                      - 'Container name: required for volumes, optional for env vars'
                      type: str
                    divisor:
                      description:
                      - Specifies the output format of the exposed resources, defaults
                        to "1"
                      type: str
                    resource:
                      description:
                      - 'Required: resource to select'
                      type: str
                secret_key_ref:
                  description:
                  - Selects a key of a secret in the pod's namespace
                  type: complex
                  contains:
                    key:
                      description:
                      - The key of the secret to select from. Must be a valid secret
                        key.
                      type: str
                    name:
                      description:
                      - Name of the referent.
                      type: str
                    optional:
                      description:
                      - Specify whether the Secret or it's key must be defined
                      type: bool
        no_cache:
          description:
          - noCache overrides the docker-strategy noCache option in the build config
          type: bool
    env:
      description:
      - env contains additional environment variables you want to pass into a builder
        container.
      type: list
      contains:
        name:
          description:
          - Name of the environment variable. Must be a C_IDENTIFIER.
          type: str
        value:
          description:
          - 'Variable references $(VAR_NAME) are expanded using the previous defined
            environment variables in the container and any service environment variables.
            If a variable cannot be resolved, the reference in the input string will
            be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$,
            ie: $$(VAR_NAME). Escaped references will never be expanded, regardless
            of whether the variable exists or not. Defaults to "".'
          type: str
        value_from:
          description:
          - Source for the environment variable's value. Cannot be used if value is
            not empty.
          type: complex
          contains:
            config_map_key_ref:
              description:
              - Selects a key of a ConfigMap.
              type: complex
              contains:
                key:
                  description:
                  - The key to select.
                  type: str
                name:
                  description:
                  - Name of the referent.
                  type: str
                optional:
                  description:
                  - Specify whether the ConfigMap or it's key must be defined
                  type: bool
            field_ref:
              description:
              - 'Selects a field of the pod: supports metadata.name, metadata.namespace,
                metadata.labels, metadata.annotations, spec.nodeName, spec.serviceAccountName,
                status.hostIP, status.podIP.'
              type: complex
              contains:
                api_version:
                  description:
                  - Version of the schema the FieldPath is written in terms of, defaults
                    to "v1".
                  type: str
                field_path:
                  description:
                  - Path of the field to select in the specified API version.
                  type: str
            resource_field_ref:
              description:
              - 'Selects a resource of the container: only resources limits and requests
                (limits.cpu, limits.memory, requests.cpu and requests.memory) are
                currently supported.'
              type: complex
              contains:
                container_name:
                  description:
                  - 'Container name: required for volumes, optional for env vars'
                  type: str
                divisor:
                  description:
                  - Specifies the output format of the exposed resources, defaults
                    to "1"
                  type: str
                resource:
                  description:
                  - 'Required: resource to select'
                  type: str
            secret_key_ref:
              description:
              - Selects a key of a secret in the pod's namespace
              type: complex
              contains:
                key:
                  description:
                  - The key of the secret to select from. Must be a valid secret key.
                  type: str
                name:
                  description:
                  - Name of the referent.
                  type: str
                optional:
                  description:
                  - Specify whether the Secret or it's key must be defined
                  type: bool
    kind:
      description:
      - Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to. Cannot
        be updated. In CamelCase.
      type: str
    last_version:
      description:
      - lastVersion (optional) is the LastVersion of the BuildConfig that was used
        to generate the build. If the BuildConfig in the generator doesn't match,
        a build will not be generated.
      type: int
    metadata:
      description:
      - metadata for BuildRequest.
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
        initializers:
          description:
          - An initializer is a controller which enforces some system invariant at
            object creation time. This field is a list of initializers that have not
            yet acted on this object. If nil or empty, this object has been completely
            initialized. Otherwise, the object is considered uninitialized and is
            hidden (in list/watch and get calls) from clients that haven't explicitly
            asked to observe uninitialized objects. When an object is created, the
            system will populate this list with the current set of initializers. Only
            privileged users may set or modify this list. Once it is empty, it may
            not be modified further by any user.
          type: complex
          contains:
            pending:
              description:
              - Pending is a list of initializers that must execute in order before
                this object is visible. When the last pending initializer is removed,
                and no failing result is set, the initializers struct will be set
                to nil and the object is considered as initialized and visible to
                all clients.
              type: list
              contains:
                name:
                  description:
                  - name of the process that is responsible for initializing this
                    object.
                  type: str
            result:
              description:
              - If result is set with the Failure field, the object will be persisted
                to storage and then deleted, ensuring that other clients can observe
                the deletion.
              type: complex
              contains:
                api_version:
                  description:
                  - APIVersion defines the versioned schema of this representation
                    of an object. Servers should convert recognized schemas to the
                    latest internal value, and may reject unrecognized values.
                  type: str
                code:
                  description:
                  - Suggested HTTP return code for this status, 0 if not set.
                  type: int
                details:
                  description:
                  - Extended data associated with the reason. Each reason may define
                    its own extended details. This field is optional and the data
                    returned is not guaranteed to conform to any schema except that
                    defined by the reason type.
                  type: complex
                  contains:
                    causes:
                      description:
                      - The Causes array includes more details associated with the
                        StatusReason failure. Not all StatusReasons may provide detailed
                        causes.
                      type: list
                      contains:
                        field:
                          description:
                          - 'The field of the resource that has caused this error,
                            as named by its JSON serialization. May include dot and
                            postfix notation for nested attributes. Arrays are zero-indexed.
                            Fields may appear more than once in an array of causes
                            due to fields having multiple errors. Optional. Examples:
                            "name" - the field "name" on the current resource "items[0].name"
                            - the field "name" on the first array entry in "items"'
                          type: str
                        message:
                          description:
                          - A human-readable description of the cause of the error.
                            This field may be presented as-is to a reader.
                          type: str
                        reason:
                          description:
                          - A machine-readable description of the cause of the error.
                            If this value is empty there is no information available.
                          type: str
                    group:
                      description:
                      - The group attribute of the resource associated with the status
                        StatusReason.
                      type: str
                    kind:
                      description:
                      - The kind attribute of the resource associated with the status
                        StatusReason. On some operations may differ from the requested
                        resource Kind.
                      type: str
                    name:
                      description:
                      - The name attribute of the resource associated with the status
                        StatusReason (when there is a single name which can be described).
                      type: str
                    retry_after_seconds:
                      description:
                      - If specified, the time in seconds before the operation should
                        be retried.
                      type: int
                    uid:
                      description:
                      - UID of the resource. (when there is a single resource which
                        can be described).
                      type: str
                kind:
                  description:
                  - Kind is a string value representing the REST resource this object
                    represents. Servers may infer this from the endpoint the client
                    submits requests to. Cannot be updated. In CamelCase.
                  type: str
                message:
                  description:
                  - A human-readable description of the status of this operation.
                  type: str
                metadata:
                  description:
                  - Standard list metadata.
                  type: complex
                  contains:
                    resource_version:
                      description:
                      - String that identifies the server's internal version of this
                        object that can be used by clients to determine when objects
                        have changed. Value must be treated as opaque by clients and
                        passed unmodified back to the server. Populated by the system.
                        Read-only.
                      type: str
                    self_link:
                      description:
                      - SelfLink is a URL representing this object. Populated by the
                        system. Read-only.
                      type: str
                reason:
                  description:
                  - A machine-readable description of why this operation is in the
                    "Failure" status. If this value is empty there is no information
                    available. A Reason clarifies an HTTP status code but does not
                    override it.
                  type: str
                status:
                  description:
                  - 'Status of the operation. One of: "Success" or "Failure".'
                  type: str
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
            block_owner_deletion:
              description:
              - If true, AND if the owner has the "foregroundDeletion" finalizer,
                then the owner cannot be deleted from the key-value store until this
                reference is removed. Defaults to false. To set this field, a user
                needs "delete" permission of the owner, otherwise 422 (Unprocessable
                Entity) will be returned.
              type: bool
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
    revision:
      description:
      - revision is the information from the source for a specific repo snapshot.
      type: complex
      contains:
        git:
          description:
          - Git contains information about git-based build source
          type: complex
          contains:
            author:
              description:
              - author is the author of a specific commit
              type: complex
              contains:
                email:
                  description:
                  - email of the source control user
                  type: str
                name:
                  description:
                  - name of the source control user
                  type: str
            commit:
              description:
              - commit is the commit hash identifying a specific commit
              type: str
            committer:
              description:
              - committer is the committer of a specific commit
              type: complex
              contains:
                email:
                  description:
                  - email of the source control user
                  type: str
                name:
                  description:
                  - name of the source control user
                  type: str
            message:
              description:
              - message is the description of a specific commit
              type: str
        type:
          description:
          - type of the build source, may be one of 'Source', 'Dockerfile', 'Binary',
            or 'Images'
          type: str
    source_strategy_options:
      description:
      - SourceStrategyOptions contains additional source-strategy specific options
        for the build
      type: complex
      contains:
        incremental:
          description:
          - incremental overrides the source-strategy incremental option in the build
            config
          type: bool
    triggered_by:
      description:
      - triggeredBy describes which triggers started the most recent update to the
        build configuration and contains information about those triggers.
      type: list
      contains:
        bitbucket_web_hook:
          description:
          - BitbucketWebHook represents data for a Bitbucket webhook that fired a
            specific build.
          type: complex
          contains:
            revision:
              description:
              - Revision is the git source revision information of the trigger.
              type: complex
              contains:
                git:
                  description:
                  - Git contains information about git-based build source
                  type: complex
                  contains:
                    author:
                      description:
                      - author is the author of a specific commit
                      type: complex
                      contains:
                        email:
                          description:
                          - email of the source control user
                          type: str
                        name:
                          description:
                          - name of the source control user
                          type: str
                    commit:
                      description:
                      - commit is the commit hash identifying a specific commit
                      type: str
                    committer:
                      description:
                      - committer is the committer of a specific commit
                      type: complex
                      contains:
                        email:
                          description:
                          - email of the source control user
                          type: str
                        name:
                          description:
                          - name of the source control user
                          type: str
                    message:
                      description:
                      - message is the description of a specific commit
                      type: str
                type:
                  description:
                  - type of the build source, may be one of 'Source', 'Dockerfile',
                    'Binary', or 'Images'
                  type: str
            secret:
              description:
              - Secret is the obfuscated webhook secret that triggered a build.
              type: str
        generic_web_hook:
          description:
          - genericWebHook holds data about a builds generic webhook trigger.
          type: complex
          contains:
            revision:
              description:
              - revision is an optional field that stores the git source revision
                information of the generic webhook trigger when it is available.
              type: complex
              contains:
                git:
                  description:
                  - Git contains information about git-based build source
                  type: complex
                  contains:
                    author:
                      description:
                      - author is the author of a specific commit
                      type: complex
                      contains:
                        email:
                          description:
                          - email of the source control user
                          type: str
                        name:
                          description:
                          - name of the source control user
                          type: str
                    commit:
                      description:
                      - commit is the commit hash identifying a specific commit
                      type: str
                    committer:
                      description:
                      - committer is the committer of a specific commit
                      type: complex
                      contains:
                        email:
                          description:
                          - email of the source control user
                          type: str
                        name:
                          description:
                          - name of the source control user
                          type: str
                    message:
                      description:
                      - message is the description of a specific commit
                      type: str
                type:
                  description:
                  - type of the build source, may be one of 'Source', 'Dockerfile',
                    'Binary', or 'Images'
                  type: str
            secret:
              description:
              - secret is the obfuscated webhook secret that triggered a build.
              type: str
        github_web_hook:
          description:
          - gitHubWebHook represents data for a GitHub webhook that fired a specific
            build.
          type: complex
          contains:
            revision:
              description:
              - revision is the git revision information of the trigger.
              type: complex
              contains:
                git:
                  description:
                  - Git contains information about git-based build source
                  type: complex
                  contains:
                    author:
                      description:
                      - author is the author of a specific commit
                      type: complex
                      contains:
                        email:
                          description:
                          - email of the source control user
                          type: str
                        name:
                          description:
                          - name of the source control user
                          type: str
                    commit:
                      description:
                      - commit is the commit hash identifying a specific commit
                      type: str
                    committer:
                      description:
                      - committer is the committer of a specific commit
                      type: complex
                      contains:
                        email:
                          description:
                          - email of the source control user
                          type: str
                        name:
                          description:
                          - name of the source control user
                          type: str
                    message:
                      description:
                      - message is the description of a specific commit
                      type: str
                type:
                  description:
                  - type of the build source, may be one of 'Source', 'Dockerfile',
                    'Binary', or 'Images'
                  type: str
            secret:
              description:
              - secret is the obfuscated webhook secret that triggered a build.
              type: str
        gitlab_web_hook:
          description:
          - GitLabWebHook represents data for a GitLab webhook that fired a specific
            build.
          type: complex
          contains:
            revision:
              description:
              - Revision is the git source revision information of the trigger.
              type: complex
              contains:
                git:
                  description:
                  - Git contains information about git-based build source
                  type: complex
                  contains:
                    author:
                      description:
                      - author is the author of a specific commit
                      type: complex
                      contains:
                        email:
                          description:
                          - email of the source control user
                          type: str
                        name:
                          description:
                          - name of the source control user
                          type: str
                    commit:
                      description:
                      - commit is the commit hash identifying a specific commit
                      type: str
                    committer:
                      description:
                      - committer is the committer of a specific commit
                      type: complex
                      contains:
                        email:
                          description:
                          - email of the source control user
                          type: str
                        name:
                          description:
                          - name of the source control user
                          type: str
                    message:
                      description:
                      - message is the description of a specific commit
                      type: str
                type:
                  description:
                  - type of the build source, may be one of 'Source', 'Dockerfile',
                    'Binary', or 'Images'
                  type: str
            secret:
              description:
              - Secret is the obfuscated webhook secret that triggered a build.
              type: str
        image_change_build:
          description:
          - imageChangeBuild stores information about an imagechange event that triggered
            a new build.
          type: complex
          contains:
            from_ref:
              description:
              - fromRef contains detailed information about an image that triggered
                a build.
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
            image_id:
              description:
              - imageID is the ID of the image that triggered a a new build.
              type: str
        message:
          description:
          - 'message is used to store a human readable message for why the build was
            triggered. E.g.: "Manually triggered by user", "Configuration change",etc.'
          type: str
    triggered_by_image:
      description:
      - triggeredByImage is the Image that triggered this build.
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
'''


def main():
    try:
        module = OpenShiftAnsibleModule('build_request', 'v1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
