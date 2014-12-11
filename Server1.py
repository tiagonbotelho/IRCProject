import socket

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

def login(data, main_dicio, conn, main_list): #primeira opcao de login
    user_error=404
    for i in data: #vai percorrer a informacao fornecida pelo cliente
        if i not in main_dicio: #se nao estiver no dicionario de users
            conn.send('2'.encode()) 
            option=conn.recv(1024)
            option=option.decode() #pergunta ao cliente se deseja criar um user
            if option == 'y':
                new_dicio={}
                main_dicio.update(dicio) #faz update ao dicionario de users
                aux_dicio[i]=[]
                main_list.append(aux_dicio) #faz update a lista de mails de users
                write_file(main_dicio, "users.txt") #update no file de users
                conn.send("continue".encode()) #pede mais informacao ao user
                accept_option(conn, i)
            else:
                conn.send("break".encode()) #caso nao manda o cliente terminar
        else:                               #caso exista
             if(main_dicio[i] != dicio[i]): #se a pass estiver errada
                 conn.send(str(user_error).encode()) #manda erro de pass errada
             else:
                 conn.send("continue".encode()) #validation approved
                 accept_option(conn, i)

def accept_option(conn, username):
    
    

if __name__=='__main__':
    HOST = "127.0.0.1"                
    PORT =9000               
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)
    while True:
        data=conn.recv(1024)
        data=data.decode()
        dicio=eval(data)
        if not data: break
        login(dicio, main_dicio, conn)
        conn.close()
