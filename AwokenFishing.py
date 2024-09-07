import time
import pyautogui
import win32gui
import win32con
import ctypes
import random

# https://learn.microsoft.com/en-us/windows/win32/inputdev/about-keyboard-input#virtual-key-codes-described


window_name="World of Warcraft"

useRealKey=False



# Constants
# Will be use to press an release
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
# If you want to use numpad
KEY_NumpadPlus = 0x6B
KEY_NumpadMinus = 0x6D
KEY_NumpadDivide = 0x6F
KEY_NumpadMultiply = 0x6A
KEY_NumpadDecimal = 0x6E


# Some id that you will probably use
VK_SPACE = 0x20    # Space
VK_TAB = 0x09      # Tab
VK_ENTER = 0x0D    # Enter
VK_ESCAPE = 0x1B   # Escape

KEY_ArrowLeft = 0x25
KEY_ArrowUp = 0x26
KEY_ArrowRight = 0x27
KEY_ArrowDown = 0x28
KEY_Numpad0 = 0x60
KEY_Numpad1 = 0x61
KEY_Numpad2 = 0x62
KEY_Numpad3 = 0x63
KEY_Numpad4 = 0x64
KEY_Numpad5 = 0x65
KEY_Numpad6 = 0x66
KEY_Numpad7 = 0x67
KEY_Numpad8 = 0x68
KEY_Numpad9 = 0x69

VK_LEFT = 0x25     # Left arrow
VK_UP = 0x26       # Up arrow
VK_RIGHT = 0x27    # Right arrow
VK_DOWN = 0x28     # Down arrow

VK_NUMPAD1 = 0x61  # Numpad 1
VK_0 = 0x30       # Alphanumeric 1
VK_1 = 0x31       # Alphanumeric 1
VK_2 = 0x32       # Alphanumeric 1
VK_3 = 0x33       # Alphanumeric 1
VK_4 = 0x34       # Alphanumeric 1
VK_5 = 0x35       # Alphanumeric 1
VK_6 = 0x36       # Alphanumeric 1
VK_7 = 0x37       # Alphanumeric 1
VK_8 = 0x38       # Alphanumeric 1
VK_9 = 0x39        # Alphanumeric 1
VK_L = 0x4C 		# Alphanumeric 1
VK_F = 0x46 		# Alphanumeric 1


# We will store all the wow window when the script is launch here
target_windows=[]

# This methode will fetch all the window with the given title
def get_windows_by_title(title):
    windows = []
    win32gui.EnumWindows(lambda hwnd, _: windows.append((hwnd, win32gui.GetWindowText(hwnd))), None)
    return [hwnd for hwnd, window_title in windows if title.lower() in window_title.lower()]

def refresh_windows_by_title():
    global target_windows
    target_windows=get_windows_by_title(window_name)


def write_chat_message(message):
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.typewrite(message)
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)




  





# This methode press a target window with and int unique id
def press_key_hwnd(hwnd, key):
    ctypes.windll.user32.PostMessageW(hwnd, WM_KEYDOWN, key, 0)
                                      
# This methode release a target window with and int unique id, 0)
def release_key_hwnd(hwnd, key):
    ctypes.windll.user32.PostMessageW(hwnd, WM_KEYUP, key, 0)

def press_and_release_key_hwnd(hwnd, key):
    press_key_hwnd(hwnd, key)
    time.sleep(0.1)  # Adjust the delay as needed
    release_key_hwnd(hwnd, key)

def enum_child_windows(hwnd, lParam):
    child_windows.append(hwnd)
    return True


def wow_press(key):
    send_key_press_to_children(key)
    
def wow_release(key):
    send_key_release_to_children(key)
    
def wow_click(key):
    send_key_click_to_children(key)

 # If you want to send a key to a window and it children base on his name   
def send_key_release_to_children_title(window_title, key):
    hwnd_main = ctypes.windll.user32.FindWindowW(None, window_title)
    if hwnd_main == 0:
        print(f"Window with title '{window_title}' not found.")
        return

    release_key_hwnd(hwnd_main, key)
    global child_windows
    child_windows = []
    ctypes.windll.user32.EnumChildWindows(hwnd_main, ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_long, ctypes.c_long)(enum_child_windows), 0)

    for hwnd_child in child_windows:
        release_key_hwnd(hwnd_child, key)

