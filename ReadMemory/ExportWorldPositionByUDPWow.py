import ctypes
import os


import socket
import pickle
import time

global_file_path = 'example.txt'
SLEEP_DURATION = 4


# Your data
world = {'x': 1, 'y': 2, 'z': 3}
local = {'x': 4, 'y': 5, 'z': 6}
textcoordinate = 'Hello, UDP!'

# Define the receiver's address (replace with the actual IP and port)
receiver_address = ('127.0.0.1', 12345)

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class ProcessHandler:
    def __init__(self, process_id):
        self.process_id = process_id
        self.process_handle = None

    def open_process(self):
        self.process_handle = ctypes.windll.kernel32.OpenProcess(0x10, False, ctypes.c_ulonglong(self.process_id))
        if self.process_handle == 0:
            error_code = ctypes.windll.kernel32.GetLastError()
            print(f"Failed to open process. Error code: {error_code}")
            return False
        return True

    def close_process(self):
        try:
            if self.process_handle:
                ctypes.windll.kernel32.CloseHandle(self.process_handle)
        except Exception as e:
            print(f"Error closing process handle: {e}")

class MemoryReader:
    def __init__(self, process_handler, addresses):
        self.process_handler = process_handler
        self.addresses = addresses
        self.values = {}

    def read_memory(self):
        for address, label in self.addresses.items():
            buffer = ctypes.c_float()
            bytes_read = ctypes.c_ulong(0)
            if ctypes.windll.kernel32.ReadProcessMemory(self.process_handler.process_handle, ctypes.c_void_p(address), ctypes.byref(buffer), ctypes.sizeof(buffer), ctypes.byref(bytes_read)):
                self.values[label] = buffer.value
                print(f"Read {label} value at address {hex(address)}: {self.values[label]}")
            else:
                error_code = ctypes.windll.kernel32.GetLastError()
                print(f"Failed to read process memory at address {hex(address)}. Error code: {error_code}")

    def read_xp_value(self):
        xp_address = 0x20FF45AA29C
        buffer = ctypes.c_float()
        bytes_read = ctypes.c_ulong(0)
        if ctypes.windll.kernel32.ReadProcessMemory(self.process_handler.process_handle, ctypes.c_void_p(xp_address), ctypes.byref(buffer), ctypes.sizeof(buffer), ctypes.byref(bytes_read)):
            xp_value = buffer.value
            print(f"Read XP value at address {hex(xp_address)}: {xp_value}")
            return xp_value
        else:
            error_code = ctypes.windll.kernel32.GetLastError()
            print(f"Failed to read XP value. Error code: {error_code}")
            return None

class StringReader:
    def __init__(self, process_handler, address, max_length):
        self.process_handler = process_handler
        self.address = address
        self.max_length = max_length
        self.value = None

    def read_string(self):
        buffer = ctypes.create_string_buffer(self.max_length)
        bytes_read = ctypes.c_ulong(0)
        if ctypes.windll.kernel32.ReadProcessMemory(self.process_handler.process_handle, ctypes.c_void_p(self.address), buffer, self.max_length, ctypes.byref(bytes_read)):
            self.value = buffer.value.decode("utf-8")
            print(f"Read string value at address {hex(self.address)}: {self.value}")
            
        else:
            print(f"Failed to read process memory at address {hex(self.address)}. Error code: {ctypes.windll.kernel32.GetLastError()}")


def extact_wow_map_info(text):
    split_text_num= text.split(":")
    split_world_local = split_text_num[0].split("-")
    split_x_y = split_text_num[1].split(",")
    world = split_world_local[0].strip()
    local=""
    if len(split_world_local)>1:
        local= split_world_local[1].strip()
    x = (split_x_y[0]).strip()
    y = (split_x_y[1]).strip()
    return world, local, x , y  
    


def append_line_to_file(line):
    try:
        if not os.path.exists(global_file_path):
            with open(global_file_path, 'w'):
                pass

        with open(global_file_path, 'a') as file:
            file.write(line + '\n')
        print(f"Line '{line}' appended to {global_file_path} successfully.")
    except Exception as e:
        print(f"Error appending line to {global_file_path}: {e}")

if __name__ == "__main__":
    process_id = 0x00004320
    addresses = {
        0x45121FBBE4: "Player_X",
        0x20F26775CA0: "Player_Y",
        0x20F26305380: "Player_Z",
        0x20FF45AA29C: "XP",
    }
    
    process_handler = ProcessHandler(process_id)
    memory_reader = MemoryReader(process_handler, addresses)
    string_reader = StringReader(process_handler, 0x2101F8D3520, 200)  # Adjust the address accordingly

    previous_xp_value = None

    while process_handler.open_process():
        memory_reader.read_memory()
        xp_value = memory_reader.read_xp_value()

        
        string_reader.read_string()
        localisation =string_reader.value
        
        coordinates_wow = extact_wow_map_info(localisation) 
        print(", ".join(coordinates_wow))

        world['x']=int(memory_reader.values['Player_X'])
        world['y']=int(memory_reader.values['Player_Y'])
        world['z']=int(memory_reader.values['Player_Z'])
        local['x']=float(coordinates_wow[2])
        local['y']=float(coordinates_wow[3])
        local['z']=world['z']
        textcoordinate= localisation
        
        # Pack your data into a single string
        data_to_send = f"{world['x']},{world['y']},{world['z']};" \
                       f"{local['x']},{local['y']},{local['z']};" \
                       f"{coordinates_wow[0]},{coordinates_wow[1]};" \
                       f"{textcoordinate}"

        # Send the data as UTF-8
        udp_socket.sendto(data_to_send.encode('utf-8'), receiver_address)

        # Print or log information (optional)
        print("Sent data:", data_to_send)
        if xp_value is not None and xp_value != previous_xp_value:
            # Append to the file only if XP value changes

            player_coordinates_line = f"{int(memory_reader.values['Player_X'])}|{int(memory_reader.values['Player_Y'])}|{int(memory_reader.values['Player_Z'])}|{localisation}"
            append_line_to_file(player_coordinates_line)
            
            
            previous_xp_value = xp_value

        process_handler.close_process()
        time.sleep(SLEEP_DURATION)
    
    # Close the socket (this part will not be reached in this simple example)
    udp_socket.close()
