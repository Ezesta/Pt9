import socket
import threading


class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.pool = threading.Thread(target=self._server())
        self.pool.start()


    def _server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.host, self.port))
        clients_address = []
        print('Start server')

        while True:
            data, address = sock.recvfrom(1024)
            if address not in clients_address:
                clients_address.append(address)
                print(f'{clients_address[-1]} join')
            for client in clients_address:
                if client == address:
                    continue
                sock.sendto(data, client)
if __name__ == '__main__':
    host = '127.0.0.1'
    port = 9090
    server = Server(host=host, port=port)


