# Kubernetes Collection for Ansible

[![CI](https://github.com/ansible-collections/community.kubernetes/workflows/CI/badge.svg?event=push)](https://github.com/ansible-collections/community.kubernetes/actions) [![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/community.kubernetes)](https://codecov.io/gh/ansible-collections/community.kubernetes)

This repo hosts the `community.kubernetes` Ansible Collection.

The collection includes a variety of Ansible content to help automate the management of applications in Kubernetes and OpenShift clusters, as well as the provisioning and maintenance of clusters themselves.

## Included content

Click on the name of a plugin or module to view that content's documentation:

  - **Connection Plugins**:
    - [kubectl](https://docs.ansible.com/ansible/2.10/collections/community/kubernetes/kubectl_connection.html)
  - **Filter Plugins**:
    - [k8s_config_resource_name](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#kubernetes-filters)
  - **Inventory Source**:
    - [k8s](https://docs.ansible.com/ansible/2.10/collections/community/kubernetes/k8s_inventory.html)
    - [openshift](https://docs.ansible.com/ansible/2.10/collections/community/kubernetes/openshift_inventory.html)
  - **Lookup Plugins**:
    - [k8s](https://docs.ansible.com/ansible/2.10/collections/community/kubernetes/k8s_lookup.html)
  - **Modules**:
    - [k8s](https://docs.ansible.com/ansible/2.10/collections/community/kubernetes/k8s_module.html)
    - [k8s_auth](https://docs.ansible.com/ansible/2.10/collections/community/kubernetes/k8s_auth_module.html)
    - [k8s_exec](https://docs.ansible.com/ansible/2.10/collections/community/kubernetes/k8s_exec_module.html)
    - [k8s_info](https://docs.ansible.com/ansible/2.10/collections/community/kubernetes/k8s_info_module.html)
    - [k8s_log](https://docs.ansible.com/ansible/2.10/collections/community/kubernetes/k8s_log_module.html)
    - [k8s_scale](https://docs.ansible.com/ansible/2.10/collections/community/kubernetes/k8s_scale_module.html)
    - [k8s_service](https://docs.ansible.com/ansible/2.10/collections/community/kubernetes/k8s_service_module.html)
    - [helm](https://docs.ansible.com/ansible/2.10/collections/community/kubernetes/helm_module.html)
    - [helm_info](https://docs.ansible.com/ansible/2.10/collections/community/kubernetes/helm_info_module.html)
    - [helm_plugin](https://github.com/ansible-collections/community.kubernetes/blob/main/plugins/modules/helm_plugin.py)
    - [helm_plugin_info](https://github.com/ansible-collections/community.kubernetes/blob/main/plugins/modules/helm_plugin_info.py)
    - [helm_repository](https://docs.ansible.com/ansible/2.10/collections/community/kubernetes/helm_repository_module.html)

## Installation and Usage

### Installing the Collection from Ansible Galaxy

Before using the Kuberentes collection, you need to install it with the Ansible Galaxy CLI:

    ansible-galaxy collection install community.kubernetes

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: community.kubernetes
    version: 1.0.0
```

### Installing the OpenShift Python Library

Content in this collection requires the [OpenShift Python client](https://pypi.org/project/openshift/) to interact with Kubernetes' APIs. You can install it with:

    pip3 install openshift

### Using modules from the Kubernetes Collection in your playbooks

It's preferable to use content in this collection using their Fully Qualified Collection Namespace (FQCN), for example `community.kubernetes.k8s_info`:

```yaml
---
- hosts: localhost
  gather_facts: false
  connection: local

  tasks:
    - name: Ensure the myapp Namespace exists.
      community.kubernetes.k8s:
        api_version: v1
        kind: Namespace
        name: myapp
        state: present

    - name: Ensure the myapp Service exists in the myapp Namespace.
      community.kubernetes.k8s:
        state: present
        definition:
          apiVersion: v1
          kind: Service
          metadata:
            name: myapp
            namespace: myapp
          spec:
            type: LoadBalancer
            ports:
            - port: 8080
              targetPort: 8080
            selector:
              app: myapp

    - name: Get a list of all Services in the myapp namespace.
      community.kubernetes.k8s_info:
        kind: Service
        namespace: myapp
      register: myapp_services

    - name: Display number of Services in the myapp namespace.
      debug:
        var: myapp_services.resources | count
```

If upgrading older playbooks which were built prior to Ansible 2.10 and this collection's existence, you can also define `collections` in your play and refer to this collection's modules as you did in Ansible 2.9 and below, as in this example:

```yaml
---
- hosts: localhost
  gather_facts: false
  connection: local

  collections:
    - community.kubernetes

  tasks:
    - name: Ensure the myapp Namespace exists.
      k8s:
        api_version: v1
        kind: Namespace
        name: myapp
        state: present
```

For documentation on how to use individual modules and other content included in this collection, please see the links in the 'Included content' section earlier in this README.

## Testing and Development

If you want to develop new content for this collection or improve what's already here, the easiest way to work on the collection is to clone it into one of the configured [`COLLECTIONS_PATHS`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths), and work on it there.

### Testing with `ansible-test`

The `tests` directory contains configuration for running sanity and integration tests using [`ansible-test`](https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html).

You can run the collection's test suites with the commands:

    ansible-test sanity --docker -v --color
    ansible-test integration --docker -v --color

### Testing with `molecule`

There are also integration tests in the `molecule` directory which are meant to be run against a local Kubernetes cluster, e.g. using [KinD](https://kind.sigs.k8s.io) or [Minikube](https://minikube.sigs.k8s.io). To run the tests, set up a local cluster, then run Molecule:

    kind create cluster
    molecule test

## Publishing New Versions

The current process for publishing new versions of the Kubernetes Collection is manual, and requires a user who has access to the `community.kubernetes` namespace on Ansible Galaxy to publish the build artifact. See [Issue #43](https://github.com/ansible-collections/community.kubernetes/issues/43) for progress in automating this process.

  1. Ensure you're running Ansible from devel, so the [`build_ignore` key](https://github.com/ansible/ansible/issues/67130) in `galaxy.yml` is used.
  1. Run `git clean -x -d -f` in this repository's directory to clean out any extra files which should not be included.
  1. Update `galaxy.yml` and this README's `requirements.yml` example with the new `version` for the collection.
  1. Update the CHANGELOG:
    1. Make sure you have [`antsibull-changelog`](https://pypi.org/project/antsibull-changelog/) installed.
    1. Make sure there are fragments for all known changes in `changelogs/fragments`.
    1. Run `antsibull-changelog release`.
  1. Commit the changes and create a PR with the changes. Wait for tests to pass, then merge it once they have.
  1. Tag the version in Git and push to GitHub.
  1. Run the following commands to build and release the new version on Galaxy:

     ```
     ansible-galaxy collection build
     ansible-galaxy collection publish ./community-kubernetes-$VERSION_HERE.tar.gz
     ```

After the version is published, verify it exists on the [Kubernetes Collection Galaxy page](https://galaxy.ansible.com/community/kubernetes).

## More Information

For more information about Ansible's Kubernetes integration, join the `#ansible-kubernetes` channel on Freenode IRC, and browse the resources in the [Kubernetes Working Group](https://github.com/ansible/community/wiki/Kubernetes) Community wiki page.

## License

GNU General Public License v3.0 or later

See LICENCE to see the full text.
