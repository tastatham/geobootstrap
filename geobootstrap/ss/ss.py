import numpy as np


def exterior_coords(gdf):
    """
    Return exterior coordinates for a GeoDataFrame

    Parameters
    ----------
    gdf : gpd.GeoDataFrame

    Returns
    -------
    array_like
    """
    return np.array(list(zip(*gdf.geometry[0].exterior.coords.xy)))
