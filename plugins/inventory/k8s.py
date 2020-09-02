# Copyright (c) 2018 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: k8s
    plugin_type: inventory
    author:
      - Chris Houseknecht <@chouseknecht>
      - Fabian von Feilitzsch <@fabianvf>

    short_description: Kubernetes (K8s) inventory source

    description:
      - Fetch containers in pods for one or more clusters.
      - Groups by cluster name, namespace, namespace_services, namespace_pods, and labels.
      - Uses the kubectl connection plugin to access the Kubernetes cluster.
      - Uses k8s.(yml|yaml) YAML configuration file to set parameter values.

    options:
      plugin:
         description: token that ensures this is a source file for the 'k8s' plugin.
         required: True
         choices: ['community.kubernetes.k8s', 'k8s']
      connections:
          description:
          - Optional list of cluster connection settings. If no connections are provided, the default
            I(~/.kube/config) and active context will be used, and objects will be returned for all namespaces
            the active user is authorized to access.
          suboptions:
              name:
                  description:
                  - Optional name to assign to the cluster. If not provided, a name is constructed from the server
                    and port.
              kubeconfig:
                  description:
                  - Path to an existing Kubernetes config file. If not provided, and no other connection
                    options are provided, the OpenShift client will attempt to load the default
                    configuration file from I(~/.kube/config.json). Can also be specified via K8S_AUTH_KUBECONFIG
                    environment variable.
              context:
                  description:
                  - The name of a context found in the config file. Can also be specified via K8S_AUTH_CONTEXT environment
                    variable.
              host:
                  description:
                  - Provide a URL for accessing the API. Can also be specified via K8S_AUTH_HOST environment variable.
              api_key:
                  description:
                  - Token used to authenticate with the API. Can also be specified via K8S_AUTH_API_KEY environment
                    variable.
              username:
                  description:
                  - Provide a username for authenticating with the API. Can also be specified via K8S_AUTH_USERNAME
                    environment variable.
              password:
                  description:
                  - Provide a password for authenticating with the API. Can also be specified via K8S_AUTH_PASSWORD
                    environment variable.
              client_cert:
                  description:
                  - Path to a certificate used to authenticate with the API. Can also be specified via K8S_AUTH_CERT_FILE
                    environment variable.
                  aliases: [ cert_file ]
              client_key:
                  description:
                  - Path to a key file used to authenticate with the API. Can also be specified via K8S_AUTH_KEY_FILE
                    environment variable.
                  aliases: [ key_file ]
              ca_cert:
                  description:
                  - Path to a CA certificate used to authenticate with the API. Can also be specified via
                    K8S_AUTH_SSL_CA_CERT environment variable.
                  aliases: [ ssl_ca_cert ]
              validate_certs:
                  description:
                  - "Whether or not to verify the API server's SSL certificates. Can also be specified via
                    K8S_AUTH_VERIFY_SSL environment variable."
                  type: bool
                  aliases: [ verify_ssl ]
              namespaces:
                  description:
                  - List of namespaces. If not specified, will fetch all containers for all namespaces user is authorized
                    to access.

    requirements:
    - "python >= 2.7"
    - "openshift >= 0.6"
    - "PyYAML >= 3.11"
"""

EXAMPLES = """
# File must be named k8s.yaml or k8s.yml

# Authenticate with token, and return all pods and services for all namespaces
plugin: community.kubernetes.k8s
connections:
  - host: https://192.168.64.4:8443
    api_key: xxxxxxxxxxxxxxxx
    validate_certs: false

# Use default config (~/.kube/config) file and active context, and return objects for a specific namespace
plugin: community.kubernetes.k8s
connections:
  - namespaces:
    - testing

# Use a custom config file, and a specific context.
plugin: community.kubernetes.k8s
connections:
  - kubeconfig: /path/to/config
    context: 'awx/192-168-64-4:8443/developer'
