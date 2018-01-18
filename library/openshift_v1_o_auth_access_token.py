#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.openshift_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: openshift_v1_o_auth_access_token
short_description: OpenShift OAuthAccessToken
description:
- Manage the lifecycle of a o_auth_access_token object. Supports check mode, and attempts
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
  authorize_token:
    description:
    - AuthorizeToken contains the token that authorized this token
  cert_file:
    description:
    - Path to a certificate used to authenticate with the API.
    type: path
  client_name:
    description:
    - ClientName references the client that created this token.
  context:
    description:
    - The name of a context found in the Kubernetes config file.
  debug:
    description:
    - Enable debug output from the OpenShift helper. Logging info is written to KubeObjHelper.log
    default: false
    type: bool
  expires_in:
    description:
    - ExpiresIn is the seconds from CreationTime before this token expires.
    type: int
  force:
    description:
    - If set to C(True), and I(state) is C(present), an existing object will updated,
      and lists will be replaced, rather than merged.
    default: false
    type: bool
  host:
    description:
    - Provide a URL for acessing the Kubernetes API.
  inactivity_timeout_seconds:
    description:
    - InactivityTimeoutSeconds is the value in seconds, from the CreationTimestamp,
      after which this token can no longer be used. The value is automatically incremented
      when the token is used.
    type: int
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
  redirect_uri:
    description:
    - RedirectURI is the redirection associated with the token.
  refresh_token:
    description:
    - RefreshToken is the value by which this token can be renewed. Can be blank.
  resource_definition:
    description:
    - Provide the YAML definition for the object, bypassing any modules parameters
      intended to define object attributes.
    type: dict
  scopes:
    description:
    - Scopes is an array of the requested scopes.
    type: list
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
  user_name:
    description:
    - UserName is the user name associated with this token
  user_uid:
    description:
    - UserUID is the unique UID associated with this token
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
o_auth_access_token:
  type: complex
  returned: when I(state) = C(present)
  contains:
    api_version:
      description:
      - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values.
      type: str
    authorize_token:
      description:
      - AuthorizeToken contains the token that authorized this token
      type: str
    client_name:
      description:
      - ClientName references the client that created this token.
      type: str
    expires_in:
      description:
      - ExpiresIn is the seconds from CreationTime before this token expires.
      type: int
    inactivity_timeout_seconds:
      description:
      - InactivityTimeoutSeconds is the value in seconds, from the CreationTimestamp,
        after which this token can no longer be used. The value is automatically incremented
        when the token is used.
      type: int
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
    redirect_uri:
      description:
      - RedirectURI is the redirection associated with the token.
      type: str
    refresh_token:
      description:
      - RefreshToken is the value by which this token can be renewed. Can be blank.
      type: str
    scopes:
      description:
      - Scopes is an array of the requested scopes.
      type: list
      contains: str
    user_name:
      description:
      - UserName is the user name associated with this token
      type: str
    user_uid:
      description:
      - UserUID is the unique UID associated with this token
      type: str
'''


def main():
    try:
        module = OpenShiftAnsibleModule('o_auth_access_token', 'v1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
