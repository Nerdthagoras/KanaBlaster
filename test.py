import pygame
import os
pygame.init()
WIDTH, HEIGHT = 1440,900
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

running = True

class Player:
    def __init__(self,x,y,width,height,image):
        self.x, self.y = x, y
        self.image = image
        self.spaceship_rect = self.image.get_rect(center = (self.x, self.y))
        self.movex, self.movey = 0, 0
        self.width, self.height = width, height
        self.speed = 5
        self.pullback = 1.5

    def movement(self):
        keys = pygame.key.get_pressed()

        # Vertical
        if keys[pygame.K_w] and keys[pygame.K_s]: self.movey = 0
        elif keys[pygame.K_w]: self.movey = -self.speed
        elif keys[pygame.K_s]: self.movey = self.speed
        else: self.movey = 0

        # Horizontal
        if keys[pygame.K_a] and keys[pygame.K_d]: self.movex = 0
        elif keys[pygame.K_a]: self.movex = -self.speed
        elif keys[pygame.K_d]: self.movex = self.speed
        else: self.movex = 0

    def update(self):
        player.movement()        
        self.y += self.movey
        self.x += self.movex
        if self.x > 100:
            self.x -= self.pullback
        elif self.x < 98:
            self.x += self.pullback
        if self.y > HEIGHT-128:
            self.y = HEIGHT-128
        elif self.y < 64:
            self.y = 64
        if self.x < 0:
            self.x = 0
        # elif self.x > 500:
        #     self.pullback += 0.1
        # elif self.x < 500:
        #     self.pullback -= 0.05
        # if self.pullback <= 1.5:
        #     self.pullback = 1.5
        self.x = int(self.x)

    def draw(self,screen):
        self.image_rect = self.image.get_rect(center = (self.x, self.y))
        screen.blit(self.image, self.image_rect)

class LoadSpritesheet():
    def __init__(self, image, spritesize,scale):
        self.sheet = image
        self.spritesize = spritesize
        self.scale = scale
        self.images = []

        counterx,countery = 0,0
        num_of_frames = int((self.sheet.get_width()/self.spritesize) * (self.sheet.get_height()/spritesize))
        for _ in range(num_of_frames):
            self.images.append(self.get_image(counterx, countery, self.spritesize, self.spritesize, self.scale))
            counterx += 1
            if counterx >= self.sheet.get_width()/self.spritesize:
                countery += 1
                counterx = 0

    def get_image(self, framex, framey, width, height, scale):
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), ((framex * width), (framey * width), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))

        return image

class SinglePlayAnimation(pygame.sprite.Sprite):
    def __init__(self, x, y, spritearray, repeat):
        pygame.sprite.Sprite.__init__(self)
        self.explode_last_update = pygame.time.get_ticks()
        self.spritearray = spritearray
        self.index = 0
        self.image = self.spritearray[self.index]
        self.rect = self.image.get_rect(center = (x,y))
        self.counter = 0
        self.repeat = repeat

    def update(self):
        global running
        explosion_speed = 1
		#update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.spritearray) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.spritearray[self.index]

		#if the animation is complete, reset animation index
        if self.index >= len(self.spritearray) - 1 and self.counter >= explosion_speed:
            if self.repeat:
                self.index = 0
            else:
                self.kill()

explosion_group = pygame.sprite.Group()
explosion = LoadSpritesheet(pygame.image.load(os.path.join('sprites','explode.png')).convert_alpha(),256,2)
Explode = SinglePlayAnimation(100,100,explosion.images,True)
explosion_group.add(Explode)

spaceship_surf = pygame.image.load(os.path.join('images', 'ship.png')).convert_alpha()
player = Player(WIDTH//2,HEIGHT//2,0,0,spaceship_surf)

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))
    player.update()
    player.draw(screen)
    explosion_group.draw(screen)
    explosion_group.update()
    pygame.display.flip()

pygame.quit()