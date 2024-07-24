# CN_project
# Secure Chat Application
link of demo video-https://drive.google.com/file/d/1R6R_aO58b0LqljSEyPbyV20tECCqajqC/view?usp=sharing



This is a secure chat application implemented using Python. It allows clients to securely communicate with each other, request and stream videos, and disconnect from the server.
## Additional Imp Notes
- If there is empty without printed with (enter operation number) ,consider it as asking for operation 1-4.enter operation it will work properly.
- for input for video streming use 1.mp4,2.mp4 type.
- if you have error like already useage of port change port number in code.
-videos should be in same folder where .py placed
-name videos as <videoname>_<resolutions>.mp4,<videoname>_<resolution>.mp4 e.t.c
-if server used error occurs change port number.
## Program Structure

The application consists of two main components:

1. **Server**:
    - `secure_chat_server.py`: This file contains the implementation of the server. It handles incoming client connections, manages client information, facilitates secure communication through RSA encryption, and streams videos upon client requests.

2. **Client**:
    - `secure_chat_client.py`: This file contains the implementation of the client. It connects to the server, sends and receives encrypted messages, requests video streaming, and displays the streamed videos.

## Dependencies

The application relies on several Python libraries for its functionality:

- `socket`: Used for establishing network communication between the server and clients.
- `threading`: Utilized for handling multiple client connections concurrently.
- `pickle`: Utilized for serializing and deserializing Python objects.
- `Crypto`: Provides cryptographic functions such as RSA encryption and decryption for secure communication.
- `cv2` (OpenCV): Utilized for video streaming functionalities.
- `PyQt5`: Used for building the client-side graphical user interface.
- `os`: Used for file operations, such as listing available videos on the server.

## Demo Instructions

To run the secure chat application, follow these steps:

1. **Server Setup**:
    - Run `secure_chat_server.py` on a host machine accessible to clients.
    - Provide the desired host and port information for the server to listen on.

2. **Client Setup**:
    - Run `secure_chat_client.py` on client machines intending to connect to the server.
    - Upon execution, enter a unique username when prompted to identify the client.
    - Use the provided menu options to interact with the server, including sending messages, requesting video streaming, and listing available videos.

  3. **Usage**:
    - **Sending Messages**: Enter `1` from the client menu, provide the recipient's username, and type the desired message to send encrypted messages to other clients.
    - **Requesting Video Streaming**: Enter `3` from the client menu, provide the name of the video file to stream, and select the desired resolution if available.
    - **Listing Available Videos**: Enter `2` from the client menu to view a list of videos available on the server.
    - **Disconnecting from the Server**: Enter `4` from the client menu to gracefully disconnect from the server and exit the application.
    1. **Sending Messages**:
       - Enter `1` from the client menu.
       - Provide the recipient's username and type the desired message to send encrypted messages to other clients.

    2. **Listing Available Videos**:
       - Enter `2` from the client menu to view a list of videos available on the server.

    3. **Requesting Video Streaming**:
       - Enter `3` from the client menu.
       - Provide the name of the video file to stream.
       - Select the desired resolution if available.

    4. **Disconnecting from the Server**:
       - Enter `4` from the client menu to gracefully disconnect from the server and exit the application.

    #### Further Information:

    - **Sending Messages**:
      - The client encrypts the message with the recipient's public key and sends it to the server, which then broadcasts the encrypted message to all clients.

    - **Listing Available Videos**:
      - The client requests the server to list available videos.
      - The server responds with a list of available video files, which the client can view.

    - **Requesting Video Streaming**:
      - The client requests the server to stream a video file.
      - If the requested video file is available in multiple resolutions, the client selects the desired resolution.
      - The server streams the video frames to the client, ensuring proportional sourcing from available resolutions.

    - **Disconnecting from the Server**:
      - The client sends a disconnect signal to the server, closes the connection, and exits the application.

## Additional Notes

