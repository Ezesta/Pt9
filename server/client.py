import socket
import threading


class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server = self.host, self.port
        self.alias = input('Введите ваш ник: ')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', 0))
        self.sock.sendto((f'{self.alias} connected to server').encode('utf-8'), self.server)

        pool = threading.Thread(target=self._read_sock)
        pool.start()
        self.send_message()

    def _read_sock(self):
        while True:
            data = self.sock.recv(1024)
            print(data.decode('utf-8'))

    def send_message(self):
        while True:
            message = input('')
            try:
                self.sock.sendto(
                    (f'[{self.alias}] {message}').encode('utf-8'), self.server
                )
            except Exception as ex:
                print(repr(ex))

if __name__ == '__main__':
    user = Client(host='127.0.0.1', port=9090)
