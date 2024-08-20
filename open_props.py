import os
import subprocess
import pyautogui
import time

def open_folder_properties(target_path):
    folders = [f for f in os.listdir(target_path) if os.path.isdir(os.path.join(target_path, f))]

    for folder in folders:
        folder_path = os.path.abspath(os.path.join(target_path, folder))

        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            print(f"The path {folder_path} is not a valid directory.")
            continue

        # Open the folder in File Explorer and get the process object
        process = subprocess.Popen(f'explorer /select,"{folder_path}"')

        # Wait for a moment to ensure the window is opened
        time.sleep(2)

        # Simulate pressing Alt+Enter to open the properties window
        pyautogui.hotkey('alt', 'enter')

        # Wait for a moment to ensure the properties window is opened
        time.sleep(2)

        # Simulate pressing Alt+Tab to switch focus back to the Explorer window
        pyautogui.hotkey('alt', 'tab')

        # Wait a bit to ensure the focus is switched
        time.sleep(1)

        # Simulate pressing Ctrl+W to close the Explorer window
        pyautogui.hotkey('ctrl', 'w')

        # Wait for a moment to ensure the Explorer window is closed
        time.sleep(2)

if __name__ == "__main__":
    path = "C:/Users/yajie/AppData"
    # path = os.path.abspath(path)
    open_folder_properties(path)
