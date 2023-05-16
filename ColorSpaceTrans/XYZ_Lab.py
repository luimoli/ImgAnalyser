import numpy as np

from .utils.func import split, stack
from .utils.constants import const
from .XYZ_xyY import xyy2xyz, xy2xyy

def xyz2lab(XYZ, illuminant_mode='d65'):
    if illuminant_mode.lower() == 'd65':
        illuminant=const.ILLUMINANTS['D65']
    elif illuminant_mode.lower() == 'd50':
        illuminant=const.ILLUMINANTS['D50']
    else:
        raise ValueError(illuminant_mode)
    
    XYZ_r = xyy2xyz(xy2xyy(illuminant))

    XYZ_f = XYZ / XYZ_r
    XYZ_f = np.where(XYZ_f > const.CIE_E, np.power(XYZ_f, 1 / 3), (const.CIE_K * XYZ_f + 16) / 116)
    X_f, Y_f, Z_f = split(XYZ_f)

    L = 116 * Y_f - 16
    a = 500 * (X_f - Y_f)
    b = 200 * (Y_f - Z_f)

    Lab = stack((L, a, b))

    return Lab

def lab2xyz(Lab, illuminant_mode='d65'):
    """
    Converts from *CIE Lab* colourspace to *CIE XYZ* tristimulus values.
    """
    if illuminant_mode.lower() == 'd65':
        illuminant=const.ILLUMINANTS['D65']
    elif illuminant_mode.lower() == 'd50':
        illuminant=const.ILLUMINANTS['D50']
    else:
        raise ValueError(illuminant_mode)

    L, a, b = split(Lab)
    XYZ_r = xyy2xyz(xy2xyy(illuminant))

    f_y = (L + 16) / 116
    f_x = a / 500 + f_y
    f_z = f_y - b / 200

    x_r = np.where(f_x ** 3 > const.CIE_E, f_x ** 3, (116 * f_x - 16) / const.CIE_K)
    y_r = np.where(L > const.CIE_K * const.CIE_E, ((L + 16) / 116) ** 3, L / const.CIE_K)
    z_r = np.where(f_z ** 3 > const.CIE_E, f_z ** 3, (116 * f_z - 16) / const.CIE_K)

    XYZ = stack((x_r, y_r, z_r)) * XYZ_r

    return XYZ

if __name__ == '__main__':
    randxyz = np.float32(np.random.random((1080,1920,3)))

    # # verify XYZ_to_Lab
    # v0 = colour.XYZ_to_Lab(randxyz)
    # v1 = xyz2lab(randxyz)
    # diff = v0 - v1
    # print(diff.max(),diff.mean())

    # # # verify Lab_to_XYZ
    # randlab = colour.XYZ_to_Lab(randxyz)
    # cs = colour.Lab_to_XYZ(randlab)
    # our = lab2xyz(randlab)
    # diff = cs - our
    # print(diff.max(),diff.mean())

