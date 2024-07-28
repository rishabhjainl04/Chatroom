#importing libraries
import threading
import socket

#taking name from user
name = input("Login with your name :")

#creating socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '10.196.14.36'
port = 55000
#connecting
client.connect((host,port))

#function for receiving message
def rev_msg():
    #running infinite loop
    while True:
        try:
            #receiving message
            msg = client.recv(1024)
            if msg.decode()=="Enter your login name:":
                client.sendto(name.encode('utf-8'),(host,port))
            else:
                print(msg.decode())
        #running exception
        except:
            print("Some error has occured!!")
            client.close()


#function for sending message
def send_msg():
    #infinite loop for accepting messg
    while True:
        msg = f'{name}: {input("")}'
        client.sendto(msg.encode('utf-8'),(host,port))


#running threads for receiving message
thread_recv = threading.Thread(target = rev_msg)
thread_recv.start()

#running thread fro sending message
thread_send = threading.Thread(target = send_msg)
thread_send.start()