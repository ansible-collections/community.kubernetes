[![Build Status](https://travis-ci.org/ansible/ansible-kubernetes-modules.svg?branch=master)](https://travis-ci.org/ansible/ansible-kubernetes-modules)

# ansible-kubernetes-modules

Provides access to the latest release of the K8s modules. 

Include this role in a playbook, and any other plays, roles, and includes will have access to the modules.

The modules are found in the [library folder](./library). Each has full documentation for parameters and the returned data structure. However, not all modules will include examples, only those where [test data](https://github.com/openshift/openshift-restclient-python/tree/master/openshift/ansiblegen/examples) has been created.

If you find an issue with a particular module, or have suggestions, please file an issue at the [OpenShift Rest Client repo](https://github.com/openshift/openshift-restclient-python/issues).

For convenience, the `k8s_common.py` and `openshift_common.py` modules are included under [module_utils](./module_utils). It is not currenlty part of an official Ansible release, but it is part of Ansible, and lives in the `devel` branch. In the meantime, if you happen to find a bug, or would like to make a change, please open issues and submit pull requests at the [Ansible repo](https://github.com/ansible/ansible).

## Requirements

- Ansible
- [OpenShift Rest Client](https://github.com/openshift/openshift-restclient-python) installed on the host where the modules will execute.

## Installation and use

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

## Authenticating with the API

The modules interact directly with the Kubernetes or OpenShift API. It is not required that you have the `kubectl` or `oc` CLI tool installed. 

### Module parameters 

The OpenShift rest client requires a Kubernetes config file. Use the following options to control where it looks for the file, and the context it uses to authenticate with the API:

kubeconfig
> The default path to the config file is `~/.kube/config`. Use to pass an alternate file path.

context
> Name of the configuration context to use for authentication. If not specified, the current, active contexts is used.

Use the following parameters to ovrride the settings found in the config file:

host
> Provide the URL to the API server.

ssl_ca_cert
> Path to the Certificate Authority certificate file.

cert_file
> Path to the server certificate file.

key_file
> Path to the private key file.

api_key
> API token.

verify_ssl
> Set to *true* or *false*. If *false*, SSL verification will not be enforced. 

### Environment Variables

Rather than pass the authentication settings as parameters to individual modules,  you can pass the information using environment variables. The name of the environment variables is *K8S_AUTH_* followed by the variable name in uppercase. For example, *key_file* would be *K8S_AUTH_KEY_FILE*

## Role Variables

install_python_requirements
> Set to true, if you want the OpenShift Rest Client installed. Defaults to false. Will install via `pip`.

virtualenv
> Provide the name of a virtualenv to use when installing `pip` packages.

## License

Apache V2
