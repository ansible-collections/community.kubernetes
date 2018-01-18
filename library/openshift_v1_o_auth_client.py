#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.openshift_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: openshift_v1_o_auth_client
short_description: OpenShift OAuthClient
description:
- Manage the lifecycle of a o_auth_client object. Supports check mode, and attempts
  to to be idempotent.
version_added: 2.3.0
author: OpenShift (@openshift)
options:
  access_token_inactivity_timeout_seconds:
    description:
    - 'AccessTokenInactivityTimeoutSeconds overrides the default token inactivity
      timeout for tokens granted to this client. The value represents the maximum
      amount of time that can occur between consecutive uses of the token. Tokens
      become invalid if they are not used within this temporal window. The user will
      need to acquire a new token to regain access once a token times out. This value
      needs to be set only if the default set in configuration is not appropriate
      for this client. Valid values are: - 0: Tokens for this client never time out
      - X: Tokens time out if there is no activity for X seconds The current minimum
      allowed value for X is 300 (5 minutes)'
    type: int
  access_token_max_age_seconds:
    description:
    - AccessTokenMaxAgeSeconds overrides the default access token max age for tokens
      granted to this client. 0 means no expiration.
    type: int
  additional_secrets:
    description:
    - AdditionalSecrets holds other secrets that may be used to identify the client.
      This is useful for rotation and for service account token validation
    type: list
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
  grant_method:
    description:
    - 'GrantMethod determines how to handle grants for this client. If no method is
      provided, the cluster default grant handling method will be used. Valid grant
      handling methods are: - auto: always approves grant requests, useful for trusted
      clients - prompt: prompts the end user for approval of grant requests, useful
      for third-party clients - deny: always denies grant requests, useful for black-listed
      clients'
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
  redirect_ur_is:
    description:
    - RedirectURIs is the valid redirection URIs associated with a client
    type: list
  resource_definition:
    description:
    - Provide the YAML definition for the object, bypassing any modules parameters
      intended to define object attributes.
    type: dict
  respond_with_challenges:
    description:
    - RespondWithChallenges indicates whether the client wants authentication needed
      responses made in the form of challenges instead of redirects
    type: bool
  scope_restrictions:
    description:
    - ScopeRestrictions describes which scopes this client can request. Each requested
      scope is checked against each restriction. If any restriction matches, then
      the scope is allowed. If no restriction matches, then the scope is denied.
    type: list
  secret:
    description:
    - Secret is the unique secret associated with a client
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
o_auth_client:
  type: complex
  returned: when I(state) = C(present)
  contains:
    access_token_inactivity_timeout_seconds:
      description:
      - 'AccessTokenInactivityTimeoutSeconds overrides the default token inactivity
        timeout for tokens granted to this client. The value represents the maximum
        amount of time that can occur between consecutive uses of the token. Tokens
        become invalid if they are not used within this temporal window. The user
        will need to acquire a new token to regain access once a token times out.
        This value needs to be set only if the default set in configuration is not
        appropriate for this client. Valid values are: - 0: Tokens for this client
        never time out - X: Tokens time out if there is no activity for X seconds
        The current minimum allowed value for X is 300 (5 minutes)'
      type: int
    access_token_max_age_seconds:
      description:
      - AccessTokenMaxAgeSeconds overrides the default access token max age for tokens
        granted to this client. 0 means no expiration.
      type: int
    additional_secrets:
      description:
      - AdditionalSecrets holds other secrets that may be used to identify the client.
        This is useful for rotation and for service account token validation
      type: list
      contains: str
    api_version:
      description:
      - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values.
      type: str
    grant_method:
      description:
      - 'GrantMethod determines how to handle grants for this client. If no method
        is provided, the cluster default grant handling method will be used. Valid
        grant handling methods are: - auto: always approves grant requests, useful
        for trusted clients - prompt: prompts the end user for approval of grant requests,
        useful for third-party clients - deny: always denies grant requests, useful
        for black-listed clients'
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
    redirect_ur_is:
      description:
      - RedirectURIs is the valid redirection URIs associated with a client
      type: list
      contains: str
    respond_with_challenges:
      description:
      - RespondWithChallenges indicates whether the client wants authentication needed
        responses made in the form of challenges instead of redirects
      type: bool
    scope_restrictions:
      description:
      - ScopeRestrictions describes which scopes this client can request. Each requested
        scope is checked against each restriction. If any restriction matches, then
        the scope is allowed. If no restriction matches, then the scope is denied.
      type: list
      contains:
        cluster_role:
          description:
          - ClusterRole describes a set of restrictions for cluster role scoping.
          type: complex
        literals:
          description:
          - ExactValues means the scope has to match a particular set of strings exactly
          type: list
          contains: str
    secret:
      description:
      - Secret is the unique secret associated with a client
      type: str
'''


def main():
    try:
        module = OpenShiftAnsibleModule('o_auth_client', 'v1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
