## Install

Create a [virtualenv][virtualenv] for scanapi and activate it.

```bash
$ git clone git@github.com:camilamaia/scanapi.git
$ cd scanapi
$ pip install -r requirements.txt
$ pre-commit install
```

## Run

```bash
$ scanapi
```

For help, run:

```bash
$ scanapi --help
```

### Tests


```
$ pytest
```

To have the BDD reports on terminal, run:

```
$ pytest --gherkin-terminal-reporter
```

## Deploy on PyPI

Requirements:

- [setuptools][setuptools]
- [twine][twine]

### Test Environment

Check the last release number at https://test.pypi.org/manage/project/scanapi/releases/
Increment the version number at `setup.py` according to the version you have just got.

Then, send the new version to PyPi server

```bash
$ rm -r dist/*
$ python3 setup.py sdist bdist_wheel
$ python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

To test it, run:

```
$ pip install -i https://test.pypi.org/simple/ scanapi
```

### Production Environment

Check the last release number at https://pypi.org/manage/project/scanapi/releases/
Increment the version number at `setup.py` according to the version you have just got.

Then, send the new version to PyPi server

```bash
$ rm -r dist/*
$ python3 setup.py sdist bdist_wheel
$ twine upload dist/*
```

[virtualenv]: https://virtualenv.pypa.io/en/latest/
[setuptools]: https://packaging.python.org/key_projects/#setuptools
[twine]: https://packaging.python.org/key_projects/#twine
