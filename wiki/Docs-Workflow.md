# MkDocs and Read the Docs Workflow

## Documentation Structure

This project uses MkDocs and Read the Docs for documentation generation and deployment.

Important documentation-related files and directories:

- `documentation/` contains documentation source files
- `wiki/` contains contributor guides and workflow documentation
- `mkdocs.yml` controls MkDocs configuration
- `.readthedocs.yaml` configures automatic Read the Docs builds

---

## MkDocs Configuration

The `mkdocs.yml` file defines:

- site navigation
- enabled plugins
- themes
- Markdown extensions
- documentation structure

MkDocs uses this configuration to generate the final documentation site.

---

## Read the Docs Workflow

The project uses Read the Docs for automatic documentation deployment.

Workflow overview:

1. Contributor pushes documentation changes to GitHub
2. GitHub webhook triggers Read the Docs
3. Read the Docs rebuilds the documentation
4. Updated documentation is published automatically

---

## Documentation Commands

### Install Documentation Dependencies

```bash
make docs-install