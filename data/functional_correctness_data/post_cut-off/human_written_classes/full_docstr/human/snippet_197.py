from src.utils.global_var import WINDOW_WORKING_SIZE
import numpy as np
from src.utils.common import find_pattern_sqdiff, screenshot, load_image, is_mac, override_cfg, load_yaml, click_in_game_window
from src.input.KeyBoardListener import KeyBoardListener
import cv2
import time
from src.utils.logger import logger

class AutoDiceRoller:
    """
    AutoDiceRoller
    """

    def __init__(self, args):
        """
        Init AutoDiceRoller
        """
        self.args = args
        self.fps = 0
        self.is_first_frame = True
        self.is_enable = True
        self.frame = None
        self.img_frame = None
        self.img_frame_gray = None
        self.img_frame_debug = None
        self.img_route = None
        self.img_route_debug = None
        self.img_minimap = np.zeros((10, 10, 3), dtype=np.uint8)
        self.t_last_frame = time.time()
        cfg = load_yaml('config/config_default.yaml')
        if is_mac():
            cfg = override_cfg(cfg, load_yaml('config/config_macOS.yaml'))
        self.cfg = override_cfg(cfg, load_yaml(f'config/config_{args.cfg}.yaml'))
        self.fps_limit = self.cfg['system']['fps_limit_auto_dice_roller']
        self.img_numbers = [load_image(f'numbers/{i}.png', cv2.IMREAD_GRAYSCALE) for i in range(4, 14)]
        self.kb = KeyBoardListener(self.cfg, is_autobot=False)
        logger.info('Waiting for game window to activate, please click on game window')
        self.capture = GameWindowCapturor(self.cfg)

    def update_img_frame_debug(self):
        """
        update_img_frame_debug
        """
        cv2.imshow('Game Window Debug', self.img_frame_debug[:self.cfg['ui_coords']['ui_y_start'], :])
        self.t_last_frame = time.time()

    def run_once(self):
        """
        Process one game window frame
        """
        self.frame = self.capture.get_frame()
        if self.frame is None:
            logger.warning('Failed to capture game frame.')
            return
        if self.cfg['game_window']['size'] != self.frame.shape[:2]:
            text = f"Unexpeted window size: {self.frame.shape[:2]} (expect {self.cfg['game_window']['size']})"
            logger.error(text)
            return
        self.img_frame = cv2.resize(self.frame, WINDOW_WORKING_SIZE, interpolation=cv2.INTER_NEAREST)
        self.img_frame_gray = cv2.cvtColor(self.img_frame, cv2.COLOR_BGR2GRAY)
        self.img_frame_debug = self.img_frame.copy()
        self.is_first_frame = False
        if self.kb.is_pressed_func_key[0]:
            self.is_enable = not self.is_enable
            logger.info(f'User press F1, is_enable = {self.is_enable}')
            self.kb.is_pressed_func_key[0] = False
        if self.kb.is_pressed_func_key[1]:
            screenshot(self.img_frame)
            self.kb.is_pressed_func_key[1] = False
        if self.is_enable and self.kb.is_game_window_active():
            loc_dice = (981, 445)
            loc_first_box = (890, 371)
            box_size = (22, 37)
            box_y_interval = 25
            window_title = self.cfg['game_window']['title']
            attibutes_info = []
            for i, attibute in enumerate(['STR', 'DEX', 'INT', 'LUK']):
                p0 = (loc_first_box[0], loc_first_box[1] + i * box_y_interval)
                p1 = (p0[0] + box_size[1], p0[1] + box_size[0])
                img_roi = self.img_frame_gray[p0[1]:p1[1], p0[0]:p1[0]]
                best_score = float('inf')
                best_digit = None
                for idx, img_number in enumerate(self.img_numbers, start=4):
                    _, score, _ = find_pattern_sqdiff(img_roi, img_number)
                    if score < best_score:
                        best_score = score
                        best_digit = idx
                logger.info(f'[{attibute}]: {best_digit} (score: {round(best_score, 2)})')
                attibutes_info.append((best_digit, best_score))
                cv2.rectangle(self.img_frame_debug, p0, p1, (0, 0, 255), 1)
                cv2.putText(self.img_frame_debug, f'{best_digit}', (p0[0], p0[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
            is_jackpot = True
            for i, (val, score) in enumerate(attibutes_info):
                target = self.args.attribute[i]
                if target is not None and target != val:
                    is_jackpot = False
            if is_jackpot:
                self.is_enable = False
                logger.info('Hit Jackpot! Stop!')
            if self.is_enable:
                click_in_game_window(window_title, loc_dice)
                logger.info('Roll the dice')
        self.update_img_frame_debug()