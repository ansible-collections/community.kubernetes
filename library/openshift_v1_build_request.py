#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.openshift_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: openshift_v1_build_request
short_description: OpenShift BuildRequest
description:
- Manage the lifecycle of a build_request object. Supports check mode, and attempts
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
  binary_as_file:
    description:
    - asFile indicates that the provided binary input should be considered a single
      file within the build input. For example, specifying "webapp.war" would place
      the provided binary as `/webapp.war` for the builder. If left empty, the Docker
      and Source build strategies assume this file is a zip, tar, or tar.gz file and
      extract it as the source. The custom strategy receives this binary as standard
      input. This filename may not contain slashes or be '..' or '.'.
    aliases:
    - as_file
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
  docker_strategy_options_build_args:
    description:
    - Args contains any build arguments that are to be passed to Docker. See
    aliases:
    - build_args
    type: list
  docker_strategy_options_no_cache:
    description:
    - noCache overrides the docker-strategy noCache option in the build config
    aliases:
    - no_cache
    type: bool
  env:
    description:
    - env contains additional environment variables you want to pass into a builder
      container.
    type: list
  force:
    description:
    - If set to C(True), and I(state) is C(present), an existing object will updated,
      and lists will be replaced, rather than merged.
    default: false
    type: bool
  from_api_version:
    description:
    - API version of the referent.
    aliases:
    - api_version
  from_field_path:
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
  from_kind:
    description:
    - Kind of the referent.
    aliases:
    - kind
  from_name:
    description:
    - Name of the referent.
  from_namespace:
    description:
    - Namespace of the referent.
  from_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - resource_version
  from_uid:
    description:
    - UID of the referent.
    aliases:
    - uid
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
  last_version:
    description:
    - lastVersion (optional) is the LastVersion of the BuildConfig that was used to
      generate the build. If the BuildConfig in the generator doesn't match, a build
      will not be generated.
    type: int
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
  revision_git_author_email:
    description:
    - email of the source control user
    aliases:
    - email
  revision_git_author_name:
    description:
    - name of the source control user
  revision_git_commit:
    description:
    - commit is the commit hash identifying a specific commit
    aliases:
    - commit
  revision_git_committer_email:
    description:
    - email of the source control user
  revision_git_committer_name:
    description:
    - name of the source control user
  revision_git_message:
    description:
    - message is the description of a specific commit
    aliases:
    - message
  revision_type:
    description:
    - type of the build source, may be one of 'Source', 'Dockerfile', 'Binary', or
      'Images'
    aliases:
    - type
  source_strategy_options_incremental:
    description:
    - incremental overrides the source-strategy incremental option in the build config
    aliases:
    - incremental
    type: bool
  ssl_ca_cert:
    description:
    - Path to a CA certificate used to authenticate with the API.
    type: path
  triggered_by:
    description:
    - triggeredBy describes which triggers started the most recent update to the build
      configuration and contains information about those triggers.
    type: list
  triggered_by_image_api_version:
    description:
    - API version of the referent.
  triggered_by_image_field_path:
    description:
    - 'If referring to a piece of an object instead of an entire object, this string
      should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2].
      For example, if the object reference is to a container within a pod, this would
      take on a value like: "spec.containers{name}" (where "name" refers to the name
      of the container that triggered the event) or if no container name is specified
      "spec.containers[2]" (container with index 2 in this pod). This syntax is chosen
      only to have some well-defined way of referencing a part of an object.'
  triggered_by_image_kind:
    description:
    - Kind of the referent.
  triggered_by_image_name:
    description:
    - Name of the referent.
  triggered_by_image_namespace:
    description:
    - Namespace of the referent.
  triggered_by_image_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
  triggered_by_image_uid:
    description:
    - UID of the referent.
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
build_request:
  type: complex
  returned: on success
  contains:
    from:
      description:
      - from is the reference to the ImageStreamTag that triggered the build.
      type: complex
    api_version:
      description:
      - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values.
      type: str
    binary:
      description:
      - binary indicates a request to build from a binary provided to the builder
      type: complex
    docker_strategy_options:
      description:
      - DockerStrategyOptions contains additional docker-strategy specific options
        for the build
      type: complex
    env:
      description:
      - env contains additional environment variables you want to pass into a builder
        container.
      type: list
      contains:
        name:
          description:
          - Name of the environment variable. Must be a C_IDENTIFIER.
          type: str
        value:
          description:
          - 'Variable references $(VAR_NAME) are expanded using the previous defined
            environment variables in the container and any service environment variables.
            If a variable cannot be resolved, the reference in the input string will
            be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$,
            ie: $$(VAR_NAME). Escaped references will never be expanded, regardless
            of whether the variable exists or not. Defaults to "".'
          type: str
        value_from:
          description:
          - Source for the environment variable's value. Cannot be used if value is
            not empty.
          type: complex
    kind:
      description:
      - Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to. Cannot
        be updated. In CamelCase.
      type: str
    last_version:
      description:
      - lastVersion (optional) is the LastVersion of the BuildConfig that was used
        to generate the build. If the BuildConfig in the generator doesn't match,
        a build will not be generated.
      type: int
    metadata:
      description:
      - metadata for BuildRequest.
      type: complex
    revision:
      description:
      - revision is the information from the source for a specific repo snapshot.
      type: complex
    source_strategy_options:
      description:
      - SourceStrategyOptions contains additional source-strategy specific options
        for the build
      type: complex
    triggered_by:
      description:
      - triggeredBy describes which triggers started the most recent update to the
        build configuration and contains information about those triggers.
      type: list
      contains:
        bitbucket_web_hook:
          description:
          - BitbucketWebHook represents data for a Bitbucket webhook that fired a
            specific build.
          type: complex
        generic_web_hook:
          description:
          - genericWebHook holds data about a builds generic webhook trigger.
          type: complex
        github_web_hook:
          description:
          - gitHubWebHook represents data for a GitHub webhook that fired a specific
            build.
          type: complex
        gitlab_web_hook:
          description:
          - GitLabWebHook represents data for a GitLab webhook that fired a specific
            build.
          type: complex
        image_change_build:
          description:
          - imageChangeBuild stores information about an imagechange event that triggered
            a new build.
          type: complex
        message:
          description:
          - 'message is used to store a human readable message for why the build was
            triggered. E.g.: "Manually triggered by user", "Configuration change",etc.'
          type: str
    triggered_by_image:
      description:
      - triggeredByImage is the Image that triggered this build.
      type: complex
'''


def main():
    try:
        module = OpenShiftAnsibleModule('build_request', 'v1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