- Ensure that all necessary dependencies are installed before running the application.
- Verify that both the server and client scripts are executed in compatible environments to enable communication.
- Clients must be connected to the same network as the server to establish communication.
- The application provides a secure communication channel through RSA encryption, ensuring confidentiality and integrity of exchanged messages.
## Additional Imp Notes
- If there is empty without printed with enter operation number consider it as asking for operation 1-4.enter operation it will work properly.
## Server Features

### Client Connection Management

- **Server Socket Setup**:
  - Implemented a server socket to receive client connection requests.
  - Upon connection, the server prompts the client to provide its name and generated public key.

- **Dictionary Management**:
  - Maintains a dictionary to store each client's name and its associated public key.
  - Stores the client’s name and public key as the value in the dictionary.

- **Broadcasting Client Information**:
  - When a new client connects, the server broadcasts the client's name and public key from the dictionary to all connected clients.

- **Client Disconnection Handling**:
  - If a client wishes to disconnect, it sends a "QUIT" message to the server.
  - The server removes the client's entry from the dictionary and notifies all connected clients.

### Secure Communication Management

- **Message Encryption**:
  - Clients use the public key of another client to encrypt their messages.
  - The server broadcasts the encrypted message (cipher text) to all clients.

- **Broadcasting Cipher Text**:
  - Broadcasting cipher text ensures that only the intended recipient, possessing the corresponding private key, can decrypt the message.

### Video Streaming Management

- **Video Resolution Management**:
  - The server maintains a directory containing multiple resolutions for each video file.

- **Proportional Frame Streaming**:
  - Upon receiving a client's request, the server streams the video by sourcing frames proportionately in sequence from each available resolution video file.
  - For example, frames are distributed equally among different resolutions, providing a balanced viewing experience.

## Client Features

### Connection Establishment

- **Socket Creation and Connection**:
  - Clients create a socket and connect to the server.
  - Upon connection, clients send their name and generated public key to the server.

### Secure Communication

- **Dictionary Maintenance**:
  - Clients maintain a dictionary at their end, which gets updated whenever the server broadcasts the dictionary.
  - Clients fetch the public key of another client from the saved dictionary for secret communication.

- **Message Decryption**:
  - Clients decrypt and display the received cipher text using their private key.

### Video Playback

- **Listing Available Videos**:
  - Clients request the server to list available videos.
  - Clients start playing a video file by providing its name from the available video file list displayed by the server.ill work properly.
- for input for video streming use 1.mp4,2.mp4 type.
- if you have error like already useage of port change port number in code.
## Program Structure

The application consists of two main components:

1. **Server**:
    - `secure_chat_server.py`: This file contains the implementation of the server. It handles incoming client connections, manages client information, facilitates secure communication through RSA encryption, and streams videos upon client requests.

2. **Client**:
    - `secure_chat_client.py`: This file contains the implementation of the client. It connects to the server, sends and receives encrypted messages, requests video streaming, and displays the streamed videos.

## Dependencies

The application relies on several Python libraries for its functionality:

- `socket`: Used for establishing network communication between the server and clients.
- `threading`: Utilized for handling multiple client connections concurrently.
- `pickle`: Utilized for serializing and deserializing Python objects.
- `Crypto`: Provides cryptographic functions such as RSA encryption and decryption for secure communication.
- `cv2` (OpenCV): Utilized for video streaming functionalities.
- `PyQt5`: Used for building the client-side graphical user interface.
- `os`: Used for file operations, such as listing available videos on the server.

## Demo Instructions

To run the secure chat application, follow these steps:

1. **Server Setup**:
    - Run `secure_chat_server.py` on a host machine accessible to clients.
    - Provide the desired host and port information for the server to listen on.

