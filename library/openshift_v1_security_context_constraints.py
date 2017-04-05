#!/usr/bin/env python

from ansible.module_utils.openshift_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: openshift_v1_security_context_constraints
short_description: OpenShift SecurityContextConstraints
description:
- Manage the lifecycle of a security_context_constraints object. Supports check mode,
  and attempts to to be idempotent.
version_added: 2.3.0
author: OpenShift (@openshift)
options:
  allow_host_dir_volume_plugin:
    description:
    - AllowHostDirVolumePlugin determines if the policy allow containers to use the
      HostDir volume plugin
    type: bool
  allow_host_ipc:
    description:
    - AllowHostIPC determines if the policy allows host ipc in the containers.
    type: bool
  allow_host_network:
    description:
    - AllowHostNetwork determines if the policy allows the use of HostNetwork in the
      pod spec.
    type: bool
  allow_host_pid:
    description:
    - AllowHostPID determines if the policy allows host pid in the containers.
    type: bool
  allow_host_ports:
    description:
    - AllowHostPorts determines if the policy allows host ports in the containers.
    type: bool
  allow_privileged_container:
    description:
    - AllowPrivilegedContainer determines if a container can request to be run as
      privileged.
    type: bool
  allowed_capabilities:
    description:
    - AllowedCapabilities is a list of capabilities that can be requested to add to
      the container. Capabilities in this field maybe added at the pod author's discretion.
      You must not list a capability in both AllowedCapabilities and RequiredDropCapabilities.
      To allow all capabilities you may use '*'.
    type: list
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
  default_add_capabilities:
    description:
    - DefaultAddCapabilities is the default set of capabilities that will be added
      to the container unless the pod spec specifically drops the capability. You
      may not list a capabiility in both DefaultAddCapabilities and RequiredDropCapabilities.
    type: list
  force:
    description:
    - If set to C(True), and I(state) is C(present), an existing object will updated,
      and lists will be replaced, rather than merged.
    default: false
    type: bool
  fs_group_ranges:
    description:
    - Ranges are the allowed ranges of fs groups. If you would like to force a single
      fs group then supply a single range with the same start and end.
    aliases:
    - ranges
    type: list
  fs_group_type:
    description:
    - Type is the strategy that will dictate what FSGroup is used in the SecurityContext.
    aliases:
    - type
  groups:
    description:
    - The groups that have permission to use this security context constraints
    type: list
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
  priority:
    description:
    - Priority influences the sort order of SCCs when evaluating which SCCs to try
      first for a given pod request based on access in the Users and Groups fields.
      The higher the int, the higher priority. If scores for multiple SCCs are equal
      they will be sorted by name.
    type: int
  read_only_root_filesystem:
    description:
    - ReadOnlyRootFilesystem when set to true will force containers to run with a
      read only root file system. If the container specifically requests to run with
      a non-read only root file system the SCC should deny the pod. If set to false
      the container may run with a read only root file system if it wishes but it
      will not be forced to.
    type: bool
  required_drop_capabilities:
    description:
    - RequiredDropCapabilities are the capabilities that will be dropped from the
      container. These are required to be dropped and cannot be added.
    type: list
  run_as_user_type:
    description:
    - Type is the strategy that will dictate what RunAsUser is used in the SecurityContext.
    aliases:
    - type
  run_as_user_uid:
    description:
    - UID is the user id that containers must run as. Required for the MustRunAs strategy
      if not using namespace/service account allocated uids.
    aliases:
    - uid
    type: int
  run_as_user_uid_range_max:
    description:
    - UIDRangeMax defines the max value for a strategy that allocates by range.
    aliases:
    - uid_range_max
    type: int
  run_as_user_uid_range_min:
    description:
    - UIDRangeMin defines the min value for a strategy that allocates by range.
    aliases:
    - uid_range_min
    type: int
  se_linux_context_se_linux_options_level:
    description:
    - Level is SELinux level label that applies to the container.
    aliases:
    - level
  se_linux_context_se_linux_options_role:
    description:
    - Role is a SELinux role label that applies to the container.
    aliases:
    - role
  se_linux_context_se_linux_options_type:
    description:
    - Type is a SELinux type label that applies to the container.
    aliases:
    - type
  se_linux_context_se_linux_options_user:
    description:
    - User is a SELinux user label that applies to the container.
    aliases:
    - user
  se_linux_context_type:
    description:
    - Type is the strategy that will dictate what SELinux context is used in the SecurityContext.
    aliases:
    - type
  seccomp_profiles:
    description:
    - SeccompProfiles lists the allowed profiles that may be set for the pod or container's
      seccomp annotations. An unset (nil) or empty value means that no profiles may
      be specifid by the pod or container. The wildcard '*' may be used to allow all
      profiles. When used to generate a value for a pod the first non-wildcard profile
      will be used as the default.
    type: list
  ssl_ca_cert:
    description:
    - Path to a CA certificate used to authenticate with the API.
    type: path
  supplemental_groups_ranges:
    description:
    - Ranges are the allowed ranges of supplemental groups. If you would like to force
      a single supplemental group then supply a single range with the same start and
      end.
    aliases:
    - ranges
    type: list
  supplemental_groups_type:
    description:
    - Type is the strategy that will dictate what supplemental groups is used in the
      SecurityContext.
    aliases:
    - type
  username:
    description:
    - Provide a username for connecting to the API.
  users:
    description:
    - The users who have permissions to use this security context constraints
    type: list
  verify_ssl:
    description:
    - Whether or not to verify the API server's SSL certificates.
    type: bool
  volumes:
    description:
    - Volumes is a white list of allowed volume plugins. FSType corresponds directly
      with the field names of a VolumeSource (azureFile, configMap, emptyDir). To
      allow all volumes you may use '*'.
    type: list
