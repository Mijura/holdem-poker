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