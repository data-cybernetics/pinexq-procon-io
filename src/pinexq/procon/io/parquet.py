"""Parquet I/O helpers (requires the ``parquet`` extra).

Provides buffer-level read/write for Apache Parquet using pandas and PyArrow.
"""

import logging
from typing import IO

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pyarrow import ArrowInvalid

LOG = logging.getLogger(__name__)

parquet_media_type = "application/vnd.apache.parquet"


def parquet_buffer_writer(buffer: IO, df: pd.DataFrame) -> None:
    """Write a pandas DataFrame to *buffer* as Parquet.

    The buffer position is reset to the beginning after writing so it can
    be read back immediately.
    """
    table = pa.Table.from_pandas(df)
    pq.write_table(table, buffer)
    buffer.seek(0)


def parquet_buffer_reader(buffer: IO) -> pd.DataFrame | None:
    """Read a pandas DataFrame from a Parquet *buffer*.

    Returns ``None`` if the buffer does not contain valid Parquet data.
    """
    try:
        return pq.read_table(buffer).to_pandas()
    except ArrowInvalid as ex:
        LOG.warning(f"ArrowInvalid: {ex}")
        return None

