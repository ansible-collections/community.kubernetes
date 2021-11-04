# Kubernetes Collection for Ansible

**IMPORTANT**
The `community.kubernetes` collection is being renamed to [`kubernetes.core`](https://github.com/ansible-collections/kubernetes.core). As of version 2.0.0, the collection has been replaced by deprecated redirects for all content to `kubernetes.core`. If you are using FQCNs starting with `community.kubernetes`, please update them to `kubernetes.core`.

This repo hosts the `community.kubernetes` (a.k.a. [`kubernetes.core`](https://github.com/ansible-collections/kubernetes.core)) Ansible Collection.

The collection includes a variety of Ansible content to help automate the management of applications in Kubernetes and OpenShift clusters, as well as the provisioning and maintenance of clusters themselves.

## Installation and Usage

### Installing the Collection from Ansible Galaxy

Before using the Kubernetes collection, you need to install it with the Ansible Galaxy CLI:

    ansible-galaxy collection install community.kubernetes

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: community.kubernetes
    version: 2.0.1
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

See [Contributing to community.kubernetes](CONTRIBUTING.md).

### Testing with `ansible-test`

The `tests` directory contains configuration for running sanity and integration tests using [`ansible-test`](https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html).

You can run the collection's test suites with the commands:

    make test-sanity
    make test-integration

### Testing with `molecule`

There are also integration tests in the `molecule` directory which are meant to be run against a local Kubernetes cluster, e.g. using [KinD](https://kind.sigs.k8s.io) or [Minikube](https://minikube.sigs.k8s.io). To setup a local cluster using KinD and run Molecule:

    kind create cluster
    make test-molecule

## Publishing New Versions

Releases are automatically built and pushed to Ansible Galaxy for any new tag. Before tagging a release, make sure to do the following:

  1. Update the version in the following places:
     1. The `version` in `galaxy.yml`
     2. This README's `requirements.yml` example
     3. The `DOWNSTREAM_VERSION` in `utils/downstream.sh`
     4. The `VERSION` in `Makefile`
  2. Update the CHANGELOG:
     1. Make sure you have [`antsibull-changelog`](https://pypi.org/project/antsibull-changelog/) installed.
     2. Make sure there are fragments for all known changes in `changelogs/fragments`.
     3. Run `antsibull-changelog release`.
  3. Commit the changes and create a PR with the changes. Wait for tests to pass, then merge it once they have.
  4. Tag the version in Git and push to GitHub.
  5. Manually build and release the `kubernetes.core` collection (see following section).

After the version is published, verify it exists on the [Kubernetes Collection Galaxy page](https://galaxy.ansible.com/community/kubernetes).

### Publishing `kubernetes.core`

Until the contents of repository are moved into a new `kubernetes.core` repository on GitHub, this repository is the source of both the `kubernetes.core` and `community.kubernetes` repositories on Ansible Galaxy.

To publish the `kubernetes.core` collection on Ansible Galaxy, do the following:

  1. Run `make downstream-release` (on macOS, add `LC_ALL=C` before the command).

The process for uploading a supported release to Automation Hub is documented separately.

## More Information

For more information about Ansible's Kubernetes integration, join the `#ansible-kubernetes` channel on [irc.libera.chat](https://libera.chat/), and browse the resources in the [Kubernetes Working Group](https://github.com/ansible/community/wiki/Kubernetes) Community wiki page.

## License

GNU General Public License v3.0 or later

See LICENCE to see the full text.
