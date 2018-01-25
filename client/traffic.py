'''
    Class for communication with remote server (core)
'''
import socketserver
import json
import requests

class Sender():
    
    def __init__(self, client):
    
        self.client = client
        self.remote_server = "http://localhost:8080"
    
    def register_player(self, address, name):
        r = requests.post(self.remote_server + "/registerPlayer", 
                            data={'name': name, 'address': address})

    def get_players(self):
        r = requests.get(self.remote_server + "/inGame")
        data = json.loads(r.text)
        self.client.draw_seats(data)

    def take_seat(self, address, number):
        r = requests.post(self.remote_server + "/takeSeat", 
                            data={'seat': number, 'address': address})
        data = json.loads(r.text)
        if(data):
            self.client.draw_empty_seats(data)

    def check(self):
        pass
    
    def bet(self):
        pass
    
    def fold(self):
        pass

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def __init__(self, client):
        self.client = client

    def __call__(self, request, client_address, server):
        h = MyTCPHandler(self.client)
        socketserver.BaseRequestHandler.__init__(h, request, client_address, server)

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        
        data = self.data.decode('UTF-8').split('\r\n\r\n')[1] #split request with new line (header is at position 0, data is at position 1)
        data = json.loads(data)
        self.client.data = data

        for x in data:
            self.client.refresh_table(x)

        # just send back the same data, but upper-cased
        response = b'HTTP/1.1 200 OK\n\n'
        self.request.sendall(response)