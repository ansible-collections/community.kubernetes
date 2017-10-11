#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.openshift_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: openshift_v1_build_config
short_description: OpenShift BuildConfig
description:
- Manage the lifecycle of a build_config object. Supports check mode, and attempts
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
  spec_failed_builds_history_limit:
    description:
    - failedBuildsHistoryLimit is the number of old failed builds to retain. If not
      specified, all failed builds are retained.
    aliases:
    - failed_builds_history_limit
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
  spec_run_policy:
    description:
    - RunPolicy describes how the new build created from this build configuration
      will be scheduled for execution. This is optional, if not specified we default
      to "Serial".
    aliases:
    - run_policy
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
  spec_strategy_custom_strategy__from_api_version:
    description:
    - API version of the referent.
    aliases:
    - strategy_custom_strategy__from_api_version
  spec_strategy_custom_strategy__from_field_path:
    description:
    - 'If referring to a piece of an object instead of an entire object, this string
      should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2].
      For example, if the object reference is to a container within a pod, this would
      take on a value like: "spec.containers{name}" (where "name" refers to the name
      of the container that triggered the event) or if no container name is specified
      "spec.containers[2]" (container with index 2 in this pod). This syntax is chosen
      only to have some well-defined way of referencing a part of an object.'
    aliases:
    - strategy_custom_strategy__from_field_path
  spec_strategy_custom_strategy__from_kind:
    description:
    - Kind of the referent.
    aliases:
    - strategy_custom_strategy__from_kind
  spec_strategy_custom_strategy__from_name:
    description:
    - Name of the referent.
    aliases:
    - strategy_custom_strategy__from_name
  spec_strategy_custom_strategy__from_namespace:
    description:
    - Namespace of the referent.
    aliases:
    - strategy_custom_strategy__from_namespace
  spec_strategy_custom_strategy__from_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - strategy_custom_strategy__from_resource_version
  spec_strategy_custom_strategy__from_uid:
    description:
    - UID of the referent.
    aliases:
    - strategy_custom_strategy__from_uid
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
  spec_strategy_docker_strategy__from_api_version:
    description:
    - API version of the referent.
    aliases:
    - strategy_docker_strategy__from_api_version
  spec_strategy_docker_strategy__from_field_path:
    description:
    - 'If referring to a piece of an object instead of an entire object, this string
      should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2].
      For example, if the object reference is to a container within a pod, this would
      take on a value like: "spec.containers{name}" (where "name" refers to the name
      of the container that triggered the event) or if no container name is specified
      "spec.containers[2]" (container with index 2 in this pod). This syntax is chosen
      only to have some well-defined way of referencing a part of an object.'
    aliases:
    - strategy_docker_strategy__from_field_path
  spec_strategy_docker_strategy__from_kind:
    description:
    - Kind of the referent.
    aliases:
    - strategy_docker_strategy__from_kind
  spec_strategy_docker_strategy__from_name:
    description:
    - Name of the referent.
    aliases:
    - strategy_docker_strategy__from_name
  spec_strategy_docker_strategy__from_namespace:
    description:
    - Namespace of the referent.
    aliases:
    - strategy_docker_strategy__from_namespace
  spec_strategy_docker_strategy__from_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - strategy_docker_strategy__from_resource_version
  spec_strategy_docker_strategy__from_uid:
    description:
    - UID of the referent.
    aliases:
    - strategy_docker_strategy__from_uid
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
  spec_strategy_source_strategy__from_api_version:
    description:
    - API version of the referent.
    aliases:
    - strategy_source_strategy__from_api_version
  spec_strategy_source_strategy__from_field_path:
    description:
    - 'If referring to a piece of an object instead of an entire object, this string
      should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2].
      For example, if the object reference is to a container within a pod, this would
      take on a value like: "spec.containers{name}" (where "name" refers to the name
      of the container that triggered the event) or if no container name is specified
      "spec.containers[2]" (container with index 2 in this pod). This syntax is chosen
      only to have some well-defined way of referencing a part of an object.'
    aliases:
    - strategy_source_strategy__from_field_path
  spec_strategy_source_strategy__from_kind:
    description:
    - Kind of the referent.
    aliases:
    - strategy_source_strategy__from_kind
  spec_strategy_source_strategy__from_name:
    description:
    - Name of the referent.
    aliases:
    - strategy_source_strategy__from_name
  spec_strategy_source_strategy__from_namespace:
    description:
    - Namespace of the referent.
    aliases:
    - strategy_source_strategy__from_namespace
  spec_strategy_source_strategy__from_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - strategy_source_strategy__from_resource_version
  spec_strategy_source_strategy__from_uid:
    description:
    - UID of the referent.
    aliases:
    - strategy_source_strategy__from_uid
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
  spec_strategy_source_strategy_runtime_artifacts:
    description:
    - 'runtimeArtifacts specifies a list of source/destination pairs that will be
      copied from the builder to the runtime image. sourcePath can be a file or directory.
      destinationDir must be a directory. destinationDir can also be empty or equal
      to ".", in this case it just refers to the root of WORKDIR. Deprecated: This
      feature will be removed in a future release. Use ImageSource to copy binary
      artifacts created from one build into a separate runtime image.'
    aliases:
    - strategy_source_strategy_runtime_artifacts
    type: list
  spec_strategy_source_strategy_runtime_image_api_version:
    description:
    - API version of the referent.
    aliases:
    - strategy_source_strategy_runtime_image_api_version
  spec_strategy_source_strategy_runtime_image_field_path:
    description:
    - 'If referring to a piece of an object instead of an entire object, this string
      should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2].
      For example, if the object reference is to a container within a pod, this would
      take on a value like: "spec.containers{name}" (where "name" refers to the name
      of the container that triggered the event) or if no container name is specified
      "spec.containers[2]" (container with index 2 in this pod). This syntax is chosen
      only to have some well-defined way of referencing a part of an object.'
    aliases:
    - strategy_source_strategy_runtime_image_field_path
  spec_strategy_source_strategy_runtime_image_kind:
    description:
    - Kind of the referent.
    aliases:
    - strategy_source_strategy_runtime_image_kind
  spec_strategy_source_strategy_runtime_image_name:
    description:
    - Name of the referent.
    aliases:
    - strategy_source_strategy_runtime_image_name
  spec_strategy_source_strategy_runtime_image_namespace:
    description:
    - Namespace of the referent.
    aliases:
    - strategy_source_strategy_runtime_image_namespace
  spec_strategy_source_strategy_runtime_image_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - strategy_source_strategy_runtime_image_resource_version
  spec_strategy_source_strategy_runtime_image_uid:
    description:
    - UID of the referent.
    aliases:
    - strategy_source_strategy_runtime_image_uid
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
  spec_successful_builds_history_limit:
    description:
    - successfulBuildsHistoryLimit is the number of old successful builds to retain.
      If not specified, all successful builds are retained.
    aliases:
    - successful_builds_history_limit
    type: int
  spec_triggers:
    description:
    - triggers determine how new Builds can be launched from a BuildConfig. If no
      triggers are defined, a new build can only occur as a result of an explicit
      client build creation.
    aliases:
    - triggers
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
- openshift == 0.3.3
'''

EXAMPLES = '''
'''

RETURN = '''
api_version:
  type: string
  description: Requested API version
