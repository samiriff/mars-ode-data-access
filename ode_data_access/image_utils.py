import numpy as np
from numpy.lib.stride_tricks import as_strided
from warnings import warn
from ode_data_access.autocropper import AutoCropper
import sys


def view_as_blocks(arr_in, block_shape):
    """
    Based on https://stackoverflow.com/questions/8070349/using-numpy-stride-tricks-to-get-non-overlapping-array-blocks/28207538#28207538
    Block view of the input n-dimensional array (using re-striding).
    Blocks are non-overlapping views of the input array.
    Parameters
    ----------
    arr_in : ndarray
        N-d input array.
    block_shape : tuple
        The shape of the block. Each dimension must divide evenly into the
        corresponding dimensions of `arr_in`.
    Returns
    -------
    arr_out : ndarray
        Block view of the input array.  If `arr_in` is non-contiguous, a copy
        is made.
    Examples
    --------
    >>> import numpy as np
    >>> from skimage.util.shape import view_as_blocks
    >>> A = np.arange(4*4).reshape(4,4)
    >>> A
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])
    >>> B = view_as_blocks(A, block_shape=(2, 2))
    >>> B[0, 0]
    array([[0, 1],
           [4, 5]])
    >>> B[0, 1]
    array([[2, 3],
           [6, 7]])
    >>> B[1, 0, 1, 1]
    13
    >>> A = np.arange(4*4*6).reshape(4,4,6)
    >>> A  # doctest: +NORMALIZE_WHITESPACE
    array([[[ 0,  1,  2,  3,  4,  5],
            [ 6,  7,  8,  9, 10, 11],
            [12, 13, 14, 15, 16, 17],
            [18, 19, 20, 21, 22, 23]],
           [[24, 25, 26, 27, 28, 29],
            [30, 31, 32, 33, 34, 35],
            [36, 37, 38, 39, 40, 41],
            [42, 43, 44, 45, 46, 47]],
           [[48, 49, 50, 51, 52, 53],
            [54, 55, 56, 57, 58, 59],
            [60, 61, 62, 63, 64, 65],
            [66, 67, 68, 69, 70, 71]],
           [[72, 73, 74, 75, 76, 77],
            [78, 79, 80, 81, 82, 83],
            [84, 85, 86, 87, 88, 89],
            [90, 91, 92, 93, 94, 95]]])
    >>> B = view_as_blocks(A, block_shape=(1, 2, 2))
    >>> B.shape
    (4, 2, 3, 1, 2, 2)
    >>> B[2:, 0, 2]  # doctest: +NORMALIZE_WHITESPACE
    array([[[[52, 53],
             [58, 59]]],
           [[[76, 77],
             [82, 83]]]])
    """
    if not isinstance(block_shape, tuple):
        raise TypeError('block needs to be a tuple')

    block_shape = np.array(block_shape)
    if (block_shape <= 0).any():
        raise ValueError("'block_shape' elements must be strictly positive")

    if block_shape.size != arr_in.ndim:
        raise ValueError("'block_shape' must have the same length "
                         "as 'arr_in.shape'")

    arr_shape = np.array(arr_in.shape)
    if (arr_shape % block_shape).sum() != 0:
        raise ValueError("'block_shape' is not compatible with 'arr_in'")

    # -- restride the array to build the block view

    if not arr_in.flags.contiguous:
        warn(RuntimeWarning("Cannot provide views on a non-contiguous input "
                            "array without copying."))

    arr_in = np.ascontiguousarray(arr_in)

    new_shape = tuple(arr_shape // block_shape) + tuple(block_shape)
    new_strides = tuple(arr_in.strides * block_shape) + arr_in.strides

    arr_out = as_strided(arr_in, shape=new_shape, strides=new_strides)

    return arr_out


def is_black(img, threshold=20):
    width, height = img.shape
    for row in (height // 2 - threshold, height // 2 + threshold):
        if (img[row][width // 2 - threshold] == 0):
            return True
        if (img[row][width // 2 + threshold] == 0):
            return True

    for col in (width // 2 - threshold, width // 2 + threshold):
        if (img[height // 2 - threshold][col] == 0):
            return True
        if (img[height // 2 + threshold][col] == 0):
            return True

    return False


def align_and_crop(img, max_border_size=200, safety_margin=0, tolerance=10):
    ac = AutoCropper(img)
    ac.max_border_size = max_border_size 	# defaults to 300
    ac.safety_margin = safety_margin 		# defaults to 4, removes extra pixels from the sides to make sure no black remains
    ac.tolerance = tolerance     			# defaults to 4, a gray value is more likely to be considered black when you increase the tolerance
    result = ac.autocrop()
    return result


def query_yes_no(question, default="yes"):
    """
    Ask a yes/no question via raw_input() and return the answer
    Written by Trent Mick under the MIT license, see:
    https://code.activestate.com/recipes/577058-query-yesno/

    @param question: A string that is presented to the user
    @param default: The presumed answer if the user just hits <Enter>.
                    It must be "yes" (the default), "no" or None (meaning
                    an answer is required of the user)
    @return The "answer", i.e., either "yes" or "no"
    """

    valid = {"yes": "yes", "y": "yes", "ye": "yes",
             "no": "no", "n": "no"}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")
