import ctypes
import os


import socket
import pickle
import time


use_visual_debug=True
process_id = 0x000046AC
text_picking_address=0x12C1816FEC0

SLEEP_DURATION = 0.1

port_to_use= 12345

textcoordinate = 'Hello, Wow UDP Text Picking!'

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
            #if(use_visual_debug):
            #   print(f"Read string value at address {hex(self.address)}: {self.value}")
            
        else:
            if(use_visual_debug):
                print(f"Failed to read process memory at address {hex(self.address)}. Error code: {ctypes.windll.kernel32.GetLastError()}")



def truncate_string(text, max_length):
    return text[:max_length]


if __name__ == "__main__":
    
    
    process_handler = ProcessHandler(process_id)
    string_reader = StringReader(process_handler, text_picking_address, 1000)  
 

    while process_handler.open_process():
       
        string_reader.read_string()
        text =string_reader.value
        
        if(use_visual_debug):
            print(truncate_string(text, 100).replace("\n", "\t"))


        isValueValide=False
        if(isValueValide):
            udp_socket.sendto(text.encode('utf-8'), receiver_address)

        process_handler.close_process()
        time.sleep(SLEEP_DURATION)
    
    udp_socket.close()
