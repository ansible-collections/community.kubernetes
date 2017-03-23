#!/usr/bin/env python

from ansible.module_utils.k8s_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

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
  spec_deprecated_public_i_ps:
    description:
    - deprecatedPublicIPs is deprecated and replaced by the externalIPs field with
      almost the exact same semantics. This field is retained in the v1 API for compatibility
      until at least 8/20/2016. It will be removed from any new API revisions. If
      both deprecatedPublicIPs *and* externalIPs are set, deprecatedPublicIPs is used.
    aliases:
    - deprecated_public_i_ps
    type: list
  spec_external_i_ps:
    description:
    - externalIPs is a list of IP addresses for which nodes in the cluster will also
      accept traffic for this service. These IPs are not managed by Kubernetes. The
      user is responsible for ensuring that traffic arrives at a node with this IP.
      A common example is external load-balancers that are not part of the Kubernetes
      system. A previous form of this functionality exists as the deprecatedPublicIPs
      field. When using this field, callers should also clear the deprecatedPublicIPs
      field.
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
    - Determines if the object should be created, patched, deleted or replaced. When
      set to C(present), the object will be created, if it does not exist, or patched,
      if requested parameters differ from existing object attributes. If set to C(absent),
      an existing object will be deleted, and if set to C(replaced), an existing object
      will be completely replaced with a new object created from the supplied parameters.
    default: present
    choices:
    - present
    - absent
    - replaced
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
- name: Create service
  k8s_v1_service:
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
  k8s_v1_service:
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
    type: NodePort

- name: Create service
  k8s_v1_service:
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
  k8s_v1_service:
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
  k8s_v1_service:
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
    type: ClusterIP
'''

RETURN = '''
api_version:
  type: string
  description: Requested API version
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
      - Spec defines the behavior of a service. http://releases.k8s.io/HEAD/docs/devel/api-conventions.md
      type: complex
      contains:
        cluster_ip:
          description:
          - clusterIP is the IP address of the service and is usually assigned randomly
            by the master. If an address is specified manually and is not in use by
            others, it will be allocated to the service; otherwise, creation of the
            service will fail. This field can not be changed through updates. Valid
            values are "None", empty string (""), or a valid IP address. "None" can
            be specified for headless services when proxying is not required. Only
            applies to types ClusterIP, NodePort, and LoadBalancer. Ignored if type
            is ExternalName.
          type: str
        deprecated_public_i_ps:
          description:
          - deprecatedPublicIPs is deprecated and replaced by the externalIPs field
            with almost the exact same semantics. This field is retained in the v1
            API for compatibility until at least 8/20/2016. It will be removed from
            any new API revisions. If both deprecatedPublicIPs *and* externalIPs are
            set, deprecatedPublicIPs is used.
          type: list
          contains: str
        external_i_ps:
          description:
          - externalIPs is a list of IP addresses for which nodes in the cluster will
            also accept traffic for this service. These IPs are not managed by Kubernetes.
            The user is responsible for ensuring that traffic arrives at a node with
            this IP. A common example is external load-balancers that are not part
            of the Kubernetes system. A previous form of this functionality exists
            as the deprecatedPublicIPs field. When using this field, callers should
            also clear the deprecatedPublicIPs field.
          type: list
          contains: str
        external_name:
          description:
          - externalName is the external reference that kubedns or equivalent will
            return as a CNAME record for this service. No proxying will be involved.
            Must be a valid DNS name and requires Type to be ExternalName.
          type: str
        load_balancer_ip:
          description:
          - 'Only applies to Service Type: LoadBalancer LoadBalancer will get created
            with the IP specified in this field. This feature depends on whether the
            underlying cloud-provider supports specifying the loadBalancerIP when
            a load balancer is created. This field will be ignored if the cloud-provider
            does not support the feature.'
          type: str
        load_balancer_source_ranges:
          description:
          - If specified and supported by the platform, this will restrict traffic
            through the cloud-provider load-balancer will be restricted to the specified
            client IPs. This field will be ignored if the cloud-provider does not
            support the feature."
          type: list
          contains: str
        ports:
          description:
          - The list of ports that are exposed by this service.
          type: list
          contains:
            name:
              description:
              - The name of this port within the service. This must be a DNS_LABEL.
                All ports within a ServiceSpec must have unique names. This maps to
                the 'Name' field in EndpointPort objects. Optional if only one ServicePort
                is defined on this service.
              type: str
            node_port:
              description:
              - The port on each node on which this service is exposed when type=NodePort
                or LoadBalancer. Usually assigned by the system. If specified, it
                will be allocated to the service if unused or else creation of the
                service will fail. Default is to auto-allocate a port if the ServiceType
                of this Service requires one.
              type: int
            port:
              description:
              - The port that will be exposed by this service.
              type: int
            protocol:
              description:
              - The IP protocol for this port. Supports "TCP" and "UDP". Default is
                TCP.
              type: str
            target_port:
              description:
              - Number or name of the port to access on the pods targeted by the service.
                Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME.
                If this is a string, it will be looked up as a named port in the target
                Pod's container ports. If this is not specified, the value of the
                'port' field is used (an identity map). This field is ignored for
                services with clusterIP=None, and should be omitted or set equal to
                the 'port' field.
              type: complex
              contains: {}
        selector:
          description:
          - Route service traffic to pods with label keys and values matching this
            selector. If empty or not present, the service is assumed to have an external
            process managing its endpoints, which Kubernetes will not modify. Only
            applies to types ClusterIP, NodePort, and LoadBalancer. Ignored if type
            is ExternalName.
          type: complex
          contains: str, str
        session_affinity:
          description:
          - Supports "ClientIP" and "None". Used to maintain session affinity. Enable
            client IP based session affinity. Must be ClientIP or None. Defaults to
            None.
          type: str
        type:
          description:
          - type determines how the Service is exposed. Defaults to ClusterIP. Valid
            options are ExternalName, ClusterIP, NodePort, and LoadBalancer. "ExternalName"
            maps to the specified externalName. "ClusterIP" allocates a cluster-internal
            IP address for load-balancing to endpoints. Endpoints are determined by
            the selector or if that is not specified, by manual construction of an
            Endpoints object. If clusterIP is "None", no virtual IP is allocated and
            the endpoints are published as a set of endpoints rather than a stable
            IP. "NodePort" builds on ClusterIP and allocates a port on every node
            which routes to the clusterIP. "LoadBalancer" builds on NodePort and creates
            an external load-balancer (if supported in the current cloud) which routes
            to the clusterIP.
          type: str
    status:
      description:
      - Most recently observed status of the service. Populated by the system. Read-only.
      type: complex
      contains:
        load_balancer:
          description:
          - LoadBalancer contains the current status of the load-balancer, if one
            is present.
          type: complex
          contains:
            ingress:
              description:
              - Ingress is a list containing ingress points for the load-balancer.
                Traffic intended for the service should be sent to these ingress points.
              type: list
              contains:
                hostname:
                  description:
                  - Hostname is set for load-balancer ingress points that are DNS
                    based (typically AWS load-balancers)
                  type: str
                ip:
                  description:
                  - IP is set for load-balancer ingress points that are IP based (typically
                    GCE or OpenStack load-balancers)
                  type: str
'''


def main():
    try:
        module = OpenShiftAnsibleModule('service', 'V1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()

