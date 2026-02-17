import json
from io import StringIO

import pytest
from pydantic import BaseModel, ValidationError

from pinexq.procon.io import dict_2_json_writer, pydantic_reader, pydantic_writer


class SampleModel(BaseModel):
    name: str
    value: int


def test_dict_2_json_writer():
    buf = StringIO()
    data = {"key": "value", "num": 42}
    dict_2_json_writer(buf, data)
    buf.seek(0)
    assert json.loads(buf.read()) == data


def test_dict_2_json_writer_indent():
    buf = StringIO()
    dict_2_json_writer(buf, {"a": 1})
    buf.seek(0)
    raw = buf.read()
    # indent=2 produces multiline output
    assert "\n" in raw
    assert "  " in raw


def test_dict_2_json_writer_nested():
    buf = StringIO()
    data = {"outer": {"inner": [1, 2, 3]}, "flag": True}
    dict_2_json_writer(buf, data)
    buf.seek(0)
    assert json.loads(buf.read()) == data


def test_pydantic_writer():
    buf = StringIO()
    model = SampleModel(name="test", value=99)
    pydantic_writer(buf, model)
    buf.seek(0)
    parsed = json.loads(buf.read())
    assert parsed == {"name": "test", "value": 99}


def test_pydantic_reader_round_trip():
    buf = StringIO()
    original = SampleModel(name="round-trip", value=7)
    pydantic_writer(buf, original)
    buf.seek(0)
    reader = pydantic_reader(SampleModel)
    restored = reader(buf)
    assert restored == original


def test_pydantic_reader_invalid_json():
    buf = StringIO("not valid json")
    reader = pydantic_reader(SampleModel)
    with pytest.raises(ValidationError):
        reader(buf)
