import pyautogui
import time
import random
import numpy as np
from utils.logger import Logger
from utils.config import TARGET_JITTER, MOUSE_SPEED

pyautogui.FAILSAFE = True

class Humanizer:
    def __init__(self):
        self.logger = Logger("HUMANIZER")
        self.base_speed = MOUSE_SPEED
        self.jitter = TARGET_JITTER 

    def _get_bezier_points(self, start, end, control_points=1):
        """generates curved path - subtle arc, not crazy loops"""
        start = np.array(start)
        end = np.array(end)
        
        diff = end - start
        distance = np.linalg.norm(diff)
        
        # subtle curve, proportional to distance
        control = start + diff/2
        arc_amount = min(30, distance * 0.1)  # max 30px arc
        control[0] += random.randint(int(-arc_amount), int(arc_amount))
        control[1] += random.randint(int(-arc_amount), int(arc_amount))

        # fewer steps = faster movement
        steps = random.randint(12, 20)
        
        points = []
        for t in np.linspace(0, 1, steps):
            pt = (1-t)**2 * start + 2*(1-t)*t * control + t**2 * end
            points.append(pt)
            
        return points

    def move_mouse(self, x, y):
        """moves mouse fast but with slight curve"""
        start_x, start_y = pyautogui.position()
        
        target_x = x + random.randint(-self.jitter, self.jitter)
        target_y = y + random.randint(-self.jitter, self.jitter)
        
        path = self._get_bezier_points((start_x, start_y), (target_x, target_y))
        
        for i, point in enumerate(path):
            pyautogui.moveTo(point[0], point[1])
            # very short delays - total move should be ~0.1-0.2s
            time.sleep(random.uniform(0.005, 0.015))

    def click(self):
        """click with realistic hold duration"""
        pyautogui.mouseDown()
        time.sleep(random.uniform(0.05, 0.12))
        pyautogui.mouseUp()

    def make_move(self, start_coords, end_coords, promotion_piece=None, square_size=None, player_is_white=True):
        """click piece, drag to square, handle promotion if needed"""
        self.logger.log("Making move...")
        
        self.move_mouse(*start_coords)
        self.click()
        
        time.sleep(random.uniform(0.1, 0.3))
        
        self.move_mouse(*end_coords)
        self.click()
        
        if promotion_piece:
            time.sleep(random.uniform(0.2, 0.4))
            self._click_promotion_piece(end_coords, promotion_piece, square_size, player_is_white)
        
        self.logger.success("Done.")
    
    def _click_promotion_piece(self, square_coords, piece, square_size=None, player_is_white=True):
        """clicks on the promotion popup. order is queen, rook, bishop, knight"""
        piece_order = {'q': 0, 'r': 1, 'b': 2, 'n': 3}
        
        if piece.lower() not in piece_order:
            self.logger.error(f"Invalid piece: {piece}")
            return
        
        offset_index = piece_order[piece.lower()]
        sq_size = square_size or 80
        
        x, y = square_coords
        
        # white promotes on rank 8 (popup goes DOWN), black on rank 1 (popup goes UP)
        if player_is_white:
            promotion_y = y + (offset_index * sq_size)
        else:
            promotion_y = y - (offset_index * sq_size)
        
        self.logger.log(f"Clicking {piece.upper()}")
        
        time.sleep(random.uniform(0.1, 0.2))
        self.move_mouse(x, int(promotion_y))
        self.click()

if __name__ == "__main__":
    h = Humanizer()
    print("Testing in 3 seconds... move mouse to corner to abort")
    time.sleep(3)
    h.make_move((500, 500), (600, 600))