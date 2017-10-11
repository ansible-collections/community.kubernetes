#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.k8s_common import KubernetesAnsibleModule, KubernetesAnsibleException

DOCUMENTATION = '''
module: k8s_v1_persistent_volume
short_description: Kubernetes PersistentVolume
description:
- Manage the lifecycle of a persistent_volume object. Supports check mode, and attempts
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
  spec_access_modes:
    description:
    - AccessModes contains all ways the volume can be mounted.
    aliases:
    - access_modes
    type: list
  spec_aws_elastic_block_store_fs_type:
    description:
    - 'Filesystem type of the volume that you want to mount. Tip: Ensure that the
      filesystem type is supported by the host operating system. Examples: "ext4",
      "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.'
    aliases:
    - aws_elastic_block_store_fs_type
  spec_aws_elastic_block_store_partition:
    description:
    - 'The partition in the volume that you want to mount. If omitted, the default
      is to mount by volume name. Examples: For volume /dev/sda1, you specify the
      partition as "1". Similarly, the volume partition for /dev/sda is "0" (or you
      can leave the property empty).'
    aliases:
    - aws_elastic_block_store_partition
    type: int
  spec_aws_elastic_block_store_read_only:
    description:
    - Specify "true" to force and set the ReadOnly property in VolumeMounts to "true".
      If omitted, the default is "false".
    aliases:
    - aws_elastic_block_store_read_only
    type: bool
  spec_aws_elastic_block_store_volume_id:
    description:
    - Unique ID of the persistent disk resource in AWS (Amazon EBS volume).
    aliases:
    - aws_elastic_block_store_volume_id
  spec_azure_disk_caching_mode:
    description:
    - 'Host Caching mode: None, Read Only, Read Write.'
    aliases:
    - azure_disk_caching_mode
  spec_azure_disk_disk_name:
    description:
    - The Name of the data disk in the blob storage
    aliases:
    - azure_disk_disk_name
  spec_azure_disk_disk_uri:
    description:
    - The URI the data disk in the blob storage
    aliases:
    - azure_disk_disk_uri
  spec_azure_disk_fs_type:
    description:
    - Filesystem type to mount. Must be a filesystem type supported by the host operating
      system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.
    aliases:
    - azure_disk_fs_type
  spec_azure_disk_kind:
    description:
    - 'Expected values Shared: mulitple blob disks per storage account Dedicated:
      single blob disk per storage account Managed: azure managed data disk (only
      in managed availability set). defaults to shared'
    aliases:
    - azure_disk_kind
  spec_azure_disk_read_only:
    description:
    - Defaults to false (read/write). ReadOnly here will force the ReadOnly setting
      in VolumeMounts.
    aliases:
    - azure_disk_read_only
    type: bool
  spec_azure_file_read_only:
    description:
    - Defaults to false (read/write). ReadOnly here will force the ReadOnly setting
      in VolumeMounts.
    aliases:
    - azure_file_read_only
    type: bool
  spec_azure_file_secret_name:
    description:
    - the name of secret that contains Azure Storage Account Name and Key
    aliases:
    - azure_file_secret_name
  spec_azure_file_share_name:
    description:
    - Share Name
    aliases:
    - azure_file_share_name
  spec_capacity:
    description:
    - A description of the persistent volume's resources and capacity.
    aliases:
    - capacity
    type: dict
  spec_cephfs_monitors:
    description:
    - 'Required: Monitors is a collection of Ceph monitors'
    aliases:
    - cephfs_monitors
    type: list
  spec_cephfs_path:
    description:
    - 'Optional: Used as the mounted root, rather than the full Ceph tree, default
      is /'
    aliases:
    - cephfs_path
  spec_cephfs_read_only:
    description:
    - 'Optional: Defaults to false (read/write). ReadOnly here will force the ReadOnly
      setting in VolumeMounts.'
    aliases:
    - cephfs_read_only
    type: bool
  spec_cephfs_secret_file:
    description:
    - 'Optional: SecretFile is the path to key ring for User, default is /etc/ceph/user.secret'
    aliases:
    - cephfs_secret_file
  spec_cephfs_secret_ref_name:
    description:
    - Name of the referent.
    aliases:
    - cephfs_secret_ref_name
  spec_cephfs_user:
    description:
    - 'Optional: User is the rados user name, default is admin'
    aliases:
    - cephfs_user
  spec_cinder_fs_type:
    description:
    - 'Filesystem type to mount. Must be a filesystem type supported by the host operating
      system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if
      unspecified.'
    aliases:
    - cinder_fs_type
  spec_cinder_read_only:
    description:
    - 'Optional: Defaults to false (read/write). ReadOnly here will force the ReadOnly
      setting in VolumeMounts.'
    aliases:
    - cinder_read_only
    type: bool
  spec_cinder_volume_id:
    description:
    - volume id used to identify the volume in cinder
    aliases:
    - cinder_volume_id
  spec_claim_ref_api_version:
    description:
    - API version of the referent.
    aliases:
    - claim_ref_api_version
  spec_claim_ref_field_path:
    description:
    - 'If referring to a piece of an object instead of an entire object, this string
      should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2].
      For example, if the object reference is to a container within a pod, this would
      take on a value like: "spec.containers{name}" (where "name" refers to the name
      of the container that triggered the event) or if no container name is specified
      "spec.containers[2]" (container with index 2 in this pod). This syntax is chosen
      only to have some well-defined way of referencing a part of an object.'
    aliases:
    - claim_ref_field_path
  spec_claim_ref_kind:
    description:
    - Kind of the referent.
    aliases:
    - claim_ref_kind
  spec_claim_ref_name:
    description:
    - Name of the referent.
    aliases:
    - claim_ref_name
  spec_claim_ref_namespace:
    description:
    - Namespace of the referent.
    aliases:
    - claim_ref_namespace
  spec_claim_ref_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - claim_ref_resource_version
  spec_claim_ref_uid:
    description:
    - UID of the referent.
    aliases:
    - claim_ref_uid
  spec_fc_fs_type:
    description:
    - Filesystem type to mount. Must be a filesystem type supported by the host operating
      system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.
    aliases:
    - fc_fs_type
  spec_fc_lun:
    description:
    - 'Required: FC target lun number'
    aliases:
    - fc_lun
    type: int
  spec_fc_read_only:
    description:
    - 'Optional: Defaults to false (read/write). ReadOnly here will force the ReadOnly
      setting in VolumeMounts.'
    aliases:
    - fc_read_only
    type: bool
  spec_fc_target_ww_ns:
    description:
    - 'Required: FC target worldwide names (WWNs)'
    aliases:
    - fc_target_ww_ns
    type: list
  spec_flex_volume_driver:
    description:
    - Driver is the name of the driver to use for this volume.
    aliases:
    - flex_volume_driver
  spec_flex_volume_fs_type:
    description:
    - Filesystem type to mount. Must be a filesystem type supported by the host operating
      system. Ex. "ext4", "xfs", "ntfs". The default filesystem depends on FlexVolume
      script.
    aliases:
    - flex_volume_fs_type
  spec_flex_volume_options:
    description:
    - 'Optional: Extra command options if any.'
    aliases:
    - flex_volume_options
    type: dict
  spec_flex_volume_read_only:
    description:
    - 'Optional: Defaults to false (read/write). ReadOnly here will force the ReadOnly
      setting in VolumeMounts.'
    aliases:
    - flex_volume_read_only
    type: bool
  spec_flex_volume_secret_ref_name:
    description:
    - Name of the referent.
    aliases:
    - flex_volume_secret_ref_name
  spec_flocker_dataset_name:
    description:
    - Name of the dataset stored as metadata -> name on the dataset for Flocker should
      be considered as deprecated
    aliases:
    - flocker_dataset_name
  spec_flocker_dataset_uuid:
    description:
    - UUID of the dataset. This is unique identifier of a Flocker dataset
    aliases:
    - flocker_dataset_uuid
  spec_gce_persistent_disk_fs_type:
    description:
    - 'Filesystem type of the volume that you want to mount. Tip: Ensure that the
      filesystem type is supported by the host operating system. Examples: "ext4",
      "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.'
    aliases:
    - gce_persistent_disk_fs_type
  spec_gce_persistent_disk_partition:
    description:
    - 'The partition in the volume that you want to mount. If omitted, the default
      is to mount by volume name. Examples: For volume /dev/sda1, you specify the
      partition as "1". Similarly, the volume partition for /dev/sda is "0" (or you
      can leave the property empty).'
    aliases:
    - gce_persistent_disk_partition
    type: int
  spec_gce_persistent_disk_pd_name:
    description:
    - Unique name of the PD resource in GCE. Used to identify the disk in GCE.
    aliases:
    - gce_persistent_disk_pd_name
  spec_gce_persistent_disk_read_only:
    description:
    - ReadOnly here will force the ReadOnly setting in VolumeMounts. Defaults to false.
    aliases:
    - gce_persistent_disk_read_only
    type: bool
  spec_glusterfs_endpoints:
    description:
    - EndpointsName is the endpoint name that details Glusterfs topology.
    aliases:
    - glusterfs_endpoints
  spec_glusterfs_path:
    description:
    - Path is the Glusterfs volume path.
    aliases:
    - glusterfs_path
  spec_glusterfs_read_only:
    description:
    - ReadOnly here will force the Glusterfs volume to be mounted with read-only permissions.
      Defaults to false.
    aliases:
    - glusterfs_read_only
    type: bool
  spec_host_path_path:
    description:
    - Path of the directory on the host.
    aliases:
    - host_path_path
  spec_iscsi_chap_auth_discovery:
    description:
    - whether support iSCSI Discovery CHAP authentication
    aliases:
    - iscsi_chap_auth_discovery
    type: bool
  spec_iscsi_chap_auth_session:
    description:
    - whether support iSCSI Session CHAP authentication
    aliases:
    - iscsi_chap_auth_session
    type: bool
  spec_iscsi_fs_type:
    description:
    - 'Filesystem type of the volume that you want to mount. Tip: Ensure that the
      filesystem type is supported by the host operating system. Examples: "ext4",
      "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.'
    aliases:
    - iscsi_fs_type
  spec_iscsi_iqn:
    description:
    - Target iSCSI Qualified Name.
    aliases:
    - iscsi_iqn
  spec_iscsi_iscsi_interface:
    description:
    - "Optional: Defaults to 'default' (tcp). iSCSI interface name that uses an iSCSI\
      \ transport."
    aliases:
    - iscsi_iscsi_interface
  spec_iscsi_lun:
    description:
    - iSCSI target lun number.
    aliases:
    - iscsi_lun
    type: int
  spec_iscsi_portals:
    description:
    - iSCSI target portal List. The portal is either an IP or ip_addr:port if the
      port is other than default (typically TCP ports 860 and 3260).
    aliases:
    - iscsi_portals
    type: list
  spec_iscsi_read_only:
    description:
    - ReadOnly here will force the ReadOnly setting in VolumeMounts. Defaults to false.
    aliases:
    - iscsi_read_only
    type: bool
  spec_iscsi_secret_ref_name:
    description:
    - Name of the referent.
    aliases:
    - iscsi_secret_ref_name
  spec_iscsi_target_portal:
    description:
    - iSCSI target portal. The portal is either an IP or ip_addr:port if the port
      is other than default (typically TCP ports 860 and 3260).
    aliases:
    - iscsi_target_portal
  spec_local_path:
    description:
    - The full path to the volume on the node For alpha, this path must be a directory
      Once block as a source is supported, then this path can point to a block device
    aliases:
    - local_path
  spec_nfs_path:
    description:
    - Path that is exported by the NFS server.
    aliases:
    - nfs_path
  spec_nfs_read_only:
    description:
    - ReadOnly here will force the NFS export to be mounted with read-only permissions.
      Defaults to false.
    aliases:
    - nfs_read_only
    type: bool
  spec_nfs_server:
    description:
    - Server is the hostname or IP address of the NFS server.
    aliases:
    - nfs_server
  spec_persistent_volume_reclaim_policy:
    description:
    - What happens to a persistent volume when released from its claim. Valid options
      are Retain (default) and Recycle. Recycling must be supported by the volume
      plugin underlying this persistent volume.
    aliases:
    - persistent_volume_reclaim_policy
  spec_photon_persistent_disk_fs_type:
    description:
    - Filesystem type to mount. Must be a filesystem type supported by the host operating
      system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.
    aliases:
    - photon_persistent_disk_fs_type
  spec_photon_persistent_disk_pd_id:
    description:
    - ID that identifies Photon Controller persistent disk
    aliases:
    - photon_persistent_disk_pd_id
  spec_portworx_volume_fs_type:
    description:
    - FSType represents the filesystem type to mount Must be a filesystem type supported
      by the host operating system. Ex. "ext4", "xfs". Implicitly inferred to be "ext4"
      if unspecified.
    aliases:
    - portworx_volume_fs_type
  spec_portworx_volume_read_only:
    description:
    - Defaults to false (read/write). ReadOnly here will force the ReadOnly setting
      in VolumeMounts.
    aliases:
    - portworx_volume_read_only
    type: bool
  spec_portworx_volume_volume_id:
    description:
    - VolumeID uniquely identifies a Portworx volume
    aliases:
    - portworx_volume_volume_id
  spec_quobyte_group:
    description:
    - Group to map volume access to Default is no group
    aliases:
    - quobyte_group
  spec_quobyte_read_only:
    description:
    - ReadOnly here will force the Quobyte volume to be mounted with read-only permissions.
      Defaults to false.
    aliases:
    - quobyte_read_only
    type: bool
  spec_quobyte_registry:
    description:
    - Registry represents a single or multiple Quobyte Registry services specified
      as a string as host:port pair (multiple entries are separated with commas) which
      acts as the central registry for volumes
    aliases:
    - quobyte_registry
  spec_quobyte_user:
    description:
    - User to map volume access to Defaults to serivceaccount user
    aliases:
    - quobyte_user
  spec_quobyte_volume:
    description:
    - Volume is a string that references an already created Quobyte volume by name.
    aliases:
    - quobyte_volume
  spec_rbd_fs_type:
    description:
    - 'Filesystem type of the volume that you want to mount. Tip: Ensure that the
      filesystem type is supported by the host operating system. Examples: "ext4",
      "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.'
    aliases:
    - rbd_fs_type
  spec_rbd_image:
    description:
    - The rados image name.
    aliases:
    - rbd_image
  spec_rbd_keyring:
    description:
    - Keyring is the path to key ring for RBDUser. Default is /etc/ceph/keyring.
    aliases:
    - rbd_keyring
  spec_rbd_monitors:
    description:
    - A collection of Ceph monitors.
    aliases:
    - rbd_monitors
    type: list
  spec_rbd_pool:
    description:
    - The rados pool name. Default is rbd.
    aliases:
    - rbd_pool
  spec_rbd_read_only:
    description:
    - ReadOnly here will force the ReadOnly setting in VolumeMounts. Defaults to false.
    aliases:
    - rbd_read_only
    type: bool
  spec_rbd_secret_ref_name:
    description:
    - Name of the referent.
    aliases:
    - rbd_secret_ref_name
  spec_rbd_user:
    description:
    - The rados user name. Default is admin.
    aliases:
    - rbd_user
  spec_scale_io_fs_type:
    description:
    - Filesystem type to mount. Must be a filesystem type supported by the host operating
      system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.
    aliases:
    - scale_io_fs_type
  spec_scale_io_gateway:
    description:
    - The host address of the ScaleIO API Gateway.
    aliases:
    - scale_io_gateway
  spec_scale_io_protection_domain:
    description:
    - The name of the Protection Domain for the configured storage (defaults to "default").
    aliases:
    - scale_io_protection_domain
  spec_scale_io_read_only:
    description:
    - Defaults to false (read/write). ReadOnly here will force the ReadOnly setting
      in VolumeMounts.
    aliases:
    - scale_io_read_only
    type: bool
  spec_scale_io_secret_ref_name:
    description:
    - Name of the referent.
    aliases:
    - scale_io_secret_ref_name
  spec_scale_io_ssl_enabled:
    description:
    - Flag to enable/disable SSL communication with Gateway, default false
    aliases:
    - scale_io_ssl_enabled
    type: bool
  spec_scale_io_storage_mode:
    description:
    - Indicates whether the storage for a volume should be thick or thin (defaults
      to "thin").
    aliases:
    - scale_io_storage_mode
  spec_scale_io_storage_pool:
    description:
    - The Storage Pool associated with the protection domain (defaults to "default").
    aliases:
    - scale_io_storage_pool
  spec_scale_io_system:
    description:
    - The name of the storage system as configured in ScaleIO.
    aliases:
    - scale_io_system
  spec_scale_io_volume_name:
    description:
    - The name of a volume already created in the ScaleIO system that is associated
      with this volume source.
    aliases:
    - scale_io_volume_name
  spec_storage_class_name:
    description:
    - Name of StorageClass to which this persistent volume belongs. Empty value means
      that this volume does not belong to any StorageClass.
    aliases:
    - storage_class_name
  spec_storageos_fs_type:
    description:
    - Filesystem type to mount. Must be a filesystem type supported by the host operating
      system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.
    aliases:
    - storageos_fs_type
  spec_storageos_read_only:
    description:
    - Defaults to false (read/write). ReadOnly here will force the ReadOnly setting
      in VolumeMounts.
    aliases:
    - storageos_read_only
    type: bool
  spec_storageos_secret_ref_api_version:
    description:
    - API version of the referent.
    aliases:
    - storageos_secret_ref_api_version
  spec_storageos_secret_ref_field_path:
    description:
    - 'If referring to a piece of an object instead of an entire object, this string
      should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2].
      For example, if the object reference is to a container within a pod, this would
      take on a value like: "spec.containers{name}" (where "name" refers to the name
      of the container that triggered the event) or if no container name is specified
      "spec.containers[2]" (container with index 2 in this pod). This syntax is chosen
      only to have some well-defined way of referencing a part of an object.'
    aliases:
    - storageos_secret_ref_field_path
  spec_storageos_secret_ref_kind:
    description:
    - Kind of the referent.
    aliases:
    - storageos_secret_ref_kind
  spec_storageos_secret_ref_name:
    description:
    - Name of the referent.
    aliases:
    - storageos_secret_ref_name
  spec_storageos_secret_ref_namespace:
    description:
    - Namespace of the referent.
    aliases:
    - storageos_secret_ref_namespace
  spec_storageos_secret_ref_resource_version:
    description:
    - Specific resourceVersion to which this reference is made, if any.
    aliases:
    - storageos_secret_ref_resource_version
  spec_storageos_secret_ref_uid:
    description:
    - UID of the referent.
    aliases:
    - storageos_secret_ref_uid
  spec_storageos_volume_name:
    description:
    - VolumeName is the human-readable name of the StorageOS volume. Volume names
      are only unique within a namespace.
    aliases:
    - storageos_volume_name
  spec_storageos_volume_namespace:
    description:
    - VolumeNamespace specifies the scope of the volume within StorageOS. If no namespace
      is specified then the Pod's namespace will be used. This allows the Kubernetes
      name scoping to be mirrored within StorageOS for tighter integration. Set VolumeName
      to any name to override the default behaviour. Set to "default" if you are not
      using namespaces within StorageOS. Namespaces that do not pre-exist within StorageOS
      will be created.
    aliases:
    - storageos_volume_namespace
  spec_vsphere_volume_fs_type:
    description:
    - Filesystem type to mount. Must be a filesystem type supported by the host operating
      system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.
    aliases:
    - vsphere_volume_fs_type
  spec_vsphere_volume_storage_policy_id:
    description:
    - Storage Policy Based Management (SPBM) profile ID associated with the StoragePolicyName.
    aliases:
    - vsphere_volume_storage_policy_id
  spec_vsphere_volume_storage_policy_name:
    description:
    - Storage Policy Based Management (SPBM) profile name.
    aliases:
    - vsphere_volume_storage_policy_name
  spec_vsphere_volume_volume_path:
    description:
    - Path that identifies vSphere volume vmdk
    aliases:
    - vsphere_volume_volume_path
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
- kubernetes == 3.0.0
'''

