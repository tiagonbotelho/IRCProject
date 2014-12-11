import socket
import system

def login(socket_fd):
    dicio={}
    username=input("Introduza o seu username: ")
    password=input("Introduza a sua password: ")
    dicio[username]=password #coloca em dicionario a informacao do user
    socket_fd.send(str(dicio).encode()) #manda pelo socket
    new_data=socket_fd.recv(1024) 
    new_data=new_data.decode()
    if new_data == '404': 
        print("[ERROR] password wrong please try again!")
        login(socket_fd) #volta ao menu inicial para poder pedir a informacao
    elif new_data == '2':
        option=input("[User not found] do you wish to create one? [y/n] ")
        socket_fd.send(option.encode())
        nextm=socket_fd.recv(1024)
        nextm=nextm.decode()
            if nextm == 'continue':
                options_menu(socket_fd)
            else:
                print("Ok... bye bye!")
                sys.exit(0)

def options_menu(socket_fd):
    
            

if __name__=='__main__':
    HOST = '127.0.0.1'    # The remote host
    PORT = 9000              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    login(s)
    data = s.recv(1024)
    data=data.decode()
    dicionary=eval(data)
    s.close()
