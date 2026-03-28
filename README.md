# east-parmon

## Courtside Dynasty (Basketball GM Simulation)

This repository now includes an interactive basketball simulation game inspired by **2K MyNBA/MyGM style loops**:

- Real NBA teams, star players, and coaches (sample set).
- **GM Mode** (roster management, free-agent signing, player training, season simulation).
- **Player Career Mode** (create your player and build a career over multiple seasons).
- **Coach Mode** (choose tactical gameplans that affect outcomes).
- Dynamic multi-season progression with aging/regression/progression.
- New rookie classes generated every offseason.
- Encrypted face/avatar tokens for players and coaches for style/flavor.

## Run

```bash
python game.py
```

## Notes

- This is a terminal-based interactive prototype.
- Player/coach "face" and "avatar" are encrypted token strings generated via hashing + base64 encoding.
- You can expand the team/player database, add salary cap rules, trades, injuries, and deeper playoff logic.
