# Echo client program
import socket

def menu_inicial(socket_fd):
    print("WebMail:\n\n")
    print("1.Login user\t\t\t2.Create user\n\nYour option: ")
    c1='1'
    c2='2'
    opcao=int(input())
    print(opcao)
    if (opcao.isalpha()!=True or (opcao!=1 and opcao!=2)):
        while(opcao.isalpha()!=True or (opcao!=1 and opcao!=2)):
            opcao=input("Introduza uma opcao valida por favor: ")
            print(opcao)
    login(socket_fd)

def login(socket_fd):
    lista=[]
    username=input("Introduza o seu username: ")
    password=input("Introduza a sua password: ")
    lista.append(username)
    lista.append(password)
    socket_fd.send(lista)

if __name__=='__main__':
    HOST = '127.0.0.1'    # The remote host
    PORT = 9000              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(b'Hello, world\n')
    s.send(b'te fudere')
    menu_inicial(s)
    data = s.recv(1024)
    s.close()
    print('Received', repr(data))
