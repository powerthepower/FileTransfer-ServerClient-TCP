import socket
import os
import sys

HOST = '127.0.0.1'
PORT = 5000

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))


# Protocol:
# [NameOfFile][SizeOfFile]
while True:
    print("would you like to send/recieve a file? or list all files")
    inp = input("0 to send, 1 to recieve, 2 to list all files. and 3 to close the program : ")
    if inp=="3" or inp.lower() == "close" or inp.lower()=="exit":
        print("Closing connection as per user request.")
        break
    if inp == "0" or inp.lower()=="send":
        FileName = input("Please enter the file you want to send to the server:")

        # Read file content
        try:
            with open(FileName, 'rb') as file:
                content = file.read()
        except:
            print("file not found")
            continue
        PrePacket = "[{}][{}]".format(FileName, len(content))
        client_socket.send(PrePacket.encode())
        response= client_socket.recv(6)
        client_socket.sendall(content)
        response = client_socket.recv(1024)
        if(response.decode()=="upload"):
            print("upload in progress...")
        else:
            print("upload failed")
        response= client_socket.recv(4)
        if(response.decode()=="recv"):
            print("upload was successful!")
        else:
            print("upload failed")
        
        
    elif inp == "1" or inp.lower()=="recieve" or inp.lower()=="recv":
        print("Which file would you like to recieve?")
        FileName = input("Enter the name of the file to receive: ")
        client_socket.send(f"receiveFile:{FileName}".encode())
        response = client_socket.recv(1024)
        if response == b"FileNotFound":
            print("File not found on server.")
        else:
            FileName, SizeOfFile = response.decode().strip('[]').split('][') 
            client_socket.sendall(b"ACK")
            data = b""
            while len(data) < int(SizeOfFile):
                chunk = client_socket.recv(1024)
                data += chunk
            with open(FileName, 'wb') as f:
                f.write(data)
            print(f"File {FileName} received successfully.")
    elif inp == "2" or inp.lower()=="list" or inp.lower()=="listfiles" or inp.lower()=="files":
        print("All files:")
        client_socket.send(b"listFiles")
        data = client_socket.recv(4096)
        print(data.decode())
    else:
        print("Unknown command")
client_socket.close()
