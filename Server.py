import json
import pickle
import uuid
from socket import *


class Task:
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description


class Server:
    def __init__(self, c=None):
        host = '127.0.0.1'
        port = 8888
        if c is None:
            self.c = socket(AF_INET, SOCK_STREAM)
            self.c.bind((host, port))
            self.c.listen(3)

        else:
            self.c = c

    def accept_connection(self):
        return self.c.accept()

    def close_connection_with_client(self):
        self.c.close()
        print("Client close")

    @staticmethod
    def send_to_client(client, message):
        client.send(str(message))


def receive_prompt(conn):
    data = conn.recv(4096)
    return data


def read_task(conn):
    data = conn.recv(4096)
    data_variable = pickle.loads(data)
    return data_variable


def save_task_to_json(filename, task):
    with open(filename, 'r') as fp:
        old_json = json.load(fp)
    task_uuid = str(uuid.uuid4())
    json_task = {task_uuid: {"priority": task.priority, "description": task.description}}

    old_json.update(json_task)
    with open(filename, 'w') as fp:
        json.dump(old_json, fp)


def list_all_tasks(filename):
    tasks_file = open(filename, 'r')
    json_decode = json.load(tasks_file)
    message = ""
    for key in json_decode.keys():
        priority = json_decode[str(key)]["priority"]
        description = json_decode[str(key)]["description"]
        message += "Id:{0}, Priority: {1}, Description: {2}".format(key, priority, description) + "\n"
    return message


def delete_task(filename, task_uuid):
    with open(filename, 'r') as fp:
        old_json = json.load(fp)
    try:
        old_json.pop(task_uuid)
    except KeyError, e:
        return str("Item with UUID: '{0}' doesn't exist".format(e.message))
    with open(filename, 'w') as fp:
        json.dump(old_json, fp)


def get_tasks_with_priority(filename, exact_priority):
    tasks_file = open(filename, 'r')
    json_decode = json.load(tasks_file)
    message = ""

    for key in json_decode.keys():
        priority = json_decode[str(key)]["priority"]
        if priority == exact_priority:
            description = json_decode[str(key)]["description"]
            message += "Id:{0}, Priority: {1}, Description: {2}".format(key, priority, description) + "\n"

    message += "-"
    return message


def main():
    # while True:
    server = Server()
    client, address = server.accept_connection()
    print('Connection with {0}'.format(str(address)))
    while True:
        data = receive_prompt(client)
        if data == 'close':
            break
        elif data == 'get_tasks':
            server.send_to_client(client, list_all_tasks("./tasks.json"))
        elif data == 'get_tasks_with_priority':
            server.send_to_client(client, get_tasks_with_priority("./tasks.json", receive_prompt(client)))
        elif data == 'add_task':
            task = read_task(client)
            save_task_to_json("./tasks.json", task)
        elif data == 'delete_task':
            server.send_to_client(client, delete_task("./tasks.json", receive_prompt(client)))

    server.close_connection_with_client()


if __name__ == "__main__":
    main()
