# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.17] - 2019-12-19
### Added
- Added PyPI Test section to CONTRIBUTING.md
- Added templates to pypi package - fix [#84](https://github.com/camilamaia/scanapi/issues/84)


## [0.0.16] - 2019-12-18
### Changed
- Fixed No module named 'scanapi.tree' [#82](https://github.com/camilamaia/scanapi/issues/82)

## [0.0.15] - 2019-12-14
## Added
- CodeCov Setup
- CircleCI Setup

### Changed
- Updated Documentation
- Increased coverage
- Fixed join of urls to keep the last slash
- Used dot notation to access responses inside api spec
- Renamed option report_path to output_path
- Reporter option -r, --reporter [console|markdown|html]

### Removed
- Removed requirements files and put every dependency under setup.py
- Removed dcvars key

## [0.0.14] - 2019-10-09
### Changed
- Bumped version

## [0.0.12] - 2019-08-15
### Added
- Used env variables from os

## [0.0.11] - 2019-08-09
### Added
- Added Docker file

## [0.0.10] - 2019-08-09
### Added
- Fix vars interpolation
- Add logging
- Option to hide headers fields



[Unreleased]: https://github.com/camilamaia/scanapi/compare/v0.0.17...HEAD
[0.0.17]: https://github.com/camilamaia/scanapi/compare/v0.0.16...v0.0.17
[0.0.16]: https://github.com/camilamaia/scanapi/compare/v0.0.15...v0.0.16
[0.0.15]: https://github.com/camilamaia/scanapi/compare/v0.0.14...v0.0.15
[0.0.14]: https://github.com/camilamaia/scanapi/compare/v0.0.13...v0.0.14
[0.0.13]: https://github.com/camilamaia/scanapi/compare/v0.0.12...v0.0.13
[0.0.12]: https://github.com/camilamaia/scanapi/compare/v0.0.11...v0.0.12
[0.0.11]: https://github.com/camilamaia/scanapi/compare/v0.0.10...v0.0.11
[0.0.10]: https://github.com/camilamaia/scanapi/releases/tag/v0.0.10
