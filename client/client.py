import pygame
from threading import Thread
from traffic import *
import socketserver
from contextlib import closing
import socket

class Client:
    
    def __init__(self, name):
        pygame.init()

        self.name = name
        
        #set window size, title and bacground image (table)
        self.display = pygame.display.set_mode((800,577))
        pygame.display.set_caption("Texas Hold`em Poker")
        self.bg = pygame.image.load("images/table.png")
        self.display.blit(self.bg, (0, 0))
        pygame.display.flip()
        
        self.player_coord = {'1': (5, 345), '2': (5, 105), '3': (325, 30), '4': (645, 105), '5': (645, 345), '6': (325, 420)}
        self.empty_coord = {'1': (55, 390), '2': (55, 105), '3': (355, 45), '4': (645, 105), '5': (645, 390), '6': (355, 450)}

        self.HOST, self.PORT = self.get_address()
        self.address = ''.join([self.HOST,':', str(self.PORT)])
        
        #instancing object for sender
        self.sender = Sender(self)

        #registering player on server
        self.sender.register_player(self.address, self.name)

        #get players in the game
        self.sender.get_players()

        #wait for changes from core server
        #must be on thread because method for listening use infinity loop
        listen = Thread(target = self.listen, args = ())
        listen.start()

        t_s = Thread(target = self.sender.take_seat, args = (self.address, "1"))
        t_s.start()

        self.game_loop()
        listen.join()

    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)
    
    def draw_player(func):
        def callf(self, news):
            if(news['message']=='take seat'):
                seat = news['seat']
                previous = pygame.image.load("images/take.png")
                if(int(seat)>=4):
                    side = 'left'
                else:
                    side = 'right'
                self.display.blit(self.bg, self.empty_coord[seat], pygame.Rect(self.empty_coord[seat], previous.get_rect().size))
                self.display.blit(pygame.image.load("images/purple_"+side+".png"), self.player_coord[seat])
            return func(self, news)
        return callf

    def move(func):
        def callf(self, news):
            if(news['message']=='move'):
                seat = news['seat']
                self.display.blit(pygame.image.load("images/purple_right.png"), self.player_coord[seat])
            return func(self, news)
        return callf

    def take_button(func):
        def callf(self, news):
            if(news['message']=='take button'):
                seat = news['seat']
                self.display.blit(pygame.image.load("images/take.png"), self.empty_coord[seat])
            return func(self, news)
        return callf

    def init_table(self, seat):
        if(str(seat) in self.players):
            player = self.players[str(seat)]
            player['message'] = 'take seat'
            result = player
        else:
            result = {'message':'take button', 'seat': str(seat)}
        return result

    @move
    @draw_player
    @take_button
    def refresh_table(self, news):
        pygame.display.flip()

    def draw_seats(self, players):
        self.players = players
        news = map(self.init_table, range(1,7))
        for n in list(news):
            self.refresh_table(n)

    def get_address(self):
        HOST = socket.gethostbyname(socket.gethostname()) # get ip address
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind((HOST, 0))
            PORT = s.getsockname()[1]
            return HOST, PORT

    def listen(self):
        # Create the server, binding to localhost and port
        with socketserver.TCPServer((self.HOST, self.PORT), MyTCPHandler(self)) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            server.serve_forever()
        
    def game_loop(self):
        gameExit = False
        while not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True

        pygame.quit()
        quit()