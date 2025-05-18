import pytest
from envtomllib import __version__
from envtomllib import load, loads
import os


SIMPLE_OUTPUT = {'x': 5, 'y': 10}
MORE_COMPLEX_OUTPUT = {
    'fruit': [
        {'name': 'apple', 'price': 2},
        {'name': 'orange', 'price': 3.14}
    ],
    'other': [
        {'name': 'laptop', 'price': 1000, 'sold': True},
        {'name': 'phone', 'price': 500}
    ]
}


def test_version():
    assert __version__ == '0.1.0'


def test_simple_load():
    with open('./tests/test_simple.toml', 'rb') as f:
        assert load(f) == SIMPLE_OUTPUT


def test_complex_load():
    with open('./tests/test_complex.toml', 'rb') as f:
        assert load(f) == MORE_COMPLEX_OUTPUT


def test_load_with_replace():
    os.environ['MY_CONFIG_VAR'] = "10"
    with open('./tests/test_simple_replacement.toml', 'rb') as f:
        assert load(f) == SIMPLE_OUTPUT


def test_loads():
    toml_str = """
x = 5
y = 10
"""
    assert loads(toml_str) == SIMPLE_OUTPUT


def test_loads_with_replace():
    os.environ['MY_CONFIG_VAR'] = "10"
    toml_str = """
x = 5
y = '${MY_CONFIG_VAR}'
"""
    assert loads(toml_str) == SIMPLE_OUTPUT


def test_loads_with_replace_str():
    os.environ['MY_STR_CONFIG_VAR'] = "Hello"
    toml_str = """
name = '${MY_STR_CONFIG_VAR}'
"""
    assert loads(toml_str) == {'name': 'Hello'}


def test_loads_with_replace_float():
    os.environ['MY_FLOAT_CONFIG_VAR'] = "3.14"
    toml_str = """
val = '${MY_FLOAT_CONFIG_VAR}'
"""
    assert loads(toml_str) == {'val': 3.14}


def test_loads_with_replace_bool():
    os.environ['MY_BOOL_CONFIG_VAR'] = 'true'
    toml_str = """
is_set = '${MY_BOOL_CONFIG_VAR}'
"""
    assert loads(toml_str) == {'is_set': True}

    os.environ['MY_BOOL_CONFIG_VAR'] = 'false'
    assert loads(toml_str) == {'is_set': False}


def test_complex_replacement():
    os.environ['MY_LAPTOP_NAME'] = 'laptop'
    os.environ['MY_LAPTOP_PRICE'] = '1000'
    os.environ['MY_IS_LAPTOP_SOLD'] = 'true'

    with open('./tests/test_complex_replacement.toml', 'rb') as f:
        assert load(f) == MORE_COMPLEX_OUTPUT


def test_loads_with_replace_and_empty_value():
    toml_str = """
x = 5
y = '${NON_EXISTENT_VAR}'
"""
    with pytest.warns(UserWarning,
                      match=r'WARNING: Environmental variable NON_EXISTENT_VAR'
                      ' does no exist.'):
        assert loads(toml_str) == {'x': 5, 'y': None}


def test_loads_with_replace_dict():
    os.environ['MY_CONFIG_VAR'] = "{z = 123}"
    toml_str = """
x = 5
y = '${MY_CONFIG_VAR}'
"""
    assert loads(toml_str) == {'x': 5, 'y': {'z': 123}}


TEST_ELEMENTALS_TOML_STR = """
y = '${MY_CONFIG_VAR}'
"""


def test_loads_with_replace_list():
    os.environ['MY_CONFIG_VAR'] = '[1, 2, 3, foo, False, True]'
    assert loads(TEST_ELEMENTALS_TOML_STR) == {
        'y': [1, 2, 3, 'foo', False, True]}


def test_loads_with_replace_int():
    os.environ['MY_CONFIG_VAR'] = '54321'
    result = loads(TEST_ELEMENTALS_TOML_STR)
    assert result == {'y': 54321}
    assert isinstance(result['y'], int)
