# Ghost-Shell Roadmap

Future features and improvements. PRs welcome.

---

## High Priority

### Auto-Detect Opponent Moves
Currently you have to type opponent moves manually. The goal is to automatically detect what move was played by:
- Detecting highlighted squares (most sites highlight last move)
- Comparing board states before/after
- Template matching for piece recognition

### Multi-Monitor Support
Right now it only scans the primary monitor. Should detect which monitor has the chess board.

---

## Medium Priority

### Opening Book Integration
Instead of calculating from move 1, use known opening theory for the first 10-15 moves. Makes play look more human.

### Time Control Awareness
Adjust think time based on clock. Blitz = faster moves, classical = longer thinks.

### Pre-Move Detection
Detect opponent premoves and react accordingly.

---

## Low Priority / Nice to Have

### Profile System
Save different play styles:
- Aggressive (high contempt)
- Solid (lower depth, more draw-ish)
- Blunder Mode (intentionally make occasional mistakes)

### Move History Export
Log all games played for review.

### Cross-Platform Support
Currently Windows-only (uses pywin32). Add macOS/Linux support for the overlay.

### Lichess API Integration
Instead of screen reading, connect directly to Lichess API for cleaner detection.

---

## Known Issues

- Side auto-detection isn't always accurate (use W/B manual selection)
- Very fast opponents might trigger movement detection prematurely
- Promotion popup click position may vary by site/board theme

---

## Contributing

1. Fork the repo
2. Create feature branch
3. Make changes
4. Open PR

No formal process, just dont break stuff.
