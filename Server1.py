import socket
import os
import signal
import sys


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



def login(data, main_dicio, conn, mail_dicio): #primeira opcao de login
    user_error=404
    for i in data: #vai percorrer a informacao fornecida pelo cliente
        print(i)
        if i in main_dicio: #se nao estiver no dicionario de users
            if(main_dicio[i] != data[i]): #se a pass estiver errada
                conn.send(str(user_error).encode()) #manda erro de pass errada
                return (False, i)
            else:
                conn.send("continue".encode()) #validation approved
                return (True, i)
        else:                               #caso exista
            conn.send('2'.encode()) 
            option=conn.recv(1024)
            option=option.decode() #pergunta ao cliente se deseja criar um user
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
    for j in lista:
        buffer_string+=str(itera)+"\n---------------\n"+str(j[0])+"\n"+str(j[1])+"\n"+"-----------\n"
        itera+=1
    return buffer_string



def delete_mail(username, number, mail_dicio): #deleta do mail 
    for i in mail_dicio:
        if i == username:
            lista=mail_dicio[i] #copia para uma lista os mails de um user
    lista.pop(int(number)-1) #retira o mail na pos numero-1
    mail_dicio[username]=lista #renova o mail_dicio
    write_file(mail_dicio, 'mails.txt')
    return mail_dicio



def search_mail(mail_dicio, number, username): #procura o mail total para o mandar caso necessario
    for i in mail_dicio:
        if i == username:
            lista=mail_dicio[i]
    total_mail=str(lista[int(number)-1][2])
    return total_mail


def set_mail(mail_dicio, new_mail, username):
    lista=[username, new_mail[0], new_mail[2]]
    mail_dicio[new_mail[1]].append(lista)
    return mail_dicio

def accept_option(conn, username, mail_dicio): 
    new_data=conn.recv(2048)
    new_data=new_data.decode()
    print(new_data)
    if new_data=='1':
        sender=char_inbox(username, mail_dicio) #string com todos os emails
        conn.send(sender.encode())
        opcao=conn.recv(1024)
        opcao=opcao.decode() #vai decidir se quer ler um mail ou nao 0 se nao
        if opcao == '0':
            conn.send("break".encode())
        else:
            mail=search_mail(mail_dicio, opcao, username) #procura o mail
            conn.send(mail.encode()) #manda o email
    elif new_data=='2':
        sender=char_inbox(username, mail_dicio) 
        conn.send(sender.encode())
        deletion=conn.recv(1024) #vai receber o numero para deletar 0 nao deleta
        deletion=deletion.decode()
        if deletion == '0':
            conn.send("break".encode())
        else:
            mail_dicio=delete_mail(username, deletion, mail_dicio)
            new_product=char_inbox(username, mail_dicio)
            conn.send(new_product.encode())
    elif new_data == '3':
        new_mail=conn.recv(2048)
        new_mail=new_mail.decode()
        new_mail=eval(new_mail)
        mail_dicio=set_mail(mail_dicio, new_mail, username)
        write_file(mail_dicio, 'mails.txt')
        conn.send("sent".encode())
    elif new_data == '4':
        conn.send("ok".encode())
        return False
    accept_option(conn, username, mail_dicio)
    return True
            

if __name__=='__main__':
    PORT =9000               
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST= socket.gethostname()
    s.bind((HOST, PORT))
    s.listen(1)
    #conn, addr = s.accept()
    #print('Connected by', addr)
    mail_dicio=read_user_file("mails.txt")
    main_dicio=read_user_file("users.txt")
    while True:
        signal.signal(signal.SIGINT, signal_handler)
        conn, addr = s.accept()
        print('Connected by', addr)
        data=conn.recv(1024)
        data=data.decode()
        dicio=eval(data)
        result, i=login(dicio, main_dicio, conn, mail_dicio)
        if result == True:
            log=accept_option(conn, i, mail_dicio)
            #if log == False:
            #    break
        else:
            break
        if not data: break
        
    conn.close()
