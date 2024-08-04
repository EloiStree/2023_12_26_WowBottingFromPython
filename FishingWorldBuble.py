import time
import pyautogui
import win32gui
import win32con
import ctypes
import socket
import threading

from datetime import datetime
import time
from datetime import datetime, timedelta

class CooldownManager:
    def __init__(self, cooldown_seconds):
        self.cooldown_seconds = cooldown_seconds
        self.last_action_time = None

    def record_action(self):
        self.last_action_time = datetime.now()

    def is_cooldown_passed(self):
        if self.last_action_time is None:
            # No action recorded yet, cooldown is considered passed
            return True

        current_time = datetime.now()
        elapsed_time = current_time - self.last_action_time

        return elapsed_time.total_seconds() >= self.cooldown_seconds

# Example usage:
cooldown_manager = CooldownManager(cooldown_seconds=60)  # Set cooldown time to 60 seconds

# Perform an action and record the time
cooldown_manager.record_action()

# Check if cooldown has passed
if cooldown_manager.is_cooldown_passed():
    print("Cooldown has passed. You can perform the action.")
else:
    print("Cooldown is still active. Please wait.")


class WaitToBeExecuted:
    def __init__(self, seconds_to_wait,action):
        self._set_current_timestamp()
        self.seconds_to_wait = seconds_to_wait
        self.action = action  # The function to be triggered

    def trigger_action(self):
        if self.action:
            self.action()
        else:
            print("No action specified for execution.")
            
    def _set_current_timestamp(self):
        self.timestamp = datetime.now()

    def get_timestamp(self):
        return self.timestamp

    def seconds_since(self, other_date):
        time_difference = other_date - self.timestamp
        return time_difference.total_seconds()

    def seconds_since_current(self):
        current_date = datetime.now()
        return self.seconds_since(current_date)

    def is_time_over(self):
        seconds_since_current = self.seconds_since_current()
        return seconds_since_current > self.seconds_to_wait

    def wait_for_seconds(self):
        time.sleep(self.seconds_to_wait)

class WaitList:
    def __init__(self):
        self.wait_list = []

    def add_to_wait_list(self, wait_instance):
        if isinstance(wait_instance, WaitToBeExecuted):
            self.wait_list.append(wait_instance)
        else:
            raise ValueError("Only instances of WaitToBeExecuted can be added to the wait list")

    def check_and_dequeue(self):
        ready_to_execute = [item for item in self.wait_list if item.is_time_over()]

        for item in ready_to_execute:
            print(f"Executing item: {item}")
            self.wait_list.remove(item)

wait_list = WaitList()


WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101

VK_SPACE = 0x20    # Space
VK_TAB = 0x09      # Tab
KEY_NumpadPlus = 0x6B
KEY_NumpadMinus = 0x6D
KEY_NumpadDivide = 0x6F
KEY_NumpadMultiply = 0x6A
KEY_NumpadDecimal = 0x6E
VK_ENTER = 0x0D    # Enter
VK_ESCAPE = 0x1B   # Escape

listen_port = 2509

wowWindowTitle= "World of Warcraft"
target_windows=[]
wowwindowbyhand=[461806,264698,5178416,2425914]
wowwindowbyhand=[CooldownManager(5),CooldownManager(5),CooldownManager(5),CooldownManager(5)]
qDSQZ
#  /cry




# This methode press a target window with and int unique id
def press_key_hwnd(hwnd, key):
    ctypes.windll.user32.PostMessageW(hwnd, WM_KEYDOWN, key, 0)
                                      
# This methode release a target window with and int unique id, 0)
def release_key_hwnd(hwnd, key):
    ctypes.windll.user32.PostMessageW(hwnd, WM_KEYUP, key, 0)

# This methode press a target window with and int unique id
def click_key_hwnd(hwnd, key):
    ctypes.windll.user32.PostMessageW(hwnd, WM_KEYDOWN, key, 0)
    ctypes.windll.user32.PostMessageW(hwnd, WM_KEYUP, key, 0)
                                      

def interact(hwnd):
    click_key_hwnd(hwnd,KEY_NumpadMinus )
    
def interact_index(index):

    print(f"Do {index})") 
    if len(wowwindowbyhand)>index:
        click_key_hwnd(wowwindowbyhand[index],KEY_NumpadMinus )

        
def interact_index_delay(index):
    interact_index(index)
    wait_list.add_to_wait_list(WaitToBeExecuted(2, lambda:interact_index(index) ))
    
    
def jump(hwnd):
    click_key_hwnd(hwnd,VK_SPACE )

def debugbooltohwnd(a,b):
    print(">"+ str(a)+" "+str(b))
    
def jumpdebug(text,index):
    print("Do something "+str(index))

    if(len(wowwindowbyhand)>index):
        debugbooltohwnd(text, wowwindowbyhand[index])
        jump(wowwindowbyhand[index])
    
    

# This methode will fetch all the window with the given title
def get_windows_by_title(title):
    windows = []
    win32gui.EnumWindows(lambda hwnd, _: windows.append((hwnd, win32gui.GetWindowText(hwnd))), None)
    return [hwnd for hwnd, window_title in windows if title.lower() in window_title.lower()]

jumpdebugmode=False
def handle(text):

     #print(text)
    if(text.lower().strip()=="b:1:wowaudio0"):
        if jumpdebugmode:
            jumpdebug("wowaudio0", 0)
        else:
            interact_index(0)
    if(text.lower().strip()=="b:1:wowaudio1"):  
        if jumpdebugmode:
            jumpdebug("wowaudio1", 1)
        else:
            interact_index(1)
    if(text.lower().strip()=="b:1:wowaudio2"):    
        if jumpdebugmode:
            jumpdebug("wowaudio2", 2)
        else:
            interact_index(2)
    if(text.lower().strip()=="b:1:wowaudio3"):    
        #
        if jumpdebugmode:
            jumpdebug("wowaudio3",3)
        else:
            interact_index(3)
    

def udp_server(host, port):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to a specific address and port
    server_socket.bind((host, port))
    
    print(f"UDP server listening on port {port}")
    
    while True:
        # Receive data from the socket
        data, address = server_socket.recvfrom(1024)
        #print(data )
        print(len(data) )
        # Decode the received data
        message = data.decode('utf-8')
        
        print(message)
        # Perform an action based on the received message
        handle(message)

if __name__ == "__main__":
    target_windows = get_windows_by_title(wowWindowTitle)
    for item in target_windows:
        print(item)
        jump(item)
        time.sleep(2)
    udp_thread = threading.Thread(target=udp_server, args=('127.0.0.1', listen_port), daemon=True)
    udp_thread.start()


