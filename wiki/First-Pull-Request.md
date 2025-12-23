# First Pull Request

How to submit a pull request:

- [1. Create a GitHub Account](#1-create-a-github-account)
- [2. Install Git](#2-install-git)
- [3. Fork the Project](#3-fork-the-project)
- [4. Clone your Fork](#4-clone-your-fork)
- [5. Create a New Branch](#5-create-a-new-branch)
- [6. Run ScanAPI locally](#6-run-scanapi-locally)
- [7. Make your changes](#7-make-your-changes)
- [8. Test your changes](#8-test-your-changes)
- [9. Commit and push your changes](#9-commit-and-push-your-changes)
- [10. Add changelog entries](#10-add-changelog-entries)
- [11. Create a GitHub PR](#11-create-a-github-pr)
- [12. Update your branch if needed](#12-update-your-branch-if-needed)

### 1. Create a GitHub Account

Make sure you have a [GitHub account](https://github.com/join)

### 2. Install Git

Make sure you have [Git installed](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### 3. Fork the Project

[Fork the ScanAPI repository](https://guides.github.com/activities/forking/)

### 4. Clone your Fork

[Clone](https://docs.github.com/en/enterprise/2.13/user/articles/cloning-a-repository) your fork locally

### 5. Create a New Branch

Go into the ScanAPI folder:

```bash
$ cd scanapi
```

And create a new branch:

```bash
$ git switch -c <issue_number>
```

### 6. Run ScanAPI locally

[Run ScanAPI locally](Run-ScanAPI-Locally.md)

### 7. Make your changes

Now is the step where you can implement your changes in the code.

It is important to notice that we document our code using [docstrings](https://www.python.org/dev/peps/pep-0257/#what-is-a-docstring). Modules, classes, functions, and methods should be documented. Your changes should also be well documented and should reflect updated docstrings if any of the params were changed for a class/attributes or even functions.

We follow the given pattern below to keep consistency in the docstrings:

```python
class Example:
    """Explain the purpose of the class

    Attributes:
        spec[dict]: Short explanation here
        parent[type, optional]: Short explanation here

    """

    def __init__(self, spec, parent=None):
        self.spec = spec
        self.parent = parent

    def foobar(self, field_name):
        """Purpose of the function

        Args:
            field_name[str]: Short explanation here

        Returns:
            value[str]: Short explanation here

        """
        value = field_name.get('node')
        return value
```

One last thing to keep in mind while self-documenting code with docstrings that you can ignore docstrings in property decorators and magic methods.

### 8. Test your changes

#### 8.1 Write new tests

Make sure you have created the necessary tests for every new change you made. Please, visit the page [Writing Tests](Writing-Tests.md) to find the instructions of how to create tests

#### 8.2 Make sure all tests passed

[Run all the tests](Run-ScanAPI-Locally.md#tests) and make sure that they all passed.

PRs will not be merged if there is any test missing or failing.

### 9. Commit and push your changes

Commit the changes:

```bash
$ git commit -a -m "<commit_message>"
```

We encourage you to follow these rules to write great commit messages: https://www.conventionalcommits.org/en/v1.0.0/

Push your commit to GitHub

```bash
$ git push --set-upstream origin <issue_number>
```

Create the number of changes/commits you need and push them.

### 10. Add changelog entries

[Add a CHANGELOG entry](Changelog-Guide.md)

### 11. Create a GitHub PR

[Create a GitHub PR](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

### 12. Update your branch if needed.

Make sure your branch is updated with main.
