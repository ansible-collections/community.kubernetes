# ansible-kubernetes-modules

Provides access to the latest pre-release K8s modules. 

Include this role in a playbook, and any other plays, roles, and includes will have access to the modules.

The modules are found in the [library folder](./library). Each has full documentation for parameters and the returned data structure. However, not all modules will include examples, only those where [test data](https://github.com/openshift/openshift-restclient-python/tree/master/openshift/ansiblegen/examples) has been created.

If you find an issue with a particular module, or have suggestions, please file an issue at the [OpenShift Rest Client repo](https://github.com/openshift/openshift-restclient-python/issues).

Requirements
------------

- Ansible installed from source
- [OpenShift Rest Client](https://github.com/openshift/openshift-restclient-python) installed on the host where the modules will execute.

Installation and use
--------------------

Use the Galaxy client to install the role:

```
$ ansible-galaxy install ansible.kubernetes-modules
```

Once installed, add it to a playbook:

```
---
- hosts: localhost
  remote_user: root
  roles:
    - role: ansible.kubernetes-modules
      install_python_requirements: no
    - role: hello-world
```

Because the role is referenced, the `hello-world` role is able to deploy an applicatoin using the K8s modules. To see contents of the actual role, check in the [tests/roles](./tests/roles) folder.

Authenticating with the API
---------------------------
The modules interact directly with the Kubernetes or OpenShift API. It is not required that you have the `kubectl` or `oc` CLI tool installed. 

By default the OpenShift Rest Client will look for `~/.kube/config`, and if found, connect using the active context. You can override the location of the file using the `kubeconfig` parameter, and the context, using the `context` parameter.

Basic authentication is also supported using the `username` and `password` options. You can override the URL using the `host` parameter. Certificate authentication works through the `ssl_ca_cert`, `cert_file`, and `key_file` parameters, and for token authentication, use the `api_key` parameter.

To disable SSL certificate verification, set `verify_ssl` to false.


Role Variables
--------------

install_python_requirements
> Set to true, if you want the OpenShift Rest Client installed. Defaults to false. Will install via `pip`.

virtualenv
> Provide the name of a virtualenv to use when installing `pip` packages.

License
-------

Apache V2

