import numpy as np
import pandas as pd
import geopandas as gpd


def _get_coords(gdf):
    """
    Get array containing x,y coordinates from GeoDataFrame

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        a
    Returns
    -------
    type : np.array
        array containing x and y values
    """

    if "x" and "y" not in gdf:
        raise ValueError("x and y attributes not present in GeoDataFrame")
    # elif gdf does not contain point geoms:
    #    raise ValueError("geometry column must be of type Point")
    else:
        return gdf[["x", "y"]].values


def _random_points(bounds, p):
    """
    Calculate p random points based on GeoDataFrame bounds

    Parameters
    ----------
    bounds : array_like
        bounds of GeoDataFrame
    p : int
        number of random points to generate points within bounds

    Returns
    -------
    type : np.array
        array containing random points
    """
    return np.array(
        [
            np.random.uniform(bounds[0], bounds[2], p),
            np.random.uniform(bounds[1], bounds[3], p),
        ]
    ).T


def _calculate_mid_points(bounds):
    """
    Calculate middle points based on the geometry bounds

    Parameters
    ----------
    bounds : array_like
        array containing xmin, ymin, xmax, ymax

    Returns
    -------
    type: np.array
        x_mids : mid points of x values
        y_mids : mid points of y values
    """

    # Calculate mid points for x and y bound coords
    x_mids = (bounds[:, 0] + bounds[:, 2]) / 2.0
    y_mids = (bounds[:, 1] + bounds[:, 3]) / 2.0

    return x_mids, y_mids


def _get_points(gdf, method, bounds, n=None, p=None):
    """
    Get GeoDataFrame point coordinates from GeoDataFrame using a defined method

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        GeoDataFrame to get point coordinates from
    method : str
        method
    bounds : array_like
        bounds of a GeoDataFrame
    n : int
        number of random points to generate
    p : int
        number of random points to generate points within bounds
    Returns
    -------
    type : gpd.GeoDataFrame
        GeoDataFrame containing point coordinates
    """

    gdf = gdf.copy()

    if "x" and "y" not in gdf:
        print(
            "x and y not in GeoDataFrame, \
            estimating coordinates using %s"
            % method
        )

        if bounds is None:
            bounds = gdf.bounds.to_numpy()

        if method == "mid points":
            from geobootstrap.utils import _calculate_mid_points

            x_mids, y_mids = _calculate_mid_points(bounds)
            points = np.array([x_mids, y_mids]).T
            df = pd.DataFrame(points, columns=["x", "y"])

            return gpd.GeoDataFrame(
                df, geometry=gpd.points_from_xy(x_mids, y_mids), crs=gdf.crs
            )

        elif method == "random points":
            """
            if n or p is None:
                raise ValueError("n and p must be specified
                with random points")
            """
            gdf_points = _random_points_sample(gdf, bounds, p=p, n=n)

        else:
            raise ValueError(
                "Only 'mid points' and \
                'random points' are supported"
            )

        return gdf_points


def _random_points_sample(gdf, bounds=None, n=1, p=1000):
    """
    Gets n random points for every polygon in a GeoDataFrame

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        GeoDataFrame containing polygons
    bounds : array_like
        GeoDataFrame bounds
    n : int
        number of random points to generate
    p : int
        number of random points to generate points within bounds

    Returns
    ---------
    type : gpd.GeoDataFrame
    """

    # if gdf does not contain polygons:
    #    raise TypeError("")

    gdfs = []

    if bounds is None:
        bounds = gdf.bounds.to_numpy()

    for i in range(len(gdf)):
        g = gdf.iloc[[i]]
        # Initially create p random points based on bounds
        points = _random_points(bounds[i], p)
        df = pd.DataFrame(data=points, columns=["x", "y"])
        gdf_point = gpd.GeoDataFrame(
            df, geometry=gpd.points_from_xy(df["x"], df["y"]), crs=gdf.crs
        )

        # Then clip the points to the polygon boundary
        gdf_point = gdf_point.clip(g)
        # And sample n points within polygon
        gdf_point = gdf_point.sample(n)
        # Set index
        gdf_point = gdf_point.set_index(g.index)
        gdfs.append(gdf_point)

    return pd.concat(gdfs)


def _poly_to_points(
    gdf,
    method="mid points",
    uid=None,
    bounds=None,
    p=1000,
    n=1,
    join=False,
):
    """
    Transforms polygon geometries to point ones using a method

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        GeoDataFrame containing polygons
    method : str
        method for generating coordinates for each polygon
    uid : str
        GeoDataFrame unique identifier
    bounds : array_like
        GeoDataFrame bounds
    p : int
        number of random points to generate within bounds
    n : int
        number of random points to generate within polygon (default 1)
    join :
        whether to spatially join original data back

    Returns
    ---------
    type : gpd.GeoDataFrame
    """

    if "x" and "y" not in gdf:
        print(
            "x and y attributes not in GeoDataFrame, \
            estimating coordinates using %s"
            % method
        )

        gdf_points = _get_points(gdf, method, bounds, n, p)

    else:
        gdf_points = gpd.GeoDataFrame(
            geometry=gpd.points_from_xy(gdf["x"], gdf["y"]), crs=gdf.crs
        )

    if join is True:
        gdf = gpd.sjoin(gdf_points, gdf, op="intersects")
        return gdf

    else:
        return gdf_points
