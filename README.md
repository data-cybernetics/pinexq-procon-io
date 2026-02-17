# pinexq-procon-io

Part of the `pinexq` namespace. Provides the `pinexq.procon.io` package.

## Installation

### From GitHub

```bash
pip install git+https://github.com/data-cybernetics/pinexq-procon-io.git
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add git+https://github.com/data-cybernetics/pinexq-procon-io.git
```

### From source

```bash
git clone https://github.com/data-cybernetics/pinexq-procon-io.git
cd pinexq-procon-io
pip install .
```

## Usage

```python
from pinexq.procon.io import main

main()
```

A CLI entry point is also available:

```bash
pinexq-procon-io
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
git clone https://github.com/data-cybernetics/pinexq-procon-io.git
cd pinexq-procon-io
uv sync
```

## Namespace package

This package uses [PEP 420](https://peps.python.org/pep-0420/) implicit namespace packages. The `pinexq` and `pinexq.procon` namespaces are shared and can be extended by other distributions in the `pinexq` family.
