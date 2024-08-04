import psutil
import platform
import pyautogui
import win32gui
import time
import ctypes
import win32api
import win32process
import win32con
import pygetwindow as gw
wow_hyper_pid = [15564, 16496,19524 , 20036, 25404]
wow_hyper_pid_handle=[]

process_name = "Wow.exe"
process_title = "World of Warcraft"

def get_window_rect(hwnd):

    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        return rect
    else:
        print(f"Window with title '{window_title}' not found.")
        return None

def move_mouse_to_middle_of_window(hwnd):
    window_rect = get_window_rect(hwnd)
    if window_rect:
        middle_x = (window_rect[0] + window_rect[2]) // 2
        middle_y = (window_rect[1] + window_rect[3]) // 2
        pyautogui.moveTo(middle_x, middle_y)
        print(f"Mouse moved to the middle of the '{window_title}' window.")
    else:
        print("Unable to move mouse.")

def list_processes_by_title(process_title):
    processes = []

    for process in psutil.process_iter(['pid', 'name']):
        try:
            # Get the process object
            proc = psutil.Process(process.info['pid'])
            
            # Get the window title of the process
            if platform.system() == 'Windows':
                title = proc.exe()
            elif platform.system() == 'Linux':
                title = ' '.join(proc.cmdline())
            else:
                # Add support for other operating systems if needed
                title = ''

            # Check if the process title contains the specified title
            if process_title.lower() in title.lower():
                processes.append(process.info)
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            # Handle exceptions for processes that can't be accessed
            pass

    return processes


def get_processes_by_name(process_name):
    matching_processes = []
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            matching_processes.append(process.info['pid'])
    return matching_processes

def get_process_handle_by_pid(pid):
    PROCESS_ALL_ACCESS = 0x1F0FFF  # Adjust this value based on your requirements

    # Get process handle
    handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if handle == 0:
        print(f"Failed to open process with PID {pid}. Error code: {ctypes.windll.kernel32.GetLastError()}")
        return None
    else:
        print(f"Successfully obtained handle for process with PID {pid}.")
        return handle



def process_has_window_pid(pid):
    return process_has_window(get_process_handle_by_pid(pid))


def process_has_window(pid):
    try:
        
        rect = win32gui.GetWindowRect(pid)
        width = rect.width
        return width > 0
    except IndexError:
        print(f"No window found with title or PID: {pid}")
        return False
    
def set_foreground_window(pid):
    # Get the window handle for the specified PID
    hwnd = ctypes.windll.user32.FindWindowW(None, None)
    while hwnd:
        current_pid = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(current_pid))
        if current_pid.value == pid:
            # Set the foreground window
            ctypes.windll.user32.ShowWindow(hwnd, win32con.SW_RESTORE)
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            break
        hwnd = ctypes.windll.user32.GetWindow(hwnd, win32con.GW_HWNDNEXT)

def get_window_size_from_pid(pid):
    # Find the window handle based on the PID
    hwnd = ctypes.windll.user32.FindWindowW(None, None)
    while hwnd:
        current_pid = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(current_pid))
        if current_pid.value == pid:
            # Get the dimensions of the window
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            
            # Calculate the width and height
            width = rect.right - rect.left
            height = rect.bottom - rect.top
            
            return width, height
        
        hwnd = ctypes.windll.user32.GetWindow(hwnd, win32con.GW_HWNDNEXT)

    return None

def get_hwnd_from_pid(pid):
    hwnd_result = None
    
    def callback(hwnd, lParam):
        nonlocal hwnd_result
        current_pid = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(current_pid))
        
        if current_pid.value == pid:
            hwnd_result = hwnd
            return False  # Stop enumeration
        
        return True  # Continue enumeration
    
    # Enumerate all top-level windows
    ctypes.windll.user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(callback), 0)
    
    return hwnd_result

if __name__ == "__main__":


    matching_processes = get_processes_by_name(process_name)

    print("Process wow.exe")
    if matching_processes:
        print(f"Processes with name '{process_name}': {matching_processes}")
    else:
        print(f"No processes found with name '{process_name}'.")
        
    wow_processes = list_processes_by_title(process_title)


    print("Process title World of warcraft")
    if wow_processes:
        print(f"Processes with the title '{process_title}':")
        for process in wow_processes:
            print(f"PID: {process['pid']}, Name: {process['name']}")
    else:
        print(f"No processes found with the title '{process_title}'.")


    print(f"Will be use process {wow_hyper_pid}")
    for process in wow_hyper_pid:
        set_foreground_window(process)
        get_window_size_from_pid(process)
        wow_hyper_pid_handle.append(get_hwnd_from_pid(process))
        time.sleep(2)

    print(f"Will be use process {wow_hyper_pid_handle}")
    for process_handle in wow_hyper_pid_handle:
        print(process_handle)
        time.sleep(2)
        
