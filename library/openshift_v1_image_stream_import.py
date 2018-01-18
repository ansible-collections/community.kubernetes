#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.openshift_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: openshift_v1_image_stream_import
short_description: OpenShift ImageStreamImport
description:
- Manage the lifecycle of a image_stream_import object. Supports check mode, and attempts
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
  spec_images:
    description:
    - Images are a list of individual images to import.
    aliases:
    - images
    type: list
  spec_import:
    description:
    - Import indicates whether to perform an import - if so, the specified tags are
      set on the spec and status of the image stream defined by the type meta.
    aliases:
    - import
    type: bool
  spec_repository_from_api_version:
    description:
    - API version of the referent.
    aliases:
    - repository_from_api_version
  spec_repository_from_field_path:
    description:
    - 'If referring to a piece of an object instead of an entire object, this string
      should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2].
      For example, if the object reference is to a container within a pod, this would
      take on a value like: "spec.containers{name}" (where "name" refers to the name
      of the container that triggered the event) or if no container name is specified
      "spec.containers[2]" (container with index 2 in this pod). This syntax is chosen
      only to have some well-defined way of referencing a part of an object.'
    aliases:
    - repository_from_field_path
  spec_repository_from_kind:
    description:
    - Kind of the referent.
    aliases:
    - repository_from_kind
  spec_repository_from_name:
    description:
    - Name of the referent.
    aliases:
    - repository_from_name
  spec_repository_from_namespace:
    description:
    - Namespace of the referent.
    aliases:
    - repository_from_namespace
  spec_repository_from_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - repository_from_resource_version
  spec_repository_from_uid:
    description:
    - UID of the referent.
    aliases:
    - repository_from_uid
  spec_repository_import_policy_insecure:
    description:
    - Insecure is true if the server may bypass certificate verification or connect
      directly over HTTP during image import.
    aliases:
    - repository_import_policy_insecure
    type: bool
  spec_repository_import_policy_scheduled:
    description:
    - Scheduled indicates to the server that this tag should be periodically checked
      to ensure it is up to date, and imported
    aliases:
    - repository_import_policy_scheduled
    type: bool
  spec_repository_include_manifest:
    description:
    - IncludeManifest determines if the manifest for each image is returned in the
      response
    aliases:
    - repository_include_manifest
    type: bool
  spec_repository_reference_policy_type:
    description:
    - Type determines how the image pull spec should be transformed when the image
      stream tag is used in deployment config triggers or new builds. The default
      value is `Source`, indicating the original location of the image should be used
      (if imported). The user may also specify `Local`, indicating that the pull spec
      should point to the integrated Docker registry and leverage the registry's ability
      to proxy the pull to an upstream registry. `Local` allows the credentials used
      to pull this image to be managed from the image stream's namespace, so others
      on the platform can access a remote image but have no access to the remote secret.
      It also allows the image layers to be mirrored into the local registry which
      the images can still be pulled even if the upstream registry is unavailable.
    aliases:
    - repository_reference_policy_type
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
- openshift == 0.4.0.a1
'''

EXAMPLES = '''
'''

RETURN = '''
api_version:
  description: Requested API version
  type: string
image_stream_import:
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
      description:
      - Standard object's metadata.
      type: complex
    spec:
      description:
      - Spec is a description of the images that the user wishes to import
      type: complex
    status:
      description:
      - Status is the the result of importing the image
      type: complex
'''


def main():
    try:
        module = OpenShiftAnsibleModule('image_stream_import', 'v1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
