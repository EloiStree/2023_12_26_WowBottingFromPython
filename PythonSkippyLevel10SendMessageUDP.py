import time
import pyautogui
import win32gui
import win32con
import ctypes
import socket
import threading
import pygetwindow as gw
import time

# https://learn.microsoft.com/en-us/windows/win32/inputdev/about-keyboard-input#virtual-key-codes-described

listen_port=4758
keystroke="1"
interval_seconds=1
window_name="World of Warcraft"

# Will be use to press an release
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101



class KeyToExa:
    def __init__(self, vk_key, exa_value):
        self.m_vkKey = vk_key
        self.m_exaValue = exa_value

    def get_value_as_int(self):
        hex_string = self.m_exaValue
        if hex_string.startswith("0x"):
            hex_string = hex_string[2:]
        return int(hex_string, 16)

    def is_equal_key(self, value):
        if value is None:
            return False
        return self.m_vkKey == value

    def is_equal_exa_value(self, value):
        if value is None:
            return False
        return self.m_exaValue == value
class KeyToExa:
    def __init__(self, vk_key, exa_value):
        self.m_vkKey = vk_key
        self.m_exaValue = exa_value

    def get_value_as_int(self):
        hex_string = self.m_exaValue
        if hex_string.startswith("0x"):
            hex_string = hex_string[2:]
        return int(hex_string, 16)

    def is_equal_key(self, value):
        if value is None:
            return False
        return self.m_vkKey == value

    def is_equal_exa_value(self, value):
        if value is None:
            return False
        return self.m_exaValue == value



