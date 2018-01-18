#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.openshift_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: openshift_v1_route
short_description: OpenShift Route
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
  spec_alternate_backends:
    description:
    - alternateBackends allows up to 3 additional backends to be assigned to the route.
      Only the Service kind is allowed, and it will be defaulted to Service. Use the
      weight field in RouteTargetReference object to specify relative preference.
    aliases:
    - alternate_backends
    type: list
  spec_host:
    description:
    - host is an alias/DNS that points to the service. Optional. If not specified
      a route name will typically be automatically chosen. Must follow DNS952 subdomain
      conventions.
  spec_path:
    description:
    - Path that the router watches for, to route traffic for to the service. Optional
    aliases:
    - path
  spec_port_target_port:
    description:
    - The target port on pods selected by the service this route points to. If this
      is a string, it will be looked up as a named port in the target endpoints port
      list. Required
    aliases:
    - port_target_port
    type: object
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
      in order to have routers use it for health checks on the secure connection.
      If this field is not specified, the router may provide its own destination CA
      and perform hostname validation using the short service name (service.namespace.svc),
      which allows infrastructure generated certificates to automatically verify.
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
    - weight as an integer between 0 and 256, default 1, that specifies the target's
      relative weight against other target reference objects. 0 suppresses requests
      to this backend.
    aliases:
    - to_weight
    type: int
  spec_wildcard_policy:
    description:
    - Wildcard policy if any for the route. Currently only 'Subdomain' or 'None' is
      allowed.
    aliases:
    - wildcard_policy
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
- openshift == 0.4.0.a1
'''

EXAMPLES = '''
- name: Create route
  openshift_v1_route.yml:
    name: myroute
    namespace: k8s-project
    state: present
    host: www.example.com
    spec_to_kind: Service
    spec_to_name: service-name
    tls_termination: edge
    tls_key: |-
      -----BEGIN PRIVATE KEY-----
      key_file_contents
      -----END PRIVATE KEY-----
    tls_certificate: |-
      -----BEGIN CERTIFICATE-----
      certificate contents
      -----END CERTIFICATE-----
    tls_ca_certificate: |-
      -----BEGIN CERTIFICATE-----
      ca_certificate_contents
      -----END CERTIFICATE-----

- name: Patch route
  openshift_v1_route.yml:
    name: myroute
    namespace: k8s-project
    state: present
    host: www.example.com
    tls_termination: reencrypt
    spec_to_kind: Service
    spec_to_name: other-service-name

- name: Replace route
  openshift_v1_route.yml:
    name: myroute
    namespace: k8s-project
    state: replaced
    host: www.example.com
    path: /foo/bar/baz.html
    spec_to_kind: Service
    spec_to_name: whimsy-name
    tls_termination: edge

- name: Remove route
  openshift_v1_route.yml:
    name: myroute
    namespace: k8s-project
    state: absent
'''

RETURN = '''
api_version:
  description: Requested API version
  type: string
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
    spec:
      description:
      - spec is the desired state of the route
      type: complex
    status:
      description:
      - status is the current state of the route
      type: complex
'''


def main():
    try:
        module = OpenShiftAnsibleModule('route', 'v1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
