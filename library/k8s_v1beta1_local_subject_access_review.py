#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.k8s_common import KubernetesAnsibleModule, KubernetesAnsibleException

DOCUMENTATION = '''
module: k8s_v1beta1_local_subject_access_review
short_description: Kubernetes LocalSubjectAccessReview
description:
- Manage the lifecycle of a local_subject_access_review object. Supports check mode,
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
  spec_extra:
    description:
    - Extra corresponds to the user.Info.GetExtra() method from the authenticator.
      Since that is input to the authorizer it needs a reflection here.
    aliases:
    - extra
    type: dict
  spec_group:
    description:
    - Groups is the groups you're testing for.
    aliases:
    - group
    type: list
  spec_non_resource_attributes_path:
    description:
    - Path is the URL path of the request
    aliases:
    - non_resource_attributes_path
  spec_non_resource_attributes_verb:
    description:
    - Verb is the standard HTTP verb
    aliases:
    - non_resource_attributes_verb
  spec_resource_attributes_group:
    description:
    - Group is the API Group of the Resource. "*" means all.
    aliases:
    - resource_attributes_group
  spec_resource_attributes_name:
    description:
    - Name is the name of the resource being requested for a "get" or deleted for
      a "delete". "" (empty) means all.
    aliases:
    - resource_attributes_name
  spec_resource_attributes_namespace:
    description:
    - Namespace is the namespace of the action being requested. Currently, there is
      no distinction between no namespace and all namespaces "" (empty) is defaulted
      for LocalSubjectAccessReviews "" (empty) is empty for cluster-scoped resources
      "" (empty) means "all" for namespace scoped resources from a SubjectAccessReview
      or SelfSubjectAccessReview
    aliases:
    - resource_attributes_namespace
  spec_resource_attributes_resource:
    description:
    - Resource is one of the existing resource types. "*" means all.
    aliases:
    - resource_attributes_resource
  spec_resource_attributes_subresource:
    description:
    - Subresource is one of the existing resource types. "" means none.
    aliases:
    - resource_attributes_subresource
  spec_resource_attributes_verb:
    description:
    - 'Verb is a kubernetes resource API verb, like: get, list, watch, create, update,
      delete, proxy. "*" means all.'
    aliases:
    - resource_attributes_verb
  spec_resource_attributes_version:
    description:
    - Version is the API Version of the Resource. "*" means all.
    aliases:
    - resource_attributes_version
  spec_uid:
    description:
    - UID information about the requesting user.
    aliases:
    - uid
  spec_user:
    description:
    - User is the user you're testing for. If you specify "User" but not "Group",
      then is it interpreted as "What if User were not a member of any groups
    aliases:
    - user
  ssl_ca_cert:
    description:
    - Path to a CA certificate used to authenticate with the API.
    type: path
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
local_subject_access_review:
  type: complex
  returned: on success
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
      - Spec holds information about the request being evaluated. spec.namespace must
        be equal to the namespace you made the request against. If empty, it is defaulted.
      type: complex
    status:
      description:
      - Status is filled in by the server and indicates whether the request is allowed
        or not
      type: complex
'''


def main():
    try:
        module = KubernetesAnsibleModule('local_subject_access_review', 'v1beta1')
    except KubernetesAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except KubernetesAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
