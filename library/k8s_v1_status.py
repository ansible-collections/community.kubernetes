#!/usr/bin/env python

from ansible.module_utils.k8s_common import KubernetesAnsibleModule, KubernetesAnsibleException

DOCUMENTATION = '''
module: k8s_v1_status
short_description: Kubernetes Status
description:
- Manage the lifecycle of a status object. Supports check mode, and attempts to to
  be idempotent.
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
  code:
    description:
    - Suggested HTTP return code for this status, 0 if not set.
    type: int
  context:
    description:
    - The name of a context found in the Kubernetes config file.
  debug:
    description:
    - Enable debug output from the OpenShift helper. Logging info is written to KubeObjHelper.log
    default: false
    type: bool
  details_causes:
    description:
    - The Causes array includes more details associated with the StatusReason failure.
      Not all StatusReasons may provide detailed causes.
    aliases:
    - causes
    type: list
  details_group:
    description:
    - The group attribute of the resource associated with the status StatusReason.
    aliases:
    - group
  details_kind:
    description:
    - The kind attribute of the resource associated with the status StatusReason.
      On some operations may differ from the requested resource Kind.
    aliases:
    - kind
  details_name:
    description:
    - The name attribute of the resource associated with the status StatusReason (when
      there is a single name which can be described).
    aliases:
    - name
  details_retry_after_seconds:
    description:
    - If specified, the time in seconds before the operation should be retried.
    aliases:
    - retry_after_seconds
    type: int
  details_uid:
    description:
    - UID of the resource. (when there is a single resource which can be described).
    aliases:
    - uid
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
  message:
    description:
    - A human-readable description of the status of this operation.
  password:
    description:
    - Provide a password for connecting to the API. Use in conjunction with I(username).
  reason:
    description:
    - A machine-readable description of why this operation is in the "Failure" status.
      If this value is empty there is no information available. A Reason clarifies
      an HTTP status code but does not override it.
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
- kubernetes == 3.0.0
'''

EXAMPLES = '''
'''

RETURN = '''
api_version:
  type: string
  description: Requested API version
status:
  type: complex
  returned: on success
  contains:
    api_version:
      description:
      - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values.
      type: str
    code:
      description:
      - Suggested HTTP return code for this status, 0 if not set.
      type: int
    details:
      description:
      - Extended data associated with the reason. Each reason may define its own extended
        details. This field is optional and the data returned is not guaranteed to
        conform to any schema except that defined by the reason type.
      type: complex
      contains:
        causes:
          description:
          - The Causes array includes more details associated with the StatusReason
            failure. Not all StatusReasons may provide detailed causes.
          type: list
          contains:
            field:
              description:
              - 'The field of the resource that has caused this error, as named by
                its JSON serialization. May include dot and postfix notation for nested
                attributes. Arrays are zero-indexed. Fields may appear more than once
                in an array of causes due to fields having multiple errors. Optional.
                Examples: "name" - the field "name" on the current resource "items[0].name"
                - the field "name" on the first array entry in "items"'
              type: str
            message:
              description:
              - A human-readable description of the cause of the error. This field
                may be presented as-is to a reader.
              type: str
            reason:
              description:
              - A machine-readable description of the cause of the error. If this
                value is empty there is no information available.
              type: str
        group:
          description:
          - The group attribute of the resource associated with the status StatusReason.
          type: str
        kind:
          description:
          - The kind attribute of the resource associated with the status StatusReason.
            On some operations may differ from the requested resource Kind.
          type: str
        name:
          description:
          - The name attribute of the resource associated with the status StatusReason
            (when there is a single name which can be described).
          type: str
        retry_after_seconds:
          description:
          - If specified, the time in seconds before the operation should be retried.
          type: int
        uid:
          description:
          - UID of the resource. (when there is a single resource which can be described).
          type: str
    kind:
      description:
      - Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to. Cannot
        be updated. In CamelCase.
      type: str
    message:
      description:
      - A human-readable description of the status of this operation.
      type: str
    metadata:
      description:
      - Standard list metadata.
      type: complex
      contains:
        resource_version:
          description:
          - String that identifies the server's internal version of this object that
            can be used by clients to determine when objects have changed. Value must
            be treated as opaque by clients and passed unmodified back to the server.
            Populated by the system. Read-only.
          type: str
        self_link:
          description:
          - SelfLink is a URL representing this object. Populated by the system. Read-only.
          type: str
    reason:
      description:
      - A machine-readable description of why this operation is in the "Failure" status.
        If this value is empty there is no information available. A Reason clarifies
        an HTTP status code but does not override it.
      type: str
    status:
      description:
      - 'Status of the operation. One of: "Success" or "Failure".'
      type: str
'''


def main():
    try:
        module = KubernetesAnsibleModule('status', 'v1')
    except KubernetesAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except KubernetesAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
