import socket
import os
import sys

HOST = "0.0.0.0"  
PORT = 5000     

# Make the server directory ready
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
os.makedirs("DataBase", exist_ok=True)
# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"Echo server is listening on {HOST}:{PORT}...")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")


while True:
    
    data = conn.recv(1024)
    print(data)
    message = data.decode()
    print(f"Received: {message}")   
    if(message==""): continue
    if(message.startswith("listFiles")):
        import os
        files = os.listdir("DataBase")
        fileNames = "\n".join(files) + "\n"
        conn.sendall(fileNames.encode())
        continue
    if(message.startswith("receiveFile:")):
        FileName = message.split(":",1)[1]

        try:
            with open("DataBase\\"+FileName, "rb") as f:
                data = f.read()
            PrePacket = "[{}][{}]".format(FileName, len(data))
            conn.sendall(PrePacket.encode())
            ack = conn.recv(1024)
            conn.sendall(data)
            print(f"Sent file {FileName} to client.")
        except FileNotFoundError:
            
            conn.sendall(b"FileNotFound")
        conn.sendall(b"GotIt")
        continue
    if message.lower() == "close":
        print("Received 'close'. Shutting down server.")
        conn.sendall(b"Server closing connection.")
        break

    FileName, SizeOfFile = message.strip('[]').split('][') 
    rdx = FileName.rfind("\\")
    if rdx!=-1:
        FileName=FileName[rdx+1:]
    print(f"Preparing to receive file: {FileName} of size {SizeOfFile} bytes")


    conn.sendall(b"upload")
    amountReceived = 0
    file = open(os.path.join("DataBase", FileName), 'wb')
    while amountReceived < int(SizeOfFile):
        chunk = conn.recv(1024)
        file.write(chunk)
        amountReceived += len(chunk)
    file.close()
    print(f"File {FileName} received successfully.")
    conn.sendall(b"recv")
conn.close()
server_socket.close()
