#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.k8s_common import KubernetesAnsibleModule, KubernetesAnsibleException

DOCUMENTATION = '''
module: k8s_v1beta1_custom_resource_definition
short_description: Kubernetes CustomResourceDefinition
description:
- Manage the lifecycle of a custom_resource_definition object. Supports check mode,
  and attempts to to be idempotent.
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
  spec_group:
    description:
    - Group is the group this resource belongs in
    aliases:
    - group
  spec_names_kind:
    description:
    - Kind is the serialized kind of the resource. It is normally CamelCase and singular.
    aliases:
    - names_kind
  spec_names_list_kind:
    description:
    - ListKind is the serialized kind of the list for this resource. Defaults to <kind>List.
    aliases:
    - names_list_kind
  spec_names_plural:
    description:
    - 'Plural is the plural name of the resource to serve. It must match the name
      of the CustomResourceDefinition-registration too: plural.group and it must be
      all lowercase.'
    aliases:
    - names_plural
  spec_names_short_names:
    description:
    - ShortNames are short names for the resource. It must be all lowercase.
    aliases:
    - names_short_names
    type: list
  spec_names_singular:
    description:
    - Singular is the singular name of the resource. It must be all lowercase Defaults
      to lowercased <kind>
    aliases:
    - names_singular
  spec_scope:
    description:
    - Scope indicates whether this resource is cluster or namespace scoped. Default
      is namespaced
    aliases:
    - scope
  spec_validation_open_apiv3_schema_additional_items_allows:
    aliases:
    - validation_open_apiv3_schema_additional_items_allows
    type: bool
  spec_validation_open_apiv3_schema_additional_properties_allows:
    aliases:
    - validation_open_apiv3_schema_additional_properties_allows
    type: bool
  spec_validation_open_apiv3_schema_all_of:
    aliases:
    - validation_open_apiv3_schema_all_of
    type: list
  spec_validation_open_apiv3_schema_any_of:
    aliases:
    - validation_open_apiv3_schema_any_of
    type: list
  spec_validation_open_apiv3_schema_description:
    aliases:
    - validation_open_apiv3_schema_description
  spec_validation_open_apiv3_schema_enum:
    aliases:
    - validation_open_apiv3_schema_enum
    type: list
  spec_validation_open_apiv3_schema_format:
    aliases:
    - validation_open_apiv3_schema_format
  spec_validation_open_apiv3_schema_id:
    aliases:
    - validation_open_apiv3_schema_id
  spec_validation_open_apiv3_schema_max_length:
    aliases:
    - validation_open_apiv3_schema_max_length
    type: int
  spec_validation_open_apiv3_schema_max_properties:
    aliases:
    - validation_open_apiv3_schema_max_properties
    type: int
  spec_validation_open_apiv3_schema_min_items:
    aliases:
    - validation_open_apiv3_schema_min_items
    type: int
  spec_validation_open_apiv3_schema_min_properties:
    aliases:
    - validation_open_apiv3_schema_min_properties
    type: int
  spec_validation_open_apiv3_schema_minimum:
    aliases:
    - validation_open_apiv3_schema_minimum
    type: float
  spec_validation_open_apiv3_schema_multiple_of:
    aliases:
    - validation_open_apiv3_schema_multiple_of
    type: float
  spec_validation_open_apiv3_schema_pattern:
    aliases:
    - validation_open_apiv3_schema_pattern
  spec_validation_open_apiv3_schema_pattern_properties:
    aliases:
    - validation_open_apiv3_schema_pattern_properties
    type: dict
  spec_validation_open_apiv3_schema_schema:
    aliases:
    - validation_open_apiv3_schema_schema
  spec_validation_open_apiv3_schema_title:
    aliases:
    - validation_open_apiv3_schema_title
  spec_validation_open_apiv3_schema_type:
    aliases:
    - validation_open_apiv3_schema_type
  spec_validation_open_apiv3_schema_unique_items:
    aliases:
    - validation_open_apiv3_schema_unique_items
    type: bool
  spec_version:
    description:
    - Version is the version this resource belongs in
    aliases:
    - version
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
custom_resource_definition:
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
      description: []
      type: complex
    spec:
      description:
      - Spec describes how the user wants the resources to appear
      type: complex
    status:
      description:
      - Status indicates the actual state of the CustomResourceDefinition
      type: complex
'''


def main():
    try:
        module = KubernetesAnsibleModule('custom_resource_definition', 'v1beta1')
    except KubernetesAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except KubernetesAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
