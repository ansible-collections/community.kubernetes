#!/usr/bin/python
# -*- coding: utf-8 -*-

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
  allowed_flex_volumes:
    description:
    - AllowedFlexVolumes is a whitelist of allowed Flexvolumes. Empty or nil indicates
      that all Flexvolumes may be used. This parameter is effective only when the
      usage of the Flexvolumes is allowed in the "Volumes" field.
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
      The higher the int, the higher priority. An unset value is considered a 0 priority.
      If scores for multiple SCCs are equal they will be sorted from most restrictive
      to least restrictive. If both priorities and restrictions are equal the SCCs
      will be sorted by name.
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
  resource_definition:
    description:
    - Provide the YAML definition for the object, bypassing any modules parameters
      intended to define object attributes.
    type: dict
  run_as_user_type:
    description:
    - Type is the strategy that will dictate what RunAsUser is used in the SecurityContext.
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
  se_linux_context_se_linux_options_user:
    description:
    - User is a SELinux user label that applies to the container.
    aliases:
    - user
  se_linux_context_type:
    description:
    - Type is the strategy that will dictate what SELinux context is used in the SecurityContext.
  seccomp_profiles:
    description:
    - SeccompProfiles lists the allowed profiles that may be set for the pod or container's
      seccomp annotations. An unset (nil) or empty value means that no profiles may
      be specifid by the pod or container. The wildcard '*' may be used to allow all
      profiles. When used to generate a value for a pod the first non-wildcard profile
      will be used as the default.
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
  supplemental_groups_ranges:
    description:
    - Ranges are the allowed ranges of supplemental groups. If you would like to force
      a single supplemental group then supply a single range with the same start and
      end.
    type: list
  supplemental_groups_type:
    description:
    - Type is the strategy that will dictate what supplemental groups is used in the
      SecurityContext.
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
      allow all volumes you may use "*". To allow no volumes, set to ["none"].
    type: list
requirements:
- openshift == 0.4.0.a1
'''

EXAMPLES = '''
'''

RETURN = '''
api_version:
  description: Requested API version
  type: string
security_context_constraints:
  type: complex
  returned: when I(state) = C(present)
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
    allowed_flex_volumes:
      description:
      - AllowedFlexVolumes is a whitelist of allowed Flexvolumes. Empty or nil indicates
        that all Flexvolumes may be used. This parameter is effective only when the
        usage of the Flexvolumes is allowed in the "Volumes" field.
      type: list
      contains:
        driver:
          description:
          - Driver is the name of the Flexvolume driver.
          type: str
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
    priority:
      description:
      - Priority influences the sort order of SCCs when evaluating which SCCs to try
        first for a given pod request based on access in the Users and Groups fields.
        The higher the int, the higher priority. An unset value is considered a 0
        priority. If scores for multiple SCCs are equal they will be sorted from most
        restrictive to least restrictive. If both priorities and restrictions are
        equal the SCCs will be sorted by name.
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
    se_linux_context:
      description:
      - SELinuxContext is the strategy that will dictate what labels will be set in
        the SecurityContext.
      type: complex
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
    users:
      description:
      - The users who have permissions to use this security context constraints
      type: list
      contains: str
    volumes:
      description:
      - Volumes is a white list of allowed volume plugins. FSType corresponds directly
        with the field names of a VolumeSource (azureFile, configMap, emptyDir). To
        allow all volumes you may use "*". To allow no volumes, set to ["none"].
      type: list
      contains: str
'''


def main():
    try:
        module = OpenShiftAnsibleModule('security_context_constraints', 'v1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