EXAMPLES = '''
- name: Create persitent volume
  k8s_v1_persistent_volume.yml:
    name: mypv
    state: present
    capacity:
      storage: 1Gi
    access_modes:
    - ReadWriteOnce
    persistent_volume_reclaim_policy: Recycle
    host_path_path: /tmp/test_volume
'''

RETURN = '''
api_version:
  type: string
  description: Requested API version
persistent_volume:
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
              - 'The partition in the volume that you want to mount. If omitted, the
                default is to mount by volume name. Examples: For volume /dev/sda1,
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
          - AzureDisk represents an Azure Data Disk mount on the host and bind mount
            to the pod.
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
              - Filesystem type to mount. Must be a filesystem type supported by the
                host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred
                to be "ext4" if unspecified.
              type: str
            kind:
              description:
              - 'Expected values Shared: mulitple blob disks per storage account Dedicated:
                single blob disk per storage account Managed: azure managed data disk
                (only in managed availability set). defaults to shared'
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
              - the name of secret that contains Azure Storage Account Name and Key
              type: str
            share_name:
              description:
              - Share Name
              type: str
        capacity:
          description:
          - A description of the persistent volume's resources and capacity.
          type: complex
          contains: str, str
        cephfs:
          description:
          - CephFS represents a Ceph FS mount on the host that shares a pod's lifetime
          type: complex
          contains:
            monitors:
              description:
              - 'Required: Monitors is a collection of Ceph monitors'
              type: list
              contains: str
            path:
              description:
              - 'Optional: Used as the mounted root, rather than the full Ceph tree,
                default is /'
              type: str
            read_only:
              description:
              - 'Optional: Defaults to false (read/write). ReadOnly here will force
                the ReadOnly setting in VolumeMounts.'
              type: bool
            secret_file:
              description:
              - 'Optional: SecretFile is the path to key ring for User, default is
                /etc/ceph/user.secret'
              type: str
            secret_ref:
              description:
              - 'Optional: SecretRef is reference to the authentication secret for
                User, default is empty.'
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
          - Cinder represents a cinder volume attached and mounted on kubelets host
            machine
          type: complex
          contains:
            fs_type:
              description:
              - 'Filesystem type to mount. Must be a filesystem type supported by
                the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly
                inferred to be "ext4" if unspecified.'
              type: str
            read_only:
              description:
              - 'Optional: Defaults to false (read/write). ReadOnly here will force
                the ReadOnly setting in VolumeMounts.'
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
                such as desiredState.manifest.containers[2]. For example, if the object
                reference is to a container within a pod, this would take on a value
                like: "spec.containers{name}" (where "name" refers to the name of
                the container that triggered the event) or if no container name is
                specified "spec.containers[2]" (container with index 2 in this pod).
                This syntax is chosen only to have some well-defined way of referencing
                a part of an object.'
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
              - Filesystem type to mount. Must be a filesystem type supported by the
                host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred
                to be "ext4" if unspecified.
              type: str
            lun:
              description:
              - 'Required: FC target lun number'
              type: int
            read_only:
              description:
              - 'Optional: Defaults to false (read/write). ReadOnly here will force
                the ReadOnly setting in VolumeMounts.'
              type: bool
            target_ww_ns:
              description:
              - 'Required: FC target worldwide names (WWNs)'
              type: list
              contains: str
        flex_volume:
          description:
          - FlexVolume represents a generic volume resource that is provisioned/attached
            using an exec based plugin. This is an alpha feature and may change in
            future.
          type: complex
          contains:
            driver:
              description:
              - Driver is the name of the driver to use for this volume.
              type: str
            fs_type:
              description:
              - Filesystem type to mount. Must be a filesystem type supported by the
                host operating system. Ex. "ext4", "xfs", "ntfs". The default filesystem
                depends on FlexVolume script.
              type: str
            options:
              description:
              - 'Optional: Extra command options if any.'
              type: complex
              contains: str, str
            read_only:
              description:
              - 'Optional: Defaults to false (read/write). ReadOnly here will force
                the ReadOnly setting in VolumeMounts.'
              type: bool
            secret_ref:
              description:
              - 'Optional: SecretRef is reference to the secret object containing
                sensitive information to pass to the plugin scripts. This may be empty
                if no secret object is specified. If the secret object contains more
                than one secret, all secrets are passed to the plugin scripts.'
              type: complex
              contains:
                name:
                  description:
                  - Name of the referent.
                  type: str
        flocker:
          description:
          - Flocker represents a Flocker volume attached to a kubelet's host machine
            and exposed to the pod for its usage. This depends on the Flocker control
            service being running
          type: complex
          contains:
            dataset_name:
              description:
              - Name of the dataset stored as metadata -> name on the dataset for
                Flocker should be considered as deprecated
              type: str
            dataset_uuid:
              description:
              - UUID of the dataset. This is unique identifier of a Flocker dataset
              type: str
        gce_persistent_disk:
          description:
          - GCEPersistentDisk represents a GCE Disk resource that is attached to a
            kubelet's host machine and then exposed to the pod. Provisioned by an
            admin.
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
              - 'The partition in the volume that you want to mount. If omitted, the
                default is to mount by volume name. Examples: For volume /dev/sda1,
                you specify the partition as "1". Similarly, the volume partition
                for /dev/sda is "0" (or you can leave the property empty).'
              type: int
            pd_name:
              description:
              - Unique name of the PD resource in GCE. Used to identify the disk in
                GCE.
              type: str
            read_only:
              description:
              - ReadOnly here will force the ReadOnly setting in VolumeMounts. Defaults
                to false.
              type: bool
        glusterfs:
          description:
          - Glusterfs represents a Glusterfs volume that is attached to a host and
            exposed to the pod. Provisioned by an admin.
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
              - ReadOnly here will force the Glusterfs volume to be mounted with read-only
                permissions. Defaults to false.
              type: bool
        host_path:
          description:
          - HostPath represents a directory on the host. Provisioned by a developer
            or tester. This is useful for single-node development and testing only!
            On-host storage is not supported in any way and WILL NOT WORK in a multi-node
            cluster.
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
            chap_auth_discovery:
              description:
              - whether support iSCSI Discovery CHAP authentication
              type: bool
            chap_auth_session:
              description:
              - whether support iSCSI Session CHAP authentication
              type: bool
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
            portals:
              description:
              - iSCSI target portal List. The portal is either an IP or ip_addr:port
                if the port is other than default (typically TCP ports 860 and 3260).
              type: list
              contains: str
            read_only:
              description:
              - ReadOnly here will force the ReadOnly setting in VolumeMounts. Defaults
                to false.
              type: bool
            secret_ref:
              description:
              - CHAP secret for iSCSI target and initiator authentication
              type: complex
              contains:
                name:
                  description:
                  - Name of the referent.
                  type: str
            target_portal:
              description:
              - iSCSI target portal. The portal is either an IP or ip_addr:port if
                the port is other than default (typically TCP ports 860 and 3260).
              type: str
        local:
          description:
          - Local represents directly-attached storage with node affinity
          type: complex
          contains:
            path:
              description:
              - The full path to the volume on the node For alpha, this path must
                be a directory Once block as a source is supported, then this path
                can point to a block device
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
          - What happens to a persistent volume when released from its claim. Valid
            options are Retain (default) and Recycle. Recycling must be supported
            by the volume plugin underlying this persistent volume.
          type: str
        photon_persistent_disk:
          description:
          - PhotonPersistentDisk represents a PhotonController persistent disk attached
            and mounted on kubelets host machine
          type: complex
          contains:
            fs_type:
              description:
              - Filesystem type to mount. Must be a filesystem type supported by the
                host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred
                to be "ext4" if unspecified.
              type: str
            pd_id:
              description:
              - ID that identifies Photon Controller persistent disk
              type: str
        portworx_volume:
          description:
          - PortworxVolume represents a portworx volume attached and mounted on kubelets
            host machine
          type: complex
          contains:
            fs_type:
              description:
              - FSType represents the filesystem type to mount Must be a filesystem
                type supported by the host operating system. Ex. "ext4", "xfs". Implicitly
                inferred to be "ext4" if unspecified.
              type: str
            read_only:
              description:
              - Defaults to false (read/write). ReadOnly here will force the ReadOnly
                setting in VolumeMounts.
              type: bool
            volume_id:
              description:
              - VolumeID uniquely identifies a Portworx volume
              type: str
        quobyte:
          description:
          - Quobyte represents a Quobyte mount on the host that shares a pod's lifetime
          type: complex
          contains:
            group:
              description:
              - Group to map volume access to Default is no group
              type: str
            read_only:
              description:
              - ReadOnly here will force the Quobyte volume to be mounted with read-only
                permissions. Defaults to false.
              type: bool
            registry:
              description:
              - Registry represents a single or multiple Quobyte Registry services
                specified as a string as host:port pair (multiple entries are separated
                with commas) which acts as the central registry for volumes
              type: str
            user:
              description:
              - User to map volume access to Defaults to serivceaccount user
              type: str
            volume:
              description:
              - Volume is a string that references an already created Quobyte volume
                by name.
              type: str
        rbd:
          description:
          - RBD represents a Rados Block Device mount on the host that shares a pod's
            lifetime.
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
              - ReadOnly here will force the ReadOnly setting in VolumeMounts. Defaults
                to false.
              type: bool
            secret_ref:
              description:
              - SecretRef is name of the authentication secret for RBDUser. If provided
                overrides keyring. Default is nil.
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
        scale_io:
          description:
          - ScaleIO represents a ScaleIO persistent volume attached and mounted on
            Kubernetes nodes.
          type: complex
          contains:
            fs_type:
              description:
              - Filesystem type to mount. Must be a filesystem type supported by the
                host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred
                to be "ext4" if unspecified.
              type: str
            gateway:
              description:
              - The host address of the ScaleIO API Gateway.
              type: str
            protection_domain:
              description:
              - The name of the Protection Domain for the configured storage (defaults
                to "default").
              type: str
            read_only:
              description:
              - Defaults to false (read/write). ReadOnly here will force the ReadOnly
                setting in VolumeMounts.
              type: bool
            secret_ref:
              description:
              - SecretRef references to the secret for ScaleIO user and other sensitive
                information. If this is not provided, Login operation will fail.
              type: complex
              contains:
                name:
                  description:
                  - Name of the referent.
                  type: str
            ssl_enabled:
              description:
              - Flag to enable/disable SSL communication with Gateway, default false
              type: bool
            storage_mode:
              description:
              - Indicates whether the storage for a volume should be thick or thin
                (defaults to "thin").
              type: str
            storage_pool:
              description:
              - The Storage Pool associated with the protection domain (defaults to
                "default").
              type: str
            system:
              description:
              - The name of the storage system as configured in ScaleIO.
              type: str
            volume_name:
              description:
              - The name of a volume already created in the ScaleIO system that is
                associated with this volume source.
              type: str
        storage_class_name:
          description:
          - Name of StorageClass to which this persistent volume belongs. Empty value
            means that this volume does not belong to any StorageClass.
          type: str
        storageos:
          description:
          - StorageOS represents a StorageOS volume that is attached to the kubelet's
            host machine and mounted into the pod
          type: complex
          contains:
            fs_type:
              description:
              - Filesystem type to mount. Must be a filesystem type supported by the
                host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred
                to be "ext4" if unspecified.
              type: str
            read_only:
              description:
              - Defaults to false (read/write). ReadOnly here will force the ReadOnly
                setting in VolumeMounts.
              type: bool
            secret_ref:
              description:
              - SecretRef specifies the secret to use for obtaining the StorageOS
                API credentials. If not specified, default values will be attempted.
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
            volume_name:
              description:
              - VolumeName is the human-readable name of the StorageOS volume. Volume
                names are only unique within a namespace.
              type: str
            volume_namespace:
              description:
              - VolumeNamespace specifies the scope of the volume within StorageOS.
                If no namespace is specified then the Pod's namespace will be used.
                This allows the Kubernetes name scoping to be mirrored within StorageOS
                for tighter integration. Set VolumeName to any name to override the
                default behaviour. Set to "default" if you are not using namespaces
                within StorageOS. Namespaces that do not pre-exist within StorageOS
                will be created.
              type: str
        vsphere_volume:
          description:
          - VsphereVolume represents a vSphere volume attached and mounted on kubelets
            host machine
          type: complex
          contains:
            fs_type:
              description:
              - Filesystem type to mount. Must be a filesystem type supported by the
                host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred
                to be "ext4" if unspecified.
              type: str
            storage_policy_id:
              description:
              - Storage Policy Based Management (SPBM) profile ID associated with
                the StoragePolicyName.
              type: str
            storage_policy_name:
              description:
              - Storage Policy Based Management (SPBM) profile name.
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
          - A human-readable message indicating details about why the volume is in
            this state.
          type: str
        phase:
          description:
          - Phase indicates if a volume is available, bound to a claim, or released
            by a claim.
          type: str
        reason:
          description:
          - Reason is a brief CamelCase string that describes any failure and is meant
            for machine parsing and tidy display in the CLI.
          type: str
'''


def main():
    try:
        module = KubernetesAnsibleModule('persistent_volume', 'v1')
    except KubernetesAnsibleException as exc:
        # The helper failed to init, so there is no module object. All we can do is raise the error.
        raise Exception(exc.message)

    try:
        module.execute_module()
    except KubernetesAnsibleException as exc:
        module.fail_json(msg="Module failed!", error=str(exc))


if __name__ == '__main__':
    main()
