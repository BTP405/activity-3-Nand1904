import socket
import threading
import pickle

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []  # List to store connected clients
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))

    def broadcast_message(self, message, sender):
        """
        Broadcasts a message to all connected clients except the sender.
        """
        for client_socket in self.clients:
            if client_socket != sender:
                try:
                    client_socket.sendall(message)
                except:
                    # Remove disconnected client from the list
                    self.clients.remove(client_socket)

    def handle_client(self, client_socket):
        """
        Handles messages from a single client.
        """
        while True:
            try:
                message = client_socket.recv(1024)
                if message:
                    self.broadcast_message(message, client_socket)
            except:
                # Client disconnected
                self.clients.remove(client_socket)
                client_socket.close()
                break

    def start(self):
        """
        Starts the chat server and listens for incoming connections.
        """
        self.server_socket.listen(5)
        print("Server is listening on {}:{}".format(self.host, self.port))
        while True:
            client_socket, client_address = self.server_socket.accept()
            print("New connection from:", client_address)
            self.clients.append(client_socket)
            # Start a new thread to handle the client
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

if __name__ == "__main__":
    chat_server = ChatServer('localhost', 5000)
    chat_server.start()