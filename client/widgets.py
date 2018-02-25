import abc
import pygame
from itertools import takewhile

class Widget(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def erase(self):
        pass

class Button(Widget, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def erase(self):
        pass
    
    @abc.abstractmethod
    def mouse_click(self):
        pass

#draws image with opacity
def blit_alpha(display, source, location, opacity):
    #negative = set(map(lambda x: -1*x, location))
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(display, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    display.blit(temp, location)

class TakeSeatButton(Button):

    def __init__(self, position, seat_number, client):
        self.position = position
        self.seat_number = seat_number
        self.image = pygame.image.load("images/take.png")
        self.parent = client
        self.kind = 'seat button'

    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        x, y = self.position
        w, h = self.image.get_rect().size

        self.erase()
        
        if x+w>mouse[0]>x and y+h>mouse[1]>y:
            self.parent.display.blit(self.image, self.position)
            if(click[0]==1):
                self.parent.last_clicked_button = self
        else:

            blit_alpha(self.parent.display, self.image, self.position, 210)
                
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))

    def mouse_click(self):
        self.parent.sender.take_seat(self.parent.address, self.seat_number)

class CheckButton(Button):

    def __init__(self, position, seat_number, client):
        self.position = position
        self.image = pygame.image.load("images/check.png")
        self.seat_number = seat_number
        self.parent = client
        self.kind = 'bet button'

    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        x, y = self.position
        w, h = self.image.get_rect().size

        self.erase()
        if x+w>mouse[0]>x and y+h>mouse[1]>y:
            self.parent.display.blit(self.image, self.position)
            if(click[0]==1):
                self.parent.last_clicked_button = self
        else:
            blit_alpha(self.parent.display, self.image, self.position, 210)
                
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))

    def mouse_click(self):
        self.parent.sender.check()

class FoldButton(Button):

    def __init__(self, position, client):
        self.position = position
        self.image = pygame.image.load("images/fold.png")
        self.parent = client
        self.kind = 'bet button'

    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        x, y = self.position
        w, h = self.image.get_rect().size

        self.erase()
        if x+w>mouse[0]>x and y+h>mouse[1]>y:
            self.parent.display.blit(self.image, self.position)
            if(click[0]==1):
                self.parent.last_clicked_button = self
        else:
            blit_alpha(self.parent.display, self.image, self.position, 210)
                
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))

    def mouse_click(self):
        self.parent.sender.fold()

class CallButton(Button):

    def __init__(self, position, call_value, seat_number, client):
        self.position = position
        self.image = pygame.image.load("images/call.png")
        self.call_value = call_value
        self.seat_number = seat_number
        self.parent = client
        self.kind = 'bet button'

        image_size = self.image.get_rect().size
        self.label = client.myfont.render(str(round(call_value)), True, (255,255,255))
        l_size = self.label.get_rect().size

        x, y = position
        label_x = x + image_size[0]/2 - l_size[0]/2
        label_y = y + image_size[1]/2
        self.label_position = (label_x, label_y)
        
        
    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        x, y = self.position
        w, h = self.image.get_rect().size

        self.erase()
        if x+w>mouse[0]>x and y+h>mouse[1]>y:
            self.parent.display.blit(self.image, self.position)
            if(click[0]==1):
                self.parent.last_clicked_button = self
        else:
            blit_alpha(self.parent.display, self.image, self.position, 210)

        self.parent.display.blit(self.label, self.label_position)
                
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))

    def mouse_click(self):
        self.parent.table[int(self.seat_number)].call(self.call_value)
        self.parent.sender.call(self.call_value, self.seat_number)

class RaiseButton(Button):

    def __init__(self, position, slider, client):
        self.position = position
        self.image = pygame.image.load("images/raise.png")
        self.slider = slider
        self.parent = client
        self.kind = 'bet button'

        self.image_size = self.image.get_rect().size
        
    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        x, y = self.position
        w, h = self.image.get_rect().size

        self.erase()
        if x+w>mouse[0]>x and y+h>mouse[1]>y:
            self.parent.display.blit(self.image, self.position)
            if(click[0]==1):
                self.parent.last_clicked_button = self
        else:
            blit_alpha(self.parent.display, self.image, self.position, 210)

        
        label = self.parent.myfont.render(str(round(self.slider.val)), True, (255,255,255))
        l_size = label.get_rect().size

        x, y = self.position
        label_x = x + self.image_size[0]/2 - l_size[0]/2
        label_y = y + self.image_size[1]/2
        label_position = (label_x, label_y)

        self.parent.display.blit(label, label_position)
                
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))

    def mouse_click(self):
        self.parent.sender.raise_to(self.slider.val)

