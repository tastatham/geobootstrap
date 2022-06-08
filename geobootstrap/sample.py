import math
import warnings
import numpy as np
import scipy.spatial as sp
from geobootstrap.utils import _get_coords
from geobootstrap.kernel import _kernel


def geobootstrap(
    gdf1,
    gdf2,
    coords1=None,
    coords2=None,
    r=1000,
    kernel="gaussian",
    metric="euclidean",
    bandwidth=1000,
    fixed=True,
    check=False
):
    """
    Bootstrap a GeoDataFrame using defined kernel weights,
    determined by a distance decay function to another GeoDataFrame

    Parameters
    ----------
    gdf1 : gpd.GeoDataFrame
        GeoDataFrame to calculate distances from
    gdf2 : gpd.GeoDataFrame
        GeoDataFrame to calculate distances to
    coords1: array_like
        two dimensional array containing x, y values for sources
   coords2: array_like
        two dimensional array containing x, y values for gdf2
    r : int
        how many resamples with replacement to return
    kernel : str
        kernel distance-decay function
    metric : str
        how to calculate distances between coordinates
    bandwidth : int
       bandwidth or fixed distance
    fixed: bool
        whether to apply a fixed or adaptive (knn) bandwidth
    check: bool
        whether to check the bandwidth set allows at least 1 knn

    Returns
    -------
    type : list
        list of pd.DataFrames
    """

    if fixed is False:
        raise ValueError("Only fixed bandwidths are currently supported")

    if coords1 is None:
        coords1 = _get_coords(gdf1)
    if coords2 is None:
        coords2 = _get_coords(gdf2)

    if check is True:
        bandwidth = _check_bandwidth(coords1, coords2, bandwidth, fix=False)

    dist = sp.distance.cdist(coords2, coords1, metric)
    ks = _kernel(kernel, dist, bandwidth, fixed)

    return [gdf1.sample(n=r, weights=k, replace=True) for k in ks]


def _check_bandwidth(coords1, coords2, bandwidth, fix=False):

    """A function that checks whether the bandwidth set
    allows for pooling from at least 1 neighbour

    Parameters
    ----------
    coords1: np.array
        array containing x,y coordinate pairs
    coords2: np.array
        array containing x,y coordinate pairs
    bandwidth: int
        fixed distance for finding neighbours
    fix: bool
        to replace the bandwidth value, if less than the minimum distance
        for all zones to have neighbours

    Returns
    -------
    int: (optional)
        bandwidth

    """

    # Create KD-tree
    tree = sp.cKDTree(coords1)
    # Get number of neighbours within bandwidth
    k = tree.query_ball_point(coords2, r=bandwidth, return_length=True)
    # If any observation has less than 1 neighbour,
    # then calculate the minimum distance for each to have neighbours
    if np.any(k <= 1) == True:
        d, i = tree.query(coords2, k=1)
        max_d = math.ceil(d.max())
        if fix is True:
            warnings.warn(
                "Using minimum bandwidth:"
                f"{max_d} to ensure all zones have neighbours"
            )
            return max_d

        else:
            raise ValueError(
                "The bandwidth set is less than the distance to the"
                f"nearest neighbour of {max_d}"
            )
