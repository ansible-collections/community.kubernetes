# Kubernetes Collection Changes

## 0.11.0

### New Features

  - PR #61: Add `helm`, `helm_info`, and `helm_repository` modules.
  - PR #81: Rename repository to `community.kubernetes`.

### Bug Fixes

  - PR #78: Update GitHub Actions workflow for better CI stability.
  - PR #69: k8s_log no longer attempts to parse log as JSON.
  - PR #85: Make sure extra files are not included in built collection.

## 0.10.0

### New Features

  - PR #14: Add `k8s_exec` module for executing commands on pods via Kubernetes API.
  - PR #16: Add `k8s_log` module for retrieving pod logs.
  - Issue #49, PR #55: Add `persist_config` option for persisting refreshed tokens.

### Security Fixes

  - PR #51: Warn about disclosure when using options like `kubectl_password`, `kubectl_extra_args`, and `kubectl_token` to pass data through to the command line using the `kubectl` connection plugin.

### Bug Fixes

  - Issue #13: Fix argspec for 'elements'.
  - Issue #33, PR #34: Fix argspec in `k8s_service`.
  - Issue #10, PR #22: Test collection in a Kind cluster in CI using Molecule.
  - PR #52: Documentation fix in `kubectl.py`.
  - PR #54: Add exception handling when retrieving k8s client.
  - PR #56: Use from_yaml filter with lookup examples in `k8s` module documentation examples.

## 0.9.0

  - Initial migration of Kubernetes content from Ansible core (2.9 / devel), including content:
    - **Connection Plugins**:
      - `kubectl`
    - **Filter Plugins**:
      - `k8s_config_resource_name`
    - **Inventory Source**:
      - `k8s`
      - `openshift`
    - **Lookup Plugins**:
      - `k8s`
    - **Modules**:
      - `k8s`
      - `k8s_auth`
      - `k8s_info`
      - `k8s_scale`
      - `k8s_service`
