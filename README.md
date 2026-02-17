# pinexq-procon-io

I/O utilities for the **pinexq** ecosystem. This package provides serialization
and deserialization helpers for common data formats used across `pinexq.procon`
services — JSON (via Pydantic), Apache Parquet, and Matplotlib figures.

It is part of the `pinexq.procon` namespace and is designed to be installed
alongside other packages in that namespace.

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

## Optional extras

The core package only depends on Pydantic. Heavier I/O dependencies are
available as optional extras so you only install what you need.

### Parquet

Adds support for reading and writing Apache Parquet buffers via pandas and
PyArrow.

```bash
pip install "pinexq-procon-io[parquet] @ git+https://github.com/data-cybernetics/pinexq-procon-io.git"
```

```python
from pinexq.procon.io.parquet import parquet_buffer_writer, parquet_buffer_reader
```

### Matplotlib

Adds support for serializing Matplotlib figures to PNG buffers.

```bash
pip install "pinexq-procon-io[matplotlib] @ git+https://github.com/data-cybernetics/pinexq-procon-io.git"
```

```python
from pinexq.procon.io.matplotlib import figure_to_png_buffer
```

### Installing all extras

```bash
pip install "pinexq-procon-io[parquet,matplotlib] @ git+https://github.com/data-cybernetics/pinexq-procon-io.git"
```

## Usage

### JSON / Pydantic helpers

The core module provides helpers for reading and writing JSON via Pydantic
models and plain dicts:

```python
from pinexq.procon.io import dict_2_json_writer, base_model_dump_json, pydantic_reader
```

### Parquet helpers (requires `parquet` extra)

```python
from pinexq.procon.io.parquet import parquet_buffer_writer, parquet_buffer_reader
```

### Matplotlib helpers (requires `matplotlib` extra)

```python
from pinexq.procon.io.matplotlib import figure_to_png_buffer
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
git clone https://github.com/data-cybernetics/pinexq-procon-io.git
cd pinexq-procon-io
uv sync --all-extras
```

## Namespace package

This package uses [PEP 420](https://peps.python.org/pep-0420/) implicit
namespace packages. The `pinexq` and `pinexq.procon` namespaces are shared and
can be extended by other distributions in the `pinexq` family.
