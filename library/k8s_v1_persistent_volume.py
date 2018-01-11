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
  spec_azure_file_secret_namespace:
    description:
    - the namespace of the secret that contains Azure Storage Account Name and Key
      default is the same as the Pod
    aliases:
    - azure_file_secret_namespace
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
    - Name is unique within a namespace to reference a secret resource.
    aliases:
    - cephfs_secret_ref_name
  spec_cephfs_secret_ref_namespace:
    description:
    - Namespace defines the space within which the secret name must be unique.
    aliases:
    - cephfs_secret_ref_namespace
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
    - 'Optional: FC target lun number'
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
    - 'Optional: FC target worldwide names (WWNs)'
    aliases:
    - fc_target_ww_ns
    type: list
  spec_fc_wwids:
    description:
    - 'Optional: FC volume world wide identifiers (wwids) Either wwids or combination
      of targetWWNs and lun must be set, but not both simultaneously.'
    aliases:
    - fc_wwids
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
    - Path of the directory on the host. If the path is a symlink, it will follow
      the link to the real path.
    aliases:
    - host_path_path
  spec_host_path_type:
    description:
    - Type for HostPath Volume Defaults to ""
    aliases:
    - host_path_type
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
  spec_iscsi_initiator_name:
    description:
    - Custom iSCSI initiator name. If initiatorName is specified with iscsiInterface
      simultaneously, new iSCSI interface <target portal>:<volume name> will be created
      for the connection.
    aliases:
    - iscsi_initiator_name
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
  spec_mount_options:
    description:
    - A list of mount options, e.g. ["ro", "soft"]. Not validated - mount will simply
      fail if one is invalid.
    aliases:
    - mount_options
    type: list
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
    - The name of the ScaleIO Protection Domain for the configured storage.
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
    - Name is unique within a namespace to reference a secret resource.
    aliases:
    - scale_io_secret_ref_name
  spec_scale_io_secret_ref_namespace:
    description:
    - Namespace defines the space within which the secret name must be unique.
    aliases:
    - scale_io_secret_ref_namespace
  spec_scale_io_ssl_enabled:
    description:
    - Flag to enable/disable SSL communication with Gateway, default false
    aliases:
    - scale_io_ssl_enabled
    type: bool
  spec_scale_io_storage_mode:
    description:
    - Indicates whether the storage for a volume should be ThickProvisioned or ThinProvisioned.
    aliases:
    - scale_io_storage_mode
  spec_scale_io_storage_pool:
    description:
    - The ScaleIO Storage Pool associated with the protection domain.
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
- kubernetes == 4.0.0
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
  description: Requested API version
  type: string
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
    spec:
      description:
      - Spec defines a specification of a persistent volume owned by the cluster.
        Provisioned by an administrator.
      type: complex
    status:
      description:
      - Status represents the current information/status for the persistent volume.
        Populated by the system. Read-only.
      type: complex
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