key_to_exa_array = [
    KeyToExa("VK_LBUTTON", "0x01"),
    KeyToExa("VK_RBUTTON", "0x02"),
    KeyToExa("VK_CANCEL", "0x03"),
    KeyToExa("VK_MBUTTON", "0x04"),
    KeyToExa("VK_XBUTTON1", "0x05"),
    KeyToExa("VK_XBUTTON2", "0x06"),
    KeyToExa("VK_BACK", "0x08"),
    KeyToExa("VK_TAB", "0x09"),
    KeyToExa("VK_CLEAR", "0x0C"),
    KeyToExa("VK_RETURN", "0x0D"),
    KeyToExa("VK_SHIFT", "0x10"),
    KeyToExa("VK_CONTROL", "0x11"),
    KeyToExa("VK_MENU", "0x12"),
    KeyToExa("VK_PAUSE", "0x13"),
    KeyToExa("VK_CAPITAL", "0x14"),
    KeyToExa("VK_KANA", "0x15"),
    KeyToExa("VK_HANGUL", "0x15"),
    KeyToExa("VK_JUNJA", "0x17"),
    KeyToExa("VK_FINAL", "0x18"),
    KeyToExa("VK_HANJA", "0x19"),
    KeyToExa("VK_KANJI", "0x19"),
    KeyToExa("VK_ESCAPE", "0x1B"),
    KeyToExa("VK_CONVERT", "0x1C"),
    KeyToExa("VK_NONCONVERT", "0x1D"),
    KeyToExa("VK_ACCEPT", "0x1E"),
    KeyToExa("VK_MODECHANGE", "0x1F"),
    KeyToExa("VK_SPACE", "0x20"),
    KeyToExa("VK_PRIOR", "0x21"),
    KeyToExa("VK_NEXT", "0x22"),
    KeyToExa("VK_END", "0x23"),
    KeyToExa("VK_HOME", "0x24"),
    KeyToExa("VK_LEFT", "0x25"),
    KeyToExa("VK_UP", "0x26"),
    KeyToExa("VK_RIGHT", "0x27"),
    KeyToExa("VK_DOWN", "0x28"),
    KeyToExa("VK_SELECT", "0x29"),
    KeyToExa("VK_PRINT", "0x2A"),
    KeyToExa("VK_EXECUTE", "0x2B"),
    KeyToExa("VK_SNAPSHOT", "0x2C"),
    KeyToExa("VK_INSERT", "0x2D"),
    KeyToExa("VK_DELETE", "0x2E"),
    KeyToExa("VK_HELP", "0x2F"),
    KeyToExa("VK_0", "0x30"),
    KeyToExa("VK_1", "0x31"),
    KeyToExa("VK_2", "0x32"),
    KeyToExa("VK_3", "0x33"),
    KeyToExa("VK_4", "0x34"),
    KeyToExa("VK_5", "0x35"),
    KeyToExa("VK_6", "0x36"),
    KeyToExa("VK_7", "0x37"),
    KeyToExa("VK_8", "0x38"),
    KeyToExa("VK_9", "0x39"),
    KeyToExa("VK_A", "0x41"),
    KeyToExa("VK_B", "0x42"),
    KeyToExa("VK_C", "0x43"),
    KeyToExa("VK_D", "0x44"),
    KeyToExa("VK_E", "0x45"),
    KeyToExa("VK_F", "0x46"),
    KeyToExa("VK_G", "0x47"),
    KeyToExa("VK_H", "0x48"),
    KeyToExa("VK_I", "0x49"),
    KeyToExa("VK_J", "0x4A"),
    KeyToExa("VK_K", "0x4B"),
    KeyToExa("VK_L", "0x4C"),
    KeyToExa("VK_M", "0x4D"),
    KeyToExa("VK_N", "0x4E"),
    KeyToExa("VK_O", "0x4F"),
    KeyToExa("VK_P", "0x50"),
    KeyToExa("VK_Q", "0x51"),
    KeyToExa("VK_R", "0x52"),
    KeyToExa("VK_S", "0x53"),
    KeyToExa("VK_T", "0x54"),
    KeyToExa("VK_U", "0x55"),
    KeyToExa("VK_V", "0x56"),
    KeyToExa("VK_W", "0x57"),
    KeyToExa("VK_X", "0x58"),
    KeyToExa("VK_Y", "0x59"),
    KeyToExa("VK_Z", "0x5A"),
    KeyToExa("VK_LWIN", "0x5B"),
    KeyToExa("VK_RWIN", "0x5C"),
    KeyToExa("VK_APPS", "0x5D"),
    KeyToExa("VK_SLEEP", "0x5F"),
    KeyToExa("VK_NUMPAD0", "0x60"),
    KeyToExa("VK_NUMPAD1", "0x61"),
    KeyToExa("VK_NUMPAD2", "0x62"),
    KeyToExa("VK_NUMPAD3", "0x63"),
    KeyToExa("VK_NUMPAD4", "0x64"),
    KeyToExa("VK_NUMPAD5", "0x65"),
    KeyToExa("VK_NUMPAD6", "0x66"),
    KeyToExa("VK_NUMPAD7", "0x67"),
    KeyToExa("VK_NUMPAD8", "0x68"),
    KeyToExa("VK_NUMPAD9", "0x69"),
    KeyToExa("VK_MULTIPLY", "0x6A"),
    KeyToExa("VK_ADD", "0x6B"),
    KeyToExa("VK_SEPARATOR", "0x6C"),
    KeyToExa("VK_SUBTRACT", "0x6D"),
    KeyToExa("VK_DECIMAL", "0x6E"),
    KeyToExa("VK_DIVIDE", "0x6F"),
    KeyToExa("VK_F1", "0x70"),
    KeyToExa("VK_F2", "0x71"),
    KeyToExa("VK_F3", "0x72"),
    KeyToExa("VK_F4", "0x73"),
    KeyToExa("VK_F5", "0x74"),
    KeyToExa("VK_F6", "0x75"),
    KeyToExa("VK_F7", "0x76"),
    KeyToExa("VK_F8", "0x77"),
    KeyToExa("VK_F9", "0x78"),
    KeyToExa("VK_F10", "0x79"),
    KeyToExa("VK_F11", "0x7A"),
    KeyToExa("VK_F12", "0x7B"),
    KeyToExa("VK_F13", "0x7C"),
    KeyToExa("VK_F14", "0x7D"),
    KeyToExa("VK_F15", "0x7E"),
    KeyToExa("VK_F16", "0x7F"),
    KeyToExa("VK_F17", "0x80"),
    KeyToExa("VK_F18", "0x81"),
    KeyToExa("VK_F19", "0x82"),
    KeyToExa("VK_F20", "0x83"),
    KeyToExa("VK_F21", "0x84"),
    KeyToExa("VK_F22", "0x85"),
    KeyToExa("VK_F23", "0x86"),
    KeyToExa("VK_F24", "0x87"),
    KeyToExa("VK_NUMLOCK", "0x90"),
    KeyToExa("VK_SCROLL", "0x91"),
    KeyToExa("VK_OEM_NEC_EQUAL", "0x92"),
    KeyToExa("VK_OEM_FJ_JISHO", "0x92"),
    KeyToExa("VK_OEM_FJ_MASSHOU", "0x93"),
    KeyToExa("VK_OEM_FJ_TOUROKU", "0x94"),
    KeyToExa("VK_OEM_FJ_LOYA", "0x95"),
    KeyToExa("VK_OEM_FJ_ROYA", "0x96"),
    KeyToExa("VK_LSHIFT", "0xA0"),
    KeyToExa("VK_RSHIFT", "0xA1"),
    KeyToExa("VK_LCONTROL", "0xA2"),
    KeyToExa("VK_RCONTROL", "0xA3"),
    KeyToExa("VK_LMENU", "0xA4"),
    KeyToExa("VK_RMENU", "0xA5"),
    KeyToExa("VK_BROWSER_BACK", "0xA6"),
    KeyToExa("VK_BROWSER_FORWARD", "0xA7"),
    KeyToExa("VK_BROWSER_REFRESH", "0xA8"),
    KeyToExa("VK_BROWSER_STOP", "0xA9"),
    KeyToExa("VK_BROWSER_SEARCH", "0xAA"),
    KeyToExa("VK_BROWSER_FAVORITES", "0xAB"),
    KeyToExa("VK_BROWSER_HOME", "0xAC"),
    KeyToExa("VK_VOLUME_MUTE", "0xAD"),
    KeyToExa("VK_VOLUME_DOWN", "0xAE"),
    KeyToExa("VK_VOLUME_UP", "0xAF"),
    KeyToExa("VK_MEDIA_NEXT_TRACK", "0xB0"),
    KeyToExa("VK_MEDIA_PREV_TRACK", "0xB1"),
    KeyToExa("VK_MEDIA_STOP", "0xB2"),
    KeyToExa("VK_MEDIA_PLAY_PAUSE", "0xB3"),
    KeyToExa("VK_LAUNCH_MAIL", "0xB4"),
    KeyToExa("VK_LAUNCH_MEDIA_SELECT", "0xB5"),
    KeyToExa("VK_LAUNCH_APP1", "0xB6"),
    KeyToExa("VK_LAUNCH_APP2", "0xB7"),
    KeyToExa("VK_OEM_1", "0xBA"),
    KeyToExa("VK_OEM_PLUS", "0xBB"),
    KeyToExa("VK_OEM_COMMA", "0xBC"),
    KeyToExa("VK_OEM_MINUS", "0xBD"),
    KeyToExa("VK_OEM_PERIOD", "0xBE"),
    KeyToExa("VK_OEM_2", "0xBF"),
    KeyToExa("VK_OEM_3", "0xC0"),
    KeyToExa("VK_OEM_4", "0xDB"),
    KeyToExa("VK_OEM_5", "0xDC"),
    KeyToExa("VK_OEM_6", "0xDD"),
    KeyToExa("VK_OEM_7", "0xDE"),
    KeyToExa("VK_OEM_8", "0xDF"),
    KeyToExa("VK_OEM_AX", "0xE1"),
    KeyToExa("VK_OEM_102", "0xE2"),
    KeyToExa("VK_ICO_HELP", "0xE3"),
    KeyToExa("VK_ICO_00", "0xE4"),
    KeyToExa("VK_PROCESSKEY", "0xE5"),
    KeyToExa("VK_ICO_CLEAR", "0xE6"),
    KeyToExa("VK_PACKET", "0xE7"),
    KeyToExa("VK_OEM_RESET", "0xE9"),
    KeyToExa("VK_OEM_JUMP", "0xEA"),
    KeyToExa("VK_OEM_PA1", "0xEB"),
    KeyToExa("VK_OEM_PA2", "0xEC"),
    KeyToExa("VK_OEM_PA3", "0xED"),
    KeyToExa("VK_OEM_WSCTRL", "0xEE"),
    KeyToExa("VK_OEM_CUSEL", "0xEF"),
    KeyToExa("VK_OEM_ATTN", "0xF0"),
    KeyToExa("VK_OEM_FINISH", "0xF1"),
    KeyToExa("VK_OEM_COPY", "0xF2"),
    KeyToExa("VK_OEM_AUTO", "0xF3"),
    KeyToExa("VK_OEM_ENLW", "0xF4"),
    KeyToExa("VK_OEM_BACKTAB", "0xF5"),
    KeyToExa("VK_ATTN", "0xF6"),
    KeyToExa("VK_CRSEL", "0xF7"),
    KeyToExa("VK_EXSEL", "0xF8"),
    KeyToExa("VK_EREOF", "0xF9"),
    KeyToExa("VK_PLAY", "0xFA"),
    KeyToExa("VK_ZOOM", "0xFB"),
    KeyToExa("VK_NONAME", "0xFC"),
    KeyToExa("VK_PA1", "0xFD"),
    KeyToExa("VK_OEM_CLEAR", "0xFE"),
    # Add more entries as needed
]

