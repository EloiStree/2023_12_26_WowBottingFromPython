import ctypes
import time

class ProcessHandler:
    def __init__(self, process_id):
        self.process_id = process_id
        self.process_handle = None

    def open_process(self):
        self.process_handle = ctypes.windll.kernel32.OpenProcess(0x10, False, ctypes.c_ulonglong(self.process_id))
        if self.process_handle == 0:
            print(f"Failed to open process. Error code: {ctypes.windll.kernel32.GetLastError()}")
            return False
        return True

    def close_process(self):
        if self.process_handle:
            ctypes.windll.kernel32.CloseHandle(self.process_handle)

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
                print(f"Failed to read process memory at address {hex(address)}. Error code: {ctypes.windll.kernel32.GetLastError()}")

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

    while process_handler.open_process():
        memory_reader.read_memory()
        string_reader.read_string()
        process_handler.close_process()
        time.sleep(1)
