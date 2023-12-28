import time
import pyautogui
import win32gui
import win32con
import ctypes

keystroke="1"
interval_seconds=1
window_name="World of Warcraft"

def is_window_focused(window_title):
    # Get the handle of the foreground window
    foreground_window = win32gui.GetForegroundWindow()

    # Get the title of the foreground window
    window_text = win32gui.GetWindowText(foreground_window)

    # Check if the window title matches the specified title
    return window_text == window_title

def press_key( keystroke):
    if is_window_focused (window_name):
        pyautogui.keyDown(keystroke)
        time.sleep(0.1)  
        pyautogui.keyUp(keystroke)


def attack_same_target_then_switch():
    time.sleep(1.8)
    press_key("1")
    time.sleep(1.8)
    press_key("1")
    time.sleep(1.8)
    press_key("1")
    time.sleep(1.8)
    press_key("1")
    time.sleep(1.8)
    press_key("tab")
def attack_target_then_switch():
    press_key("1")
    time.sleep(1.8)
    press_key("tab")

def get_focused_window_title():
    # Get the handle of the foreground window
    foreground_window = win32gui.GetForegroundWindow()

    # Get the title of the foreground window
    window_title = win32gui.GetWindowText(foreground_window)

    return window_title if window_title else ""



def repeat_keystroke():
    try:
        print("Press Ctrl+C to stop the script.")
        while True:
            if not is_window_focused (window_name):
                print("Wait "+get_focused_window_title())
                time.sleep(3)
            else:
                attack_target_then_switch()
                #attack_same_target_then_switch()
                
    

    except KeyboardInterrupt:
        print("\nScript stopped.")

if __name__ == "__main__":
     repeat_keystroke()

