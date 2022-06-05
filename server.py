# UDP protocol

from email import message
import socket
import sqlite3

# create db for user data
db = sqlite3.connect('user_databse.db')
# создание курсора в БД
cursor = db.cursor()
# Создание таблицы в БД(создать таблицу, если она не создана)
cursor.execute('''CREATE TABLE IF NOT EXISTS users(
    login TEXT,
    password TEXT,
    client_id REAL
    )
    ''')
db.commit()

# max UPD package size
UDP_MAX_SIZE = 65535

# start server function
def listen(host: 'str' = '127.0.0.1', port: int = 3000):
    # create socket object, IPv4, UDP protocol
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # add addres and host
    s.bind((host, port))
    print(f'Listening at {host}:{port}')

    members = []

    while True:
        msg, addr = s.recvfrom(UDP_MAX_SIZE)

        if addr not in members:
            members.append(addr)
        if not message:
            continue

        # Get client port
        client_id = addr[1]
        client_name = cursor.execute(f'SELECT login FROM users WHERE client_id = "{client_id}"').fetchone()[0]

        # Welcome message

        if msg.decode('ascii') == '__join':
            add_mes = f'User {client_name} joined chat!'
            [s.sendto(add_mes.encode('ascii'), member) for member in members if member != addr]
            continue

        # Main logic. Send message to all users, include sender

        msg = f'{client_name}: {msg.decode("ascii")}'
        for member in members:
            if member == addr:
                continue
            else:
                s.sendto(msg.encode('ascii'), member)


if __name__ == '__main__':
    listen()