# Release all the recorded targets at start with given window key (as int)
def send_key_release_to_children( key):
    for hwnd_main in target_windows:

        if hwnd_main == 0:
            print(f"Window with title '{window_title}' not found.")
            return

        release_key_hwnd(hwnd_main, key)
        global child_windows
        child_windows = []
        ctypes.windll.user32.EnumChildWindows(hwnd_main, ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_long, ctypes.c_long)(enum_child_windows), 0)

        for hwnd_child in child_windows:
            release_key_hwnd(hwnd_child, key)

# Press and release all the recorded targets at start with given window key (as int)
def send_key_click_to_children( key):
    for hwnd_main in target_windows:

        if hwnd_main == 0:
            print(f"Window with title '{window_title}' not found.")
            return
        
        print(f"{hwnd_main} {key}")
        press_and_release_key_hwnd(hwnd_main, key)
        global child_windows
        child_windows = []
        ctypes.windll.user32.EnumChildWindows(hwnd_main, ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_long, ctypes.c_long)(enum_child_windows), 0)

        for hwnd_child in child_windows:
            press_and_release_key_hwnd(hwnd_child, key)

# Press all the recorded targets at start with given window key (as int)
def send_key_press_to_children( key):
    for hwnd_main in target_windows:
        #hwnd_main = ctypes.windll.user32.FindWindowW(None, window_title)
        if hwnd_main == 0:
            print(f"Window with title '{window_title}' not found.")
            return
        press_key_hwnd(hwnd_main, key)
        global child_windows
        child_windows = []
        ctypes.windll.user32.EnumChildWindows(hwnd_main, ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_long, ctypes.c_long)(enum_child_windows), 0)

        for hwnd_child in child_windows:
            press_key_hwnd(hwnd_child, key)



# -------------------


key_target_one=VK_7
key_target_two=VK_8
key_pet_attack=VK_1
key_pet_back=VK_2
key_pet_dismiss=VK_3
key_pet_heal=VK_4
key_pet_call=VK_5
key_pet_rez=VK_9
key_pet_invoke_pet1=VK_6

key_space=VK_SPACE


def sometimes_jump():
    if random.randint(0, 100) < 30:
        wow_click(key_space)

def call_back_rez():
    wow_click(key_pet_dismiss)
    time.sleep(4)
    wow_click(key_pet_invoke_pet1)
    time.sleep(2)
    check_target()
    wow_click(key_pet_rez)
    wow_click(key_pet_heal)
    check_target()
    time.sleep(2)
    
def fetch_target():
    time_for_pet_to_go=15
    #select_target_one()
    wow_click(key_target_one)
    #send_pet_to_attack()
    wow_click(key_pet_attack)
    #wait_for_pet_to_go(time_for_pet_to_go)
    time.sleep(time_for_pet_to_go)
    #slect_target_two()
    wow_click(key_target_two)
    #send_pet_to_attack()
    wow_click(key_pet_attack)
    #wait_for_pet_to_go(3)

def check_target():
    wow_click(key_target_two)
    wow_click(key_pet_attack)
    time.sleep(0.1)
    wow_click(key_target_one)
    
    wow_click(key_pet_attack)


def coroutine_steps():
    
    wow_click(key_space)
    time_for_respawn=60
    time_for_respawn=13
    power_time_delay=1.9
    check_time =3
    wow_click(key_space)
    time.sleep(2)
    while True:
        
        call_back_rez()
        time.sleep(5)
        fetch_target()
        check = int(time_for_respawn/check_time)
        #check ever n second the time of the respawn
        for i in range( check):
            print (f"Time to respawn {time_for_respawn-i*check_time}")
            time.sleep(check_time)
            check_target()

        sometimes_jump()
        
        #jump_once_()

## /targetexact Silent Boris
## /targetexact Lindel the snatcher

def loop_attack():
    while True:
        #select_target_one()
        wow_click(VK_TAB)
        wow_click(VK_1)
        wow_click(VK_2)
        wow_click(VK_3)
        wow_click(VK_4)
        wow_click(VK_5)
        time.sleep(2)
        wow_click(VK_F)
        print("Attack")
    

if __name__ == "__main__":
    refresh_windows_by_title()
    print(window_name)
    print(target_windows)
    coroutine_steps()
    loop_attack()
