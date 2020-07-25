import pygame


class MyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("image/主角飞机.png").convert_alpha()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = self.width/2 - 18, self.height - 50
        self.speed = 10
        self.active = True
        self.invincible = False
        # self.mask = pygame.mask.from_surface(self.image)

    def moveup(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def movedown(self):
        if self.rect.bottom < self.height - 50:
            self.rect.bottom += self.speed
        else:
            self.rect.bottom = self.height - 50

    def moveleft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveright(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width

    def reset(self):
        self.active = True
        self.invincible = True
        self.rect.left, self.rect.bottom = self.width / 2 - 18, self.height - 50