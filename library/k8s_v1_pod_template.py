#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.k8s_common import KubernetesAnsibleModule, KubernetesAnsibleException

DOCUMENTATION = '''
module: k8s_v1_pod_template
short_description: Kubernetes PodTemplate
description:
- Manage the lifecycle of a pod_template object. Supports check mode, and attempts
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
  template_metadata_annotations:
    description:
    - Annotations is an unstructured key value map stored with a resource that may
      be set by external tools to store and retrieve arbitrary metadata. They are
      not queryable and should be preserved when modifying objects.
    type: dict
  template_metadata_labels:
    description:
    - Map of string keys and values that can be used to organize and categorize (scope
      and select) objects. May match selectors of replication controllers and services.
    type: dict
  template_metadata_name:
    description:
    - Name must be unique within a namespace. Is required when creating resources,
      although some resources may allow a client to request the generation of an appropriate
      name automatically. Name is primarily intended for creation idempotence and
      configuration definition. Cannot be updated.
  template_metadata_namespace:
    description:
    - Namespace defines the space within each name must be unique. An empty namespace
      is equivalent to the "default" namespace, but "default" is the canonical representation.
      Not all objects are required to be scoped to a namespace - the value of this
      field for those objects will be empty. Must be a DNS_LABEL. Cannot be updated.
  template_spec_active_deadline_seconds:
    description:
    - Optional duration in seconds the pod may be active on the node relative to StartTime
      before the system will actively try to mark it failed and kill associated containers.
      Value must be a positive integer.
    aliases:
    - active_deadline_seconds
    type: int
  template_spec_affinity_node_affinity_preferred_during_scheduling_ignored_during_execution:
    description:
    - The scheduler will prefer to schedule pods to nodes that satisfy the affinity
      expressions specified by this field, but it may choose a node that violates
      one or more of the expressions. The node that is most preferred is the one with
      the greatest sum of weights, i.e. for each node that meets all of the scheduling
      requirements (resource request, requiredDuringScheduling affinity expressions,
      etc.), compute a sum by iterating through the elements of this field and adding
      "weight" to the sum if the node matches the corresponding matchExpressions;
      the node(s) with the highest sum are the most preferred.
    aliases:
    - affinity_node_affinity_preferred_during_scheduling_ignored_during_execution
    type: list
  template_spec_affinity_node_affinity_required_during_scheduling_ignored_during_execution_node_selector_terms:
    description:
    - Required. A list of node selector terms. The terms are ORed.
    aliases:
    - affinity_node_affinity_required_during_scheduling_ignored_during_execution_node_selector_terms
    type: list
  template_spec_affinity_pod_affinity_preferred_during_scheduling_ignored_during_execution:
    description:
    - The scheduler will prefer to schedule pods to nodes that satisfy the affinity
      expressions specified by this field, but it may choose a node that violates
      one or more of the expressions. The node that is most preferred is the one with
      the greatest sum of weights, i.e. for each node that meets all of the scheduling
      requirements (resource request, requiredDuringScheduling affinity expressions,
      etc.), compute a sum by iterating through the elements of this field and adding
      "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm;
      the node(s) with the highest sum are the most preferred.
    aliases:
    - affinity_pod_affinity_preferred_during_scheduling_ignored_during_execution
    type: list
  template_spec_affinity_pod_affinity_required_during_scheduling_ignored_during_execution:
    description:
    - If the affinity requirements specified by this field are not met at scheduling
      time, the pod will not be scheduled onto the node. If the affinity requirements
      specified by this field cease to be met at some point during pod execution (e.g.
      due to a pod label update), the system may or may not try to eventually evict
      the pod from its node. When there are multiple elements, the lists of nodes
      corresponding to each podAffinityTerm are intersected, i.e. all terms must be
      satisfied.
    aliases:
    - affinity_pod_affinity_required_during_scheduling_ignored_during_execution
    type: list
  template_spec_affinity_pod_anti_affinity_preferred_during_scheduling_ignored_during_execution:
    description:
    - The scheduler will prefer to schedule pods to nodes that satisfy the anti-affinity
      expressions specified by this field, but it may choose a node that violates
      one or more of the expressions. The node that is most preferred is the one with
      the greatest sum of weights, i.e. for each node that meets all of the scheduling
      requirements (resource request, requiredDuringScheduling anti-affinity expressions,
      etc.), compute a sum by iterating through the elements of this field and adding
      "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm;
      the node(s) with the highest sum are the most preferred.
    aliases:
    - affinity_pod_anti_affinity_preferred_during_scheduling_ignored_during_execution
    type: list
  template_spec_affinity_pod_anti_affinity_required_during_scheduling_ignored_during_execution:
    description:
    - If the anti-affinity requirements specified by this field are not met at scheduling
      time, the pod will not be scheduled onto the node. If the anti-affinity requirements
      specified by this field cease to be met at some point during pod execution (e.g.
      due to a pod label update), the system may or may not try to eventually evict
      the pod from its node. When there are multiple elements, the lists of nodes
      corresponding to each podAffinityTerm are intersected, i.e. all terms must be
      satisfied.
    aliases:
    - affinity_pod_anti_affinity_required_during_scheduling_ignored_during_execution
    type: list
  template_spec_automount_service_account_token:
    description:
    - AutomountServiceAccountToken indicates whether a service account token should
      be automatically mounted.
    aliases:
    - automount_service_account_token
    type: bool
  template_spec_containers:
    description:
    - List of containers belonging to the pod. Containers cannot currently be added
      or removed. There must be at least one container in a Pod. Cannot be updated.
    aliases:
    - containers
    type: list
  template_spec_dns_policy:
    description:
    - Set DNS policy for containers within the pod. One of 'ClusterFirstWithHostNet',
      'ClusterFirst' or 'Default'. Defaults to "ClusterFirst". To have DNS options
      set along with hostNetwork, you have to specify DNS policy explicitly to 'ClusterFirstWithHostNet'.
    aliases:
    - dns_policy
  template_spec_host_aliases:
    description:
    - HostAliases is an optional list of hosts and IPs that will be injected into
      the pod's hosts file if specified. This is only valid for non-hostNetwork pods.
    aliases:
    - host_aliases
    type: list
  template_spec_host_ipc:
    description:
    - "Use the host's ipc namespace. Optional: Default to false."
    aliases:
    - host_ipc
    type: bool
  template_spec_host_network:
    description:
    - Host networking requested for this pod. Use the host's network namespace. If
      this option is set, the ports that will be used must be specified. Default to
      false.
    aliases:
    - host_network
    type: bool
  template_spec_host_pid:
    description:
    - "Use the host's pid namespace. Optional: Default to false."
    aliases:
    - host_pid
    type: bool
  template_spec_hostname:
    description:
    - Specifies the hostname of the Pod If not specified, the pod's hostname will
      be set to a system-defined value.
    aliases:
    - hostname
  template_spec_image_pull_secrets:
    description:
    - ImagePullSecrets is an optional list of references to secrets in the same namespace
      to use for pulling any of the images used by this PodSpec. If specified, these
      secrets will be passed to individual puller implementations for them to use.
      For example, in the case of docker, only DockerConfig type secrets are honored.
    aliases:
    - image_pull_secrets
    type: list
  template_spec_init_containers:
    description:
    - List of initialization containers belonging to the pod. Init containers are
      executed in order prior to containers being started. If any init container fails,
      the pod is considered to have failed and is handled according to its restartPolicy.
      The name for an init container or normal container must be unique among all
      containers. Init containers may not have Lifecycle actions, Readiness probes,
      or Liveness probes. The resourceRequirements of an init container are taken
      into account during scheduling by finding the highest request/limit for each
      resource type, and then using the max of of that value or the sum of the normal
      containers. Limits are applied to init containers in a similar fashion. Init
      containers cannot currently be added or removed. Cannot be updated.
    aliases:
    - init_containers
    type: list
  template_spec_node_name:
    description:
    - NodeName is a request to schedule this pod onto a specific node. If it is non-empty,
      the scheduler simply schedules this pod onto that node, assuming that it fits
      resource requirements.
    aliases:
    - node_name
  template_spec_node_selector:
    description:
    - NodeSelector is a selector which must be true for the pod to fit on a node.
      Selector which must match a node's labels for the pod to be scheduled on that
      node.
    aliases:
    - node_selector
    type: dict
  template_spec_priority:
    description:
    - The priority value. Various system components use this field to find the priority
      of the pod. When Priority Admission Controller is enabled, it prevents users
      from setting this field. The admission controller populates this field from
      PriorityClassName. The higher the value, the higher the priority.
    aliases:
    - priority
    type: int
  template_spec_priority_class_name:
    description:
    - If specified, indicates the pod's priority. "SYSTEM" is a special keyword which
      indicates the highest priority. Any other name must be defined by creating a
      PriorityClass object with that name. If not specified, the pod priority will
      be default or zero if there is no default.
    aliases:
    - priority_class_name
  template_spec_restart_policy:
    description:
    - Restart policy for all containers within the pod. One of Always, OnFailure,
      Never. Default to Always.
    aliases:
    - restart_policy
  template_spec_scheduler_name:
    description:
    - If specified, the pod will be dispatched by specified scheduler. If not specified,
      the pod will be dispatched by default scheduler.
    aliases:
    - scheduler_name
  template_spec_security_context_fs_group:
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
  template_spec_security_context_run_as_non_root:
    description:
    - Indicates that the container must run as a non-root user. If true, the Kubelet
      will validate the image at runtime to ensure that it does not run as UID 0 (root)
      and fail to start the container if it does. If unset or false, no such validation
      will be performed. May also be set in SecurityContext. If set in both SecurityContext
      and PodSecurityContext, the value specified in SecurityContext takes precedence.
    aliases:
    - security_context_run_as_non_root
    type: bool
  template_spec_security_context_run_as_user:
    description:
    - The UID to run the entrypoint of the container process. Defaults to user specified
      in image metadata if unspecified. May also be set in SecurityContext. If set
      in both SecurityContext and PodSecurityContext, the value specified in SecurityContext
      takes precedence for that container.
    aliases:
    - security_context_run_as_user
    type: int
  template_spec_security_context_se_linux_options_level:
    description:
    - Level is SELinux level label that applies to the container.
    aliases:
    - security_context_se_linux_options_level
  template_spec_security_context_se_linux_options_role:
    description:
    - Role is a SELinux role label that applies to the container.
    aliases:
    - security_context_se_linux_options_role
  template_spec_security_context_se_linux_options_type:
    description:
    - Type is a SELinux type label that applies to the container.
    aliases:
    - security_context_se_linux_options_type
  template_spec_security_context_se_linux_options_user:
    description:
    - User is a SELinux user label that applies to the container.
    aliases:
    - security_context_se_linux_options_user
  template_spec_security_context_supplemental_groups:
    description:
    - A list of groups applied to the first process run in each container, in addition
      to the container's primary GID. If unspecified, no groups will be added to any
      container.
    aliases:
    - security_context_supplemental_groups
    type: list
  template_spec_service_account:
    description:
    - 'DeprecatedServiceAccount is a depreciated alias for ServiceAccountName. Deprecated:
      Use serviceAccountName instead.'
    aliases:
    - service_account
  template_spec_service_account_name:
    description:
    - ServiceAccountName is the name of the ServiceAccount to use to run this pod.
    aliases:
    - service_account_name
  template_spec_subdomain:
    description:
    - If specified, the fully qualified Pod hostname will be "<hostname>.<subdomain>.<pod
      namespace>.svc.<cluster domain>". If not specified, the pod will not have a
      domainname at all.
    aliases:
    - subdomain
  template_spec_termination_grace_period_seconds:
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
  template_spec_tolerations:
    description:
    - If specified, the pod's tolerations.
    aliases:
    - tolerations
    type: list
  template_spec_volumes:
    description:
    - List of volumes that can be mounted by containers belonging to the pod.
    aliases:
    - volumes
    type: list
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
pod_template:
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
    template:
      description:
      - Template defines the pods that will be created from this pod template.
      type: complex
'''


def main():
    try:
        module = KubernetesAnsibleModule('pod_template', 'v1')
    except KubernetesAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except KubernetesAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
