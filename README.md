# envsub

**envsub** is a text preprocessing tool that performs environment variable
substitution in files, with support for default values. Written in Rust and
callable from Python, it provides a fast and reliable way to inject environment
variables into text files during runtime.

## Features

- Environment variable substitution in any text file.
- Support for default values when environment variables are missing.
- Fast performance with Rust under the hood, accessible from Python.

## Installation

```bash
pip install envsub
```


## Usage


### envsub api

envsub comes with a `sub` method that text a `io.TextIO` and return
a `io.TextIO` containing the replaced variable.

Basic usage:

```python
from envsub import sub


with open("/path/to/file", "r") as downstream:
    with sub(downstream) as upstream:
        upstream.read()

```


When it is usefull.

``envsub`` is made for replacing a set of variable inside a configuration
file from envisonment variable, its feet well with confifuration file format.

Example with json:


```python
import json
from envsub import sub

with open("/path/to/file.json", "r") as downstream:
    with sub(downstream) as upstream:
        data = json.load(upstream)

```


### Substitution format

envsubst subsitute variable format that are curly-braced, like in bash.

```json
{"hello": "${NAME}"}
```

> ⚠️ **Warning:**
>
> The variable stay in the same line, no `\n` are permitted.**
>
> This will **not** work:
> {"hello": "${
>      NAME
>    }"
> }
>


#### Default value:

If the environment variable is not present, no substitution will be made,
it means than in the previous example, `${NAME}` will stay in the read value.

Alternatively, a default value can be set in the variable, using a `-` value.


```json
{"hello": "${NAME-world}"}
```

In this case the final result will be `{"hello": "world"}`.



## Alternatives

Similar tools exists, but did not find any good one in python.

The envsub lib has been created to replace non existing tool like
[a8m/envsubst](https://github.com/a8m/envsubst) a Go binary that
update the GNU envsubst that do not support default values.
