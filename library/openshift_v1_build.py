#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.openshift_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: openshift_v1_build
short_description: OpenShift Build
description:
- Manage the lifecycle of a build object. Supports check mode, and attempts to to
  be idempotent.
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
  resource_definition:
    description:
    - Provide the YAML definition for the object, bypassing any modules parameters
      intended to define object attributes.
    type: dict
  spec_completion_deadline_seconds:
    description:
    - completionDeadlineSeconds is an optional duration in seconds, counted from the
      time when a build pod gets scheduled in the system, that the build may be active
      on a node before the system actively tries to terminate the build; value must
      be positive integer
    aliases:
    - completion_deadline_seconds
    type: int
  spec_node_selector:
    description:
    - nodeSelector is a selector which must be true for the build pod to fit on a
      node If nil, it can be overridden by default build nodeselector values for the
      cluster. If set to an empty map or a map with any values, default build nodeselector
      values are ignored.
    aliases:
    - node_selector
    type: dict
  spec_output_image_labels:
    description:
    - imageLabels define a list of labels that are applied to the resulting image.
      If there are multiple labels with the same name then the last one in the list
      is used.
    aliases:
    - output_image_labels
    type: list
  spec_output_push_secret_name:
    description:
    - Name of the referent.
    aliases:
    - output_push_secret_name
  spec_output_to_api_version:
    description:
    - API version of the referent.
    aliases:
    - output_to_api_version
  spec_output_to_field_path:
    description:
    - 'If referring to a piece of an object instead of an entire object, this string
      should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2].
      For example, if the object reference is to a container within a pod, this would
      take on a value like: "spec.containers{name}" (where "name" refers to the name
      of the container that triggered the event) or if no container name is specified
      "spec.containers[2]" (container with index 2 in this pod). This syntax is chosen
      only to have some well-defined way of referencing a part of an object.'
    aliases:
    - output_to_field_path
  spec_output_to_kind:
    description:
    - Kind of the referent.
    aliases:
    - output_to_kind
  spec_output_to_name:
    description:
    - Name of the referent.
    aliases:
    - output_to_name
  spec_output_to_namespace:
    description:
    - Namespace of the referent.
    aliases:
    - output_to_namespace
  spec_output_to_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - output_to_resource_version
  spec_output_to_uid:
    description:
    - UID of the referent.
    aliases:
    - output_to_uid
  spec_post_commit_args:
    description:
    - args is a list of arguments that are provided to either Command, Script or the
      Docker image's default entrypoint. The arguments are placed immediately after
      the command to be run.
    aliases:
    - post_commit_args
    type: list
  spec_post_commit_command:
    description:
    - command is the command to run. It may not be specified with Script. This might
      be needed if the image doesn't have `/bin/sh`, or if you do not want to use
      a shell. In all other cases, using Script might be more convenient.
    aliases:
    - post_commit_command
    type: list
  spec_post_commit_script:
    description:
    - script is a shell script to be run with `/bin/sh -ic`. It may not be specified
      with Command. Use Script when a shell script is appropriate to execute the post
      build hook, for example for running unit tests with `rake test`. If you need
      control over the image entrypoint, or if the image does not have `/bin/sh`,
      use Command and/or Args. The `-i` flag is needed to support CentOS and RHEL
      images that use Software Collections (SCL), in order to have the appropriate
      collections enabled in the shell. E.g., in the Ruby image, this is necessary
      to make `ruby`, `bundle` and other binaries available in the PATH.
    aliases:
    - post_commit_script
  spec_resources_limits:
    description:
    - Limits describes the maximum amount of compute resources allowed.
    aliases:
    - resources_limits
    type: dict
  spec_resources_requests:
    description:
    - Requests describes the minimum amount of compute resources required. If Requests
      is omitted for a container, it defaults to Limits if that is explicitly specified,
      otherwise to an implementation-defined value.
    aliases:
    - resources_requests
    type: dict
  spec_revision_git_author_email:
    description:
    - email of the source control user
    aliases:
    - revision_git_author_email
  spec_revision_git_author_name:
    description:
    - name of the source control user
    aliases:
    - revision_git_author_name
  spec_revision_git_commit:
    description:
    - commit is the commit hash identifying a specific commit
    aliases:
    - revision_git_commit
  spec_revision_git_committer_email:
    description:
    - email of the source control user
    aliases:
    - revision_git_committer_email
  spec_revision_git_committer_name:
    description:
    - name of the source control user
    aliases:
    - revision_git_committer_name
  spec_revision_git_message:
    description:
    - message is the description of a specific commit
    aliases:
    - revision_git_message
  spec_revision_type:
    description:
    - type of the build source, may be one of 'Source', 'Dockerfile', 'Binary', or
      'Images'
    aliases:
    - revision_type
  spec_service_account:
    description:
    - serviceAccount is the name of the ServiceAccount to use to run the pod created
      by this build. The pod will be allowed to use secrets referenced by the ServiceAccount
    aliases:
    - service_account
  spec_source_binary_as_file:
    description:
    - asFile indicates that the provided binary input should be considered a single
      file within the build input. For example, specifying "webapp.war" would place
      the provided binary as `/webapp.war` for the builder. If left empty, the Docker
      and Source build strategies assume this file is a zip, tar, or tar.gz file and
      extract it as the source. The custom strategy receives this binary as standard
      input. This filename may not contain slashes or be '..' or '.'.
    aliases:
    - source_binary_as_file
  spec_source_context_dir:
    description:
    - contextDir specifies the sub-directory where the source code for the application
      exists. This allows to have buildable sources in directory other than root of
      repository.
    aliases:
    - source_context_dir
  spec_source_dockerfile:
    description:
    - dockerfile is the raw contents of a Dockerfile which should be built. When this
      option is specified, the FROM may be modified based on your strategy base image
      and additional ENV stanzas from your strategy environment will be added after
      the FROM, but before the rest of your Dockerfile stanzas. The Dockerfile source
      type may be used with other options like git - in those cases the Git repo will
      have any innate Dockerfile replaced in the context dir.
    aliases:
    - source_dockerfile
  spec_source_git_http_proxy:
    description:
    - httpProxy is a proxy used to reach the git repository over http
    aliases:
    - source_git_http_proxy
  spec_source_git_https_proxy:
    description:
    - httpsProxy is a proxy used to reach the git repository over https
    aliases:
    - source_git_https_proxy
  spec_source_git_no_proxy:
    description:
    - noProxy is the list of domains for which the proxy should not be used
    aliases:
    - source_git_no_proxy
  spec_source_git_ref:
    description:
    - ref is the branch/tag/ref to build.
    aliases:
    - source_git_ref
  spec_source_git_uri:
    description:
    - uri points to the source that will be built. The structure of the source will
      depend on the type of build to run
    aliases:
    - source_git_uri
  spec_source_images:
    description:
    - images describes a set of images to be used to provide source for the build
    aliases:
    - source_images
    type: list
  spec_source_secrets:
    description:
    - secrets represents a list of secrets and their destinations that will be used
      only for the build.
    aliases:
    - source_secrets
    type: list
  spec_source_source_secret_name:
    description:
    - Name of the referent.
    aliases:
    - source_secret_name
  spec_source_type:
    description:
    - type of build input to accept
    aliases:
    - source_type
  spec_strategy_custom_strategy_build_api_version:
    description:
    - buildAPIVersion is the requested API version for the Build object serialized
      and passed to the custom builder
    aliases:
    - strategy_custom_strategy_build_api_version
  spec_strategy_custom_strategy_env:
    description:
    - env contains additional environment variables you want to pass into a builder
      container.
    aliases:
    - strategy_custom_strategy_env
    type: list
  spec_strategy_custom_strategy_expose_docker_socket:
    description:
    - exposeDockerSocket will allow running Docker commands (and build Docker images)
      from inside the Docker container.
    aliases:
    - strategy_custom_strategy_expose_docker_socket
    type: bool
  spec_strategy_custom_strategy_force_pull:
    description:
    - forcePull describes if the controller should configure the build pod to always
      pull the images for the builder or only pull if it is not present locally
    aliases:
    - strategy_custom_strategy_force_pull
    type: bool
  spec_strategy_custom_strategy_from_api_version:
    description:
    - API version of the referent.
    aliases:
    - strategy_custom_strategy_from_api_version
  spec_strategy_custom_strategy_from_field_path:
    description:
    - 'If referring to a piece of an object instead of an entire object, this string
      should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2].
      For example, if the object reference is to a container within a pod, this would
      take on a value like: "spec.containers{name}" (where "name" refers to the name
      of the container that triggered the event) or if no container name is specified
      "spec.containers[2]" (container with index 2 in this pod). This syntax is chosen
      only to have some well-defined way of referencing a part of an object.'
    aliases:
    - strategy_custom_strategy_from_field_path
  spec_strategy_custom_strategy_from_kind:
    description:
    - Kind of the referent.
    aliases:
    - strategy_custom_strategy_from_kind
  spec_strategy_custom_strategy_from_name:
    description:
    - Name of the referent.
    aliases:
    - strategy_custom_strategy_from_name
  spec_strategy_custom_strategy_from_namespace:
    description:
    - Namespace of the referent.
    aliases:
    - strategy_custom_strategy_from_namespace
  spec_strategy_custom_strategy_from_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - strategy_custom_strategy_from_resource_version
  spec_strategy_custom_strategy_from_uid:
    description:
    - UID of the referent.
    aliases:
    - strategy_custom_strategy_from_uid
  spec_strategy_custom_strategy_pull_secret_name:
    description:
    - Name of the referent.
    aliases:
    - strategy_custom_strategy_pull_secret_name
  spec_strategy_custom_strategy_secrets:
    description:
    - secrets is a list of additional secrets that will be included in the build pod
    aliases:
    - strategy_custom_strategy_secrets
    type: list
  spec_strategy_docker_strategy_build_args:
    description:
    - buildArgs contains build arguments that will be resolved in the Dockerfile.
      See
    aliases:
    - strategy_docker_strategy_build_args
    type: list
  spec_strategy_docker_strategy_dockerfile_path:
    description:
    - dockerfilePath is the path of the Dockerfile that will be used to build the
      Docker image, relative to the root of the context (contextDir).
    aliases:
    - strategy_docker_strategy_dockerfile_path
  spec_strategy_docker_strategy_env:
    description:
    - env contains additional environment variables you want to pass into a builder
      container.
    aliases:
    - strategy_docker_strategy_env
    type: list
  spec_strategy_docker_strategy_force_pull:
    description:
    - forcePull describes if the builder should pull the images from registry prior
      to building.
    aliases:
    - strategy_docker_strategy_force_pull
    type: bool
  spec_strategy_docker_strategy_from_api_version:
    description:
    - API version of the referent.
    aliases:
    - strategy_docker_strategy_from_api_version
  spec_strategy_docker_strategy_from_field_path:
    description:
    - 'If referring to a piece of an object instead of an entire object, this string
      should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2].
      For example, if the object reference is to a container within a pod, this would
      take on a value like: "spec.containers{name}" (where "name" refers to the name
      of the container that triggered the event) or if no container name is specified
      "spec.containers[2]" (container with index 2 in this pod). This syntax is chosen
      only to have some well-defined way of referencing a part of an object.'
    aliases:
    - strategy_docker_strategy_from_field_path
  spec_strategy_docker_strategy_from_kind:
    description:
    - Kind of the referent.
    aliases:
    - strategy_docker_strategy_from_kind
  spec_strategy_docker_strategy_from_name:
    description:
    - Name of the referent.
    aliases:
    - strategy_docker_strategy_from_name
  spec_strategy_docker_strategy_from_namespace:
    description:
    - Namespace of the referent.
    aliases:
    - strategy_docker_strategy_from_namespace
  spec_strategy_docker_strategy_from_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - strategy_docker_strategy_from_resource_version
  spec_strategy_docker_strategy_from_uid:
    description:
    - UID of the referent.
    aliases:
    - strategy_docker_strategy_from_uid
  spec_strategy_docker_strategy_image_optimization_policy:
    description:
    - imageOptimizationPolicy describes what optimizations the system can use when
      building images to reduce the final size or time spent building the image. The
      default policy is 'None' which means the final build image will be equivalent
      to an image created by the Docker build API. The experimental policy 'SkipLayers'
      will avoid commiting new layers in between each image step, and will fail if
      the Dockerfile cannot provide compatibility with the 'None' policy. An additional
      experimental policy 'SkipLayersAndWarn' is the same as 'SkipLayers' but simply
      warns if compatibility cannot be preserved.
    aliases:
    - strategy_docker_strategy_image_optimization_policy
  spec_strategy_docker_strategy_no_cache:
    description:
    - noCache if set to true indicates that the docker build must be executed with
      the --no-cache=true flag
    aliases:
    - strategy_docker_strategy_no_cache
    type: bool
  spec_strategy_docker_strategy_pull_secret_name:
    description:
    - Name of the referent.
    aliases:
    - strategy_docker_strategy_pull_secret_name
  spec_strategy_jenkins_pipeline_strategy_env:
    description:
    - env contains additional environment variables you want to pass into a build
      pipeline.
    aliases:
    - strategy_jenkins_pipeline_strategy_env
    type: list
  spec_strategy_jenkins_pipeline_strategy_jenkinsfile:
    description:
    - Jenkinsfile defines the optional raw contents of a Jenkinsfile which defines
      a Jenkins pipeline build.
    aliases:
    - strategy_jenkins_pipeline_strategy_jenkinsfile
  spec_strategy_jenkins_pipeline_strategy_jenkinsfile_path:
    description:
    - JenkinsfilePath is the optional path of the Jenkinsfile that will be used to
      configure the pipeline relative to the root of the context (contextDir). If
      both JenkinsfilePath & Jenkinsfile are both not specified, this defaults to
      Jenkinsfile in the root of the specified contextDir.
    aliases:
    - strategy_jenkins_pipeline_strategy_jenkinsfile_path
  spec_strategy_source_strategy_env:
    description:
    - env contains additional environment variables you want to pass into a builder
      container.
    aliases:
    - strategy_source_strategy_env
    type: list
  spec_strategy_source_strategy_force_pull:
    description:
    - forcePull describes if the builder should pull the images from registry prior
      to building.
    aliases:
    - strategy_source_strategy_force_pull
    type: bool
  spec_strategy_source_strategy_from_api_version:
    description:
    - API version of the referent.
    aliases:
    - strategy_source_strategy_from_api_version
  spec_strategy_source_strategy_from_field_path:
    description:
    - 'If referring to a piece of an object instead of an entire object, this string
      should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2].
      For example, if the object reference is to a container within a pod, this would
      take on a value like: "spec.containers{name}" (where "name" refers to the name
      of the container that triggered the event) or if no container name is specified
      "spec.containers[2]" (container with index 2 in this pod). This syntax is chosen
      only to have some well-defined way of referencing a part of an object.'
    aliases:
    - strategy_source_strategy_from_field_path
  spec_strategy_source_strategy_from_kind:
    description:
    - Kind of the referent.
    aliases:
    - strategy_source_strategy_from_kind
  spec_strategy_source_strategy_from_name:
    description:
    - Name of the referent.
    aliases:
    - strategy_source_strategy_from_name
  spec_strategy_source_strategy_from_namespace:
    description:
    - Namespace of the referent.
    aliases:
    - strategy_source_strategy_from_namespace
  spec_strategy_source_strategy_from_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - strategy_source_strategy_from_resource_version
  spec_strategy_source_strategy_from_uid:
    description:
    - UID of the referent.
    aliases:
    - strategy_source_strategy_from_uid
  spec_strategy_source_strategy_incremental:
    description:
    - incremental flag forces the Source build to do incremental builds if true.
    aliases:
    - strategy_source_strategy_incremental
    type: bool
  spec_strategy_source_strategy_pull_secret_name:
    description:
    - Name of the referent.
    aliases:
    - strategy_source_strategy_pull_secret_name
  spec_strategy_source_strategy_scripts:
    description:
    - scripts is the location of Source scripts
    aliases:
    - strategy_source_strategy_scripts
  spec_strategy_type:
    description:
    - type is the kind of build strategy.
    aliases:
    - strategy_type
  spec_triggered_by:
    description:
    - triggeredBy describes which triggers started the most recent update to the build
      configuration and contains information about those triggers.
    aliases:
    - triggered_by
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
build:
  type: complex
  returned: when I(state) = C(present)
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
      - spec is all the inputs used to execute the build.
      type: complex
    status:
      description:
      - status is the current status of the build.
      type: complex
'''


def main():
    try:
        module = OpenShiftAnsibleModule('build', 'v1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
