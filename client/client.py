import pygame
from threading import Thread, Lock
from traffic import *
import socketserver
from contextlib import closing
import socket
from itertools import takewhile
from widgets import *
import functools
import abc

class Client:
    
    def __init__(self, name):
        pygame.init()

        self.myfont = pygame.font.Font("myriad_pro.ttf", 15)
        self.name = name
        
        self.buttons = []
        self.table = {}
        self.thread_lock = Lock()
        self.last_clicked_button = None
        self.button_args = None

        #set window size, title and bacground image (table)
        self.display = pygame.display.set_mode((800,577))
        pygame.display.set_caption("Texas Hold`em Poker")
        self.bg = pygame.image.load("images/table.png")
        self.display.blit(self.bg, (0, 0))
        self.slider = Slider()
        self.show_slider = False

        pygame.display.flip()
        
        self.player_coord = {1: (5, 345), 2: (5, 105), 3: (325, 30), 4: (645, 105), 5: (645, 345), 6: (325, 420)}
        self.empty_coord = {1: (55, 390), 2: (55, 105), 3: (355, 45), 4: (645, 105), 5: (645, 390), 6: (355, 450)}
        self.cards_coord = {1: (5, 320), 2: (5, 80), 3: (325, 5), 4: (675, 80), 5: (675, 320), 6: (355, 395)}
        self.buttons_coord = {'check': (410, 527), 'call': (410, 527), 'raise': (540, 527), 'bet': (540, 527), 'fold': (670, 527)}
        self.chips_coord = {1: (190, 325), 2: (190, 150), 3: (400, 110), 4: (590, 150), 5: (590, 325), 6: (400, 370)}
        self.chips = [1, 5, 10, 25, 50, 100, 200, 500, 1000]
        self.stake_keys = ['bet','raise','call','big blind', 'small blind']

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
        self.listen_thread = Thread(target = self.listen, args = ())
        self.listen_thread.start()

        self.game_loop()

    # creates button and save button args if user click on button (left click)
    def create_button(self, image, coord, action, action_args, type):
        if type=='raise' or type=='bet':
            myfont = pygame.font.Font("myriad_pro.ttf", 15)
            label = myfont.render(str(round(self.slider.val)), True, (255,255,255))
            l_size = label.get_rect().size
            self.display.blit(label, ((540 + 60 - l_size[0]/2), 547))

    # adds bet buttons in dictionary
    def draw_bet_buttons(func):
        def callf(self, news):
            if('on move' in news and news['address']==self.address):
                
                #add bet button in dict
                key = self.buttons_coord['bet']
                value = (pygame.image.load("images/bet.png"), key, self.sender.bet, (), 'bet')
                self.thread_lock.acquire()
                self.buttons[key] = value
                self.thread_lock.release()

                #add fold button in dict
                key = self.buttons_coord['fold']
                value = (pygame.image.load("images/fold.png"), key, self.sender.fold, (), 'fold')
                self.thread_lock.acquire()
                self.buttons[key] = value
                self.thread_lock.release()

                #slider
                maxi = 0
                for player in self.data: #search player who whas max chips
                    if(player['address']!=self.address):
                        if player['chips']>maxi:
                            maxi = player['chips']

                if(maxi>news['chips']): #if current player has less chips
                    maxi = news['chips']

                self.slider.maxi = maxi
                self.slider.mini = 0
                self.slider.val = 0
                self.show_slider = True

            return func(self, news)
        return callf

    # returns player's stake
    def get_stake(self, player):
        return player['stake']

    # returns True if all elements of list are equal, otherwise returns False
    def check_equal(self, lst):
        return lst[1:] == lst[:-1]

    # adds check button in dictionary
    def draw_call_button(func):
        def callf(self, news):
            if('on move' in news and news['address']==self.address):
                stakes = list(map(self.get_stake, self.data))
                if self.check_equal(stakes):
                    #add chceck button in dict
                    key = self.buttons_coord['check']
                    value = (pygame.image.load("images/check.png"), 
                        key, self.sender.check, (), 'check')
                    self.thread_lock.acquire()
                    self.buttons[key] = value
                    self.thread_lock.release()
            return func(self, news)
        return callf
    
    # adds check button in dictionary
    def draw_check_button(func):
        def callf(self, news):
            if('on move' in news and news['address']==self.address):
                stakes = list(map(self.get_stake, self.data))
                if self.check_equal(stakes):
                    #add chceck button in dict
                    key = self.buttons_coord['check']
                    value = (pygame.image.load("images/check.png"), 
                        key, self.sender.check, (), 'check')
                    self.thread_lock.acquire()
                    self.buttons[key] = value
                    self.thread_lock.release()
            return func(self, news)
        return callf

    # if seat is busy, returns player
    # if seat is not busy, returns message wich said that on this position it's need to be "take button"
    def player_or_take(self, seat):
        if(str(seat) in self.players):
            player = self.players[str(seat)]
            return player
        else:
            return {'set take button':True, 'seat': str(seat)}

    def post_take(self, seat):
        if(str(seat) in self.players):
            player = self.players[str(seat)]
            return {}
        else:
            return {'set empty seat':True, 'seat': str(seat)}

    def set_player(func):
        def callf(self, news):
            if('set player' in news):
                seat = int(news['seat'])
                self.thread_lock.acquire()
                if seat in self.table:
                    self.table[seat].erase()
                self.table[seat] = Player(self.player_coord[seat], seat, news['name'], news['chips'], 
                        news['on move'], news['bet'], news['cards'], news['address'], self)
                self.thread_lock.release()
            return func(self, news)
        return callf

    def set_empty_seat(func):
        def callf(self, news):
            if('set empty seat' in news):
                seat = int(news['seat'])
                self.thread_lock.acquire()
                if seat in self.table:
                    self.table[seat].erase()
                self.table[seat] = EmptySeat(self.empty_coord[seat], seat, self)
                self.thread_lock.release()
            return func(self, news)
        return callf

    def set_take_button(func):
        def callf(self, news):
            if('set take button' in news):
                seat = int(news['seat'])
                self.thread_lock.acquire()
                if seat in self.table:
                    self.table[seat].erase()
                self.table[seat] = TakeSeatButton(self.empty_coord[seat], seat, self)
                self.thread_lock.release()
            return func(self, news)
        return callf

    #@draw_bet_buttons
    #@draw_call_button
    #@draw_check_button
    @set_player
    @set_take_button
    @set_empty_seat
    def refresh_table(self, news):
        pygame.display.flip()

    def init_table(self, players):
        self.players = players
        seats = map(self.player_or_take, range(1,7))
        for seat in seats:
            self.refresh_table(seat)

    def draw_empty_seats(self, players):
        self.players = players
        empty_seats = map(self.post_take, range(1,7))
        for seat in empty_seats:
            self.refresh_table(seat)
        
    #return ip address and free port
    def get_address(self):
        HOST = socket.gethostbyname(socket.gethostname()) # get ip address
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind((HOST, 0))
            PORT = s.getsockname()[1]
            return HOST, PORT

    def listen(self):
        # Create the server, binding to localhost and port
        with socketserver.TCPServer((self.HOST, self.PORT), MyTCPHandler(self)) as self.server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            self.server.serve_forever()
    
    #Update the display
    def update_table(self):
        self.thread_lock.acquire()
        for widget in self.table.values():
            widget.draw()
        self.thread_lock.release()
        pygame.display.flip()

    def game_loop(self):
        gameExit = False
        while not gameExit:
            self.update_table() #each time, draws all seats
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.server.shutdown()
                    self.server.server_close()
                    gameExit = True
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.show_slider and self.slider.button_rect.collidepoint(pos):
                        self.slider.hit = True
                    
                # if the user click on some button
                elif event.type == pygame.MOUSEBUTTONUP and self.last_clicked_button:

                    t = Thread(target = self.last_clicked_button.mouse_click, args = {})
                    t.start()
                    
                    self.last_clicked_button.erase()

                    self.thread_lock.acquire()
                    del self.table[self.last_clicked_button.seat_number]
                    self.thread_lock.release()

                    self.last_clicked_button = None
                    self.buttons = []

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.slider.hit = False

            if self.slider.hit:
                self.slider.move()

            if self.show_slider:
                self.slider.draw(self.display)
                
            pygame.display.flip()

        pygame.quit()
        quit()