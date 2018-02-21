import abc
import pygame

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
    
class Slider(Widget):
    def __init__(self):
        self.WHITE = (255, 255, 255)
        self.TRANS = (1, 1, 1)

        self.val = 0  # start value
        self.maxi = 0  # maximum at slider position right
        self.mini = 0  # minimum at slider position left
        self.xpos = 540  # x-location on screen
        self.ypos = 495 # y-location on screen

        self.hit = False  # the hit attribute indicates slider movement due to mouse interaction

        # button surface #
        self.button_surf = pygame.surface.Surface((20, 20))
        self.button_surf.fill(self.TRANS)
        self.button_surf.set_colorkey(self.TRANS)
        self.button_surf.blit(pygame.image.load("images/slider_button.png"),(0,0))

    def draw(self, screen):
        screen.blit(pygame.image.load("images/table.png"), (self.xpos, self.ypos), pygame.Rect((self.xpos, self.ypos),(120, 25)))
        surf = pygame.surface.Surface((120, 25), pygame.SRCALPHA, 32)
        surf.blit(pygame.image.load("images/slider_scale.png"),(0,8))

        pos = (10+int((self.val-self.mini)/(self.maxi-self.mini)*100), 13)
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)  # move of button box to correct screen position

        screen.blit(surf, (self.xpos, self.ypos))
    
    def erase(self):
        pass
    
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

    def __init__(self, position, seat_number, name, chips, on_move, bet, client):
        self.position = position
        self.seat_number = seat_number
        self.name = name
        self.chips = chips
        self.on_move = on_move
        self.bet = bet
        self.parent = client

    def draw(self):
        x, y = self.position

        name_label = self.parent.myfont.render(self.name, True, pygame.Color('white'))
        l_size = name_label.get_rect().size
        chips_label = self.parent.myfont.render(str(self.chips)+' $', True, pygame.Color('white'))
        c_size = chips_label.get_rect().size

        if(self.seat_number >= 4):
            side = 'left'
            l_x = x + 100 - l_size[0]/2
            c_x = x + 100 - c_size[0]/2    
        else:
            side = 'right'
            l_x = x + 50 - l_size[0]/2
            c_x = x + 50 - c_size[0]/2

        if(self.on_move):
            color = "green"
        else:
            color = "purple"
        
        self.image = pygame.image.load("images/"+color+"_"+side+".png")
        self.erase()
        self.parent.display.blit(self.image, self.position)
                
        l_y = y + 15
        c_y = y + 37
        self.parent.display.blit(name_label, (l_x, l_y))
        self.parent.display.blit(chips_label, (c_x, c_y))
    
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))

class EmptySeat(Widget):

    def __init__(self, position, seat_number, client):
        self.position = position
        self.seat_number = seat_number
        self.image = pygame.image.load("images/empty.png")
        self.parent = client

    def draw(self):
        self.erase()
        blit_alpha(self.parent.display, self.image, self.position, 128)
                
    def erase(self):
        self.parent.display.blit(self.parent.bg, self.position, pygame.Rect(self.position, self.image.get_rect().size))