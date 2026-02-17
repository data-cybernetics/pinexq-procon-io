"""Matplotlib I/O helpers (requires the ``matplotlib`` extra).

Provides a writer callable for serializing Matplotlib figures to PNG byte
buffers. The function conforms to the dataslot annotation signature::

    @dataslot.returns(media_type=MediaTypes.PNG, writer=figure_to_png_buffer)
"""

from typing import IO

from matplotlib.figure import Figure


def figure_to_png_buffer(buffer: IO, figure: Figure) -> None:
    """Write a Matplotlib *figure* to *buffer* as PNG bytes.

    Conforms to the ``WriterType`` signature expected by
    :meth:`dataslot.output` and :meth:`dataslot.returns`::

        @dataslot.returns(media_type=MediaTypes.PNG, writer=figure_to_png_buffer)

    The buffer position is reset to the beginning after writing so it can
    be read back immediately.
    """
    figure.savefig(buffer, format='png')
    buffer.seek(0)
