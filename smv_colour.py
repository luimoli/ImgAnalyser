from ColorSpaceTrans import RGB_XYZ, XYZ_Lab

def RGB2XYZ(img_rgb, color_space):
    """
        color_space ([str]): ['bt709', 'bt2020']
    """
    trans = RGB_XYZ.RGBXYZTransfer(color_space)
    return trans.rgb2xyz(img_rgb)
def XYZ2RGB(img_xyz, color_space):
    """
        color_space ([str]): ['bt709', 'bt2020']
    """
    trans = RGB_XYZ.RGBXYZTransfer(color_space)
    return trans.xyz2rgb(img_xyz)


def XYZ2Lab(img_xyz, illuminant_mode='d65'):
    """
    Args:
        img_xyz (arr): CIE XYZ colorspace array.
        illuminant_mode (str, optional): ['d65', 'd50']. Defaults to 'd65'.
    """
    return XYZ_Lab.xyz2lab(img_xyz, illuminant_mode)
def Lab2XYZ(img_lab, illuminant_mode='d65'):
    """
    Args:
        img_lab (arr): CIE LAB colorspace array.
        illuminant_mode (str, optional): ['d65', 'd50']. Defaults to 'd65'.
    """
    return XYZ_Lab.lab2xyz(img_lab, illuminant_mode)


def RGB2Lab(img_rgb, color_space, illuminant_mode='d65'):
    """_summary_
    Args:
        img_rgb (arr): R-G-B
        color_space ([str]): ['bt709', 'bt2020']
        illuminant_mode (str, optional): ['d65', 'd50']. Defaults to 'd65'.
    """
    trans1 = RGB_XYZ.RGBXYZTransfer(color_space)
    img_xyz = trans1.rgb2xyz(img_rgb)
    img_lab = XYZ_Lab.xyz2lab(img_xyz, illuminant_mode)
    return img_lab
