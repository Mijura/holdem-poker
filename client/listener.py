'''
    Simple socket server using threads
'''
 
import socket
import json
import requests

class Traffic:
    
    def __init__(self, client):
    
        self.client = client
        self.HOST = socket.gethostbyname(socket.gethostname()) # get ip address
        self.PORT = 0 #when we put zero 'socket bind' will randomly take one of free ports
 
        #socket opening
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.s.bind((self.HOST, self.PORT))

        self.PORT = self.s.getsockname()[1] #setting obtained port
        print(self.PORT)
        
        self.done = False
    
    def register_player(self):
        address = ''.join([self.HOST,':', str(self.PORT)])
        r = requests.post("http://localhost:8080/registerPlayer", data={'name': 'mio', 'address': address})
        print(r.status_code, r.reason)

    def listen(self):
        self.s.listen(10)
        #wait for changes
        while not self.done:
            connection, addr = self.s.accept()
            request = connection.recv(100000)
            data = request.decode('UTF-8').split('\r\n\r\n')[1] #split request with new line (header is at position 0, data is at position 1)
            data = json.loads(data) # convert json string to json
            try:
                self.client.refresh_table(data)
            except:
                raise
            connection.close()
     
        self.s.close()