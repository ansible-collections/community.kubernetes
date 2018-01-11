#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.k8s_common import KubernetesAnsibleModule, KubernetesAnsibleException

DOCUMENTATION = '''
module: k8s_v1beta1_pod_security_policy
short_description: Kubernetes PodSecurityPolicy
description:
- Manage the lifecycle of a pod_security_policy object. Supports check mode, and attempts
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
  spec_allow_privilege_escalation:
    description:
    - AllowPrivilegeEscalation determines if a pod can request to allow privilege
      escalation. If unspecified, defaults to true.
    aliases:
    - allow_privilege_escalation
    type: bool
  spec_allowed_capabilities:
    description:
    - AllowedCapabilities is a list of capabilities that can be requested to add to
      the container. Capabilities in this field may be added at the pod author's discretion.
      You must not list a capability in both AllowedCapabilities and RequiredDropCapabilities.
    aliases:
    - allowed_capabilities
    type: list
  spec_allowed_host_paths:
    description:
    - is a white list of allowed host paths. Empty indicates that all host paths may
      be used.
    aliases:
    - allowed_host_paths
    type: list
  spec_default_add_capabilities:
    description:
    - DefaultAddCapabilities is the default set of capabilities that will be added
      to the container unless the pod spec specifically drops the capability. You
      may not list a capabiility in both DefaultAddCapabilities and RequiredDropCapabilities.
    aliases:
    - default_add_capabilities
    type: list
  spec_default_allow_privilege_escalation:
    description:
    - DefaultAllowPrivilegeEscalation controls the default setting for whether a process
      can gain more privileges than its parent process.
    aliases:
    - default_allow_privilege_escalation
    type: bool
  spec_fs_group_ranges:
    description:
    - Ranges are the allowed ranges of fs groups. If you would like to force a single
      fs group then supply a single range with the same start and end.
    aliases:
    - fs_group_ranges
    type: list
  spec_fs_group_rule:
    description:
    - Rule is the strategy that will dictate what FSGroup is used in the SecurityContext.
    aliases:
    - fs_group_rule
  spec_host_ipc:
    description:
    - hostIPC determines if the policy allows the use of HostIPC in the pod spec.
    aliases:
    - host_ipc
    type: bool
  spec_host_network:
    description:
    - hostNetwork determines if the policy allows the use of HostNetwork in the pod
      spec.
    aliases:
    - host_network
    type: bool
  spec_host_pid:
    description:
    - hostPID determines if the policy allows the use of HostPID in the pod spec.
    aliases:
    - host_pid
    type: bool
  spec_host_ports:
    description:
    - hostPorts determines which host port ranges are allowed to be exposed.
    aliases:
    - host_ports
    type: list
  spec_privileged:
    description:
    - privileged determines if a pod can request to be run as privileged.
    aliases:
    - privileged
    type: bool
  spec_read_only_root_filesystem:
    description:
    - ReadOnlyRootFilesystem when set to true will force containers to run with a
      read only root file system. If the container specifically requests to run with
      a non-read only root file system the PSP should deny the pod. If set to false
      the container may run with a read only root file system if it wishes but it
      will not be forced to.
    aliases:
    - read_only_root_filesystem
    type: bool
  spec_required_drop_capabilities:
    description:
    - RequiredDropCapabilities are the capabilities that will be dropped from the
      container. These are required to be dropped and cannot be added.
    aliases:
    - required_drop_capabilities
    type: list
  spec_run_as_user_ranges:
    description:
    - Ranges are the allowed ranges of uids that may be used.
    aliases:
    - run_as_user_ranges
    type: list
  spec_run_as_user_rule:
    description:
    - Rule is the strategy that will dictate the allowable RunAsUser values that may
      be set.
    aliases:
    - run_as_user_rule
  spec_se_linux_rule:
    description:
    - type is the strategy that will dictate the allowable labels that may be set.
    aliases:
    - se_linux_rule
  spec_se_linux_se_linux_options_level:
    description:
    - Level is SELinux level label that applies to the container.
    aliases:
    - se_linux_se_options_level
  spec_se_linux_se_linux_options_role:
    description:
    - Role is a SELinux role label that applies to the container.
    aliases:
    - se_linux_se_options_role
  spec_se_linux_se_linux_options_type:
    description:
    - Type is a SELinux type label that applies to the container.
    aliases:
    - se_linux_se_options_type
  spec_se_linux_se_linux_options_user:
    description:
    - User is a SELinux user label that applies to the container.
    aliases:
    - se_linux_se_options_user
  spec_supplemental_groups_ranges:
    description:
    - Ranges are the allowed ranges of supplemental groups. If you would like to force
      a single supplemental group then supply a single range with the same start and
      end.
    aliases:
    - supplemental_groups_ranges
    type: list
  spec_supplemental_groups_rule:
    description:
    - Rule is the strategy that will dictate what supplemental groups is used in the
      SecurityContext.
    aliases:
    - supplemental_groups_rule
  spec_volumes:
    description:
    - volumes is a white list of allowed volume plugins. Empty indicates that all
      plugins may be used.
    aliases:
    - volumes
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
pod_security_policy:
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
      - spec defines the policy enforced.
      type: complex
'''


def main():
    try:
        module = KubernetesAnsibleModule('pod_security_policy', 'v1beta1')
    except KubernetesAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except KubernetesAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
