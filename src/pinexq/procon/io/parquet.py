"""Parquet I/O helpers (requires the ``parquet`` extra).

Provides reader and writer callables for Apache Parquet buffers using pandas
and PyArrow. Both functions conform to the dataslot annotation signatures::

    @dataslot.input("data_in", media_type=MediaTypes.OCTETSTREAM, reader=parquet_buffer_reader)
    @dataslot.output("data_out", media_type=MediaTypes.OCTETSTREAM, writer=parquet_buffer_writer)
"""

import logging
from typing import IO

import pandas as pd
from pyarrow import ArrowInvalid

LOG = logging.getLogger(__name__)

parquet_media_type = "application/vnd.apache.parquet"


def parquet_buffer_writer(buffer: IO, df: pd.DataFrame) -> None:
    """Write a pandas DataFrame to *buffer* as Parquet.

    Conforms to the ``WriterType`` signature expected by
    :meth:`dataslot.output` and :meth:`dataslot.returns`::

        @dataslot.output("data_out", media_type=MediaTypes.OCTETSTREAM, writer=parquet_buffer_writer)

    The buffer position is reset to the beginning after writing so it can
    be read back immediately.
    """
    df.to_parquet(buffer)
    buffer.seek(0)


def parquet_buffer_reader(buffer: IO) -> pd.DataFrame | None:
    """Read a pandas DataFrame from a Parquet *buffer*.

    Conforms to the ``ReaderType`` signature expected by
    :meth:`dataslot.input`::

        @dataslot.input("data_in", media_type=MediaTypes.OCTETSTREAM, reader=parquet_buffer_reader)

    Returns ``None`` if the buffer does not contain valid Parquet data.
    """
    try:
        return pd.read_parquet(buffer)
    except ArrowInvalid as ex: #Pandas raises most errors from the PyArrow engine directly
        LOG.warning(f"ArrowInvalid: {ex}")
        return None

