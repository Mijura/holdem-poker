'''
    Simple socket server using threads
'''
 
import socket
import json

class Listener:
    
    def __init__(self, client):
    
        self.client = client
        self.HOST = socket.gethostbyname(socket.gethostname()) # get ip address
        self.PORT = 0 #when we put zero soceket bind will get free port
 
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))

        self.PORT = self.s.getsockname()[1] #get port
        print(self.PORT)
        
        self.done = False
        
    def listen(self):
        self.s.listen(10)
        #wait for changes
        while not self.done:
            connection, addr = self.s.accept()
            request = connection.recv(100000)
            data = request.decode('UTF-8').split('\r\n\r\n')[1] #split request with new line (header is at position 0, data is at position 1)
            data = json.loads(data) # convert json string to json
            try:
                self.client.refresh_table()
            except:
                print("client is gone...")
            connection.close()
     
        self.s.close()