def get_focused_window_title():
    try:
        focused_window = gw.getWindows()[0]
        return focused_window.title
    except IndexError:
        return "No focused window found"

def display_process_info():
    while True:
        try:
            focused_process = psutil.Process(gw.getActiveWindow().pid)
            process_name = focused_process.name()
            
            print("=== Process Information ===")
            print(f"Process Name: {process_name}")
            print(f"Process ID: {focused_process.pid}")
            print(f"Memory Usage: {focused_process.memory_info().rss} bytes")
            print(f"CPU Usage: {focused_process.cpu_percent(interval=1)}%")
            print(f"Focused Window Title: {get_focused_window_title()}")
            
            # Find and display all other process IDs with the same process name
            same_name_processes = [p.info for p in psutil.process_iter(['pid', 'name']) if p.info['name'] == process_name]
            same_name_pids = [info['pid'] for info in same_name_processes if info['pid'] != focused_process.pid]
            
            if same_name_pids:
                print(f"\nOther Process IDs with the same name ({process_name}): {', '.join(map(str, same_name_pids))}")
            
            print("===========================")
            time.sleep(2)  # Adjust the sleep time as needed
        except psutil.NoSuchProcess:
            print("No such process found.")
            time.sleep(2)
        except psutil.AccessDenied:
            print("Access denied. Try running the script as administrator.")
            break
        except KeyboardInterrupt:
            print("Script terminated by user.")
            break

