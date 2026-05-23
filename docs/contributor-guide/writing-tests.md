# Writing Tests

Tests are located in the `tests` folder. We only have unit tests in the project for now.

## Table of Contents

- [Unit Tests](#unit-tests)
  - [Tools](#tools)
  - [Folder Structure](#folder-structure)
  - [How to create a test](#how-to-create-a-test)
  - [Examples](#examples)

## Unit Tests

### Tools

For unit tests, we use [pytest](https://docs.pytest.org/en/stable/) and [pytest-it](https://pypi.org/project/pytest-it/). If you are not familiar with these tools, please take a quick look at their official docs, it might help you:

- [pytest](https://docs.pytest.org/en/stable/)
- [pytest-it](https://pypi.org/project/pytest-it/)

### Folder Structure

Unit tests are located in the `tests/unit` folder.

Test files should follow the same structure as the project itself and their names should start with `test_`. For example:

- File: `scanapi/evaluators/code_evaluator.py`. Test File `tests/unit/evaluators/test_code_evaluator.py`
- File: `scanapi/scan.py`. Test file: `tests/unit/test_scan.py`

If the test file gets too long, we create a folder and split the tests there. For example:

- File: `scanapi/tree/endpoint_node.py`.
- Test Files:
  - `tests/unit/tree/endpoint_node/test_delay.py`
  - `tests/unit/tree/endpoint_node/test_get_requests.py`
  - `tests/unit/tree/endpoint_node/test_get_specs.py`
  - ...

### How to create a test

We create a separate class for each method we want to test. We add two `describe` decorators for this test class:

- one for the class name that the method belongs to;
- another for the method name itself.

We use `context` decorators to specify different scenarios. And, we use the `it` decorator for every test case, to describe what is the expected behavior.

Let's say we have the following file to be tested:

```python
# my_file.py
class MyClassA:
    def method_1(self):
        pass

    def method_2(self):
        pass

class MyClassB:
    def method_3(self):
        pass
```

The test file `test_my_file.py` would look like something similar to this:

```python
from pytest import mark


@mark.describe("my class a")
@mark.describe("method_1")
class TestMethod1:
    @mark.context("when scenario A happens")
    @mark.it("should do this")
    def test_should_do_this(self):
        # test here
        pass

    @mark.context("when scenario A happens")
    @mark.it("should not do that")
    def test_should_not_do_that(self):
        # test here
        pass

    @mark.context("when scenario B happens")
    @mark.it("should do another thing")
    def test_should_do_another_thing(self):
        # test here
        pass


@mark.describe("my class a")
@mark.describe("method_2")
class TestMethod2:
    @mark.context("when scenario C happens")
    @mark.it("should do something")
    def test_should_do_something(self):
        # test here
        pass

    @mark.context("when scenario D happens")
    @mark.it("should do another thing")
    def test_should_do_another_thing(self):
        # test here
        pass


@mark.describe("my class b")
@mark.describe("method_3")
class TestMethod3:
    @mark.context("when scenario E happens")
    @mark.it("should do something")
    def test_should_do_something(self):
        # test here
        pass

    @mark.context("when scenario F happens")
    @mark.it("should do another thing")
    def test_should_do_another_thing(self):
        # test here
        pass
```

The output for this would be like:

```
* tests/unit/test_my_file.py...
- Describe: My class a...

  - Describe: Method_1...

    - Context: When scenario a happens...
      - ✓ It: should do this
      - ✓ It: should not do that

    - Context: When scenario b happens...
      - ✓ It: should do another thing

  - Describe: Method_2...

    - Context: When scenario c happens...
      - ✓ It: should do something

    - Context: When scenario d happens...
      - ✓ It: should do another thing

- Describe: My class b...

  - Describe: Method_3...

    - Context: When scenario e happens...
      - ✓ It: should do something

    - Context: When scenario f happens...
      - ✓ It: should do another thing
```

Sometimes we have files without classes. It is not a problem, we can change the `describe` decorator to point out the file name

Let's say we have the following file to be tested:

```python
# `my_file.py`
def method_1(self):
    pass


def method_2(self):
    pass
```

The test file `test_my_file.py` would look like something similar to this:

```python
from pytest import mark


@mark.describe("my file")
@mark.describe("method_1")
class TestMethod1:
    @mark.context("when scenario A happens")
    @mark.it("should do this")
    def test_should_do_this(self):
        # test here
        pass

    @mark.context("when scenario A happens")
    @mark.it("should not do that")
    def test_should_not_do_that(self):
        # test here
        pass

    @mark.context("when scenario B happens")
    @mark.it("should do another thing")
    def test_should_do_another_thing(self):
        # test here
        pass

@mark.describe("my file")
@mark.describe("method_2")
class TestMethod2:
    @mark.context("when scenario C happens")
    @mark.it("should do something")
    def test_should_do_something(self):
        # test here
        pass

    @mark.context("when scenario D happens")
    @mark.it("should do another thing")
    def test_should_do_another_thing(self):
        # test here
        pass
```

The output for it would be like:

```
* tests/unit/test_my_file.py...
- Describe: My file...

  - Describe: Method_1...

    - Context: When scenario a happens...
      - ✓ It: should do this
      - ✓ It: should not do that

    - Context: When scenario b happens...
      - ✓ It: should do another thing

  - Describe: Method_2...

    - Context: When scenario c happens...
      - ✓ It: should do something

    - Context: When scenario d happens...
      - ✓ It: should do another thing
```

### Examples

Do you wanna see real examples? Check the folder https://github.com/scanapi/scanapi/tree/main/tests/unit
