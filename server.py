#!/usr/bin/env python
import zmq, sys, os
import json
import datetime
from datetime import datetime, date

CLIENTELE = []
MAX_CLIENTS = 6
data = []

def main(server: str, port: str):
    context = zmq.Context()

    # Bind to the server port
    server_socket = context.socket(zmq.REP)
    add = "tcp://*:" + port
    server_socket.bind(add)

    # Connect to the registry server
    registry_socket = context.socket(zmq.REQ)
    registry_socket.connect("tcp://localhost:5555")

    # Send a registration request
    add = "tcp://localhost:" + port
    registry_socket.send_json({"name": server, "address": add, "request": "Register"})

    # Receive response from the registry server
    response = registry_socket.recv_json()
    print(response["status"])

    while True:
        result = server_socket.recv_json()

        if (result["request"] == "JoinServer"):
            print("JOIN REQUEST FROM", result["name"])
            if(len(CLIENTELE) < MAX_CLIENTS):
                if (result["name"] not in CLIENTELE):
                    CLIENTELE.append(result["name"])
                    response = {"status": "SUCCESS"}
                else:
                    response = {"status": "FAILED"}
            else:
                response = {"status": "FAILED"}
            server_socket.send_json(response)

        elif(result["request"] == "LeaveServer"):
            print("LEAVE REQUEST FROM", result["name"])
            if (result["name"] in CLIENTELE):
                CLIENTELE.remove(result["name"])
                response = {"status": "SUCCESS"}
            else:
                response = {"status": "FAILED"}
            server_socket.send_json(response)
        
        elif(result["request"] == "GetArticles"):
            print("ARTICLES REQUEST FROM", result["name"])
            print("FOR", result["type"],"," ,result["author"],",",result["date"])
            if (result["name"] in CLIENTELE):
                type = result["type"]
                authorr = result["author"]
                date_get = result["date"]
                if(type and authorr):
                    filtered_data = [d for d in data if d['type'] == type and d['author'] == authorr and datetime.strptime(d['date'], '%d/%m/%Y') > datetime.strptime(date_get, '%d/%m/%Y')]
                elif(type and not(authorr)):
                    filtered_data = [d for d in data if d['type'] == type and datetime.strptime(d['date'], '%d/%m/%Y') > datetime.strptime(date_get, '%d/%m/%Y')]
                elif(authorr and not(type)):
                    filtered_data = [d for d in data if d['author'] == authorr and datetime.strptime(d['date'], '%d/%m/%Y') > datetime.strptime(date_get, '%d/%m/%Y')]
                else:
                    filtered_data = [d for d in data if datetime.strptime(d['date'], '%d/%m/%Y') > datetime.strptime(date_get, '%d/%m/%Y')]

                response = {"status": "SUCCESS", "data": filtered_data}
            else:
                response = {"status": "FAILED"}
            server_socket.send_json(response)

        elif(result["request"] == "PublishArticle"):
            print("ARTICLES PUBLISH FROM", result["name"])
            if(result["name"] not in CLIENTELE):
                response = {"status": "FAILED"}
            else:
                ty = result["type"]
                author = result["author"]
                date_pub = date.today().strftime('%d/%m/%Y') 
                content = result["content"]
                obj = {'type': ty, 'author': author, 'date': date_pub, 'content': content}
                data.append(obj)
                response = {"status": "SUCCESS"}
            server_socket.send_json(response)


if __name__ == '__main__':
    try:
        args = sys.argv
        main(args[1], args[2])
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)