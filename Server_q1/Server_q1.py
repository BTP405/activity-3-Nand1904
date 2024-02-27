import socket
import pickle
import os

def receive_file(conn, save_dir):
    """
    Function to receive a file from the client and save it to disk.

    Args:
        conn (socket): Connection socket object.
        save_dir (str): Directory where the received file will be saved.
    """
    try:
        # Open a file-like object for reading from the connection
        with conn, conn.makefile('rb') as clientfile:
            # Unpickle the file object sent by the client
            file_data = pickle.load(clientfile)
            # Extract filename and construct full path to save
            filename = os.path.join(save_dir, os.path.basename(file_data["filename"]))
            # Write the received data to a new file
            with open(filename, 'wb') as f:
                f.write(file_data["data"])
            print(f"File saved to: {filename}")
    except Exception as e:
        print("Error receiving file:", e)

def main():
    # Server configuration
    host = '127.0.0.1'
    port = 12345
    save_dir = "server_files"  # Directory to save received files
    
    # Ensure the directory exists, or create it if it doesn't
    os.makedirs(save_dir, exist_ok=True)
    
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))  # Bind the socket to the address and port
    server_socket.listen(1)  # Listen for incoming connections (1 connection queue)

    print("Server is listening...")

    # Accept a connection
    conn, addr = server_socket.accept()
    print("Connected to:", addr)

    # Receive and save the file
    receive_file(conn, save_dir)

    server_socket.close()  # Close the server socket

if __name__ == "__main__":
    main()