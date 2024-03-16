from socket import socket
import threading
import pandas as pd
import App


class Server():
    def __init__(self):
        self.SERVER_IP = '127.0.0.1'
        self.SERVER_PORT = 12345
        self.soc = socket()
        self.soc.bind(( self.SERVER_IP,  self.SERVER_PORT))
        self.users_db = pd.read_csv('users.csv',header=0,index_col=0)
        self.soc.listen(2)
        print('server is up and ready')
        self.handle_clients()


    def handle_clients(self):
        while True:
            s1, addr = self.soc.accept()
            print('client is connected')
            t=threading.Thread(target=self.Handle_client,args=(s1,addr))
            t.start()



    def Handle_client(self, s1:socket, addr:tuple):
        global mutex
        while True:
            data=s1.recv(1024).decode()
            print(f'{data} was recieved')
            data_info = data.split(':')
            connection_type = data_info[0]
            user = data_info[1].split('&')
            print(user)
            if connection_type=='login':
                mutex.acquire()
                if ((self.users_db['username']==user[0]) & (self.users_db['password']==user[1])).any():
                    mutex.release()
                    s1.send('valid user'.encode())
                else:
                    mutex.release()
                    s1.send('invalid user'.encode())
            elif connection_type=='signup':
                mutex.acquire()
                if ((self.users_db['username']==user[0]) & (self.users_db['password']==user[1])).any():
                    mutex.release()
                    s1.send('user already exists'.encode())
                else:
                    self.users_db.loc[len(self.users_db)] = [user[0], user[1]]
                    self.users_db.to_csv('users.csv')
                    mutex.release()
                    s1.send('new user has been succecfuly added'.encode())


                



        '''
        while True:
            self.s1, self.addr =self.soc.accept()
            t=threading.Thread(target=self.HandleUser,args=(self.s1,self.addr, self.users_db))
            t.start()
        '''
    #def HandleUser(self):
        #App.main()


def main():
    global mutex
    mutex = threading.Lock()
    server = Server()


if __name__=='__main__':
    main()

