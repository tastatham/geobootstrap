from scipy.spatial.distance import cdist
from geobootstrap.utils import _get_coords
from geobootstrap.kernel import _kernel


def geobootstrap(
    gdf1,
    gdf2,
    r=1000,
    kernel="gaussian",
    metric="euclidean",
    bandwidth=1000,
):
    """
    Bootstrap a GeoDataFrame using defined kernel weights,
    determined by a distance decay function to another GeoDataFrame

    Parameters
    ----------
    gdf1 : gpd.GeoDataFrame
        GeoDataFrame to calculate distances from
    gdf1 : gpd.GeoDataFrame
        GeoDataFrame to calculate distances to
    r : int
        how many resamples with replacement to return
    kernel : str
        kernel distance-decay function
    metric : str
        how to calculate distances between coordinates
    bandwidth : int
       bandwidth or fixed distance

    Returns
    -------
    type : list
        list of pd.DataFrames
    """

    coords1, coords2 = _get_coords(gdf1), _get_coords(gdf2)

    dist = cdist(coords2, coords1, metric)
    ks = _kernel(kernel, dist, bandwidth)

    return [gdf1.sample(n=r, weights=k, replace=True) for k in ks]
