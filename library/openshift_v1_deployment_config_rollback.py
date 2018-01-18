#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.openshift_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: openshift_v1_deployment_config_rollback
short_description: OpenShift DeploymentConfigRollback
description:
- Manage the lifecycle of a deployment_config_rollback object. Supports check mode,
  and attempts to to be idempotent.
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
  name:
    description:
    - Name of the deployment config that will be rolled back.
  password:
    description:
    - Provide a password for connecting to the API. Use in conjunction with I(username).
  spec_from_api_version:
    description:
    - API version of the referent.
    aliases:
    - from_api_version
  spec_from_field_path:
    description:
    - 'If referring to a piece of an object instead of an entire object, this string
      should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2].
      For example, if the object reference is to a container within a pod, this would
      take on a value like: "spec.containers{name}" (where "name" refers to the name
      of the container that triggered the event) or if no container name is specified
      "spec.containers[2]" (container with index 2 in this pod). This syntax is chosen
      only to have some well-defined way of referencing a part of an object.'
    aliases:
    - from_field_path
  spec_from_kind:
    description:
    - Kind of the referent.
    aliases:
    - from_kind
  spec_from_name:
    description:
    - Name of the referent.
    aliases:
    - from_name
  spec_from_namespace:
    description:
    - Namespace of the referent.
    aliases:
    - from_namespace
  spec_from_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - from_resource_version
  spec_from_uid:
    description:
    - UID of the referent.
    aliases:
    - from_uid
  spec_include_replication_meta:
    description:
    - IncludeReplicationMeta specifies whether to include the replica count and selector.
    aliases:
    - include_replication_meta
    type: bool
  spec_include_strategy:
    description:
    - IncludeStrategy specifies whether to include the deployment Strategy.
    aliases:
    - include_strategy
    type: bool
  spec_include_template:
    description:
    - IncludeTemplate specifies whether to include the PodTemplateSpec.
    aliases:
    - include_template
    type: bool
  spec_include_triggers:
    description:
    - IncludeTriggers specifies whether to include config Triggers.
    aliases:
    - include_triggers
    type: bool
  spec_revision:
    description:
    - Revision to rollback to. If set to 0, rollback to the last revision.
    aliases:
    - revision
    type: int
  ssl_ca_cert:
    description:
    - Path to a CA certificate used to authenticate with the API.
    type: path
  updated_annotations:
    description:
    - UpdatedAnnotations is a set of new annotations that will be added in the deployment
      config.
    type: dict
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
deployment_config_rollback:
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
    name:
      description:
      - Name of the deployment config that will be rolled back.
      type: str
    spec:
      description:
      - Spec defines the options to rollback generation.
      type: complex
    updated_annotations:
      description:
      - UpdatedAnnotations is a set of new annotations that will be added in the deployment
        config.
      type: complex
      contains: str, str
'''


def main():
    try:
        module = OpenShiftAnsibleModule('deployment_config_rollback', 'v1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
