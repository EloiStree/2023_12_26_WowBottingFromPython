from win32gui import GetWindowRect, GetForegroundWindow
import time
import psutil
import pygetwindow as gw
import win32process


def set_active_window_by_pid(pid):
    try:
        # Find the window handle by the given PID
        hwnd = win32gui.FindWindow(None, None)  # Iterate over all windows
        while hwnd:
            window_pid = win32process.GetWindowThreadProcessId(hwnd)[1]
            if window_pid == pid:
                # Set the window as active
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restore if minimized
                win32gui.SetForegroundWindow(hwnd)
                break
            hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
    except Exception as e:
        print(f"An error occurred: {e}")

def get_active_window_pid():
    # Get the active window title
    active_window_title = gw.getActiveWindow().title

    # Iterate through all processes and find the one with a matching window title
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info.get('name') is not None and active_window_title in ' '.join(process.info.get('cmdline', [])):
            return process.info['pid']

    return None

def get_active_window_info():
    # Get the handle of the active window
    hwnd = GetForegroundWindow()

    # Get window dimensions (left, top, right, bottom)
    rect = GetWindowRect(hwnd)
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]

    # Get window position (x, y)
    position = (rect[0], rect[1])

    # Get the Process ID (PID) of the active window
    _, pid = win32process.GetWindowThreadProcessId(hwnd)

    return {
        'dimension': {'width': width, 'height': height},
        'position': {'x': position[0], 'y': position[1]},
        'pid': pid
    }
def display_all_info():
    try:
        
        active_window_info = get_active_window_info()

        print("Active Window Information:")
        print("Dimensions:", active_window_info['dimension'])
        print("Position:", active_window_info['position'])
        print("PID:", active_window_info['pid'])
        print("PIDS:",get_active_window_pid())
    except Exception as e:
        print(f"An error occurred: {e}")


time.sleep(2)
set_active_window_by_pid(20036)


while True:
    display_all_info()
    time.sleep(1)





