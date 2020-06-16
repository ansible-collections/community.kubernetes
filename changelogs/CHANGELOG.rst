===================================
Kubernetes Collection Release Notes
===================================

.. contents:: Topics


v0.11.0
=======

Major Changes
-------------

- helm - New module for managing Helm charts.
- helm_info - New module for retrieving Helm chart information.
- helm_repository - New module for managing Helm repositories.

Minor Changes
-------------

- Rename repository to ``community.kubernetes``.

Bugfixes
--------

- Make sure extra files are not included in built collection.
- Update GitHub Actions workflow for better CI stability.
- k8s_log - Module no longer attempts to parse log as JSON.

New Modules
-----------

- helm - Manages Kubernetes packages with the Helm package manager
- helm_info - Get information from Helm package deployed inside the cluster
- helm_repository - Add and remove Helm repository

v0.10.0
=======

Major Changes
-------------

- k8s_exec - New module for executing commands on pods via Kubernetes API.
- k8s_log - New module for retrieving pod logs.

Minor Changes
-------------

- k8s - Added ``persist_config`` option for persisting refreshed tokens.

Security Fixes
--------------

- kubectl - Warn about information disclosure when using options like ``kubectl_password``, ``kubectl_extra_args``, and ``kubectl_token`` to pass data through to the command line using the ``kubectl`` connection plugin.

Bugfixes
--------

- k8s - Add exception handling when retrieving k8s client.
- k8s - Fix argspec for 'elements'.
- k8s - Use ``from_yaml`` filter with lookup examples in ``k8s`` module documentation examples.
- k8s_service - Fix argspec.
- kubectl - Fix documentation in kubectl connection plugin.

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
