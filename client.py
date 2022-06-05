# UDP protocol

import socket
import threading
import os
import sqlite3

# max UPD package size
UDP_MAX_SIZE = 65535

# connect to db
db = sqlite3.connect('user_databse.db')
# создание курсора в БД
cursor = db.cursor()


def sign_in(login, id):
    cursor.execute(f'SELECT login FROM users WHERE login = "{login}"')
    if cursor.fetchone() is None:
        registration(login, id)
    else:
        password = input('Password: ')
        while cursor.execute(f'SELECT password FROM users WHERE login = "{login}"').fetchone()[0] != password:
            print('Password incorrect! Please try again')
            password = input('Password: ')
    if cursor.execute(f'SELECT client_id FROM users WHERE login = "{login}"').fetchone()[0] != id:
        cursor.execute(f"UPDATE users SET client_id = '{id}' WHERE login = '{login}'")
        db.commit()

def registration(login, id):
    password = input(f"Hello {login}! Please input your password for registration: ")
    cursor.execute(f'INSERT INTO users (login, password, client_id) VALUES (?, ?, ?)', (login, password, id))
    print(f'User {login} successfully created!')
    db.commit()


def listen(s: socket.socket):
    while True:
        msg = s.recv(UDP_MAX_SIZE)
        print('\r\r' + msg.decode('ascii') + '\n' + f'You: ', end='')


def connect(host: 'str' = '127.0.0.1', port: int = 3000):
    global login
    # create socket object, IPv4, UDP protocol
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    
    s.connect((host, port))
    id = s.getsockname()[1]
    login = input('Login: ')
    sign_in(login, id)
    threading.Thread(target=listen, args=(s,), daemon=True).start()

    s.send('__join'.encode('ascii'))

    while True:
        msg = input(f'You: ')
        s.send(msg.encode('ascii'))

if __name__ == '__main__':
    os.system('clear')
    print('Welcome to chat!')
    connect()