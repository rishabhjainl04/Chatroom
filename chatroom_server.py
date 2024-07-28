#importing libraries
import threading
import socket

#creating socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '10.196.14.36'
port = 55000
#binding 
server.bind((host,port))
#listenign 100 connections
server.listen(100)


clients = []#array for clients
names = []#array for name


#function for broadcasting messg to eveeryone
def broadcast(msg):
    for client in clients:
        client.send(msg)


#function for messging clients
def manage_Clients(client):
    while True:
        try:
            #accepting data
            name = names[clients.index(client)]
            messg = client.recv(1024).decode("utf-8")
            if messg == f'{name}: q':
                #conditin for quitting
                names.remove(names[clients.index(client)])
                clients.remove(client)
                
                broadcast(f'{name} disconencted from server'.encode("utf-8"))
                c = len(clients)
                broadcast('No. of chatters {}'.format(c).encode("utf-8"))
                client.close()
                break
            else:
                broadcast(messg.encode("utf-8"))

        except:
            
            name = names[clients.index(client)]
            names.remove(names[clients.index(client)])
            clients.remove(client)
            client.close()
            broadcast(f'{name} has left the chat room!'.encode('utf-8'))
            break


#function for receiving messages
def server_recv():
    c=0
    #running loop infinite times
    while True:
        print("Server Listening and Running: ")
        client,addr = server.accept()
        #performing other functions
        print(f'Established connection with {str(addr)}')
        client.send('Enter your login name:'.encode('utf-8'))
        name = client.recv(1024).decode()
        #aooending data to client and name
        names.append(name)
        clients.append(client)
        #finding length of clients
        c = len(clients)
        print(f"Users name is {name}")
        broadcast(f"{name} is connected with us now.".encode('utf-8'))
        broadcast("No. of chatters is {}".format(c).encode('utf-8'))
        #starting thread
        thread = threading.Thread(target = manage_Clients,args = (client,))
        thread.start()

#function call for receiving function
server_recv()