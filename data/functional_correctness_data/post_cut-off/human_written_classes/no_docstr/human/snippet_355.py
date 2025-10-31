from PIL import Image

class BaseFeatureDict:
    action_key: str
    room_image_key: str
    wrist_image_key: str
    state_key: str
    seg_room_key: str
    seg_wrist_key: str
    depth_room_key: str
    depth_wrist_key: str

    def __init__(self, image_shape: tuple[int, int, int]=(224, 224, 3), state_shape: tuple[int, ...]=(7,), actions_shape: tuple[int, ...]=(6,), include_depth: bool=False, include_seg: bool=False, include_video: bool=False):
        self.image_shape = image_shape
        self.state_shape = state_shape
        self.actions_shape = actions_shape
        self.include_depth = include_depth
        self.include_seg = include_seg
        self.include_video = include_video

    @property
    def features(self):
        features_dict = {self.room_image_key: {'dtype': 'image', 'shape': self.image_shape, 'names': ['height', 'width', 'channels']}, self.wrist_image_key: {'dtype': 'image', 'shape': self.image_shape, 'names': ['height', 'width', 'channels']}, self.state_key: {'dtype': 'float32', 'shape': self.state_shape, 'names': ['state']}, self.action_key: {'dtype': 'float32', 'shape': self.actions_shape, 'names': ['action']}}
        if self.include_depth:
            depth_data_img = {self.depth_room_key: {'dtype': 'image', 'shape': self.image_shape, 'names': ['height', 'width', 'channels']}, self.depth_wrist_key: {'dtype': 'image', 'shape': self.image_shape, 'names': ['height', 'width', 'channels']}}
            features_dict.update(depth_data_img)
            if self.include_video:
                depth_data_vid = {self.depth_room_key: {'dtype': 'video', 'shape': self.image_shape, 'names': ['height', 'width', 'channels']}, self.depth_wrist_key: {'dtype': 'video', 'shape': self.image_shape, 'names': ['height', 'width', 'channels']}}
                features_dict.update(depth_data_vid)
        if self.include_seg:
            seg_data_img = {self.seg_room_key: {'dtype': 'image', 'shape': self.image_shape, 'names': ['height', 'width', 'channels']}, self.seg_wrist_key: {'dtype': 'image', 'shape': self.image_shape, 'names': ['height', 'width', 'channels']}}
            features_dict.update(seg_data_img)
            if self.include_video:
                seg_data_vid = {self.seg_room_key: {'dtype': 'video', 'shape': self.image_shape, 'names': ['height', 'width', 'channels']}, self.seg_wrist_key: {'dtype': 'video', 'shape': self.image_shape, 'names': ['height', 'width', 'channels']}}
                features_dict.update(seg_data_vid)
        if self.include_video:
            main_img_vid = {self.room_image_key: {'dtype': 'video', 'shape': self.image_shape, 'names': ['height', 'width', 'channels']}, self.wrist_image_key: {'dtype': 'video', 'shape': self.image_shape, 'names': ['height', 'width', 'channels']}}
            features_dict.update(main_img_vid)
        return features_dict

    def __call__(self, rgb, state, action, seg=None, depth_room=None, depth_wrist=None) -> dict:
        frame_data = {}
        img_h, img_w, _ = self.image_shape
        current_features = self.features
        frame_data[self.room_image_key] = resize_with_pad(rgb[0], img_h, img_w)
        frame_data[self.wrist_image_key] = resize_with_pad(rgb[1], img_h, img_w)
        frame_data[self.state_key] = state
        frame_data[self.action_key] = action
        if seg is not None and self.seg_room_key in current_features:
            frame_data[self.seg_room_key] = resize_with_pad(seg[0], img_h, img_w, method=Image.NEAREST)
        if seg is not None and self.seg_wrist_key in current_features:
            frame_data[self.seg_wrist_key] = resize_with_pad(seg[1], img_h, img_w, method=Image.NEAREST)
        if depth_room is not None and self.depth_room_key in current_features:
            frame_data[self.depth_room_key] = resize_with_pad(depth_room, img_h, img_w).squeeze(2)
        if depth_wrist is not None and self.depth_wrist_key in current_features:
            frame_data[self.depth_wrist_key] = resize_with_pad(depth_wrist, img_h, img_w).squeeze(2)
        return frame_data