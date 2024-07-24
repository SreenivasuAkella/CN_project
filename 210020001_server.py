import socket
import threading
import pickle
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import cv2
import os

class Signal:
    def __init__(self):
        self.frame_received = None

class SecureChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients_sockets = {}
        self.clients_keys = {}
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print("Server is listening...")
        self.keys_lock = threading.Lock()
        self.sockets_lock = threading.Lock()
        self.video_stream_buffer = {}
        self.message_buffer = {}


    def handle_client_connection(self, client_socket, client_address):
        print(f"Connected with {client_address}")

        client_name = self.receive_data(client_socket).decode()
        print(f"{client_name} has connected.")
        client_public_key = RSA.import_key(self.receive_data(client_socket))
        with self.keys_lock:
            self.clients_keys[client_name] = client_public_key
        with self.sockets_lock:
            self.clients_sockets[client_socket] = client_address
        self.broadcast_keys_to_client()
        receive_thread = threading.Thread(target=self.receive_messages_from_client, args=(client_socket, client_name))
        receive_thread.start()

    def list_available_videos(self):
        video_files = [f for f in os.listdir() if f.endswith(".mp4")]
        return video_files

    def send_available_videos_to_client(self, client_socket):
        video_files = self.list_available_videos()
        self.send_data(client_socket, "2".encode().ljust(128) + pickle.dumps(video_files))

    def receive_messages_from_client(self, client_socket, client_name):
        is_streaming_video = False  # Flag to indicate video streaming
        while True:
            try:
                data = self.receive_data(client_socket)
                if not data:
                    break
                operation_type = data[:128].decode().strip()
                if operation_type == "1":
                    self.message_buffer[client_socket] = data
                    self.broadcast_message_to_clients(data)
                elif operation_type == "3":
                    self.video_stream_buffer[client_socket] = data
                    host_req = data[128:256].decode().strip()
                    vid_file = data[256:].decode().strip()
                    client_socket.send("3".encode().ljust(128))
                    is_streaming_video = True  # Set flag when video streaming starts
                    self.handle_video_streaming(client_socket, vid_file)
                    is_streaming_video = False  # Reset flag when video streaming ends
                elif operation_type == "4":
                    print(f"{client_name} has disconnected.")
                    client_socket.close()
                    del self.clients_keys[client_name]
                    self.broadcast_keys_to_client()
                    break
                elif operation_type == "2":
                    self.send_available_videos_to_client(client_socket)
            except Exception as e:
                print(f"Error: {e}")
                break


    def handle_video_streaming(self, client_socket, video_file):
        resolutions = {'240p': (1280, 720), '720p': (1280, 720), '1440p': (1280, 720)}
        total_frames_per_resolution = sum([int(cv2.VideoCapture(f"{os.path.splitext(video_file)[0]}_{resolution}.mp4").get(cv2.CAP_PROP_FRAME_COUNT)) // 3 for resolution in resolutions])

        current_frame = 0
        for resolution, dimensions in resolutions.items():
            filename = f"{os.path.splitext(video_file)[0]}_{resolution}.mp4"
            if os.path.exists(filename):
                print(f"File  found: {filename}")
                cap_resolution = cv2.VideoCapture(filename)
                frame_count_resolution = int(cap_resolution.get(cv2.CAP_PROP_FRAME_COUNT))

                frames_to_stream = min(frame_count_resolution // 3, total_frames_per_resolution)
                cap_resolution.set(cv2.CAP_PROP_POS_FRAMES, current_frame)

                for _ in range(frames_to_stream):
                    ret, frame = cap_resolution.read()
                    if not ret:
                        break

                    frame_resized = cv2.resize(frame, dimensions)
                    frame_data = cv2.imencode('.jpg', frame_resized)[1].tobytes()
                    client_socket.sendall((str(len(frame_data))).encode().ljust(16) + frame_data)

                current_frame += frames_to_stream
                cap_resolution.release()
            else:
                print(f"File not found: {filename}")

        client_socket.sendall('0'.encode().ljust(16))

    def broadcast_keys_to_client(self):
        with self.sockets_lock:
            for client_socket in self.clients_sockets:
                try:
                    client_name = self.get_client_name_from_socket(client_socket)
                    keys_data = {}
                    with self.keys_lock:
                        for name, key in self.clients_keys.items():
                            keys_data[name] = key.export_key()
                    keys_data = pickle.dumps(keys_data)
                    message_code = "0".encode().ljust(128)
                    self.send_data(client_socket, message_code + keys_data)
                    print("Updated client_keys dictionary:")
                    print(self.clients_keys)
                except Exception as e:
                    print(f"Error broadcasting message to {client_name}: {e}")

    def broadcast_message_to_clients(self, data):
        with self.sockets_lock:
            for client_socket in self.clients_sockets:
                try:
                    client_name = self.get_client_name_from_socket(client_socket)
                    self.send_data(client_socket, data)
                except Exception as e:
                    print(f"Error broadcasting message to {client_name}: {e}")

    def get_client_name_from_key(self, public_key):
        for name, key in self.clients_keys.items():
            if key == public_key:
                return name
        return None

    def get_client_name_from_socket(self, client_socket):
        for name, socket in self.clients_sockets.items():
            if socket == client_socket:
                return name
        return None

    def get_socket_from_client_name(self, client_name):
        for name, socket in self.clients_sockets.items():
            if name == client_name:
                return socket
        return None

    def receive_data(self, socket):
        data = b""
        while True:
            packet = socket.recv(4096)
            if not packet:
                break
            data += packet
            if len(packet) < 4096:
                break
        return data

    def send_data(self, socket, data):
        socket.sendall(data)

    def start_server(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.clients_sockets[client_socket] = client_address
            client_handler_thread = threading.Thread(target=self.handle_client_connection, args=(client_socket, client_address))
            client_handler_thread.start()

# Usage
host = 'localhost'
port = 6667
server = SecureChatServer(host, port)
server.start_server()
