#!/usr/bin/env python3
import pickle
from socket import *


class Task:
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description


class Client:
    def __init__(self, s=None):
        if s is None:
            self.s = socket(AF_INET, SOCK_STREAM)
            self.s.settimeout(4)
        else:
            self.s = s

    def connect(self, host, port):
        try:
            self.s.connect((host, port))
            print("Connected to server")
        except Exception, msg:
            print ("Can't connect: {0}".format(msg))

    def get_tasks(self, request):
        self.s.send(request)
        tm = self.s.recv(4096).encode()
        print tm

    def get_tasks_with_priority(self, request, priority):
        self.s.send(request)
        self.s.send(priority)
        tm = self.s.recv(4096).encode()
        print tm

    def add_task(self):
        task = Task(raw_input("Priority: "), raw_input("Description: "))
        self.s.send("add_task")
        self.s.send(pickle.dumps(task))

    def delete_task(self, request, task_uuid):
        self.s.send(request)
        self.s.send(task_uuid)
        tm = self.s.recv(4096).encode()
        print tm

    def close_connection(self):
        self.s.send("close")
        self.s.close()
        print("Connection closed")


# def add_task

def switch(argument, server_connection):
    if argument == '1':
        server_connection.connect('127.0.0.1', 8888)
    elif argument == '2':
        server_connection.get_tasks("get_tasks")
    elif argument == '3':
        server_connection.get_tasks_with_priority("get_tasks_with_priority", str(raw_input("Priority -> ")))
    elif argument == '4':
        server_connection.add_task()
    elif argument == '5':
        server_connection.delete_task("delete_task", raw_input("UUID -> "))
    elif argument == '6':
        server_connection.close_connection()
    elif argument == '0':
        exit(0)
    else:
        print("Invalid value")


def menu(server_connection):
    choose = 0
    while choose is not '0':
        print("1: Connect with server")
        print("2: Print to-do list")
        print("3: Print to-do list with certain priority")
        print("4: Add task")
        print("5: Delete task")
        print("6: Close connection")
        print("0: Exit")
        choose = raw_input("Select: ")
        switch(choose, server_connection)


def main():
    server_connection = Client()
    menu(server_connection)


if __name__ == '__main__':
    main()
