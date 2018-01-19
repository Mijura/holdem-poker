import pygame as pg
from client import Client

pg.init()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)
myfont = pg.font.Font("myriad_pro.ttf", 15)
myfont2 = pg.font.Font("myriad_pro.ttf", 24)

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = myfont2.render(text, True, self.color)
        self.active = False
        self.end = False
        self.max = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                length = len(self.text)
                if event.key == pg.K_RETURN:
                    if(self.text and length<9):
                        self.end = True
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.txt_surface = myfont2.render(self.text, True, self.color)
                    if len(self.text)<9:
                        self.max=False
                else:
                    char = event.unicode
                    if(char.isalpha() or char.isdigit()):
                        if length < 9:
                            self.text += char
                            if length == 8:
                                self.max = True
                    self.txt_surface = myfont2.render(self.text, True, self.color)
                    

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


class Username:

    def __init__(self):
        self.screen = pg.display.set_mode((320, 240))
        pg.display.set_caption("Texas Hold`em Poker")
        
        
    def update(self):
        clock = pg.time.Clock()
        
        input_box = InputBox(60, 105, 200, 30)
        self.done = False
        self.quit = False
        self.text = input_box.text

        while not self.done:
        
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.done = True
                    self.quit = True
                else:
                    input_box.handle_event(event)

            if input_box.end:
                self.done = True

            self.screen.fill((30, 30, 30))
            label = myfont.render("Enter name:", True, COLOR_INACTIVE)
            self.screen.blit(label, (60, 80))

            input_box.draw(self.screen)
            
            if(input_box.max):
                label = myfont.render("The name can have max 8 characters!", True, COLOR_INACTIVE)
                self.screen.blit(label, (60, 150))

            self.text = input_box.text
            pg.display.flip()
            clock.tick(30)
        pg.quit()


if __name__ == '__main__':
    u = Username()
    u.update()
    if not u.quit:
        c = Client(u.text)
        
