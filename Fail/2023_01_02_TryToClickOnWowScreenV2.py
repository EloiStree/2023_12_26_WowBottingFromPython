import psutil
import platform
import pyautogui
import time
import win32api
import win32process
import win32con
import pygetwindow as gw
from win32gui import FindWindow, GetWindowRect


import ctypes
from ctypes.wintypes import HWND, DWORD, RECT

wow_hyper_pid = [15564, 16496,19524 , 20036, 25404]
wow_hyper_pid = [788062, 527076,263738 , 527504, 656406]
wow_hyper_pid_handle=[]

process_name = "Wow.exe"
process_title = "World of Warcraft"

def set_focus_and_click(pid):
    # Get the window based on the process ID
    window = gw.getWindowsWithTitle(f"pid:{pid}")

    if not window:
        print(f"No window found with PID {pid}")
        return

    # Bring the window to focus
    window[0].activate()

    # Wait for a short time to ensure the window is brought to the front
    pyautogui.sleep(1)

    # Get the center coordinates of the window
    center_x = window[0].left + window[0].width // 2
    center_y = window[0].top + window[0].height // 2

    # Move the mouse to the center of the window and click
    pyautogui.click(center_x, center_y)


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




def get_process_tree(pid, tree=None):
    if tree is None:
        tree = {}

    process = psutil.Process(pid)
    children = process.children()

    if not children:
        return {pid: None}

    tree[pid] = {}

    for child in children:
        get_process_tree(child.pid, tree[pid])

    return tree

def flatten_process_tree(tree, flat_tree=None):
    if flat_tree is None:
        flat_tree = []

    for key, value in tree.items():
        flat_tree.append(key)
        if value:
            flatten_process_tree(value, flat_tree)

    return flat_tree

def get_parent_pid(pid):
    try:
        process = psutil.Process(pid)
        return process.ppid()
    except psutil.NoSuchProcess as e:
        print(f"Process with PID {pid} not found: {e}")
    except psutil.AccessDenied as e:
        print(f"Access denied to process with PID {pid}: {e}")

def get_display_info(pid):
    try:
        process = psutil.Process(pid)
        windows = gw.getWindowsWithTitle(process.name())

        if windows:
            main_window = windows[0]
            return {
                'title': main_window.title,
                'class': main_window.class_name,
                'rect': main_window.rect,
            }
        else:
            return None

    except psutil.NoSuchProcess as e:
        print(f"Process with PID {pid} not found: {e}")
    except psutil.AccessDenied as e:
        print(f"Access denied to process with PID {pid}: {e}")


def find_display_process(pid):
    try:
        # Get the main process
        main_process = psutil.Process(pid)

        # Get the descendants of the main process
        descendants = main_process.children(recursive=True)

        # Look for a process with a visible GUI window
        for descendant in descendants:
            windows = gw.getWindowsWithTitle(descendant.name())

            if windows:
                return {
                    'pid': descendant.pid,
                    'name': descendant.name(),
                    'title': windows[0].title,
                    'class': windows[0].class_name,
                    'rect': windows[0].rect,
                }

        return None

    except psutil.NoSuchProcess as e:
        print(f"Process with PID {pid} not found: {e}")
    except psutil.AccessDenied as e:
        print(f"Access denied to process with PID {pid}: {e}")

def get_window_handle(pid):
    try:
        process = psutil.Process(pid)
        process_name = process.name()

        # Get all windows with the same title as the process name
        windows = gw.getWindowsWithTitle(process_name)

        # Check if any window is associated with the given process
        for window in windows:
            if window.pid == pid:
                return window._hWnd  # Access the handle of the window

        return None  # No matching window found for the given PID

    except psutil.NoSuchProcess as e:
        print(f"Process with PID {pid} not found: {e}")
    except psutil.AccessDenied as e:
        print(f"Access denied to process with PID {pid}: {e}")


if __name__ == "__main__":

    #print (gw.getAllTitles())
    pt = get_window_handle(15564)
    window_rect   = GetWindowRect(pt)
    print(window_rect)
    
    process_tree = get_process_tree(15564)
    
    flattened_tree = flatten_process_tree(process_tree)
    parent_test=get_parent_pid(15564)
    print("Process tree:", parent_test)
    parent_test2=find_display_process(parent_test)
    print("Process tree:", parent_test2)
    set_focus_and_click(parent_test)

    main_process = psutil.Process(15564)

        # Get the descendants of the main process
    descendants = main_process.children(recursive=True)
    print("Childs :", descendants)

    
    set_focus_and_click(26916)
    

    print("Process tree:", flattened_tree)
 
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


    for target_pid in wow_hyper_pid:
        set_focus_and_click(target_pid)
