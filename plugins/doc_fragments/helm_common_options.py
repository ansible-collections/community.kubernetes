# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Ansible Project
# Copyright: (c) 2020, Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Options for common Helm modules

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r'''
options:
  binary_path:
    description:
      - The path of a helm binary to use.
    required: false
    type: path
  context:
    description:
      - Helm option to specify which kubeconfig context to use.
      - If the value is not specified in the task, the value of environment variable C(K8S_AUTH_CONTEXT) will be used instead.
    type: str
    aliases: [ kube_context ]
  kubeconfig:
    description:
      - Helm option to specify kubeconfig path to use.
      - If the value is not specified in the task, the value of environment variable C(K8S_AUTH_KUBECONFIG) will be used instead.
    type: path
    aliases: [ kubeconfig_path ]
'''
