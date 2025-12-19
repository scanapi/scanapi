# Changelog Guide

This guide explains how to add entries to the ScanAPI changelog.

## Table of Contents

- [What is a changelog?](#what-is-a-changelog)
- [Why keep a changelog?](#why-keep-a-changelog)
- [Who needs a changelog?](#who-needs-a-changelog)
- [Where is ScanAPI changelog?](#where-is-scanapi-changelog)
- [Guiding Principles](#guiding-principles)
- [What warrants a changelog entry?](#what-warrants-a-changelog-entry)
- [Writing good changelog entries](#writing-good-changelog-entries)
- [How to add a changelog entry](#how-to-add-a-changelog-entry)

## What is a changelog?

A changelog is a file which contains a curated, chronologically ordered list of notable changes for each version of a project.

## Why keep a changelog?

To make it easier for users and contributors to see precisely what notable changes have been made between each release (or version) of the project.

## Who needs a changelog?

People do. Whether consumers or developers, the end users of software are human beings who care about what's in the software. When the software changes, people want to know why and how.

## Where is ScanAPI changelog?

ScanAPI changelog is available at [CHANGELOG.md](../CHANGELOG.md)

## Guiding Principles

- Changelogs are for humans, not machines.
- There should be an entry for every single version.
- The same types of changes should be grouped.
- Versions and sections should be linkable.
- The latest version comes first.
- The release date of each version is displayed.

## What warrants a changelog entry?

- Security fixes must have a changelog entry with type set to security.
- Any user-facing change should have a changelog entry.
- Performance improvements should have a changelog entry.
- Any docs-only changes should not have a changelog entry.
- A fix for a bug introduced and then fixed in the same release should not have a changelog entry.
- Any developer-facing change (e.g., refactoring, technical debt remediation, test suite changes) should not have a changelog entry. Example: "Fix flaky tests."

## Writing good changelog entries

A good changelog entry should be descriptive and concise. It should explain the change to a reader who has zero context about the change. If you have trouble making it both concise and descriptive, err on the side of descriptive.

- **Bad**: Go to a project order.
- **Good**: Show a user's starred projects at the top of the "Go to project" dropdown.

The first example provides no context of where the change was made, or why, or how it benefits the user.

- **Bad**: Copy (some text) to clipboard.
- **Good**: Update the "Copy to clipboard" tooltip to indicate what's being copied.

Again, the first example is too vague and provides no context.

- **Bad**: Fixes and Improves CSS and HTML problems in mini pipeline graph and builds dropdown.
- **Good**: Fix tooltips and hover states in mini pipeline graph and builds dropdown.

The first example is too focused on implementation details. The user doesn't care that we changed CSS and HTML, they care about the end result of those changes.

- **Bad**: Strip out nils in the Array of Commit objects returned from find_commits_by_message_with_elastic
- **Good**: Fix 500 errors caused by Elasticsearch results referencing garbage-collected commits

The first example focuses on how we fixed something, not on what it fixes. The rewritten version clearly describes the end benefit to the user (fewer 500 errors), and when (searching commits with Elasticsearch).

Use your best judgement and try to put yourself in the mindset of someone reading the compiled changelog. Does this entry add value? Does it offer context about where and why the change was made?

source: http://www.obsis.unb.br/gitlab/help/development/changelog.md

## How to add a changelog entry

The changelog is available in the file [CHANGELOG.md](../CHANGELOG.md).

First you need to identify the type of your change. Type of changes:

- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Fixed` for any bug fixes.
- `Removed` for now removed features.
- `Security` in case of vulnerabilities.

You should always add new changelog entries in the `Unreleased` section. At release time, we will move the `Unreleased` section changes into a new release version section.

So, inside the `Unreleased` section, you need to add your entry in the proper type section. If there is no section for it yet, you should add it.

Let's see some examples. Let's suppose I have a new `Fixed` change to add, and current the CHANGELOG.md file is like this:

```markdown
## [Unreleased]
### Added
- JSON response is now properly rendered, instead of plain text. [#213](https://github.com/scanapi/scanapi/pull/213)

### Changed
- Renamed `api.(yaml|json)` to `scanapi.yaml`. [#222](https://github.com/scanapi/scanapi/pull/222)
```

I need to add a new `Fixed` section and add my entry there:

```markdown
## [Unreleased]
### Added
- JSON response is now properly rendered, instead of plain text. [#213](https://github.com/scanapi/scanapi/pull/213)

### Changed
- Renamed `api.(yaml|json)` to `scanapi.yaml`. [#222](https://github.com/scanapi/scanapi/pull/222)

### Fixed
- My changelog message here. [#<PR_number>](<pr_link>)
```

Note the order of the type sections matters. We have a lint that checks it, so it must be ordered Alphabetically. First Added, second Changed, third `Deprecated` and so on.

Now, let's say I have one more entry to add and its type is `Added`. Since we already have a section for it, I will only add an extra line:

```markdown
## [Unreleased]
### Added
- JSON response is now properly rendered, instead of plain text. [#213](https://github.com/scanapi/scanapi/pull/213)
- My other changelog message here. [#<PR_number>](<pr_link>)

### Changed
- Renamed `api.(yaml|json)` to `scanapi.yaml`. [#222](https://github.com/scanapi/scanapi/pull/222)

### Fixed
- My changelog message here. [#<PR_number>](<pr_link>)
```

This content is totally based on [keep a changelog website](https://keepachangelog.com/en/1.0.0/), since we follow its guidelines.
