"""Polars I/O helpers (requires the ``polars`` extra).

Provides reader and writer callables for Apache Parquet buffers using polars.
All functions conform to the dataslot annotation signatures::

    @dataslot.input("data_in", media_type="application/vnd.apache.parquet", reader=polars_buffer_reader)
    @dataslot.input_collection("data_in", media_type="application/vnd.apache.parquet", reader=polars_buffer_collection_reader)
    @dataslot.output("data_out", media_type="application/vnd.apache.parquet", writer=parquet_buffer_writer)
    @dataslot.output("data_out", media_type="application/vnd.apache.parquet", writer=parquet_buffer_collection_writer)
"""

import logging
from typing import IO

import polars as pl
from polars.exceptions import PolarsError

LOG = logging.getLogger(__name__)

parquet_media_type = "application/vnd.apache.parquet"

def polars_eager_reader(buffer: IO) -> pl.DataFrame | None:
    try:
        return pl.read_parquet(buffer)
    except PolarsError as ex:
        LOG.warning(f"PolarsError: {ex}")
        return None

def polars_eager_collection_reader(buffers: list[IO]) -> pl.DataFrame | None:
    try:
        return pl.read_parquet(buffers)
    except PolarsError as ex:
        LOG.warning(f"PolarsError: {ex}")
        return None

def polars_eager_writer(buffer: IO, df: pl.DataFrame) -> None:
    df.write_parquet(buffer)
    buffer.seek(0)

def polars_lazy_reader(buffer: IO) -> pl.LazyFrame | None:
    # any error will not be raised until LazyFrame.collect()...
    return pl.scan_parquet(buffer)

def polars_lazy_collection_reader(buffers: list[IO]) -> pl.LazyFrame | None:
    # any error will not be raised until LazyFrame.collect()...
    return pl.scan_parquet(buffers)

def polars_lazy_writer(buffer: IO, lf: pl.LazyFrame) -> None:
    lf.sink_parquet(buffer)
    buffer.seek(0)