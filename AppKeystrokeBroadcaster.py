import time
import pyautogui
import win32gui
import win32con
import ctypes
import socket
import threading

# https://learn.microsoft.com/en-us/windows/win32/inputdev/about-keyboard-input#virtual-key-codes-described

listen_port=4758
keystroke="1"
interval_seconds=1
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
VK_1 = 0x31       # Alphanumeric 1


# We will store all the wow window when the script is launch here
target_windows=[]

# This methode will fetch all the window with the given title
def get_windows_by_title(title):
    windows = []
    win32gui.EnumWindows(lambda hwnd, _: windows.append((hwnd, win32gui.GetWindowText(hwnd))), None)
    return [hwnd for hwnd, window_title in windows if title.lower() in window_title.lower()]


# This methode press a target window with and int unique id
def press_key_hwnd(hwnd, key):
    ctypes.windll.user32.PostMessageW(hwnd, WM_KEYDOWN, key, 0)
                                      
# This methode release a target window with and int unique id, 0)
def release_key_hwnd(hwnd, key):
    ctypes.windll.user32.PostMessageW(hwnd, WM_KEYUP, key, 0)

def press_and_release_key_hwnd(hwnd, key):
    press_key(hwnd, key)
    time.sleep(0.1)  # Adjust the delay as needed
    release_key(hwnd, key)

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



def broadcast_key_click( keystroke):
    if  isinstance(keystroke, int):
            print(keystroke)
            wow_press(keystroke)
            time.sleep(0.1)  
            wow_release(keystroke)
            




def repeat_keystroke():
    try:
        print("Press Ctrl+C to stop the script.")
        
        global target_windows
        target_windows = get_windows_by_title(window_name)
        print(len(target_windows))
        for a in target_windows:
            print(f"W:{a}")
        while True:
            #attack_target_then_switch()
            attack_target_then_switch_post()
            #attack_same_target_then_switch()
                
    

    except KeyboardInterrupt:
        print("\nScript stopped.")



def handle_message(message):

    print(f"Received message: {message}")
    if message.startswith("h:"):
        message = message[2:]
        
        try:
            keyid = int (message,16)
            #broadcast_key_click(hex(keyid))
            broadcast_key_click(keyid)
            
        except ValueError:
            print(f"{my_string} is not a valid integer.")
            
    if message.startswith("i:"):
        message = message[2:]
        
        try:
            keyid = int (message)
            #broadcast_key_click(hex(keyid))
            broadcast_key_click(keyid)
            
        except ValueError:
            print(f"{my_string} is not a valid integer.")

    if message.startswith("s:"):
        message = message[2:]
        if message.startswith("window:"):
            message = message[len("window:"):]
            print(f"Reset target window to {message}")
            target_windows = get_windows_by_title(message)

                

        

def udp_server(host, port):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to a specific address and port
    server_socket.bind((host, port))
    
    print(f"UDP server listening on port {port}")
    
    while True:
        # Receive data from the socket
        data, address = server_socket.recvfrom(1024)
        
        # Decode the received data
        message = data.decode('utf-8')
        
        # Perform an action based on the received message
        handle_message(message)


if __name__ == "__main__":

    target_windows = get_windows_by_title(window_name)
    for target in target_windows:
        print(target)
    udp_thread = threading.Thread(target=udp_server, args=('0.0.0.0', listen_port), daemon=True)
    udp_thread.start()
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping UDP server...")

