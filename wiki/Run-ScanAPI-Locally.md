# Run ScanAPI Locally

## Install

### Requirements:

- [Python 3.10.x+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/#installation)

Fork or clone the repository and enter into the project's folder:

```bash
$ git clone git@github.com:scanapi/scanapi.git
$ cd scanapi
```

Install the dependencies:

```bash
$ make install
```

## Run

Run the ScanAPI:

```bash
$ uv run scanapi
```

For help, run:

```bash
$ uv run scanapi --help
```

As you may have noticed, you need an API specification file to run ScanAPI properly. Otherwise you will receive this error:

```bash
$ uv run scanapi
ERROR:scanapi:Could not find API spec file: scanapi.yaml.
[Errno 2] No such file or directory: 'scanapi.yaml'
```

For that, we have the [ScanAPI Examples](https://github.com/scanapi/examples) repository, with some API specification examples that you can use.

### Clone ScanAPI Examples

In another terminal tab, outside `scanapi` folder, clone the [ScanAPI examples](https://github.com/scanapi/examples) project:

```bash
$ git clone git@github.com:scanapi/examples.git
```

Your workspace should have these both folders now:

```bash
▶ ls
scanapi               examples
```

Run the ScanAPI for the API example you prefer:

**PokèAPI**

```bash
$ uv run scanapi run examples/pokeapi/scanapi.yaml -c examples/pokeapi/scanapi.conf -o examples/pokeapi/scanapi-report.html
```

**Demo-API**

```bash
$ uv run scanapi run examples/demo-api/scanapi.yaml -c examples/demo-api/scanapi.conf -o examples/demo-api/scanapi-report.html
```

## Tests

To run the tests, run:

```bash
$ make test
```
