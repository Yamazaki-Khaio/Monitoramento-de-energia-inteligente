import json
import socket
import time

from models.servidor import write_database, read_database


def main():
    host = '0.0.0.0'
    port = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    while True:
        c, addr = s.accept()
        print('Obeteve conexão de', addr)
        c.send(b'energy_meter_value')
        c.close()


def insert_energy_meter_value(id, value, timestamp):
    write_database(id, value, timestamp)



def get_energy_meter_value(id):
    read_database(id)


def update_energy_meter_value(id, value):
    timestamp = int(time.time())
    insert_energy_meter_value(id, value, timestamp)


def handle_client_connection(client_socket, id):
    request = client_socket.recv(1024)
    value = get_energy_meter_value(id)
    client_socket.send(str(value).encode())
    update_energy_meter_value(id, value)


if __name__ == '__main__':
    main()