build_config:
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
      - metadata for BuildConfig.
      type: complex
      contains:
        annotations:
          description:
          - Annotations is an unstructured key value map stored with a resource that
            may be set by external tools to store and retrieve arbitrary metadata.
            They are not queryable and should be preserved when modifying objects.
          type: complex
          contains: str, str
        cluster_name:
          description:
          - The name of the cluster which the object belongs to. This is used to distinguish
            resources with same name and namespace in different clusters. This field
            is not set anywhere right now and apiserver is going to ignore it if set
            in create or update request.
          type: str
        creation_timestamp:
          description:
          - CreationTimestamp is a timestamp representing the server time when this
            object was created. It is not guaranteed to be set in happens-before order
            across separate operations. Clients may not set this value. It is represented
            in RFC3339 form and is in UTC. Populated by the system. Read-only. Null
            for lists.
          type: complex
          contains: {}
        deletion_grace_period_seconds:
          description:
          - Number of seconds allowed for this object to gracefully terminate before
            it will be removed from the system. Only set when deletionTimestamp is
            also set. May only be shortened. Read-only.
          type: int
        deletion_timestamp:
          description:
          - DeletionTimestamp is RFC 3339 date and time at which this resource will
            be deleted. This field is set by the server when a graceful deletion is
            requested by the user, and is not directly settable by a client. The resource
            is expected to be deleted (no longer visible from resource lists, and
            not reachable by name) after the time in this field. Once set, this value
            may not be unset or be set further into the future, although it may be
            shortened or the resource may be deleted prior to this time. For example,
            a user may request that a pod is deleted in 30 seconds. The Kubelet will
            react by sending a graceful termination signal to the containers in the
            pod. After that 30 seconds, the Kubelet will send a hard termination signal
            (SIGKILL) to the container and after cleanup, remove the pod from the
            API. In the presence of network partitions, this object may still exist
            after this timestamp, until an administrator or automated process can
            determine the resource is fully terminated. If not set, graceful deletion
            of the object has not been requested. Populated by the system when a graceful
            deletion is requested. Read-only.
          type: complex
          contains: {}
        finalizers:
          description:
          - Must be empty before the object is deleted from the registry. Each entry
            is an identifier for the responsible component that will remove the entry
            from the list. If the deletionTimestamp of the object is non-nil, entries
            in this list can only be removed.
          type: list
          contains: str
        generate_name:
          description:
          - GenerateName is an optional prefix, used by the server, to generate a
            unique name ONLY IF the Name field has not been provided. If this field
            is used, the name returned to the client will be different than the name
            passed. This value will also be combined with a unique suffix. The provided
            value has the same validation rules as the Name field, and may be truncated
            by the length of the suffix required to make the value unique on the server.
            If this field is specified and the generated name exists, the server will
            NOT return a 409 - instead, it will either return 201 Created or 500 with
            Reason ServerTimeout indicating a unique name could not be found in the
            time allotted, and the client should retry (optionally after the time
            indicated in the Retry-After header). Applied only if Name is not specified.
          type: str
        generation:
          description:
          - A sequence number representing a specific generation of the desired state.
            Populated by the system. Read-only.
          type: int
        initializers:
          description:
          - An initializer is a controller which enforces some system invariant at
            object creation time. This field is a list of initializers that have not
            yet acted on this object. If nil or empty, this object has been completely
            initialized. Otherwise, the object is considered uninitialized and is
            hidden (in list/watch and get calls) from clients that haven't explicitly
            asked to observe uninitialized objects. When an object is created, the
            system will populate this list with the current set of initializers. Only
            privileged users may set or modify this list. Once it is empty, it may
            not be modified further by any user.
          type: complex
          contains:
            pending:
              description:
              - Pending is a list of initializers that must execute in order before
                this object is visible. When the last pending initializer is removed,
                and no failing result is set, the initializers struct will be set
                to nil and the object is considered as initialized and visible to
                all clients.
              type: list
              contains:
                name:
                  description:
                  - name of the process that is responsible for initializing this
                    object.
                  type: str
            result:
              description:
              - If result is set with the Failure field, the object will be persisted
                to storage and then deleted, ensuring that other clients can observe
                the deletion.
              type: complex
              contains:
                api_version:
                  description:
                  - APIVersion defines the versioned schema of this representation
                    of an object. Servers should convert recognized schemas to the
                    latest internal value, and may reject unrecognized values.
                  type: str
                code:
                  description:
                  - Suggested HTTP return code for this status, 0 if not set.
                  type: int
                details:
                  description:
                  - Extended data associated with the reason. Each reason may define
                    its own extended details. This field is optional and the data
                    returned is not guaranteed to conform to any schema except that
                    defined by the reason type.
                  type: complex
                  contains:
                    causes:
                      description:
                      - The Causes array includes more details associated with the
                        StatusReason failure. Not all StatusReasons may provide detailed
                        causes.
                      type: list
                      contains:
                        field:
                          description:
                          - 'The field of the resource that has caused this error,
                            as named by its JSON serialization. May include dot and
                            postfix notation for nested attributes. Arrays are zero-indexed.
                            Fields may appear more than once in an array of causes
                            due to fields having multiple errors. Optional. Examples:
                            "name" - the field "name" on the current resource "items[0].name"
                            - the field "name" on the first array entry in "items"'
                          type: str
                        message:
                          description:
                          - A human-readable description of the cause of the error.
                            This field may be presented as-is to a reader.
                          type: str
                        reason:
                          description:
                          - A machine-readable description of the cause of the error.
                            If this value is empty there is no information available.
                          type: str
                    group:
                      description:
                      - The group attribute of the resource associated with the status
                        StatusReason.
                      type: str
                    kind:
                      description:
                      - The kind attribute of the resource associated with the status
                        StatusReason. On some operations may differ from the requested
                        resource Kind.
                      type: str
                    name:
                      description:
                      - The name attribute of the resource associated with the status
                        StatusReason (when there is a single name which can be described).
                      type: str
                    retry_after_seconds:
                      description:
                      - If specified, the time in seconds before the operation should
                        be retried.
                      type: int
                    uid:
                      description:
                      - UID of the resource. (when there is a single resource which
                        can be described).
                      type: str
                kind:
                  description:
                  - Kind is a string value representing the REST resource this object
                    represents. Servers may infer this from the endpoint the client
                    submits requests to. Cannot be updated. In CamelCase.
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
                      - String that identifies the server's internal version of this
                        object that can be used by clients to determine when objects
                        have changed. Value must be treated as opaque by clients and
                        passed unmodified back to the server. Populated by the system.
                        Read-only.
                      type: str
                    self_link:
                      description:
                      - SelfLink is a URL representing this object. Populated by the
                        system. Read-only.
                      type: str
                reason:
                  description:
                  - A machine-readable description of why this operation is in the
                    "Failure" status. If this value is empty there is no information
                    available. A Reason clarifies an HTTP status code but does not
                    override it.
                  type: str
                status:
                  description:
                  - 'Status of the operation. One of: "Success" or "Failure".'
                  type: str
        labels:
          description:
          - Map of string keys and values that can be used to organize and categorize
            (scope and select) objects. May match selectors of replication controllers
            and services.
          type: complex
          contains: str, str
        name:
          description:
          - Name must be unique within a namespace. Is required when creating resources,
            although some resources may allow a client to request the generation of
            an appropriate name automatically. Name is primarily intended for creation
            idempotence and configuration definition. Cannot be updated.
          type: str
        namespace:
          description:
          - Namespace defines the space within each name must be unique. An empty
            namespace is equivalent to the "default" namespace, but "default" is the
            canonical representation. Not all objects are required to be scoped to
            a namespace - the value of this field for those objects will be empty.
            Must be a DNS_LABEL. Cannot be updated.
          type: str
        owner_references:
          description:
          - List of objects depended by this object. If ALL objects in the list have
            been deleted, this object will be garbage collected. If this object is
            managed by a controller, then an entry in this list will point to this
            controller, with the controller field set to true. There cannot be more
            than one managing controller.
          type: list
          contains:
            api_version:
              description:
              - API version of the referent.
              type: str
            block_owner_deletion:
              description:
              - If true, AND if the owner has the "foregroundDeletion" finalizer,
                then the owner cannot be deleted from the key-value store until this
                reference is removed. Defaults to false. To set this field, a user
                needs "delete" permission of the owner, otherwise 422 (Unprocessable
                Entity) will be returned.
              type: bool
            controller:
              description:
              - If true, this reference points to the managing controller.
              type: bool
            kind:
              description:
              - Kind of the referent.
              type: str
            name:
              description:
              - Name of the referent.
              type: str
            uid:
              description:
              - UID of the referent.
              type: str
        resource_version:
          description:
          - An opaque value that represents the internal version of this object that
            can be used by clients to determine when objects have changed. May be
            used for optimistic concurrency, change detection, and the watch operation
            on a resource or set of resources. Clients must treat these values as
            opaque and passed unmodified back to the server. They may only be valid
            for a particular resource or set of resources. Populated by the system.
            Read-only. Value must be treated as opaque by clients and .
          type: str
        self_link:
          description:
          - SelfLink is a URL representing this object. Populated by the system. Read-only.
          type: str
        uid:
          description:
          - UID is the unique in time and space value for this object. It is typically
            generated by the server on successful creation of a resource and is not
            allowed to change on PUT operations. Populated by the system. Read-only.
          type: str
    spec:
      description:
      - spec holds all the input necessary to produce a new build, and the conditions
        when to trigger them.
      type: complex
      contains:
        completion_deadline_seconds:
          description:
          - completionDeadlineSeconds is an optional duration in seconds, counted
            from the time when a build pod gets scheduled in the system, that the
            build may be active on a node before the system actively tries to terminate
            the build; value must be positive integer
          type: int
        failed_builds_history_limit:
          description:
          - failedBuildsHistoryLimit is the number of old failed builds to retain.
            If not specified, all failed builds are retained.
          type: int
        node_selector:
          description:
          - nodeSelector is a selector which must be true for the build pod to fit
            on a node If nil, it can be overridden by default build nodeselector values
            for the cluster. If set to an empty map or a map with any values, default
            build nodeselector values are ignored.
          type: complex
          contains: str, str
        output:
          description:
          - output describes the Docker image the Strategy should produce.
          type: complex
          contains:
            image_labels:
              description:
              - imageLabels define a list of labels that are applied to the resulting
                image. If there are multiple labels with the same name then the last
                one in the list is used.
              type: list
              contains:
                name:
                  description:
                  - name defines the name of the label. It must have non-zero length.
                  type: str
                value:
                  description:
                  - value defines the literal value of the label.
                  type: str
            push_secret:
              description:
              - PushSecret is the name of a Secret that would be used for setting
                up the authentication for executing the Docker push to authentication
                enabled Docker Registry (or Docker Hub).
              type: complex
              contains:
                name:
                  description:
                  - Name of the referent.
                  type: str
            to:
              description:
              - to defines an optional location to push the output of this build to.
                Kind must be one of 'ImageStreamTag' or 'DockerImage'. This value
                will be used to look up a Docker image repository to push to. In the
                case of an ImageStreamTag, the ImageStreamTag will be looked for in
                the namespace of the build unless Namespace is specified.
              type: complex
              contains:
                api_version:
                  description:
                  - API version of the referent.
                  type: str
                field_path:
                  description:
                  - 'If referring to a piece of an object instead of an entire object,
                    this string should contain a valid JSON/Go field access statement,
                    such as desiredState.manifest.containers[2]. For example, if the
                    object reference is to a container within a pod, this would take
                    on a value like: "spec.containers{name}" (where "name" refers
                    to the name of the container that triggered the event) or if no
                    container name is specified "spec.containers[2]" (container with
                    index 2 in this pod). This syntax is chosen only to have some
                    well-defined way of referencing a part of an object.'
                  type: str
                kind:
                  description:
                  - Kind of the referent.
                  type: str
                name:
                  description:
                  - Name of the referent.
                  type: str
                namespace:
                  description:
                  - Namespace of the referent.
                  type: str
                resource_version:
                  description:
                  - Specific resourceVersion to which this reference is made, if any.
                  type: str
                uid:
                  description:
                  - UID of the referent.
                  type: str
        post_commit:
          description:
          - postCommit is a build hook executed after the build output image is committed,
            before it is pushed to a registry.
          type: complex
          contains:
            args:
              description:
              - args is a list of arguments that are provided to either Command, Script
                or the Docker image's default entrypoint. The arguments are placed
                immediately after the command to be run.
              type: list
              contains: str
            command:
              description:
              - command is the command to run. It may not be specified with Script.
                This might be needed if the image doesn't have `/bin/sh`, or if you
                do not want to use a shell. In all other cases, using Script might
                be more convenient.
              type: list
              contains: str
            script:
              description:
              - script is a shell script to be run with `/bin/sh -ic`. It may not
                be specified with Command. Use Script when a shell script is appropriate
                to execute the post build hook, for example for running unit tests
                with `rake test`. If you need control over the image entrypoint, or
                if the image does not have `/bin/sh`, use Command and/or Args. The
                `-i` flag is needed to support CentOS and RHEL images that use Software
                Collections (SCL), in order to have the appropriate collections enabled
                in the shell. E.g., in the Ruby image, this is necessary to make `ruby`,
                `bundle` and other binaries available in the PATH.
              type: str
        resources:
          description:
          - resources computes resource requirements to execute the build.
          type: complex
          contains:
            limits:
              description:
              - Limits describes the maximum amount of compute resources allowed.
              type: complex
              contains: str, str
            requests:
              description:
              - Requests describes the minimum amount of compute resources required.
                If Requests is omitted for a container, it defaults to Limits if that
                is explicitly specified, otherwise to an implementation-defined value.
              type: complex
              contains: str, str
        revision:
          description:
          - revision is the information from the source for a specific repo snapshot.
            This is optional.
          type: complex
          contains:
            git:
              description:
              - Git contains information about git-based build source
              type: complex
              contains:
                author:
                  description:
                  - author is the author of a specific commit
                  type: complex
                  contains:
                    email:
                      description:
                      - email of the source control user
                      type: str
                    name:
                      description:
                      - name of the source control user
                      type: str
                commit:
                  description:
                  - commit is the commit hash identifying a specific commit
                  type: str
                committer:
                  description:
                  - committer is the committer of a specific commit
                  type: complex
                  contains:
                    email:
                      description:
                      - email of the source control user
                      type: str
                    name:
                      description:
                      - name of the source control user
                      type: str
                message:
                  description:
                  - message is the description of a specific commit
                  type: str
            type:
              description:
              - type of the build source, may be one of 'Source', 'Dockerfile', 'Binary',
                or 'Images'
              type: str
        run_policy:
          description:
          - RunPolicy describes how the new build created from this build configuration
            will be scheduled for execution. This is optional, if not specified we
            default to "Serial".
          type: str
        service_account:
          description:
          - serviceAccount is the name of the ServiceAccount to use to run the pod
            created by this build. The pod will be allowed to use secrets referenced
            by the ServiceAccount
          type: str
        source:
          description:
          - source describes the SCM in use.
          type: complex
          contains:
            binary:
              description:
              - binary builds accept a binary as their input. The binary is generally
                assumed to be a tar, gzipped tar, or zip file depending on the strategy.
                For Docker builds, this is the build context and an optional Dockerfile
                may be specified to override any Dockerfile in the build context.
                For Source builds, this is assumed to be an archive as described above.
                For Source and Docker builds, if binary.asFile is set the build will
                receive a directory with a single file. contextDir may be used when
                an archive is provided. Custom builds will receive this binary as
                input on STDIN.
              type: complex
              contains:
                as_file:
                  description:
                  - asFile indicates that the provided binary input should be considered
                    a single file within the build input. For example, specifying
                    "webapp.war" would place the provided binary as `/webapp.war`
                    for the builder. If left empty, the Docker and Source build strategies
                    assume this file is a zip, tar, or tar.gz file and extract it
                    as the source. The custom strategy receives this binary as standard
                    input. This filename may not contain slashes or be '..' or '.'.
                  type: str
            context_dir:
              description:
              - contextDir specifies the sub-directory where the source code for the
                application exists. This allows to have buildable sources in directory
                other than root of repository.
              type: str
            dockerfile:
              description:
              - dockerfile is the raw contents of a Dockerfile which should be built.
                When this option is specified, the FROM may be modified based on your
                strategy base image and additional ENV stanzas from your strategy
                environment will be added after the FROM, but before the rest of your
                Dockerfile stanzas. The Dockerfile source type may be used with other
                options like git - in those cases the Git repo will have any innate
                Dockerfile replaced in the context dir.
              type: str
            git:
              description:
              - git contains optional information about git build source
              type: complex
              contains:
                http_proxy:
                  description:
                  - httpProxy is a proxy used to reach the git repository over http
                  type: str
                https_proxy:
                  description:
                  - httpsProxy is a proxy used to reach the git repository over https
                  type: str
                no_proxy:
                  description:
                  - noProxy is the list of domains for which the proxy should not
                    be used
                  type: str
                ref:
                  description:
                  - ref is the branch/tag/ref to build.
                  type: str
                uri:
                  description:
                  - uri points to the source that will be built. The structure of
                    the source will depend on the type of build to run
                  type: str
            images:
              description:
              - images describes a set of images to be used to provide source for
                the build
              type: list
              contains:
                _from:
                  description:
                  - from is a reference to an ImageStreamTag, ImageStreamImage, or
                    DockerImage to copy source from.
                  type: complex
                  contains:
                    api_version:
                      description:
                      - API version of the referent.
                      type: str
                    field_path:
                      description:
                      - 'If referring to a piece of an object instead of an entire
                        object, this string should contain a valid JSON/Go field access
                        statement, such as desiredState.manifest.containers[2]. For
                        example, if the object reference is to a container within
                        a pod, this would take on a value like: "spec.containers{name}"
                        (where "name" refers to the name of the container that triggered
                        the event) or if no container name is specified "spec.containers[2]"
                        (container with index 2 in this pod). This syntax is chosen
                        only to have some well-defined way of referencing a part of
                        an object.'
                      type: str
                    kind:
                      description:
                      - Kind of the referent.
                      type: str
                    name:
                      description:
                      - Name of the referent.
                      type: str
                    namespace:
                      description:
                      - Namespace of the referent.
                      type: str
                    resource_version:
                      description:
                      - Specific resourceVersion to which this reference is made,
                        if any.
                      type: str
                    uid:
                      description:
                      - UID of the referent.
                      type: str
                paths:
                  description:
                  - paths is a list of source and destination paths to copy from the
                    image.
                  type: list
                  contains:
                    destination_dir:
                      description:
                      - destinationDir is the relative directory within the build
                        directory where files copied from the image are placed.
                      type: str
                    source_path:
                      description:
                      - sourcePath is the absolute path of the file or directory inside
                        the image to copy to the build directory. If the source path
                        ends in /. then the content of the directory will be copied,
                        but the directory itself will not be created at the destination.
                      type: str
                pull_secret:
                  description:
                  - pullSecret is a reference to a secret to be used to pull the image
                    from a registry If the image is pulled from the OpenShift registry,
                    this field does not need to be set.
                  type: complex
                  contains:
                    name:
                      description:
                      - Name of the referent.
                      type: str
            secrets:
              description:
              - secrets represents a list of secrets and their destinations that will
                be used only for the build.
              type: list
              contains:
                destination_dir:
                  description:
                  - destinationDir is the directory where the files from the secret
                    should be available for the build time. For the Source build strategy,
                    these will be injected into a container where the assemble script
                    runs. Later, when the script finishes, all files injected will
                    be truncated to zero length. For the Docker build strategy, these
                    will be copied into the build directory, where the Dockerfile
                    is located, so users can ADD or COPY them during docker build.
                  type: str
                secret:
                  description:
                  - secret is a reference to an existing secret that you want to use
                    in your build.
                  type: complex
                  contains:
                    name:
                      description:
                      - Name of the referent.
                      type: str
            source_secret:
              description:
              - "sourceSecret is the name of a Secret that would be used for setting\
                \ up the authentication for cloning private repository. The secret\
                \ contains valid credentials for remote repository, where the data's\
                \ key represent the authentication method to be used and value is\
                \ the base64 encoded credentials. Supported auth methods are: ssh-privatekey."
              type: complex
              contains:
                name:
                  description:
                  - Name of the referent.
                  type: str
            type:
              description:
              - type of build input to accept
              type: str
        strategy:
          description:
          - strategy defines how to perform a build.
          type: complex
          contains:
            custom_strategy:
              description:
              - customStrategy holds the parameters to the Custom build strategy
              type: complex
              contains:
                _from:
                  description:
                  - from is reference to an DockerImage, ImageStreamTag, or ImageStreamImage
                    from which the docker image should be pulled
                  type: complex
                  contains:
                    api_version:
                      description:
                      - API version of the referent.
                      type: str
                    field_path:
                      description:
                      - 'If referring to a piece of an object instead of an entire
                        object, this string should contain a valid JSON/Go field access
                        statement, such as desiredState.manifest.containers[2]. For
                        example, if the object reference is to a container within
                        a pod, this would take on a value like: "spec.containers{name}"
                        (where "name" refers to the name of the container that triggered
                        the event) or if no container name is specified "spec.containers[2]"
                        (container with index 2 in this pod). This syntax is chosen
                        only to have some well-defined way of referencing a part of
                        an object.'
                      type: str
                    kind:
                      description:
                      - Kind of the referent.
                      type: str
                    name:
                      description:
                      - Name of the referent.
                      type: str
                    namespace:
                      description:
                      - Namespace of the referent.
                      type: str
                    resource_version:
                      description:
                      - Specific resourceVersion to which this reference is made,
                        if any.
                      type: str
                    uid:
                      description:
                      - UID of the referent.
                      type: str
                build_api_version:
                  description:
                  - buildAPIVersion is the requested API version for the Build object
                    serialized and passed to the custom builder
                  type: str
                env:
                  description:
                  - env contains additional environment variables you want to pass
                    into a builder container.
                  type: list
                  contains:
                    name:
                      description:
                      - Name of the environment variable. Must be a C_IDENTIFIER.
                      type: str
                    value:
                      description:
                      - 'Variable references $(VAR_NAME) are expanded using the previous
                        defined environment variables in the container and any service
                        environment variables. If a variable cannot be resolved, the
                        reference in the input string will be unchanged. The $(VAR_NAME)
                        syntax can be escaped with a double $$, ie: $$(VAR_NAME).
                        Escaped references will never be expanded, regardless of whether
                        the variable exists or not. Defaults to "".'
                      type: str
                    value_from:
                      description:
                      - Source for the environment variable's value. Cannot be used
                        if value is not empty.
                      type: complex
                      contains:
                        config_map_key_ref:
                          description:
                          - Selects a key of a ConfigMap.
                          type: complex
                          contains:
                            key:
                              description:
                              - The key to select.
                              type: str
                            name:
                              description:
                              - Name of the referent.
                              type: str
                            optional:
                              description:
                              - Specify whether the ConfigMap or it's key must be
                                defined
                              type: bool
                        field_ref:
                          description:
                          - 'Selects a field of the pod: supports metadata.name, metadata.namespace,
                            metadata.labels, metadata.annotations, spec.nodeName,
                            spec.serviceAccountName, status.hostIP, status.podIP.'
                          type: complex
                          contains:
                            api_version:
                              description:
                              - Version of the schema the FieldPath is written in
                                terms of, defaults to "v1".
                              type: str
                            field_path:
                              description:
                              - Path of the field to select in the specified API version.
                              type: str
                        resource_field_ref:
                          description:
                          - 'Selects a resource of the container: only resources limits
                            and requests (limits.cpu, limits.memory, requests.cpu
                            and requests.memory) are currently supported.'
                          type: complex
                          contains:
                            container_name:
                              description:
                              - 'Container name: required for volumes, optional for
                                env vars'
                              type: str
                            divisor:
                              description:
                              - Specifies the output format of the exposed resources,
                                defaults to "1"
                              type: str
                            resource:
                              description:
                              - 'Required: resource to select'
                              type: str
                        secret_key_ref:
                          description:
                          - Selects a key of a secret in the pod's namespace
                          type: complex
                          contains:
                            key:
                              description:
                              - The key of the secret to select from. Must be a valid
                                secret key.
                              type: str
                            name:
                              description:
                              - Name of the referent.
                              type: str
                            optional:
                              description:
                              - Specify whether the Secret or it's key must be defined
                              type: bool
                expose_docker_socket:
                  description:
                  - exposeDockerSocket will allow running Docker commands (and build
                    Docker images) from inside the Docker container.
                  type: bool
                force_pull:
                  description:
                  - forcePull describes if the controller should configure the build
                    pod to always pull the images for the builder or only pull if
                    it is not present locally
                  type: bool
                pull_secret:
                  description:
                  - pullSecret is the name of a Secret that would be used for setting
                    up the authentication for pulling the Docker images from the private
                    Docker registries
                  type: complex
                  contains:
                    name:
                      description:
                      - Name of the referent.
                      type: str
                secrets:
                  description:
                  - secrets is a list of additional secrets that will be included
                    in the build pod
                  type: list
                  contains:
                    mount_path:
                      description:
                      - mountPath is the path at which to mount the secret
                      type: str
                    secret_source:
                      description:
                      - secretSource is a reference to the secret
                      type: complex
                      contains:
                        name:
                          description:
                          - Name of the referent.
                          type: str
            docker_strategy:
              description:
              - dockerStrategy holds the parameters to the Docker build strategy.
              type: complex
              contains:
                _from:
                  description:
                  - from is reference to an DockerImage, ImageStreamTag, or ImageStreamImage
                    from which the docker image should be pulled the resulting image
                    will be used in the FROM line of the Dockerfile for this build.
                  type: complex
                  contains:
                    api_version:
                      description:
                      - API version of the referent.
                      type: str
                    field_path:
                      description:
                      - 'If referring to a piece of an object instead of an entire
                        object, this string should contain a valid JSON/Go field access
                        statement, such as desiredState.manifest.containers[2]. For
                        example, if the object reference is to a container within
                        a pod, this would take on a value like: "spec.containers{name}"
                        (where "name" refers to the name of the container that triggered
                        the event) or if no container name is specified "spec.containers[2]"
                        (container with index 2 in this pod). This syntax is chosen
                        only to have some well-defined way of referencing a part of
                        an object.'
                      type: str
                    kind:
                      description:
                      - Kind of the referent.
                      type: str
                    name:
                      description:
                      - Name of the referent.
                      type: str
                    namespace:
                      description:
                      - Namespace of the referent.
                      type: str
                    resource_version:
                      description:
                      - Specific resourceVersion to which this reference is made,
                        if any.
                      type: str
                    uid:
                      description:
                      - UID of the referent.
                      type: str
                build_args:
                  description:
                  - buildArgs contains build arguments that will be resolved in the
                    Dockerfile. See
                  type: list
                  contains:
                    name:
                      description:
                      - Name of the environment variable. Must be a C_IDENTIFIER.
                      type: str
                    value:
                      description:
                      - 'Variable references $(VAR_NAME) are expanded using the previous
                        defined environment variables in the container and any service
                        environment variables. If a variable cannot be resolved, the
                        reference in the input string will be unchanged. The $(VAR_NAME)
                        syntax can be escaped with a double $$, ie: $$(VAR_NAME).
                        Escaped references will never be expanded, regardless of whether
                        the variable exists or not. Defaults to "".'
                      type: str
                    value_from:
                      description:
                      - Source for the environment variable's value. Cannot be used
                        if value is not empty.
                      type: complex
                      contains:
                        config_map_key_ref:
                          description:
                          - Selects a key of a ConfigMap.
                          type: complex
                          contains:
                            key:
                              description:
                              - The key to select.
                              type: str
                            name:
                              description:
                              - Name of the referent.
                              type: str
                            optional:
                              description:
                              - Specify whether the ConfigMap or it's key must be
                                defined
                              type: bool
                        field_ref:
                          description:
                          - 'Selects a field of the pod: supports metadata.name, metadata.namespace,
                            metadata.labels, metadata.annotations, spec.nodeName,
                            spec.serviceAccountName, status.hostIP, status.podIP.'
                          type: complex
                          contains:
                            api_version:
                              description:
                              - Version of the schema the FieldPath is written in
                                terms of, defaults to "v1".
                              type: str
                            field_path:
                              description:
                              - Path of the field to select in the specified API version.
                              type: str
                        resource_field_ref:
                          description:
                          - 'Selects a resource of the container: only resources limits
                            and requests (limits.cpu, limits.memory, requests.cpu
                            and requests.memory) are currently supported.'
                          type: complex
                          contains:
                            container_name:
                              description:
                              - 'Container name: required for volumes, optional for
                                env vars'
                              type: str
                            divisor:
                              description:
                              - Specifies the output format of the exposed resources,
                                defaults to "1"
                              type: str
                            resource:
                              description:
                              - 'Required: resource to select'
                              type: str
                        secret_key_ref:
                          description:
                          - Selects a key of a secret in the pod's namespace
                          type: complex
                          contains:
                            key:
                              description:
                              - The key of the secret to select from. Must be a valid
                                secret key.
                              type: str
                            name:
                              description:
                              - Name of the referent.
                              type: str
                            optional:
                              description:
                              - Specify whether the Secret or it's key must be defined
                              type: bool
                dockerfile_path:
                  description:
                  - dockerfilePath is the path of the Dockerfile that will be used
                    to build the Docker image, relative to the root of the context
                    (contextDir).
                  type: str
                env:
                  description:
                  - env contains additional environment variables you want to pass
                    into a builder container.
                  type: list
                  contains:
                    name:
                      description:
                      - Name of the environment variable. Must be a C_IDENTIFIER.
                      type: str
                    value:
                      description:
                      - 'Variable references $(VAR_NAME) are expanded using the previous
                        defined environment variables in the container and any service
                        environment variables. If a variable cannot be resolved, the
                        reference in the input string will be unchanged. The $(VAR_NAME)
                        syntax can be escaped with a double $$, ie: $$(VAR_NAME).
                        Escaped references will never be expanded, regardless of whether
                        the variable exists or not. Defaults to "".'
                      type: str
                    value_from:
                      description:
                      - Source for the environment variable's value. Cannot be used
                        if value is not empty.
                      type: complex
                      contains:
                        config_map_key_ref:
                          description:
                          - Selects a key of a ConfigMap.
                          type: complex
                          contains:
                            key:
                              description:
                              - The key to select.
                              type: str
                            name:
                              description:
                              - Name of the referent.
                              type: str
                            optional:
                              description:
                              - Specify whether the ConfigMap or it's key must be
                                defined
                              type: bool
                        field_ref:
                          description:
                          - 'Selects a field of the pod: supports metadata.name, metadata.namespace,
                            metadata.labels, metadata.annotations, spec.nodeName,
                            spec.serviceAccountName, status.hostIP, status.podIP.'
                          type: complex
                          contains:
                            api_version:
                              description:
                              - Version of the schema the FieldPath is written in
                                terms of, defaults to "v1".
                              type: str
                            field_path:
                              description:
                              - Path of the field to select in the specified API version.
                              type: str
                        resource_field_ref:
                          description:
                          - 'Selects a resource of the container: only resources limits
                            and requests (limits.cpu, limits.memory, requests.cpu
                            and requests.memory) are currently supported.'
                          type: complex
                          contains:
                            container_name:
                              description:
                              - 'Container name: required for volumes, optional for
                                env vars'
                              type: str
                            divisor:
                              description:
                              - Specifies the output format of the exposed resources,
                                defaults to "1"
                              type: str
                            resource:
                              description:
                              - 'Required: resource to select'
                              type: str
                        secret_key_ref:
                          description:
                          - Selects a key of a secret in the pod's namespace
                          type: complex
                          contains:
                            key:
                              description:
                              - The key of the secret to select from. Must be a valid
                                secret key.
                              type: str
                            name:
                              description:
                              - Name of the referent.
                              type: str
                            optional:
                              description:
                              - Specify whether the Secret or it's key must be defined
                              type: bool
                force_pull:
                  description:
                  - forcePull describes if the builder should pull the images from
                    registry prior to building.
                  type: bool
                image_optimization_policy:
                  description:
                  - imageOptimizationPolicy describes what optimizations the system
                    can use when building images to reduce the final size or time
                    spent building the image. The default policy is 'None' which means
                    the final build image will be equivalent to an image created by
                    the Docker build API. The experimental policy 'SkipLayers' will
                    avoid commiting new layers in between each image step, and will
                    fail if the Dockerfile cannot provide compatibility with the 'None'
                    policy. An additional experimental policy 'SkipLayersAndWarn'
                    is the same as 'SkipLayers' but simply warns if compatibility
                    cannot be preserved.
                  type: str
                no_cache:
                  description:
                  - noCache if set to true indicates that the docker build must be
                    executed with the --no-cache=true flag
                  type: bool
                pull_secret:
                  description:
                  - pullSecret is the name of a Secret that would be used for setting
                    up the authentication for pulling the Docker images from the private
                    Docker registries
                  type: complex
                  contains:
                    name:
                      description:
                      - Name of the referent.
                      type: str
            jenkins_pipeline_strategy:
              description:
              - JenkinsPipelineStrategy holds the parameters to the Jenkins Pipeline
                build strategy. This strategy is in tech preview.
              type: complex
              contains:
                env:
                  description:
                  - env contains additional environment variables you want to pass
                    into a build pipeline.
                  type: list
                  contains:
                    name:
                      description:
                      - Name of the environment variable. Must be a C_IDENTIFIER.
                      type: str
                    value:
                      description:
                      - 'Variable references $(VAR_NAME) are expanded using the previous
                        defined environment variables in the container and any service
                        environment variables. If a variable cannot be resolved, the
                        reference in the input string will be unchanged. The $(VAR_NAME)
                        syntax can be escaped with a double $$, ie: $$(VAR_NAME).
                        Escaped references will never be expanded, regardless of whether
                        the variable exists or not. Defaults to "".'
                      type: str
                    value_from:
                      description:
                      - Source for the environment variable's value. Cannot be used
                        if value is not empty.
                      type: complex
                      contains:
                        config_map_key_ref:
                          description:
                          - Selects a key of a ConfigMap.
                          type: complex
                          contains:
                            key:
                              description:
                              - The key to select.
                              type: str
                            name:
                              description:
                              - Name of the referent.
                              type: str
                            optional:
                              description:
                              - Specify whether the ConfigMap or it's key must be
                                defined
                              type: bool
                        field_ref:
                          description:
                          - 'Selects a field of the pod: supports metadata.name, metadata.namespace,
                            metadata.labels, metadata.annotations, spec.nodeName,
                            spec.serviceAccountName, status.hostIP, status.podIP.'
                          type: complex
                          contains:
                            api_version:
                              description:
                              - Version of the schema the FieldPath is written in
                                terms of, defaults to "v1".
                              type: str
                            field_path:
                              description:
                              - Path of the field to select in the specified API version.
                              type: str
                        resource_field_ref:
                          description:
                          - 'Selects a resource of the container: only resources limits
                            and requests (limits.cpu, limits.memory, requests.cpu
                            and requests.memory) are currently supported.'
                          type: complex
                          contains:
                            container_name:
                              description:
                              - 'Container name: required for volumes, optional for
                                env vars'
                              type: str
                            divisor:
                              description:
                              - Specifies the output format of the exposed resources,
                                defaults to "1"
                              type: str
                            resource:
                              description:
                              - 'Required: resource to select'
                              type: str
                        secret_key_ref:
                          description:
                          - Selects a key of a secret in the pod's namespace
                          type: complex
                          contains:
                            key:
                              description:
                              - The key of the secret to select from. Must be a valid
                                secret key.
                              type: str
                            name:
                              description:
                              - Name of the referent.
                              type: str
                            optional:
                              description:
                              - Specify whether the Secret or it's key must be defined
                              type: bool
                jenkinsfile:
                  description:
                  - Jenkinsfile defines the optional raw contents of a Jenkinsfile
                    which defines a Jenkins pipeline build.
                  type: str
                jenkinsfile_path:
                  description:
                  - JenkinsfilePath is the optional path of the Jenkinsfile that will
                    be used to configure the pipeline relative to the root of the
                    context (contextDir). If both JenkinsfilePath & Jenkinsfile are
                    both not specified, this defaults to Jenkinsfile in the root of
                    the specified contextDir.
                  type: str
            source_strategy:
              description:
              - sourceStrategy holds the parameters to the Source build strategy.
              type: complex
              contains:
                _from:
                  description:
                  - from is reference to an DockerImage, ImageStreamTag, or ImageStreamImage
                    from which the docker image should be pulled
                  type: complex
                  contains:
                    api_version:
                      description:
                      - API version of the referent.
                      type: str
                    field_path:
                      description:
                      - 'If referring to a piece of an object instead of an entire
                        object, this string should contain a valid JSON/Go field access
                        statement, such as desiredState.manifest.containers[2]. For
                        example, if the object reference is to a container within
                        a pod, this would take on a value like: "spec.containers{name}"
                        (where "name" refers to the name of the container that triggered
                        the event) or if no container name is specified "spec.containers[2]"
                        (container with index 2 in this pod). This syntax is chosen
                        only to have some well-defined way of referencing a part of
                        an object.'
                      type: str
                    kind:
                      description:
                      - Kind of the referent.
                      type: str
                    name:
                      description:
                      - Name of the referent.
                      type: str
                    namespace:
                      description:
                      - Namespace of the referent.
                      type: str
                    resource_version:
                      description:
                      - Specific resourceVersion to which this reference is made,
                        if any.
                      type: str
                    uid:
                      description:
                      - UID of the referent.
                      type: str
                env:
                  description:
                  - env contains additional environment variables you want to pass
                    into a builder container.
                  type: list
                  contains:
                    name:
                      description:
                      - Name of the environment variable. Must be a C_IDENTIFIER.
                      type: str
                    value:
                      description:
                      - 'Variable references $(VAR_NAME) are expanded using the previous
                        defined environment variables in the container and any service
                        environment variables. If a variable cannot be resolved, the
                        reference in the input string will be unchanged. The $(VAR_NAME)
                        syntax can be escaped with a double $$, ie: $$(VAR_NAME).
                        Escaped references will never be expanded, regardless of whether
                        the variable exists or not. Defaults to "".'
                      type: str
                    value_from:
                      description:
                      - Source for the environment variable's value. Cannot be used
                        if value is not empty.
                      type: complex
                      contains:
                        config_map_key_ref:
                          description:
                          - Selects a key of a ConfigMap.
                          type: complex
                          contains:
                            key:
                              description:
                              - The key to select.
                              type: str
                            name:
                              description:
                              - Name of the referent.
                              type: str
                            optional:
                              description:
                              - Specify whether the ConfigMap or it's key must be
                                defined
                              type: bool
                        field_ref:
                          description:
                          - 'Selects a field of the pod: supports metadata.name, metadata.namespace,
                            metadata.labels, metadata.annotations, spec.nodeName,
                            spec.serviceAccountName, status.hostIP, status.podIP.'
                          type: complex
                          contains:
                            api_version:
                              description:
                              - Version of the schema the FieldPath is written in
                                terms of, defaults to "v1".
                              type: str
                            field_path:
                              description:
                              - Path of the field to select in the specified API version.
                              type: str
                        resource_field_ref:
                          description:
                          - 'Selects a resource of the container: only resources limits
                            and requests (limits.cpu, limits.memory, requests.cpu
                            and requests.memory) are currently supported.'
                          type: complex
                          contains:
                            container_name:
                              description:
                              - 'Container name: required for volumes, optional for
                                env vars'
                              type: str
                            divisor:
                              description:
                              - Specifies the output format of the exposed resources,
                                defaults to "1"
                              type: str
                            resource:
                              description:
                              - 'Required: resource to select'
                              type: str
                        secret_key_ref:
                          description:
                          - Selects a key of a secret in the pod's namespace
                          type: complex
                          contains:
                            key:
                              description:
                              - The key of the secret to select from. Must be a valid
                                secret key.
                              type: str
                            name:
                              description:
                              - Name of the referent.
                              type: str
                            optional:
                              description:
                              - Specify whether the Secret or it's key must be defined
                              type: bool
                force_pull:
                  description:
                  - forcePull describes if the builder should pull the images from
                    registry prior to building.
                  type: bool
                incremental:
                  description:
                  - incremental flag forces the Source build to do incremental builds
                    if true.
                  type: bool
                pull_secret:
                  description:
                  - pullSecret is the name of a Secret that would be used for setting
                    up the authentication for pulling the Docker images from the private
                    Docker registries
                  type: complex
                  contains:
                    name:
                      description:
                      - Name of the referent.
                      type: str
                runtime_artifacts:
                  description:
                  - 'runtimeArtifacts specifies a list of source/destination pairs
                    that will be copied from the builder to the runtime image. sourcePath
                    can be a file or directory. destinationDir must be a directory.
                    destinationDir can also be empty or equal to ".", in this case
                    it just refers to the root of WORKDIR. Deprecated: This feature
                    will be removed in a future release. Use ImageSource to copy binary
                    artifacts created from one build into a separate runtime image.'
                  type: list
                  contains:
                    destination_dir:
                      description:
                      - destinationDir is the relative directory within the build
                        directory where files copied from the image are placed.
                      type: str
                    source_path:
                      description:
                      - sourcePath is the absolute path of the file or directory inside
                        the image to copy to the build directory. If the source path
                        ends in /. then the content of the directory will be copied,
                        but the directory itself will not be created at the destination.
                      type: str
                runtime_image:
                  description:
                  - 'runtimeImage is an optional image that is used to run an application
                    without unneeded dependencies installed. The building of the application
                    is still done in the builder image but, post build, you can copy
                    the needed artifacts in the runtime image for use. Deprecated:
                    This feature will be removed in a future release. Use ImageSource
                    to copy binary artifacts created from one build into a separate
                    runtime image.'
                  type: complex
                  contains:
                    api_version:
                      description:
                      - API version of the referent.
                      type: str
                    field_path:
                      description:
                      - 'If referring to a piece of an object instead of an entire
                        object, this string should contain a valid JSON/Go field access
                        statement, such as desiredState.manifest.containers[2]. For
                        example, if the object reference is to a container within
                        a pod, this would take on a value like: "spec.containers{name}"
                        (where "name" refers to the name of the container that triggered
                        the event) or if no container name is specified "spec.containers[2]"
                        (container with index 2 in this pod). This syntax is chosen
                        only to have some well-defined way of referencing a part of
                        an object.'
                      type: str
                    kind:
                      description:
                      - Kind of the referent.
                      type: str
                    name:
                      description:
                      - Name of the referent.
                      type: str
                    namespace:
                      description:
                      - Namespace of the referent.
                      type: str
                    resource_version:
                      description:
                      - Specific resourceVersion to which this reference is made,
                        if any.
                      type: str
                    uid:
                      description:
                      - UID of the referent.
                      type: str
                scripts:
                  description:
                  - scripts is the location of Source scripts
                  type: str
            type:
              description:
              - type is the kind of build strategy.
              type: str
        successful_builds_history_limit:
          description:
          - successfulBuildsHistoryLimit is the number of old successful builds to
            retain. If not specified, all successful builds are retained.
          type: int
        triggers:
          description:
          - triggers determine how new Builds can be launched from a BuildConfig.
            If no triggers are defined, a new build can only occur as a result of
            an explicit client build creation.
          type: list
          contains:
            bitbucket:
              description:
              - BitbucketWebHook contains the parameters for a Bitbucket webhook type
                of trigger
              type: complex
              contains:
                allow_env:
                  description:
                  - allowEnv determines whether the webhook can set environment variables;
                    can only be set to true for GenericWebHook.
                  type: bool
                secret:
                  description:
                  - secret used to validate requests.
                  type: str
            generic:
              description:
              - generic contains the parameters for a Generic webhook type of trigger
              type: complex
              contains:
                allow_env:
                  description:
                  - allowEnv determines whether the webhook can set environment variables;
                    can only be set to true for GenericWebHook.
                  type: bool
                secret:
                  description:
                  - secret used to validate requests.
                  type: str
            github:
              description:
              - github contains the parameters for a GitHub webhook type of trigger
              type: complex
              contains:
                allow_env:
                  description:
                  - allowEnv determines whether the webhook can set environment variables;
                    can only be set to true for GenericWebHook.
                  type: bool
                secret:
                  description:
                  - secret used to validate requests.
                  type: str
            gitlab:
              description:
              - GitLabWebHook contains the parameters for a GitLab webhook type of
                trigger
              type: complex
              contains:
                allow_env:
                  description:
                  - allowEnv determines whether the webhook can set environment variables;
                    can only be set to true for GenericWebHook.
                  type: bool
                secret:
                  description:
                  - secret used to validate requests.
                  type: str
            image_change:
              description:
              - imageChange contains parameters for an ImageChange type of trigger
              type: complex
              contains:
                _from:
                  description:
                  - from is a reference to an ImageStreamTag that will trigger a build
                    when updated It is optional. If no From is specified, the From
                    image from the build strategy will be used. Only one ImageChangeTrigger
                    with an empty From reference is allowed in a build configuration.
                  type: complex
                  contains:
                    api_version:
                      description:
                      - API version of the referent.
                      type: str
                    field_path:
                      description:
                      - 'If referring to a piece of an object instead of an entire
                        object, this string should contain a valid JSON/Go field access
                        statement, such as desiredState.manifest.containers[2]. For
                        example, if the object reference is to a container within
                        a pod, this would take on a value like: "spec.containers{name}"
                        (where "name" refers to the name of the container that triggered
                        the event) or if no container name is specified "spec.containers[2]"
                        (container with index 2 in this pod). This syntax is chosen
                        only to have some well-defined way of referencing a part of
                        an object.'
                      type: str
                    kind:
                      description:
                      - Kind of the referent.
                      type: str
                    name:
                      description:
                      - Name of the referent.
                      type: str
                    namespace:
                      description:
                      - Namespace of the referent.
                      type: str
                    resource_version:
                      description:
                      - Specific resourceVersion to which this reference is made,
                        if any.
                      type: str
                    uid:
                      description:
                      - UID of the referent.
                      type: str
                last_triggered_image_id:
                  description:
                  - lastTriggeredImageID is used internally by the ImageChangeController
                    to save last used image ID for build
                  type: str
            type:
              description:
              - type is the type of build trigger
              type: str
    status:
      description:
      - status holds any relevant information about a build config
      type: complex
      contains:
        last_version:
          description:
          - lastVersion is used to inform about number of last triggered build.
          type: int
'''


def main():
    try:
        module = OpenShiftAnsibleModule('build_config', 'v1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
