import pygame
import os
pygame.init()
WIDTH, HEIGHT = 1440,900
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

running = True

class Player:
    def __init__(self,x,y,image):
        self.x, self.y = x, y
        self.image = image
        self.spaceship_rect = self.image.get_rect(center = (self.x, self.y))
        self.direction = pygame.math.Vector2()
        self.Vvelocity = 0
        self.Xvelocity = 0
        self.speedup = 0.8
        self.slowdown = 0.2
        self.speed = 8

    def movement(self):
        keys = pygame.key.get_pressed()
        #region Vecors
        # Vertical
        if keys[pygame.K_w]: 
            if self.Vvelocity >= -self.speed:
                self.Vvelocity -= self.speedup
        elif keys[pygame.K_s]:
            if self.Vvelocity <= self.speed:
                self.Vvelocity += self.speedup
        else: 
            if self.Vvelocity < 0:
                self.Vvelocity += self.slowdown
                if self.Vvelocity > self.slowdown:
                    self.Vvelocity = 0
            elif self.Vvelocity > 0:
                self.Vvelocity -= self.slowdown
                if self.Vvelocity < self.slowdown:
                    self.Vvelocity = 0

        # Horizontal
        if keys[pygame.K_a]: 
            if self.Xvelocity >= -self.speed:
                self.Xvelocity -= self.speedup
        elif keys[pygame.K_d]:
            if self.Xvelocity <= self.speed:
                self.Xvelocity +=self.speedup
        else: 
            if self.Xvelocity < 0:
                self.Xvelocity += self.slowdown
                if self.Xvelocity > self.slowdown:
                    self.Xvelocity = 0
            elif self.Xvelocity > 0:
                self.Xvelocity -= self.slowdown
                if self.Xvelocity < self.slowdown:
                    self.Xvelocity = 0
        #endregion
    
    def move(self):
        self.direction[1] = self.Vvelocity
        self.direction[0] = self.Xvelocity
        self.spaceship_rect.center += self.direction

    def update(self):
        player.movement()
        self.move()

    def draw(self,screen):
        self.hitbox = self.spaceship_rect
        print(self.spaceship_rect.center)
        screen.blit(self.image, self.spaceship_rect)
        pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)
        pygame.draw.circle(screen,(0,0,255),(self.spaceship_rect.center), 4)

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
player = Player(WIDTH//2,HEIGHT//2,spaceship_surf)

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    screen.fill((0,0,0))
    player.update()
    player.draw(screen)
    # explosion_group.draw(screen)
    # explosion_group.update()
    pygame.display.flip()

pygame.quit()