# Deploy

Here you will find how to deploy a new production version of ScanAPI.

Requirements:

- Docker
- Access to [camilamaia/scanapi repo on Docker Hub](https://hub.docker.com/r/camilamaia/scanapi)

Steps:

1. Release PR
2. Deploy on GitHub
3. Push Docker Images

## 1. Release PR

### Bump the lib Version

Check the last release number at https://pypi.org/project/scanapi/#history

Increment the version number in the `pyproject.toml` according to the version you have just got: https://github.com/scanapi/scanapi/blob/main/pyproject.toml#L3

Also, increment the version number in the `Dockerfile` according to the version you have just got: https://github.com/scanapi/scanapi/blob/main/Dockerfile#L9

### Update the CHANGELOG.md

Add a new version title with the new version number and the current date, like [this](https://github.com/scanapi/scanapi/commit/86e89e6ab52bbf64e058c02dbfdbbb1500066bff#diff-4ac32a78649ca5bdd8e0ba38b7006a1eR9-R10)

And add the version links, like [this](https://github.com/scanapi/scanapi/commit/86e89e6ab52bbf64e058c02dbfdbbb1500066bff#diff-4ac32a78649ca5bdd8e0ba38b7006a1eR69-R70)

### Create the PR

Create a PR named `Release <version>` containing these two changes above.

[Example of Release PR](https://github.com/scanapi/scanapi/commit/86e89e6ab52bbf64e058c02dbfdbbb1500066bff)

### Merge the PR

Once the PR has been accepted and passed on all checks, merge it.

## 2. Deploy on GitHub

Deploy on GitHub is done when a [new release is created](https://docs.github.com/pt/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release).

- The `tag version` should be `v<version>`, like for example `v0.0.18`.
- The `release title` should be the same as tag version, (e.g `v0.0.18`).
- The `release description` should be the content copied from the CHANGELOG.md file from the corresponding version section.

Real examples are available at: https://github.com/scanapi/scanapi/releases.

When the Deploy on GitHub is done, the new version will be also automatically deployed on [PyPI](https://pypi.org/project/scanapi/). Download the new ScanAPI version from PyPI and test if everything is working as expected.

## 3. Push Docker Images

On the ScanAPI repository, in the main branch, run the following commands from your terminal:

```bash
docker build -f Dockerfile -t camilamaia/scanapi:<version_number> -t camilamaia/scanapi:latest . --no-cache
docker tag camilamaia/scanapi:<version_number> camilamaia/scanapi:<version_number>
docker tag camilamaia/scanapi:latest camilamaia/scanapi:latest
docker push camilamaia/scanapi:<version_number>
docker push camilamaia/scanapi:latest
```

Example:

```bash
docker build -f Dockerfile -t camilamaia/scanapi:2.5.0 -t camilamaia/scanapi:latest . --no-cache
docker tag camilamaia/scanapi:2.5.0 camilamaia/scanapi:2.5.0
docker tag camilamaia/scanapi:latest camilamaia/scanapi:latest
docker push camilamaia/scanapi:2.5.0
docker push camilamaia/scanapi:latest
```

This will push the new images to Docker Hub.
