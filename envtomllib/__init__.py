__version__ = '0.2.0'

import tomllib
import os
import re

RE_ENV_VAR = r'^\$\{([a-zA-Z_][a-zA-Z0-9_]+)\}$'
RE_INLINE_TABLE_PATTERN = r'^\{(.+)\}$'


class EnvVarDoesNotExist(Exception):
    pass


def env_replace(x):
    env_var = x.group(1)
    print("env_var", env_var)
    try:
        return os.environ[env_var]
    except KeyError as error:
        print(error)
        raise EnvVarDoesNotExist(f'Enviromnet variable {
                                 env_var} does not exist.')


def convert_inline_table_toml_str(value: str):
    helper_str = f"tmp = {value}"
    print("conversion inline table", helper_str)
    test = tomllib.loads(helper_str)['tmp']
    print(test)
    return test


def type_env_value(value: str):
    print("typed env value:", value)

    try:
        return float(value)
    except ValueError:
        pass

    try:
        return int(value)
    except ValueError:
        pass

    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    if re.match(RE_INLINE_TABLE_PATTERN, value):
        print("much inline table pattern", value)
        try:
            return convert_inline_table_toml_str(value)
        except tomllib.TOMLDecodeError:
            pass

    return value


def process_value(val: str):
    print("processing value:", val)
    if re.match(RE_ENV_VAR, val):
        r = re.sub(RE_ENV_VAR, env_replace, val)
        return type_env_value(r)
    else:
        return val


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