requirements:
- openshift == 1.0.0-snapshot
'''

EXAMPLES = '''
'''

RETURN = '''
api_version:
  type: string
  description: Requested API version
security_context_constraints:
  type: complex
  returned: on success
  contains:
    allow_host_dir_volume_plugin:
      description:
      - AllowHostDirVolumePlugin determines if the policy allow containers to use
        the HostDir volume plugin
      type: bool
    allow_host_ipc:
      description:
      - AllowHostIPC determines if the policy allows host ipc in the containers.
      type: bool
    allow_host_network:
      description:
      - AllowHostNetwork determines if the policy allows the use of HostNetwork in
        the pod spec.
      type: bool
    allow_host_pid:
      description:
      - AllowHostPID determines if the policy allows host pid in the containers.
      type: bool
    allow_host_ports:
      description:
      - AllowHostPorts determines if the policy allows host ports in the containers.
      type: bool
    allow_privileged_container:
      description:
      - AllowPrivilegedContainer determines if a container can request to be run as
        privileged.
      type: bool
    allowed_capabilities:
      description:
      - AllowedCapabilities is a list of capabilities that can be requested to add
        to the container. Capabilities in this field maybe added at the pod author's
        discretion. You must not list a capability in both AllowedCapabilities and
        RequiredDropCapabilities. To allow all capabilities you may use '*'.
      type: list
      contains: str
    api_version:
      description:
      - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values.
      type: str
    default_add_capabilities:
      description:
      - DefaultAddCapabilities is the default set of capabilities that will be added
        to the container unless the pod spec specifically drops the capability. You
        may not list a capabiility in both DefaultAddCapabilities and RequiredDropCapabilities.
      type: list
      contains: str
    fs_group:
      description:
      - FSGroup is the strategy that will dictate what fs group is used by the SecurityContext.
      type: complex
      contains:
        ranges:
          description:
          - Ranges are the allowed ranges of fs groups. If you would like to force
            a single fs group then supply a single range with the same start and end.
          type: list
          contains:
            max:
              description:
              - Max is the end of the range, inclusive.
              type: int
            min:
              description:
              - Min is the start of the range, inclusive.
              type: int
        type:
          description:
          - Type is the strategy that will dictate what FSGroup is used in the SecurityContext.
          type: str
    groups:
      description:
      - The groups that have permission to use this security context constraints
      type: list
      contains: str
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
    priority:
      description:
      - Priority influences the sort order of SCCs when evaluating which SCCs to try
        first for a given pod request based on access in the Users and Groups fields.
        The higher the int, the higher priority. If scores for multiple SCCs are equal
        they will be sorted by name.
      type: int
    read_only_root_filesystem:
      description:
      - ReadOnlyRootFilesystem when set to true will force containers to run with
        a read only root file system. If the container specifically requests to run
        with a non-read only root file system the SCC should deny the pod. If set
        to false the container may run with a read only root file system if it wishes
        but it will not be forced to.
      type: bool
    required_drop_capabilities:
      description:
      - RequiredDropCapabilities are the capabilities that will be dropped from the
        container. These are required to be dropped and cannot be added.
      type: list
      contains: str
    run_as_user:
      description:
      - RunAsUser is the strategy that will dictate what RunAsUser is used in the
        SecurityContext.
      type: complex
      contains:
        type:
          description:
          - Type is the strategy that will dictate what RunAsUser is used in the SecurityContext.
          type: str
        uid:
          description:
          - UID is the user id that containers must run as. Required for the MustRunAs
            strategy if not using namespace/service account allocated uids.
          type: int
        uid_range_max:
          description:
          - UIDRangeMax defines the max value for a strategy that allocates by range.
          type: int
        uid_range_min:
          description:
          - UIDRangeMin defines the min value for a strategy that allocates by range.
          type: int
    se_linux_context:
      description:
      - SELinuxContext is the strategy that will dictate what labels will be set in
        the SecurityContext.
      type: complex
      contains:
        se_linux_options:
          description:
          - seLinuxOptions required to run as; required for MustRunAs
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
        type:
          description:
          - Type is the strategy that will dictate what SELinux context is used in
            the SecurityContext.
          type: str
    seccomp_profiles:
      description:
      - SeccompProfiles lists the allowed profiles that may be set for the pod or
        container's seccomp annotations. An unset (nil) or empty value means that
        no profiles may be specifid by the pod or container. The wildcard '*' may
        be used to allow all profiles. When used to generate a value for a pod the
        first non-wildcard profile will be used as the default.
      type: list
      contains: str
    supplemental_groups:
      description:
      - SupplementalGroups is the strategy that will dictate what supplemental groups
        are used by the SecurityContext.
      type: complex
      contains:
        ranges:
          description:
          - Ranges are the allowed ranges of supplemental groups. If you would like
            to force a single supplemental group then supply a single range with the
            same start and end.
          type: list
          contains:
            max:
              description:
              - Max is the end of the range, inclusive.
              type: int
            min:
              description:
              - Min is the start of the range, inclusive.
              type: int
        type:
          description:
          - Type is the strategy that will dictate what supplemental groups is used
            in the SecurityContext.
          type: str
    users:
      description:
      - The users who have permissions to use this security context constraints
      type: list
      contains: str
    volumes:
      description:
      - Volumes is a white list of allowed volume plugins. FSType corresponds directly
        with the field names of a VolumeSource (azureFile, configMap, emptyDir). To
        allow all volumes you may use '*'.
      type: list
      contains: str
'''


def main():
    try:
        module = OpenShiftAnsibleModule('security_context_constraints', 'V1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
