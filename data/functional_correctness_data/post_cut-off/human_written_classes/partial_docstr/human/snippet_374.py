import cv2
from config.config import Config
from GameWindowCapturor import GameWindowCapturor
from src.utils.common import draw_rectangle, load_image, find_pattern_sqdiff, get_mask
import datetime
import time
from src.utils.logger import logger
import numpy as np

class MapScanner:
    """
    MapScanner
    """

    def __init__(self):
        self.cfg = Config
        self.kp_prev = None
        self.desc_prev = None
        self.fps = 0
        self.frame = None
        self.img_frame = None
        self.img_frame_gray = None
        self.img_debug = None
        self.img_camera = None
        self.img_camera_gray = None
        self.img_camera_gray_prev = None
        self.img_nametag = load_image('name_tag.png')
        self.img_nametag_gray = load_image('name_tag.png', cv2.IMREAD_GRAYSCALE)
        self.img_map = np.zeros((2000, 2000, 3), dtype=np.uint8)
        self.loc_nametag = (0, 0)
        self.loc_camera = (500, 500)
        self.fps_limit = 10
        self.feature_extractor = cv2.ORB_create(500)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        self.t_last_run = time.time()
        logger.info('Waiting for game window to activate, please click on game window')
        self.capture = GameWindowCapturor(self.cfg)

    def limit_fps(self):
        """
        Limit FPS
        """
        target_duration = 1.0 / self.fps_limit
        frame_duration = time.time() - self.t_last_run
        if frame_duration < target_duration:
            time.sleep(target_duration - frame_duration)
        self.fps = round(1.0 / (time.time() - self.t_last_run))
        self.t_last_run = time.time()

    def ensure_map_capacity(self, x, y, h, w):
        """
        ensure_map_capacity
        """
        map_h, map_w = self.img_map.shape[:2]
        expand_top = max(0, -y)
        expand_left = max(0, -x)
        expand_bottom = max(0, y + h - map_h)
        expand_right = max(0, x + w - map_w)
        if expand_top == 0 and expand_bottom == 0 and (expand_left == 0) and (expand_right == 0):
            return
        new_h = map_h + expand_top + expand_bottom
        new_w = map_w + expand_left + expand_right
        new_map = np.zeros((new_h, new_w, 3), dtype=np.uint8)
        new_map[expand_top:expand_top + map_h, expand_left:expand_left + map_w] = self.img_map
        self.img_map = new_map
        self.loc_camera += np.array([expand_left, expand_top])

    def update_nametag_loc(self):
        """
        get player location by detecting player's nametag
        """
        pad_y, pad_x = self.img_nametag.shape[:2]
        img_roi_padded = cv2.copyMakeBorder(self.img_camera_gray, pad_y, pad_y, pad_x, pad_x, borderType=cv2.BORDER_REPLICATE)
        last_result = (self.loc_nametag[0] + pad_x, self.loc_nametag[1] + pad_y)
        loc_nametag, score, is_cached = find_pattern_sqdiff(img_roi_padded, self.img_nametag_gray, last_result=last_result, mask=get_mask(self.img_nametag, (0, 255, 0)), global_threshold=0.3)
        loc_nametag = (loc_nametag[0] - pad_x, loc_nametag[1] - pad_y)
        if score < self.cfg.nametag_diff_thres:
            self.loc_nametag = loc_nametag
        draw_rectangle(self.img_debug, self.loc_nametag, self.img_nametag.shape, (0, 255, 0), '')
        text = f"NameTag, {round(score, 2)}, {('cached' if is_cached else 'missed')}"
        cv2.putText(self.img_debug, text, (self.loc_nametag[0], self.loc_nametag[1] + self.img_nametag.shape[0] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    def is_inside_bbox(self, pt, bbox):
        """Check if point pt = (x, y) is inside bounding box"""
        x, y = pt
        x0, y0 = bbox['position']
        h, w = bbox['size']
        return x0 <= x <= x0 + w and y0 <= y <= y0 + h

    def save_map(self):
        """
        save_map: Save the current stitched map to disk
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'maps/map_{timestamp}.png'
        cv2.imwrite(filename, self.img_map)
        print(f'[INFO] Map saved to {filename}')

    def runOnce(self):
        """
        run once
        """
        self.frame = self.capture.get_frame()
        self.img_frame = cv2.resize(self.frame, (1296, 759), interpolation=cv2.INTER_NEAREST)
        self.img_frame_gray = cv2.cvtColor(self.img_frame, cv2.COLOR_BGR2GRAY)
        if self.img_camera_gray_prev is None:
            self.img_camera_gray_prev = self.img_frame_gray
        self.img_camera = self.img_frame[self.cfg.camera_ceiling:self.cfg.camera_floor, :]
        self.img_camera_gray = cv2.cvtColor(self.img_camera, cv2.COLOR_BGR2GRAY)
        self.img_debug = self.img_camera.copy()
        self.update_nametag_loc()
        black_mask = np.all(self.img_camera == [0, 0, 0], axis=2).astype(np.uint8) * 255
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (50, 50))
        closed_mask = cv2.morphologyEx(black_mask, cv2.MORPH_CLOSE, kernel)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(closed_mask, connectivity=8)
        dynamic_objs = [{'position': self.loc_nametag, 'size': self.img_nametag.shape[:2], 'score': 1.0}]
        min_area = 1000
        for i in range(1, num_labels):
            x, y, w, h, area = stats[i]
            if area > min_area:
                dynamic_objs.append({'position': (x, y), 'size': (h, w), 'score': 1.0})
        dynamic_obj_margin = 10
        img_h, img_w = self.img_camera_gray.shape
        for obj in dynamic_objs:
            x, y = obj['position']
            h, w = obj['size']
            x_new = max(0, x - dynamic_obj_margin)
            y_new = max(0, y - dynamic_obj_margin)
            x_end = min(img_w, x + w + dynamic_obj_margin)
            y_end = min(img_h, y + h + dynamic_obj_margin)
            obj['position'] = (x_new, y_new)
            obj['size'] = (y_end - y_new, x_end - x_new)
        mask = np.ones_like(self.img_camera_gray, dtype=np.uint8) * 255
        for obj in dynamic_objs:
            draw_rectangle(self.img_debug, obj['position'], obj['size'], (0, 255, 0), str(round(obj['score'], 2)))
            x, y = obj['position']
            h, w = obj['size']
            mask[y:y + h, x:x + w] = 0
        kp_cur, desc_cur = self.feature_extractor.detectAndCompute(self.img_camera_gray, mask)
        if self.kp_prev is None:
            dx, dy = (0, 0)
        else:
            matches = self.bf.match(self.desc_prev, desc_cur)
            matches = sorted(matches, key=lambda x: x.distance)
            if len(matches) < 4:
                return
            pts1 = np.float32([self.kp_prev[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
            pts2 = np.float32([kp_cur[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
            M, inliers = cv2.estimateAffinePartial2D(pts2, pts1, method=cv2.RANSAC)
            dx, dy = (M[0, 2], M[1, 2])
            for i, m in enumerate(matches):
                if inliers[i]:
                    pt = tuple(np.round(kp_cur[m.trainIdx].pt).astype(int))
                    cv2.circle(self.img_debug, pt, 4, (0, 0, 255), thickness=-1)
            h, w = self.img_debug.shape[:2]
            center = (w // 2, h // 2)
            motion_endpoint = (int(center[0] + dx), int(center[1] + dy))
            cv2.arrowedLine(self.img_debug, center, motion_endpoint, color=(0, 0, 255), thickness=2, tipLength=0.3)
        cv2.putText(self.img_debug, f'dx: {dx:.2f}, dy: {dy:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.imshow('Map Scanner Debug', self.img_debug)
        self.loc_camera = (round(self.loc_camera[0] + dx), round(self.loc_camera[1] + dy))
        h, w = self.img_camera.shape[:2]
        x, y = self.loc_camera
        self.ensure_map_capacity(x, y, h, w)
        x, y = self.loc_camera
        mask_rgb = mask == 255
        self.img_map[y:y + h, x:x + w][mask_rgb] = self.img_camera[mask_rgb]
        map_vis = cv2.resize(self.img_map, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
        cv2.imshow('Map', map_vis)
        self.kp_prev = kp_cur
        self.desc_prev = desc_cur
        self.img_camera_gray_prev = self.img_camera_gray