class BetButton(Button):

    def __init__(self, position, slider, client):
        self.position = position
        self.image = pygame.image.load("images/bet.png")
        self.slider = slider
        self.parent = client
        self.kind = 'bet button'

        self.image_size = self.image.get_rect().size
        
    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        x, y = self.position
        w, h = self.image.get_rect().size

        self.erase()
        if x+w>mouse[0]>x and y+h>mouse[1]>y:
            self.parent.display.blit(self.image, self.position)
            if(click[0]==1):
                self.parent.last_clicked_button = self
        else:
            blit_alpha(self.parent.display, self.image, self.position, 210)

        
        label = self.parent.myfont.render(str(round(self.slider.val)), True, (255,255,255))
        l_size = label.get_rect().size

        x, y = self.position
        label_x = x + self.image_size[0]/2 - l_size[0]/2
        label_y = y + self.image_size[1]/2
        label_position = (label_x, label_y)

        self.parent.display.blit(label, label_position)
                
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))

    def mouse_click(self):
        self.parent.sender.bet_to(self.slider.val)
    
class Slider(Widget):
    
    def __init__(self, client):
        
        self.parent = client
        
        self.WHITE = (255, 255, 255)
        self.TRANS = (1, 1, 1)

        self.val = 0  # start value
        self.maxi = 0  # maximum at slider position right
        self.mini = 0  # minimum at slider position left
        self.xpos = 540  # x-location on screen
        self.ypos = 495 # y-location on screen
        self.position = (self.xpos, self.ypos)

        self.hit = False  # the hit attribute indicates slider movement due to mouse interaction

        self.surf_size = (120, 25)
        # button surface #
        self.button_surf = pygame.surface.Surface((20, 20))
        self.button_surf.fill(self.TRANS)
        self.button_surf.set_colorkey(self.TRANS)
        self.button_surf.blit(pygame.image.load("images/slider_button.png"),(0,0))


    def set_slider_params(self, params):
        self.maxi = params[1]
        self.mini = params[0]
        self.val = params[0]

    def draw(self):
        self.erase()
        self.surf = pygame.surface.Surface(self.surf_size, pygame.SRCALPHA, 32)
        self.surf.blit(pygame.image.load("images/slider_scale.png"), (0,8))

        pos = (10 + int ((self.val - self.mini) / (self.maxi - self.mini) * 100), 13)
        self.button_rect = self.button_surf.get_rect(center=pos)
        self.surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)  # move of button box to correct screen position

        self.parent.display.blit(self.surf, (self.xpos, self.ypos))
    
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.surf_size))
    
    def move(self):
        """
        The dynamic part; reacts to movement of the slider button.
        """
        self.val = (pygame.mouse.get_pos()[0] - self.xpos - 10) / 100 * (self.maxi - self.mini) + self.mini
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi

