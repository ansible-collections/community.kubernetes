# Kubernetes Collection for Ansible

[![CI](https://github.com/ansible-collections/kubernetes/workflows/CI/badge.svg?branch=master)](https://github.com/ansible-collections/kubernetes/actions)

This repo hosts the `community.kubernetes` Ansible Collection.

The collection includes a variety of Ansible content to help automate the management of applications in Kubernetes and OpenShift clusters, as well as the provisioning and maintenance of clusters themselves.

## Included content

Click on the name of a plugin or module to view that content's documentation:

  - **Connection Plugins**:
    - [kubectl](https://docs.ansible.com/ansible/latest/plugins/connection/kubectl.html)
  - **Filter Plugins**:
    - [k8s_config_resource_name](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#kubernetes-filters)
  - **Inventory Source**:
    - [k8s](https://docs.ansible.com/ansible/latest/plugins/inventory/k8s.html)
    - [openshift](https://docs.ansible.com/ansible/latest/plugins/inventory/openshift.html)
  - **Lookup Plugins**:
    - [k8s](https://docs.ansible.com/ansible/latest/plugins/lookup/k8s.html)
  - **Modules**:
    - [k8s](https://docs.ansible.com/ansible/latest/modules/k8s_module.html)
    - [k8s_auth](https://docs.ansible.com/ansible/latest/modules/k8s_auth_module.html)
    - [k8s_info](https://docs.ansible.com/ansible/latest/modules/k8s_info_module.html)
    - [k8s_scale](https://docs.ansible.com/ansible/latest/modules/k8s_scale_module.html)
    - [k8s_service](https://docs.ansible.com/ansible/latest/modules/k8s_service_module.html)

## Installation and Usage

### Installing the Collection from Ansible Galaxy

Before using the Kuberentes collection, you need to install it with the Ansible Galaxy CLI:

    ansible-galaxy collection install community.kubernetes

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: community.kubernetes
    version: 0.9.0
```

### Installing the OpenShift Python Library

Content in this collection requires the [OpenShift Python client](https://pypi.org/project/openshift/) to interact with Kubernetes' APIs. You can install it with:

    pip3 install openshift

### Using modules from the Kubernetes Collection in your playbooks

You can either call modules by their Fully Qualified Collection Namespace (FQCN), like `community.kubernetes.k8s_info`, or you can call modules by their short name if you list the `community.kubernetes` collection in the playbook's `collections`, like so:

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

    - name: Ensure the myapp Service exists in the myapp Namespace.
      k8s:
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
      k8s_info:
        kind: Service
        namespace: myapp
      register: myapp_services

    - name: Display number of Services in the myapp namespace.
      debug:
        var: myapp_services.resources | count

```

For documentation on how to use individual modules and other content included in this collection, please see the links in the 'Included content' section earlier in this README.

## Testing and Development

If you want to develop new content for this collection or improve what's already here, the easiest way to work on the collection is to clone it into one of the configured [`COLLECTIONS_PATHS`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths), and work on it there.

The `tests` directory contains configuration for running sanity and integration tests using [`ansible-test`](https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html).

You can run the collection's test suites with the commands:

    ansible-test sanity --docker -v --color
    ansible-test integration --docker -v --color

## More Information

For more information about Ansible's Kubernetes integration, join the `#ansible-community` channel on Freenode IRC, and browse the resources in the [Kubernetes Working Group](https://github.com/ansible/community/wiki/Kubernetes) Community wiki page.

## License

GNU General Public License v3.0 or later

See LICENCE to see the full text.
