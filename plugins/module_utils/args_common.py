from __future__ import (absolute_import, division, print_function)

from ansible.module_utils.six import string_types

__metaclass__ = type


def list_dict_str(value):
    if isinstance(value, (list, dict, string_types)):
        return value
    raise TypeError


AUTH_ARG_SPEC = {
    'kubeconfig': {
        'type': 'path',
    },
    'context': {},
    'host': {},
    'api_key': {
        'no_log': True,
    },
    'username': {},
    'password': {
        'no_log': True,
    },
    'validate_certs': {
        'type': 'bool',
        'aliases': ['verify_ssl'],
    },
    'ca_cert': {
        'type': 'path',
        'aliases': ['ssl_ca_cert'],
    },
    'client_cert': {
        'type': 'path',
        'aliases': ['cert_file'],
    },
    'client_key': {
        'type': 'path',
        'aliases': ['key_file'],
    },
    'proxy': {
        'type': 'str',
    },
    'persist_config': {
        'type': 'bool',
    },
}

WAIT_ARG_SPEC = dict(
    wait=dict(type='bool', default=False),
    wait_sleep=dict(type='int', default=5),
    wait_timeout=dict(type='int', default=120),
    wait_condition=dict(
        type='dict',
        default=None,
        options=dict(
            type=dict(),
            status=dict(default=True, choices=[True, False, "Unknown"]),
            reason=dict()
        )
    )
)

# Map kubernetes-client parameters to ansible parameters
AUTH_ARG_MAP = {
    'kubeconfig': 'kubeconfig',
    'context': 'context',
    'host': 'host',
    'api_key': 'api_key',
    'username': 'username',
    'password': 'password',
    'verify_ssl': 'validate_certs',
    'ssl_ca_cert': 'ca_cert',
    'cert_file': 'client_cert',
    'key_file': 'client_key',
    'proxy': 'proxy',
    'persist_config': 'persist_config',
}

NAME_ARG_SPEC = {
    'kind': {},
    'name': {},
    'namespace': {},
    'api_version': {
        'default': 'v1',
        'aliases': ['api', 'version'],
    },
}

COMMON_ARG_SPEC = {
    'state': {
        'default': 'present',
        'choices': ['present', 'absent'],
    },
    'force': {
        'type': 'bool',
        'default': False,
    },
}

RESOURCE_ARG_SPEC = {
    'resource_definition': {
        'type': list_dict_str,
        'aliases': ['definition', 'inline']
    },
    'src': {
        'type': 'path',
    },
}

ARG_ATTRIBUTES_BLACKLIST = ('property_path',)
