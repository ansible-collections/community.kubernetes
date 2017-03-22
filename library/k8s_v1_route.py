#!/usr/bin/env python

from ansible.module_utils.k8s_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: k8s_v1_route
short_description: Kubernetes Route
description:
- Manage the lifecycle of a route object. Supports check mode, and attempts to to
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
    required: true
  namespace:
    description:
    - Namespace defines the space within each name must be unique. An empty namespace
      is equivalent to the "default" namespace, but "default" is the canonical representation.
      Not all objects are required to be scoped to a namespace - the value of this
      field for those objects will be empty. Must be a DNS_LABEL. Cannot be updated.
  password:
    description:
    - Provide a password for connecting to the API. Use in conjunction with I(username).
  spec_alternate_backends:
    description:
    - alternateBackends is an extension of the 'to' field. If more than one service
      needs to be pointed to, then use this field. Use the weight field in RouteTargetReference
      object to specify relative preference. If the weight field is zero, the backend
      is ignored.
    aliases:
    - alternate_backends
    type: list
  spec_host:
    description:
    - host is an alias/DNS that points to the service. Optional. If not specified
      a route name will typically be automatically chosen. Must follow DNS952 subdomain
      conventions.
    aliases:
    - host
  spec_path:
    description:
    - Path that the router watches for, to route traffic for to the service. Optional
    aliases:
    - path
  spec_tls_ca_certificate:
    description:
    - caCertificate provides the cert authority certificate contents
    aliases:
    - tls_ca_certificate
  spec_tls_certificate:
    description:
    - certificate provides certificate contents
    aliases:
    - tls_certificate
  spec_tls_destination_ca_certificate:
    description:
    - destinationCACertificate provides the contents of the ca certificate of the
      final destination. When using reencrypt termination this file should be provided
      in order to have routers use it for health checks on the secure connection
    aliases:
    - tls_destination_ca_certificate
  spec_tls_insecure_edge_termination_policy:
    description:
    - insecureEdgeTerminationPolicy indicates the desired behavior for insecure connections
      to a route. While each router may make its own decisions on which ports to expose,
      this is normally port 80. * Allow - traffic is sent to the server on the insecure
      port (default) * Disable - no traffic is allowed on the insecure port. * Redirect
      - clients are redirected to the secure port.
    aliases:
    - tls_insecure_edge_termination_policy
  spec_tls_key:
    description:
    - key provides key file contents
    aliases:
    - tls_key
  spec_tls_termination:
    description:
    - termination indicates termination type.
    aliases:
    - tls_termination
  spec_to_kind:
    description:
    - The kind of target that the route is referring to. Currently, only 'Service'
      is allowed
    aliases:
    - to_kind
  spec_to_name:
    description:
    - name of the service/target that is being referred to. e.g. name of the service
    aliases:
    - to_name
  spec_to_weight:
    description:
    - weight as an integer between 1 and 256 that specifies the target's relative
      weight against other target reference objects
    aliases:
    - to_weight
    type: int
  spec_wildcard_policy:
    description:
    - Wildcard policy if any for the route. Currently only 'Subdomain' or 'None' is
      allowed.
    aliases:
    - wildcard_policy
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
- name: Create route
  k8s_v1_route:
    name: myroute
    namespace: k8s-project
    state: present
    host: www.example.com
    target_reference_kind: Service
    target_reference_name: service-name
    tls_termination: edge
    tls_key: |-
      -----BEGIN PRIVATE KEY-----
      asjdflajd0fjasldjflsjflkjlkjfaljsdfljasljflasjfljsdf
      sdlfjalsdjfljasdfljsljfljsfljdf
      -----END PRIVATE KEY-----
    tls_certificate: |-
      -----BEGIN CERTIFICATE-----
      kdlslfsfljetuoeiursljflsdjffljsfsf90909wrjf94lsjdf99KK
      -----END CERTIFICATE-----
    tls_ca_certificate: |-
      -----BEGIN CERTIFICATE-----
      asdfajflasfjfsljlrjlrjlsjfoijlsornkvksflsbgoehfflf54444
      -----END CERTIFICATE-----

- name: Patch route
  k8s_v1_route:
    name: myroute
    namespace: k8s-project
    state: present
    host: www.example.com
    tls_termination: reencrypt
    target_reference_kind: Service
    target_reference_name: other-service-name
    tls_destination_ca_certificate: |-
      -----BEGIN CERTIFICATE-----
      destination cetricate_contents
      -----END CERTIFICATE-----

- name: Replace route
  k8s_v1_route:
    name: myroute
    namespace: k8s-project
    state: replaced
    host: www.example.com
    path: /foo/bar/baz.html
    target_reference_kind: Service
    target_reference_name: whimsy-name
    tls_termination: edge
    tls_key: |-
      -----BEGIN PRIVATE KEY-----
      key_file_contents
      -----END PRIVATE KEY-----
    tls_certificate: |-
      -----BEGIN CERTIFICATE-----
      certificate_contents
      -----END CERTIFICATE-----
    tls_ca_certificate: |-
      -----BEGIN CERTIFICATE-----
      ca_certificate_contents
      -----END CERTIFICATE-----

