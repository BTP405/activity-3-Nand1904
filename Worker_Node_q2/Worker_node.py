# Import the necessary modules for socket communication and serialization
import socket
import pickle
# Import the 'square' function from the 'task_functions' module
from task_functions import square

# Define a class named TaskWorker for handling tasks in the worker node
class TaskWorker:
    # Constructor to initialize the server address
    def __init__(self, server_address):
        self.server_address = server_address

    # Method to start the worker node and listen for incoming connections
    def start(self):
        # Create a TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Bind the socket to the server address and start listening
            s.bind(self.server_address)
            s.listen(5)
            print("Worker node is listening...")
            # Continuously accept incoming connections and handle tasks
            while True:
                # Accept a connection from a client
                conn, addr = s.accept()
                print("Connected to", addr)
                # Use 'with' statement to ensure proper cleanup of the connection
                with conn:
                    print("Handling task...")
                    serialized_task = b''
                    # Receive the serialized task data in chunks until fully received
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        serialized_task += data
                        # Check if the serialized task is complete
                        if serialized_task.endswith(b'\x94.') or serialized_task.endswith(b'\x94\x0a.'):
                            break
                    try:
                        # Unpickle the serialized task to get the task name and argument
                        task_name, argument = pickle.loads(serialized_task)
                        print("Task name:", task_name)
                        print("Argument:", argument)
                        # Dynamically execute the function based on its name
                        if task_name == 'square':
                            # Call the 'square' function with the provided argument
                            result = square(argument)
                            # Serialize the result and send it back to the client
                            serialized_result = pickle.dumps(result)
                            conn.sendall(serialized_result)
                            print("Result sent back to the client:", result)
                        else:
                            print("Unknown task:", task_name)
                    except Exception as e:
                        print("Error processing task:", e)

# Entry point of the script
if __name__ == "__main__":
    # Create a TaskWorker instance with the server address
    worker = TaskWorker(('localhost', 5000))
    # Start the worker node
    worker.start()