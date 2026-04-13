# First Pull Request

This guide walks you through the process of contributing code and opening a pull request.

At this point, it is expected that you already:

* have a GitHub account
* forked the repository
* set up your environment (locally or with Codespaces)
* have an issue assigned to you

Now, let’s go step by step.

* [1. Create a New Branch](#1-create-a-new-branch)
* [2. Make your changes](#2-make-your-changes)
* [3. Test your changes](#3-test-your-changes)
* [4. Commit and push your changes](#4-commit-and-push-your-changes)
* [5. Add changelog entries](#5-add-changelog-entries)
* [6. Create a GitHub PR](#6-create-a-github-pr)
* [7. Follow up on your Pull Request](#7-follow-up-on-your-pull-request)

## 1. Create a New Branch

Go into the ScanAPI folder (if you are not already there):

```bash
cd scanapi
````

Create a new branch using the issue number:

```bash
git switch -c <issue_number>
```

## 2. Make your changes

Now you can implement your changes in the code.

We document code using docstrings. Modules, classes, functions, and methods should
be documented. If your changes modify behavior or parameters, make sure to update
the corresponding docstrings.

We follow this pattern:

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

You can skip docstrings for property decorators and magic methods.

## 3. Test your changes

### 3.1 Write new tests

Make sure you create tests for any new behavior: [Writing Tests](Writing-Tests.md).

### 3.2 Run all tests

Run all tests and ensure they pass: [Run tests](Run-ScanAPI-in-Dev-Env.md#tests).
Pull requests will not be merged if tests are missing or failing.

## 4. Commit and push your changes

Before committing, review your changes:

```bash
git status
git diff
```

Add files intentionally, one by one:

```bash
git add <file>
```

Then commit:

```bash
git commit -m "<commit_message>"
```

Commit messages must follow the Conventional Commits specification:
[https://www.conventionalcommits.org/en/v1.0.0/](https://www.conventionalcommits.org/en/v1.0.0/)

Push your branch:

```bash
git push --set-upstream origin <issue_number>
```

You can create multiple commits as needed.

## 5. Add changelog entries

Make sure your change is documented: [Changelog Guide](Changelog-Guide.md).

## 6. Create a GitHub PR

Before opening your PR, it is recommended to make sure your branch is up to date:

```bash
git pull origin main
```

Open a pull request to the main repository:

[https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request)

Make sure to:

* reference the issue (e.g. `closes #123`)
* clearly explain your changes

## 7. Follow up on your Pull Request

After opening your PR, your work is not finished yet. You need to follow the review process until it is merged.

### 7.1 Monitor your PR

* Check your PR regularly on GitHub
* Watch for:

  * Review comments
  * Requested changes
  * Approvals

### 7.2 Address feedback

If a reviewer requests changes:

1. Update your code locally
2. Commit your changes
3. Push again to the same branch

```bash
git commit -a -m "fix: address review feedback"
git push
```

The PR will update automatically.

### 7.3 Keep your branch up to date

While your PR is open, new changes may be merged into `main`.

To avoid conflicts, update your branch when needed:

```bash
git pull origin main
```

If there are conflicts:

* resolve them in your editor
* commit the merge

In ScanAPI, Pull Requests are merged using squash merge. Because of that, using `git pull` (merge) is the simplest and safest approach.

### 7.4 Wait for approval

Your PR will be merged after:

* required changes are addressed
* reviewers approve the PR

### 7.5 Merge process

A maintainer will:

* review your final changes
* merge your PR (using squash merge)

You don’t need to merge it yourself.

### Tips

* Keep PRs small and focused (faster reviews)
* Respond to comments clearly (what you changed)
* Don’t hesitate to ask questions if something is unclear
