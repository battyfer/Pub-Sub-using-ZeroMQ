#!/usr/bin/env python
import zmq, sys, os
import json
import uuid

def main():
    context = zmq.Context()
    client_id = str(uuid.uuid4())
    while True:
        print("\nChoose an option:")
        print("1. Get Server List")
        print("2. Join a server")
        print("3. Leave a server")
        print("4. Get Articles")
        print("5. Publish Article")
        print("6. Quit")

        choice = input("Enter your choice:\n")

        if choice == "1":
            context = zmq.Context()
            registry_socket = context.socket(zmq.REQ)
            registry_socket.connect("tcp://localhost:5555")
            registry_socket.send_json({"name": client_id, "request": "GetServerList"})
            response = registry_socket.recv_json()
            print(response) 

        elif choice == "2":
            server_address = input("Enter the server address to connect to (e.g. tcp://localhost:2000): ")
            server_socket = context.socket(zmq.REQ)
            server_socket.connect(server_address)

            server_socket.send_json({"name": client_id, "request": "JoinServer"})
            response = server_socket.recv_json()
            print(response["status"])

        elif choice == "3":
            server_address = input("Enter the server address you want to leave (e.g. tcp://localhost:2000): ")
            server_socket = context.socket(zmq.REQ)
            server_socket.connect(server_address)

            server_socket.send_json({"name": client_id, "request": "LeaveServer"})
            response = server_socket.recv_json()
            print(response["status"])

        elif choice == "4":
            server_address = input("Enter the server address you want to get articles from (e.g. tcp://localhost:2000): ")
            server_socket = context.socket(zmq.REQ)
            server_socket.connect(server_address)

            typ = input("Enter the type:\n")
            auth = input("Enter the author:\n")
            date = input("Enter the date(DD/MM/YYYY):\n")

            server_socket.send_json({"name": client_id, "request": "GetArticles", "type": typ, "author": auth, "date": date})
            response = server_socket.recv_json()
            if(response["status"] == "FAILED"):
                print(response["status"])
            else:
                data = response["data"]
                print(data)

        elif choice == "5":
            server_address = input("Enter the server address you want to publish an article to (e.g. tcp://localhost:2000): ")
            server_socket = context.socket(zmq.REQ)
            server_socket.connect(server_address)

            typ = input("Enter the type:\n")
            auth = input("Enter the author:\n")
            content = input("Enter the content:\n")

            if not (typ and auth and content):
                print("Illegal Format!")
                break
            server_socket.send_json({"name": client_id, "request": "PublishArticle", "type": typ, "author": auth, "content": content})
            response = server_socket.recv_json()
            print(response["status"])

        elif choice == "6":
            break
        else:
            print("Invalid Choice")




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)