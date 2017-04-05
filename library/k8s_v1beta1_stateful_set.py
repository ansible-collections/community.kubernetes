#!/usr/bin/env python

from ansible.module_utils.k8s_common import KubernetesAnsibleModule, KubernetesAnsibleException

DOCUMENTATION = '''
module: k8s_v1beta1_stateful_set
short_description: Kubernetes StatefulSet
description:
- Manage the lifecycle of a stateful_set object. Supports check mode, and attempts
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
  spec_replicas:
    description:
    - Replicas is the desired number of replicas of the given Template. These are
      replicas in the sense that they are instantiations of the same Template, but
      individual replicas also have a consistent identity. If unspecified, defaults
      to 1.
    aliases:
    - replicas
    type: int
  spec_selector_match_expressions:
    description:
    - matchExpressions is a list of label selector requirements. The requirements
      are ANDed.
    aliases:
    - selector_match_expressions
    type: list
  spec_selector_match_labels:
    description:
    - matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels
      map is equivalent to an element of matchExpressions, whose key field is "key",
      the operator is "In", and the values array contains only "value". The requirements
      are ANDed.
    aliases:
    - selector_match_labels
    type: dict
  spec_service_name:
    description:
    - 'ServiceName is the name of the service that governs this StatefulSet. This
      service must exist before the StatefulSet, and is responsible for the network
      identity of the set. Pods get DNS/hostnames that follow the pattern: pod-specific-string.serviceName.default.svc.cluster.local
      where "pod-specific-string" is managed by the StatefulSet controller.'
    aliases:
    - service_name
  spec_template_metadata_annotations:
    description:
    - Annotations is an unstructured key value map stored with a resource that may
      be set by external tools to store and retrieve arbitrary metadata. They are
      not queryable and should be preserved when modifying objects.
    type: dict
  spec_template_metadata_labels:
    description:
    - Map of string keys and values that can be used to organize and categorize (scope
      and select) objects. May match selectors of replication controllers and services.
    type: dict
  spec_template_metadata_name:
    description:
    - Name must be unique within a namespace. Is required when creating resources,
      although some resources may allow a client to request the generation of an appropriate
      name automatically. Name is primarily intended for creation idempotence and
      configuration definition. Cannot be updated.
  spec_template_metadata_namespace:
    description:
    - Namespace defines the space within each name must be unique. An empty namespace
      is equivalent to the "default" namespace, but "default" is the canonical representation.
      Not all objects are required to be scoped to a namespace - the value of this
      field for those objects will be empty. Must be a DNS_LABEL. Cannot be updated.
  spec_template_spec_active_deadline_seconds:
    description:
    - Optional duration in seconds the pod may be active on the node relative to StartTime
      before the system will actively try to mark it failed and kill associated containers.
      Value must be a positive integer.
    aliases:
    - active_deadline_seconds
    type: int
  spec_template_spec_containers:
    description:
    - List of containers belonging to the pod. Containers cannot currently be added
      or removed. There must be at least one container in a Pod. Cannot be updated.
    aliases:
    - containers
    type: list
  spec_template_spec_dns_policy:
    description:
    - Set DNS policy for containers within the pod. One of 'ClusterFirst' or 'Default'.
      Defaults to "ClusterFirst".
    aliases:
    - dns_policy
  spec_template_spec_host_ipc:
    description:
    - "Use the host's ipc namespace. Optional: Default to false."
    aliases:
    - host_ipc
    type: bool
  spec_template_spec_host_network:
    description:
    - Host networking requested for this pod. Use the host's network namespace. If
      this option is set, the ports that will be used must be specified. Default to
      false.
    aliases:
    - host_network
    type: bool
  spec_template_spec_host_pid:
    description:
    - "Use the host's pid namespace. Optional: Default to false."
    aliases:
    - host_pid
    type: bool
  spec_template_spec_hostname:
    description:
    - Specifies the hostname of the Pod If not specified, the pod's hostname will
      be set to a system-defined value.
    aliases:
    - hostname
  spec_template_spec_image_pull_secrets:
    description:
    - ImagePullSecrets is an optional list of references to secrets in the same namespace
      to use for pulling any of the images used by this PodSpec. If specified, these
      secrets will be passed to individual puller implementations for them to use.
      For example, in the case of docker, only DockerConfig type secrets are honored.
    aliases:
    - image_pull_secrets
    type: list
  spec_template_spec_node_name:
    description:
    - NodeName is a request to schedule this pod onto a specific node. If it is non-empty,
      the scheduler simply schedules this pod onto that node, assuming that it fits
      resource requirements.
    aliases:
    - node_name
  spec_template_spec_node_selector:
    description:
    - NodeSelector is a selector which must be true for the pod to fit on a node.
      Selector which must match a node's labels for the pod to be scheduled on that
      node.
    aliases:
    - node_selector
    type: dict
  spec_template_spec_restart_policy:
    description:
    - Restart policy for all containers within the pod. One of Always, OnFailure,
      Never. Default to Always.
    aliases:
    - restart_policy
  spec_template_spec_security_context_fs_group:
    description:
    - "A special supplemental group that applies to all containers in a pod. Some\
      \ volume types allow the Kubelet to change the ownership of that volume to be\
      \ owned by the pod: 1. The owning GID will be the FSGroup 2. The setgid bit\
      \ is set (new files created in the volume will be owned by FSGroup) 3. The permission\
      \ bits are OR'd with rw-rw---- If unset, the Kubelet will not modify the ownership\
      \ and permissions of any volume."
    aliases:
    - security_context_fs_group
    type: int
  spec_template_spec_security_context_run_as_non_root:
    description:
    - Indicates that the container must run as a non-root user. If true, the Kubelet
      will validate the image at runtime to ensure that it does not run as UID 0 (root)
      and fail to start the container if it does. If unset or false, no such validation
      will be performed. May also be set in SecurityContext. If set in both SecurityContext
      and PodSecurityContext, the value specified in SecurityContext takes precedence.
    aliases:
    - security_context_run_as_non_root
    type: bool
  spec_template_spec_security_context_run_as_user:
    description:
    - The UID to run the entrypoint of the container process. Defaults to user specified
      in image metadata if unspecified. May also be set in SecurityContext. If set
      in both SecurityContext and PodSecurityContext, the value specified in SecurityContext
      takes precedence for that container.
    aliases:
    - security_context_run_as_user
    type: int
  spec_template_spec_security_context_se_linux_options_level:
    description:
    - Level is SELinux level label that applies to the container.
    aliases:
    - security_context_se_linux_options_level
  spec_template_spec_security_context_se_linux_options_role:
    description:
    - Role is a SELinux role label that applies to the container.
    aliases:
    - security_context_se_linux_options_role
  spec_template_spec_security_context_se_linux_options_type:
    description:
    - Type is a SELinux type label that applies to the container.
    aliases:
    - security_context_se_linux_options_type
  spec_template_spec_security_context_se_linux_options_user:
    description:
    - User is a SELinux user label that applies to the container.
    aliases:
    - security_context_se_linux_options_user
  spec_template_spec_security_context_supplemental_groups:
    description:
    - A list of groups applied to the first process run in each container, in addition
      to the container's primary GID. If unspecified, no groups will be added to any
      container.
    aliases:
    - security_context_supplemental_groups
    type: list
  spec_template_spec_service_account:
    description:
    - 'DeprecatedServiceAccount is a depreciated alias for ServiceAccountName. Deprecated:
      Use serviceAccountName instead.'
    aliases:
    - service_account
  spec_template_spec_service_account_name:
    description:
    - ServiceAccountName is the name of the ServiceAccount to use to run this pod.
    aliases:
    - service_account_name
  spec_template_spec_subdomain:
    description:
    - If specified, the fully qualified Pod hostname will be "<hostname>.<subdomain>.<pod
      namespace>.svc.<cluster domain>". If not specified, the pod will not have a
      domainname at all.
    aliases:
    - subdomain
  spec_template_spec_termination_grace_period_seconds:
    description:
    - Optional duration in seconds the pod needs to terminate gracefully. May be decreased
      in delete request. Value must be non-negative integer. The value zero indicates
      delete immediately. If this value is nil, the default grace period will be used
      instead. The grace period is the duration in seconds after the processes running
      in the pod are sent a termination signal and the time when the processes are
      forcibly halted with a kill signal. Set this value longer than the expected
      cleanup time for your process. Defaults to 30 seconds.
    aliases:
    - termination_grace_period_seconds
    type: int
  spec_template_spec_volumes:
    description:
    - List of volumes that can be mounted by containers belonging to the pod.
    aliases:
    - volumes
    type: list
  spec_volume_claim_templates:
    description:
    - VolumeClaimTemplates is a list of claims that pods are allowed to reference.
      The StatefulSet controller is responsible for mapping network identities to
      claims in a way that maintains the identity of a pod. Every claim in this list
      must have at least one matching (by name) volumeMount in one container in the
      template. A claim in this list takes precedence over any volumes in the template,
      with the same name.
    aliases:
    - volume_claim_templates
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
- kubernetes == 1.0.0
'''

