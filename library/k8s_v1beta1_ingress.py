#!/usr/bin/env python

from ansible.module_utils.k8s_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: k8s_v1beta1_ingress
short_description: Kubernetes Ingress
description:
- Manage the lifecycle of a ingress object. Supports check mode, and attempts to to
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
  spec_backend_service_name:
    description:
    - Specifies the name of the referenced service.
    aliases:
    - backend_service_name
  spec_rules:
    description:
    - A list of host rules used to configure the Ingress. If unspecified, or no rule
      matches, all traffic is sent to the default backend.
    aliases:
    - rules
    type: list
  spec_tls:
    description:
    - TLS configuration. Currently the Ingress only supports a single TLS port, 443.
      If multiple members of this list specify different hosts, they will be multiplexed
      on the same port according to the hostname specified through the SNI TLS extension,
      if the ingress controller fulfilling the ingress supports SNI.
    aliases:
    - tls
    type: list
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
'''

RETURN = '''
api_version:
  type: string
  description: Requested API version
ingress:
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
      - Spec is the desired state of the Ingress.
      type: complex
      contains:
        backend:
          description:
          - A default backend capable of servicing requests that don't match any rule.
            At least one of 'backend' or 'rules' must be specified. This field is
            optional to allow the loadbalancer controller or defaulting logic to specify
            a global default.
          type: complex
          contains:
            service_name:
              description:
              - Specifies the name of the referenced service.
              type: str
            service_port:
              description:
              - Specifies the port of the referenced service.
              type: complex
              contains: {}
        rules:
          description:
          - A list of host rules used to configure the Ingress. If unspecified, or
            no rule matches, all traffic is sent to the default backend.
          type: list
          contains:
            host:
              description:
              - 'Host is the fully qualified domain name of a network host, as defined
                by RFC 3986. Note the following deviations from the "host" part of
                the URI as defined in the RFC: 1. IPs are not allowed. Currently an
                IngressRuleValue can only apply to the IP in the Spec of the parent
                Ingress. 2. The `:` delimiter is not respected because ports are not
                allowed. Currently the port of an Ingress is implicitly :80 for http
                and :443 for https. Both these may change in the future. Incoming
                requests are matched against the host before the IngressRuleValue.
                If the host is unspecified, the Ingress routes all traffic based on
                the specified IngressRuleValue.'
              type: str
            http:
              description: []
              type: complex
              contains:
                paths:
                  description:
                  - A collection of paths that map requests to backends.
                  type: list
                  contains:
                    backend:
                      description:
                      - Backend defines the referenced service endpoint to which the
                        traffic will be forwarded to.
                      type: complex
                      contains:
                        service_name:
                          description:
                          - Specifies the name of the referenced service.
                          type: str
                        service_port:
                          description:
                          - Specifies the port of the referenced service.
                          type: complex
                          contains: {}
                    path:
                      description:
                      - Path is an extended POSIX regex as defined by IEEE Std 1003.1,
                        (i.e this follows the egrep/unix syntax, not the perl syntax)
                        matched against the path of an incoming request. Currently
                        it can contain characters disallowed from the conventional
                        "path" part of a URL as defined by RFC 3986. Paths must begin
                        with a '/'. If unspecified, the path defaults to a catch all
                        sending traffic to the backend.
                      type: str
        tls:
          description:
          - TLS configuration. Currently the Ingress only supports a single TLS port,
            443. If multiple members of this list specify different hosts, they will
            be multiplexed on the same port according to the hostname specified through
            the SNI TLS extension, if the ingress controller fulfilling the ingress
            supports SNI.
          type: list
          contains:
            hosts:
              description:
              - Hosts are a list of hosts included in the TLS certificate. The values
                in this list must match the name/s used in the tlsSecret. Defaults
                to the wildcard host setting for the loadbalancer controller fulfilling
                this Ingress, if left unspecified.
              type: list
              contains: str
            secret_name:
              description:
              - SecretName is the name of the secret used to terminate SSL traffic
                on 443. Field is left optional to allow SSL routing based on SNI hostname
                alone. If the SNI host in a listener conflicts with the "Host" header
                field used by an IngressRule, the SNI host is used for termination
                and value of the Host header is used for routing.
              type: str
    status:
      description:
      - Status is the current state of the Ingress.
      type: complex
      contains:
        load_balancer:
          description:
          - LoadBalancer contains the current status of the load-balancer.
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
        module = OpenShiftAnsibleModule('ingress', 'V1beta1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()

