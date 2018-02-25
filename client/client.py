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
        self.slider = Slider(self)
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
    
    # returns player's stake
    def get_bet(self, player):
        return player['bet']

    # returns True if all elements of list are equal, otherwise returns False
    def check_equal(self, lst):
        return lst[1:] == lst[:-1]

    def find_max_chips(self):
        max_chips = 0
        for player in self.data: #search player who whas max chips
            if(player['address'] != self.address):
                if player['chips'] > max_chips:
                    max_chips = player['chips'] + player['bet']
        return max_chips

    def find_max_bet(self):
        max_bet = 0
        for player in self.data: #search player who whas max chips
            if(player['address'] != self.address):
                if player['bet'] > max_bet:
                    max_bet = player['bet']
        return max_bet

    def determine_call_value(self, chips, max_bet, bet):
        call_value = max_bet - bet 
        if(call_value > chips): #if current player has less chips
            return chips
        return call_value
    """
    def bet_slider_params(self, chips, bet):
        max_chips = self.find_max_chips()
        if(max_chips > chips): #if current player has less chips
            max_chips = chips 
        return (1, max_chips + bet)"""
    # adds bet button to list
    def set_bet_button(func):
        def callf(self, news):
            if('on move' in news and news['on move']==True and news['address']==self.address):
                bets = list(map(self.get_bet, self.data))
                if self.check_equal(bets):
                    if news['chips'] > 1:
                        self.slider.set_slider_params((news['bet'] + 1, news['chips'] + news['bet']))
                        self.show_slider = True
                        self.thread_lock.acquire()
                        self.buttons.append(BetButton(self.buttons_coord['bet'], self.slider, self))
                        self.thread_lock.release()
            return func(self, news)
        return callf


    # adds raise button to list and show slider
    def set_raise_button(func):
        def callf(self, news):
            if('on move' in news and news['on move']==True and news['address']==self.address):
                bets = list(map(self.get_bet, self.data))
                if not self.check_equal(bets):
                    max_bet = self.find_max_bet()
                    down_border = max_bet + 1
                    up_border = self.find_max_chips()
                    bet_difference = max_bet - news['bet']
                    if news['chips'] > bet_difference and up_border >= down_border:
                        self.slider.set_slider_params((down_border, up_border))
                        if up_border > down_border:
                            self.show_slider = True
                        self.thread_lock.acquire()
                        self.buttons.append(RaiseButton(self.buttons_coord['raise'], self.slider, self))
                        self.thread_lock.release()
            return func(self, news)
        return callf

    # adds call button to list
    def set_call_button(func):
        def callf(self, news):
            if('on move' in news and news['on move']==True and news['address']==self.address):
                bets = list(map(self.get_bet, self.data))
                if not self.check_equal(bets):
                    max_bet = self.find_max_bet()
                    call_value = self.determine_call_value(news['chips'], max_bet, news['bet'])
                    self.thread_lock.acquire()
                    self.buttons.append(CallButton(self.buttons_coord['call'], call_value, news['seat'], self))
                    self.thread_lock.release()
            return func(self, news)
        return callf

    # adds fold button to list
    def set_fold_button(func):
        def callf(self, news):
            if('on move' in news and news['on move']==True and news['address']==self.address):
                bets = list(map(self.get_bet, self.data))
                if not self.check_equal(bets):
                    self.thread_lock.acquire()
                    self.buttons.append(FoldButton(self.buttons_coord['fold'], self))
                    self.thread_lock.release()
            return func(self, news)
        return callf

    # adds check button to list
    def set_check_button(func):
        def callf(self, news):
            if('on move' in news and news['on move']==True and news['address']==self.address):
                bets = list(map(self.get_bet, self.data))
                if self.check_equal(bets):
                    self.thread_lock.acquire()
                    self.buttons.append(CheckButton(self.buttons_coord['check'], news['seat'], self))
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
                        news['on move'], news['bet'], news['cards'], news['address'], news['in game'], self)
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

    @set_bet_button
    @set_raise_button
    @set_call_button
    @set_fold_button
    @set_check_button
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

    def is_button_clicked(self):
        pos = pygame.mouse.get_pos()
        for button in self.buttons:
            r = pygame.Rect(button.position, button.image.get_rect().size)
            if button.kind == 'bet button' and r.collidepoint(pos):
                return True
        for widget in self.table.values():
            r = pygame.Rect(widget.position, widget.image.get_rect().size)
            if widget.kind == 'seat button' and r.collidepoint(pos):
                return True
        return False
    
    #Update the display
    def update_table(self):
        self.thread_lock.acquire()
        for widget in self.table.values():
            widget.draw()
        self.thread_lock.release()
        pygame.display.flip()
    
    def draw_bet_buttons(self):
        for button in self.buttons:
            button.draw()

    def game_loop(self):
        gameExit = False
        while not gameExit:
            self.update_table() #each time, draws all seats
            self.draw_bet_buttons()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.server.shutdown()
                    self.server.server_close()
                    gameExit = True
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.show_slider and self.slider.button_rect.collidepoint(pos):
                        self.slider.hit = True
                    
                    self.button_clicked = self.is_button_clicked()
                    
                # if the user click on some button
                elif event.type == pygame.MOUSEBUTTONUP and self.button_clicked:

                    t = Thread(target = self.last_clicked_button.mouse_click, args = {})
                    t.start()
                    
                    self.last_clicked_button.erase()

                    if(self.last_clicked_button.kind == 'seat button'):
                        self.thread_lock.acquire()
                        del self.table[self.last_clicked_button.seat_number]
                        self.thread_lock.release()
                    elif(self.last_clicked_button.kind == 'bet button'):
                        for button in self.buttons:
                            button.erase()
                        self.buttons = []
                        self.slider.erase()
                        self.show_slider = False

                    self.last_clicked_button = None
                    

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.slider.hit = False

            if self.slider.hit:
                self.slider.move()

            if self.show_slider:
                self.slider.draw()
                
            pygame.display.flip()

        pygame.quit()
        quit()