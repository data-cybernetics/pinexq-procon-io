from io import BytesIO

import pytest

mpl_figure = pytest.importorskip("matplotlib.figure")

from pinexq.procon.io.matplotlib import figure_to_png_buffer


def test_figure_to_png_buffer():
    fig = mpl_figure.Figure()
    ax = fig.add_subplot()
    ax.plot([1, 2, 3], [4, 5, 6])

    buf = BytesIO()
    figure_to_png_buffer(buf, fig)
    # PNG files start with the magic bytes \x89PNG
    assert buf.read(4) == b"\x89PNG"


def test_figure_to_png_buffer_seeks_to_zero():
    fig = mpl_figure.Figure()
    buf = BytesIO()
    figure_to_png_buffer(buf, fig)
    assert buf.tell() == 0
