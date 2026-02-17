import json
from io import StringIO

import pytest

pd = pytest.importorskip("pandas")
np = pytest.importorskip("numpy")
sparse = pytest.importorskip("scipy.sparse")

from pinexq.procon.io.plotly import (
    dataframe_to_dict,
    plotly_json_writer,
    plotly_media_type,
    to_plotly_json,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame({"col_a": [1.0, 2.0, 3.0], "col_b": [4.0, 5.0, 6.0]})


def test_plotly_media_type():
    assert plotly_media_type == "application/vnd.plotly.v1+json"


def test_dataframe_to_dict_dense(sample_df):
    result = dataframe_to_dict(sample_df, return_sparse=False)
    assert set(result.keys()) == {"col_a", "col_b"}
    assert isinstance(result["col_a"], np.ndarray)
    np.testing.assert_array_equal(result["col_a"], [1.0, 2.0, 3.0])


def test_dataframe_to_dict_sparse(sample_df):
    result = dataframe_to_dict(sample_df, return_sparse=True)
    assert set(result.keys()) == {"col_a", "col_b"}
    assert isinstance(result["col_a"], sparse.coo_array)
    np.testing.assert_array_equal(result["col_a"].toarray().squeeze(), [1.0, 2.0, 3.0])


def test_to_plotly_json_structure(sample_df):
    fig = to_plotly_json(sample_df)
    assert "data" in fig
    assert "layout" in fig
    assert len(fig["data"]) == 2
    assert fig["layout"]["title"] == "Simulation Results"
    assert fig["layout"]["xaxis"]["title"] == "time"


def test_to_plotly_json_traces(sample_df):
    fig = to_plotly_json(sample_df)
    trace_names = {t["name"] for t in fig["data"]}
    assert trace_names == {"col_a", "col_b"}
    for trace in fig["data"]:
        assert trace["type"] == "scatter"
        assert trace["x"] == [0, 1, 2]


def test_to_plotly_json_does_not_mutate_input(sample_df):
    original = sample_df.copy()
    to_plotly_json(sample_df)
    pd.testing.assert_frame_equal(sample_df, original)


def test_plotly_json_writer(sample_df):
    buf = StringIO()
    plotly_json_writer(buf, sample_df)
    buf.seek(0)
    parsed = json.loads(buf.read())
    assert "data" in parsed
    assert "layout" in parsed
    assert len(parsed["data"]) == 2
