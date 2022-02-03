from scipy.spatial.distance import cdist
from geobootstrap.utils import _get_coords
from geobootstrap.kernel import _kernel


def geobootstrap(
    gdf1,
    gdf2,
    coords1,
    coords2,
    n=1000,
    metric="euclidean",
    kernel="gaussian",
    bandwidth=1000,
    col=None,
):
    """
    Parameters
    ----------
    gdf1 : gpd.GeoDataFrame
        GeoDataFrame to calculate distances from
    gdf1 : gpd.GeoDataFrame
        GeoDataFrame to calculate distances to
    coords1 : array_like (optional)
        coordinates for geodataframe GeoDataFrame to calculate distances
    coords2 : gpd.GeoDataFrame (optional)
    n : int
        how many resamples with replacement to return
        coordinates for geodataframe GeoDataFrame to calculate distances
    metric : str
        how to calculate distances between coordinates
    kernel : str
        kernel function
    bandwidth : int
       bandwidth value in metres
    col : str (optional)
        whether to return list of gpd.GeoDataFrames or arrays, based on column

    Returns
    -------
    type : list
        either a list of pd.DataFrames or np.array
    """

    if coords1 is None:
        coords1 = _get_coords(gdf1)
    if coords2 is None:
        coords2 = _get_coords(gdf2)

    gs = []
    for i in range(len(gdf2)):
        coord = coords2[i]
        dist = cdist([coord], coords1, metric).reshape(-1)
        k = _kernel(kernel, dist, bandwidth)
        gdf1["weight"] = k
        g = gdf1.sample(n=n, weights="weight", replace=True)

        if col is not None:
            g = g[col].to_numpy()
            gs.append(g)
        else:
            gs.append(g)
    return gs
