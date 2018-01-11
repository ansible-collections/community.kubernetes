#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.k8s_common import KubernetesAnsibleModule, KubernetesAnsibleException

DOCUMENTATION = '''
module: k8s_v1alpha1_external_admission_hook_configuration_list
short_description: Kubernetes ExternalAdmissionHookConfigurationList
description:
- Retrieve a list of external_admission_hook_configurations. List operations provide
  a snapshot read of the underlying objects, returning a resource_version representing
  a consistent version of the listed objects.
version_added: 2.3.0
author: OpenShift (@openshift)
options:
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
external_admission_hook_configuration_list:
  type: complex
  returned: when I(state) = C(present)
  contains:
    api_version:
      description:
      - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values.
      type: str
    items:
      description:
      - List of ExternalAdmissionHookConfiguration.
      type: list
      contains:
        api_version:
          description:
          - APIVersion defines the versioned schema of this representation of an object.
            Servers should convert recognized schemas to the latest internal value,
            and may reject unrecognized values.
          type: str
        external_admission_hooks:
          description:
          - ExternalAdmissionHooks is a list of external admission webhooks and the
            affected resources and operations.
          type: list
          contains:
            client_config:
              description:
              - ClientConfig defines how to communicate with the hook. Required
              type: complex
            failure_policy:
              description:
              - FailurePolicy defines how unrecognized errors from the admission endpoint
                are handled - allowed values are Ignore or Fail. Defaults to Ignore.
              type: str
            name:
              description:
              - The name of the external admission webhook. Name should be fully qualified,
                e.g., imagepolicy.kubernetes.io, where "imagepolicy" is the name of
                the webhook, and kubernetes.io is the name of the organization. Required.
              type: str
            rules:
              description:
              - Rules describes what operations on what resources/subresources the
                webhook cares about. The webhook cares about an operation if it matches
                _any_ Rule.
              type: list
              contains:
                api_groups:
                  description:
                  - APIGroups is the API groups the resources belong to. '*' is all
                    groups. If '*' is present, the length of the slice must be one.
                    Required.
                  type: list
                  contains: str
                api_versions:
                  description:
                  - APIVersions is the API versions the resources belong to. '*' is
                    all versions. If '*' is present, the length of the slice must
                    be one. Required.
                  type: list
                  contains: str
                operations:
                  description:
                  - Operations is the operations the admission hook cares about -
                    CREATE, UPDATE, or * for all operations. If '*' is present, the
                    length of the slice must be one. Required.
                  type: list
                  contains: str
                resources:
                  description:
                  - "Resources is a list of resources this rule applies to. For example:\
                    \ 'pods' means pods. 'pods/log' means the log subresource of pods.\
                    \ '*' means all resources, but not subresources. 'pods/*' means\
                    \ all subresources of pods. '*/scale' means all scale subresources.\
                    \ '*/*' means all resources and their subresources. If wildcard\
                    \ is present, the validation rule will ensure resources do not\
                    \ overlap with each other. Depending on the enclosing object,\
                    \ subresources might not be allowed. Required."
                  type: list
                  contains: str
        kind:
          description:
          - Kind is a string value representing the REST resource this object represents.
            Servers may infer this from the endpoint the client submits requests to.
            Cannot be updated. In CamelCase.
          type: str
        metadata:
          description:
          - Standard object metadata;
          type: complex
    kind:
      description:
      - Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to. Cannot
        be updated. In CamelCase.
      type: str
    metadata:
      description:
      - Standard list metadata.
      type: complex
'''


def main():
    try:
        module = KubernetesAnsibleModule('external_admission_hook_configuration_list', 'v1alpha1')
    except KubernetesAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except KubernetesAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
