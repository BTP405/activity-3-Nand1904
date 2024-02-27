# Import the necessary modules for socket communication and serialization
import socket
import pickle

# Define a class named TaskClient for sending tasks to the server
class TaskClient:
    # Constructor to initialize the server address
    def __init__(self, server_address):
        self.server_address = server_address

    # Method to send a task to the server and receive the result
    def send_task(self, task_data):
        try:
            # Create a TCP/IP socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Connect to the server
                s.connect(self.server_address)
                # Serialize the task data and send it to the server
                serialized_task_data = pickle.dumps(task_data)
                s.sendall(serialized_task_data)
                # Receive the result from the server
                response = s.recv(1024)
                return response
        except Exception as e:
            # Handle any errors that occur during the communication
            print("Error:", e)
            return None

# Entry point of the script
if __name__ == "__main__":
    # Create a TaskClient instance with the server address
    client = TaskClient(('localhost', 5000))
    # Define the task data: task function name and its argument as a tuple
    task_data = ('square', 25)
    # Send the task data to the server and receive the result
    result = client.send_task(task_data)
    # Check if the result is received successfully
    if result:
        # Deserialize the result and print it
        print("Client 1, sent", task_data[1],"to get the square and received: ", pickle.loads(result))
    else:
        # Print an error message if an error occurred during task execution
        print("Error occurred while executing the task.")
