import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Engine Settings
ENGINE_DEPTH = int(os.getenv("ENGINE_DEPTH", 15))
ENGINE_CONTEMPT = int(os.getenv("ENGINE_CONTEMPT", 20))

# Humanization  
MOUSE_SPEED = float(os.getenv("MOUSE_SPEED", 0.4))
TARGET_JITTER = int(os.getenv("TARGET_JITTER", 6))

# Thinking Time (simulates human deliberation)
THINK_TIME_MIN = float(os.getenv("THINK_TIME_MIN", 1.5))
THINK_TIME_MAX = float(os.getenv("THINK_TIME_MAX", 6.0))

# Player Side: "AUTO", "WHITE", or "BLACK"
PLAYER_SIDE = os.getenv("PLAYER_SIDE", "AUTO").upper()

# Legacy config (for backwards compatibility)
BOT_PERSONA = "AGGRESSIVE"
JITTER_AMOUNT = TARGET_JITTER