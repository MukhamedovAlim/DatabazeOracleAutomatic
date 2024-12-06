import os
import cv2
import pyautogui
import numpy as np
import time

def is_complete_detected_in_bottom_third(threshold=0.8):
    """
    Detect if the 'Complete' text or icon is visible in the bottom 1/3 of the screen.

    Args:
        threshold (float): Matching threshold (default: 0.8).

    Returns:
        bool: True if 'Complete' is detected, False otherwise.
    """
    # Get screen size
    screen_width, screen_height = pyautogui.size()

    # Define the region for the bottom 1/3 of the screen
    region = (0, screen_height * 2 // 3, screen_width, screen_height // 3)  # (x, y, width, height)

    # Define fixed paths
    current_dir = os.path.dirname(__file__)
    template_path = os.path.join(current_dir, "complete", "complete_template.png")
    screenshots_folder = os.path.join(current_dir, "screenshots")
    os.makedirs(screenshots_folder, exist_ok=True)
    screenshot_path = os.path.join(screenshots_folder, "bottom_third_screenshot.png")

    print(f"Looking for template at: {template_path}")

    # Check if template exists
    if not os.path.exists(template_path):
        raise ValueError(f"Template file not found at {template_path}")

    # Capture the bottom 1/3 of the screen
    screenshot = pyautogui.screenshot(region=region)
    #screenshot.save(screenshot_path)
    print(f"Screenshot of bottom third saved at: {screenshot_path}")

    # Read the screenshot and template as grayscale images
    screenshot_img = cv2.imread(screenshot_path, cv2.IMREAD_GRAYSCALE)
    template_img = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # Error handling
    if screenshot_img is None:
        raise ValueError(f"Screenshot file not found at {screenshot_path}")
    if template_img is None:
        raise ValueError(f"Template file not found or unreadable at {template_path}")

    # Perform template matching
    result = cv2.matchTemplate(screenshot_img, template_img, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)

    # Return True if matches are found
    return len(loc[0]) > 0

def scroll_through_list(threshold=0.8):
    """
    Scroll through a list and process each visible section.
    """
    processed_items = set()  # Keep track of processed items to avoid duplicates

    while True:
        # Detect items in the bottom third of the screen
        detected = is_complete_detected_in_bottom_third(threshold=threshold)

        if detected:
            print("Detected item in view!")
            # Add logic to process detected items (e.g., clicking) here
        else:
            print("No new items detected in view.")
            # Scroll down
            pyautogui.scroll(-500)  # Adjust scroll amount as needed
            time.sleep(1)  # Pause to let the screen update


        # Optional: Add logic to detect the end of the list
        if detected == False:  # If no items detected in consecutive scrolls
            print("End of the list detected. Stopping.")
            break

# Run the scrolling process
scroll_through_list()
