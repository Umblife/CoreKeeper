import cv2
import mss
import numpy as np
import pyautogui
import pygetwindow as gw
import time
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

# --- Configuration Parameters ------------------------------------------------
# Automatically detect the game window size
AUTO_WINDOWSIZE = True
# Manual: Coordinates and size of the monitoring area (just above the character's head)
MONITOR_BOX = {"top": 515, "left": 1255, "width": 70, "height": 60}

# Sensitivity settings for change detection
#   THRESHOLD: Minimum pixel color difference (0-255) to consider as a change
#   DETECTION_PERCENT: Percentage of the area that must change to trigger the reel (0.0 - 100.0)
THRESHOLD = 30
DETECTION_PERCENT = 40.0  # Example: Triggers when 40% or more of the pixels change

# Fishing cycle and timing management
CAST_DELAY = 0.5    # Time (seconds) from casting the line until the bobber hits the water
RESET_DELAY = 3.0   # Wait time (seconds) after catching a fish before the next cast
# CLICK_DELAY = 0.2   # Wait time (seconds) after the pixel change exceeds the threshold
TIMEOUT_SEC = 15.0  # Max wait time (seconds) while waiting for a bite (anti-bug safety feature)


# --- Determine the monitoring area -------------------------------------------
def get_game_monitor_box():
    """Find the Core Keeper window and calculate the monitoring area using WQHD-based proportions."""
    try:
        windows = gw.getWindowsWithTitle('Core Keeper')
        if not windows:
            raise Exception("Core Keeper window not found. Please start the game.")

        game_win = windows[0]

        win_left = game_win.left
        win_top = game_win.top
        win_width = game_win.width
        win_height = game_win.height

        center_x = win_left + (win_width // 2)
        center_y = win_top + (win_height // 2)

        # Calculate the offsets based on the window resolution
        # Based on measurements at WQHD resolution: {"top": 515, "left": 1255, "width": 70, "height": 60}
        offset_x = int(win_width * 0.00976)
        offset_y = int(win_height * 0.14236)

        # Scale the monitoring area to the window resolution (70x60 at WQHD)
        box_width = int(win_width * (70 / 2560))
        box_height = int(win_height * (60 / 1440))

        # Set the monitoring area
        monitor_box = {
            "top": center_y - offset_y,
            "left": center_x - offset_x,
            "width": box_width,
            "height": box_height
        }

        print(f"Core Keeper window detected: position=({win_left}, {win_top}), size={win_width}x{win_height}")
        return monitor_box

    except Exception as e:
        print(f"Error: {e}")
        return None


# --- Main Logic --------------------------------------------------------------
def main():
    monitor_box = get_game_monitor_box() if AUTO_WINDOWSIZE else None
    # Use a local variable for the active monitoring area settings
    monitor_box = MONITOR_BOX if monitor_box is None else monitor_box
    print(f"Monitoring area: {monitor_box}")

    total_pixels = monitor_box["width"] * monitor_box["height"]
    print(f"Settings: Monitoring area = {total_pixels} pixels | Detection threshold = {DETECTION_PERCENT}%")
    print("Fishing will start in 3 seconds. Make sure the game window is active.\n")
    time.sleep(3)

    fish_count = 0  # Number of fish caught
    with mss.mss() as sct:
        while True:
            # Cast the fishing line
            pyautogui.rightClick()

            # --- Status: Line cast ---
            current_percent = 0.0
            print(
                "\033[F"
                f"Count: {fish_count:<54}\n"
                f"[Status]: Cast    | Pixel Change Rate: {current_percent:5.2f}%",
                end="", flush=True)

            time.sleep(CAST_DELAY)

            # Capture the initial frame to use as the reference image
            img_initial = np.array(sct.grab(monitor_box))
            gray_initial = cv2.cvtColor(img_initial, cv2.COLOR_BGRA2GRAY)

            # Record the start time for the bite detection period
            start_waiting_time = time.time()

            fishing_loop = True
            while fishing_loop:
                # Capture the current frame
                img_current = np.array(sct.grab(monitor_box))
                gray_current = cv2.cvtColor(img_current, cv2.COLOR_BGRA2GRAY)

                # Calculate the absolute difference between the reference and current frames
                diff = cv2.absdiff(gray_initial, gray_current)
                _, thresh = cv2.threshold(diff, THRESHOLD, 255, cv2.THRESH_BINARY)

                # Calculate the percentage of pixels that have changed
                changed_pixels = np.sum(thresh == 255)
                current_percent = (changed_pixels / total_pixels) * 100.0

                # --- Status: Waiting for a bite ---
                print(
                    "\033[F"
                    f"Count: {fish_count:<54}\n"
                    f"[Status]: Waiting | Pixel Change Rate: {current_percent:5.2f}%",
                    end="", flush=True)

                # Check whether the pixel change exceeds the threshold (indicating a bite)
                if current_percent >= DETECTION_PERCENT:
                    # Reel in the fish
                    pyautogui.rightClick() 
                    fish_count += 1     # Increment the fish counter

                    # --- Status: Fish caught ---
                    print(
                        "\033[F"
                        f"Count: {fish_count:<54}\n"
                        f"[Status]: Catch!  | Pixel Change Rate: {current_percent:5.2f}%",
                        end="", flush=True)
                    fishing_loop = False  
                    time.sleep(RESET_DELAY) 

                # Handle a timeout if no bite is detected within the specified period
                elif (time.time() - start_waiting_time) > TIMEOUT_SEC:
                    # Reel in the line and reset the fishing state
                    pyautogui.rightClick()
                    time.sleep(CAST_DELAY)  # Wait for the reel-in animation to finish before trying again
                    start_waiting_time = time.time()

                    # --- Status: Timed out ---
                    print(
                        "\033[F"
                        f"Count: {fish_count:<54}\n"
                        f"[Status]: Timeout | Pixel Change Rate: {current_percent:5.2f}%",
                        end="", flush=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScript stopped by user.")
