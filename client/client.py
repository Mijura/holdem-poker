import pygame
from threading import Thread
from listener import *

class Client:
    
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((800,577))
        pygame.display.set_caption("Texas Hold`em Poker")
        self.bg = pygame.image.load("images/table.png")
        self.display.blit(self.bg, (0, 0))
        pygame.display.flip()
        
        self.listener = Listener(self)
        listen = Thread(target = self.listener.listen, args = ())
        listen.start()

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
    
    def take_seat(func):
        def callf(self, news):
            if(news['message']=='take seat'):
                self.display.blit(pygame.image.load("images/purple_right.png"), (5, 105))
            return func(self, news)
        return callf

    def move(func):
        def callf(self, news):
            if(news['message']=='move'):
                self.display.blit(pygame.image.load("images/purple_right.png"), (5, 105))
            return func(self, news)
        return callf

    @move
    @take_seat
    def refresh_table(self, news):
        pygame.display.flip()
        
    def game_loop(self):
        gameExit = False
        while not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.listener.done = True
                    gameExit = True

        pygame.quit()
        quit()
        
if __name__ == "__main__":
    c = Client()
    