"""

WM_KEYDOWN = 0x0100
VK_SHIFT = 0x10
VK_CONTROL = 0x11
VK_MENU = 0x12
VK_PAUSE = 0x13
VK_CAPITAL = 0x14
VK_KANA = 0x15
VK_HANGUL = VK_KANA
VK_JUNJA = 0x17
VK_FINAL = 0x18
VK_HANJA = 0x19
VK_KANJI = VK_HANJA
VK_ESCAPE = 0x1B
VK_CONVERT = 0x1C
VK_NONCONVERT = 0x1D
VK_ACCEPT = 0x1E
VK_MODECHANGE = 0x1F
VK_SPACE = 0x20
VK_PRIOR = 0x21
VK_NEXT = 0x22
VK_END = 0x23
VK_HOME = 0x24
VK_LEFT = 0x25
VK_UP = 0x26
VK_RIGHT = 0x27
VK_DOWN = 0x28
VK_SELECT = 0x29
VK_PRINT = 0x2A
VK_EXECUTE = 0x2B
VK_SNAPSHOT = 0x2C
VK_INSERT = 0x2D
VK_DELETE = 0x2E
VK_HELP = 0x2F
VK_0 = 0x30
VK_1 = 0x31
VK_2 = 0x32
VK_3 = 0x33
VK_4 = 0x34
VK_5 = 0x35
VK_6 = 0x36
VK_7 = 0x37
VK_8 = 0x38
VK_9 = 0x39
VK_A = 0x41
VK_B = 0x42
VK_C = 0x43
VK_D = 0x44
VK_E = 0x45
VK_F = 0x46
VK_G = 0x47
VK_H = 0x48
VK_I = 0x49
VK_J = 0x4A
VK_K = 0x4B
VK_L = 0x4C
VK_M = 0x4D
VK_N = 0x4E
VK_O = 0x4F
VK_P = 0x50
VK_Q = 0x51
VK_R = 0x52
VK_S = 0x53
VK_T = 0x54
VK_U = 0x55
VK_V = 0x56
VK_W = 0x57
VK_X = 0x58
VK_Y = 0x59
VK_Z = 0x5A
VK_LWIN = 0x5B
VK_RWIN = 0x5C
VK_APPS = 0x5D
VK_SLEEP = 0x5F
VK_NUMPAD0 = 0x60
VK_NUMPAD1 = 0x61
VK_NUMPAD2 = 0x62
VK_NUMPAD3 = 0x63
VK_NUMPAD4 = 0x64
VK_NUMPAD5 = 0x65
VK_NUMPAD6 = 0x66
VK_NUMPAD7 = 0x67
VK_NUMPAD8 = 0x68
VK_NUMPAD9 = 0x69
VK_MULTIPLY = 0x6A
VK_ADD = 0x6B
VK_SEPARATOR = 0x6C
VK_SUBTRACT = 0x6D
VK_DECIMAL = 0x6E
VK_DIVIDE = 0x6F
VK_F1 = 0x70
VK_F2 = 0x71
VK_F3 = 0x72
VK_F4 = 0x73
VK_F5 = 0x74
VK_F6 = 0x75
VK_F7 = 0x76
VK_F8 = 0x77
VK_F9 = 0x78
VK_F10 = 0x79
VK_F11 = 0x7A
VK_F12 = 0x7B
VK_F13 = 0x7C
VK_F14 = 0x7D
VK_F15 = 0x7E
VK_F16 = 0x7F
VK_F17 = 0x80
VK_F18 = 0x81
VK_F19 = 0x82
VK_F20 = 0x83
VK_F21 = 0x84
VK_F22 = 0x85
VK_F23 = 0x86
VK_F24 = 0x87
VK_NUMLOCK = 0x90
VK_SCROLL = 0x91
VK_OEM_NEC_EQUAL = 0x92
VK_OEM_FJ_JISHO = 0x92
VK_OEM_FJ_MASSHOU = 0x93
VK_OEM_FJ_TOUROKU = 0x94
VK_OEM_FJ_LOYA = 0x95
VK_OEM_FJ_ROYA = 0x96
VK_LSHIFT = 0xA0
VK_RSHIFT = 0xA1
VK_LCONTROL = 0xA2
VK_RCONTROL = 0xA3
VK_LMENU = 0xA4
VK_RMENU = 0xA5
VK_BROWSER_BACK = 0xA6
VK_BROWSER_FORWARD = 0xA7
VK_BROWSER_REFRESH = 0xA8
VK_BROWSER_STOP = 0xA9
VK_BROWSER_SEARCH = 0xAA
VK_BROWSER_FAVORITES = 0xAB
VK_BROWSER_HOME = 0xAC
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_STOP = 0xB2
VK_MEDIA_PLAY_PAUSE = 0xB3
VK_LAUNCH_MAIL = 0xB4
VK_LAUNCH_MEDIA_SELECT = 0xB5
VK_LAUNCH_APP1 = 0xB6
VK_LAUNCH_APP2 = 0xB7
VK_OEM_1 = 0xBA
VK_OEM_PLUS = 0xBB
VK_OEM_COMMA = 0xBC
VK_OEM_MINUS = 0xBD
VK_OEM_PERIOD = 0xBE
VK_OEM_2 = 0xBF
VK_OEM_3 = 0xC0
VK_OEM_4 = 0xDB
VK_OEM_5 = 0xDC
VK_OEM_6 = 0xDD
VK_OEM_7 = 0xDE
VK_OEM_8 = 0xDF
VK_OEM_AX = 0xE1
VK_OEM_102 = 0xE2
VK_ICO_HELP = 0xE3
VK_ICO_00 = 0xE4
VK_PROCESSKEY = 0xE5
VK_ICO_CLEAR = 0xE6
VK_PACKET = 0xE7
VK_OEM_RESET = 0xE9
VK_OEM_JUMP = 0xEA
VK_OEM_PA1 = 0xEB
VK_OEM_PA2 = 0xEC
VK_OEM_PA3 = 0xED
VK_OEM_WSCTRL = 0xEE
VK_OEM_CUSEL = 0xEF
VK_OEM_ATTN = 0xF0
VK_OEM_FINISH = 0xF1
VK_OEM_COPY = 0xF2
VK_OEM_AUTO = 0xF3
VK_OEM_ENLW = 0xF4
VK_OEM_BACKTAB = 0xF5
VK_ATTN = 0xF6
VK_CRSEL = 0xF7
VK_EXSEL = 0xF8
VK_EREOF = 0xF9
VK_PLAY = 0xFA
VK_ZOOM = 0xFB
VK_NONAME = 0xFC
VK_PA1 = 0xFD
VK_OEM_CLEAR = 0xFE

"""
