===================================
Kubernetes Collection Release Notes
===================================

.. contents:: Topics


v1.0.0
======

Major Changes
-------------

- helm_plugin - new module to manage Helm plugins (https://github.com/ansible-collections/community.kubernetes/pull/154).
- helm_plugin_info - new modules to gather information about Helm plugins (https://github.com/ansible-collections/community.kubernetes/pull/154).
- k8s_exec - Return rc for the command executed (https://github.com/ansible-collections/community.kubernetes/pull/158).

Minor Changes
-------------

- Ensure check mode results are as expected (https://github.com/ansible-collections/community.kubernetes/pull/155).
- Update base branch to 'main' (https://github.com/ansible-collections/community.kubernetes/issues/148).
- helm - Add support for K8S_AUTH_CONTEXT, K8S_AUTH_KUBECONFIG env (https://github.com/ansible-collections/community.kubernetes/pull/141).
- helm - Allow creating namespaces with Helm (https://github.com/ansible-collections/community.kubernetes/pull/157).
- helm - add aliases context for kube_context (https://github.com/ansible-collections/community.kubernetes/pull/152).
- helm - add support for K8S_AUTH_KUBECONFIG and K8S_AUTH_CONTEXT environment variable (https://github.com/ansible-collections/community.kubernetes/issues/140).
- helm_info - add aliases context for kube_context (https://github.com/ansible-collections/community.kubernetes/pull/152).
- helm_info - add support for K8S_AUTH_KUBECONFIG and K8S_AUTH_CONTEXT environment variable (https://github.com/ansible-collections/community.kubernetes/issues/140).
- k8s_exec - return RC for the command executed (https://github.com/ansible-collections/community.kubernetes/issues/122).
- k8s_info - Update example using vars (https://github.com/ansible-collections/community.kubernetes/pull/156).

Security Fixes
--------------

- kubectl - connection plugin now redact kubectl_token and kubectl_password in console log (https://github.com/ansible-collections/community.kubernetes/issues/65).
- kubectl - redacted token and password from console log (https://github.com/ansible-collections/community.kubernetes/pull/159).

Bugfixes
--------

- Test against stable ansible branch so molecule tests work (https://github.com/ansible-collections/community.kubernetes/pull/168).
- Update openshift requirements in k8s module doc (https://github.com/ansible-collections/community.kubernetes/pull/153).

New Modules
-----------

- helm_plugin - Manage Helm plugins
- helm_plugin_info - Gather information about Helm plugins

v0.11.1
=======

Major Changes
-------------

- Add changelog and fragments and document changelog process (https://github.com/ansible-collections/community.kubernetes/pull/131).

Minor Changes
-------------

- Add action groups for playbooks with module_defaults (https://github.com/ansible-collections/community.kubernetes/pull/107).
- Add requires_ansible version constraints to runtime.yml (https://github.com/ansible-collections/community.kubernetes/pull/126).
- Add sanity test ignore file for Ansible 2.11 (https://github.com/ansible-collections/community.kubernetes/pull/130).
- Add test for openshift apply bug (https://github.com/ansible-collections/community.kubernetes/pull/94).
- Add version_added to each new collection module (https://github.com/ansible-collections/community.kubernetes/pull/98).
- Check Python code using flake8 (https://github.com/ansible-collections/community.kubernetes/pull/123).
- Don't require project coverage check on PRs (https://github.com/ansible-collections/community.kubernetes/pull/102).
- Improve k8s Deployment and Daemonset wait conditions (https://github.com/ansible-collections/community.kubernetes/pull/35).
- Minor documentation fixes and use of FQCN in some examples (https://github.com/ansible-collections/community.kubernetes/pull/114).
- Remove action_groups_redirection entry from meta/runtime.yml (https://github.com/ansible-collections/community.kubernetes/pull/127).
- Remove deprecated ANSIBLE_METADATA field (https://github.com/ansible-collections/community.kubernetes/pull/95).
- Use FQCN in module docs and plugin examples (https://github.com/ansible-collections/community.kubernetes/pull/146).
- Use improved kubernetes diffs where possible (https://github.com/ansible-collections/community.kubernetes/pull/105).
- helm - add 'atomic' option (https://github.com/ansible-collections/community.kubernetes/pull/115).
- helm - minor code refactoring (https://github.com/ansible-collections/community.kubernetes/pull/110).
- helm_info and helm_repository - minor code refactor (https://github.com/ansible-collections/community.kubernetes/pull/117).
- k8s - Handle set object retrieved from lookup plugin (https://github.com/ansible-collections/community.kubernetes/pull/118).

Bugfixes
--------

- Fix suboption docs structure for inventory plugins (https://github.com/ansible-collections/community.kubernetes/pull/103).
- Handle invalid kubeconfig parsing error (https://github.com/ansible-collections/community.kubernetes/pull/119).
- Make sure Service changes run correctly in check_mode (https://github.com/ansible-collections/community.kubernetes/pull/84).
- k8s_info - remove unneccessary k8s_facts deprecation notice (https://github.com/ansible-collections/community.kubernetes/pull/97).
- k8s_scale - Fix scale wait and add tests (https://github.com/ansible-collections/community.kubernetes/pull/100).
- raw - handle condition when definition is none (https://github.com/ansible-collections/community.kubernetes/pull/139).

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