- name: Remove route
  k8s_v1_route:
    name: myroute
    namespace: k8s-project
    state: absent
'''

RETURN = '''
api_version:
  type: string
  description: Requested API version
route:
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
      - Standard object metadata.
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
      - spec is the desired state of the route
      type: complex
      contains:
        alternate_backends:
          description:
          - alternateBackends is an extension of the 'to' field. If more than one
            service needs to be pointed to, then use this field. Use the weight field
            in RouteTargetReference object to specify relative preference. If the
            weight field is zero, the backend is ignored.
          type: list
          contains:
            kind:
              description:
              - The kind of target that the route is referring to. Currently, only
                'Service' is allowed
              type: str
            name:
              description:
              - name of the service/target that is being referred to. e.g. name of
                the service
              type: str
            weight:
              description:
              - weight as an integer between 1 and 256 that specifies the target's
                relative weight against other target reference objects
              type: int
        host:
          description:
          - host is an alias/DNS that points to the service. Optional. If not specified
            a route name will typically be automatically chosen. Must follow DNS952
            subdomain conventions.
          type: str
        path:
          description:
          - Path that the router watches for, to route traffic for to the service.
            Optional
          type: str
        port:
          description:
          - If specified, the port to be used by the router. Most routers will use
            all endpoints exposed by the service by default - set this value to instruct
            routers which port to use.
          type: complex
          contains:
            target_port:
              description:
              - The target port on pods selected by the service this route points
                to. If this is a string, it will be looked up as a named port in the
                target endpoints port list. Required
              type: complex
              contains: {}
        tls:
          description:
          - The tls field provides the ability to configure certificates and termination
            for the route.
          type: complex
          contains:
            ca_certificate:
              description:
              - caCertificate provides the cert authority certificate contents
              type: str
            certificate:
              description:
              - certificate provides certificate contents
              type: str
            destination_ca_certificate:
              description:
              - destinationCACertificate provides the contents of the ca certificate
                of the final destination. When using reencrypt termination this file
                should be provided in order to have routers use it for health checks
                on the secure connection
              type: str
            insecure_edge_termination_policy:
              description:
              - insecureEdgeTerminationPolicy indicates the desired behavior for insecure
                connections to a route. While each router may make its own decisions
                on which ports to expose, this is normally port 80. * Allow - traffic
                is sent to the server on the insecure port (default) * Disable - no
                traffic is allowed on the insecure port. * Redirect - clients are
                redirected to the secure port.
              type: str
            key:
              description:
              - key provides key file contents
              type: str
            termination:
              description:
              - termination indicates termination type.
              type: str
        to:
          description:
          - to is an object the route should use as the primary backend. Only the
            Service kind is allowed, and it will be defaulted to Service. If the weight
            field is set to zero, no traffic will be sent to this service.
          type: complex
          contains:
            kind:
              description:
              - The kind of target that the route is referring to. Currently, only
                'Service' is allowed
              type: str
            name:
              description:
              - name of the service/target that is being referred to. e.g. name of
                the service
              type: str
            weight:
              description:
              - weight as an integer between 1 and 256 that specifies the target's
                relative weight against other target reference objects
              type: int
        wildcard_policy:
          description:
          - Wildcard policy if any for the route. Currently only 'Subdomain' or 'None'
            is allowed.
          type: str
    status:
      description:
      - status is the current state of the route
      type: complex
      contains:
        ingress:
          description:
          - ingress describes the places where the route may be exposed. The list
            of ingress points may contain duplicate Host or RouterName values. Routes
            are considered live once they are `Ready`
          type: list
          contains:
            conditions:
              description:
              - Conditions is the state of the route, may be empty.
              type: list
              contains:
                last_transition_time:
                  description:
                  - RFC 3339 date and time when this condition last transitioned
                  type: complex
                  contains: {}
                message:
                  description:
                  - Human readable message indicating details about last transition.
                  type: str
                reason:
                  description:
                  - (brief) reason for the condition's last transition, and is usually
                    a machine and human readable constant
                  type: str
                status:
                  description:
                  - Status is the status of the condition. Can be True, False, Unknown.
                  type: str
                type:
                  description:
                  - Type is the type of the condition. Currently only Ready.
                  type: str
            host:
              description:
              - Host is the host string under which the route is exposed; this value
                is required
              type: str
            router_canonical_hostname:
              description:
              - CanonicalHostname is the external host name for the router that can
                be used as a CNAME for the host requested for this route. This value
                is optional and may not be set in all cases.
              type: str
            router_name:
              description:
              - Name is a name chosen by the router to identify itself; this value
                is required
              type: str
            wildcard_policy:
              description:
              - Wildcard policy is the wildcard policy that was allowed where this
                route is exposed.
              type: str
'''


def main():
    try:
        module = OpenShiftAnsibleModule('route', 'V1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()

