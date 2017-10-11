#!/usr/bin/env python

from ansible.module_utils.k8s_common import KubernetesAnsibleModule, KubernetesAnsibleException

DOCUMENTATION = '''
module: k8s_v1alpha1_pod_preset_list
short_description: Kubernetes PodPresetList
description:
- Retrieve a list of pod_presets. List operations provide a snapshot read of the underlying
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
- kubernetes == 3.0.0
'''

EXAMPLES = '''
'''

RETURN = '''
api_version:
  type: string
  description: Requested API version
pod_preset_list:
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
      - Items is a list of schema objects.
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
          description: []
          type: complex
          contains:
            annotations:
              description:
              - Annotations is an unstructured key value map stored with a resource
                that may be set by external tools to store and retrieve arbitrary
                metadata. They are not queryable and should be preserved when modifying
                objects.
              type: complex
              contains: str, str
            cluster_name:
              description:
              - The name of the cluster which the object belongs to. This is used
                to distinguish resources with same name and namespace in different
                clusters. This field is not set anywhere right now and apiserver is
                going to ignore it if set in create or update request.
              type: str
            creation_timestamp:
              description:
              - CreationTimestamp is a timestamp representing the server time when
                this object was created. It is not guaranteed to be set in happens-before
                order across separate operations. Clients may not set this value.
                It is represented in RFC3339 form and is in UTC. Populated by the
                system. Read-only. Null for lists.
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
                will be deleted. This field is set by the server when a graceful deletion
                is requested by the user, and is not directly settable by a client.
                The resource is expected to be deleted (no longer visible from resource
                lists, and not reachable by name) after the time in this field. Once
                set, this value may not be unset or be set further into the future,
                although it may be shortened or the resource may be deleted prior
                to this time. For example, a user may request that a pod is deleted
                in 30 seconds. The Kubelet will react by sending a graceful termination
                signal to the containers in the pod. After that 30 seconds, the Kubelet
                will send a hard termination signal (SIGKILL) to the container and
                after cleanup, remove the pod from the API. In the presence of network
                partitions, this object may still exist after this timestamp, until
                an administrator or automated process can determine the resource is
                fully terminated. If not set, graceful deletion of the object has
                not been requested. Populated by the system when a graceful deletion
                is requested. Read-only.
              type: complex
              contains: {}
            finalizers:
              description:
              - Must be empty before the object is deleted from the registry. Each
                entry is an identifier for the responsible component that will remove
                the entry from the list. If the deletionTimestamp of the object is
                non-nil, entries in this list can only be removed.
              type: list
              contains: str
            generate_name:
              description:
              - GenerateName is an optional prefix, used by the server, to generate
                a unique name ONLY IF the Name field has not been provided. If this
                field is used, the name returned to the client will be different than
                the name passed. This value will also be combined with a unique suffix.
                The provided value has the same validation rules as the Name field,
                and may be truncated by the length of the suffix required to make
                the value unique on the server. If this field is specified and the
                generated name exists, the server will NOT return a 409 - instead,
                it will either return 201 Created or 500 with Reason ServerTimeout
                indicating a unique name could not be found in the time allotted,
                and the client should retry (optionally after the time indicated in
                the Retry-After header). Applied only if Name is not specified.
              type: str
            generation:
              description:
              - A sequence number representing a specific generation of the desired
                state. Populated by the system. Read-only.
              type: int
            initializers:
              description:
              - An initializer is a controller which enforces some system invariant
                at object creation time. This field is a list of initializers that
                have not yet acted on this object. If nil or empty, this object has
                been completely initialized. Otherwise, the object is considered uninitialized
                and is hidden (in list/watch and get calls) from clients that haven't
                explicitly asked to observe uninitialized objects. When an object
                is created, the system will populate this list with the current set
                of initializers. Only privileged users may set or modify this list.
                Once it is empty, it may not be modified further by any user.
              type: complex
              contains:
                pending:
                  description:
                  - Pending is a list of initializers that must execute in order before
                    this object is visible. When the last pending initializer is removed,
                    and no failing result is set, the initializers struct will be
                    set to nil and the object is considered as initialized and visible
                    to all clients.
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
                        of an object. Servers should convert recognized schemas to
                        the latest internal value, and may reject unrecognized values.
                      type: str
                    code:
                      description:
                      - Suggested HTTP return code for this status, 0 if not set.
                      type: int
                    details:
                      description:
                      - Extended data associated with the reason. Each reason may
                        define its own extended details. This field is optional and
                        the data returned is not guaranteed to conform to any schema
                        except that defined by the reason type.
                      type: complex
                      contains:
                        causes:
                          description:
                          - The Causes array includes more details associated with
                            the StatusReason failure. Not all StatusReasons may provide
                            detailed causes.
                          type: list
                          contains:
                            field:
                              description:
                              - 'The field of the resource that has caused this error,
                                as named by its JSON serialization. May include dot
                                and postfix notation for nested attributes. Arrays
                                are zero-indexed. Fields may appear more than once
                                in an array of causes due to fields having multiple
                                errors. Optional. Examples: "name" - the field "name"
                                on the current resource "items[0].name" - the field
                                "name" on the first array entry in "items"'
                              type: str
                            message:
                              description:
                              - A human-readable description of the cause of the error.
                                This field may be presented as-is to a reader.
                              type: str
                            reason:
                              description:
                              - A machine-readable description of the cause of the
                                error. If this value is empty there is no information
                                available.
                              type: str
                        group:
                          description:
                          - The group attribute of the resource associated with the
                            status StatusReason.
                          type: str
                        kind:
                          description:
                          - The kind attribute of the resource associated with the
                            status StatusReason. On some operations may differ from
                            the requested resource Kind.
                          type: str
                        name:
                          description:
                          - The name attribute of the resource associated with the
                            status StatusReason (when there is a single name which
                            can be described).
                          type: str
                        retry_after_seconds:
                          description:
                          - If specified, the time in seconds before the operation
                            should be retried.
                          type: int
                        uid:
                          description:
                          - UID of the resource. (when there is a single resource
                            which can be described).
                          type: str
                    kind:
                      description:
                      - Kind is a string value representing the REST resource this
                        object represents. Servers may infer this from the endpoint
                        the client submits requests to. Cannot be updated. In CamelCase.
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
                          - String that identifies the server's internal version of
                            this object that can be used by clients to determine when
                            objects have changed. Value must be treated as opaque
                            by clients and passed unmodified back to the server. Populated
                            by the system. Read-only.
                          type: str
                        self_link:
                          description:
                          - SelfLink is a URL representing this object. Populated
                            by the system. Read-only.
                          type: str
                    reason:
                      description:
                      - A machine-readable description of why this operation is in
                        the "Failure" status. If this value is empty there is no information
                        available. A Reason clarifies an HTTP status code but does
                        not override it.
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
              - Name must be unique within a namespace. Is required when creating
                resources, although some resources may allow a client to request the
                generation of an appropriate name automatically. Name is primarily
                intended for creation idempotence and configuration definition. Cannot
                be updated.
              type: str
            namespace:
              description:
              - Namespace defines the space within each name must be unique. An empty
                namespace is equivalent to the "default" namespace, but "default"
                is the canonical representation. Not all objects are required to be
                scoped to a namespace - the value of this field for those objects
                will be empty. Must be a DNS_LABEL. Cannot be updated.
              type: str
            owner_references:
              description:
              - List of objects depended by this object. If ALL objects in the list
                have been deleted, this object will be garbage collected. If this
                object is managed by a controller, then an entry in this list will
                point to this controller, with the controller field set to true. There
                cannot be more than one managing controller.
              type: list
              contains:
                api_version:
                  description:
                  - API version of the referent.
                  type: str
                block_owner_deletion:
                  description:
                  - If true, AND if the owner has the "foregroundDeletion" finalizer,
                    then the owner cannot be deleted from the key-value store until
                    this reference is removed. Defaults to false. To set this field,
                    a user needs "delete" permission of the owner, otherwise 422 (Unprocessable
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
              - An opaque value that represents the internal version of this object
                that can be used by clients to determine when objects have changed.
                May be used for optimistic concurrency, change detection, and the
                watch operation on a resource or set of resources. Clients must treat
                these values as opaque and passed unmodified back to the server. They
                may only be valid for a particular resource or set of resources. Populated
                by the system. Read-only. Value must be treated as opaque by clients
                and .
              type: str
            self_link:
              description:
              - SelfLink is a URL representing this object. Populated by the system.
                Read-only.
              type: str
            uid:
              description:
              - UID is the unique in time and space value for this object. It is typically
                generated by the server on successful creation of a resource and is
                not allowed to change on PUT operations. Populated by the system.
                Read-only.
              type: str
        spec:
          description: []
          type: complex
          contains:
            env:
              description:
              - Env defines the collection of EnvVar to inject into containers.
              type: list
              contains:
                name:
                  description:
                  - Name of the environment variable. Must be a C_IDENTIFIER.
                  type: str
                value:
                  description:
                  - 'Variable references $(VAR_NAME) are expanded using the previous
                    defined environment variables in the container and any service
                    environment variables. If a variable cannot be resolved, the reference
                    in the input string will be unchanged. The $(VAR_NAME) syntax
                    can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references
                    will never be expanded, regardless of whether the variable exists
                    or not. Defaults to "".'
                  type: str
                value_from:
                  description:
                  - Source for the environment variable's value. Cannot be used if
                    value is not empty.
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
                          - Version of the schema the FieldPath is written in terms
                            of, defaults to "v1".
                          type: str
                        field_path:
                          description:
                          - Path of the field to select in the specified API version.
                          type: str
                    resource_field_ref:
                      description:
                      - 'Selects a resource of the container: only resources limits
                        and requests (limits.cpu, limits.memory, requests.cpu and
                        requests.memory) are currently supported.'
                      type: complex
                      contains:
                        container_name:
                          description:
                          - 'Container name: required for volumes, optional for env
                            vars'
                          type: str
                        divisor:
                          description:
                          - Specifies the output format of the exposed resources,
                            defaults to "1"
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
                          - The key of the secret to select from. Must be a valid
                            secret key.
                          type: str
                        name:
                          description:
                          - Name of the referent.
                          type: str
                        optional:
                          description:
                          - Specify whether the Secret or it's key must be defined
                          type: bool
            env_from:
              description:
              - EnvFrom defines the collection of EnvFromSource to inject into containers.
              type: list
              contains:
                config_map_ref:
                  description:
                  - The ConfigMap to select from
                  type: complex
                  contains:
                    name:
                      description:
                      - Name of the referent.
                      type: str
                    optional:
                      description:
                      - Specify whether the ConfigMap must be defined
                      type: bool
                prefix:
                  description:
                  - An optional identifer to prepend to each key in the ConfigMap.
                    Must be a C_IDENTIFIER.
                  type: str
                secret_ref:
                  description:
                  - The Secret to select from
                  type: complex
                  contains:
                    name:
                      description:
                      - Name of the referent.
                      type: str
                    optional:
                      description:
                      - Specify whether the Secret must be defined
                      type: bool
            selector:
              description:
              - Selector is a label query over a set of resources, in this case pods.
                Required.
              type: complex
              contains:
                match_expressions:
                  description:
                  - matchExpressions is a list of label selector requirements. The
                    requirements are ANDed.
                  type: list
                  contains:
                    key:
                      description:
                      - key is the label key that the selector applies to.
                      type: str
                    operator:
                      description:
                      - operator represents a key's relationship to a set of values.
                        Valid operators ard In, NotIn, Exists and DoesNotExist.
                      type: str
                    values:
                      description:
                      - values is an array of string values. If the operator is In
                        or NotIn, the values array must be non-empty. If the operator
                        is Exists or DoesNotExist, the values array must be empty.
                        This array is replaced during a strategic merge patch.
                      type: list
                      contains: str
                match_labels:
                  description:
                  - matchLabels is a map of {key,value} pairs. A single {key,value}
                    in the matchLabels map is equivalent to an element of matchExpressions,
                    whose key field is "key", the operator is "In", and the values
                    array contains only "value". The requirements are ANDed.
                  type: complex
                  contains: str, str
            volume_mounts:
              description:
              - VolumeMounts defines the collection of VolumeMount to inject into
                containers.
              type: list
              contains:
                mount_path:
                  description:
                  - Path within the container at which the volume should be mounted.
                    Must not contain ':'.
                  type: str
                name:
                  description:
                  - This must match the Name of a Volume.
                  type: str
                read_only:
                  description:
                  - Mounted read-only if true, read-write otherwise (false or unspecified).
                    Defaults to false.
                  type: bool
                sub_path:
                  description:
                  - Path within the volume from which the container's volume should
                    be mounted. Defaults to "" (volume's root).
                  type: str
            volumes:
              description:
              - Volumes defines the collection of Volume to inject into the pod.
              type: list
              contains:
                aws_elastic_block_store:
                  description:
                  - AWSElasticBlockStore represents an AWS Disk resource that is attached
                    to a kubelet's host machine and then exposed to the pod.
                  type: complex
                  contains:
                    fs_type:
                      description:
                      - 'Filesystem type of the volume that you want to mount. Tip:
                        Ensure that the filesystem type is supported by the host operating
                        system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred
                        to be "ext4" if unspecified.'
                      type: str
                    partition:
                      description:
                      - 'The partition in the volume that you want to mount. If omitted,
                        the default is to mount by volume name. Examples: For volume
                        /dev/sda1, you specify the partition as "1". Similarly, the
                        volume partition for /dev/sda is "0" (or you can leave the
                        property empty).'
                      type: int
                    read_only:
                      description:
                      - Specify "true" to force and set the ReadOnly property in VolumeMounts
                        to "true". If omitted, the default is "false".
                      type: bool
                    volume_id:
                      description:
                      - Unique ID of the persistent disk resource in AWS (Amazon EBS
                        volume).
                      type: str
                azure_disk:
                  description:
                  - AzureDisk represents an Azure Data Disk mount on the host and
                    bind mount to the pod.
                  type: complex
                  contains:
                    caching_mode:
                      description:
                      - 'Host Caching mode: None, Read Only, Read Write.'
                      type: str
                    disk_name:
                      description:
                      - The Name of the data disk in the blob storage
                      type: str
                    disk_uri:
                      description:
                      - The URI the data disk in the blob storage
                      type: str
                    fs_type:
                      description:
                      - Filesystem type to mount. Must be a filesystem type supported
                        by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly
                        inferred to be "ext4" if unspecified.
                      type: str
                    kind:
                      description:
                      - 'Expected values Shared: mulitple blob disks per storage account
                        Dedicated: single blob disk per storage account Managed: azure
                        managed data disk (only in managed availability set). defaults
                        to shared'
                      type: str
                    read_only:
                      description:
                      - Defaults to false (read/write). ReadOnly here will force the
                        ReadOnly setting in VolumeMounts.
                      type: bool
                azure_file:
                  description:
                  - AzureFile represents an Azure File Service mount on the host and
                    bind mount to the pod.
                  type: complex
                  contains:
                    read_only:
                      description:
                      - Defaults to false (read/write). ReadOnly here will force the
                        ReadOnly setting in VolumeMounts.
                      type: bool
                    secret_name:
                      description:
                      - the name of secret that contains Azure Storage Account Name
                        and Key
                      type: str
                    share_name:
                      description:
                      - Share Name
                      type: str
                cephfs:
                  description:
                  - CephFS represents a Ceph FS mount on the host that shares a pod's
                    lifetime
                  type: complex
                  contains:
                    monitors:
                      description:
                      - 'Required: Monitors is a collection of Ceph monitors'
                      type: list
                      contains: str
                    path:
                      description:
                      - 'Optional: Used as the mounted root, rather than the full
                        Ceph tree, default is /'
                      type: str
                    read_only:
                      description:
                      - 'Optional: Defaults to false (read/write). ReadOnly here will
                        force the ReadOnly setting in VolumeMounts.'
                      type: bool
                    secret_file:
                      description:
                      - 'Optional: SecretFile is the path to key ring for User, default
                        is /etc/ceph/user.secret'
                      type: str
                    secret_ref:
                      description:
                      - 'Optional: SecretRef is reference to the authentication secret
                        for User, default is empty.'
                      type: complex
                      contains:
                        name:
                          description:
                          - Name of the referent.
                          type: str
                    user:
                      description:
                      - 'Optional: User is the rados user name, default is admin'
                      type: str
                cinder:
                  description:
                  - Cinder represents a cinder volume attached and mounted on kubelets
                    host machine
                  type: complex
                  contains:
                    fs_type:
                      description:
                      - 'Filesystem type to mount. Must be a filesystem type supported
                        by the host operating system. Examples: "ext4", "xfs", "ntfs".
                        Implicitly inferred to be "ext4" if unspecified.'
                      type: str
                    read_only:
                      description:
                      - 'Optional: Defaults to false (read/write). ReadOnly here will
                        force the ReadOnly setting in VolumeMounts.'
                      type: bool
                    volume_id:
                      description:
                      - volume id used to identify the volume in cinder
                      type: str
                config_map:
                  description:
                  - ConfigMap represents a configMap that should populate this volume
                  type: complex
                  contains:
                    default_mode:
                      description:
                      - 'Optional: mode bits to use on created files by default. Must
                        be a value between 0 and 0777. Defaults to 0644. Directories
                        within the path are not affected by this setting. This might
                        be in conflict with other options that affect the file mode,
                        like fsGroup, and the result can be other mode bits set.'
                      type: int
                    items:
                      description:
                      - If unspecified, each key-value pair in the Data field of the
                        referenced ConfigMap will be projected into the volume as
                        a file whose name is the key and content is the value. If
                        specified, the listed keys will be projected into the specified
                        paths, and unlisted keys will not be present. If a key is
                        specified which is not present in the ConfigMap, the volume
                        setup will error unless it is marked optional. Paths must
                        be relative and may not contain the '..' path or start with
                        '..'.
                      type: list
                      contains:
                        key:
                          description:
                          - The key to project.
                          type: str
                        mode:
                          description:
                          - 'Optional: mode bits to use on this file, must be a value
                            between 0 and 0777. If not specified, the volume defaultMode
                            will be used. This might be in conflict with other options
                            that affect the file mode, like fsGroup, and the result
                            can be other mode bits set.'
                          type: int
                        path:
                          description:
                          - The relative path of the file to map the key to. May not
                            be an absolute path. May not contain the path element
                            '..'. May not start with the string '..'.
                          type: str
                    name:
                      description:
                      - Name of the referent.
                      type: str
                    optional:
                      description:
                      - Specify whether the ConfigMap or it's keys must be defined
                      type: bool
                downward_api:
                  description:
                  - DownwardAPI represents downward API about the pod that should
                    populate this volume
                  type: complex
                  contains:
                    default_mode:
                      description:
                      - 'Optional: mode bits to use on created files by default. Must
                        be a value between 0 and 0777. Defaults to 0644. Directories
                        within the path are not affected by this setting. This might
                        be in conflict with other options that affect the file mode,
                        like fsGroup, and the result can be other mode bits set.'
                      type: int
                    items:
                      description:
                      - Items is a list of downward API volume file
                      type: list
                      contains:
                        field_ref:
                          description:
                          - 'Required: Selects a field of the pod: only annotations,
                            labels, name and namespace are supported.'
                          type: complex
                          contains:
                            api_version:
                              description:
                              - Version of the schema the FieldPath is written in
                                terms of, defaults to "v1".
                              type: str
                            field_path:
                              description:
                              - Path of the field to select in the specified API version.
                              type: str
                        mode:
                          description:
                          - 'Optional: mode bits to use on this file, must be a value
                            between 0 and 0777. If not specified, the volume defaultMode
                            will be used. This might be in conflict with other options
                            that affect the file mode, like fsGroup, and the result
                            can be other mode bits set.'
                          type: int
                        path:
                          description:
                          - "Required: Path is the relative path name of the file\
                            \ to be created. Must not be absolute or contain the '..'\
                            \ path. Must be utf-8 encoded. The first item of the relative\
                            \ path must not start with '..'"
                          type: str
                        resource_field_ref:
                          description:
                          - 'Selects a resource of the container: only resources limits
                            and requests (limits.cpu, limits.memory, requests.cpu
                            and requests.memory) are currently supported.'
                          type: complex
                          contains:
                            container_name:
                              description:
                              - 'Container name: required for volumes, optional for
                                env vars'
                              type: str
                            divisor:
                              description:
                              - Specifies the output format of the exposed resources,
                                defaults to "1"
                              type: str
                            resource:
                              description:
                              - 'Required: resource to select'
                              type: str
                empty_dir:
                  description:
                  - EmptyDir represents a temporary directory that shares a pod's
                    lifetime.
                  type: complex
                  contains:
                    medium:
                      description:
                      - What type of storage medium should back this directory. The
                        default is "" which means to use the node's default medium.
                        Must be an empty string (default) or Memory.
                      type: str
                    size_limit:
                      description:
                      - Total amount of local storage required for this EmptyDir volume.
                        The size limit is also applicable for memory medium. The maximum
                        usage on memory medium EmptyDir would be the minimum value
                        between the SizeLimit specified here and the sum of memory
                        limits of all containers in a pod. The default is nil which
                        means that the limit is undefined.
                      type: str
                fc:
                  description:
                  - FC represents a Fibre Channel resource that is attached to a kubelet's
                    host machine and then exposed to the pod.
                  type: complex
                  contains:
                    fs_type:
                      description:
                      - Filesystem type to mount. Must be a filesystem type supported
                        by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly
                        inferred to be "ext4" if unspecified.
                      type: str
                    lun:
                      description:
                      - 'Required: FC target lun number'
                      type: int
                    read_only:
                      description:
                      - 'Optional: Defaults to false (read/write). ReadOnly here will
                        force the ReadOnly setting in VolumeMounts.'
                      type: bool
                    target_ww_ns:
                      description:
                      - 'Required: FC target worldwide names (WWNs)'
                      type: list
                      contains: str
                flex_volume:
                  description:
                  - FlexVolume represents a generic volume resource that is provisioned/attached
                    using an exec based plugin. This is an alpha feature and may change
                    in future.
                  type: complex
                  contains:
                    driver:
                      description:
                      - Driver is the name of the driver to use for this volume.
                      type: str
                    fs_type:
                      description:
                      - Filesystem type to mount. Must be a filesystem type supported
                        by the host operating system. Ex. "ext4", "xfs", "ntfs". The
                        default filesystem depends on FlexVolume script.
                      type: str
                    options:
                      description:
                      - 'Optional: Extra command options if any.'
                      type: complex
                      contains: str, str
                    read_only:
                      description:
                      - 'Optional: Defaults to false (read/write). ReadOnly here will
                        force the ReadOnly setting in VolumeMounts.'
                      type: bool
                    secret_ref:
                      description:
                      - 'Optional: SecretRef is reference to the secret object containing
                        sensitive information to pass to the plugin scripts. This
                        may be empty if no secret object is specified. If the secret
                        object contains more than one secret, all secrets are passed
                        to the plugin scripts.'
                      type: complex
                      contains:
                        name:
                          description:
                          - Name of the referent.
                          type: str
                flocker:
                  description:
                  - Flocker represents a Flocker volume attached to a kubelet's host
                    machine. This depends on the Flocker control service being running
                  type: complex
                  contains:
                    dataset_name:
                      description:
                      - Name of the dataset stored as metadata -> name on the dataset
                        for Flocker should be considered as deprecated
                      type: str
                    dataset_uuid:
                      description:
                      - UUID of the dataset. This is unique identifier of a Flocker
                        dataset
                      type: str
                gce_persistent_disk:
                  description:
                  - GCEPersistentDisk represents a GCE Disk resource that is attached
                    to a kubelet's host machine and then exposed to the pod.
                  type: complex
                  contains:
                    fs_type:
                      description:
                      - 'Filesystem type of the volume that you want to mount. Tip:
                        Ensure that the filesystem type is supported by the host operating
                        system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred
                        to be "ext4" if unspecified.'
                      type: str
                    partition:
                      description:
                      - 'The partition in the volume that you want to mount. If omitted,
                        the default is to mount by volume name. Examples: For volume
                        /dev/sda1, you specify the partition as "1". Similarly, the
                        volume partition for /dev/sda is "0" (or you can leave the
                        property empty).'
                      type: int
                    pd_name:
                      description:
                      - Unique name of the PD resource in GCE. Used to identify the
                        disk in GCE.
                      type: str
                    read_only:
                      description:
                      - ReadOnly here will force the ReadOnly setting in VolumeMounts.
                        Defaults to false.
                      type: bool
                git_repo:
                  description:
                  - GitRepo represents a git repository at a particular revision.
                  type: complex
                  contains:
                    directory:
                      description:
                      - Target directory name. Must not contain or start with '..'.
                        If '.' is supplied, the volume directory will be the git repository.
                        Otherwise, if specified, the volume will contain the git repository
                        in the subdirectory with the given name.
                      type: str
                    repository:
                      description:
                      - Repository URL
                      type: str
                    revision:
                      description:
                      - Commit hash for the specified revision.
                      type: str
                glusterfs:
                  description:
                  - Glusterfs represents a Glusterfs mount on the host that shares
                    a pod's lifetime.
                  type: complex
                  contains:
                    endpoints:
                      description:
                      - EndpointsName is the endpoint name that details Glusterfs
                        topology.
                      type: str
                    path:
                      description:
                      - Path is the Glusterfs volume path.
                      type: str
                    read_only:
                      description:
                      - ReadOnly here will force the Glusterfs volume to be mounted
                        with read-only permissions. Defaults to false.
                      type: bool
                host_path:
                  description:
                  - HostPath represents a pre-existing file or directory on the host
                    machine that is directly exposed to the container. This is generally
                    used for system agents or other privileged things that are allowed
                    to see the host machine. Most containers will NOT need this.
                  type: complex
                  contains:
                    path:
                      description:
                      - Path of the directory on the host.
                      type: str
                iscsi:
                  description:
                  - ISCSI represents an ISCSI Disk resource that is attached to a
                    kubelet's host machine and then exposed to the pod.
                  type: complex
                  contains:
                    chap_auth_discovery:
                      description:
                      - whether support iSCSI Discovery CHAP authentication
                      type: bool
                    chap_auth_session:
                      description:
                      - whether support iSCSI Session CHAP authentication
                      type: bool
                    fs_type:
                      description:
                      - 'Filesystem type of the volume that you want to mount. Tip:
                        Ensure that the filesystem type is supported by the host operating
                        system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred
                        to be "ext4" if unspecified.'
                      type: str
                    iqn:
                      description:
                      - Target iSCSI Qualified Name.
                      type: str
                    iscsi_interface:
                      description:
                      - "Optional: Defaults to 'default' (tcp). iSCSI interface name\
                        \ that uses an iSCSI transport."
                      type: str
                    lun:
                      description:
                      - iSCSI target lun number.
                      type: int
                    portals:
                      description:
                      - iSCSI target portal List. The portal is either an IP or ip_addr:port
                        if the port is other than default (typically TCP ports 860
                        and 3260).
                      type: list
                      contains: str
                    read_only:
                      description:
                      - ReadOnly here will force the ReadOnly setting in VolumeMounts.
                        Defaults to false.
                      type: bool
                    secret_ref:
                      description:
                      - CHAP secret for iSCSI target and initiator authentication
                      type: complex
                      contains:
                        name:
                          description:
                          - Name of the referent.
                          type: str
                    target_portal:
                      description:
                      - iSCSI target portal. The portal is either an IP or ip_addr:port
                        if the port is other than default (typically TCP ports 860
                        and 3260).
                      type: str
                name:
                  description:
                  - Volume's name. Must be a DNS_LABEL and unique within the pod.
                  type: str
                nfs:
                  description:
                  - NFS represents an NFS mount on the host that shares a pod's lifetime
                  type: complex
                  contains:
                    path:
                      description:
                      - Path that is exported by the NFS server.
                      type: str
                    read_only:
                      description:
                      - ReadOnly here will force the NFS export to be mounted with
                        read-only permissions. Defaults to false.
                      type: bool
                    server:
                      description:
                      - Server is the hostname or IP address of the NFS server.
                      type: str
                persistent_volume_claim:
                  description:
                  - PersistentVolumeClaimVolumeSource represents a reference to a
                    PersistentVolumeClaim in the same namespace.
                  type: complex
                  contains:
                    claim_name:
                      description:
                      - ClaimName is the name of a PersistentVolumeClaim in the same
                        namespace as the pod using this volume.
                      type: str
                    read_only:
                      description:
                      - Will force the ReadOnly setting in VolumeMounts. Default false.
                      type: bool
                photon_persistent_disk:
                  description:
                  - PhotonPersistentDisk represents a PhotonController persistent
                    disk attached and mounted on kubelets host machine
                  type: complex
                  contains:
                    fs_type:
                      description:
                      - Filesystem type to mount. Must be a filesystem type supported
                        by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly
                        inferred to be "ext4" if unspecified.
                      type: str
                    pd_id:
                      description:
                      - ID that identifies Photon Controller persistent disk
                      type: str
                portworx_volume:
                  description:
                  - PortworxVolume represents a portworx volume attached and mounted
                    on kubelets host machine
                  type: complex
                  contains:
                    fs_type:
                      description:
                      - FSType represents the filesystem type to mount Must be a filesystem
                        type supported by the host operating system. Ex. "ext4", "xfs".
                        Implicitly inferred to be "ext4" if unspecified.
                      type: str
                    read_only:
                      description:
                      - Defaults to false (read/write). ReadOnly here will force the
                        ReadOnly setting in VolumeMounts.
                      type: bool
                    volume_id:
                      description:
                      - VolumeID uniquely identifies a Portworx volume
                      type: str
                projected:
                  description:
                  - Items for all in one resources secrets, configmaps, and downward
                    API
                  type: complex
                  contains:
                    default_mode:
                      description:
                      - Mode bits to use on created files by default. Must be a value
                        between 0 and 0777. Directories within the path are not affected
                        by this setting. This might be in conflict with other options
                        that affect the file mode, like fsGroup, and the result can
                        be other mode bits set.
                      type: int
                    sources:
                      description:
                      - list of volume projections
                      type: list
                      contains:
                        config_map:
                          description:
                          - information about the configMap data to project
                          type: complex
                          contains:
                            items:
                              description:
                              - If unspecified, each key-value pair in the Data field
                                of the referenced ConfigMap will be projected into
                                the volume as a file whose name is the key and content
                                is the value. If specified, the listed keys will be
                                projected into the specified paths, and unlisted keys
                                will not be present. If a key is specified which is
                                not present in the ConfigMap, the volume setup will
                                error unless it is marked optional. Paths must be
                                relative and may not contain the '..' path or start
                                with '..'.
                              type: list
                              contains:
                                key:
                                  description:
                                  - The key to project.
                                  type: str
                                mode:
                                  description:
                                  - 'Optional: mode bits to use on this file, must
                                    be a value between 0 and 0777. If not specified,
                                    the volume defaultMode will be used. This might
                                    be in conflict with other options that affect
                                    the file mode, like fsGroup, and the result can
                                    be other mode bits set.'
                                  type: int
                                path:
                                  description:
                                  - The relative path of the file to map the key to.
                                    May not be an absolute path. May not contain the
                                    path element '..'. May not start with the string
                                    '..'.
                                  type: str
                            name:
                              description:
                              - Name of the referent.
                              type: str
                            optional:
                              description:
                              - Specify whether the ConfigMap or it's keys must be
                                defined
                              type: bool
                        downward_api:
                          description:
                          - information about the downwardAPI data to project
                          type: complex
                          contains:
                            items:
                              description:
                              - Items is a list of DownwardAPIVolume file
                              type: list
                              contains:
                                field_ref:
                                  description:
                                  - 'Required: Selects a field of the pod: only annotations,
                                    labels, name and namespace are supported.'
                                  type: complex
                                  contains:
                                    api_version:
                                      description:
                                      - Version of the schema the FieldPath is written
                                        in terms of, defaults to "v1".
                                      type: str
                                    field_path:
                                      description:
                                      - Path of the field to select in the specified
                                        API version.
                                      type: str
                                mode:
                                  description:
                                  - 'Optional: mode bits to use on this file, must
                                    be a value between 0 and 0777. If not specified,
                                    the volume defaultMode will be used. This might
                                    be in conflict with other options that affect
                                    the file mode, like fsGroup, and the result can
                                    be other mode bits set.'
                                  type: int
                                path:
                                  description:
                                  - "Required: Path is the relative path name of the\
                                    \ file to be created. Must not be absolute or\
                                    \ contain the '..' path. Must be utf-8 encoded.\
                                    \ The first item of the relative path must not\
                                    \ start with '..'"
                                  type: str
                                resource_field_ref:
                                  description:
                                  - 'Selects a resource of the container: only resources
                                    limits and requests (limits.cpu, limits.memory,
                                    requests.cpu and requests.memory) are currently
                                    supported.'
                                  type: complex
                                  contains:
                                    container_name:
                                      description:
                                      - 'Container name: required for volumes, optional
                                        for env vars'
                                      type: str
                                    divisor:
                                      description:
                                      - Specifies the output format of the exposed
                                        resources, defaults to "1"
                                      type: str
                                    resource:
                                      description:
                                      - 'Required: resource to select'
                                      type: str
                        secret:
                          description:
                          - information about the secret data to project
                          type: complex
                          contains:
                            items:
                              description:
                              - If unspecified, each key-value pair in the Data field
                                of the referenced Secret will be projected into the
                                volume as a file whose name is the key and content
                                is the value. If specified, the listed keys will be
                                projected into the specified paths, and unlisted keys
                                will not be present. If a key is specified which is
                                not present in the Secret, the volume setup will error
                                unless it is marked optional. Paths must be relative
                                and may not contain the '..' path or start with '..'.
                              type: list
                              contains:
                                key:
                                  description:
                                  - The key to project.
                                  type: str
                                mode:
                                  description:
                                  - 'Optional: mode bits to use on this file, must
                                    be a value between 0 and 0777. If not specified,
                                    the volume defaultMode will be used. This might
                                    be in conflict with other options that affect
                                    the file mode, like fsGroup, and the result can
                                    be other mode bits set.'
                                  type: int
                                path:
                                  description:
                                  - The relative path of the file to map the key to.
                                    May not be an absolute path. May not contain the
                                    path element '..'. May not start with the string
                                    '..'.
                                  type: str
                            name:
                              description:
                              - Name of the referent.
                              type: str
                            optional:
                              description:
                              - Specify whether the Secret or its key must be defined
                              type: bool
                quobyte:
                  description:
                  - Quobyte represents a Quobyte mount on the host that shares a pod's
                    lifetime
                  type: complex
                  contains:
                    group:
                      description:
                      - Group to map volume access to Default is no group
                      type: str
                    read_only:
                      description:
                      - ReadOnly here will force the Quobyte volume to be mounted
                        with read-only permissions. Defaults to false.
                      type: bool
                    registry:
                      description:
                      - Registry represents a single or multiple Quobyte Registry
                        services specified as a string as host:port pair (multiple
                        entries are separated with commas) which acts as the central
                        registry for volumes
                      type: str
                    user:
                      description:
                      - User to map volume access to Defaults to serivceaccount user
                      type: str
                    volume:
                      description:
                      - Volume is a string that references an already created Quobyte
                        volume by name.
                      type: str
                rbd:
                  description:
                  - RBD represents a Rados Block Device mount on the host that shares
                    a pod's lifetime.
                  type: complex
                  contains:
                    fs_type:
                      description:
                      - 'Filesystem type of the volume that you want to mount. Tip:
                        Ensure that the filesystem type is supported by the host operating
                        system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred
                        to be "ext4" if unspecified.'
                      type: str
                    image:
                      description:
                      - The rados image name.
                      type: str
                    keyring:
                      description:
                      - Keyring is the path to key ring for RBDUser. Default is /etc/ceph/keyring.
                      type: str
                    monitors:
                      description:
                      - A collection of Ceph monitors.
                      type: list
                      contains: str
                    pool:
                      description:
                      - The rados pool name. Default is rbd.
                      type: str
                    read_only:
                      description:
                      - ReadOnly here will force the ReadOnly setting in VolumeMounts.
                        Defaults to false.
                      type: bool
                    secret_ref:
                      description:
                      - SecretRef is name of the authentication secret for RBDUser.
                        If provided overrides keyring. Default is nil.
                      type: complex
                      contains:
                        name:
                          description:
                          - Name of the referent.
                          type: str
                    user:
                      description:
                      - The rados user name. Default is admin.
                      type: str
                scale_io:
                  description:
                  - ScaleIO represents a ScaleIO persistent volume attached and mounted
                    on Kubernetes nodes.
                  type: complex
                  contains:
                    fs_type:
                      description:
                      - Filesystem type to mount. Must be a filesystem type supported
                        by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly
                        inferred to be "ext4" if unspecified.
                      type: str
                    gateway:
                      description:
                      - The host address of the ScaleIO API Gateway.
                      type: str
                    protection_domain:
                      description:
                      - The name of the Protection Domain for the configured storage
                        (defaults to "default").
                      type: str
                    read_only:
                      description:
                      - Defaults to false (read/write). ReadOnly here will force the
                        ReadOnly setting in VolumeMounts.
                      type: bool
                    secret_ref:
                      description:
                      - SecretRef references to the secret for ScaleIO user and other
                        sensitive information. If this is not provided, Login operation
                        will fail.
                      type: complex
                      contains:
                        name:
                          description:
                          - Name of the referent.
                          type: str
                    ssl_enabled:
                      description:
                      - Flag to enable/disable SSL communication with Gateway, default
                        false
                      type: bool
                    storage_mode:
                      description:
                      - Indicates whether the storage for a volume should be thick
                        or thin (defaults to "thin").
                      type: str
                    storage_pool:
                      description:
                      - The Storage Pool associated with the protection domain (defaults
                        to "default").
                      type: str
                    system:
                      description:
                      - The name of the storage system as configured in ScaleIO.
                      type: str
                    volume_name:
                      description:
                      - The name of a volume already created in the ScaleIO system
                        that is associated with this volume source.
                      type: str
                secret:
                  description:
                  - Secret represents a secret that should populate this volume.
                  type: complex
                  contains:
                    default_mode:
                      description:
                      - 'Optional: mode bits to use on created files by default. Must
                        be a value between 0 and 0777. Defaults to 0644. Directories
                        within the path are not affected by this setting. This might
                        be in conflict with other options that affect the file mode,
                        like fsGroup, and the result can be other mode bits set.'
                      type: int
                    items:
                      description:
                      - If unspecified, each key-value pair in the Data field of the
                        referenced Secret will be projected into the volume as a file
                        whose name is the key and content is the value. If specified,
                        the listed keys will be projected into the specified paths,
                        and unlisted keys will not be present. If a key is specified
                        which is not present in the Secret, the volume setup will
                        error unless it is marked optional. Paths must be relative
                        and may not contain the '..' path or start with '..'.
                      type: list
                      contains:
                        key:
                          description:
                          - The key to project.
                          type: str
                        mode:
                          description:
                          - 'Optional: mode bits to use on this file, must be a value
                            between 0 and 0777. If not specified, the volume defaultMode
                            will be used. This might be in conflict with other options
                            that affect the file mode, like fsGroup, and the result
                            can be other mode bits set.'
                          type: int
                        path:
                          description:
                          - The relative path of the file to map the key to. May not
                            be an absolute path. May not contain the path element
                            '..'. May not start with the string '..'.
                          type: str
                    optional:
                      description:
                      - Specify whether the Secret or it's keys must be defined
                      type: bool
                    secret_name:
                      description:
                      - Name of the secret in the pod's namespace to use.
                      type: str
                storageos:
                  description:
                  - StorageOS represents a StorageOS volume attached and mounted on
                    Kubernetes nodes.
                  type: complex
                  contains:
                    fs_type:
                      description:
                      - Filesystem type to mount. Must be a filesystem type supported
                        by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly
                        inferred to be "ext4" if unspecified.
                      type: str
                    read_only:
                      description:
                      - Defaults to false (read/write). ReadOnly here will force the
                        ReadOnly setting in VolumeMounts.
                      type: bool
                    secret_ref:
                      description:
                      - SecretRef specifies the secret to use for obtaining the StorageOS
                        API credentials. If not specified, default values will be
                        attempted.
                      type: complex
                      contains:
                        name:
                          description:
                          - Name of the referent.
                          type: str
                    volume_name:
                      description:
                      - VolumeName is the human-readable name of the StorageOS volume.
                        Volume names are only unique within a namespace.
                      type: str
                    volume_namespace:
                      description:
                      - VolumeNamespace specifies the scope of the volume within StorageOS.
                        If no namespace is specified then the Pod's namespace will
                        be used. This allows the Kubernetes name scoping to be mirrored
                        within StorageOS for tighter integration. Set VolumeName to
                        any name to override the default behaviour. Set to "default"
                        if you are not using namespaces within StorageOS. Namespaces
                        that do not pre-exist within StorageOS will be created.
                      type: str
                vsphere_volume:
                  description:
                  - VsphereVolume represents a vSphere volume attached and mounted
                    on kubelets host machine
                  type: complex
                  contains:
                    fs_type:
                      description:
                      - Filesystem type to mount. Must be a filesystem type supported
                        by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly
                        inferred to be "ext4" if unspecified.
                      type: str
                    storage_policy_id:
                      description:
                      - Storage Policy Based Management (SPBM) profile ID associated
                        with the StoragePolicyName.
                      type: str
                    storage_policy_name:
                      description:
                      - Storage Policy Based Management (SPBM) profile name.
                      type: str
                    volume_path:
                      description:
                      - Path that identifies vSphere volume vmdk
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
      contains:
        resource_version:
          description:
          - String that identifies the server's internal version of this object that
            can be used by clients to determine when objects have changed. Value must
            be treated as opaque by clients and passed unmodified back to the server.
            Populated by the system. Read-only.
          type: str
        self_link:
          description:
          - SelfLink is a URL representing this object. Populated by the system. Read-only.
          type: str
'''


def main():
    try:
        module = KubernetesAnsibleModule('pod_preset_list', 'v1alpha1')
    except KubernetesAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except KubernetesAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
