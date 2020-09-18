# Copyright (c) 2012-2014, Michael DeHaan <michael.dehaan@gmail.com>
# Copyright (c) 2017, Toshio Kuratomi <tkuraotmi@ansible.com>
# Copyright (c) 2020, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import copy
import traceback

from ansible.module_utils._text import to_text
from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError


class ActionModule(ActionBase):

    TRANSFERS_FILES = True

    def _ensure_invocation(self, result):
        # NOTE: adding invocation arguments here needs to be kept in sync with
        # any no_log specified in the argument_spec in the module.
        if 'invocation' not in result:
            if self._play_context.no_log:
                result['invocation'] = "CENSORED: no_log is set"
            else:
                result['invocation'] = self._task.args.copy()
                result['invocation']['module_args'] = self._task.args.copy()

        return result

    def run(self, tmp=None, task_vars=None):
        ''' handler for k8s options '''
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        new_module_args = copy.deepcopy(self._task.args)
        kubeconfig = self._task.args.get('kubeconfig', None)
        # find the file in the expected search path
        if kubeconfig:
            try:
                # find in expected paths
                kubeconfig = self._find_needle('files', kubeconfig)
            except AnsibleError as e:
                result['failed'] = True
                result['msg'] = to_text(e)
                result['exception'] = traceback.format_exc()
                return result

        if kubeconfig:
            # decrypt kubeconfig found
            actual_file = self._loader.get_real_file(kubeconfig, decrypt=True)
            new_module_args['kubeconfig'] = actual_file

        # find the file in the expected search path
        src = self._task.args.get('src', None)
        if src:
            try:
                # find in expected paths
                src = self._find_needle('files', src)
            except AnsibleError as e:
                result['failed'] = True
                result['msg'] = to_text(e)
                result['exception'] = traceback.format_exc()
                return result

        if src:
            new_module_args['src'] = src

        # Execute the k8s_* module.
        module_return = self._execute_module(module_name=self._task.action, module_args=new_module_args, task_vars=task_vars)

        # Delete tmp path
        self._remove_tmp_path(self._connection._shell.tmpdir)

        result.update(module_return)

        return self._ensure_invocation(result)
