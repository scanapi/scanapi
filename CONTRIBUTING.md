# Contributing

Thanks for taking the time to contribute! 🙇‍♀️🙇‍♂️ Every little bit of help counts!

## Install

### Requirements:
- [Python 3][python]
- [Poetry][poetry]

Clone the repository and enter into the project's folder:

```shell
$ git clone git@github.com:scanapi/scanapi.git
$ cd scanapi
```

Create a [virtualenv][virtualenv] for ScanAPI and activate it:

```shell
$ make sh
```

Install the dependencies:

```shell
$ make install
```

## Run

Run the ScanAPI:

```shell
$ poetry run scanapi
```

For help, run:

```shell
$ poetry run scanapi --help
```

As you may noticed, you need an API specification file to run ScanAPI properly.
Otherwise you will receive this error:

```shell
$ poetry run scanapi
ERROR:scanapi:Could not find API spec file: scanapi.yaml. [Errno 2] No such file or directory: 'scanapi.yaml'
```

For that, we have the [ScanAPI Examples][scanapi-examples] repository, with some API specification
examples that you can use.

### Clone ScanAPI Examples

In another terminal tab, outside `scanapi` folder, clone the [ScanAPI examples][scanapi-examples] project:

```shell
$ git clone git@github.com:scanapi/examples.git
```

Your workspace should have these both folders now:

```shell
▶ ls
scanapi               examples
```

Activate the virtualenv created before:

```shell
$ cd scanapi
$ make sh
```

Run the ScanAPI for the API example you prefer:

**PokèAPI**

```shell
$ poetry run scanapi ../examples/pokeapi/scanapi.yaml -c ../examples/pokeapi/.scanapi.yaml -o ../examples/pokeapi/scanapi-report.html
```

**Demo-API**

```shell
$ source ../examples/demo-api/.env
$ poetry run scanapi ../examples/demo-api/api.yaml -c ../examples/demo-api/.scanapi.yaml -o ../examples/demo-api/scanapi-report.html
```

## Tests

To run the tests, run:

```shell
$ make test
```

For testing, we use [pytest](https://docs.pytest.org/en/stable/). We also use classes to give some
context to the tests, something inspired in [BDD](https://www.departmentofproduct.com/blog/writing-bdd-test-scenarios/):

```python
class TestFileName: # example: TestRegistration
   class TestFunctionName: # example TestRegisterAccount
      class TestContext: # example TestWhenDataIsIncomplete
         def test_expect_behavior(self): # example test_should_return_422
            pass
```

## Add new dependencies

For adding new dependencies, we use Poetry. You can check the official documentation: [https://python-poetry.org/docs/basic-usage/#specifying-dependencies](https://python-poetry.org/docs/basic-usage/#specifying-dependencies)

## Deploy

Steps:
1. Release PR
2. Deploy on GitHub

### 1. Release PR

### Bump the lib Version

Check the last release number at [https://pypi.org/project/scanapi/#history](https://pypi.org/project/scanapi/#history)

Increment the version number in the `pyproject.toml` according to the version you have just got: https://github.com/scanapi/scanapi/blob/master/pyproject.toml#L3

Also, increment the version number in the `Dockerfile` according to the version you have just got: https://github.com/scanapi/scanapi/blob/master/Dockerfile#L9

### Update the CHANGELOG.md

Add a new version title with the new version number and the current date, like [this](https://github.com/camilamaia/scanapi/commit/86e89e6ab52bbf64e058c02dbfdbbb1500066bff#diff-4ac32a78649ca5bdd8e0ba38b7006a1eR9-R10)

And add the version links, like [this](https://github.com/camilamaia/scanapi/commit/86e89e6ab52bbf64e058c02dbfdbbb1500066bff#diff-4ac32a78649ca5bdd8e0ba38b7006a1eR69-R70)

### Create the PR

Create a PR named `Release <version>` containing these two changes above.

[Example of Release PR](https://github.com/camilamaia/scanapi/commit/86e89e6ab52bbf64e058c02dbfdbbb1500066bff)

### Merge the PR

Once the PR has been accepted and passed on all checks, merge it.

### 2. Deploy on GitHub

Deploy on GitHub is done when a [new release is created][creating-releases].

- The `tag version` should be `v<version>`, like for example `v0.0.18`.
- The `release title` should be the same as tag version,(e.g `v0.0.18`).
- The `release description` should be the content copied from the CHANGELOG.md file from the
corresponding version section.

Real examples are available at: https://github.com/scanapi/scanapi/releases.

When the Deploy on GitHub is done, the new version will be automatically deployed on [Docker Hub][scanapi-on-docker-hub] and [PyPI][scanapi-on-pypi].
Check if everything run as expected for both and that is it, the deploy is done 🎉


[creating-releases]: https://help.github.com/en/enterprise/2.13/user/articles/creating-releases
[poetry]: https://python-poetry.org/docs/#installation
[python]: https://www.python.org/downloads/
[scanapi-examples]: https://github.com/scanapi/examples
[scanapi-on-docker-hub]: https://hub.docker.com/r/camilamaia/scanapi
[scanapi-on-pypi]: https://pypi.org/project/scanapi/
[virtualenv]: https://virtualenv.pypa.io/en/latest/