EXAMPLES = '''
'''

RETURN = '''
api_version:
  type: string
  description: Requested API version
stateful_set:
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
    spec:
      description:
      - Spec defines the desired identities of pods in this set.
      type: complex
      contains:
        replicas:
          description:
          - Replicas is the desired number of replicas of the given Template. These
            are replicas in the sense that they are instantiations of the same Template,
            but individual replicas also have a consistent identity. If unspecified,
            defaults to 1.
          type: int
        selector:
          description:
          - Selector is a label query over pods that should match the replica count.
            If empty, defaulted to labels on the pod template.
          type: complex
          contains:
            match_expressions:
              description:
              - matchExpressions is a list of label selector requirements. The requirements
                are ANDed.
              type: list
              contains:
                key:
                  description:
                  - key is the label key that the selector applies to.
                  type: str
                operator:
                  description:
                  - operator represents a key's relationship to a set of values. Valid
                    operators ard In, NotIn, Exists and DoesNotExist.
                  type: str
                values:
                  description:
                  - values is an array of string values. If the operator is In or
                    NotIn, the values array must be non-empty. If the operator is
                    Exists or DoesNotExist, the values array must be empty. This array
                    is replaced during a strategic merge patch.
                  type: list
                  contains: str
            match_labels:
              description:
              - matchLabels is a map of {key,value} pairs. A single {key,value} in
                the matchLabels map is equivalent to an element of matchExpressions,
                whose key field is "key", the operator is "In", and the values array
                contains only "value". The requirements are ANDed.
              type: complex
              contains: str, str
        service_name:
          description:
          - 'ServiceName is the name of the service that governs this StatefulSet.
            This service must exist before the StatefulSet, and is responsible for
            the network identity of the set. Pods get DNS/hostnames that follow the
            pattern: pod-specific-string.serviceName.default.svc.cluster.local where
            "pod-specific-string" is managed by the StatefulSet controller.'
          type: str
        template:
          description:
          - Template is the object that describes the pod that will be created if
            insufficient replicas are detected. Each pod stamped out by the StatefulSet
            will fulfill this Template, but have a unique identity from the rest of
            the StatefulSet.
          type: complex
          contains:
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
            spec:
              description:
              - Specification of the desired behavior of the pod.
              type: complex
              contains:
                active_deadline_seconds:
                  description:
                  - Optional duration in seconds the pod may be active on the node
                    relative to StartTime before the system will actively try to mark
                    it failed and kill associated containers. Value must be a positive
                    integer.
                  type: int
                containers:
                  description:
                  - List of containers belonging to the pod. Containers cannot currently
                    be added or removed. There must be at least one container in a
                    Pod. Cannot be updated.
                  type: list
                  contains:
                    args:
                      description:
                      - "Arguments to the entrypoint. The docker image's CMD is used\
                        \ if this is not provided. Variable references $(VAR_NAME)\
                        \ are expanded using the container's environment. If a variable\
                        \ cannot be resolved, the reference in the input string will\
                        \ be unchanged. The $(VAR_NAME) syntax can be escaped with\
                        \ a double $$, ie: $$(VAR_NAME). Escaped references will never\
                        \ be expanded, regardless of whether the variable exists or\
                        \ not. Cannot be updated."
                      type: list
                      contains: str
                    command:
                      description:
                      - "Entrypoint array. Not executed within a shell. The docker\
                        \ image's ENTRYPOINT is used if this is not provided. Variable\
                        \ references $(VAR_NAME) are expanded using the container's\
                        \ environment. If a variable cannot be resolved, the reference\
                        \ in the input string will be unchanged. The $(VAR_NAME) syntax\
                        \ can be escaped with a double $$, ie: $$(VAR_NAME). Escaped\
                        \ references will never be expanded, regardless of whether\
                        \ the variable exists or not. Cannot be updated."
                      type: list
                      contains: str
                    env:
                      description:
                      - List of environment variables to set in the container. Cannot
                        be updated.
                      type: list
                      contains:
                        name:
                          description:
                          - Name of the environment variable. Must be a C_IDENTIFIER.
                          type: str
                        value:
                          description:
                          - 'Variable references $(VAR_NAME) are expanded using the
                            previous defined environment variables in the container
                            and any service environment variables. If a variable cannot
                            be resolved, the reference in the input string will be
                            unchanged. The $(VAR_NAME) syntax can be escaped with
                            a double $$, ie: $$(VAR_NAME). Escaped references will
                            never be expanded, regardless of whether the variable
                            exists or not. Defaults to "".'
                          type: str
                        value_from:
                          description:
                          - Source for the environment variable's value. Cannot be
                            used if value is not empty.
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
                            field_ref:
                              description:
                              - 'Selects a field of the pod: supports metadata.name,
                                metadata.namespace, metadata.labels, metadata.annotations,
                                spec.nodeName, spec.serviceAccountName, status.podIP.'
                              type: complex
                              contains:
                                api_version:
                                  description:
                                  - Version of the schema the FieldPath is written
                                    in terms of, defaults to "v1".
                                  type: str
                                field_path:
                                  description:
                                  - Path of the field to select in the specified API
                                    version.
                                  type: str
                            resource_field_ref:
                              description:
                              - 'Selects a resource of the container: only resources
                                limits and requests (limits.cpu, limits.memory, requests.cpu
                                and requests.memory) are currently supported.'
                              type: complex
                              contains:
                                container_name:
                                  description:
                                  - 'Container name: required for volumes, optional
                                    for env vars'
                                  type: str
                                divisor:
                                  description:
                                  - Specifies the output format of the exposed resources,
                                    defaults to "1"
                                  type: complex
                                  contains: {}
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
                                  - The key of the secret to select from. Must be
                                    a valid secret key.
                                  type: str
                                name:
                                  description:
                                  - Name of the referent.
                                  type: str
                    image:
                      description:
                      - Docker image name.
                      type: str
                    image_pull_policy:
                      description:
                      - Image pull policy. One of Always, Never, IfNotPresent. Defaults
                        to Always if :latest tag is specified, or IfNotPresent otherwise.
                        Cannot be updated.
                      type: str
                    lifecycle:
                      description:
                      - Actions that the management system should take in response
                        to container lifecycle events. Cannot be updated.
                      type: complex
                      contains:
                        post_start:
                          description:
                          - PostStart is called immediately after a container is created.
                            If the handler fails, the container is terminated and
                            restarted according to its restart policy. Other management
                            of the container blocks until the hook completes.
                          type: complex
                          contains:
                            _exec:
                              description:
                              - One and only one of the following should be specified.
                                Exec specifies the action to take.
                              type: complex
                              contains:
                                command:
                                  description:
                                  - Command is the command line to execute inside
                                    the container, the working directory for the command
                                    is root ('/') in the container's filesystem. The
                                    command is simply exec'd, it is not run inside
                                    a shell, so traditional shell instructions ('|',
                                    etc) won't work. To use a shell, you need to explicitly
                                    call out to that shell. Exit status of 0 is treated
                                    as live/healthy and non-zero is unhealthy.
                                  type: list
                                  contains: str
                            http_get:
                              description:
                              - HTTPGet specifies the http request to perform.
                              type: complex
                              contains:
                                host:
                                  description:
                                  - Host name to connect to, defaults to the pod IP.
                                    You probably want to set "Host" in httpHeaders
                                    instead.
                                  type: str
                                http_headers:
                                  description:
                                  - Custom headers to set in the request. HTTP allows
                                    repeated headers.
                                  type: list
                                  contains:
                                    name:
                                      description:
                                      - The header field name
                                      type: str
                                    value:
                                      description:
                                      - The header field value
                                      type: str
                                path:
                                  description:
                                  - Path to access on the HTTP server.
                                  type: str
                                port:
                                  description:
                                  - Name or number of the port to access on the container.
                                    Number must be in the range 1 to 65535. Name must
                                    be an IANA_SVC_NAME.
                                  type: complex
                                  contains: {}
                                scheme:
                                  description:
                                  - Scheme to use for connecting to the host. Defaults
                                    to HTTP.
                                  type: str
                            tcp_socket:
                              description:
                              - TCPSocket specifies an action involving a TCP port.
                                TCP hooks not yet supported
                              type: complex
                              contains:
                                port:
                                  description:
                                  - Number or name of the port to access on the container.
                                    Number must be in the range 1 to 65535. Name must
                                    be an IANA_SVC_NAME.
                                  type: complex
                                  contains: {}
                        pre_stop:
                          description:
                          - PreStop is called immediately before a container is terminated.
                            The container is terminated after the handler completes.
                            The reason for termination is passed to the handler. Regardless
                            of the outcome of the handler, the container is eventually
                            terminated. Other management of the container blocks until
                            the hook completes.
                          type: complex
                          contains:
                            _exec:
                              description:
                              - One and only one of the following should be specified.
                                Exec specifies the action to take.
                              type: complex
                              contains:
                                command:
                                  description:
                                  - Command is the command line to execute inside
                                    the container, the working directory for the command
                                    is root ('/') in the container's filesystem. The
                                    command is simply exec'd, it is not run inside
                                    a shell, so traditional shell instructions ('|',
                                    etc) won't work. To use a shell, you need to explicitly
                                    call out to that shell. Exit status of 0 is treated
                                    as live/healthy and non-zero is unhealthy.
                                  type: list
                                  contains: str
                            http_get:
                              description:
                              - HTTPGet specifies the http request to perform.
                              type: complex
                              contains:
                                host:
                                  description:
                                  - Host name to connect to, defaults to the pod IP.
                                    You probably want to set "Host" in httpHeaders
                                    instead.
                                  type: str
                                http_headers:
                                  description:
                                  - Custom headers to set in the request. HTTP allows
                                    repeated headers.
                                  type: list
                                  contains:
                                    name:
                                      description:
                                      - The header field name
                                      type: str
                                    value:
                                      description:
                                      - The header field value
                                      type: str
                                path:
                                  description:
                                  - Path to access on the HTTP server.
                                  type: str
                                port:
                                  description:
                                  - Name or number of the port to access on the container.
                                    Number must be in the range 1 to 65535. Name must
                                    be an IANA_SVC_NAME.
                                  type: complex
                                  contains: {}
                                scheme:
                                  description:
                                  - Scheme to use for connecting to the host. Defaults
                                    to HTTP.
                                  type: str
                            tcp_socket:
                              description:
                              - TCPSocket specifies an action involving a TCP port.
                                TCP hooks not yet supported
                              type: complex
                              contains:
                                port:
                                  description:
                                  - Number or name of the port to access on the container.
                                    Number must be in the range 1 to 65535. Name must
                                    be an IANA_SVC_NAME.
                                  type: complex
                                  contains: {}
                    liveness_probe:
                      description:
                      - Periodic probe of container liveness. Container will be restarted
                        if the probe fails. Cannot be updated.
                      type: complex
                      contains:
                        _exec:
                          description:
                          - One and only one of the following should be specified.
                            Exec specifies the action to take.
                          type: complex
                          contains:
                            command:
                              description:
                              - Command is the command line to execute inside the
                                container, the working directory for the command is
                                root ('/') in the container's filesystem. The command
                                is simply exec'd, it is not run inside a shell, so
                                traditional shell instructions ('|', etc) won't work.
                                To use a shell, you need to explicitly call out to
                                that shell. Exit status of 0 is treated as live/healthy
                                and non-zero is unhealthy.
                              type: list
                              contains: str
                        failure_threshold:
                          description:
                          - Minimum consecutive failures for the probe to be considered
                            failed after having succeeded. Defaults to 3. Minimum
                            value is 1.
                          type: int
                        http_get:
                          description:
                          - HTTPGet specifies the http request to perform.
                          type: complex
                          contains:
                            host:
                              description:
                              - Host name to connect to, defaults to the pod IP. You
                                probably want to set "Host" in httpHeaders instead.
                              type: str
                            http_headers:
                              description:
                              - Custom headers to set in the request. HTTP allows
                                repeated headers.
                              type: list
                              contains:
                                name:
                                  description:
                                  - The header field name
                                  type: str
                                value:
                                  description:
                                  - The header field value
                                  type: str
                            path:
                              description:
                              - Path to access on the HTTP server.
                              type: str
                            port:
                              description:
                              - Name or number of the port to access on the container.
                                Number must be in the range 1 to 65535. Name must
                                be an IANA_SVC_NAME.
                              type: complex
                              contains: {}
                            scheme:
                              description:
                              - Scheme to use for connecting to the host. Defaults
                                to HTTP.
                              type: str
                        initial_delay_seconds:
                          description:
                          - Number of seconds after the container has started before
                            liveness probes are initiated.
                          type: int
                        period_seconds:
                          description:
                          - How often (in seconds) to perform the probe. Default to
                            10 seconds. Minimum value is 1.
                          type: int
                        success_threshold:
                          description:
                          - Minimum consecutive successes for the probe to be considered
                            successful after having failed. Defaults to 1. Must be
                            1 for liveness. Minimum value is 1.
                          type: int
                        tcp_socket:
                          description:
                          - TCPSocket specifies an action involving a TCP port. TCP
                            hooks not yet supported
                          type: complex
                          contains:
                            port:
                              description:
                              - Number or name of the port to access on the container.
                                Number must be in the range 1 to 65535. Name must
                                be an IANA_SVC_NAME.
                              type: complex
                              contains: {}
                        timeout_seconds:
                          description:
                          - Number of seconds after which the probe times out. Defaults
                            to 1 second. Minimum value is 1.
                          type: int
                    name:
                      description:
                      - Name of the container specified as a DNS_LABEL. Each container
                        in a pod must have a unique name (DNS_LABEL). Cannot be updated.
                      type: str
                    ports:
                      description:
                      - List of ports to expose from the container. Exposing a port
                        here gives the system additional information about the network
                        connections a container uses, but is primarily informational.
                        Not specifying a port here DOES NOT prevent that port from
                        being exposed. Any port which is listening on the default
                        "0.0.0.0" address inside a container will be accessible from
                        the network. Cannot be updated.
                      type: list
                      contains:
                        container_port:
                          description:
                          - Number of port to expose on the pod's IP address. This
                            must be a valid port number, 0 < x < 65536.
                          type: int
                        host_ip:
                          description:
                          - What host IP to bind the external port to.
                          type: str
                        host_port:
                          description:
                          - Number of port to expose on the host. If specified, this
                            must be a valid port number, 0 < x < 65536. If HostNetwork
                            is specified, this must match ContainerPort. Most containers
                            do not need this.
                          type: int
                        name:
                          description:
                          - If specified, this must be an IANA_SVC_NAME and unique
                            within the pod. Each named port in a pod must have a unique
                            name. Name for the port that can be referred to by services.
                          type: str
                        protocol:
                          description:
                          - Protocol for port. Must be UDP or TCP. Defaults to "TCP".
                          type: str
                    readiness_probe:
                      description:
                      - Periodic probe of container service readiness. Container will
                        be removed from service endpoints if the probe fails. Cannot
                        be updated.
                      type: complex
                      contains:
                        _exec:
                          description:
                          - One and only one of the following should be specified.
                            Exec specifies the action to take.
                          type: complex
                          contains:
                            command:
                              description:
                              - Command is the command line to execute inside the
                                container, the working directory for the command is
                                root ('/') in the container's filesystem. The command
                                is simply exec'd, it is not run inside a shell, so
                                traditional shell instructions ('|', etc) won't work.
                                To use a shell, you need to explicitly call out to
                                that shell. Exit status of 0 is treated as live/healthy
                                and non-zero is unhealthy.
                              type: list
                              contains: str
                        failure_threshold:
                          description:
                          - Minimum consecutive failures for the probe to be considered
                            failed after having succeeded. Defaults to 3. Minimum
                            value is 1.
                          type: int
                        http_get:
                          description:
                          - HTTPGet specifies the http request to perform.
                          type: complex
                          contains:
                            host:
                              description:
                              - Host name to connect to, defaults to the pod IP. You
                                probably want to set "Host" in httpHeaders instead.
                              type: str
                            http_headers:
                              description:
                              - Custom headers to set in the request. HTTP allows
                                repeated headers.
                              type: list
                              contains:
                                name:
                                  description:
                                  - The header field name
                                  type: str
                                value:
                                  description:
                                  - The header field value
                                  type: str
                            path:
                              description:
                              - Path to access on the HTTP server.
                              type: str
                            port:
                              description:
                              - Name or number of the port to access on the container.
                                Number must be in the range 1 to 65535. Name must
                                be an IANA_SVC_NAME.
                              type: complex
                              contains: {}
                            scheme:
                              description:
                              - Scheme to use for connecting to the host. Defaults
                                to HTTP.
                              type: str
                        initial_delay_seconds:
                          description:
                          - Number of seconds after the container has started before
                            liveness probes are initiated.
                          type: int
                        period_seconds:
                          description:
                          - How often (in seconds) to perform the probe. Default to
                            10 seconds. Minimum value is 1.
                          type: int
                        success_threshold:
                          description:
                          - Minimum consecutive successes for the probe to be considered
                            successful after having failed. Defaults to 1. Must be
                            1 for liveness. Minimum value is 1.
                          type: int
                        tcp_socket:
                          description:
                          - TCPSocket specifies an action involving a TCP port. TCP
                            hooks not yet supported
                          type: complex
                          contains:
                            port:
                              description:
                              - Number or name of the port to access on the container.
                                Number must be in the range 1 to 65535. Name must
                                be an IANA_SVC_NAME.
                              type: complex
                              contains: {}
                        timeout_seconds:
                          description:
                          - Number of seconds after which the probe times out. Defaults
                            to 1 second. Minimum value is 1.
                          type: int
                    resources:
                      description:
                      - Compute Resources required by this container. Cannot be updated.
                      type: complex
                      contains:
                        limits:
                          description:
                          - Limits describes the maximum amount of compute resources
                            allowed.
                          type: complex
                          contains: str, ResourceQuantity
                        requests:
                          description:
                          - Requests describes the minimum amount of compute resources
                            required. If Requests is omitted for a container, it defaults
                            to Limits if that is explicitly specified, otherwise to
                            an implementation-defined value.
                          type: complex
                          contains: str, ResourceQuantity
                    security_context:
                      description:
                      - Security options the pod should run with.
                      type: complex
                      contains:
                        capabilities:
                          description:
                          - The capabilities to add/drop when running containers.
                            Defaults to the default set of capabilities granted by
                            the container runtime.
                          type: complex
                          contains:
                            add:
                              description:
                              - Added capabilities
                              type: list
                              contains: str
                            drop:
                              description:
                              - Removed capabilities
                              type: list
                              contains: str
                        privileged:
                          description:
                          - Run container in privileged mode. Processes in privileged
                            containers are essentially equivalent to root on the host.
                            Defaults to false.
                          type: bool
                        read_only_root_filesystem:
                          description:
                          - Whether this container has a read-only root filesystem.
                            Default is false.
                          type: bool
                        run_as_non_root:
                          description:
                          - Indicates that the container must run as a non-root user.
                            If true, the Kubelet will validate the image at runtime
                            to ensure that it does not run as UID 0 (root) and fail
                            to start the container if it does. If unset or false,
                            no such validation will be performed. May also be set
                            in PodSecurityContext. If set in both SecurityContext
                            and PodSecurityContext, the value specified in SecurityContext
                            takes precedence.
                          type: bool
                        run_as_user:
                          description:
                          - The UID to run the entrypoint of the container process.
                            Defaults to user specified in image metadata if unspecified.
                            May also be set in PodSecurityContext. If set in both
                            SecurityContext and PodSecurityContext, the value specified
                            in SecurityContext takes precedence.
                          type: int
                        se_linux_options:
                          description:
                          - The SELinux context to be applied to the container. If
                            unspecified, the container runtime will allocate a random
                            SELinux context for each container. May also be set in
                            PodSecurityContext. If set in both SecurityContext and
                            PodSecurityContext, the value specified in SecurityContext
                            takes precedence.
                          type: complex
                          contains:
                            level:
                              description:
                              - Level is SELinux level label that applies to the container.
                              type: str
                            role:
                              description:
                              - Role is a SELinux role label that applies to the container.
                              type: str
                            type:
                              description:
                              - Type is a SELinux type label that applies to the container.
                              type: str
                            user:
                              description:
                              - User is a SELinux user label that applies to the container.
                              type: str
                    stdin:
                      description:
                      - Whether this container should allocate a buffer for stdin
                        in the container runtime. If this is not set, reads from stdin
                        in the container will always result in EOF. Default is false.
                      type: bool
                    stdin_once:
                      description:
                      - Whether the container runtime should close the stdin channel
                        after it has been opened by a single attach. When stdin is
                        true the stdin stream will remain open across multiple attach
                        sessions. If stdinOnce is set to true, stdin is opened on
                        container start, is empty until the first client attaches
                        to stdin, and then remains open and accepts data until the
                        client disconnects, at which time stdin is closed and remains
                        closed until the container is restarted. If this flag is false,
                        a container processes that reads from stdin will never receive
                        an EOF. Default is false
                      type: bool
                    termination_message_path:
                      description:
                      - "Optional: Path at which the file to which the container's\
                        \ termination message will be written is mounted into the\
                        \ container's filesystem. Message written is intended to be\
                        \ brief final status, such as an assertion failure message.\
                        \ Defaults to /dev/termination-log. Cannot be updated."
                      type: str
                    tty:
                      description:
                      - Whether this container should allocate a TTY for itself, also
                        requires 'stdin' to be true. Default is false.
                      type: bool
                    volume_mounts:
                      description:
                      - Pod volumes to mount into the container's filesystem. Cannot
                        be updated.
                      type: list
                      contains:
                        mount_path:
                          description:
                          - Path within the container at which the volume should be
                            mounted. Must not contain ':'.
                          type: str
                        name:
                          description:
                          - This must match the Name of a Volume.
                          type: str
                        read_only:
                          description:
                          - Mounted read-only if true, read-write otherwise (false
                            or unspecified). Defaults to false.
                          type: bool
                        sub_path:
                          description:
                          - Path within the volume from which the container's volume
                            should be mounted. Defaults to "" (volume's root).
                          type: str
                    working_dir:
                      description:
                      - Container's working directory. If not specified, the container
                        runtime's default will be used, which might be configured
                        in the container image. Cannot be updated.
                      type: str
                dns_policy:
                  description:
                  - Set DNS policy for containers within the pod. One of 'ClusterFirst'
                    or 'Default'. Defaults to "ClusterFirst".
                  type: str
                host_ipc:
                  description:
                  - "Use the host's ipc namespace. Optional: Default to false."
                  type: bool
                host_network:
                  description:
                  - Host networking requested for this pod. Use the host's network
                    namespace. If this option is set, the ports that will be used
                    must be specified. Default to false.
                  type: bool
                host_pid:
                  description:
                  - "Use the host's pid namespace. Optional: Default to false."
                  type: bool
                hostname:
                  description:
                  - Specifies the hostname of the Pod If not specified, the pod's
                    hostname will be set to a system-defined value.
                  type: str
                image_pull_secrets:
                  description:
                  - ImagePullSecrets is an optional list of references to secrets
                    in the same namespace to use for pulling any of the images used
                    by this PodSpec. If specified, these secrets will be passed to
                    individual puller implementations for them to use. For example,
                    in the case of docker, only DockerConfig type secrets are honored.
                  type: list
                  contains:
                    name:
                      description:
                      - Name of the referent.
                      type: str
                node_name:
                  description:
                  - NodeName is a request to schedule this pod onto a specific node.
                    If it is non-empty, the scheduler simply schedules this pod onto
                    that node, assuming that it fits resource requirements.
                  type: str
                node_selector:
                  description:
                  - NodeSelector is a selector which must be true for the pod to fit
                    on a node. Selector which must match a node's labels for the pod
                    to be scheduled on that node.
                  type: complex
                  contains: str, str
                restart_policy:
                  description:
                  - Restart policy for all containers within the pod. One of Always,
                    OnFailure, Never. Default to Always.
                  type: str
                security_context:
                  description:
                  - 'SecurityContext holds pod-level security attributes and common
                    container settings. Optional: Defaults to empty. See type description
                    for default values of each field.'
                  type: complex
                  contains:
                    fs_group:
                      description:
                      - "A special supplemental group that applies to all containers\
                        \ in a pod. Some volume types allow the Kubelet to change\
                        \ the ownership of that volume to be owned by the pod: 1.\
                        \ The owning GID will be the FSGroup 2. The setgid bit is\
                        \ set (new files created in the volume will be owned by FSGroup)\
                        \ 3. The permission bits are OR'd with rw-rw---- If unset,\
                        \ the Kubelet will not modify the ownership and permissions\
                        \ of any volume."
                      type: int
                    run_as_non_root:
                      description:
                      - Indicates that the container must run as a non-root user.
                        If true, the Kubelet will validate the image at runtime to
                        ensure that it does not run as UID 0 (root) and fail to start
                        the container if it does. If unset or false, no such validation
                        will be performed. May also be set in SecurityContext. If
                        set in both SecurityContext and PodSecurityContext, the value
                        specified in SecurityContext takes precedence.
                      type: bool
                    run_as_user:
                      description:
                      - The UID to run the entrypoint of the container process. Defaults
                        to user specified in image metadata if unspecified. May also
                        be set in SecurityContext. If set in both SecurityContext
                        and PodSecurityContext, the value specified in SecurityContext
                        takes precedence for that container.
                      type: int
                    se_linux_options:
                      description:
                      - The SELinux context to be applied to all containers. If unspecified,
                        the container runtime will allocate a random SELinux context
                        for each container. May also be set in SecurityContext. If
                        set in both SecurityContext and PodSecurityContext, the value
                        specified in SecurityContext takes precedence for that container.
                      type: complex
                      contains:
                        level:
                          description:
                          - Level is SELinux level label that applies to the container.
                          type: str
                        role:
                          description:
                          - Role is a SELinux role label that applies to the container.
                          type: str
                        type:
                          description:
                          - Type is a SELinux type label that applies to the container.
                          type: str
                        user:
                          description:
                          - User is a SELinux user label that applies to the container.
                          type: str
                    supplemental_groups:
                      description:
                      - A list of groups applied to the first process run in each
                        container, in addition to the container's primary GID. If
                        unspecified, no groups will be added to any container.
                      type: list
                      contains: int
                service_account:
                  description:
                  - 'DeprecatedServiceAccount is a depreciated alias for ServiceAccountName.
                    Deprecated: Use serviceAccountName instead.'
                  type: str
                service_account_name:
                  description:
                  - ServiceAccountName is the name of the ServiceAccount to use to
                    run this pod.
                  type: str
                subdomain:
                  description:
                  - If specified, the fully qualified Pod hostname will be "<hostname>.<subdomain>.<pod
                    namespace>.svc.<cluster domain>". If not specified, the pod will
                    not have a domainname at all.
                  type: str
                termination_grace_period_seconds:
                  description:
                  - Optional duration in seconds the pod needs to terminate gracefully.
                    May be decreased in delete request. Value must be non-negative
                    integer. The value zero indicates delete immediately. If this
                    value is nil, the default grace period will be used instead. The
                    grace period is the duration in seconds after the processes running
                    in the pod are sent a termination signal and the time when the
                    processes are forcibly halted with a kill signal. Set this value
                    longer than the expected cleanup time for your process. Defaults
                    to 30 seconds.
                  type: int
                volumes:
                  description:
                  - List of volumes that can be mounted by containers belonging to
                    the pod.
                  type: list
                  contains:
                    aws_elastic_block_store:
                      description:
                      - AWSElasticBlockStore represents an AWS Disk resource that
                        is attached to a kubelet's host machine and then exposed to
                        the pod.
                      type: complex
                      contains:
                        fs_type:
                          description:
                          - 'Filesystem type of the volume that you want to mount.
                            Tip: Ensure that the filesystem type is supported by the
                            host operating system. Examples: "ext4", "xfs", "ntfs".
                            Implicitly inferred to be "ext4" if unspecified.'
                          type: str
                        partition:
                          description:
                          - 'The partition in the volume that you want to mount. If
                            omitted, the default is to mount by volume name. Examples:
                            For volume /dev/sda1, you specify the partition as "1".
                            Similarly, the volume partition for /dev/sda is "0" (or
                            you can leave the property empty).'
                          type: int
                        read_only:
                          description:
                          - Specify "true" to force and set the ReadOnly property
                            in VolumeMounts to "true". If omitted, the default is
                            "false".
                          type: bool
                        volume_id:
                          description:
                          - Unique ID of the persistent disk resource in AWS (Amazon
                            EBS volume).
                          type: str
                    azure_disk:
                      description:
                      - AzureDisk represents an Azure Data Disk mount on the host
                        and bind mount to the pod.
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
                            by the host operating system. Ex. "ext4", "xfs", "ntfs".
                            Implicitly inferred to be "ext4" if unspecified.
                          type: str
                        read_only:
                          description:
                          - Defaults to false (read/write). ReadOnly here will force
                            the ReadOnly setting in VolumeMounts.
                          type: bool
                    azure_file:
                      description:
                      - AzureFile represents an Azure File Service mount on the host
                        and bind mount to the pod.
                      type: complex
                      contains:
                        read_only:
                          description:
                          - Defaults to false (read/write). ReadOnly here will force
                            the ReadOnly setting in VolumeMounts.
                          type: bool
                        secret_name:
                          description:
                          - the name of secret that contains Azure Storage Account
                            Name and Key
                          type: str
                        share_name:
                          description:
                          - Share Name
                          type: str
                    cephfs:
                      description:
                      - CephFS represents a Ceph FS mount on the host that shares
                        a pod's lifetime
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
                          - 'Optional: Defaults to false (read/write). ReadOnly here
                            will force the ReadOnly setting in VolumeMounts.'
                          type: bool
                        secret_file:
                          description:
                          - 'Optional: SecretFile is the path to key ring for User,
                            default is /etc/ceph/user.secret'
                          type: str
                        secret_ref:
                          description:
                          - 'Optional: SecretRef is reference to the authentication
                            secret for User, default is empty.'
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
                      - Cinder represents a cinder volume attached and mounted on
                        kubelets host machine
                      type: complex
                      contains:
                        fs_type:
                          description:
                          - 'Filesystem type to mount. Must be a filesystem type supported
                            by the host operating system. Examples: "ext4", "xfs",
                            "ntfs". Implicitly inferred to be "ext4" if unspecified.'
                          type: str
                        read_only:
                          description:
                          - 'Optional: Defaults to false (read/write). ReadOnly here
                            will force the ReadOnly setting in VolumeMounts.'
                          type: bool
                        volume_id:
                          description:
                          - volume id used to identify the volume in cinder
                          type: str
                    config_map:
                      description:
                      - ConfigMap represents a configMap that should populate this
                        volume
                      type: complex
                      contains:
                        default_mode:
                          description:
                          - 'Optional: mode bits to use on created files by default.
                            Must be a value between 0 and 0777. Defaults to 0644.
                            Directories within the path are not affected by this setting.
                            This might be in conflict with other options that affect
                            the file mode, like fsGroup, and the result can be other
                            mode bits set.'
                          type: int
                        items:
                          description:
                          - If unspecified, each key-value pair in the Data field
                            of the referenced ConfigMap will be projected into the
                            volume as a file whose name is the key and content is
                            the value. If specified, the listed keys will be projected
                            into the specified paths, and unlisted keys will not be
                            present. If a key is specified which is not present in
                            the ConfigMap, the volume setup will error. Paths must
                            be relative and may not contain the '..' path or start
                            with '..'.
                          type: list
                          contains:
                            key:
                              description:
                              - The key to project.
                              type: str
                            mode:
                              description:
                              - 'Optional: mode bits to use on this file, must be
                                a value between 0 and 0777. If not specified, the
                                volume defaultMode will be used. This might be in
                                conflict with other options that affect the file mode,
                                like fsGroup, and the result can be other mode bits
                                set.'
                              type: int
                            path:
                              description:
                              - The relative path of the file to map the key to. May
                                not be an absolute path. May not contain the path
                                element '..'. May not start with the string '..'.
                              type: str
                        name:
                          description:
                          - Name of the referent.
                          type: str
                    downward_api:
                      description:
                      - DownwardAPI represents downward API about the pod that should
                        populate this volume
                      type: complex
                      contains:
                        default_mode:
                          description:
                          - 'Optional: mode bits to use on created files by default.
                            Must be a value between 0 and 0777. Defaults to 0644.
                            Directories within the path are not affected by this setting.
                            This might be in conflict with other options that affect
                            the file mode, like fsGroup, and the result can be other
                            mode bits set.'
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
                                  - Version of the schema the FieldPath is written
                                    in terms of, defaults to "v1".
                                  type: str
                                field_path:
                                  description:
                                  - Path of the field to select in the specified API
                                    version.
                                  type: str
                            mode:
                              description:
                              - 'Optional: mode bits to use on this file, must be
                                a value between 0 and 0777. If not specified, the
                                volume defaultMode will be used. This might be in
                                conflict with other options that affect the file mode,
                                like fsGroup, and the result can be other mode bits
                                set.'
                              type: int
                            path:
                              description:
                              - "Required: Path is the relative path name of the file\
                                \ to be created. Must not be absolute or contain the\
                                \ '..' path. Must be utf-8 encoded. The first item\
                                \ of the relative path must not start with '..'"
                              type: str
                            resource_field_ref:
                              description:
                              - 'Selects a resource of the container: only resources
                                limits and requests (limits.cpu, limits.memory, requests.cpu
                                and requests.memory) are currently supported.'
                              type: complex
                              contains:
                                container_name:
                                  description:
                                  - 'Container name: required for volumes, optional
                                    for env vars'
                                  type: str
                                divisor:
                                  description:
                                  - Specifies the output format of the exposed resources,
                                    defaults to "1"
                                  type: complex
                                  contains: {}
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
                          - What type of storage medium should back this directory.
                            The default is "" which means to use the node's default
                            medium. Must be an empty string (default) or Memory.
                          type: str
                    fc:
                      description:
                      - FC represents a Fibre Channel resource that is attached to
                        a kubelet's host machine and then exposed to the pod.
                      type: complex
                      contains:
                        fs_type:
                          description:
                          - Filesystem type to mount. Must be a filesystem type supported
                            by the host operating system. Ex. "ext4", "xfs", "ntfs".
                            Implicitly inferred to be "ext4" if unspecified.
                          type: str
                        lun:
                          description:
                          - 'Required: FC target lun number'
                          type: int
                        read_only:
                          description:
                          - 'Optional: Defaults to false (read/write). ReadOnly here
                            will force the ReadOnly setting in VolumeMounts.'
                          type: bool
                        target_ww_ns:
                          description:
                          - 'Required: FC target worldwide names (WWNs)'
                          type: list
                          contains: str
                    flex_volume:
                      description:
                      - FlexVolume represents a generic volume resource that is provisioned/attached
                        using an exec based plugin. This is an alpha feature and may
                        change in future.
                      type: complex
                      contains:
                        driver:
                          description:
                          - Driver is the name of the driver to use for this volume.
                          type: str
                        fs_type:
                          description:
                          - Filesystem type to mount. Must be a filesystem type supported
                            by the host operating system. Ex. "ext4", "xfs", "ntfs".
                            The default filesystem depends on FlexVolume script.
                          type: str
                        options:
                          description:
                          - 'Optional: Extra command options if any.'
                          type: complex
                          contains: str, str
                        read_only:
                          description:
                          - 'Optional: Defaults to false (read/write). ReadOnly here
                            will force the ReadOnly setting in VolumeMounts.'
                          type: bool
                        secret_ref:
                          description:
                          - 'Optional: SecretRef is reference to the secret object
                            containing sensitive information to pass to the plugin
                            scripts. This may be empty if no secret object is specified.
                            If the secret object contains more than one secret, all
                            secrets are passed to the plugin scripts.'
                          type: complex
                          contains:
                            name:
                              description:
                              - Name of the referent.
                              type: str
                    flocker:
                      description:
                      - Flocker represents a Flocker volume attached to a kubelet's
                        host machine. This depends on the Flocker control service
                        being running
                      type: complex
                      contains:
                        dataset_name:
                          description:
                          - Name of the dataset stored as metadata -> name on the
                            dataset for Flocker should be considered as deprecated
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
                          - 'Filesystem type of the volume that you want to mount.
                            Tip: Ensure that the filesystem type is supported by the
                            host operating system. Examples: "ext4", "xfs", "ntfs".
                            Implicitly inferred to be "ext4" if unspecified.'
                          type: str
                        partition:
                          description:
                          - 'The partition in the volume that you want to mount. If
                            omitted, the default is to mount by volume name. Examples:
                            For volume /dev/sda1, you specify the partition as "1".
                            Similarly, the volume partition for /dev/sda is "0" (or
                            you can leave the property empty).'
                          type: int
                        pd_name:
                          description:
                          - Unique name of the PD resource in GCE. Used to identify
                            the disk in GCE.
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
                          - Target directory name. Must not contain or start with
                            '..'. If '.' is supplied, the volume directory will be
                            the git repository. Otherwise, if specified, the volume
                            will contain the git repository in the subdirectory with
                            the given name.
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
                      - HostPath represents a pre-existing file or directory on the
                        host machine that is directly exposed to the container. This
                        is generally used for system agents or other privileged things
                        that are allowed to see the host machine. Most containers
                        will NOT need this.
                      type: complex
                      contains:
                        path:
                          description:
                          - Path of the directory on the host.
                          type: str
                    iscsi:
                      description:
                      - ISCSI represents an ISCSI Disk resource that is attached to
                        a kubelet's host machine and then exposed to the pod.
                      type: complex
                      contains:
                        fs_type:
                          description:
                          - 'Filesystem type of the volume that you want to mount.
                            Tip: Ensure that the filesystem type is supported by the
                            host operating system. Examples: "ext4", "xfs", "ntfs".
                            Implicitly inferred to be "ext4" if unspecified.'
                          type: str
                        iqn:
                          description:
                          - Target iSCSI Qualified Name.
                          type: str
                        iscsi_interface:
                          description:
                          - "Optional: Defaults to 'default' (tcp). iSCSI interface\
                            \ name that uses an iSCSI transport."
                          type: str
                        lun:
                          description:
                          - iSCSI target lun number.
                          type: int
                        read_only:
                          description:
                          - ReadOnly here will force the ReadOnly setting in VolumeMounts.
                            Defaults to false.
                          type: bool
                        target_portal:
                          description:
                          - iSCSI target portal. The portal is either an IP or ip_addr:port
                            if the port is other than default (typically TCP ports
                            860 and 3260).
                          type: str
                    name:
                      description:
                      - Volume's name. Must be a DNS_LABEL and unique within the pod.
                      type: str
                    nfs:
                      description:
                      - NFS represents an NFS mount on the host that shares a pod's
                        lifetime
                      type: complex
                      contains:
                        path:
                          description:
                          - Path that is exported by the NFS server.
                          type: str
                        read_only:
                          description:
                          - ReadOnly here will force the NFS export to be mounted
                            with read-only permissions. Defaults to false.
                          type: bool
                        server:
                          description:
                          - Server is the hostname or IP address of the NFS server.
                          type: str
                    persistent_volume_claim:
                      description:
                      - PersistentVolumeClaimVolumeSource represents a reference to
                        a PersistentVolumeClaim in the same namespace.
                      type: complex
                      contains:
                        claim_name:
                          description:
                          - ClaimName is the name of a PersistentVolumeClaim in the
                            same namespace as the pod using this volume.
                          type: str
                        read_only:
                          description:
                          - Will force the ReadOnly setting in VolumeMounts. Default
                            false.
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
                            by the host operating system. Ex. "ext4", "xfs", "ntfs".
                            Implicitly inferred to be "ext4" if unspecified.
                          type: str
                        pd_id:
                          description:
                          - ID that identifies Photon Controller persistent disk
                          type: str
                    quobyte:
                      description:
                      - Quobyte represents a Quobyte mount on the host that shares
                        a pod's lifetime
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
                          - User to map volume access to Defaults to serivceaccount
                            user
                          type: str
                        volume:
                          description:
                          - Volume is a string that references an already created
                            Quobyte volume by name.
                          type: str
                    rbd:
                      description:
                      - RBD represents a Rados Block Device mount on the host that
                        shares a pod's lifetime.
                      type: complex
                      contains:
                        fs_type:
                          description:
                          - 'Filesystem type of the volume that you want to mount.
                            Tip: Ensure that the filesystem type is supported by the
                            host operating system. Examples: "ext4", "xfs", "ntfs".
                            Implicitly inferred to be "ext4" if unspecified.'
                          type: str
                        image:
                          description:
                          - The rados image name.
                          type: str
                        keyring:
                          description:
                          - Keyring is the path to key ring for RBDUser. Default is
                            /etc/ceph/keyring.
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
                    secret:
                      description:
                      - Secret represents a secret that should populate this volume.
                      type: complex
                      contains:
                        default_mode:
                          description:
                          - 'Optional: mode bits to use on created files by default.
                            Must be a value between 0 and 0777. Defaults to 0644.
                            Directories within the path are not affected by this setting.
                            This might be in conflict with other options that affect
                            the file mode, like fsGroup, and the result can be other
                            mode bits set.'
                          type: int
                        items:
                          description:
                          - If unspecified, each key-value pair in the Data field
                            of the referenced Secret will be projected into the volume
                            as a file whose name is the key and content is the value.
                            If specified, the listed keys will be projected into the
                            specified paths, and unlisted keys will not be present.
                            If a key is specified which is not present in the Secret,
                            the volume setup will error. Paths must be relative and
                            may not contain the '..' path or start with '..'.
                          type: list
                          contains:
                            key:
                              description:
                              - The key to project.
                              type: str
                            mode:
                              description:
                              - 'Optional: mode bits to use on this file, must be
                                a value between 0 and 0777. If not specified, the
                                volume defaultMode will be used. This might be in
                                conflict with other options that affect the file mode,
                                like fsGroup, and the result can be other mode bits
                                set.'
                              type: int
                            path:
                              description:
                              - The relative path of the file to map the key to. May
                                not be an absolute path. May not contain the path
                                element '..'. May not start with the string '..'.
                              type: str
                        secret_name:
                          description:
                          - Name of the secret in the pod's namespace to use.
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
                            by the host operating system. Ex. "ext4", "xfs", "ntfs".
                            Implicitly inferred to be "ext4" if unspecified.
                          type: str
                        volume_path:
                          description:
                          - Path that identifies vSphere volume vmdk
                          type: str
        volume_claim_templates:
          description:
          - VolumeClaimTemplates is a list of claims that pods are allowed to reference.
            The StatefulSet controller is responsible for mapping network identities
            to claims in a way that maintains the identity of a pod. Every claim in
            this list must have at least one matching (by name) volumeMount in one
            container in the template. A claim in this list takes precedence over
            any volumes in the template, with the same name.
          type: list
          contains:
            api_version:
              description:
              - APIVersion defines the versioned schema of this representation of
                an object. Servers should convert recognized schemas to the latest
                internal value, and may reject unrecognized values.
              type: str
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
            spec:
              description:
              - Spec defines the desired characteristics of a volume requested by
                a pod author.
              type: complex
              contains:
                access_modes:
                  description:
                  - AccessModes contains the desired access modes the volume should
                    have.
                  type: list
                  contains: str
                resources:
                  description:
                  - Resources represents the minimum resources the volume should have.
                  type: complex
                  contains:
                    limits:
                      description:
                      - Limits describes the maximum amount of compute resources allowed.
                      type: complex
                      contains: str, ResourceQuantity
                    requests:
                      description:
                      - Requests describes the minimum amount of compute resources
                        required. If Requests is omitted for a container, it defaults
                        to Limits if that is explicitly specified, otherwise to an
                        implementation-defined value.
                      type: complex
                      contains: str, ResourceQuantity
                selector:
                  description:
                  - A label query over volumes to consider for binding.
                  type: complex
                  contains:
                    match_expressions:
                      description:
                      - matchExpressions is a list of label selector requirements.
                        The requirements are ANDed.
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
                          - values is an array of string values. If the operator is
                            In or NotIn, the values array must be non-empty. If the
                            operator is Exists or DoesNotExist, the values array must
                            be empty. This array is replaced during a strategic merge
                            patch.
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
                volume_name:
                  description:
                  - VolumeName is the binding reference to the PersistentVolume backing
                    this claim.
                  type: str
            status:
              description:
              - Status represents the current information/status of a persistent volume
                claim. Read-only.
              type: complex
              contains:
                access_modes:
                  description:
                  - AccessModes contains the actual access modes the volume backing
                    the PVC has.
                  type: list
                  contains: str
                capacity:
                  description:
                  - Represents the actual resources of the underlying volume.
                  type: complex
                  contains: str, ResourceQuantity
                phase:
                  description:
                  - Phase represents the current phase of PersistentVolumeClaim.
                  type: str
    status:
      description:
      - Status is the current status of Pods in this StatefulSet. This data may be
        out of date by some window of time.
      type: complex
      contains:
        observed_generation:
          description:
          - most recent generation observed by this autoscaler.
          type: int
        replicas:
          description:
          - Replicas is the number of actual replicas.
          type: int
'''


def main():
    try:
        module = KubernetesAnsibleModule('stateful_set', 'V1beta1')
    except KubernetesAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except KubernetesAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
