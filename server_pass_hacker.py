import socket
import sys


def server(ip_add, port):
    '''
    A simple server.
    :param ip_add: Ip to connect.
    :param port: Port to connect to.
    :return: None.
    '''

    #The server's password, the attacker needs to crack.
    password = 'Fsx3Fc2'
    with socket.socket() as server_socket:
        server_socket.bind((ip_add, int(port)))
        server_socket.listen()
        conn, addr = server_socket.accept()
        print('Connected by', addr)

        #Listen to the client.
        while True:
            data = conn.recv(1024)
            print(data.decode())
            if not data:
                break
            if data.decode() == password:
                conn.sendall('Connection Success!'.encode())
            else:
                conn.sendall('Wrong password!'.encode())


server(sys.argv[1], sys.argv[2])
