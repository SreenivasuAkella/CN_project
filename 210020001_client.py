import socket
import pickle
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QCoreApplication
import os
import threading
import sys

class Signal(QObject):
    frame_received = pyqtSignal(np.ndarray)

class SecureChatClient(QObject):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.server_public_keys = {}
        self.rsa_key_pair = RSA.generate(2048)
        self.public_key = self.rsa_key_pair.publickey()
        self.private_key = self.rsa_key_pair
        self.signal = Signal()
        self.signal.frame_received.connect(self.display_frame)
        self.receive_thread = threading.Thread(target=self.receive_messages_from_server)
        self.receive_thread.start()
        self.is_streaming_video = False
        self.is_msg=False
    def send_data(self, data):
        self.client_socket.send(data)

    def encrypt_message_with_public_key(self, public_key, message):
        cipher = PKCS1_OAEP.new(public_key)
        ciphertext = cipher.encrypt(message)
        return ciphertext

    def decrypt_message_with_private_key(self, private_key, ciphertext):
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_message = cipher.decrypt(ciphertext)
        return decrypted_message

    def request_video_streaming(self, video_file):
        try:
            self.send_data("3".encode().ljust(128) + self.public_key.export_key() + video_file.encode())
        except Exception as e:
            print(f"Error requesting video streaming: {e}")

    def send_message(self, receiver_name, message):
        if receiver_name in self.server_public_keys:
            try:
                receiver_key = self.server_public_keys[receiver_name]
                sender_key = self.rsa_key_pair.publickey()
                encrypted_message = b""
                for i in range(0, len(message), 200):
                    chunk = message[i:i + 200]
                    encrypted_chunk = self.encrypt_message_with_public_key(RSA.import_key(receiver_key), chunk.encode())
                    encrypted_message += encrypted_chunk
                self.send_data("1".encode().ljust(128) + receiver_name.encode().ljust(256) + encrypted_message)
            except Exception as e:
                print(f"Error sending message: {e}")
        else:
            print("Receiver's name not found.")

    def send_name_and_public_key_to_server(self, name, public_key):
        self.send_data(name.encode())
        self.send_data(public_key.export_key())

    def receive_messages_from_server(self):
        keys_received = False
        try:
            while True:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                operation_type = data[:128].decode().strip()
                if operation_type == "0":
                    keys_data = data[128:].strip()
                    self.server_public_keys = pickle.loads(keys_data)
                    print("\n\nServer's Public Keys Received. Updated Client List:")
                    print(list(self.server_public_keys.keys()), self.server_public_keys)
                    print("\n")
                    keys_received = True
                elif operation_type == "1":
                    if not self.is_streaming_video:
                        if not keys_received:
                            print("\n\n***Public Keys Not Received Yet. Please Wait.***\n")
                            break
                        sender = data[128:384].decode()
                        message = data[384:]
                        try:
                            decrypted_message = self.decrypt_message_with_private_key(self.private_key, message)
                            print(f"\nMessage Received: {decrypted_message.decode()} \nFrom: {sender}\n")
                        except Exception as e:
                            print(f"Error decrypting message: {e}")
                        print("Enter operation number: ")
                elif operation_type == "3":
                    self.is_streaming_video = True
                    self.handle_video_streaming()
                    self.is_streaming_video = False
                elif operation_type == "2":
                    if not self.is_streaming_video:
                        print("hello")  # Request video list from server
                        video_list = pickle.loads(data[128:])
                        print("\nAvailable Videos:")
                        for i, video in enumerate(video_list, 1):
                            print(f"{i}. {video}")
                    else:
                        print("Skipping video list request as video streaming is in progress.")
                    print("Enter operation number: ")
        except Exception as e:
            print(f"Error : {e}")

    def handle_video_streaming(self):
        try:
            while True:
                if self.is_streaming_video:
                    frame_size_data = self.client_socket.recv(16)
                    if not frame_size_data:
                        break

                    frame_size_str = frame_size_data.strip().decode()
                    if not frame_size_str:
                        continue  # Skip processing if frame size is empty

                    frame_size = int(frame_size_str)
                    if frame_size == 0:
                        break

                    frame_data = b''.join(self.receive_frame_chunks(frame_size))
                    print("Received frame data. Decoding...,")
                    if self.is_msg:
                        frame_size_data = self.client_socket.recv(384)
                        if not frame_size_data:
                            break
                        frame_size_str = frame_size_data.strip().decode()
                        if not frame_size_str:
                            continue  # Skip processing if frame size is empty
                        frame_size = int(frame_size_str)
                        self.receive_frame_chunks(frame_size)
                    frame_np = np.frombuffer(frame_data, dtype=np.uint8)
                    frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)
                    if frame is not None:
                        print("Frame decoded successfully.")
                        self.signal.frame_received.emit(frame)
                    else:
                        continue
                else:
                    continue
        finally:
            cv2.destroyAllWindows()
            print("Enter operation number: ")



    def display_frame(self, frame):
        cv2.imshow('Video Stream', frame)
        cv2.waitKey(1)

    def receive_frame_chunks(self, frame_size):
        bytes_received = 0
        while bytes_received < frame_size:
            remaining_bytes = frame_size - bytes_received
            chunk_size = min(4096, remaining_bytes)
            chunk = self.client_socket.recv(chunk_size)
            if not chunk:
                break
            bytes_received += len(chunk)
            yield chunk

    def receive_video_list_from_server(self):
        try:
            data = self.client_socket.recv(4096)
            if data:
                operation_type = data[:128].decode().strip()
                if operation_type == "2":
                    video_list = pickle.loads(data[128:])
                    print("\nAvailable Videos:")
                    for i, video in enumerate(video_list, 1):
                        print(f"{i}. {video}")
        except Exception as e:
            print(f"Error receiving video list: {e}")

    def request_video_list_from_server(self):
        try:
            self.send_data("2".encode())
        except Exception as e:
            print(f"Error requesting video list: {e}")

    def start(self, name):
        # Start method
        self.send_name_and_public_key_to_server(name, self.public_key)
        print("\nOperations:")
        print("1. Send message")
        print("2. Videos list")
        print("3. Request video streaming")
        print("4. Quit connection")
        print("Enter operation number: ")

        while True:
            try:
                choice = input()
                if choice == "1":
                    self.is_msg=True

                    if not self.is_streaming_video:

                        print("Sending message...")
                        receiver_name = input("Enter receiver's name: ")
                        print("Sending message...")# Skip sending message if in video streaming mode
                        if receiver_name in self.server_public_keys:
                            message = input("Enter message: ")
                            receiver_key = self.server_public_keys[receiver_name]
                            sender_key = self.rsa_key_pair.publickey()
                            encrypted_message = b""
                            for i in range(0, len(message), 200):
                                chunk = message[i:i + 200]
                                encrypted_chunk = self.encrypt_message_with_public_key(RSA.import_key(receiver_key),
                                                                                         chunk.encode())
                                encrypted_message += encrypted_chunk
                            self.send_data(
                                "1".encode().ljust(128) + receiver_name.encode().ljust(256) + encrypted_message)
                        else:
                            print("Receiver's name not found.")

                    else:
                        print("Cannot send message while video streaming is active.somones msg made interupt reconnect")
                    self.is_msg=False
                    print("\nOperations:")
                    print("1. Send message")
                    print("2. Videos list")
                    print("3. Request video streaming")
                    print("4. Quit connection")
                    print("Enter operation number: ")

                elif choice == "3":
                    video_file = input("Enter video file to play: ")
                    available_resolutions = ['240p', '720p', '1440p']
                    selected_resolution = None
                    for resolution in available_resolutions:
                        filename = f"{video_file.split('.')[0]}_{resolution}.mp4"
                        print(filename)
                        if f"{video_file.split('.')[0]}_{resolution}.mp4" in os.listdir():
                            selected_resolution = resolution
                            break
                    if selected_resolution is None:
                        print("Video files with resolutions 240p, 720p, 1440p not found.")
                        continue
                    self.send_data("3".encode().ljust(128) + name.encode().ljust(128) + f"{video_file.split('.')[0]}.mp4".encode())
                    print(f"\n***Streaming now at {selected_resolution} resolution***\n")
                    print("\nOperations:")
                    print("1. Send message")
                    print("2. Videos list")
                    print("3. Request video streaming")
                    print("4. Quit connection")
                    print("Enter operation number: ")
                elif choice == "4":
                    self.send_data("4".encode())
                    print("Closing connection.")
                    break
                elif choice == "2":
                    self.request_video_list_from_server()
                else:
                    print("Invalid choice. Please enter a valid operation number.")
            except Exception as e:
                print("Error:", e)
                break
        self.client_socket.close()
        QCoreApplication.quit()
        sys.exit()

# Usage
host = 'localhost'
port = 6667
name = input("Enter your name: ")
print("generating public key")
app = QCoreApplication([])
client = SecureChatClient(host, port)
client.start(name)
app.exec_()
