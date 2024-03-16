from socket import socket


class Client():
    def __init__(self) -> None:
        self.soc = socket()
        self.is_connected:bool = False
    def connect_server(self):
        SERVER_ADDR :tuple= ('127.0.0.1', 12345)
        self.soc.connect(SERVER_ADDR)
        self.is_connected = True

    def send_data(self, data:str):
        self.soc.send(data.encode())
    
    def recieve_data(self)->str:
        return self.soc.recv(1024).decode()
    
    def is_connected_to_server(self):
        return self.is_connected

def main():
    client = Client()


if __name__=='__main__':
    main()