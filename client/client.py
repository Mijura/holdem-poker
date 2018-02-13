import pygame
from threading import Thread
from traffic import *
import socketserver
from contextlib import closing
import socket
from itertools import takewhile
import functools

class Client:
    
    def __init__(self, name):
        pygame.init()

        self.myfont = pygame.font.Font("myriad_pro.ttf", 15)
        self.name = name
        
        self.buttons = {}
        self.button_args = None

        #set window size, title and bacground image (table)
        self.display = pygame.display.set_mode((800,577))
        pygame.display.set_caption("Texas Hold`em Poker")
        self.bg = pygame.image.load("images/table.png")
        self.display.blit(self.bg, (0, 0))
        pygame.display.flip()
        
        self.player_coord = {'1': (5, 345), '2': (5, 105), '3': (325, 30), '4': (645, 105), '5': (645, 345), '6': (325, 420)}
        self.empty_coord = {'1': (55, 390), '2': (55, 105), '3': (355, 45), '4': (645, 105), '5': (645, 390), '6': (355, 450)}
        self.cards_coord = {'1': (5, 320), '2': (5, 80), '3': (325, 5), '4': (675, 80), '5': (675, 320), '6': (355, 395)}
        self.buttons_coord = {'check': (410, 527), 'call': (410, 527), 'raise': (540, 527), 'bet': (540, 527), 'fold': (670, 527)}
        self.chips_coord = {'1': (190, 325), '2': (190, 150), '3': (400, 120), '4': (590, 150), '5': (590, 325), '6': (400, 360)}
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
        listen = Thread(target = self.listen, args = ())
        listen.start()

        self.game_loop()
        listen.join()

    #draws image with opacity
    def blit_alpha(self, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(self.display, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        self.display.blit(temp, location)
    
    def remove_seat(func):
        def callf(self, news):
            if('draw player' in news):
                seat = news['seat']
                previous = pygame.image.load("images/take.png")
                p_coords = self.empty_coord[seat]
                self.display.blit(self.bg, p_coords, pygame.Rect(p_coords, previous.get_rect().size))
            return func(self, news)
        return callf

    def draw_player(func):
        def callf(self, news):
            if('draw player' in news):
                seat = news['seat']
                previous = pygame.image.load("images/take.png")
                p_coords = self.empty_coord[seat]

                #delete button from dictionary and screen
                if p_coords in self.buttons:
                    del self.buttons[p_coords]

                x, y = self.player_coord[seat]

                name_label = self.myfont.render(news['name'], True, pygame.Color('white'))
                l_size = name_label.get_rect().size
                chips_label = self.myfont.render(str(news['chips'])+' $', True, pygame.Color('white'))
                c_size = chips_label.get_rect().size

                if(int(seat)>=4):
                    side = 'left'
                    l_x = x + 100 - l_size[0]/2
                    c_x = x + 100 - c_size[0]/2    
                else:
                    side = 'right'
                    l_x = x + 50 - l_size[0]/2
                    c_x = x + 50 - c_size[0]/2

                if('on move' in news):
                    color = "green"
                else:
                    color = "purple"
                
                self.display.blit(pygame.image.load("images/"+color+"_"+side+".png"), (x, y))
                
                l_y = y + 15
                c_y = y + 37
                self.display.blit(name_label, (l_x, l_y))
                self.display.blit(chips_label, (c_x, c_y))
            return func(self, news)
        return callf

    def draw_image_part(self, image, coord, size):
        self.display.blit(image, coord, pygame.Rect((0,0), size))

    # creates button and save button args if user click on button (left click)
    def create_button(self, image, coord, action, action_args):

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
    
        x, y = coord
        w,h = image.get_rect().size
        self.display.blit(self.bg, coord, pygame.Rect(coord, image.get_rect().size))
        if x+w>mouse[0] > x and y+h>mouse[1]>y:
            self.display.blit(image, (x, y))
            if(click[0]==1):
                self.button_args = (image, coord, action, action_args)
        else:
            self.blit_alpha(image, (x, y), 210)

    # adds button in dictionary
    def draw_players_cards(func):
        def callf(self, news):
            if('cards' in news):
                seat = news['seat']
                x, y = self.cards_coord[seat]

                p = (60,60) #size of image part
                if(news['address'] == self.address):
                    f, s = news['cards']
                    self.draw_image_part(pygame.image.load("images/cards/"+f+".png"),(x, y), p)
                    self.draw_image_part(pygame.image.load("images/cards/"+s+".png"),(x+60, y), p)
                else:
                    self.draw_image_part(pygame.image.load("images/cards/0.png"),(x, y), p)
                    self.draw_image_part(pygame.image.load("images/cards/0.png"),(x+60, y), p)
            return func(self, news)
        return callf
    
    # adds button in dictionary
    def draw_take_button(func):
        def callf(self, news):
            if('draw take button' in news):
                seat = news['seat']
                key = self.empty_coord[seat]
                value = (pygame.image.load("images/take.png"), 
                         self.empty_coord[seat], 
                         self.sender.take_seat, 
                         (self.address, seat))
                self.buttons[key] = value
            return func(self, news)
        return callf

    def draw_empty_seat(func):
        def callf(self, news):
            if('draw empty seat' in news):
                seat = news['seat']
                coords = self.empty_coord[seat]
                self.display.blit(self.bg, coords, 
                    pygame.Rect(coords, pygame.image.load("images/take.png").get_rect().size))
                        
                self.blit_alpha(pygame.image.load("images/empty.png"), coords, 128)
            return func(self, news)
        return callf

    def group_chips(self, chips_hist):
        chips = [[],[],[],[]]
        i = 0
        for item in chips_hist.items():
            if(i==4):
                i = 0
            chips[i].append(item)
            i+=1
        return chips

    def draw_chips(func):
        def callf(self, news):
            if('stake' in news):
                chips = takewhile(lambda x: x<=news['stake'], self.chips)
                chips = list(chips)
                chips_hist={}
                stake = news['stake']
                seat = news['seat']

                for chip in reversed(chips):
                    i = 0
                    while ((stake-chip)>=0):
                        stake-=chip
                        i+=1
                        chips_hist[chip]=i #histogram : key chip, value count
                    if(stake<1):
                        break
                
                x, y = self.chips_coord[seat]
                start_y = y
                columns = self.group_chips(chips_hist)
                for column in columns:
                    for chips in column:
                        for i in range(0,chips[1]):
                            image = "images/chips/"+str(chips[0])+".png"
                            self.display.blit(pygame.image.load(image), (x, y))
                            y -= 5
                    y = start_y
                    if(int(seat)>=4):
                        x -= 22
                    else:
                        x += 22

            return func(self, news)
        return callf

    # adds bet buttons in dictionary
    def draw_bet_buttons(func):
        def callf(self, news):
            if('on move' in news and news['address']==self.address):
                a = filter(lambda s: 'raise' in s, self.data)
                
                all_raises = list(filter(lambda s: 'raise' in s, self.data))
                #my_raise = list(filter(lambda s: s['address']==self.address, all_raises))
                #re = list(filter(lambda s: s['a']> m, all_raises))
                all_bets = list(filter(lambda s: 'bet' in s, self.data))
                if(all_bets or all_raises):
                    pass
                else:
                    #add chceck button in dict
                    key = self.buttons_coord['check']
                    value = (pygame.image.load("images/check.png"), 
                         key, self.sender.check, ())
                    self.buttons[key] = value
                
                    #add bet button in dict
                    key = self.buttons_coord['bet']
                    value = (pygame.image.load("images/bet.png"), 
                         key, self.sender.bet, ())
                    self.buttons[key] = value

                    #add fold button in dict
                    key = self.buttons_coord['fold']
                    value = (pygame.image.load("images/fold.png"), 
                         key, self.sender.fold, ())
                    self.buttons[key] = value

            return func(self, news)
        return callf

    # creates news dependes seat's state
    # if seat is busy, returns player
    # If seat is not busy, returns message wich said that on this position it's need to be button
    def init_table(self, seat):
        if(str(seat) in self.players):
            player = self.players[str(seat)]
            result = player
        else:
            result = {'draw take button':True, 'seat': str(seat)}
        return result

    def post_take(self, seat):
        if(str(seat) in self.players):
            result = {}
        else:
            result = {'draw empty seat':True, 'seat': str(seat)}
        return result

    @draw_chips
    @remove_seat
    @draw_bet_buttons
    @draw_players_cards
    @draw_player
    @draw_take_button
    @draw_empty_seat
    def refresh_table(self, news):
        pygame.display.flip()

    # create news from list of players and calls method for drawing news
    def draw_seats(self, players):
        self.players = players
        news = map(self.init_table, range(1,7))
        for n in list(news):
            self.refresh_table(n)

    def draw_empty_seats(self, players):
        self.players = players
        news = map(self.post_take, range(1,7))
        for n in list(news):
            self.refresh_table(n)

    #return ip address and free port
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
    
    #Update the display and show the button
    def show_the_buttons(self):
        for v in self.buttons.values():
            self.create_button(v[0], v[1], v[2], v[3])
        pygame.display.flip()

    def game_loop(self):
        gameExit = False
        while not gameExit:
            self.show_the_buttons() #each time, draws all buttons from dictionary
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                
                # if the user releases the mouse button
                # button_args != None - means that user was click mouse left button before
                elif event.type == pygame.MOUSEBUTTONUP and self.button_args != None:
                    #delete button from dictionary and screen
                    
                    if self.button_args[1] in self.buttons:
                        self.display.blit(self.bg, self.button_args[1], 
                            pygame.Rect(self.button_args[1], self.button_args[0].get_rect().size))

                        #remove from screen all bets button
                        for bc in self.buttons_coord.values():
                            self.display.blit(self.bg, bc, 
                            pygame.Rect(bc, pygame.image.load("images/bet.png").get_rect().size))
                        
                        pygame.display.flip()
                        self.buttons = {}

                    #executes saved method in new thread
                    t = Thread(target = self.button_args[2], args = self.button_args[3])
                    t.start()
                    self.button_args = None #resets button args
        pygame.quit()
        quit()