#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.openshift_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: openshift_v1_cluster_role_list
short_description: OpenShift ClusterRoleList
description:
- Retrieve a list of cluster_roles. List operations provide a snapshot read of the
  underlying objects, returning a resource_version representing a consistent version
  of the listed objects.
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
- openshift == 0.4.0.a1
'''

EXAMPLES = '''
'''

RETURN = '''
api_version:
  description: Requested API version
  type: string
cluster_role_list:
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
      - Items is a list of ClusterRoles
      type: list
      contains:
        aggregation_rule:
          description:
          - AggregationRule is an optional field that describes how to build the Rules
            for this ClusterRole. If AggregationRule is set, then the Rules are controller
            managed and direct changes to Rules will be stomped by the controller.
          type: complex
        api_version:
          description:
          - APIVersion defines the versioned schema of this representation of an object.
            Servers should convert recognized schemas to the latest internal value,
            and may reject unrecognized values.
          type: str
        kind:
          description:
          - Kind is a string value representing the REST resource this object represents.
            Servers may infer this from the endpoint the client submits requests to.
            Cannot be updated. In CamelCase.
          type: str
        metadata:
          description:
          - Standard object's metadata.
          type: complex
        rules:
          description:
          - Rules holds all the PolicyRules for this ClusterRole
          type: list
          contains:
            api_groups:
              description:
              - APIGroups is the name of the APIGroup that contains the resources.
                If this field is empty, then both kubernetes and origin API groups
                are assumed. That means that if an action is requested against one
                of the enumerated resources in either the kubernetes or the origin
                API group, the request will be allowed
              type: list
              contains: str
            attribute_restrictions:
              description:
              - AttributeRestrictions will vary depending on what the Authorizer/AuthorizationAttributeBuilder
                pair supports. If the Authorizer does not recognize how to handle
                the AttributeRestrictions, the Authorizer should report an error.
              type: complex
            non_resource_ur_ls:
              description:
              - NonResourceURLsSlice is a set of partial urls that a user should have
                access to. *s are allowed, but only as the full, final step in the
                path This name is intentionally different than the internal type so
                that the DefaultConvert works nicely and because the ordering may
                be different.
              type: list
              contains: str
            resource_names:
              description:
              - ResourceNames is an optional white list of names that the rule applies
                to. An empty set means that everything is allowed.
              type: list
              contains: str
            resources:
              description:
              - Resources is a list of resources this rule applies to. ResourceAll
                represents all resources.
              type: list
              contains: str
            verbs:
              description:
              - Verbs is a list of Verbs that apply to ALL the ResourceKinds and AttributeRestrictions
                contained in this rule. VerbAll represents all kinds.
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
      - Standard object's metadata.
      type: complex
'''


def main():
    try:
        module = OpenShiftAnsibleModule('cluster_role_list', 'v1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
