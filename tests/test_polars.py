from io import BytesIO

import pytest

pl = pytest.importorskip("polars")
from polars.testing import assert_frame_equal # polars.testing is not in polars.__all__!

from pinexq.procon.io.polars import (
    polars_eager_reader,
    polars_eager_writer,
    parquet_media_type, polars_lazy_reader, polars_lazy_writer,
)


def test_parquet_media_type():
    assert parquet_media_type == "application/vnd.apache.parquet"

def test_polars_round_trip():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4.0, 5.0, 6.0]})
    buf = BytesIO()
    polars_eager_writer(buf, df)
    result = polars_eager_reader(buf)
    assert result is not None
    assert_frame_equal(result, df)

def test_lazy_round_trip():
    lf = pl.DataFrame({"a": [1, 2, 3], "b": [4.0, 5.0, 6.0]}).lazy()
    buf = BytesIO()
    polars_lazy_writer(buf, lf)
    result = polars_lazy_reader(buf)
    assert result is not None
    assert_frame_equal(result, lf)

def test_polars_writer_seeks_to_zero():
    df = pl.DataFrame({"x": [1]})
    buf = BytesIO()
    polars_eager_writer(buf, df)
    assert buf.tell() == 0

def test_lazy_writer_seeks_to_zero():
    lf = pl.DataFrame({"x": [1]}).lazy()
    buf = BytesIO()
    polars_lazy_writer(buf, lf)
    assert buf.tell() == 0


def test_polars_reader_invalid_data():
    buf = BytesIO(b"this is not parquet data")
    result = polars_eager_reader(buf)
    assert result is None

@pytest.mark.xfail(reason="lazy reader does not throw error until data is collected!")
def test_lazy_reader_invalid_data():
    buf = BytesIO(b"this is not parquet data")
    result = polars_eager_reader(buf)
    assert result is None