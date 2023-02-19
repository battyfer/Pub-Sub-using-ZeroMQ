import zmq, sys, os
# import json

servers = []
max_servers = 6

def main():
    context = zmq.Context()
    registry_socket = context.socket(zmq.REP)
    registry_socket.bind("tcp://*:5555")

    while True:
        result = registry_socket.recv_json()
        # print(result)

        if (result["request"] == "Register"):
            print("JOIN REQUEST FROM", result["address"])
            if(len(servers) < max_servers):
                if (result["address"] not in servers):
                    servers.append({"name": result["name"], "address": result["address"]})
                    response = {"status": "SUCCESS"}
                else:
                    response = {"status": "FAILED"}
            else:
                response = {"status": "FAILED"}
            registry_socket.send_json(response)

        elif(result["request"] == "GetServerList"):
            print("SERVER LIST REQUEST FROM", result["name"])
            registry_socket.send_json(servers)
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)