def find_key_in_array(search_string, key_to_exa_array):
    for key_to_exa in key_to_exa_array:
        if key_to_exa.is_equal_key(search_string) or key_to_exa.is_equal_exa_value(search_string):
            return True, key_to_exa
    return False, None

def display_key_value():
    # Accessing elements in the array
    for key_to_exa in key_to_exa_array:
        print(f"VK Key: {key_to_exa.m_vkKey}, Hex Value: {key_to_exa.m_exaValue}, Decimal Value: {key_to_exa.get_value_as_int()}")



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
            
def broadcast_key_press( keystroke):
    if  isinstance(keystroke, int):
            print(keystroke)
            wow_press(keystroke)
            
def broadcast_key_release( keystroke):
    if  isinstance(keystroke, int):
            print(keystroke)
            wow_release(keystroke)
            




def try_push_key(message, press, release):
    hasBeenFind, key= find_key_in_array(message,key_to_exa_array)
    if(hasBeenFind):
            try:            
                print(f"{key} broadcast {message}")
                if(press and release):
                    broadcast_key_click(key.get_value_as_int())
                elif(press ):
                    broadcast_key_press(key.get_value_as_int())
                elif(release):
                    broadcast_key_release(key.get_value_as_int())
            except ValueError:
                print(f"{key} is not a valid integer for {message}")

def get_windows_by_name(message):
    print("Not coded yet:"+message)
def get_windows_by_processesid(idSplitBySpace):
    print("Not coded yet:"+idSplitBySpace)


use_debug=False
def handle_message(message):

    global target_windows
    print(f"Received message: {message}")
    message=message.strip()
    
    
    if message.startswith("search:"):
        message = message[len("search:"):]
        if message.startswith("title:"):
            message = message[len("title:"):]
            if(use_debug):
                print(f"Reset target window to {message} by title")
            target_windows = get_windows_by_title(message)
    
        if message.startswith("name:"):
            message = message[len("name:"):]
            if(use_debug):
                print(f"Reset target window to {message} by name")
            target_windows = get_windows_by_name(message)

        if message.startswith("processid:"):
            message = message[len("processid:"):]
            if(use_debug):
                print(f"Reset target window to {message} by process id")
            target_windows = get_windows_by_name(message)
            
    elif message.startswith("check"):
        message = message[5:]
        display_process_info()

    elif message.startswith("press "):
        message = message[len("press "):]
        try_push_key(message, True, False)
    elif message.startswith("release "):
        message = message[len("release "):]
        try_push_key(message, False, True)
    elif message.startswith("click "):
        message = message[len("click "):]
        try_push_key(message, True, True)
       
    elif message.startswith("p "):
        message = message[2:]
        try_push_key(message, True, False)
    elif message.startswith("r "):
        message = message[2:]
        try_push_key(message, False, True)
    elif message.startswith("c "):
        message = message[2:]
        try_push_key(message, True, True)
                    

def udp_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    
    print(f"UDP server listening on port {port}")
    
    while True:
        data, address = server_socket.recvfrom(1024)
        message = data.decode('utf-8')
        handle_message(message)


if __name__ == "__main__":

    display_key_value()
    
    target_windows = get_windows_by_title(window_name)
    udp_thread = threading.Thread(target=udp_server, args=('0.0.0.0', listen_port), daemon=True)
    udp_thread.start()
    
    try:
        while True:
            time.sleep(10)
            pass
    except KeyboardInterrupt:
        print("Stopping UDP server...")

