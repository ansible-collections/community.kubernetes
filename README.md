# ansible-kubernetes-modules

Provides access to the latest pre-release K8s modules. Include this role in a playbook, and any other plays or roles will have access to the modules.

The modules are found in the [library folder](./library). Each has full documentation for parameters and the returned data structure. However, not all modules will include examples, only those where [test data](https://github.com/openshift/openshift-restclient-python/tree/master/openshift/ansiblegen/examples) has been created.

If you find an issue with a particular module, or have suggestions, please file an issue [here](https://github.com/openshift/openshift-restclient-python/issues).

Requirements
------------

- Ansible installed from source
- [OpenShift Rest Client](https://github.com/openshift/openshift-restclient-python) installed on the host where the modules will execute.

Installation and use
--------------------

Use the Galaxy client to install the role:

```
$ ansible-galaxy install ansible.ansible-kubernetes-modules
```

Once installed, add it to a playbook:

```
---
- hosts: localhost
  remote_user: root
  roles:
    - role: ansible.ansible-kubernetes-modules
      install_python_requirements: no
    - role: hello-world
```

Because the role is referenced, the `hello-world` role is able to deploy an applicatoin using the K8s modules. To see contents of the actual role, check in the [tests/roles](./tests/roles) folder.

Role Variables
--------------

install_python_requirements
> Set to true, if you want the OpenShift Rest Client installed. Defaults to false. Will install via `pip`.

virtualenv
> Provide the name of a virtualenv to use when installing `pip` packages.

License
-------

Apache V2

