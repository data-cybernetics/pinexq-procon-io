"""I/O utilities for the pinexq.procon ecosystem.

Provides reader and writer callables for common data formats that plug directly
into :class:`pinexq.procon.dataslots.dataslot` annotations.

Writers follow the signature ``(file: IO, data: Any) -> None`` and are used
with :meth:`dataslot.output` and :meth:`dataslot.returns`.

Readers follow the signature ``(file: IO) -> Any`` and are used with
:meth:`dataslot.input`.

Parquet and Matplotlib support is available through optional extras — see
:mod:`pinexq.procon.io.parquet` and :mod:`pinexq.procon.io.matplotlib`.
"""

import json
import logging
from typing import IO, TypeVar

from pydantic import BaseModel

LOG = logging.getLogger(__name__)

ModelT = TypeVar("ModelT", bound=BaseModel)


def dict_2_json_writer(file: IO, data: dict) -> None:
    """Serialize a dictionary to *file* as pretty-printed JSON.

    Conforms to the ``WriterType`` signature expected by
    :meth:`dataslot.output` and :meth:`dataslot.returns`::

        @dataslot.output("result", media_type=MediaTypes.JSON, writer=dict_2_json_writer)
    """
    # noinspection PyTypeChecker
    json.dump(data, file, indent=2)


def base_model_dump_json(file: IO, model: BaseModel) -> None:
    """Serialize a Pydantic model to *file* as pretty-printed JSON.

    Conforms to the ``WriterType`` signature expected by
    :meth:`dataslot.output` and :meth:`dataslot.returns`::

        @dataslot.returns(media_type=MediaTypes.JSON, writer=base_model_dump_json)
    """
    js = model.model_dump_json(indent=2)
    file.write(js)


def pydantic_reader(model: type[ModelT]):
    """Return a reader function that deserializes JSON from a file into *model*.

    The returned callable conforms to the ``ReaderType`` signature expected by
    :meth:`dataslot.input`::

        @dataslot.input("config", media_type=MediaTypes.JSON, reader=pydantic_reader(MyModel))
    """

    def _inner(file: IO) -> ModelT:
        return model.model_validate_json(file.read())

    return _inner
