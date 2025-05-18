# envTOMLlib
`envTOMLlib` is fork of dead project envtoml by mrshu/envtoml. But because his project is too old and was not updated at all in last couple of years I decided to rewrite it to newer python version, where tomllib has been in-build.
So here it is an `envTOMLlib`.
This library was created on my personal need to use toml configuration format in container-like environments, where environment variables are often used for project configurations.

## Usage 
1. Usage is same as using in-build tomllib library but instead of importing tomllib (ex.`import tomllib` see details on: [python tomllib docs](https://docs.python.org/3/library/tomllib.html)) you just import envtomllib like this:
`import envtomllib` or `from envtomllib import load, loads`
2. usage of `load` or `loads` is same as in tomllib.

Supported environment variable value types and conversion examples:
 - integers (ex. `'10'`=>`10`, `'20'`=>`20`, `'274'`=>`274`, `'10000006565654644'`=>`10000006565654644`)
 - floats (ex. `'3.14'`=>`3.14`, `'10.2'`=>`10.2`, `'10265.1651'`=>`10265.1651`)
 - booleans (ex. `true`=>`True`, `false`=>`False`)
 - inline tables (see: [inline tables toml](https://toml.io/en/v1.0.0#inline-table)) (ex. `'{ a = 10}'`=>`{'a':10}`) 
   - `<ENVIRONMENT VARIABLE>='{ <inline table variable> = <value> }'` 
 - supports lists (ex. `'[1, 2, 3, foo, true, false]'`=>`[1, 2, 3, 'foo', True, False]`)

### Example:
Lets suppose you have ex.toml file in the same folder where you will have python example script:
```
[table]
table_parameter = ${INLINE_TABLE_EXAMPLE}
```

Lets define environmental variable:
`INLINE_TABLE_EXAMPLE='{ foo = 10 }'`

Now we create python script in the same folder as ex.toml.
```
from envtomllib import load, loads

with open('./ex.toml', 'rb') as file: # you need to open it with reading binary mode
  toml_conf = load(file)
  print(toml_conf)

# with use of loads
toml_str = """
[table]
table_parameter = ${INLINE_TABLE_EXAMPLE}
"""
toml_conf = loads(toml_str)
print(toml_str)
```

you should get output:
```
{'table_parameter':{'foo': 10}}
{'table_parameter':{'foo': 10}}
```


## Tests
### With podman:
 1. `podman build . -t envtomllib`
 2. `podman run envtomllib`

### With docker:
 1. `cp Containerfile Dockerfile`
 2. `docker build . -t envtomllib`
 3. `docker run envtomllib`

