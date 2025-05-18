__version__ = '0.0.1'

import tomllib
import os
import re
import warnings


RE_ENV_VAR = r'^\$\{([a-zA-Z_][a-zA-Z0-9_]+)\}$'
RE_INLINE_TABLE_PATTERN = r'^\{(.+)\}$'
RE_LIST_PATTERN = r'^\[(.+)\]$'


class EnvVarDoesNotExist(Exception):
    pass


def env_replace(x):
    env_var = x.group(1)
    print('env_var', env_var)
    try:
        return os.environ[env_var]
    except KeyError as error:
        print(error)
        raise EnvVarDoesNotExist(f'Environmental variable {
                                 env_var} does no exist.')


def replace_list_pattern(x):
    return x.group(1)


def convert_inline_table_toml_str(value: str):
    helper_str = f'tmp = {value}'
    return tomllib.loads(helper_str)['tmp']


def convert_list_str(value: str):
    list_content = re.sub(RE_LIST_PATTERN, r'\1', value)
    list_content = re.sub(r'\s+', '', list_content)
    return [type_value(list_value) for list_value in list_content.split(',')]


def type_value(value: str):
    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    if re.match(RE_LIST_PATTERN, value):
        return convert_list_str(value)

    if re.match(RE_INLINE_TABLE_PATTERN, value):
        try:
            return convert_inline_table_toml_str(value)
        except tomllib.TOMLDecodeError:
            pass

    return value


def process_value(val: str):
    print("processing value:", val)
    if not re.match(RE_ENV_VAR, val):
        return val

    try:
        r = re.sub(RE_ENV_VAR, env_replace, val)
        return type_value(r)
    except EnvVarDoesNotExist as e:
        warnings.warn(f'WARNING: {e}')
        return None


def process(item):
    iter_ = None
    if isinstance(item, dict):
        iter_ = item.items()
    elif isinstance(item, list):
        iter_ = enumerate(item)

    for i, val in iter_:
        if isinstance(val, (dict, list)):
            process(val)
        elif isinstance(val, str):
            item[i] = process_value(val)


def load(*args, **kwargs):
    data = tomllib.load(*args, **kwargs)
    process(data)
    return data


def loads(*args, **kwargs):
    data = tomllib.loads(*args, **kwargs)
    process(data)
    return data
