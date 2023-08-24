import socket

# Set up the server address and port
UDP_IP = "0.0.0.0"
UDP_PORT1 = 8881
UDP_PORT2 = 8882

# Create a UDP socket
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock1.bind((UDP_IP, UDP_PORT1))
sock2.bind((UDP_IP, UDP_PORT2))

sock1.setblocking(0)
sock2.setblocking(0)

print("Waiting for data...")

while True:
    # Receive data from the Arduino
    try:
        data, addr = sock1.recvfrom(1024)
        print("Received message 1:", data.decode())
    except: pass
    try:
        data, addr = sock2.recvfrom(1024)
        print("Received message 2:", data.decode())
    except: pass