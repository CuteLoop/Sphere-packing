import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon

def plot_shape(
    ax,
    geom,
    *,
    edgecolor='black',
    facecolor='none',
    linewidth=2,
    alpha=1.0
):
    if isinstance(geom, Polygon):
        x, y = geom.exterior.xy
        ax.fill(
            x, y,
            edgecolor=edgecolor,
            facecolor=facecolor,
            linewidth=linewidth,
            alpha=alpha
        )
    elif isinstance(geom, MultiPolygon):
        for g in geom.geoms:
            plot_shape(
                ax, g,
                edgecolor=edgecolor,
                facecolor=facecolor,
                linewidth=linewidth,
                alpha=alpha
            )
    else:
        raise TypeError(f"Unsupported geometry: {type(geom)}")
