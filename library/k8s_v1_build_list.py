#!/usr/bin/env python

from ansible.module_utils.k8s_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: k8s_v1_build_list
short_description: Kubernetes BuildList
description:
- Retrieve a list of builds. List operations provide a snapshot read of the underlying
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
  namespace:
    description:
    - Namespaces provide a scope for names. Names of resources need to be unique within
      a namespace, but not across namespaces. Provide the namespace for the object.
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
    - Determines if the object should be created, patched, deleted or replaced. When
      set to C(present), the object will be created, if it does not exist, or patched,
      if requested parameters differ from existing object attributes. If set to C(absent),
      an existing object will be deleted, and if set to C(replaced), an existing object
      will be completely replaced with a new object created from the supplied parameters.
    default: present
    choices:
    - present
    - absent
    - replaced
  username:
    description:
    - Provide a username for connecting to the API.
  verify_ssl:
    description:
    - Whether or not to verify the API server's SSL certificates.
    type: bool
requirements:
- openshift == 1.0.0-snapshot
'''

EXAMPLES = '''
'''

RETURN = '''
api_version:
  type: string
  description: Requested API version
build_list:
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
      - items is a list of builds
      type: list
      contains:
        api_version:
          description:
          - APIVersion defines the versioned schema of this representation of an object.
            Servers should convert recognized schemas to the latest internal value,
            and may reject unrecognized values.
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
          contains:
            annotations:
              description:
              - Annotations is an unstructured key value map stored with a resource
                that may be set by external tools to store and retrieve arbitrary
                metadata. They are not queryable and should be preserved when modifying
                objects.
              type: complex
              contains: str, str
            cluster_name:
              description:
              - The name of the cluster which the object belongs to. This is used
                to distinguish resources with same name and namespace in different
                clusters. This field is not set anywhere right now and apiserver is
                going to ignore it if set in create or update request.
              type: str
            creation_timestamp:
              description:
              - CreationTimestamp is a timestamp representing the server time when
                this object was created. It is not guaranteed to be set in happens-before
                order across separate operations. Clients may not set this value.
                It is represented in RFC3339 form and is in UTC. Populated by the
                system. Read-only. Null for lists.
              type: complex
              contains: {}
            deletion_grace_period_seconds:
              description:
              - Number of seconds allowed for this object to gracefully terminate
                before it will be removed from the system. Only set when deletionTimestamp
                is also set. May only be shortened. Read-only.
              type: int
            deletion_timestamp:
              description:
              - DeletionTimestamp is RFC 3339 date and time at which this resource
                will be deleted. This field is set by the server when a graceful deletion
                is requested by the user, and is not directly settable by a client.
                The resource is expected to be deleted (no longer visible from resource
                lists, and not reachable by name) after the time in this field. Once
                set, this value may not be unset or be set further into the future,
                although it may be shortened or the resource may be deleted prior
                to this time. For example, a user may request that a pod is deleted
                in 30 seconds. The Kubelet will react by sending a graceful termination
                signal to the containers in the pod. After that 30 seconds, the Kubelet
                will send a hard termination signal (SIGKILL) to the container and
                after cleanup, remove the pod from the API. In the presence of network
                partitions, this object may still exist after this timestamp, until
                an administrator or automated process can determine the resource is
                fully terminated. If not set, graceful deletion of the object has
                not been requested. Populated by the system when a graceful deletion
                is requested. Read-only.
              type: complex
              contains: {}
            finalizers:
              description:
              - Must be empty before the object is deleted from the registry. Each
                entry is an identifier for the responsible component that will remove
                the entry from the list. If the deletionTimestamp of the object is
                non-nil, entries in this list can only be removed.
              type: list
              contains: str
            generate_name:
              description:
              - GenerateName is an optional prefix, used by the server, to generate
                a unique name ONLY IF the Name field has not been provided. If this
                field is used, the name returned to the client will be different than
                the name passed. This value will also be combined with a unique suffix.
                The provided value has the same validation rules as the Name field,
                and may be truncated by the length of the suffix required to make
                the value unique on the server. If this field is specified and the
                generated name exists, the server will NOT return a 409 - instead,
                it will either return 201 Created or 500 with Reason ServerTimeout
                indicating a unique name could not be found in the time allotted,
                and the client should retry (optionally after the time indicated in
                the Retry-After header). Applied only if Name is not specified.
              type: str
            generation:
              description:
              - A sequence number representing a specific generation of the desired
                state. Populated by the system. Read-only.
              type: int
            labels:
              description:
              - Map of string keys and values that can be used to organize and categorize
                (scope and select) objects. May match selectors of replication controllers
                and services.
              type: complex
              contains: str, str
            name:
              description:
              - Name must be unique within a namespace. Is required when creating
                resources, although some resources may allow a client to request the
                generation of an appropriate name automatically. Name is primarily
                intended for creation idempotence and configuration definition. Cannot
                be updated.
              type: str
            namespace:
              description:
              - Namespace defines the space within each name must be unique. An empty
                namespace is equivalent to the "default" namespace, but "default"
                is the canonical representation. Not all objects are required to be
                scoped to a namespace - the value of this field for those objects
                will be empty. Must be a DNS_LABEL. Cannot be updated.
              type: str
            owner_references:
              description:
              - List of objects depended by this object. If ALL objects in the list
                have been deleted, this object will be garbage collected. If this
                object is managed by a controller, then an entry in this list will
                point to this controller, with the controller field set to true. There
                cannot be more than one managing controller.
              type: list
              contains:
                api_version:
                  description:
                  - API version of the referent.
                  type: str
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
              - An opaque value that represents the internal version of this object
                that can be used by clients to determine when objects have changed.
                May be used for optimistic concurrency, change detection, and the
                watch operation on a resource or set of resources. Clients must treat
                these values as opaque and passed unmodified back to the server. They
                may only be valid for a particular resource or set of resources. Populated
                by the system. Read-only. Value must be treated as opaque by clients
                and .
              type: str
            self_link:
              description:
              - SelfLink is a URL representing this object. Populated by the system.
                Read-only.
              type: str
            uid:
              description:
              - UID is the unique in time and space value for this object. It is typically
                generated by the server on successful creation of a resource and is
                not allowed to change on PUT operations. Populated by the system.
                Read-only.
              type: str
        spec:
          description:
          - spec is all the inputs used to execute the build.
          type: complex
          contains:
            completion_deadline_seconds:
              description:
              - completionDeadlineSeconds is an optional duration in seconds, counted
                from the time when a build pod gets scheduled in the system, that
                the build may be active on a node before the system actively tries
                to terminate the build; value must be positive integer
              type: int
            node_selector:
              description:
              - nodeSelector is a selector which must be true for the build pod to
                fit on a node If nil, it can be overridden by default build nodeselector
                values for the cluster. If set to an empty map or a map with any values,
                default build nodeselector values are ignored.
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
                    image. If there are multiple labels with the same name then the
                    last one in the list is used.
                  type: list
                  contains:
                    name:
                      description:
                      - name defines the name of the label. It must have non-zero
                        length.
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
                  - to defines an optional location to push the output of this build
                    to. Kind must be one of 'ImageStreamTag' or 'DockerImage'. This
                    value will be used to look up a Docker image repository to push
                    to. In the case of an ImageStreamTag, the ImageStreamTag will
                    be looked for in the namespace of the build unless Namespace is
                    specified.
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
            post_commit:
              description:
              - postCommit is a build hook executed after the build output image is
                committed, before it is pushed to a registry.
              type: complex
              contains:
                args:
                  description:
                  - args is a list of arguments that are provided to either Command,
                    Script or the Docker image's default entrypoint. The arguments
                    are placed immediately after the command to be run.
                  type: list
                  contains: str
                command:
                  description:
                  - command is the command to run. It may not be specified with Script.
                    This might be needed if the image doesn't have `/bin/sh`, or if
                    you do not want to use a shell. In all other cases, using Script
                    might be more convenient.
                  type: list
                  contains: str
                script:
                  description:
                  - script is a shell script to be run with `/bin/sh -ic`. It may
                    not be specified with Command. Use Script when a shell script
                    is appropriate to execute the post build hook, for example for
                    running unit tests with `rake test`. If you need control over
                    the image entrypoint, or if the image does not have `/bin/sh`,
                    use Command and/or Args. The `-i` flag is needed to support CentOS
                    and RHEL images that use Software Collections (SCL), in order
                    to have the appropriate collections enabled in the shell. E.g.,
                    in the Ruby image, this is necessary to make `ruby`, `bundle`
                    and other binaries available in the PATH.
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
                  contains: str, ResourceQuantity
                requests:
                  description:
                  - Requests describes the minimum amount of compute resources required.
                    If Requests is omitted for a container, it defaults to Limits
                    if that is explicitly specified, otherwise to an implementation-defined
                    value.
                  type: complex
                  contains: str, ResourceQuantity
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
                  - type of the build source, may be one of 'Source', 'Dockerfile',
                    'Binary', or 'Images'
                  type: str
            service_account:
              description:
              - serviceAccount is the name of the ServiceAccount to use to run the
                pod created by this build. The pod will be allowed to use secrets
                referenced by the ServiceAccount
              type: str
            source:
              description:
              - source describes the SCM in use.
              type: complex
              contains:
                binary:
                  description:
                  - binary builds accept a binary as their input. The binary is generally
                    assumed to be a tar, gzipped tar, or zip file depending on the
                    strategy. For Docker builds, this is the build context and an
                    optional Dockerfile may be specified to override any Dockerfile
                    in the build context. For Source builds, this is assumed to be
                    an archive as described above. For Source and Docker builds, if
                    binary.asFile is set the build will receive a directory with a
                    single file. contextDir may be used when an archive is provided.
                    Custom builds will receive this binary as input on STDIN.
                  type: complex
                  contains:
                    as_file:
                      description:
                      - asFile indicates that the provided binary input should be
                        considered a single file within the build input. For example,
                        specifying "webapp.war" would place the provided binary as
                        `/webapp.war` for the builder. If left empty, the Docker and
                        Source build strategies assume this file is a zip, tar, or
                        tar.gz file and extract it as the source. The custom strategy
                        receives this binary as standard input. This filename may
                        not contain slashes or be '..' or '.'.
                      type: str
                context_dir:
                  description:
                  - contextDir specifies the sub-directory where the source code for
                    the application exists. This allows to have buildable sources
                    in directory other than root of repository.
                  type: str
                dockerfile:
                  description:
                  - dockerfile is the raw contents of a Dockerfile which should be
                    built. When this option is specified, the FROM may be modified
                    based on your strategy base image and additional ENV stanzas from
                    your strategy environment will be added after the FROM, but before
                    the rest of your Dockerfile stanzas. The Dockerfile source type
                    may be used with other options like git - in those cases the Git
                    repo will have any innate Dockerfile replaced in the context dir.
                  type: str
                git:
                  description:
                  - git contains optional information about git build source
                  type: complex
                  contains:
                    http_proxy:
                      description:
                      - httpProxy is a proxy used to reach the git repository over
                        http
                      type: str
                    https_proxy:
                      description:
                      - httpsProxy is a proxy used to reach the git repository over
                        https
                      type: str
                    no_proxy:
                      description:
                      - noProxy is the list of domains for which the proxy should
                        not be used
                      type: str
                    ref:
                      description:
                      - ref is the branch/tag/ref to build.
                      type: str
                    uri:
                      description:
                      - uri points to the source that will be built. The structure
                        of the source will depend on the type of build to run
                      type: str
                images:
                  description:
                  - images describes a set of images to be used to provide source
                    for the build
                  type: list
                  contains:
                    _from:
                      description:
                      - from is a reference to an ImageStreamTag, ImageStreamImage,
                        or DockerImage to copy source from.
                      type: complex
                      contains:
                        api_version:
                          description:
                          - API version of the referent.
                          type: str
                        field_path:
                          description:
                          - 'If referring to a piece of an object instead of an entire
                            object, this string should contain a valid JSON/Go field
                            access statement, such as desiredState.manifest.containers[2].
                            For example, if the object reference is to a container
                            within a pod, this would take on a value like: "spec.containers{name}"
                            (where "name" refers to the name of the container that
                            triggered the event) or if no container name is specified
                            "spec.containers[2]" (container with index 2 in this pod).
                            This syntax is chosen only to have some well-defined way
                            of referencing a part of an object.'
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
                      - paths is a list of source and destination paths to copy from
                        the image.
                      type: list
                      contains:
                        destination_dir:
                          description:
                          - destinationDir is the relative directory within the build
                            directory where files copied from the image are placed.
                          type: str
                        source_path:
                          description:
                          - sourcePath is the absolute path of the file or directory
                            inside the image to copy to the build directory.
                          type: str
                    pull_secret:
                      description:
                      - pullSecret is a reference to a secret to be used to pull the
                        image from a registry If the image is pulled from the OpenShift
                        registry, this field does not need to be set.
                      type: complex
                      contains:
                        name:
                          description:
                          - Name of the referent.
                          type: str
                secrets:
                  description:
                  - secrets represents a list of secrets and their destinations that
                    will be used only for the build.
                  type: list
                  contains:
                    destination_dir:
                      description:
                      - destinationDir is the directory where the files from the secret
                        should be available for the build time. For the Source build
                        strategy, these will be injected into a container where the
                        assemble script runs. Later, when the script finishes, all
                        files injected will be truncated to zero length. For the Docker
                        build strategy, these will be copied into the build directory,
                        where the Dockerfile is located, so users can ADD or COPY
                        them during docker build.
                      type: str
                    secret:
                      description:
                      - secret is a reference to an existing secret that you want
                        to use in your build.
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
                    \ contains valid credentials for remote repository, where the\
                    \ data's key represent the authentication method to be used and\
                    \ value is the base64 encoded credentials. Supported auth methods\
                    \ are: ssh-privatekey."
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
                            object, this string should contain a valid JSON/Go field
                            access statement, such as desiredState.manifest.containers[2].
                            For example, if the object reference is to a container
                            within a pod, this would take on a value like: "spec.containers{name}"
                            (where "name" refers to the name of the container that
                            triggered the event) or if no container name is specified
                            "spec.containers[2]" (container with index 2 in this pod).
                            This syntax is chosen only to have some well-defined way
                            of referencing a part of an object.'
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
                      - buildAPIVersion is the requested API version for the Build
                        object serialized and passed to the custom builder
                      type: str
                    env:
                      description:
                      - env contains additional environment variables you want to
                        pass into a builder container
                      type: list
                      contains:
                        name:
                          description:
                          - Name of the environment variable. Must be a C_IDENTIFIER.
                          type: str
                        value:
                          description:
                          - 'Variable references $(VAR_NAME) are expanded using the
                            previous defined environment variables in the container
                            and any service environment variables. If a variable cannot
                            be resolved, the reference in the input string will be
                            unchanged. The $(VAR_NAME) syntax can be escaped with
                            a double $$, ie: $$(VAR_NAME). Escaped references will
                            never be expanded, regardless of whether the variable
                            exists or not. Defaults to "".'
                          type: str
                        value_from:
                          description:
                          - Source for the environment variable's value. Cannot be
                            used if value is not empty.
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
                            field_ref:
                              description:
                              - 'Selects a field of the pod: supports metadata.name,
                                metadata.namespace, metadata.labels, metadata.annotations,
                                spec.nodeName, spec.serviceAccountName, status.podIP.'
                              type: complex
                              contains:
                                api_version:
                                  description:
                                  - Version of the schema the FieldPath is written
                                    in terms of, defaults to "v1".
                                  type: str
                                field_path:
                                  description:
                                  - Path of the field to select in the specified API
                                    version.
                                  type: str
                            resource_field_ref:
                              description:
                              - 'Selects a resource of the container: only resources
                                limits and requests (limits.cpu, limits.memory, requests.cpu
                                and requests.memory) are currently supported.'
                              type: complex
                              contains:
                                container_name:
                                  description:
                                  - 'Container name: required for volumes, optional
                                    for env vars'
                                  type: str
                                divisor:
                                  description:
                                  - Specifies the output format of the exposed resources,
                                    defaults to "1"
                                  type: complex
                                  contains: {}
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
                                  - The key of the secret to select from. Must be
                                    a valid secret key.
                                  type: str
                                name:
                                  description:
                                  - Name of the referent.
                                  type: str
                    expose_docker_socket:
                      description:
                      - exposeDockerSocket will allow running Docker commands (and
                        build Docker images) from inside the Docker container.
                      type: bool
                    force_pull:
                      description:
                      - forcePull describes if the controller should configure the
                        build pod to always pull the images for the builder or only
                        pull if it is not present locally
                      type: bool
                    pull_secret:
                      description:
                      - pullSecret is the name of a Secret that would be used for
                        setting up the authentication for pulling the Docker images
                        from the private Docker registries
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
                        from which the docker image should be pulled the resulting
                        image will be used in the FROM line of the Dockerfile for
                        this build.
                      type: complex
                      contains:
                        api_version:
                          description:
                          - API version of the referent.
                          type: str
                        field_path:
                          description:
                          - 'If referring to a piece of an object instead of an entire
                            object, this string should contain a valid JSON/Go field
                            access statement, such as desiredState.manifest.containers[2].
                            For example, if the object reference is to a container
                            within a pod, this would take on a value like: "spec.containers{name}"
                            (where "name" refers to the name of the container that
                            triggered the event) or if no container name is specified
                            "spec.containers[2]" (container with index 2 in this pod).
                            This syntax is chosen only to have some well-defined way
                            of referencing a part of an object.'
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
                    dockerfile_path:
                      description:
                      - dockerfilePath is the path of the Dockerfile that will be
                        used to build the Docker image, relative to the root of the
                        context (contextDir).
                      type: str
                    env:
                      description:
                      - env contains additional environment variables you want to
                        pass into a builder container
                      type: list
                      contains:
                        name:
                          description:
                          - Name of the environment variable. Must be a C_IDENTIFIER.
                          type: str
                        value:
                          description:
                          - 'Variable references $(VAR_NAME) are expanded using the
                            previous defined environment variables in the container
                            and any service environment variables. If a variable cannot
                            be resolved, the reference in the input string will be
                            unchanged. The $(VAR_NAME) syntax can be escaped with
                            a double $$, ie: $$(VAR_NAME). Escaped references will
                            never be expanded, regardless of whether the variable
                            exists or not. Defaults to "".'
                          type: str
                        value_from:
                          description:
                          - Source for the environment variable's value. Cannot be
                            used if value is not empty.
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
                            field_ref:
                              description:
                              - 'Selects a field of the pod: supports metadata.name,
                                metadata.namespace, metadata.labels, metadata.annotations,
                                spec.nodeName, spec.serviceAccountName, status.podIP.'
                              type: complex
                              contains:
                                api_version:
                                  description:
                                  - Version of the schema the FieldPath is written
                                    in terms of, defaults to "v1".
                                  type: str
                                field_path:
                                  description:
                                  - Path of the field to select in the specified API
                                    version.
                                  type: str
                            resource_field_ref:
                              description:
                              - 'Selects a resource of the container: only resources
                                limits and requests (limits.cpu, limits.memory, requests.cpu
                                and requests.memory) are currently supported.'
                              type: complex
                              contains:
                                container_name:
                                  description:
                                  - 'Container name: required for volumes, optional
                                    for env vars'
                                  type: str
                                divisor:
                                  description:
                                  - Specifies the output format of the exposed resources,
                                    defaults to "1"
                                  type: complex
                                  contains: {}
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
                                  - The key of the secret to select from. Must be
                                    a valid secret key.
                                  type: str
                                name:
                                  description:
                                  - Name of the referent.
                                  type: str
                    force_pull:
                      description:
                      - forcePull describes if the builder should pull the images
                        from registry prior to building.
                      type: bool
                    no_cache:
                      description:
                      - noCache if set to true indicates that the docker build must
                        be executed with the --no-cache=true flag
                      type: bool
                    pull_secret:
                      description:
                      - pullSecret is the name of a Secret that would be used for
                        setting up the authentication for pulling the Docker images
                        from the private Docker registries
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
                    jenkinsfile:
                      description:
                      - Jenkinsfile defines the optional raw contents of a Jenkinsfile
                        which defines a Jenkins pipeline build.
                      type: str
                    jenkinsfile_path:
                      description:
                      - JenkinsfilePath is the optional path of the Jenkinsfile that
                        will be used to configure the pipeline relative to the root
                        of the context (contextDir). If both JenkinsfilePath & Jenkinsfile
                        are both not specified, this defaults to Jenkinsfile in the
                        root of the specified contextDir.
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
                            object, this string should contain a valid JSON/Go field
                            access statement, such as desiredState.manifest.containers[2].
                            For example, if the object reference is to a container
                            within a pod, this would take on a value like: "spec.containers{name}"
                            (where "name" refers to the name of the container that
                            triggered the event) or if no container name is specified
                            "spec.containers[2]" (container with index 2 in this pod).
                            This syntax is chosen only to have some well-defined way
                            of referencing a part of an object.'
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
                      - env contains additional environment variables you want to
                        pass into a builder container
                      type: list
                      contains:
                        name:
                          description:
                          - Name of the environment variable. Must be a C_IDENTIFIER.
                          type: str
                        value:
                          description:
                          - 'Variable references $(VAR_NAME) are expanded using the
                            previous defined environment variables in the container
                            and any service environment variables. If a variable cannot
                            be resolved, the reference in the input string will be
                            unchanged. The $(VAR_NAME) syntax can be escaped with
                            a double $$, ie: $$(VAR_NAME). Escaped references will
                            never be expanded, regardless of whether the variable
                            exists or not. Defaults to "".'
                          type: str
                        value_from:
                          description:
                          - Source for the environment variable's value. Cannot be
                            used if value is not empty.
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
                            field_ref:
                              description:
                              - 'Selects a field of the pod: supports metadata.name,
                                metadata.namespace, metadata.labels, metadata.annotations,
                                spec.nodeName, spec.serviceAccountName, status.podIP.'
                              type: complex
                              contains:
                                api_version:
                                  description:
                                  - Version of the schema the FieldPath is written
                                    in terms of, defaults to "v1".
                                  type: str
                                field_path:
                                  description:
                                  - Path of the field to select in the specified API
                                    version.
                                  type: str
                            resource_field_ref:
                              description:
                              - 'Selects a resource of the container: only resources
                                limits and requests (limits.cpu, limits.memory, requests.cpu
                                and requests.memory) are currently supported.'
                              type: complex
                              contains:
                                container_name:
                                  description:
                                  - 'Container name: required for volumes, optional
                                    for env vars'
                                  type: str
                                divisor:
                                  description:
                                  - Specifies the output format of the exposed resources,
                                    defaults to "1"
                                  type: complex
                                  contains: {}
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
                                  - The key of the secret to select from. Must be
                                    a valid secret key.
                                  type: str
                                name:
                                  description:
                                  - Name of the referent.
                                  type: str
                    force_pull:
                      description:
                      - forcePull describes if the builder should pull the images
                        from registry prior to building.
                      type: bool
                    incremental:
                      description:
                      - incremental flag forces the Source build to do incremental
                        builds if true.
                      type: bool
                    pull_secret:
                      description:
                      - pullSecret is the name of a Secret that would be used for
                        setting up the authentication for pulling the Docker images
                        from the private Docker registries
                      type: complex
                      contains:
                        name:
                          description:
                          - Name of the referent.
                          type: str
                    runtime_artifacts:
                      description:
                      - runtimeArtifacts specifies a list of source/destination pairs
                        that will be copied from the builder to the runtime image.
                        sourcePath can be a file or directory. destinationDir must
                        be a directory. destinationDir can also be empty or equal
                        to ".", in this case it just refers to the root of WORKDIR.
                        This field and the feature it enables are in tech preview.
                      type: list
                      contains:
                        destination_dir:
                          description:
                          - destinationDir is the relative directory within the build
                            directory where files copied from the image are placed.
                          type: str
                        source_path:
                          description:
                          - sourcePath is the absolute path of the file or directory
                            inside the image to copy to the build directory.
                          type: str
                    runtime_image:
                      description:
                      - runtimeImage is an optional image that is used to run an application
                        without unneeded dependencies installed. The building of the
                        application is still done in the builder image but, post build,
                        you can copy the needed artifacts in the runtime image for
                        use. This field and the feature it enables are in tech preview.
                      type: complex
                      contains:
                        api_version:
                          description:
                          - API version of the referent.
                          type: str
                        field_path:
                          description:
                          - 'If referring to a piece of an object instead of an entire
                            object, this string should contain a valid JSON/Go field
                            access statement, such as desiredState.manifest.containers[2].
                            For example, if the object reference is to a container
                            within a pod, this would take on a value like: "spec.containers{name}"
                            (where "name" refers to the name of the container that
                            triggered the event) or if no container name is specified
                            "spec.containers[2]" (container with index 2 in this pod).
                            This syntax is chosen only to have some well-defined way
                            of referencing a part of an object.'
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
            triggered_by:
              description:
              - triggeredBy describes which triggers started the most recent update
                to the build configuration and contains information about those triggers.
              type: list
              contains:
                generic_web_hook:
                  description:
                  - genericWebHook holds data about a builds generic webhook trigger.
                  type: complex
                  contains:
                    revision:
                      description:
                      - revision is an optional field that stores the git source revision
                        information of the generic webhook trigger when it is available.
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
                          - type of the build source, may be one of 'Source', 'Dockerfile',
                            'Binary', or 'Images'
                          type: str
                    secret:
                      description:
                      - secret is the obfuscated webhook secret that triggered a build.
                      type: str
                github_web_hook:
                  description:
                  - gitHubWebHook represents data for a GitHub webhook that fired
                    a specific build.
                  type: complex
                  contains:
                    revision:
                      description:
                      - revision is the git revision information of the trigger.
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
                          - type of the build source, may be one of 'Source', 'Dockerfile',
                            'Binary', or 'Images'
                          type: str
                    secret:
                      description:
                      - secret is the obfuscated webhook secret that triggered a build.
                      type: str
                image_change_build:
                  description:
                  - imageChangeBuild stores information about an imagechange event
                    that triggered a new build.
                  type: complex
                  contains:
                    from_ref:
                      description:
                      - fromRef contains detailed information about an image that
                        triggered a build.
                      type: complex
                      contains:
                        api_version:
                          description:
                          - API version of the referent.
                          type: str
                        field_path:
                          description:
                          - 'If referring to a piece of an object instead of an entire
                            object, this string should contain a valid JSON/Go field
                            access statement, such as desiredState.manifest.containers[2].
                            For example, if the object reference is to a container
                            within a pod, this would take on a value like: "spec.containers{name}"
                            (where "name" refers to the name of the container that
                            triggered the event) or if no container name is specified
                            "spec.containers[2]" (container with index 2 in this pod).
                            This syntax is chosen only to have some well-defined way
                            of referencing a part of an object.'
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
                    image_id:
                      description:
                      - imageID is the ID of the image that triggered a a new build.
                      type: str
                message:
                  description:
                  - 'message is used to store a human readable message for why the
                    build was triggered. E.g.: "Manually triggered by user", "Configuration
                    change",etc.'
                  type: str
        status:
          description:
          - status is the current status of the build.
          type: complex
          contains:
            cancelled:
              description:
              - cancelled describes if a cancel event was triggered for the build.
              type: bool
            completion_timestamp:
              description:
              - completionTimestamp is a timestamp representing the server time when
                this Build was finished, whether that build failed or succeeded. It
                reflects the time at which the Pod running the Build terminated. It
                is represented in RFC3339 form and is in UTC.
              type: complex
              contains: {}
            config:
              description:
              - config is an ObjectReference to the BuildConfig this Build is based
                on.
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
            duration:
              description:
              - duration contains time.Duration object describing build time.
              type: int
            message:
              description:
              - message is a human-readable message indicating details about why the
                build has this status.
              type: str
            output:
              description:
              - output describes the Docker image the build has produced.
              type: complex
              contains:
                to:
                  description:
                  - to describes the status of the built image being pushed to a registry.
                  type: complex
                  contains:
                    image_digest:
                      description:
                      - imageDigest is the digest of the built Docker image. The digest
                        uniquely identifies the image in the registry to which it
                        was pushed. Please note that this field may not always be
                        set even if the push completes successfully - e.g. when the
                        registry returns no digest or returns it in a format that
                        the builder doesn't understand.
                      type: str
            output_docker_image_reference:
              description:
              - outputDockerImageReference contains a reference to the Docker image
                that will be built by this build. Its value is computed from Build.Spec.Output.To,
                and should include the registry address, so that it can be used to
                push and pull the image.
              type: str
            phase:
              description:
              - phase is the point in the build lifecycle.
              type: str
            reason:
              description:
              - reason is a brief CamelCase string that describes any failure and
                is meant for machine parsing and tidy display in the CLI.
              type: str
            start_timestamp:
              description:
              - startTimestamp is a timestamp representing the server time when this
                Build started running in a Pod. It is represented in RFC3339 form
                and is in UTC.
              type: complex
              contains: {}
    kind:
      description:
      - Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to. Cannot
        be updated. In CamelCase.
      type: str
    metadata:
      description:
      - metadata for BuildList.
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
'''


def main():
    try:
        module = OpenShiftAnsibleModule('build_list', 'V1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()

