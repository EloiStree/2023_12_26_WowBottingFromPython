import socket

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific address and port
receiver_address = ('127.0.0.1', 12345)
udp_socket.bind(receiver_address)

print("Hello")

while True:
    # Receive data from the sender
    data, sender_address = udp_socket.recvfrom(1024)

    # Decode the received data as UTF-8
    received_data = data.decode('utf-8')

    # Split the received string into individual values
    world_str, local_str,name_str, textcoordinate = received_data.split(';')
    world_values = [float(value) for value in world_str.split(',')]
    local_values = [float(value) for value in local_str.split(',')]
    local_names = [str(value) for value in name_str.split(',')]

    # Print or process the received data
    print("Received data:")
    print("World:", dict(zip(['x', 'y', 'z'], world_values)))
    print("Local:", dict(zip(['x', 'y', 'z'], local_values)))
    print("Name Locality:", dict(zip(['world_name', 'local_name'], local_names)))
    print("Text Coordinate:", textcoordinate)

# Close the socket (this part will not be reached in this simple example)
udp_socket.close()
