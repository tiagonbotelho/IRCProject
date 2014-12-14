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


def file_protection(filename):
    if os.stat(filename).st_size==0:
        ficheiro=open(filename, "w")
        ficheiro.write('{}')
        ficheiro.close()

    
def read_user_file(filename): #vai sempre ao iniciar o programa ler os users que tem
    f=open(filename,"r")
    aux=f.read()
    dicio=eval(aux) #torna a informacao num dicionario
    f.close()
    return dicio


def login(data, main_dicio, conn, mail_dicio, addr): #primeira opcao de login
    user_error=404
    for i in data: #vai percorrer a informacao fornecida pelo cliente
        print(i)
        
        if i in main_dicio: #se nao estiver no dicionario de users
            
            if(main_dicio[i] != data[i]): #se a pass estiver errada
                conn.send(str(user_error).encode()) #manda erro de pass errada
                return (False, i)

            else:
                conn.send("continue".encode()) #validation approved
                return (True,i)

        else:                               #caso exista
            conn.send('2'.encode()) 
            option=conn.recv(1024)
            option=option.decode() #pergunta ao cliente se deseja criar um user
            print(option) ##DEBUG

            if option == 'y':
                main_dicio.update(data) #faz update ao dicionario de users
                mail_dicio[i]=[]
                write_file(main_dicio, "users.txt") #update no file de users
                write_file(mail_dicio, "mails.txt")
                conn.send("continue".encode()) #pede mais informacao ao user
                return (True, i)

            else:
                conn.send("break".encode()) #caso nao manda o cliente terminar
                return (False, i)

                 
def char_inbox(username, mail_dicio): #coloca todos os emails do user numa string numerados
    buffer_string=""
    itera=1
    for i in mail_dicio:
        if i == username:
            
            lista=mail_dicio[i]
            
            if lista != []:
                for j in lista:
                    buffer_string+="Message number: "+str(itera)+"\n---------------\n"+"From: "+str(j[0])+"\n"+"Assunto: "+str(j[1])+"\n"+"-----------\n"
                    itera+=1
                return buffer_string

            else:
                return 'empty'
    return mail_dicio


def delete_mail(username, number, mail_dicio): #deleta do mail 
    for i in mail_dicio:
        if i == username:
            
            lista=mail_dicio[i] #copia para uma lista os mails de um user
            if lista != []:
                lista.pop(int(number)-1) #retira o mail na pos numero-1
                mail_dicio[username]=lista #renova o mail_dicio
                write_file(mail_dicio, 'mails.txt')
                return mail_dicio

            else:
                return empty
    return mail_dicio



def search_mail(mail_dicio, number, username): #procura o mail total para o mandar caso necessario
    for i in mail_dicio:
        if i == username:
            
            if mail_dicio[i] != '':
                lista=mail_dicio[i]
                total_mail=str(lista[int(number)-1][2])

            else:
                total_mail=''
    return total_mail


def set_mail(mail_dicio, new_mail, username, conn):
    lista=[username, new_mail[0], new_mail[2]]

    if new_mail[1] in mail_dicio: #se encontra no server1
       mail_dicio[new_mail[1]].append(lista)
       write_file(mail_dicio, 'mails.txt') #atualiza o ficheiro
       conn.send("sent".encode())

    else:
        lista.append(new_mail[1]) #se nao encontrar o user no server1
        PORT = 9001              # The same port as used by the server
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST=socket.gethostname()
        so.connect((HOST, PORT)) 
        so.send(str(lista).encode())
        data=so.recv(1024)
        data=data.decode()
        print(data) ##DEBUG

        if data == 'no':
            conn.send('no'.encode()) #manda o nao encontrou para o cliente

        elif data == 'sent':
            conn.send('sent'.encode()) #enviou para um user do servidor2
        so.close()


def accept_option(conn, username, mail_dicio):
    mail_dicio=read_user_file("mails.txt")
    main_dicio=read_user_file("users.txt")
    new_data=conn.recv(2048)
    new_data=new_data.decode()
    print(new_data)

    if new_data=='1':            #INBOX
        mail_dicio=read_user_file("mails.txt")
        main_dicio=read_user_file("users.txt")
        sender=char_inbox(username, mail_dicio) #string com todos os emails

        if sender != 'empty':
            conn.send(sender.encode())
            opcao=conn.recv(1024)
            opcao=opcao.decode() #vai decidir se quer ler um mail ou nao 0 se nao

            if opcao == '0':
                conn.send("break".encode())

            else:
                mail=search_mail(mail_dicio, opcao, username) #procura o mail
                conn.send(mail.encode()) #manda o email

        else:
            conn.send("empty".encode())        
    
    elif new_data=='2':                #DELETE
        mail_dicio=read_user_file("mails.txt")
        main_dicio=read_user_file("users.txt")
        sender=char_inbox(username, mail_dicio)
        
        if sender != 'empty':
            conn.send(sender.encode())
            deletion=conn.recv(1024) #vai receber o numero para deletar 0 nao deleta
            deletion=deletion.decode()

            if deletion == '0':
                conn.send("break".encode()) ##STILL NEEDS FIXING!!

            else:
                mail_dicio=delete_mail(username, deletion, mail_dicio) #mostra os mails atualizados
            new_product=char_inbox(username, mail_dicio)
            conn.send(new_product.encode())

        else:
            conn.send(sender.encode())

    elif new_data == '3':    #SENDER
        new_mail=conn.recv(2048)
        new_mail=new_mail.decode()
        new_mail=eval(new_mail)
        set_mail(mail_dicio, new_mail, username, conn) #coloca no email do user correspondente

    elif new_data == '4': #LOGOFF
        conn.send("ok".encode())
        return False
    accept_option(conn, username, mail_dicio)
    return True

def handler(conn, addr): #handlrer da thread
    mail_dicio=read_user_file("mails.txt")
    main_dicio=read_user_file("users.txt")

    while True:
        print('Connected by: ', addr)
        data=conn.recv(1024)
        data=data.decode()
        dicio=eval(data)
        result, i= login(dicio, main_dicio, conn, mail_dicio, addr)

        if result == True:
            log = accept_option(conn, i, mail_dicio)
        else:
            break
        if not data: break
    

if __name__=='__main__':
    PORT =9000               
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST= socket.gethostname()
    s.bind((HOST, PORT))
    s.listen(1)
    file_protection('mails.txt')
    file_protection('users.txt')
    mail_dicio=read_user_file("mails.txt")
    main_dicio=read_user_file("users.txt")

    while True:
        signal.signal(signal.SIGINT, signal_handler)
        print("Hello")
        conn, addr = s.accept()
        _thread.start_new_thread(handler, (conn, addr))
    conn.close()
