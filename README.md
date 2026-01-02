# GHOST-SHELL

```
   ▄████  ██░ ██  ▒█████    ██████ ▄▄▄█████▓
  ██▒ ▀█▒▓██░ ██▒▒██▒  ██▒▒██    ▒ ▓  ██▒ ▓▒
 ▒██░▄▄▄░▒██▀▀██░▒██░  ██▒░ ▓██▄   ▒ ▓██░ ▒░
 ░▓█  ██▓░▓█ ░██ ▒██   ██░  ▒   ██▒░ ▓██▓ ░ 
 ░▒▓███▀▒░▓█▒░██▓░ ████▓▒░▒██████▒▒  ▒██▒ ░ 
  ░▒   ▒  ▒ ░░▒░▒░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░  ▒ ░░   
        S H E L L   -   C H E S S
```

---

## Why does this exist?

My friend kept beating me at chess. So i challenged him again and told him if he was able to beat me, i would build this. Bruhhh, He beat me again in 4 moves. 4. No Way i was letting that slide. So Yeah, here we are"

---

## What is it?

Ghost-Shell watches your screen, finds the chessboard, thinks with Stockfish, then moves the mouse like a human would. Bezier curves, random delays, the whole thing.

---

## Features

- **Vision** - finds any chessboard on screen via opencv
- **Turing Filter** - sometimes picks the 2nd best move so it doesnt look like an engine  
- **Human mouse movement** - curves, jitter, variable click timing
- **Auto side detection** - figures out if youre white or black
- **Think time** - waits 1.5-6 seconds before moving like a real person would
- **Promotion clicks** - clicks the popup menu, not keyboard shortcuts
- **HUD Overlay** - transparent green arrow shows the move before it happens

---

## Install

```bash
git clone https://github.com/yourusername/ghost-shell.git
cd ghost-shell
pip install -r requirements.txt
```

Download stockfish from https://stockfishchess.org/download/ and put `stockfish.exe` in the `assets` folder.

---

## Usage

```bash
python main.py
```

1. Open chess.com or lichess or whatever
2. Make sure the board is visible
3. Choose W/B/A when prompted (White/Black/Auto)
4. Press `S` to start
5. Let it do its thing

Press `Q` to quit. Or slam mouse to corner - theres a failsafe.

---

## Entering Opponent Moves

When its your opponent's turn, you need to type their move. Format:

```
[from square][to square]
```

Examples:
- `e2e4` - pawn moves from e2 to e4
- `g1f3` - knight from g1 to f3  
- `e1g1` - castles kingside

Files are a-h (left to right), ranks are 1-8 (bottom to top for white). If you cant figure out `e2e4`, maybe stick to tic-tac-toe.

The bot shows legal moves to help. Uppercase works too.

**Coming soon:** Auto-detect opponent moves. For now, you gotta type em.

---

## Config

Edit `.env`:

```env
ENGINE_DEPTH=15          # higher = stronger
ENGINE_CONTEMPT=20       # higher = more aggressive

MOUSE_SPEED=0.4
TARGET_JITTER=6          # pixels
THINK_TIME_MIN=1.5       # seconds  
THINK_TIME_MAX=6.0

PLAYER_SIDE=AUTO         # AUTO / WHITE / BLACK
```

---

## Project Structure

```
ghost-shell/
├── main.py              # orchestrator
├── core/
│   ├── vision.py        # screen capture, board detection
│   ├── engine.py        # stockfish wrapper
│   └── humanizer.py     # mouse movement
├── ui/
│   └── overlay.py       # transparent HUD with move arrows
├── utils/
│   ├── config.py        # loads .env
│   └── logger.py        # colored output
├── assets/
│   └── stockfish.exe
└── .env
```

---

## Debug

Check if vision is working:

```bash
python -c "from core.vision import GhostVision; v = GhostVision(); v.find_board(); v.debug_draw_board()"
```

Saves `debug_vision.jpg` with the detected grid.

---

## Disclaimer

This is for educational purposes. Using this on chess sites is against their TOS and is cheating. Dont be that guy. Or do, I'm not your mom.

---

MIT License - do whatever
