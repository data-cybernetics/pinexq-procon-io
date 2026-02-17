# pinexq-procon-io

I/O utilities for the **pinexq** ecosystem. This package provides reader and
writer callables for common data formats — JSON (via Pydantic), Apache Parquet,
Matplotlib figures, and Plotly JSON — designed to plug directly into
[`pinexq-procon`](https://pypi.org/project/pinexq-procon/) dataslot
annotations.

## How readers and writers work with dataslots

In `pinexq-procon`, a processing step declares its inputs and outputs through
`@dataslot` annotations. Each annotation accepts a **reader** or **writer**
callable that handles serialization:

- `dataslot.input(reader=...)` — the reader is called with a file-like object
  and must return the deserialized data.
- `dataslot.output(writer=...)` — the writer is called with a file-like object
  and the data to serialize.
- `dataslot.returns(writer=...)` — same as output, but for the function's
  return value.

The functions in `pinexq.procon.io` follow exactly these signatures
(`Callable[[IO], T]` for readers, `Callable[[IO, T], None]` for writers) so
they can be passed directly to a dataslot annotation.

### Example

```python
from pinexq.procon.dataslots import dataslot, MediaTypes
from pinexq.procon.io import pydantic_reader, base_model_dump_json
from pinexq.procon.io.parquet import parquet_buffer_reader, parquet_buffer_writer
from pinexq.procon.io.matplotlib import figure_to_png_buffer
from pydantic import BaseModel


class Config(BaseModel):
    threshold: float


@dataslot.input("config", media_type=MediaTypes.JSON, reader=pydantic_reader(Config))
@dataslot.input("data_in", media_type=MediaTypes.OCTETSTREAM, reader=parquet_buffer_reader)
@dataslot.output("data_out", media_type=MediaTypes.OCTETSTREAM, writer=parquet_buffer_writer)
@dataslot.returns(media_type=MediaTypes.PNG, writer=figure_to_png_buffer)
def process(config: Config, data_in, data_out, **kwargs):
    # config is already deserialized into a Config instance by pydantic_reader
    # data_in is already a pandas DataFrame via parquet_buffer_reader
    filtered = data_in[data_in["value"] > config.threshold]
    # data_out will be serialized to Parquet via parquet_buffer_writer
    data_out = filtered
    # the returned figure will be written as PNG via figure_to_png_buffer
    return create_plot(filtered)
```

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

### Plotly

Adds support for writing pandas DataFrames as Plotly-compatible JSON (uses
scipy sparse arrays internally).

```bash
pip install "pinexq-procon-io[plotly] @ git+https://github.com/data-cybernetics/pinexq-procon-io.git"
```

```python
from pinexq.procon.io.plotly import plotly_json_writer
```

### Installing all extras

```bash
pip install "pinexq-procon-io[parquet,matplotlib,plotly] @ git+https://github.com/data-cybernetics/pinexq-procon-io.git"
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

### Plotly helpers (requires `plotly` extra)

```python
from pinexq.procon.io.plotly import plotly_json_writer, to_plotly_json
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
