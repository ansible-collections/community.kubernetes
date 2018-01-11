#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.k8s_common import KubernetesAnsibleModule, KubernetesAnsibleException

DOCUMENTATION = '''
module: k8s_v1_service
short_description: Kubernetes Service
description:
- Manage the lifecycle of a service object. Supports check mode, and attempts to to
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
  spec_cluster_ip:
    description:
    - clusterIP is the IP address of the service and is usually assigned randomly
      by the master. If an address is specified manually and is not in use by others,
      it will be allocated to the service; otherwise, creation of the service will
      fail. This field can not be changed through updates. Valid values are "None",
      empty string (""), or a valid IP address. "None" can be specified for headless
      services when proxying is not required. Only applies to types ClusterIP, NodePort,
      and LoadBalancer. Ignored if type is ExternalName.
    aliases:
    - cluster_ip
  spec_external_i_ps:
    description:
    - externalIPs is a list of IP addresses for which nodes in the cluster will also
      accept traffic for this service. These IPs are not managed by Kubernetes. The
      user is responsible for ensuring that traffic arrives at a node with this IP.
      A common example is external load-balancers that are not part of the Kubernetes
      system.
    aliases:
    - external_i_ps
    type: list
  spec_external_name:
    description:
    - externalName is the external reference that kubedns or equivalent will return
      as a CNAME record for this service. No proxying will be involved. Must be a
      valid DNS name and requires Type to be ExternalName.
    aliases:
    - external_name
  spec_external_traffic_policy:
    description:
    - externalTrafficPolicy denotes if this Service desires to route external traffic
      to node-local or cluster-wide endpoints. "Local" preserves the client source
      IP and avoids a second hop for LoadBalancer and Nodeport type services, but
      risks potentially imbalanced traffic spreading. "Cluster" obscures the client
      source IP and may cause a second hop to another node, but should have good overall
      load-spreading.
    aliases:
    - external_traffic_policy
  spec_health_check_node_port:
    description:
    - healthCheckNodePort specifies the healthcheck nodePort for the service. If not
      specified, HealthCheckNodePort is created by the service api backend with the
      allocated nodePort. Will use user-specified nodePort value if specified by the
      client. Only effects when Type is set to LoadBalancer and ExternalTrafficPolicy
      is set to Local.
    aliases:
    - health_check_node_port
    type: int
  spec_load_balancer_ip:
    description:
    - 'Only applies to Service Type: LoadBalancer LoadBalancer will get created with
      the IP specified in this field. This feature depends on whether the underlying
      cloud-provider supports specifying the loadBalancerIP when a load balancer is
      created. This field will be ignored if the cloud-provider does not support the
      feature.'
    aliases:
    - load_balancer_ip
  spec_load_balancer_source_ranges:
    description:
    - If specified and supported by the platform, this will restrict traffic through
      the cloud-provider load-balancer will be restricted to the specified client
      IPs. This field will be ignored if the cloud-provider does not support the feature."
    aliases:
    - load_balancer_source_ranges
    type: list
  spec_ports:
    description:
    - The list of ports that are exposed by this service.
    aliases:
    - ports
    type: list
  spec_publish_not_ready_addresses:
    description:
    - publishNotReadyAddresses, when set to true, indicates that DNS implementations
      must publish the notReadyAddresses of subsets for the Endpoints associated with
      the Service. The default value is false. The primary use case for setting this
      field is to use a StatefulSet's Headless Service to propagate SRV records for
      its Pods without respect to their readiness for purpose of peer discovery. This
      field will replace the service.alpha.kubernetes.io/tolerate-unready-endpoints
      when that annotation is deprecated and all clients have been converted to use
      this field.
    aliases:
    - publish_not_ready_addresses
    type: bool
  spec_selector:
    description:
    - Route service traffic to pods with label keys and values matching this selector.
      If empty or not present, the service is assumed to have an external process
      managing its endpoints, which Kubernetes will not modify. Only applies to types
      ClusterIP, NodePort, and LoadBalancer. Ignored if type is ExternalName.
    aliases:
    - selector
    type: dict
  spec_session_affinity:
    description:
    - Supports "ClientIP" and "None". Used to maintain session affinity. Enable client
      IP based session affinity. Must be ClientIP or None. Defaults to None.
    aliases:
    - session_affinity
  spec_session_affinity_config_client_ip_timeout_seconds:
    description:
    - timeoutSeconds specifies the seconds of ClientIP type session sticky time. The
      value must be >0 && <=86400(for 1 day) if ServiceAffinity == "ClientIP". Default
      value is 10800(for 3 hours).
    aliases:
    - session_affinity__clientip_timeout_seconds
    type: int
  spec_type:
    description:
    - type determines how the Service is exposed. Defaults to ClusterIP. Valid options
      are ExternalName, ClusterIP, NodePort, and LoadBalancer. "ExternalName" maps
      to the specified externalName. "ClusterIP" allocates a cluster-internal IP address
      for load-balancing to endpoints. Endpoints are determined by the selector or
      if that is not specified, by manual construction of an Endpoints object. If
      clusterIP is "None", no virtual IP is allocated and the endpoints are published
      as a set of endpoints rather than a stable IP. "NodePort" builds on ClusterIP
      and allocates a port on every node which routes to the clusterIP. "LoadBalancer"
      builds on NodePort and creates an external load-balancer (if supported in the
      current cloud) which routes to the clusterIP.
    aliases:
    - type
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
- name: Create service
  k8s_v1_service.yml:
    name: myservice
    namespace: k8s-project
    state: present
    selector:
      app: django
    ports:
    - port: 8765
      target_port: 8000
      name: http-port
    type: ClusterIP

- name: Patch service
  k8s_v1_service.yml:
    name: myservice
    namespace: k8s-project
    state: present
    selector:
      app: django
      env: production
    ports:
    - port: 8765
      target_port: 8010
      name: http-port
    - port: 8788
      target_port: 8080
      name: socket-port
    type: ClusterIP

- name: Create service
  k8s_v1_service.yml:
    name: myservice01
    namespace: k8s-project
    state: present
    selector:
      app_name: service_testing
      app_env: production
    ports:
    - port: 8888
      target_port: 8010
      name: http
    type: ClusterIP

- name: Patch service
  k8s_v1_service.yml:
    name: myservice01
    namespace: k8s-project
    state: present
    ports:
    - port: 9443
      target_port: 9443
      name: https
    - port: 8888
      target_port: 8015
      name: http

- name: Repace service
  k8s_v1_service.yml:
    name: myservice01
    namespace: k8s-project
    state: replaced
    selector:
      app_name: web_site
      app_env: testing
    ports:
    - port: 9999
      target_port: 9999
      name: https
    - port: 8080
      target_port: 8080
      name: http
    type: NodePort
'''

RETURN = '''
api_version:
  description: Requested API version
  type: string
service:
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
      - Spec defines the behavior of a service.
      type: complex
    status:
      description:
      - Most recently observed status of the service. Populated by the system. Read-only.
      type: complex
'''


def main():
    try:
        module = KubernetesAnsibleModule('service', 'v1')
    except KubernetesAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except KubernetesAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