class Player(Widget):

    def __init__(self, position, seat_number, name, chips, on_move, bet, cards, address, in_game, client):
        self.position = position
        self.seat_number = seat_number
        self.name = name
        self.chips = chips
        self.on_move = on_move
        self.parent = client
        self.address = address
        self.kind = 'player widget'
        self.in_game = in_game

        self.blink = 0        
        self.set_cards(cards)
        self.calculate_side()
        self.set_name_label()
        self.set_chips_label()
        self.image = pygame.image.load("images/purple_"+self.side+".png")
        self.bet = Chips(client.chips_coord[seat_number], bet, seat_number, client)

    def set_chips_label(self):
        x, y = self.position
        self.chips_label = self.parent.myfont.render(str(self.chips)+' $', True, pygame.Color('white'))
        c_size = self.chips_label.get_rect().size
        if(self.seat_number >= 4):
            self.c_x = x + 100 - c_size[0] / 2
        else:
            self.c_x = x + 50 - c_size[0] / 2
        self.c_y = y + 37

    def set_name_label(self):
        x, y = self.position
        self.name_label = self.parent.myfont.render(self.name, True, pygame.Color('white'))
        l_size = self.name_label.get_rect().size
        if(self.seat_number >= 4):
            self.l_x = x + 100 - l_size[0] / 2
        else:
            self.l_x = x + 50 - l_size[0] / 2
        self.l_y = y + 15

    def calculate_side(self):
        if(self.seat_number >= 4):
            self.side = 'left'
        else:
            self.side = 'right'

    def set_cards(self, cards):
        self.cards = []
        x, y = self.parent.cards_coord[self.seat_number]
        for card in cards:
            self.cards.append(PlayerCard((x, y), card, self.address, self.parent))
            x += 60

    def draw(self):

        self.erase()

        for card in self.cards:
            card.draw()

        if self.on_move:
            if self.blink % 2:
                self.image = pygame.image.load("images/green_"+self.side+".png")
                if self.blink == 251:
                    self.blink = 0
            else:
                self.image = pygame.image.load("images/white_"+self.side+".png")
                if self.blink == 250:
                    self.blink = 1
            self.blink += 2
        else:
            self.image = pygame.image.load("images/purple_"+self.side+".png")
        
        if self.in_game:
            self.parent.display.blit(self.image, self.position)
            self.parent.display.blit(self.name_label, (self.l_x, self.l_y))
            self.parent.display.blit(self.chips_label, (self.c_x, self.c_y))
        else:
            blit_alpha(self.parent.display, self.image, self.position, 128)
            blit_alpha(self.parent.display, self.name_label, (self.l_x, self.l_y), 128)
            blit_alpha(self.parent.display, self.chips_label, (self.c_x, self.c_y), 128)

        
        
        self.bet.draw()
    
    def erase(self):
        for card in self.cards:
            card.erase()
        
        self.bet.erase()
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))

    def call(self, call_value):
        self.chips -= call_value
        self.set_chips_label()
        self.bet.total += call_value
        self.bet.set_new_chips(self.bet.total)
        self.on_move = False

class EmptySeat(Widget):

    def __init__(self, position, seat_number, client):
        self.position = position
        self.seat_number = seat_number
        self.image = pygame.image.load("images/empty.png")
        self.parent = client
        self.kind = 'seat widget'

    def draw(self):
        self.erase()
        blit_alpha(self.parent.display, self.image, self.position, 128)
                
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))

class Chips(Widget):

    def __init__(self, position, total, seat_number, client):
        self.position = position
        self.parent = client
        self.total = total
        self.seat_number = seat_number
        
        self.set_new_chips(total)
        
    def create_chips_histogram(self, total):
        chips = takewhile(lambda x: x<=total, self.parent.chips)
        chips = list(chips)
        chips_hist={}

        for chip in reversed(chips):
            i = 0
            while ((total-chip)>=0):
                total-=chip
                i+=1
                chips_hist[chip]=i #histogram : key chip, value count
            if(total<1):
                break
        
        return chips_hist
    
    def group_chips(self):
        chips = [[],[],[],[]]
        i = 0
        for item in self.chips_histogram.items():
            if(i==4):
                i = 0
            chips[i].append(item)
            i+=1
        return chips

    def add_chips(self):
        self.chips = []

        x, y = self.position
        start_y = y
        for column in self.columns:
            for chips in column:
                for i in range(0,chips[1]):
                    self.chips.append(Chip(chips[0], (x, y), self.parent))
                    y -= 5
            y = start_y
            if(int(self.seat_number)>=4):
                x -= 22
            else:
                x += 22

    def set_new_chips(self, total):
        self.chips_histogram = self.create_chips_histogram(total)
        self.columns = self.group_chips()
        self.add_chips()

    def draw(self):
        for chip in self.chips:
            chip.draw()
                
    def erase(self):
        for chip in self.chips:
            chip.erase()

class Chip(Widget):

    def __init__(self, count, position, client):
        self.count = count
        self.position = position
        self.parent = client
        self.image = pygame.image.load("images/chips/"+str(count)+".png")

    def draw(self):
        self.parent.display.blit(self.image, self.position)
                
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))
    
class PlayerCard(Widget):

    def __init__(self, position, card, address, client):
        self.position = position
        self.card = card
        self.parent = client
        
        if client.address == address:
            self.image = pygame.image.load("images/cards/"+card+".png")
        else:
            self.image = pygame.image.load("images/cards/0.png")

    def draw_image_part(self, image, coord, size):
        self.parent.display.blit(image, coord, pygame.Rect((0,0), size))

    def draw(self):
        self.draw_image_part(self.image, self.position, (60,60))
                
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))
