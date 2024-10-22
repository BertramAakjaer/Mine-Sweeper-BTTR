import pygame

class Field:
    def __init__(self, screen, number_photos, x, y, width, height):
        self.screen = screen
        self.number_photos = number_photos

        self.flag = pygame.image.load(r"src\media\flag.png")
        self.bombImg = pygame.image.load(r"src\media\bomb.png")


        self.clicked = False
        self.flag_active = False
        self.hovering = False
        self.bomb = False
        self.bombs_near = 0

        self.hoverCol = (0, 117, 202)
        self.clickedCol = (0, 45, 86)

        self.unclickedCol = (0, 85, 163)
        self.bombCol = (255, 0, 0)

        self.width = width
        self.height = height

        self.rect = pygame.Rect(x, y, width, height)

    def increase_bombs_near(self):
        self.bombs_near += 1



    def draw(self):


        if self.clicked:
            if self.bomb:
                self.screen.fill(self.bombCol, self.rect)
                image = pygame.transform.scale(self.bombImg, (self.width, self.height))
                self.screen.blit(image, self.rect)
                return
            
            self.screen.fill(self.clickedCol, self.rect)

            if  self.bombs_near > 0:
                image = pygame.transform.scale(self.number_photos[self.bombs_near - 1], (self.width, self.height))
                self.screen.blit(image, self.rect)
        
        elif self.hovering:
            self.screen.fill(self.hoverCol, self.rect)
            self.hovering = False

        else:
            self.screen.fill(self.unclickedCol, self.rect)

        if self.flag_active:
            image = pygame.transform.scale(self.flag, (self.width, self.height))
            self.screen.blit(image, self.rect)
        