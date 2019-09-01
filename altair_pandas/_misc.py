import altair as alt
from typing import Iterable, Union, List, Optional

toltipList = List[alt.Tooltip]


def scatter_matrix(
    df,
    color: Union[str, Iterable, None] = None,
    alpha: float = 1.0,
    tooltip: Union[List[str], toltipList, None] = None,
    **kwargs
):
    """ plots a scatter matrix

    At the moment does not support neither histogram nor kde;
    Uses f-f scatterplots instead. Interactive and with a cusotmizable
    tooltip

    Parameters
    ----------
    df : DataFame
        DataFame to be used for scatterplot. Only numeric columns will be included.
    color : string or iterable [optional]
        Can be a column name, specific color value (hex, webcolors), or an array
        of values to be used.
    alpha : float
        Opacity of the markers, within [0,1]
    tooltip: list [optional]
        List of specific column names or alt.Tooltip objects. If none (default),
        will show all columns.
    """
    dfc = df.copy()  # otherwise passing array will be preserved
    cols = dfc._get_numeric_data().columns.astype(str).tolist()
    tooltip = tooltip or dfc.columns.astype(str).tolist()

    if color is None:
        pass
    elif isinstance(color, str):
        if color in df.columns.astype(str).tolist():
            if "colormap" in kwargs:
                color = alt.Color(color, scale=alt.Scale(scheme=kwargs.get("colormap")))
            else:
                pass
        else:
            color = alt.value(color)
    elif hasattr(color, "__len__") and len(color) == len(df):
        colname = "__color__"

        if colname in dfc.columns.astype(str):
            raise ValueError("Column `__color__` already exists")
        dfc[colname] = color

        if "colormap" in kwargs:
            color = alt.Color(colname, scale=alt.Scale(scheme=kwargs.get("colormap")))
        else:
            color = colname
    else:
        raise ValueError(color)

    chart = (
        alt.Chart(dfc)
        .mark_circle()
        .encode(
            x=alt.X(alt.repeat("column"), type="quantitative"),
            y=alt.X(alt.repeat("row"), type="quantitative"),
            opacity=alt.value(alpha),
            tooltip=tooltip,
        )
        .properties(width=150, height=150)
    )

    if color:
        chart = chart.encode(color=color)

    return chart.repeat(row=cols, column=cols[::-1]).interactive()
