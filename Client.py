# Echo client program
import socket

if __name__=='__main__':
    HOST = '127.0.0.1'    # The remote host
    PORT = 9000              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(b'Hello, world\n')
    s.send(b'te fudere')
    data = s.recv(1024)
    s.close()
    print('Received', repr(data))