2. **Client Setup**:
    - Run `secure_chat_client.py` on client machines intending to connect to the server.
    - Upon execution, enter a unique username when prompted to identify the client.
    - Use the provided menu options to interact with the server, including sending messages, requesting video streaming, and listing available videos.

  3. **Usage**:
    - **Sending Messages**: Enter `1` from the client menu, provide the recipient's username, and type the desired message to send encrypted messages to other clients.
    - **Requesting Video Streaming**: Enter `3` from the client menu, provide the name of the video file to stream, and select the desired resolution if available.
    - **Listing Available Videos**: Enter `2` from the client menu to view a list of videos available on the server.
    - **Disconnecting from the Server**: Enter `4` from the client menu to gracefully disconnect from the server and exit the application.
    1. **Sending Messages**:
       - Enter `1` from the client menu.
       - Provide the recipient's username and type the desired message to send encrypted messages to other clients.

    2. **Listing Available Videos**:
       - Enter `2` from the client menu to view a list of videos available on the server.

    3. **Requesting Video Streaming**:
       - Enter `3` from the client menu.
       - Provide the name of the video file to stream.
       - Select the desired resolution if available.

    4. **Disconnecting from the Server**:
       - Enter `4` from the client menu to gracefully disconnect from the server and exit the application.

    #### Further Information:

    - **Sending Messages**:
      - The client encrypts the message with the recipient's public key and sends it to the server, which then broadcasts the encrypted message to all clients.

    - **Listing Available Videos**:
      - The client requests the server to list available videos.
      - The server responds with a list of available video files, which the client can view.

    - **Requesting Video Streaming**:
      - The client requests the server to stream a video file.
      - If the requested video file is available in multiple resolutions, the client selects the desired resolution.
      - The server streams the video frames to the client, ensuring proportional sourcing from available resolutions.

    - **Disconnecting from the Server**:
      - The client sends a disconnect signal to the server, closes the connection, and exits the application.

## Additional Notes

- Ensure that all necessary dependencies are installed before running the application.
- Verify that both the server and client scripts are executed in compatible environments to enable communication.
- Clients must be connected to the same network as the server to establish communication.
- The application provides a secure communication channel through RSA encryption, ensuring confidentiality and integrity of exchanged messages.
## Additional Imp Notes
- If there is empty without printed with enter operation number consider it as asking for operation 1-4.enter operation it will work properly.
## Server Features

### Client Connection Management

- **Server Socket Setup**:
  - Implemented a server socket to receive client connection requests.
  - Upon connection, the server prompts the client to provide its name and generated public key.

- **Dictionary Management**:
  - Maintains a dictionary to store each client's name and its associated public key.
  - Stores the client’s name and public key as the value in the dictionary.

- **Broadcasting Client Information**:
  - When a new client connects, the server broadcasts the client's name and public key from the dictionary to all connected clients.

- **Client Disconnection Handling**:
  - If a client wishes to disconnect, it sends a "QUIT" message to the server.
  - The server removes the client's entry from the dictionary and notifies all connected clients.

### Secure Communication Management

- **Message Encryption**:
  - Clients use the public key of another client to encrypt their messages.
  - The server broadcasts the encrypted message (cipher text) to all clients.

- **Broadcasting Cipher Text**:
  - Broadcasting cipher text ensures that only the intended recipient, possessing the corresponding private key, can decrypt the message.

### Video Streaming Management

- **Video Resolution Management**:
  - The server maintains a directory containing multiple resolutions for each video file.

- **Proportional Frame Streaming**:
  - Upon receiving a client's request, the server streams the video by sourcing frames proportionately in sequence from each available resolution video file.
  - For example, frames are distributed equally among different resolutions, providing a balanced viewing experience.

## Client Features

### Connection Establishment

- **Socket Creation and Connection**:
  - Clients create a socket and connect to the server.
  - Upon connection, clients send their name and generated public key to the server.

### Secure Communication

- **Dictionary Maintenance**:
  - Clients maintain a dictionary at their end, which gets updated whenever the server broadcasts the dictionary.
  - Clients fetch the public key of another client from the saved dictionary for secret communication.

- **Message Decryption**:
  - Clients decrypt and display the received cipher text using their private key.

### Video Playback

- **Listing Available Videos**:
  - Clients request the server to list available videos.
  - Clients start playing a video file by providing its name from the available video file list displayed by the server.
