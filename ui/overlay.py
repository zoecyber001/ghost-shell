import tkinter as tk
import win32api
import win32con
import win32gui

class GhostOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ghost Shell HUD")
        
        # frameless window
        self.root.overrideredirect(True)
        
        # always on top
        self.root.wm_attributes("-topmost", True)
        
        # black = transparent
        self.root.wm_attributes("-transparentcolor", "black")
        self.root.config(bg="black")
        
        # drawing canvas
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # make clicks pass through
        self.make_click_through()

        self.board_x = 0
        self.board_y = 0

    def make_click_through(self):
        """windows api magic to let clicks pass through"""
        try:
            hwnd = win32gui.GetParent(self.root.winfo_id())
            styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, styles | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
        except Exception as e:
            print(f"Warning: click-through failed. {e}")

    def update_geometry(self, x, y, width, height):
        """snaps overlay to board position"""
        self.board_x = x
        self.board_y = y
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.update()

    def draw_move_arrow(self, start_coords, end_coords):
        """draws green arrow showing the move"""
        self.clear()
        
        # convert screen coords to overlay coords
        sx = start_coords[0] - self.board_x
        sy = start_coords[1] - self.board_y
        ex = end_coords[0] - self.board_x
        ey = end_coords[1] - self.board_y

        # start circle
        self.canvas.create_oval(sx-10, sy-10, sx+10, sy+10, outline="#00FF00", width=2)
        
        # arrow line
        self.canvas.create_line(sx, sy, ex, ey, fill="#00FF00", width=3, arrow=tk.LAST, arrowshape=(16, 20, 6))
        
        # target box
        self.canvas.create_rectangle(ex-15, ey-15, ex+15, ey+15, outline="#00FF00", width=2)
        
        self.root.update()

    def clear(self):
        self.canvas.delete("all")
        self.root.update()
    
    def destroy(self):
        try:
            self.root.destroy()
        except:
            pass
