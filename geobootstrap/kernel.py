import numpy as np


def _kernel(function, dist, bandwidth, fixed=True):
    """
    Function that defines kernel for geobootstrapping
    using distance and a fixed bandwidth

    In general, a fixed bandwidth suits more regular sample configurations,
    whereas an adaptive bandwidth suits irregular sample configurations

    Parameters
    ----------
    function : str
        Kernel function specified
    dist : array_like
        Distance vector
    bandwidth : int
        fixed bandwidth in metres
    fixed : bool
        whether to return a fixed or adaptive bandwidth

    Returns
    -------
    s

    """

    if fixed is True:
        return _kernel_funcs(function, zs=dist / bandwidth)
    else:
        raise ValueError("Only fixed bandwidths are currently supported")


def _kernel_funcs(function, zs):
    """
    modified from
    https://github.com/pysal/mgwr/blob/eef4f707fc2d34245c6cf0afeb85d742fdb90af5/mgwr/kernels.py#L65

    Parameters
    ----------
    function : str
        kernel function name
    zs : int
        distance / bandwidth

    Returns
    -------
    s

    """

    if function == "triangular":
        return 1 - zs
    elif function == "uniform":
        return np.ones(zs.shape) * 0.5
    elif function == "quadratic":
        return (3.0 / 4) * (1 - zs ** 2)
    elif function == "quartic":
        return (15.0 / 16) * (1 - zs ** 2) ** 2
    elif function == "gaussian":
        return np.exp(-0.5 * (zs) ** 2)
    elif function == "bisquare":
        return (1 - (zs) ** 2) ** 2
    elif function == "exponential":
        return np.exp(-zs)
    else:
        raise ValueError("Unsupported kernel function", function)
