#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.k8s_common import KubernetesAnsibleModule, KubernetesAnsibleException

DOCUMENTATION = '''
module: k8s_v1alpha1_initializer_configuration
short_description: Kubernetes InitializerConfiguration
description:
- Manage the lifecycle of a initializer_configuration object. Supports check mode,
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
  initializers:
    description:
    - Initializers is a list of resources and their default initializers Order-sensitive.
      When merging multiple InitializerConfigurations, we sort the initializers from
      different InitializerConfigurations by the name of the InitializerConfigurations;
      the order of the initializers from the same InitializerConfiguration is preserved.
    type: list
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
initializer_configuration:
  type: complex
  returned: when I(state) = C(present)
  contains:
    api_version:
      description:
      - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values.
      type: str
    initializers:
      description:
      - Initializers is a list of resources and their default initializers Order-sensitive.
        When merging multiple InitializerConfigurations, we sort the initializers
        from different InitializerConfigurations by the name of the InitializerConfigurations;
        the order of the initializers from the same InitializerConfiguration is preserved.
      type: list
      contains:
        name:
          description:
          - Name is the identifier of the initializer. It will be added to the object
            that needs to be initialized. Name should be fully qualified, e.g., alwayspullimages.kubernetes.io,
            where "alwayspullimages" is the name of the webhook, and kubernetes.io
            is the name of the organization. Required
          type: str
        rules:
          description:
          - Rules describes what resources/subresources the initializer cares about.
            The initializer cares about an operation if it matches _any_ Rule. Rule.Resources
            must not include subresources.
          type: list
          contains:
            api_groups:
              description:
              - APIGroups is the API groups the resources belong to. '*' is all groups.
                If '*' is present, the length of the slice must be one. Required.
              type: list
              contains: str
            api_versions:
              description:
              - APIVersions is the API versions the resources belong to. '*' is all
                versions. If '*' is present, the length of the slice must be one.
                Required.
              type: list
              contains: str
            resources:
              description:
              - "Resources is a list of resources this rule applies to. For example:\
                \ 'pods' means pods. 'pods/log' means the log subresource of pods.\
                \ '*' means all resources, but not subresources. 'pods/*' means all\
                \ subresources of pods. '*/scale' means all scale subresources. '*/*'\
                \ means all resources and their subresources. If wildcard is present,\
                \ the validation rule will ensure resources do not overlap with each\
                \ other. Depending on the enclosing object, subresources might not\
                \ be allowed. Required."
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
      - Standard object metadata;
      type: complex
'''


def main():
    try:
        module = KubernetesAnsibleModule('initializer_configuration', 'v1alpha1')
    except KubernetesAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except KubernetesAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
