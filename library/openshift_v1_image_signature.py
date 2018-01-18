#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.openshift_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: openshift_v1_image_signature
short_description: OpenShift ImageSignature
description:
- Manage the lifecycle of a image_signature object. Supports check mode, and attempts
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
  conditions:
    description:
    - Conditions represent the latest available observations of a signature's current
      state.
    type: list
  content:
    description:
    - "Required: An opaque binary string which is an image's signature."
  context:
    description:
    - The name of a context found in the Kubernetes config file.
  created:
    description:
    - If specified, it is the time of signature's creation.
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
  image_identity:
    description:
    - A human readable string representing image's identity. It could be a product
      name and version, or an image pull spec (e.g. "registry.access.redhat.com/rhel7/rhel:7.2").
  issued_by_common_name:
    description:
    - Common name (e.g. openshift-signing-service).
    aliases:
    - common_name
  issued_by_organization:
    description:
    - Organization name.
    aliases:
    - organization
  issued_to_common_name:
    description:
    - Common name (e.g. openshift-signing-service).
  issued_to_organization:
    description:
    - Organization name.
  issued_to_public_key_id:
    description:
    - If present, it is a human readable key id of public key belonging to the subject
      used to verify image signature. It should contain at least 64 lowest bits of
      public key's fingerprint (e.g. 0x685ebe62bf278440).
    aliases:
    - public_key_id
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
  signed_claims:
    description:
    - Contains claims from the signature.
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
  type:
    description:
    - 'Required: Describes a type of stored blob.'
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
'''

RETURN = '''
api_version:
  description: Requested API version
  type: string
image_signature:
  type: complex
  returned: when I(state) = C(present)
  contains:
    api_version:
      description:
      - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values.
      type: str
    conditions:
      description:
      - Conditions represent the latest available observations of a signature's current
        state.
      type: list
      contains:
        last_probe_time:
          description:
          - Last time the condition was checked.
          type: complex
          contains: {}
        last_transition_time:
          description:
          - Last time the condition transit from one status to another.
          type: complex
          contains: {}
        message:
          description:
          - Human readable message indicating details about last transition.
          type: str
        reason:
          description:
          - (brief) reason for the condition's last transition.
          type: str
        status:
          description:
          - Status of the condition, one of True, False, Unknown.
          type: str
        type:
          description:
          - Type of signature condition, Complete or Failed.
          type: str
    content:
      description:
      - "Required: An opaque binary string which is an image's signature."
      type: str
    created:
      description:
      - If specified, it is the time of signature's creation.
      type: complex
      contains: {}
    image_identity:
      description:
      - A human readable string representing image's identity. It could be a product
        name and version, or an image pull spec (e.g. "registry.access.redhat.com/rhel7/rhel:7.2").
      type: str
    issued_by:
      description:
      - If specified, it holds information about an issuer of signing certificate
        or key (a person or entity who signed the signing certificate or key).
      type: complex
    issued_to:
      description:
      - If specified, it holds information about a subject of signing certificate
        or key (a person or entity who signed the image).
      type: complex
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
    signed_claims:
      description:
      - Contains claims from the signature.
      type: complex
      contains: str, str
    type:
      description:
      - 'Required: Describes a type of stored blob.'
      type: str
'''


def main():
    try:
        module = OpenShiftAnsibleModule('image_signature', 'v1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
