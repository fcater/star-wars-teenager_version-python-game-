import pygame


class Ult(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font('font/msyhbd.ttc', 20)
        self.num = 3
        self.image = pygame.image.load("image/大招.png").convert_alpha()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect = self.image.get_rect()
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)