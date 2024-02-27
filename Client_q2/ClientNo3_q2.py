import socket
import pickle

class TaskClient:
    def __init__(self, server_address):
        self.server_address = server_address

    def send_task(self, task_data):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.server_address)
                serialized_task_data = pickle.dumps(task_data)
                s.sendall(serialized_task_data)
                response = s.recv(1024)
                return response
        except Exception as e:
            print("Error:", e)
            return None

if __name__ == "__main__":
    client = TaskClient(('localhost', 5000))
    task_data = ('square', 60)  # Task data for client 1
    result = client.send_task(task_data)
    if result:
        print("Client 3, sent", task_data[1],"to get the square and received: ", pickle.loads(result))
    else:
        print("Error occurred while executing the task for Client 3.")