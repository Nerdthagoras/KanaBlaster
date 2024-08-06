import pygame

# SPRITE STUFF
class LoadSpritesheet:
    def __init__(self, image, spritesizex,spritesizey,scale):
        self.sheet = image
        self.spritesizex, self.spritesizey = spritesizex, spritesizey
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