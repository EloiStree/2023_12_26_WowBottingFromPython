import ctypes
import os


import socket
import pickle
import time


process_id = 0x00002410
addresses = {
    0x224A688B840: "Player_X",
    0x224A687E6A4: "Player_Y",
    0x224A687E69C: "Player_Z",
    0x224A91DA4DC: "XP",
}

use_visual_debug=False

coordinate_address=0x22583EF1D50

global_file_path = 'dd.txt'
SLEEP_DURATION = 0.1

port_to_use= 12345

# Your data
world = {'x': 0, 'y': 0, 'z': 0}
local = {'x': 0, 'y': 0, 'z': 0}
textcoordinate = 'Hello, Wow UDP!'

# Define the receiver's address (replace with the actual IP and port)
receiver_address = ('127.0.0.1', port_to_use)

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Hello and welcome post used: {port_to_use} :)")


class ProcessHandler:
    def __init__(self, process_id):
        self.process_id = process_id
        self.process_handle = None

    def open_process(self):
        self.process_handle = ctypes.windll.kernel32.OpenProcess(0x10, False, ctypes.c_ulonglong(self.process_id))
        if self.process_handle == 0:
            error_code = ctypes.windll.kernel32.GetLastError()
            if(use_visual_debug):
                print(f"Failed to open process. Error code: {error_code}")
            return False
        return True

    def close_process(self):
        try:
            if self.process_handle:
                ctypes.windll.kernel32.CloseHandle(self.process_handle)
        except Exception as e:
            if(use_visual_debug):
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
                if(use_visual_debug):
                    print(f"Read {label} value at address {hex(address)}: {self.values[label]}")
            else:
                error_code = ctypes.windll.kernel32.GetLastError()
                if(use_visual_debug):
                    print(f"Failed to read process memory at address {hex(address)}. Error code: {error_code}")


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
            if(use_visual_debug):
                print(f"Read string value at address {hex(self.address)}: {self.value}")
            
        else:
            if(use_visual_debug):
                print(f"Failed to read process memory at address {hex(self.address)}. Error code: {ctypes.windll.kernel32.GetLastError()}")


def extact_wow_map_info(text):
    try:
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
    except:
        return "","","0","0" 
        


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
    
    
    process_handler = ProcessHandler(process_id)
    memory_reader = MemoryReader(process_handler, addresses)
    string_reader = StringReader(process_handler, coordinate_address, 200)  # Adjust the address accordingly

    previous_xp_value = None

    while process_handler.open_process():
        memory_reader.read_memory()
        xp_value = int(memory_reader.values['XP'])

        
        string_reader.read_string()
        localisation =string_reader.value
        
        coordinates_wow = extact_wow_map_info(localisation) 
        if(use_visual_debug):
            print(", ".join(coordinates_wow))

        world['x']=float(memory_reader.values['Player_X'])
        world['y']=float(memory_reader.values['Player_Y'])
        world['z']=float(memory_reader.values['Player_Z'])
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
        isValueValide= not(world['x']==0 or world['y']==0 or world['z']==0)
        if(isValueValide):
            udp_socket.sendto(data_to_send.encode('utf-8'), receiver_address)
        

        # Print or log information (optional)
        if(use_visual_debug):
            print("Sent data:", data_to_send)
        if xp_value is not None and xp_value != previous_xp_value:
            # Append to the file only if XP value changes

            player_coordinates_line = f"{int(memory_reader.values['Player_X'])}|{int(memory_reader.values['Player_Y'])}|{int(memory_reader.values['Player_Z'])}|{localisation}"
            print("Appended:"+player_coordinates_line)
            append_line_to_file(player_coordinates_line)
            
            
            previous_xp_value = xp_value

        process_handler.close_process()
        time.sleep(SLEEP_DURATION)
    
    # Close the socket (this part will not be reached in this simple example)
    udp_socket.close()
