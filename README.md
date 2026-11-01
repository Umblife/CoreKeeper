# Core Keeper Auto Fishing Macro

A Python script that automates fishing in **Core Keeper**. It detects a bite by comparing consecutive screenshots of a small area near the character's bobber, then right-clicks to reel in the fish.

## Requirements

- Python 3.10 or later

## 1. Set up Python

### Install Python

1. Install Python 3.10 or later from [python.org](https://www.python.org/downloads/).
2. On Windows, enable **Add Python to PATH** during installation.
3. Open Command Prompt or PowerShell and check the installed version:

   ```bash
   python --version
   ```

   Make sure the version is `3.10` or higher.

### Install the required packages

```bash
python -m pip install --upgrade pip
python -m pip install opencv-python mss numpy pyautogui pygetwindow
```

## 2. Get into position and run the script

### Recommended fishing position

Before starting the script, position your character as follows:

- Stand on a block directly adjacent to the water, with your character facing the water.
- Standing to the **left or right of the water** is recommended. The script detects bites by monitoring visual changes in a small area near the character's head. Standing below the water may make the monitored area less suitable for detecting those changes.

### Run the script

1. Start **Core Keeper** and disable the fishing minigame in the game settings.
2. Move your character into the recommended fishing position described above.
3. Make sure the game window is visible.
4. Open a terminal in the folder containing `fishing.py`.
4. Run:

   ```bash
   python fishing.py
   ```

5. The script displays the monitoring area and current detection settings.
6. Fishing starts after a **3-second countdown**. Activate the Core Keeper window to receive right-click input.

The status line displays the number of fish caught, the current state, and the pixel change rate.

To stop the script, press **Ctrl+C** in the terminal.

> **Note:** The script sends right-click inputs to the active desktop window. Avoid using the mouse or switching windows while it is running.

## 3. Change the parameters

Open `fishing.py` in a text editor and edit the values in the **Configuration Parameters** section near the top of the file. Save the file and run it again for the changes to take effect.

| Parameter | Description |
|---|---|
| `AUTO_WINDOWSIZE` | Enables (`True`) or disables (`False`) automatic detection of the Core Keeper window and monitoring area. |
| `MONITOR_BOX` | Monitoring rectangle used for manual setup. Its values are screen coordinates and dimensions: `top`, `left`, `width`, and `height`. |
| `THRESHOLD` | Minimum grayscale pixel difference (0–255) treated as a changed pixel. Increasing this value makes detection less sensitive to small visual changes. |
| `DETECTION_PERCENT` | Percentage of pixels in the monitoring area that must change to trigger reeling. Increasing this value makes the bite detection less sensitive. |
| `CAST_DELAY` | Seconds to wait after casting before taking the reference screenshot. |
| `RESET_DELAY` | Seconds to wait after catching a fish before casting again. |
| `TIMEOUT_SEC` | Maximum number of seconds to wait for a bite before the script reels in and resets its waiting timer. |

### Example adjustments

- If small visual changes trigger reeling too often, try increasing `DETECTION_PERCENT` or `THRESHOLD`.
- If bites are not detected reliably, try decreasing `DETECTION_PERCENT` or `THRESHOLD`.
- If the reference screenshot is captured before the bobber has settled, try increasing `CAST_DELAY`.

Change values gradually and test each adjustment. The best settings can depend on your display resolution, game window size, and in-game conditions.

## Troubleshooting

- **The game window is not found:** Make sure Core Keeper is running and its window title contains `Core Keeper`. If detection still fails, use the manual setup above.
- **The monitoring area is in the wrong place:** Use manual setup and adjust `MONITOR_BOX` for your screen resolution and game window position.
- **The script reels in too early or too often:** Increase `THRESHOLD` or `DETECTION_PERCENT`, or make the monitoring area smaller and more focused.
- **The script does not detect bites:** Decrease `THRESHOLD` or `DETECTION_PERCENT`, and check that the monitoring area includes the bite indicator.
- **The script does not respond to right-clicks:** Make sure the Core Keeper window is active and that no other application is receiving the mouse input.

