# deserializer

Deserialize class from dict from json/yaml/toml.

## Why create this

To have a strong-typed accessing experience like other language.

## How to use

1. Build the wheel:
   See [How to build](#how-to-build) for more info.

2. Import in your project:
   Install the wheel or set it as dependency in your project's package manager.

3. Use the library:
   ```python
   from deserializer import deserialize

   instance = deserialize(Class, json)
   ```

## How to build

1. Prepare pdm
   See [here](https://pdm-project.org/en/latest/#installation) for more info

2. Build
   Run `pdm install` to create virtual environment for you.
   Run `pdm build` to build wheel.

## Notes:

1. Please make sure your class is type-hinted well.
   For example, `Optional[str]` or `Union[str, None]` has been deprecated by python and you need to use `str | None` instead.
   We do not support these deprecated styles either.

2. Please make sure your class has a non-argument constructor.
   Most of the time this is not a problem, but you should ensure this yourself if you use a customized constructor.
   This means `instance = MyClass()` should be a valid way to initialize your class.
   For example:
   ```python
   class MyClass:
       pass
   ```
   This is fine, while
   ```python
   class MyClass:
       def __init__(self, argument: object):
           pass
   ```
   This is not acceptable.
