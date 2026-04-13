# Run ScanAPI in Dev Env

ScanAPI can be run in three supported development environments.
**We recommend starting with the first option unless you have a specific reason not to.**

Choose your setup:

1. **GitHub Codespaces (recommended)**
   [Run ScanAPI on GitHub Codespaces](Run-ScanAPI-On-Codespaces.md)

2. **Local Dev Container**
   [Run ScanAPI locally with Dev Container](Run-ScanAPI-Locally-with-Dev-Container.md)

3. **Manual local setup**
   [Run ScanAPI locally manually](Run-ScanAPI-Locally-Manually.md)

If you're new to the project, just follow the Codespaces guide and you’ll be ready in minutes.
The sections below explain when you might want to choose a different option.

## When to use each option

| Option              | Best for                                                        | Pros                                                                      | Cons                                                  |
| ------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------- | ----------------------------------------------------- |
| GitHub Codespaces   | New contributors, fast onboarding, no local install             | No local setup, consistent cloud environment, preconfigured tools         | Requires Codespaces access and internet               |
| Local Dev Container | Local development with isolation and reproducibility            | Matches CI/Cloud, isolates dependencies, no global Python packages needed | Requires Docker and VS Code Dev Containers extension  |
| Manual local        | Developers who want full local control or cannot use containers | Works without Docker, simple for experienced Python users                 | Requires local Python setup and dependency management |

## How to choose

* Use **Codespaces** if you want the fastest, zero-setup experience
* Use **Dev Container** if you prefer working locally but want a clean, reproducible environment
* Use **Manual setup** only if you already manage Python environments or cannot use containers
