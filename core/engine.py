import os
import sys
import random
from stockfish import Stockfish
from utils.logger import Logger
from utils.config import ENGINE_DEPTH, ENGINE_CONTEMPT

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class GhostEngine:
    def __init__(self):
        self.logger = Logger("ENGINE")
        
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        engine_path = os.path.join(base_path, "assets", "stockfish.exe")
        
        if not os.path.exists(engine_path):
            self.logger.error(f"Stockfish not found at: {engine_path}")
            sys.exit(1)

        self.stockfish = Stockfish(path=engine_path)
        self.stockfish.set_depth(ENGINE_DEPTH) 
        self.stockfish.update_engine_parameters({"Contempt": ENGINE_CONTEMPT}) 

        self.logger.success(f"Brain loaded. Depth: {ENGINE_DEPTH}, Contempt: {ENGINE_CONTEMPT}")

    def get_human_move(self, fen):
        """returns best move, but sometimes picks 2nd best to look human"""
        try:
            self.stockfish.set_fen_position(fen)
            top_moves = self.stockfish.get_top_moves(3)
        except Exception as e:
            self.logger.error(f"Stockfish error: {e}")
            return None
        
        if not top_moves:
            return None

        best_move = top_moves[0]
        
        # the turing filter - if moves are close, sometimes pick #2
        if len(top_moves) > 1:
            # handle mate scores (Centipawn can be None for mate positions)
            try:
                move1_score = int(best_move.get('Centipawn') or 0)
                move2_score = int(top_moves[1].get('Centipawn') or 0)
                score_diff = abs(move1_score - move2_score)
                
                # 30% chance to be "different" if scores are close
                if score_diff < 30 and random.random() < 0.3:
                    self.logger.log(f"Style move: {top_moves[1]['Move']} (diff: {score_diff})")
                    return top_moves[1]['Move']
            except (TypeError, ValueError):
                pass  # just use best move if score parsing fails

        self.logger.log(f"Best move: {best_move['Move']}")
        return best_move['Move']

if __name__ == "__main__":
    brain = GhostEngine()
    start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    print("Thinking...")
    move = brain.get_human_move(start_fen)
    print(f"Move: {move}")