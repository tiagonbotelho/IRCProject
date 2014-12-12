import socket
import os
import signal
import sys
import _thread

def signal_handler(signal, frame):
    print(' pressed...exiting now')
    sys.exit(1)

def write_file(dicio, filename):
    fp=open(filename, "w")
    fp.write(str(dicio))  #vai re-escrever sempre os users no ficheiro
    fp.close()


    
def read_user_file(filename): #vai sempre ao iniciar o programa ler os users que tem
    f=open(filename,"r")
    aux=f.read()
    dicio=eval(aux) #torna a informacao num dicionario
    f.close()
    return dicio


if __name__=='__main__':
    PORT =9001               
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST= socket.gethostname()
    s.bind((HOST, PORT))
    s.listen(1)
    mail_dicio=read_user_file("mails2.txt")
    main_dicio=read_user_file("users2.txt")
    while True:
        signal.signal(signal.SIGINT, signal_handler)
        conn, addr = s.accept()
        print('Connected by', addr)
        data=conn.recv(1024)
        data=data.decode()
        lista=eval(data)
        print(lista)
        if lista[3] not in main_dicio:
            conn.send("no".encode())
        else:
            new_lista=[lista[0],lista[1], lista[2]]
            mail_dicio[lista[3]].append(new_lista)
            conn.send("sent".encode())
            write_file(mail_dicio, 'mails2.txt')
        if not data: break
    conn.close()
