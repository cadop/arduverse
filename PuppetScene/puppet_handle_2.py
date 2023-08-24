from omni.kit.scripting import BehaviorScript
import socket
import numpy as np
import math
from pxr import  Gf
import numpy as np
import math 

class Puppet2(BehaviorScript):
    def on_init(self):
        print(f"{__class__.__name__}.on_init()->{self.prim_path}")

        # Set up the server address and port
        UDP_IP = "0.0.0.0"
        UDP_PORT = 8882

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))
        self.sock.setblocking(0)

        print("Waiting for data...")

    def on_destroy(self):
        print(f"{__class__.__name__}.on_destroy()->{self.prim_path}")
        self.sock = None
        rot = [0, 0, 0]
        self.prim.GetAttribute('xformOp:rotateXYZ').Set(Gf.Vec3d(rot))

    def on_play(self): 
        print(f"{__class__.__name__}.on_play()->{self.prim_path}")
        # Set up the server address and port
        UDP_IP = "0.0.0.0"
        UDP_PORT = 8882

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))
        self.sock.setblocking(0)

        # Time interval between sensor readings in seconds
        self.dt = 0.02

    def on_pause(self):
        print(f"{__class__.__name__}.on_pause()->{self.prim_path}")

    def on_stop(self):
        print(f"{__class__.__name__}.on_stop()->{self.prim_path}")
        self.on_destroy()

    def on_update(self, current_time: float, delta_time: float):
        self.get_data()

    def get_data(self):
        # # Receive data from the Arduino
        data = self.clear_socket_buffer()
        if data is None: return 
        # Decode the data and split it into Pitch and Roll
        data = data.decode()
        device, pitch, roll, yaw = data.split(",")

        x,y,z = float(roll), float(yaw), 180-float(pitch)
        rot = [x, y, z]
        self.prim.GetAttribute('xformOp:rotateXYZ').Set(Gf.Vec3d(rot))

    def clear_socket_buffer(self):
        # Function to clear the socket's buffer
        latest_data = None
        while True:
            try:
                # Try to read data from the socket in a non-blocking way
                latest_data, addr = self.sock.recvfrom(1024)
            except BlockingIOError:
                # No more data to read (buffer is empty)
                return latest_data