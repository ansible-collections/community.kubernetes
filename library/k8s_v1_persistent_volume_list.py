#!/usr/bin/env python

from ansible.module_utils.k8s_common import OpenShiftAnsibleModule, OpenShiftAnsibleException

DOCUMENTATION = '''
module: k8s_v1_persistent_volume_list
short_description: Kubernetes PersistentVolumeList
description:
- Retrieve a list of persistent_volumes. List operations provide a snapshot read of
  the underlying objects, returning a resource_version representing a consistent version
  of the listed objects.
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
- openshift == 1.0.0-snapshot
'''

EXAMPLES = '''
'''

RETURN = '''
api_version:
  type: string
  description: Requested API version
persistent_volume_list:
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
      - List of persistent volumes.
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
          - Spec defines a specification of a persistent volume owned by the cluster.
            Provisioned by an administrator.
          type: complex
          contains:
            access_modes:
              description:
              - AccessModes contains all ways the volume can be mounted.
              type: list
              contains: str
            aws_elastic_block_store:
              description:
              - AWSElasticBlockStore represents an AWS Disk resource that is attached
                to a kubelet's host machine and then exposed to the pod.
              type: complex
              contains:
                fs_type:
                  description:
                  - 'Filesystem type of the volume that you want to mount. Tip: Ensure
                    that the filesystem type is supported by the host operating system.
                    Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4"
                    if unspecified.'
                  type: str
                partition:
                  description:
                  - 'The partition in the volume that you want to mount. If omitted,
                    the default is to mount by volume name. Examples: For volume /dev/sda1,
                    you specify the partition as "1". Similarly, the volume partition
                    for /dev/sda is "0" (or you can leave the property empty).'
                  type: int
                read_only:
                  description:
                  - Specify "true" to force and set the ReadOnly property in VolumeMounts
                    to "true". If omitted, the default is "false".
                  type: bool
                volume_id:
                  description:
                  - Unique ID of the persistent disk resource in AWS (Amazon EBS volume).
                  type: str
            azure_disk:
              description:
              - AzureDisk represents an Azure Data Disk mount on the host and bind
                mount to the pod.
              type: complex
              contains:
                caching_mode:
                  description:
                  - 'Host Caching mode: None, Read Only, Read Write.'
                  type: str
                disk_name:
                  description:
                  - The Name of the data disk in the blob storage
                  type: str
                disk_uri:
                  description:
                  - The URI the data disk in the blob storage
                  type: str
                fs_type:
                  description:
                  - Filesystem type to mount. Must be a filesystem type supported
                    by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly
                    inferred to be "ext4" if unspecified.
                  type: str
                read_only:
                  description:
                  - Defaults to false (read/write). ReadOnly here will force the ReadOnly
                    setting in VolumeMounts.
                  type: bool
            azure_file:
              description:
              - AzureFile represents an Azure File Service mount on the host and bind
                mount to the pod.
              type: complex
              contains:
                read_only:
                  description:
                  - Defaults to false (read/write). ReadOnly here will force the ReadOnly
                    setting in VolumeMounts.
                  type: bool
                secret_name:
                  description:
                  - the name of secret that contains Azure Storage Account Name and
                    Key
                  type: str
                share_name:
                  description:
                  - Share Name
                  type: str
            capacity:
              description:
              - A description of the persistent volume's resources and capacity.
              type: complex
              contains: str, ResourceQuantity
            cephfs:
              description:
              - CephFS represents a Ceph FS mount on the host that shares a pod's
                lifetime
              type: complex
              contains:
                monitors:
                  description:
                  - 'Required: Monitors is a collection of Ceph monitors'
                  type: list
                  contains: str
                path:
                  description:
                  - 'Optional: Used as the mounted root, rather than the full Ceph
                    tree, default is /'
                  type: str
                read_only:
                  description:
                  - 'Optional: Defaults to false (read/write). ReadOnly here will
                    force the ReadOnly setting in VolumeMounts.'
                  type: bool
                secret_file:
                  description:
                  - 'Optional: SecretFile is the path to key ring for User, default
                    is /etc/ceph/user.secret'
                  type: str
                secret_ref:
                  description:
                  - 'Optional: SecretRef is reference to the authentication secret
                    for User, default is empty.'
                  type: complex
                  contains:
                    name:
                      description:
                      - Name of the referent.
                      type: str
                user:
                  description:
                  - 'Optional: User is the rados user name, default is admin'
                  type: str
            cinder:
              description:
              - Cinder represents a cinder volume attached and mounted on kubelets
                host machine
              type: complex
              contains:
                fs_type:
                  description:
                  - 'Filesystem type to mount. Must be a filesystem type supported
                    by the host operating system. Examples: "ext4", "xfs", "ntfs".
                    Implicitly inferred to be "ext4" if unspecified.'
                  type: str
                read_only:
                  description:
                  - 'Optional: Defaults to false (read/write). ReadOnly here will
                    force the ReadOnly setting in VolumeMounts.'
                  type: bool
                volume_id:
                  description:
                  - volume id used to identify the volume in cinder
                  type: str
            claim_ref:
              description:
              - ClaimRef is part of a bi-directional binding between PersistentVolume
                and PersistentVolumeClaim. Expected to be non-nil when bound. claim.VolumeName
                is the authoritative bind between PV and PVC.
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
            fc:
              description:
              - FC represents a Fibre Channel resource that is attached to a kubelet's
                host machine and then exposed to the pod.
              type: complex
              contains:
                fs_type:
                  description:
                  - Filesystem type to mount. Must be a filesystem type supported
                    by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly
                    inferred to be "ext4" if unspecified.
                  type: str
                lun:
                  description:
                  - 'Required: FC target lun number'
                  type: int
                read_only:
                  description:
                  - 'Optional: Defaults to false (read/write). ReadOnly here will
                    force the ReadOnly setting in VolumeMounts.'
                  type: bool
                target_ww_ns:
                  description:
                  - 'Required: FC target worldwide names (WWNs)'
                  type: list
                  contains: str
            flex_volume:
              description:
              - FlexVolume represents a generic volume resource that is provisioned/attached
                using an exec based plugin. This is an alpha feature and may change
                in future.
              type: complex
              contains:
                driver:
                  description:
                  - Driver is the name of the driver to use for this volume.
                  type: str
                fs_type:
                  description:
                  - Filesystem type to mount. Must be a filesystem type supported
                    by the host operating system. Ex. "ext4", "xfs", "ntfs". The default
                    filesystem depends on FlexVolume script.
                  type: str
                options:
                  description:
                  - 'Optional: Extra command options if any.'
                  type: complex
                  contains: str, str
                read_only:
                  description:
                  - 'Optional: Defaults to false (read/write). ReadOnly here will
                    force the ReadOnly setting in VolumeMounts.'
                  type: bool
                secret_ref:
                  description:
                  - 'Optional: SecretRef is reference to the secret object containing
                    sensitive information to pass to the plugin scripts. This may
                    be empty if no secret object is specified. If the secret object
                    contains more than one secret, all secrets are passed to the plugin
                    scripts.'
                  type: complex
                  contains:
                    name:
                      description:
                      - Name of the referent.
                      type: str
            flocker:
              description:
              - Flocker represents a Flocker volume attached to a kubelet's host machine
                and exposed to the pod for its usage. This depends on the Flocker
                control service being running
              type: complex
              contains:
                dataset_name:
                  description:
                  - Name of the dataset stored as metadata -> name on the dataset
                    for Flocker should be considered as deprecated
                  type: str
                dataset_uuid:
                  description:
                  - UUID of the dataset. This is unique identifier of a Flocker dataset
                  type: str
            gce_persistent_disk:
              description:
              - GCEPersistentDisk represents a GCE Disk resource that is attached
                to a kubelet's host machine and then exposed to the pod. Provisioned
                by an admin.
              type: complex
              contains:
                fs_type:
                  description:
                  - 'Filesystem type of the volume that you want to mount. Tip: Ensure
                    that the filesystem type is supported by the host operating system.
                    Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4"
                    if unspecified.'
                  type: str
                partition:
                  description:
                  - 'The partition in the volume that you want to mount. If omitted,
                    the default is to mount by volume name. Examples: For volume /dev/sda1,
                    you specify the partition as "1". Similarly, the volume partition
                    for /dev/sda is "0" (or you can leave the property empty).'
                  type: int
                pd_name:
                  description:
                  - Unique name of the PD resource in GCE. Used to identify the disk
                    in GCE.
                  type: str
                read_only:
                  description:
                  - ReadOnly here will force the ReadOnly setting in VolumeMounts.
                    Defaults to false.
                  type: bool
            glusterfs:
              description:
              - Glusterfs represents a Glusterfs volume that is attached to a host
                and exposed to the pod. Provisioned by an admin.
              type: complex
              contains:
                endpoints:
                  description:
                  - EndpointsName is the endpoint name that details Glusterfs topology.
                  type: str
                path:
                  description:
                  - Path is the Glusterfs volume path.
                  type: str
                read_only:
                  description:
                  - ReadOnly here will force the Glusterfs volume to be mounted with
                    read-only permissions. Defaults to false.
                  type: bool
            host_path:
              description:
              - HostPath represents a directory on the host. Provisioned by a developer
                or tester. This is useful for single-node development and testing
                only! On-host storage is not supported in any way and WILL NOT WORK
                in a multi-node cluster.
              type: complex
              contains:
                path:
                  description:
                  - Path of the directory on the host.
                  type: str
            iscsi:
              description:
              - ISCSI represents an ISCSI Disk resource that is attached to a kubelet's
                host machine and then exposed to the pod. Provisioned by an admin.
              type: complex
              contains:
                fs_type:
                  description:
                  - 'Filesystem type of the volume that you want to mount. Tip: Ensure
                    that the filesystem type is supported by the host operating system.
                    Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4"
                    if unspecified.'
                  type: str
                iqn:
                  description:
                  - Target iSCSI Qualified Name.
                  type: str
                iscsi_interface:
                  description:
                  - "Optional: Defaults to 'default' (tcp). iSCSI interface name that\
                    \ uses an iSCSI transport."
                  type: str
                lun:
                  description:
                  - iSCSI target lun number.
                  type: int
                read_only:
                  description:
                  - ReadOnly here will force the ReadOnly setting in VolumeMounts.
                    Defaults to false.
                  type: bool
                target_portal:
                  description:
                  - iSCSI target portal. The portal is either an IP or ip_addr:port
                    if the port is other than default (typically TCP ports 860 and
                    3260).
                  type: str
            nfs:
              description:
              - NFS represents an NFS mount on the host. Provisioned by an admin.
              type: complex
              contains:
                path:
                  description:
                  - Path that is exported by the NFS server.
                  type: str
                read_only:
                  description:
                  - ReadOnly here will force the NFS export to be mounted with read-only
                    permissions. Defaults to false.
                  type: bool
                server:
                  description:
                  - Server is the hostname or IP address of the NFS server.
                  type: str
            persistent_volume_reclaim_policy:
              description:
              - What happens to a persistent volume when released from its claim.
                Valid options are Retain (default) and Recycle. Recycling must be
                supported by the volume plugin underlying this persistent volume.
              type: str
            photon_persistent_disk:
              description:
              - PhotonPersistentDisk represents a PhotonController persistent disk
                attached and mounted on kubelets host machine
              type: complex
              contains:
                fs_type:
                  description:
                  - Filesystem type to mount. Must be a filesystem type supported
                    by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly
                    inferred to be "ext4" if unspecified.
                  type: str
                pd_id:
                  description:
                  - ID that identifies Photon Controller persistent disk
                  type: str
            quobyte:
              description:
              - Quobyte represents a Quobyte mount on the host that shares a pod's
                lifetime
              type: complex
              contains:
                group:
                  description:
                  - Group to map volume access to Default is no group
                  type: str
                read_only:
                  description:
                  - ReadOnly here will force the Quobyte volume to be mounted with
                    read-only permissions. Defaults to false.
                  type: bool
                registry:
                  description:
                  - Registry represents a single or multiple Quobyte Registry services
                    specified as a string as host:port pair (multiple entries are
                    separated with commas) which acts as the central registry for
                    volumes
                  type: str
                user:
                  description:
                  - User to map volume access to Defaults to serivceaccount user
                  type: str
                volume:
                  description:
                  - Volume is a string that references an already created Quobyte
                    volume by name.
                  type: str
            rbd:
              description:
              - RBD represents a Rados Block Device mount on the host that shares
                a pod's lifetime.
              type: complex
              contains:
                fs_type:
                  description:
                  - 'Filesystem type of the volume that you want to mount. Tip: Ensure
                    that the filesystem type is supported by the host operating system.
                    Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4"
                    if unspecified.'
                  type: str
                image:
                  description:
                  - The rados image name.
                  type: str
                keyring:
                  description:
                  - Keyring is the path to key ring for RBDUser. Default is /etc/ceph/keyring.
                  type: str
                monitors:
                  description:
                  - A collection of Ceph monitors.
                  type: list
                  contains: str
                pool:
                  description:
                  - The rados pool name. Default is rbd.
                  type: str
                read_only:
                  description:
                  - ReadOnly here will force the ReadOnly setting in VolumeMounts.
                    Defaults to false.
                  type: bool
                secret_ref:
                  description:
                  - SecretRef is name of the authentication secret for RBDUser. If
                    provided overrides keyring. Default is nil.
                  type: complex
                  contains:
                    name:
                      description:
                      - Name of the referent.
                      type: str
                user:
                  description:
                  - The rados user name. Default is admin.
                  type: str
            vsphere_volume:
              description:
              - VsphereVolume represents a vSphere volume attached and mounted on
                kubelets host machine
              type: complex
              contains:
                fs_type:
                  description:
                  - Filesystem type to mount. Must be a filesystem type supported
                    by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly
                    inferred to be "ext4" if unspecified.
                  type: str
                volume_path:
                  description:
                  - Path that identifies vSphere volume vmdk
                  type: str
        status:
          description:
          - Status represents the current information/status for the persistent volume.
            Populated by the system. Read-only.
          type: complex
          contains:
            message:
              description:
              - A human-readable message indicating details about why the volume is
                in this state.
              type: str
            phase:
              description:
              - Phase indicates if a volume is available, bound to a claim, or released
                by a claim.
              type: str
            reason:
              description:
              - Reason is a brief CamelCase string that describes any failure and
                is meant for machine parsing and tidy display in the CLI.
              type: str
    kind:
      description:
      - Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to. Cannot
        be updated. In CamelCase.
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
'''


def main():
    try:
        module = OpenShiftAnsibleModule('persistent_volume_list', 'V1')
    except OpenShiftAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except OpenShiftAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()

