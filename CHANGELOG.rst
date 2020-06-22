===================================
Kubernetes Collection Release Notes
===================================

.. contents:: Topics


v0.11.0
=======

Major Changes
-------------

- helm - New module for managing Helm charts (https://github.com/ansible-collections/community.kubernetes/pull/61).
- helm_info - New module for retrieving Helm chart information (https://github.com/ansible-collections/community.kubernetes/pull/61).
- helm_repository - New module for managing Helm repositories (https://github.com/ansible-collections/community.kubernetes/pull/61).

Minor Changes
-------------

- Rename repository to ``community.kubernetes`` (https://github.com/ansible-collections/community.kubernetes/pull/81).

Bugfixes
--------

- Make sure extra files are not included in built collection (https://github.com/ansible-collections/community.kubernetes/pull/85).
- Update GitHub Actions workflow for better CI stability (https://github.com/ansible-collections/community.kubernetes/pull/78).
- k8s_log - Module no longer attempts to parse log as JSON (https://github.com/ansible-collections/community.kubernetes/pull/69).

New Modules
-----------

- helm - Manages Kubernetes packages with the Helm package manager
- helm_info - Get information from Helm package deployed inside the cluster
- helm_repository - Add and remove Helm repository

v0.10.0
=======

Major Changes
-------------

- k8s_exec - New module for executing commands on pods via Kubernetes API (https://github.com/ansible-collections/community.kubernetes/pull/14).
- k8s_log - New module for retrieving pod logs (https://github.com/ansible-collections/community.kubernetes/pull/16).

Minor Changes
-------------

- k8s - Added ``persist_config`` option for persisting refreshed tokens (https://github.com/ansible-collections/community.kubernetes/issues/49).

Security Fixes
--------------

- kubectl - Warn about information disclosure when using options like ``kubectl_password``, ``kubectl_extra_args``, and ``kubectl_token`` to pass data through to the command line using the ``kubectl`` connection plugin (https://github.com/ansible-collections/community.kubernetes/pull/51).

Bugfixes
--------

- k8s - Add exception handling when retrieving k8s client (https://github.com/ansible-collections/community.kubernetes/pull/54).
- k8s - Fix argspec for 'elements' (https://github.com/ansible-collections/community.kubernetes/issues/13).
- k8s - Use ``from_yaml`` filter with lookup examples in ``k8s`` module documentation examples (https://github.com/ansible-collections/community.kubernetes/pull/56).
- k8s_service - Fix argspec (https://github.com/ansible-collections/community.kubernetes/issues/33).
- kubectl - Fix documentation in kubectl connection plugin (https://github.com/ansible-collections/community.kubernetes/pull/52).

New Modules
-----------

- k8s_exec - Execute command in Pod
- k8s_log - Fetch logs from Kubernetes resources

v0.9.0
======

Major Changes
-------------

- k8s - Inventory source migrated from Ansible 2.9 to Kubernetes collection.
- k8s - Lookup plugin migrated from Ansible 2.9 to Kubernetes collection.
- k8s - Module migrated from Ansible 2.9 to Kubernetes collection.
- k8s_auth - Module migrated from Ansible 2.9 to Kubernetes collection.
- k8s_config_resource_name - Filter plugin migrated from Ansible 2.9 to Kubernetes collection.
- k8s_info - Module migrated from Ansible 2.9 to Kubernetes collection.
- k8s_scale - Module migrated from Ansible 2.9 to Kubernetes collection.
- k8s_service - Module migrated from Ansible 2.9 to Kubernetes collection.
- kubectl - Connection plugin migrated from Ansible 2.9 to Kubernetes collection.
- openshift - Inventory source migrated from Ansible 2.9 to Kubernetes collection.
