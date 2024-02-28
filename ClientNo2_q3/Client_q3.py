import socket
import threading
import pickle

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def send_message(self, message):
        """
        Sends a message to the server.
        """
        try:
            self.client_socket.sendall(message)
        except Exception as e:
            print("Error sending message:", e)

    def receive_messages(self):
        """
        Receives messages from the server.
        """
        while True:
            try:
                message = self.client_socket.recv(1024)
                if message:
                    # Check if the received message has a prefix indicating it was sent by the client
                    if message.startswith(b'[You] '):
                        print(message.decode())
                    else:
                        print("[Broadcast] " + message.decode())
            except Exception as e:
                print("Error receiving message:", e)
                break

    def start_chat(self):
        """
        Starts the chat with user input.
        """
        while True:
            try:
                message = input()
                serialized_message = pickle.dumps(message)
                self.send_message(serialized_message)
            except KeyboardInterrupt:
                print("Exiting chat...")
                break

if __name__ == "__main__":
    chat_client = ChatClient('localhost', 5000)
    chat_client.start_chat()