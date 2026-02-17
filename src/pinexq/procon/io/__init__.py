"""I/O utilities for the pinexq.procon ecosystem.

Provides serialization and deserialization helpers for JSON (via Pydantic),
Apache Parquet, and Matplotlib figures. Parquet and Matplotlib support is
available through optional extras — see the sub-modules
:mod:`pinexq.procon.io.parquet` and :mod:`pinexq.procon.io.matplotlib`.
"""

import json
import logging
from typing import IO, TypeVar

from pydantic import BaseModel

LOG = logging.getLogger(__name__)

ModelT = TypeVar("ModelT", bound=BaseModel)


def dict_2_json_writer(file: IO, data: dict) -> None:
    """Serialize a dictionary to *file* as pretty-printed JSON."""
    # noinspection PyTypeChecker
    json.dump(data, file, indent=2)


def base_model_dump_json(file: IO, model: BaseModel) -> None:
    """Serialize a Pydantic model to *file* as pretty-printed JSON."""
    js = model.model_dump_json(indent=2)
    file.write(js)


def pydantic_reader(model: type[ModelT]):
    """Return a reader function that deserializes JSON from a file into *model*.

    Usage::

        read_my_model = pydantic_reader(MyModel)
        instance = read_my_model(open("data.json"))
    """

    def _inner(file: IO) -> ModelT:
        return model.model_validate_json(file.read())

    return _inner
