import numpy as np

from .utils.func import *
from .utils.constants import const


class RGBXYZTransfer:
    def __init__(self, color_space) -> None:
        """[This RGB<->XYZ tranform is performed without chromatic_adaptation_transform.
           Suppose that RGB-colour-space and XYZ-colour-space have the same reference white.]

        Args:
            color_space ([str]): ['bt709' / 'bt2020']
        """
        assert color_space.lower() in ['bt709', 'bt2020'] #'bt601'
        if color_space == 'bt709':
            self.RGB_to_XYZ_matrix = np.array([[0.412391, 0.357584, 0.180481],
                                                  [0.212639, 0.715169, 0.072192],
                                                  [0.019331, 0.119195, 0.950532]], dtype=np.float32)

            self.XYZ_to_RGB_matrix = np.array([[3.2409663, -1.5373788, -0.49861172],
                                                  [-0.96924204, 1.8759652, 0.04155577],
                                                  [0.05562956, -0.20397693, 1.0569717]], dtype=np.float32)
        if color_space == 'bt2020':
            self.RGB_to_XYZ_matrix = np.array([[0.636958, 0.144617, 0.168881],
                                                    [0.262700, 0.677998, 0.059302],
                                                    [0.000000, 0.028073, 1.060985]], dtype=np.float32)

            self.XYZ_to_RGB_matrix = np.array([[1.716651, -0.355671, -0.253366],
                                                    [-0.666684, 1.616481, 0.015769],
                                                    [0.017640, -0.042771, 0.942103]], dtype=np.float32)
        
    def rgb2xyz(self, img_rgb):
        return dot_vector(self.RGB_to_XYZ_matrix, img_rgb)
    
    def xyz2rgb(self, img_xyz):
        return dot_vector(self.XYZ_to_RGB_matrix, img_xyz)

if __name__ == '__main__':

    rgb_xyz = RGBXYZTransfer(color_space='bt2020')

    # # verify rgb2xyz
    # randrgb = np.rand((1080,1920,3), dtype=np.float32)
    # our = rgb_xyz.rgb2xyz(randrgb)
    # cs = colour.RGB_to_XYZ(randrgb, const.ILLUMINANTS['D65'], const.ILLUMINANTS['D65'], rgbxyz.RGB_to_XYZ_matrix)
    # cs = np.from_numpy(cs)
    # diff = abs(cs - our)
    # print(diff.max(), diff.mean())

    # # verify xyz2rgb
    # randxyz = np.rand((1080,1920,3), dtype=np.float32)
    # our = rgb_xyz.xyz2rgb(randxyz)
    # cs = colour.XYZ_to_RGB(randxyz, const.ILLUMINANTS['D65'], const.ILLUMINANTS['D65'], rgb_xyz.XYZ_to_RGB_matrix)
    # cs = np.from_numpy(cs)
    # diff = abs(cs - our)
    # print(diff.max(), diff.mean())
