import socket
import sys
import os



def login(socket_fd):
    dicio={}
    os.system('clear')
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
        socket_fd.send(option.encode()) #manda a opcao escolhida pelo user
        nextm=socket_fd.recv(1024)
        nextm=nextm.decode()
        if nextm == 'continue': #se recebeu continue proxime set de opcoes
            options_menu(socket_fd)
        else:
            print("Ok... bye bye!")
            sys.exit(0)
    elif new_data == 'continue':
        options_menu(socket_fd)


            
def options_menu(socket_fd):
    os.system('clear')
    print("1.Inbox\n2.Delete E-mail\n3.Send Mail\n4.Log-Out") #menu de opcoes do user
    opcao=input("Introduza uma opcao valida: ")
    while(opcao !='1' and opcao != '2' and opcao != '3' and opcao != '4'):
        opcao=input("Introduza uma opcao valida: ")
    socket_fd.send(opcao.encode())
    #new_data=socket_fd.recv(2048)
    #new_data=new_data.decode()
    options(opcao, socket_fd)



    
def options(option, socket_fd): #menu de opcoes possiveis
    os.system('clear')
    if option == '1': #escolhe ver a inbox
        print("------INBOX---------\n")
        new_data=socket_fd.recv(2048)
        new_data=new_data.decode()
        print(new_data) #recebe tudo da lista do utilizador
        if new_data == 'empty':
            opcao=input("Inbox vazia pressione qualquer tecla para ir para o menu inicial: ")
        else:
            number=input("Deseja observar algum email? [number/0]: ")
            socket_fd.send(number.encode()) #manda a opcao
            mail=socket_fd.recv(2048)
            mail=mail.decode()
            os.system('clear')
            if(mail=='break'): #se recebe break do servidor vai para o menu
                print("Sera agora remetido para o seu menu")
                final=input("Press any key to go to inicial menu: ")
            else:
                print(mail) #se nao for break recebe o mail correspondente
                final=input("Press any key to go to inicial menu: ")
        options_menu(socket_fd)
    elif option == '2': #opcao para dar DELETE
        print("------DELETE--------\n")
        new_data=socket_fd.recv(2048)
        new_data=new_data.decode()
        print(new_data) #imprime a lista de emails
        number=input("Insira o numero do mail que deseja eliminar [number/0]: ")
        socket_fd.send(number.encode())
        product=socket_fd.recv(2048)
        product=product.decode()
        if product == 'break': #SE MANDAR O 0
            print("Sera agora remetido para o seu menu")
            final=input("Press any key to go to inicial menu: ")
        else: #vai imprimir os mails do user atualizados
            os.system('clear')
            print("Emails atualizados com sucesso!\n\n")
            print(product)
            final=input("Press any key to go to inicial menu: ")
        options_menu(socket_fd)
    elif option == '3':
        lista=[]
        print("New Mail:\n")
        assunto=input("Assunto: ")
        remetente=input("To: ")
        info=input("Content: ")
        lista.append(assunto)
        lista.append(remetente)
        lista.append(info)
        socket_fd.send(str(lista).encode())
        confirm=socket_fd.recv(1024)
        confirm=confirm.decode()
        if confirm == 'sent':
            print("Mail sent to: ", remetente)
            final=input("Press any key to go to inicial menu: ")
            options_menu(socket_fd)
        elif confirm == 'no':
            print('Mail not sent to: ', remetente)
            final=input('Press any key to go to inicial menu: ')
            options_menu(socket_fd)
    elif option == '4':
        confirm=socket_fd.recv(1024)
        confirm=confirm.decode()
        if confirm=='ok':
            print("User disconnected")
            final=input("Press any key to go to inicial menu: ")
            sys.exit(1)

        
if __name__=='__main__':
    PORT = 9000              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST=socket.gethostname()
    s.connect((HOST, PORT))
    login(s)
    s.close()
