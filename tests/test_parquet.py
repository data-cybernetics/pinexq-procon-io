from io import BytesIO

import pytest

pd = pytest.importorskip("pandas")
pytest.importorskip("pyarrow")

from pinexq.procon.io.parquet import (
    parquet_buffer_reader,
    parquet_buffer_writer,
    parquet_media_type,
)


def test_parquet_media_type():
    assert parquet_media_type == "application/vnd.apache.parquet"


def test_parquet_round_trip():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4.0, 5.0, 6.0]})
    buf = BytesIO()
    parquet_buffer_writer(buf, df)
    result = parquet_buffer_reader(buf)
    assert result is not None
    pd.testing.assert_frame_equal(result, df)


def test_parquet_writer_seeks_to_zero():
    df = pd.DataFrame({"x": [1]})
    buf = BytesIO()
    parquet_buffer_writer(buf, df)
    assert buf.tell() == 0


def test_parquet_reader_invalid_data():
    buf = BytesIO(b"this is not parquet data")
    result = parquet_buffer_reader(buf)
    assert result is None
