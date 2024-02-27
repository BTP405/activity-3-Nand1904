import socket
import pickle

def send_file(file_path):
    """
    Function to read a file from disk and pickle it.

    Args:
        file_path (str): Path to the file to be sent.

    Returns:
        bytes: Pickled file object.
    """
    try:
        # Read the file data
        with open(file_path, 'rb') as f:
            # Create a dictionary containing filename and file data
            file_data = {"filename": file_path, "data": f.read()}
            # Pickle the dictionary
            return pickle.dumps(file_data)
    except Exception as e:
        print("Error sending file:", e)

def main():
    # Server configuration
    host = '127.0.0.1'
    port = 12345
    
    # Get the file path from user input
    file_path = input("Enter the file path: ")

    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    client_socket.connect((host, port))

    # Get pickled file data
    file_data = send_file(file_path)
    if file_data:
        try:
            # Send the file data to the server
            client_socket.sendall(file_data)
            print("File sent successfully")
        except Exception as e:
            print("Error sending file:", e)

    client_socket.close()  # Close the client socket

if __name__ == "__main__":
    main()