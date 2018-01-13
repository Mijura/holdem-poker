import pygame

def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)
        
pygame.init()

display = pygame.display.set_mode((800,577))
pygame.display.set_caption("Texas Hold`em Poker")
bg = pygame.image.load("images/table.png")
display.blit(bg, (0, 0))
pygame.display.flip()

c0 = pygame.image.load("images/cards/JH.png")
display.blit(c0, (370, 200))

c1 = pygame.image.load("images/cards/AS.png")
display.blit(c1, (300, 200))

c2 = pygame.image.load("images/cards/JH.png")
display.blit(c2, (230, 200))

c3 = pygame.image.load("images/cards/JH.png")
display.blit(c3, (440, 200))

c4 = pygame.image.load("images/cards/JH.png")
display.blit(c4, (510, 200))

display.blit(pygame.image.load("images/green_left.png"), (355, 445))
#display.blit(pygame.image.load("take.png"), (355, 450))
#display.blit(pygame.image.load("e.png"), (355, 45))
#display.blit(pygame.image.load("take.png"), (55, 105))
display.blit(pygame.image.load("images/purple_right.png"), (5, 105))
display.blit(pygame.image.load("images/take.png"), (55, 390))
#display.blit(pygame.image.load("take.png"), (645, 105))
display.blit(pygame.image.load("images/purple_left.png"), (645, 105))
display.blit(pygame.image.load("images/take.png"), (645, 390))

#display.blit(pygame.image.load("check.png"), (600, 500))
display.blit(pygame.image.load("images/fold.png"), (670, 527))
display.blit(pygame.image.load("images/raise.png"), (540, 527))
display.blit(pygame.image.load("images/check.png"), (410, 527))

image = "images/chips/1000.png"
image2 = "images/chips/100.png"
display.blit(pygame.image.load(image), (190, 150))
display.blit(pygame.image.load(image), (190, 145))
display.blit(pygame.image.load(image), (190, 140))
display.blit(pygame.image.load(image), (190, 135))
display.blit(pygame.image.load(image), (190, 130))
display.blit(pygame.image.load(image), (190, 125))
display.blit(pygame.image.load(image), (190, 120))
display.blit(pygame.image.load(image), (190, 115))
display.blit(pygame.image.load(image), (190, 110))
display.blit(pygame.image.load(image), (190, 105))
display.blit(pygame.image.load(image), (190, 100))
display.blit(pygame.image.load(image), (190, 95))
display.blit(pygame.image.load(image), (215, 150))
display.blit(pygame.image.load(image), (215, 145))
display.blit(pygame.image.load(image2), (175, 165))
display.blit(pygame.image.load(image2), (175, 160))
display.blit(pygame.image.load(image2), (175, 155))
display.blit(pygame.image.load(image2), (175, 150))

blit_alpha(display, pygame.image.load("images/empty.png"), (355, 45), 128)

pygame.display.flip()

gameExit = False

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            #bg = pygame.image.load("AS.png")
            #display.blit(bg, (440, 200))
            display.blit(bg, (440, 200), pygame.Rect(440, 200, 60, 85))
            pygame.display.flip()

pygame.quit()
quit()
