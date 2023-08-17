import pygame

# SPRITE STUFF
class LoadSpritesheet:
    def __init__(self, image, spritesizex,spritesizey,scale):
        self.sheet = image
        self.spritesizex = spritesizex
        self.spritesizey = spritesizey
        self.scale = scale
        self.images = []

        counterx,countery = 0,0
        num_of_frames = int((self.sheet.get_width()/self.spritesizex) * (self.sheet.get_height()/spritesizey))
        for _ in range(num_of_frames):
            self.images.append(self.get_image(counterx, countery, self.spritesizex, self.spritesizey, self.scale))
            counterx += 1
            if counterx >= self.sheet.get_width()/self.spritesizex:
                countery += 1
                counterx = 0

    def get_image(self, framex, framey, width, height, scale):
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), ((framex * width), (framey * width), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))

        return image

class PlayAnimation(pygame.sprite.Sprite):
    def __init__(self, x, y, spritearray, scale, repeat):
        pygame.sprite.Sprite.__init__(self)
        self.explode_last_update = pygame.time.get_ticks()
        self.spritearray = spritearray
        self.index = 0
        self.image = self.spritearray[self.index]
        self.rect = self.image.get_rect(center = (x,y))
        self.counter = 0
        self.repeat = repeat
        self.scale = scale

    def update(self):
        explosion_speed = 1
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.spritearray) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.spritearray[self.index]

        if self.index >= len(self.spritearray) - 1 and self.counter >= explosion_speed:
            if self.repeat:
                self.index = 0
            else:
                self.kill()
