import socket
import threading
from chat_settings import HOST, PORT, MAX_CLIENTS, BUFFER_SIZE

class ChatServer:
    '''
    class for chat server
    '''
    def __init__(self, host, port):
        print("init server...")
        self.all_users = []
        #create socket and listen new connections
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((HOST, PORT))
        self.sock.listen(MAX_CLIENTS)
        print("server: OK")
        print("waiting...")
        
        
    def run(self):
        '''
        function for receiving new connection,
        for creating new thread, which handle own clients.
        '''
        while True:
            conn, addr = self.sock.accept()
            tr = threading.Thread(
                                target=self.client_handler, 
                                args=(conn,)
                                )
            tr.daemon = True
            tr.start()
            
    def client_handler(self, conn):
        '''
        function for handling new connection
        '''
        
        #first message is client name
        name = conn.recv(BUFFER_SIZE)
        name = name.decode("utf-8")
        print("new "+name)
        hello_string = "Hello, {}. Users online is {}".format(
                                                    name, 
                                                    len(self.all_users)
                                                    )
        conn.sendall(hello_string.encode())
        self.all_users.append((conn, name))
        msg_to_all = "I entered chat!".format(name)
        self.send_message_to_others((conn, name), msg_to_all)    
        
        #infinite loop for receiving messages from client
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            data = data.decode("utf-8")
            print(name + ' ' + data)
            self.send_message_to_others((conn, name), data)    
        #client left chat
        conn.sendall(b'Buy')
        self.send_message_to_others(
                                (conn, name), 
                                "I left the chat!".format(name)
                                )    
        self.delete_user(conn)
        
    def delete_user(self, del_user):
        '''
        function for delete client from list all_users
        '''
        for i in range(len(self.all_users)):
            if self.all_users[i][0] == del_user:
                del self.all_users[i]
                break

    def send_message_to_others(self, from_user, message):
        '''
        function for sending message to all client except sender
        '''
        if len(self.all_users) > 1:
            for user in self.all_users:
                if user[0] != from_user[0]:
                    msg = "{}: {}".format(from_user[1], message)
                    user[0].sendall(msg.encode("utf-8"))
                    print("message send")
                    
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, tb):
        print("server is tired.")

with ChatServer(HOST, PORT) as chat:
    chat.run()
