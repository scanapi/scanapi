## Install

Create a [virtualenv][virtualenv] for scanapi and activate it.

```bash
$ git clone git@github.com:camilamaia/scanapi.git
$ cd scanapi
$ python setup.py develop
$ pip install -e .[dev] .[test]
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

## Deploy

Requirements:

- [setuptools][setuptools]
- [twine][twine]
- [PyPI Test][pypi-test] credentials
- [PyPI][pypi] credentials
- DockerHub credentials

Steps:
1. Release PR
2. Deploy on GitHub
3. Deploy on PyPI
4. Deploy on DockerHub

### 1. Release PR

### Bump the lib Version

Check the last release number at https://pypi.org/manage/project/scanapi/releases/
Increment the version number at `setup.py` according to the version you have just got.

### Update the CHANGELOG.md

Add a new version title with the new version number and the current date, like [this](https://github.com/camilamaia/scanapi/commit/86e89e6ab52bbf64e058c02dbfdbbb1500066bff#diff-4ac32a78649ca5bdd8e0ba38b7006a1eR9-R10)

And add the version links, like [this](https://github.com/camilamaia/scanapi/commit/86e89e6ab52bbf64e058c02dbfdbbb1500066bff#diff-4ac32a78649ca5bdd8e0ba38b7006a1eR69-R70)

### Create the PR

Create a PR named `Release <version>` containing these two changes above.

[Example of Release PR](https://github.com/camilamaia/scanapi/commit/86e89e6ab52bbf64e058c02dbfdbbb1500066bff)

### 2. Deploy on GitHub

Deploy on GitHub is done when a [new release is created][creating-releases].

- The `tag version` should be `v<version>`, like for example `v0.0.18`.
- The `release title` should be the same as tag version,(e.g `v0.0.18`).
- The `release description` should be the content copied from the CHANGELOG.md file from the corresponding version section.

Real examples are available at: https://github.com/camilamaia/scanapi/releases.

### 3. Deploy on PyPI

#### PyPI Test

Before sending directly the new release to the official PyPi repository, it is a good practice to send it to [PyPI Test][pypi-test] first.

For that, check the last release number at https://test.pypi.org/manage/project/scanapi/releases/
Increment **locally** the version number at `setup.py` according to the version you have just got. Do not commit the `setup.py` changes.

Run:

```bash
sudo rm -r dist/*
python3 setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

To install and test it, run:

```bash
$ pip install -i https://test.pypi.org/simple/ scanapi
```

**Revert the `setup.py` changes.**

#### PyPi Production

```bash
$ cd scanapi
$ rm -r dist/*
$ python3 setup.py sdist bdist_wheel
$ twine upload dist/*
```

### 4. Deploy on DockerHub

```bash
$ docker build -f Dockerfile -t camilamaia/scanapi:<version> -t camilamaia/scanapi:latest . --no-cache # for example $ docker build -f Dockerfile -t camilamaia/scanapi:0.0.18 -t camilamaia/scanapi:latest . --no-cache
$ docker tag camilamaia/scanapi:<version> camilamaia/scanapi:<version> # for example $ docker tag camilamaia/scanapi:0.0.18 camilamaia/scanapi:0.0.18
$ docker tag camilamaia/scanapi:latest camilamaia/scanapi:latest
$ docker push camilamaia/scanapi:<version> # for example $ docker push camilamaia/scanapi:0.0.18
$ docker push camilamaia/scanapi:latest
```

[virtualenv]: https://virtualenv.pypa.io/en/latest/
[pypi]: https://pypi.org
[pypi-test]: https://test.pypi.org
[setuptools]: https://packaging.python.org/key_projects/#setuptools
[twine]: https://packaging.python.org/key_projects/#twine
