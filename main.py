import time
import random
import cv2
import chess
import keyboard
import numpy as np
from core.vision import GhostVision
from core.engine import GhostEngine
from core.humanizer import Humanizer
from ui.overlay import GhostOverlay
from utils.logger import Logger
from utils.config import PLAYER_SIDE, THINK_TIME_MIN, THINK_TIME_MAX

class GhostShell:
    def __init__(self):
        self.logger = Logger("MAIN")
        self.vision = GhostVision()
        self.engine = GhostEngine()
        self.humanizer = Humanizer()
        self.overlay = GhostOverlay()
        self.board = chess.Board()
        self.user_side = chess.WHITE 

    def get_square_center(self, square_name):
        """converts 'e4' to screen coords"""
        file_idx = chess.FILE_NAMES.index(square_name[0])
        rank_idx = int(square_name[1]) - 1

        bx, by, bw, bh = self.vision.board_location
        sq_size = self.vision.square_size

        if self.user_side == chess.WHITE:
            x = bx + (file_idx * sq_size) + (sq_size / 2)
            y = by + ((7 - rank_idx) * sq_size) + (sq_size / 2)
        else:
            # board is flipped for black
            x = bx + ((7 - file_idx) * sq_size) + (sq_size / 2)
            y = by + (rank_idx * sq_size) + (sq_size / 2)
            
        return int(x), int(y)

    def wait_for_opponent_move(self):
        """watches screen for pixel changes - waits for stable state"""
        self.logger.log("Waiting for opponent...")
        
        # wait a bit for our own animation to finish
        time.sleep(1.0)
        previous_state_img = self.vision.capture_screen()
        
        while True:
            if keyboard.is_pressed('q'):
                self.logger.warning("Quit detected.")
                return None

            time.sleep(0.8)
            current_state_img = self.vision.capture_screen()
            
            diff = cv2.absdiff(previous_state_img, current_state_img)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
            non_zero = cv2.countNonZero(thresh)
            
            if non_zero > 1000:  # higher threshold
                self.logger.success("Movement detected!")
                time.sleep(1.0)  # wait for animation to fully finish
                return True
            
            # update baseline
            previous_state_img = current_state_img
                
    def run(self):
        self.logger.log("Initializing Ghost-Shell...")
        
        # ask user which side they're playing
        print("\n" + "="*50)
        print("Which side are you playing?")
        print("  [W] White (you move first)")
        print("  [B] Black (opponent moves first)")
        print("  [A] Auto-detect (may not be accurate)")
        print("="*50)
        
        side_input = input("Enter W/B/A: ").strip().upper()
        
        if side_input == "W":
            self.user_side = chess.WHITE
        elif side_input == "B":
            self.user_side = chess.BLACK
        else:
            # will try auto-detect after board found
            pass
        
        self.logger.warning("Make sure the board is visible.")
        self.logger.warning("Press 'S' to start.")
        keyboard.wait('s')
        
        location = self.vision.find_board()
        if not location:
            self.logger.error("Couldnt find board. Exiting.")
            return
        
        # snap overlay to board
        self.overlay.update_geometry(*location)

        # auto-detect if user chose A
        if side_input == "A" or PLAYER_SIDE == "AUTO":
            detected_side = self.vision.detect_player_side()
            if detected_side is not None:
                self.user_side = detected_side

        self.logger.success(f"Board locked. Playing as {'White' if self.user_side == chess.WHITE else 'Black'}.")
        
        # if playing black, wait for opponent's first move
        if self.user_side == chess.BLACK:
            self.logger.log("Playing as Black - waiting for White's first move...")
            print("\nEnter opponent's first move when ready.")
            while True:
                move = input("Opponent's move (e.g. e2e4): ").strip().lower()
                if move:
                    try:
                        self.board.push_uci(move)
                        break
                    except ValueError:
                        self.logger.error(f"Invalid move: {move}")
                        print(f"Legal moves: {', '.join([m.uci() for m in list(self.board.legal_moves)[:10]])}...")
        
        while not self.board.is_game_over():
            
            if self.board.turn == self.user_side:
                think_time = random.uniform(THINK_TIME_MIN, THINK_TIME_MAX)
                self.logger.log(f"My turn. Thinking for {think_time:.1f}s...")
                time.sleep(think_time)
                
                fen = self.board.fen()
                best_move_uci = self.engine.get_human_move(fen)
                
                if best_move_uci:
                    start_sq = best_move_uci[:2]
                    end_sq = best_move_uci[2:4]
                    
                    start_coords = self.get_square_center(start_sq)
                    end_coords = self.get_square_center(end_sq)
                    
                    promotion_piece = None
                    if len(best_move_uci) > 4:
                        promotion_piece = best_move_uci[4]
                    
                    sq_size = int(self.vision.square_size)
                    is_white = self.user_side == chess.WHITE
                    
                    # show the move on HUD
                    self.overlay.draw_move_arrow(start_coords, end_coords)
                    time.sleep(0.3)
                    
                    self.humanizer.make_move(start_coords, end_coords, promotion_piece, sq_size, is_white)
                    self.overlay.clear()
                    self.board.push_uci(best_move_uci)
                    
                    # log the move made
                    self.logger.success(f"Played: {best_move_uci}")
                
            else:
                self.logger.warning("Opponent's turn.")
                print(f"\n{self.board}")
                print(f"\nLegal moves: {', '.join([m.uci() for m in list(self.board.legal_moves)[:10]])}...")
                
                detected = self.wait_for_opponent_move()
                
                if detected is None:
                    break
                elif detected:
                    self.logger.log("Movement detected! Enter the move.")
                    
                    while True:
                        move = input("Opponent's move (e.g. e7e5): ").strip().lower()
                        try:
                            self.board.push_uci(move)
                            break
                        except ValueError:
                            self.logger.error(f"Invalid move: {move}")
                            print(f"Legal moves: {', '.join([m.uci() for m in list(self.board.legal_moves)[:10]])}...")

        self.logger.success("Game Over.")

if __name__ == "__main__":
    bot = GhostShell()
    bot.run()