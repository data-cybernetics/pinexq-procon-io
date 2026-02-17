"""Matplotlib I/O helpers (requires the ``matplotlib`` extra).

Provides utilities for serializing Matplotlib figures to byte buffers.
"""

from typing import IO

from matplotlib.figure import Figure

plotly_media_type = "application/vnd.plotly.v1+json"


def figure_to_png_buffer(buffer: IO, figure: Figure) -> None:
    """Write a Matplotlib *figure* to *buffer* as PNG bytes.

    The buffer position is reset to the beginning after writing so it can
    be read back immediately.
    """
    figure.savefig(buffer, format='png')
    buffer.seek(0)
