#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.openshift_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: openshift_v1_image_list
short_description: OpenShift ImageList
description:
- Retrieve a list of images. List operations provide a snapshot read of the underlying
  objects, returning a resource_version representing a consistent version of the listed
  objects.
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
image_list:
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
      - Items is a list of images
      type: list
      contains:
        api_version:
          description:
          - APIVersion defines the versioned schema of this representation of an object.
            Servers should convert recognized schemas to the latest internal value,
            and may reject unrecognized values.
          type: str
        docker_image_config:
          description:
          - DockerImageConfig is a JSON blob that the runtime uses to set up the container.
            This is a part of manifest schema v2.
          type: str
        docker_image_layers:
          description:
          - DockerImageLayers represents the layers in the image. May not be set if
            the image does not define that data.
          type: list
          contains:
            media_type:
              description:
              - MediaType of the referenced object.
              type: str
            name:
              description:
              - Name of the layer as defined by the underlying store.
              type: str
            size:
              description:
              - Size of the layer in bytes as defined by the underlying store.
              type: int
        docker_image_manifest:
          description:
          - DockerImageManifest is the raw JSON of the manifest
          type: str
        docker_image_manifest_media_type:
          description:
          - DockerImageManifestMediaType specifies the mediaType of manifest. This
            is a part of manifest schema v2.
          type: str
        docker_image_metadata:
          description:
          - DockerImageMetadata contains metadata about this image
          type: complex
        docker_image_metadata_version:
          description:
          - DockerImageMetadataVersion conveys the version of the object, which if
            empty defaults to "1.0"
          type: str
        docker_image_reference:
          description:
          - DockerImageReference is the string that can be used to pull this image.
          type: str
        docker_image_signatures:
          description:
          - DockerImageSignatures provides the signatures as opaque blobs. This is
            a part of manifest schema v1.
          type: list
          contains: str
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
        signatures:
          description:
          - Signatures holds all signatures of the image.
          type: list
          contains:
            api_version:
              description:
              - APIVersion defines the versioned schema of this representation of
                an object. Servers should convert recognized schemas to the latest
                internal value, and may reject unrecognized values.
              type: str
            conditions:
              description:
              - Conditions represent the latest available observations of a signature's
                current state.
              type: list
              contains:
                last_probe_time:
                  description:
                  - Last time the condition was checked.
                  type: complex
                  contains: {}
                last_transition_time:
                  description:
                  - Last time the condition transit from one status to another.
                  type: complex
                  contains: {}
                message:
                  description:
                  - Human readable message indicating details about last transition.
                  type: str
                reason:
                  description:
                  - (brief) reason for the condition's last transition.
                  type: str
                status:
                  description:
                  - Status of the condition, one of True, False, Unknown.
                  type: str
                type:
                  description:
                  - Type of signature condition, Complete or Failed.
                  type: str
            content:
              description:
              - "Required: An opaque binary string which is an image's signature."
              type: str
            created:
              description:
              - If specified, it is the time of signature's creation.
              type: complex
              contains: {}
            image_identity:
              description:
              - A human readable string representing image's identity. It could be
                a product name and version, or an image pull spec (e.g. "registry.access.redhat.com/rhel7/rhel:7.2").
              type: str
            issued_by:
              description:
              - If specified, it holds information about an issuer of signing certificate
                or key (a person or entity who signed the signing certificate or key).
              type: complex
            issued_to:
              description:
              - If specified, it holds information about a subject of signing certificate
                or key (a person or entity who signed the image).
              type: complex
            kind:
              description:
              - Kind is a string value representing the REST resource this object
                represents. Servers may infer this from the endpoint the client submits
                requests to. Cannot be updated. In CamelCase.
              type: str
            metadata:
              description:
              - Standard object's metadata.
              type: complex
            signed_claims:
              description:
              - Contains claims from the signature.
              type: complex
              contains: str, str
            type:
              description:
              - 'Required: Describes a type of stored blob.'
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
        module = OpenShiftAnsibleModule('image_list', 'v1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
