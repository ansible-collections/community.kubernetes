#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.openshift_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: openshift_v1_image_stream_image
short_description: OpenShift ImageStreamImage
description:
- Manage the lifecycle of a image_stream_image object. Supports check mode, and attempts
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
  image_api_version:
    description:
    - APIVersion defines the versioned schema of this representation of an object.
      Servers should convert recognized schemas to the latest internal value, and
      may reject unrecognized values.
    aliases:
    - api_version
  image_docker_image_config:
    description:
    - DockerImageConfig is a JSON blob that the runtime uses to set up the container.
      This is a part of manifest schema v2.
    aliases:
    - docker_image_config
  image_docker_image_layers:
    description:
    - DockerImageLayers represents the layers in the image. May not be set if the
      image does not define that data.
    aliases:
    - docker_image_layers
    type: list
  image_docker_image_manifest:
    description:
    - DockerImageManifest is the raw JSON of the manifest
    aliases:
    - docker_image_manifest
  image_docker_image_manifest_media_type:
    description:
    - DockerImageManifestMediaType specifies the mediaType of manifest. This is a
      part of manifest schema v2.
    aliases:
    - docker_image_manifest_media_type
  image_docker_image_metadata_raw:
    description:
    - Raw is the underlying serialization of this object.
    aliases:
    - image_docker_metadata_raw
  image_docker_image_metadata_version:
    description:
    - DockerImageMetadataVersion conveys the version of the object, which if empty
      defaults to "1.0"
    aliases:
    - docker_image_metadata_version
  image_docker_image_reference:
    description:
    - DockerImageReference is the string that can be used to pull this image.
    aliases:
    - docker_image_reference
  image_docker_image_signatures:
    description:
    - DockerImageSignatures provides the signatures as opaque blobs. This is a part
      of manifest schema v1.
    aliases:
    - docker_image_signatures
    type: list
  image_kind:
    description:
    - Kind is a string value representing the REST resource this object represents.
      Servers may infer this from the endpoint the client submits requests to. Cannot
      be updated. In CamelCase.
    aliases:
    - kind
  image_metadata_annotations:
    description:
    - Annotations is an unstructured key value map stored with a resource that may
      be set by external tools to store and retrieve arbitrary metadata. They are
      not queryable and should be preserved when modifying objects.
    type: dict
  image_metadata_labels:
    description:
    - Map of string keys and values that can be used to organize and categorize (scope
      and select) objects. May match selectors of replication controllers and services.
    type: dict
  image_metadata_name:
    description:
    - Name must be unique within a namespace. Is required when creating resources,
      although some resources may allow a client to request the generation of an appropriate
      name automatically. Name is primarily intended for creation idempotence and
      configuration definition. Cannot be updated.
  image_metadata_namespace:
    description:
    - Namespace defines the space within each name must be unique. An empty namespace
      is equivalent to the "default" namespace, but "default" is the canonical representation.
      Not all objects are required to be scoped to a namespace - the value of this
      field for those objects will be empty. Must be a DNS_LABEL. Cannot be updated.
  image_signatures:
    description:
    - Signatures holds all signatures of the image.
    aliases:
    - signatures
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
image_stream_image:
  type: complex
  returned: on success
  contains:
    api_version:
      description:
      - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values.
      type: str
    image:
      description:
      - Image associated with the ImageStream and image name.
      type: complex
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
        module = OpenShiftAnsibleModule('image_stream_image', 'v1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
