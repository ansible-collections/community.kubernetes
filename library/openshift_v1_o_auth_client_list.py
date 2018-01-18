#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.openshift_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: openshift_v1_o_auth_client_list
short_description: OpenShift OAuthClientList
description:
- Retrieve a list of o_auth_clients. List operations provide a snapshot read of the
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
o_auth_client_list:
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
      - Items is the list of OAuth clients
      type: list
      contains:
        access_token_inactivity_timeout_seconds:
          description:
          - 'AccessTokenInactivityTimeoutSeconds overrides the default token inactivity
            timeout for tokens granted to this client. The value represents the maximum
            amount of time that can occur between consecutive uses of the token. Tokens
            become invalid if they are not used within this temporal window. The user
            will need to acquire a new token to regain access once a token times out.
            This value needs to be set only if the default set in configuration is
            not appropriate for this client. Valid values are: - 0: Tokens for this
            client never time out - X: Tokens time out if there is no activity for
            X seconds The current minimum allowed value for X is 300 (5 minutes)'
          type: int
        access_token_max_age_seconds:
          description:
          - AccessTokenMaxAgeSeconds overrides the default access token max age for
            tokens granted to this client. 0 means no expiration.
          type: int
        additional_secrets:
          description:
          - AdditionalSecrets holds other secrets that may be used to identify the
            client. This is useful for rotation and for service account token validation
          type: list
          contains: str
        api_version:
          description:
          - APIVersion defines the versioned schema of this representation of an object.
            Servers should convert recognized schemas to the latest internal value,
            and may reject unrecognized values.
          type: str
        grant_method:
          description:
          - 'GrantMethod determines how to handle grants for this client. If no method
            is provided, the cluster default grant handling method will be used. Valid
            grant handling methods are: - auto: always approves grant requests, useful
            for trusted clients - prompt: prompts the end user for approval of grant
            requests, useful for third-party clients - deny: always denies grant requests,
            useful for black-listed clients'
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
        redirect_ur_is:
          description:
          - RedirectURIs is the valid redirection URIs associated with a client
          type: list
          contains: str
        respond_with_challenges:
          description:
          - RespondWithChallenges indicates whether the client wants authentication
            needed responses made in the form of challenges instead of redirects
          type: bool
        scope_restrictions:
          description:
          - ScopeRestrictions describes which scopes this client can request. Each
            requested scope is checked against each restriction. If any restriction
            matches, then the scope is allowed. If no restriction matches, then the
            scope is denied.
          type: list
          contains:
            cluster_role:
              description:
              - ClusterRole describes a set of restrictions for cluster role scoping.
              type: complex
            literals:
              description:
              - ExactValues means the scope has to match a particular set of strings
                exactly
              type: list
              contains: str
        secret:
          description:
          - Secret is the unique secret associated with a client
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
'''


def main():
    try:
        module = OpenShiftAnsibleModule('o_auth_client_list', 'v1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
