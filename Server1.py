# Echo server program
import socket    

if __name__=='__main__':
    HOST = "127.0.0.1"                # Symbolic name meaning all available interfaces
    PORT =9000               # Arbitrary non-privileged port
    data=[]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)
    while True:
        data.append( conn.recv(1024))
        if not data: break
        conn.send(data)
        conn.close()
