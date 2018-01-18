#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.openshift_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: openshift_v1_image_stream_tag
short_description: OpenShift ImageStreamTag
description:
- Manage the lifecycle of a image_stream_tag object. Supports check mode, and attempts
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
  conditions:
    description:
    - conditions is an array of conditions that apply to the image stream tag.
    type: list
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
  generation:
    description:
    - generation is the current generation of the tagged image - if tag is provided
      and this value is not equal to the tag generation, a user has requested an import
      that has not completed, or conditions will be filled out indicating any error.
    type: int
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
  lookup_policy_local:
    description:
    - local will change the docker short image references (like "mysql" or "php:latest")
      on objects in this namespace to the image ID whenever they match this image
      stream, instead of reaching out to a remote registry. The name will be fully
      qualified to an image ID if found. The tag's referencePolicy is taken into account
      on the replaced value. Only works within the current namespace.
    aliases:
    - local
    type: bool
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
  tag_annotations:
    description:
    - Optional; if specified, annotations that are applied to images retrieved via
      ImageStreamTags.
    type: dict
  tag_from_api_version:
    description:
    - API version of the referent.
  tag_from_field_path:
    description:
    - 'If referring to a piece of an object instead of an entire object, this string
      should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2].
      For example, if the object reference is to a container within a pod, this would
      take on a value like: "spec.containers{name}" (where "name" refers to the name
      of the container that triggered the event) or if no container name is specified
      "spec.containers[2]" (container with index 2 in this pod). This syntax is chosen
      only to have some well-defined way of referencing a part of an object.'
    aliases:
    - field_path
  tag_from_kind:
    description:
    - Kind of the referent.
  tag_from_name:
    description:
    - Name of the referent.
  tag_from_namespace:
    description:
    - Namespace of the referent.
  tag_from_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - resource_version
  tag_from_uid:
    description:
    - UID of the referent.
    aliases:
    - uid
  tag_generation:
    description:
    - Generation is a counter that tracks mutations to the spec tag (user intent).
      When a tag reference is changed the generation is set to match the current stream
      generation (which is incremented every time spec is changed). Other processes
      in the system like the image importer observe that the generation of spec tag
      is newer than the generation recorded in the status and use that as a trigger
      to import the newest remote tag. To trigger a new import, clients may set this
      value to zero which will reset the generation to the latest stream generation.
      Legacy clients will send this value as nil which will be merged with the current
      tag generation.
    type: int
  tag_import_policy_insecure:
    description:
    - Insecure is true if the server may bypass certificate verification or connect
      directly over HTTP during image import.
    aliases:
    - insecure
    type: bool
  tag_import_policy_scheduled:
    description:
    - Scheduled indicates to the server that this tag should be periodically checked
      to ensure it is up to date, and imported
    aliases:
    - scheduled
    type: bool
  tag_name:
    description:
    - Name of the tag
  tag_reference:
    description:
    - Reference states if the tag will be imported. Default value is false, which
      means the tag will be imported.
    aliases:
    - reference
    type: bool
  tag_reference_policy_type:
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
    - type
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
image_stream_tag:
  type: complex
  returned: when I(state) = C(present)
  contains:
    api_version:
      description:
      - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values.
      type: str
    conditions:
      description:
      - conditions is an array of conditions that apply to the image stream tag.
      type: list
      contains:
        generation:
          description:
          - Generation is the spec tag generation that this status corresponds to
          type: int
        last_transition_time:
          description:
          - LastTransitionTIme is the time the condition transitioned from one status
            to another.
          type: complex
          contains: {}
        message:
          description:
          - Message is a human readable description of the details about last transition,
            complementing reason.
          type: str
        reason:
          description:
          - Reason is a brief machine readable explanation for the condition's last
            transition.
          type: str
        status:
          description:
          - Status of the condition, one of True, False, Unknown.
          type: str
        type:
          description:
          - Type of tag event condition, currently only ImportSuccess
          type: str
    generation:
      description:
      - generation is the current generation of the tagged image - if tag is provided
        and this value is not equal to the tag generation, a user has requested an
        import that has not completed, or conditions will be filled out indicating
        any error.
      type: int
    image:
      description:
      - image associated with the ImageStream and tag.
      type: complex
    kind:
      description:
      - Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to. Cannot
        be updated. In CamelCase.
      type: str
    lookup_policy:
      description:
      - lookupPolicy indicates whether this tag will handle image references in this
        namespace.
      type: complex
    metadata:
      description:
      - Standard object's metadata.
      type: complex
    tag:
      description:
      - tag is the spec tag associated with this image stream tag, and it may be null
        if only pushes have occurred to this image stream.
      type: complex
'''


def main():
    try:
        module = OpenShiftAnsibleModule('image_stream_tag', 'v1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
