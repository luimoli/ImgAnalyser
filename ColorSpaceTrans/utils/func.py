import numpy as np

def stack(arr):
    """[Stacks arrays in sequence along the last axis (tail).]
    Args:
        arr ([array_like]): [arrays to perform the stacking.]
    Returns:
        [type]: [description]
    """
    return np.concatenate([x[..., None] for x in arr], axis=-1)


def split(arr):
    """[Splits arrays in sequence along the last axis (tail).]
    Args:
        arr ([array_like]): [Array to perform the splitting.]
    Returns:
        [type]: [description]
    """
    return [arr[..., x] for x in range(arr.shape[-1])]

def dot_vector(matrix, vector):
    return np.einsum('ij,...j->...i', matrix, vector)