"""

import re
import json

from ansible.errors import AnsibleError
from ansible_collections.community.kubernetes.plugins.module_utils.common import (
    K8sAnsibleMixin,
    HAS_K8S_MODULE_HELPER,
    k8s_import_exception,
    get_api_client,
)
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable

try:
    from openshift.dynamic.exceptions import DynamicApiError
except ImportError:
    pass


def format_dynamic_api_exc(exc):
    if exc.body:
        if exc.headers and exc.headers.get("Content-Type") == "application/json":
            message = json.loads(exc.body).get("message")
            if message:
                return message
        return exc.body
    else:
        return "%s Reason: %s" % (exc.status, exc.reason)


class K8sInventoryException(Exception):
    pass


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable, K8sAnsibleMixin):
    NAME = "community.kubernetes.k8s"

    connection_plugin = "community.kubernetes.kubectl"
    transport = "kubectl"

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)
        cache_key = self._get_cache_prefix(path)
        config_data = self._read_config_data(path)
        self.setup(config_data, cache, cache_key)

    def setup(self, config_data, cache, cache_key):
        connections = config_data.get("connections")

        if not HAS_K8S_MODULE_HELPER:
            raise K8sInventoryException(
                "This module requires the OpenShift Python client. Try `pip install openshift`. Detail: {0}".format(
                    k8s_import_exception
                )
            )

        source_data = None
        if cache and cache_key in self._cache:
            try:
                source_data = self._cache[cache_key]
            except KeyError:
                pass

        if not source_data:
            self.fetch_objects(connections)

    def fetch_objects(self, connections):
        if not connections:
            connections = [{}]

        if not isinstance(connections, list):
            raise K8sInventoryException("Expecting connections to be a list.")

        for connection in connections:
            if not isinstance(connection, dict):
                raise K8sInventoryException("Expecting connection to be a dictionary.")
            client = self.get_api_client(**connection)
            name = connection.get(
                "name", self.get_default_host_name(client.configuration.host)
            )
            if connection.get("namespaces"):
                namespaces = connection["namespaces"]
            else:
                namespaces = self.get_available_namespaces(client)

            sanitized_name = self.sanitize(name)
            self.inventory.add_group(sanitized_name)
            for namespace in namespaces:
                namespace_group = self.sanitize("namespace_{0}".format(namespace))

                self.inventory.add_group(namespace_group)
                self.inventory.add_child(sanitized_name, namespace_group)

                self.get_pods_for_namespace(client, name, namespace, namespace_group)
                self.get_pods_from_parents(client, name, namespace, namespace_group)

    @staticmethod
    def get_default_host_name(host):
        return (
            host.replace("https://", "")
            .replace("http://", "")
            .replace(".", "-")
            .replace(":", "_")
        )

    @staticmethod
    def sanitize(name):
        if name[:1].isdigit():
            name = "_" + name
        return re.sub("[^0-9a-zA-Z_]", "_", name)

    def get_available_namespaces(self, client):
        v1_namespace = client.resources.get(api_version="v1", kind="Namespace")
        try:
            obj = v1_namespace.get()
        except DynamicApiError as exc:
            self.display.debug(exc)
            raise K8sInventoryException(
                "Error fetching Namespace list: %s" % format_dynamic_api_exc(exc)
            )
        return [namespace.metadata.name for namespace in obj.items]

    def get_pods_from_parents(self, client, name, namespace, namespace_group):

        v1_pods = client.resources.get(api_version="v1", kind="Pod")
        for kind in ["Deployment", "Daemonset", "StatefulSet"]:
            try:
                resource = client.resources.get(api_version="apps/v1", kind=kind)
                instances = resource.get(namespace=namespace)
            except Exception:
                # TODO Could be expected due to RBAC or odd cluster, maybe should log a warning or something?
                continue
            for instance in instances.items:
                try:
                    label_selector = ",".join(self.extract_selectors(instance))
                except ValueError:
                    # TODO Maybe a warning here as well?
                    continue

                if not label_selector:
                    # This shouldn't be possible but better safe than sorry
                    continue

                try:
                    pods = v1_pods.get(
                        namespace=namespace, label_selector=label_selector
                    )
                except DynamicApiError as exc:
                    self.display.debug(exc)
                    raise K8sInventoryException(
                        "Error fetching Pod list: %s" % format_dynamic_api_exc(exc)
                    )

                instance_group = self.sanitize(
                    "{0}_{1}_{2}".format(
                        namespace_group, kind.lower(), instance.metadata.name
                    )
                )
                self.inventory.add_group(instance_group)
                self.inventory.add_child(namespace_group, instance_group)

                for pod in pods.items:
                    self.add_pod_to_groups(pod, [instance_group])

    def get_pods_for_namespace(self, client, name, namespace, namespace_group):
        v1_pod = client.resources.get(api_version="v1", kind="Pod")
        try:
            obj = v1_pod.get(namespace=namespace)
        except DynamicApiError as exc:
            self.display.debug(exc)
            raise K8sInventoryException(
                "Error fetching Pod list: %s" % format_dynamic_api_exc(exc)
            )

        for pod in obj.items:
            pod_groups = [namespace_group]
            if pod.metadata.labels:
                # create a group for each label_value
                for key, value in pod.metadata.labels:
                    group_name = self.sanitize("label_{0}_{1}".format(key, value))
                    if group_name not in pod_groups:
                        pod_groups.append(group_name)
                    self.inventory.add_group(group_name)
            self.add_pod_to_groups(pod, pod_groups)

    def add_pod_to_groups(self, pod, pod_groups):
        # If the pod has no running containers or has permanently terminated we should skip
        if not pod.status.containerStatuses or pod.status.phase not in [
            "Pending",
            "Running",
        ]:
            return

        pod_name = pod.metadata.name
        namespace = pod.metadata.namespace
        pod_annotations = (
            dict(pod.metadata.annotations) if pod.metadata.annotations else {}
        )
        pod_labels = dict(pod.metadata.labels) if pod.metadata.labels else {}

        for container in pod.status.containerStatuses:
            # If the container has permanently terminated we should skip
            if container.state.terminated:
                continue
            # add each pod_container to the namespace group, and to each label_value group
            container_name = "{0}_{1}".format(pod.metadata.name, container.name)
            self.inventory.add_host(container_name)
            if pod_groups:
                for group in pod_groups:
                    self.inventory.add_child(group, container_name)

            # Add hostvars
            self.inventory.set_variable(container_name, "object_type", "pod")
            self.inventory.set_variable(container_name, "labels", pod_labels)
            self.inventory.set_variable(container_name, "annotations", pod_annotations)
            self.inventory.set_variable(
                container_name, "cluster_name", pod.metadata.clusterName
            )
            self.inventory.set_variable(
                container_name, "pod_node_name", pod.spec.nodeName
            )
            self.inventory.set_variable(container_name, "pod_name", pod.spec.name)
            self.inventory.set_variable(
                container_name, "pod_host_ip", pod.status.hostIP
            )
            self.inventory.set_variable(container_name, "pod_phase", pod.status.phase)
            self.inventory.set_variable(container_name, "pod_ip", pod.status.podIP)
            self.inventory.set_variable(
                container_name, "pod_self_link", pod.metadata.selfLink
            )
            self.inventory.set_variable(
                container_name, "pod_resource_version", pod.metadata.resourceVersion
            )
            self.inventory.set_variable(container_name, "pod_uid", pod.metadata.uid)
            self.inventory.set_variable(
                container_name, "container_name", container.image
            )
            self.inventory.set_variable(
                container_name, "container_image", container.image
            )
            if container.state.running:
                self.inventory.set_variable(
                    container_name, "container_state", "Running"
                )
            if container.state.waiting:
                self.inventory.set_variable(
                    container_name, "container_state", "Waiting"
                )
            self.inventory.set_variable(
                container_name, "container_ready", container.ready
            )
            self.inventory.set_variable(container_name, "ansible_remote_tmp", "/tmp/")
            self.inventory.set_variable(
                container_name, "ansible_connection", self.connection_plugin
            )
            self.inventory.set_variable(
                container_name, "ansible_{0}_pod".format(self.transport), pod_name
            )
            self.inventory.set_variable(
                container_name,
                "ansible_{0}_container".format(self.transport),
                container.name,
            )
            self.inventory.set_variable(
                container_name,
                "ansible_{0}_namespace".format(self.transport),
                namespace,
            )
