"""Plotly JSON I/O helpers (requires the ``plotly`` extra).

Provides a writer callable that converts a pandas DataFrame into Plotly-
compatible JSON and writes it to a file-like object. Uses scipy sparse arrays
internally for efficient column extraction::

    @dataslot.returns(media_type=plotly_media_type, writer=plotly_json_writer)
"""

import json
from typing import IO, Dict

import numpy as np
import pandas as pd
from scipy import sparse

plotly_media_type = "application/vnd.plotly.v1+json"


def dataframe_to_dict(df: pd.DataFrame, return_sparse=False) -> Dict[str, np.ndarray | sparse.coo_array]:
    """Convert a pandas DataFrame to a dictionary of numpy arrays or sparse arrays.

    Args:
        df: The DataFrame to convert.
        return_sparse: If ``True``, return :class:`scipy.sparse.coo_array`
            instances instead of dense numpy arrays.
    """
    if return_sparse:
        return {col: sparse.coo_array(df[col].to_numpy()) for col in df.columns}
    else:
        return {col: df[col].to_numpy() for col in df.columns}


def to_plotly_json(result_df: pd.DataFrame) -> dict:
    """Convert a pandas DataFrame into a Plotly figure dictionary.

    Each column becomes a scatter trace with the row index as x-axis.

    Args:
        result_df: The DataFrame whose columns will be plotted.

    Returns:
        A dict with ``"data"`` and ``"layout"`` keys conforming to the Plotly
        JSON schema.
    """
    result = dataframe_to_dict(result_df.copy(), return_sparse=True)
    pl_data_list = []
    for name, coo_array in result.items():
        plotly_data = {
            "type": "scatter",
            "x": list(range(coo_array.shape[0])),
            "y": coo_array.toarray().squeeze().tolist(),
            "name": name
        }
        pl_data_list.append(plotly_data)

    layout = {
        "title": "Simulation Results",
        "xaxis": {
            "title": "time"
        },
    }
    return {
        "data": pl_data_list,
        "layout": layout
    }


def plotly_json_writer(file: IO, df: pd.DataFrame) -> None:
    """Write a pandas DataFrame to *file* as Plotly JSON.

    Converts the DataFrame into a Plotly figure dictionary via
    :func:`to_plotly_json` and serializes it as JSON.

    Conforms to the ``WriterType`` signature expected by
    :meth:`dataslot.output` and :meth:`dataslot.returns`::

        @dataslot.returns(media_type=plotly_media_type, writer=plotly_json_writer)

    Args:
        file: A writable file-like object.
        df: The DataFrame to convert and write.
    """
    json.dump(to_plotly_json(df), file, indent=2)
