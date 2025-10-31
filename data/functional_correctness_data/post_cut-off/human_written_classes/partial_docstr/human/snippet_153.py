from typing import Optional, Dict, List, Any, Union

class Clip_settings:
    """素材片段的图像调节设置"""
    alpha: float
    '图像不透明度, 0-1'
    flip_horizontal: bool
    '是否水平翻转'
    flip_vertical: bool
    '是否垂直翻转'
    rotation: float
    '顺时针旋转的**角度**, 可正可负'
    scale_x: float
    '水平缩放比例'
    scale_y: float
    '垂直缩放比例'
    transform_x: float
    '水平位移, 单位为半个画布宽'
    transform_y: float
    '垂直位移, 单位为半个画布高'

    def __init__(self, *, alpha: float=1.0, flip_horizontal: bool=False, flip_vertical: bool=False, rotation: float=0.0, scale_x: float=1.0, scale_y: float=1.0, transform_x: float=0.0, transform_y: float=0.0):
        """初始化图像调节设置, 默认不作任何图像变换

        Args:
            alpha (float, optional): 图像不透明度, 0-1. 默认为1.0.
            flip_horizontal (bool, optional): 是否水平翻转. 默认为False.
            flip_vertical (bool, optional): 是否垂直翻转. 默认为False.
            rotation (float, optional): 顺时针旋转的**角度**, 可正可负. 默认为0.0.
            scale_x (float, optional): 水平缩放比例. 默认为1.0.
            scale_y (float, optional): 垂直缩放比例. 默认为1.0.
            transform_x (float, optional): 水平位移, 单位为半个画布宽. 默认为0.0.
            transform_y (float, optional): 垂直位移, 单位为半个画布高. 默认为0.0.
                参考: 剪映导入的字幕似乎取此值为-0.8
        """
        self.alpha = alpha
        self.flip_horizontal, self.flip_vertical = (flip_horizontal, flip_vertical)
        self.rotation = rotation
        self.scale_x, self.scale_y = (scale_x, scale_y)
        self.transform_x, self.transform_y = (transform_x, transform_y)

    def export_json(self) -> Dict[str, Any]:
        clip_settings_json = {'alpha': self.alpha, 'flip': {'horizontal': self.flip_horizontal, 'vertical': self.flip_vertical}, 'rotation': self.rotation, 'scale': {'x': self.scale_x, 'y': self.scale_y}, 'transform': {'x': self.transform_x, 'y': self.transform_y}}
        return clip_settings_json