# from Constants import enginesound,WIDTH,HEIGHT,screen,pew_surf,pewsound,planet_surfs,spacejunkfiles,small_font,'white',bridgewhoosh,question_position,bridge_surf,question_font,off_screen_offset,large_font
from Constants import *
from graphicgroups import *
import Variables

import math
import random
import os

# PLAYER
class Ship:
    def __init__(self,x,y,image):
        self.image = image
        self.direction = pygame.math.Vector2(x,y)
        self.spaceship_rect = self.image.get_rect(center = self.direction)
        self.deadzone = 20
        self.Yvelocity = 0
        self.Xvelocity = 0
        self.speed = 800
        self.acceleration = self.speed*3
        self.deceleration = self.speed*4
        self.shiprest = 100
        self.speedup = 2
        self.slowdown = 1
        self.last_pewtimer = 0
        self.maxnumpew = 2
        # self.shiprestpoint = 100
        self.shipborder = 128
        self.respawn_timer = -1

        self.poweruptimelength = 1000
        self.speedboost = False
        self.speedboostcounter = self.poweruptimelength

        self.lasersight = False
        self.lasersightcounter = self.poweruptimelength

    def movement(self):
        keys = pygame.key.get_pressed()
        self.temp_acc = self.acceleration * Variables.dt
        self.temp_dec = self.deceleration * Variables.dt
        #region Vecors
        # Vertical
        if keys[pygame.K_w]:
            if self.Yvelocity <= self.speed:
                self.Yvelocity += self.temp_acc
        elif keys[pygame.K_s]:
            if self.Yvelocity >= -self.speed:
                self.Yvelocity -= self.temp_acc
        else:
            if self.Yvelocity < 0:
                if self.Yvelocity >= -self.deadzone:
                    self.Yvelocity = 0
                else:
                    self.Yvelocity += self.temp_dec
            elif self.Yvelocity > 0:
                if self.Yvelocity <= self.deadzone:
                    self.Yvelocity = 0
                else:
                    self.Yvelocity -= self.temp_dec

        # Horizontal
        if keys[pygame.K_a]: 
            if self.Xvelocity <= self.speed:
                self.Xvelocity += self.temp_acc
        elif keys[pygame.K_d] and self.direction[0] < WIDTH-500:
            if self.Xvelocity >= -self.speed:
                self.Xvelocity -= self.temp_acc
        else:
            if self.Xvelocity < 0:
                if self.Xvelocity >= -self.deadzone:
                    self.Xvelocity = 0
                else:
                    self.Xvelocity += self.temp_dec
            elif self.Xvelocity > 0:
                if self.Xvelocity <= self.deadzone:
                    self.Xvelocity = 0
                else:
                    self.Xvelocity -= self.temp_dec
        #endregion
        # Pew
        if keys[pygame.K_SPACE]:
            if Variables.shipcollision == True:
                Pew.spawn(self)

    def move(self):
        self.direction[0] -= self.Xvelocity * Variables.dt
        self.direction[1] -= self.Yvelocity * Variables.dt
        if self.direction[1] < self.shipborder:
            self.direction[1] = self.shipborder
            self.Yvelocity = 0
        elif self.direction[1] > HEIGHT-self.shipborder:
            self.direction[1] = HEIGHT-self.shipborder
            self.Yvelocity = 0
        elif self.direction[0] < 48:
            self.direction[0] = 48
            self.Xvelocity = 0
        # elif self.direction[0] > WIDTH-500: self.direction[0] = WIDTH-500
        self.spaceship_rect.center = self.direction

    def update(self):
        self.movement()
        self.move()

        # RESPAWN
        if self.respawn_timer == 3:
            Variables.shipcollision = False
            self.lasersight = False
            self.speedboost = False
            self.direction = pygame.math.Vector2(100, HEIGHT // 2)
            self.respawn_timer -= 1 * Variables.dt
        elif self.respawn_timer > 0:
            self.respawn_timer -= 1 * Variables.dt
        elif self.respawn_timer < 0 and self.respawn_timer > -1:
            Variables.shipcollision = True
            self.respawn_timer -= 1 * Variables.dt
        elif self.respawn_timer <= -1: self.respawn_timer = -1

        # # SPEED BOOST PowerUp
        if self.speedboost and self.speedboostcounter > 0:
            self.speed = 1000
            self.acceleration = self.speed*6
            self.deceleration = self.speed*7
            self.speedboostcounter -= 1
        else:
            self.speed = 800
            self.acceleration = self.speed*3
            self.deceleration = self.speed*4
            self.speedboost = False

        # LASER PowerUp
        if self.lasersight and self.lasersightcounter > 256:
            laser = pygame.Surface((WIDTH,2))
            laser.set_alpha(128)
            laser.fill((255,0,0))
            screen.blit(laser,self.spaceship_rect.midright)
            self.lasersightcounter -= 100 * Variables.dt
        elif self.lasersight and self.lasersightcounter <= 256 and self.lasersightcounter > 0:
            laser = pygame.Surface((WIDTH,2))
            laser.fill((self.lasersightcounter/2,0,0))
            screen.blit(laser,self.spaceship_rect.midright)
            self.lasersightcounter -= 100 * Variables.dt
        elif self.lasersight and self.lasersightcounter <= 0:
            self.lasersight = False

    def draw(self,screen):
        from Variables import hitboxshow
        self.update()

        if Variables.shipcollision == False:
            if int(self.respawn_timer*100) % 3 == 0: self.image.set_alpha(200)
            elif int(self.respawn_timer*100) % 3 == 1: self.image.set_alpha(128)
            elif int(self.respawn_timer*100) % 3 == 2: self.image.set_alpha(16)
        else:
            self.image.set_alpha(255)
        screen.blit(self.image, self.spaceship_rect)

        # Draw hitbox
        if hitboxshow:
            pygame.draw.rect(screen, (255,0,0),self.spaceship_rect, 2)

    def respawn(self):
        Variables.lives -= 1
        self.respawn_timer = 3

class Pew:
    def __init__(self,x,y,image):
        self.x, self.y = x, y
        self.image = image
        self.pew_rect = self.image.get_rect(center = (self.x, self.y))
        self.velocity = 3000

    def update(self):
        self.x += self.velocity * Variables.dt
        if self.x > WIDTH+200:
            bullets.pop(bullets.index(self))

    def draw(self,screen):
        self.update()
        self.image = pygame.transform.scale(self.image,(128,16))
        self.pew_rect = self.image.get_rect(center = (self.x, self.y))
        screen.blit(self.image, self.pew_rect)

        # Draw hitbox
        if Variables.hitboxshow:
            pygame.draw.rect(screen, (0,255,0),self.pew_rect, 2)
    
    def spawn(player):
        if len(bullets) < player.maxnumpew:
            if pygame.time.get_ticks() - player.last_pewtimer >= 200:
                bullets.append(Pew(player.spaceship_rect.midright[0],player.spaceship_rect.midright[1],pew_surf))
                pygame.mixer.Sound.play(pewsound)
                player.last_pewtimer = pygame.time.get_ticks()

# ENVIRONMENT
class Planet:
    def __init__(self):
        self.num = random.randint(0,len(planet_surfs)-1)
        self.planet_surf = planet_surfs[self.num]
        self.scale = random.randint(5,15)/10
        self.planet_surf = pygame.transform.scale(self.planet_surf,(self.planet_surf.get_width()*self.scale,self.planet_surf.get_height()*self.scale))
        self.x = WIDTH+500
        self.y = random.randrange(0,HEIGHT)
        self.velocity = 50
    
    def update(self,player):
        self.x -= self.velocity * Variables.dt
        if self.x < -1000:
            planets.pop(planets.index(self))

    def draw(self,screen):
        self.planet_surf.set_alpha(255)
        self.planet_rect = self.planet_surf.get_rect(center = (self.x,self.y))
        screen.blit(self.planet_surf, self.planet_rect)
    
    def spawn():
        planets.append(Planet())

class SpaceJunk:
    def __init__(self,num,rotate,scale):
        self.img = pygame.image.load(os.getcwd() + spacejunkfiles[num][0]).convert_alpha()
        self.img = pygame.transform.scale(self.img,(self.img.get_width()*scale,self.img.get_height()*scale))
        self.x, self.y = WIDTH+50, random.randrange(128,HEIGHT-128)
        self.velocity = 600
        self.rotate = 0
        self.rotate_rate = rotate / 10

    def update(self,player):
        self.x -= self.velocity * Variables.dt
        if self.x < -100: spacejunk.pop(spacejunk.index(self))

    def draw(self,screen):
        self.img.set_alpha(255)
        orig_rect = self.img.get_rect()
        rotated_image = pygame.transform.rotate(self.img,self.rotate)
        rot_rect = orig_rect.copy()
        rot_rect.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rot_rect).copy()
        self.centered_image = rotated_image.get_rect(center = (self.x,self.y))
        screen.blit(rotated_image, self.centered_image)
        self.rotate += self.rotate_rate

    def spawn():
        whichjunk = random.randint(0,len(spacejunkfiles)-1)
        junksize = random.randrange(2,10)
        spacejunk.append(SpaceJunk(whichjunk,random.randrange(-10,10),junksize*0.1))
        junkobject = pygame.mixer.Sound(os.getcwd() + spacejunkfiles[whichjunk][1])
        junkobject.set_volume(junksize*0.1)
        pygame.mixer.Sound.play(junkobject)

class Star:
    def __init__(self):
        self.depth = random.randrange(100,1000)
        self.x, self.y = WIDTH, random.randrange(50,HEIGHT-50)
        self.gamemode = Variables.gamemode
        self.kana = random.randint(0,45)
        self.velocity = float(self.depth)
        fontsize = 15
        star_font = pygame.font.SysFont(font_name, fontsize)
        self.startext = star_font.render(Variables.commasep[self.kana][(Variables.gamemode+1)%2], False, 'white')
        if Variables.lives <= 0: self.startext = star_font.render('GAME OVER', True, 'white')

        # scale = (self.depth*2)/fontsize
        # self.startext = pygame.transform.scale(self.startext,(self.startext.get_width()*scale,self.startext.get_height()*scale))

    def update(self,player):
        self.x -= self.velocity * Variables.dt
        if self.x < -100: starfield.pop(starfield.index(self))

    def draw(self,screen):
        self.startext.set_alpha(self.depth/900*255)
        screen.blit(self.startext, (self.x,self.y))

    def spawn():
        starfield.append(Star())

class Bridge:
    def __init__(self,x,y,image):
        self.img = image
        self.x, self.y = x, y
        self.velocity = 3000
        self.drawn = False
        self.sound = True

    def update(self,player):
        self.x -= self.velocity * Variables.dt
        if self.x < -1000:
            bridges.pop(bridges.index(self))
            self.drawn = False

    def draw(self,screen):
        Variables.last_kananum = Variables.kananum
        Variables.last_level = Variables.level
        if self.sound == True:
            pygame.mixer.Sound.play(bridgewhoosh)
            self.sound = False
        if self.x < question_position[0]-40 and self.x > question_position[0]-80 and self.drawn == False:
            Variables.kananum += 1
            if Variables.kananum >= len(Variables.gamekana[Variables.level]):
                Variables.kananum = 0
                Variables.level += 1
            self.drawn = True
            CutOffLine.spawn()
        screen.blit(self.img, (self.x,self.y))

    def spawn():
        bridges.append(Bridge(WIDTH,0,bridge_surf))

class CutOffLine:
    def __init__(self,x,y,kanatohit,lastkana):
        self.x = x
        self.y = y
        self.lastkana = lastkana
        self.kanatohit = kanatohit
        self.velocity = 200

    def update(self,player):
        self.x -= self.velocity * Variables.dt
        if self.x < -200: cuttoffline.pop(cuttoffline.index(self))

    def draw(self,screen):
        self.box = pygame.Rect(self.x,0,2,HEIGHT)
        kanaoffset = 40
        pygame.draw.rect(screen, (128,0,0), self.box, 2)
        last_kana_text = question_font.render(self.lastkana, True, 'white')
        next_kana_text = question_font.render(self.kanatohit, True, 'white')
        lkt_rect = last_kana_text.get_rect()
        nkt_rect = next_kana_text.get_rect()
        screen.blit(last_kana_text, (self.x-kanaoffset-(lkt_rect.centerx), HEIGHT-64))
        screen.blit(next_kana_text, (self.x+kanaoffset-(nkt_rect.centerx), HEIGHT-64))

    def spawn():
        cuttoffline.append(CutOffLine(WIDTH+off_screen_offset,0,Variables.gamekana[Variables.level][Variables.kananum][2],Variables.gamekana[Variables.last_level][Variables.last_kananum][2]))

class BigLaser:
    def __init__(self,x,y):
        self.x, self.y = x, y
        self.image = biglaser_surf
        self.velocity = 8000
        self.hitboxYshrink = 50
    
    def update(self):
        self.x -= self.velocity * Variables.dt
        if self.x < -512:
            biglasers.pop(biglasers.index(self))
            self.laserdelay = 100

    def draw(self,screen):
        self.update()
        self.image = pygame.transform.scale(self.image,(2048,256))
        self.biglaser_rect = self.image.get_rect(center = (self.x, self.y))
        screen.blit(self.image, self.biglaser_rect)

        self.hitbox = self.biglaser_rect
        self.hitbox[1] += self.hitboxYshrink
        self.hitbox[3] -= (self.hitboxYshrink*2)
        if Variables.hitboxshow:
            pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)

    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False

    def spawn(y):
        biglasers.append(BigLaser(WIDTH+1000,y))
        pygame.mixer.Sound.play(biglaser_sound)

class BigLaserWarning:
    def __init__(self,y):
        self.last_warn_timer = 0
        self.opacity = True
        self.y = y
        self.image_flash_delay = 100
        self.warning_length = 10
        self.image = biglaser_warning_surf

    def update(self):
        if self.warning_length > 0:
            if pygame.time.get_ticks() - self.last_warn_timer >= self.image_flash_delay:
                if self.opacity == True:
                    self.opacity = False
                else:
                    self.opacity = True
                    pygame.mixer.Sound.play(warning_sound)
                self.warning_length -= 1
                self.last_warn_timer = pygame.time.get_ticks()
        if self.warning_length <= 0:
            pygame.mixer.Sound.stop(warning_sound)
            BigLaser.spawn(self.y)
            warnings.pop(warnings.index(self))

    def draw(self,screen):
        self.update()
        if self.opacity == True:
            self.warning_rect = self.image.get_rect(midright = (WIDTH, self.y))
            screen.blit(self.image, self.warning_rect)

    def spawn(player):
        warnings.append(BigLaserWarning(random.randint(player.spaceship_rect.center[1]-64,player.spaceship_rect.center[1]+64)))

# INTERACTABLES
class Kana:
    def __init__(self,x,y,kana,fade,rotate,color='white'):
        self.x, self.y = x, y
        self.color = color
        self.xvelocity, self.yvelocity = 200, random.randint(-20,20)
        self.shrink = 5
        self.kana = kana
        self.fade = fade
        self.rotate = 0
        self.rotate_rate = rotate * 0.002
        self.kanatext = kana_font.render(Variables.gamekana[Variables.level][self.kana][Variables.gamemode], True, self.color)

    def update(self,player):
        self.x -= self.xvelocity * Variables.dt
        self.y += self.yvelocity * Variables.dt

    def draw(self,screen):
        orig_rect = self.kanatext.get_rect()
        rotated_image = pygame.transform.rotate(self.kanatext,self.rotate)
        rot_rect = orig_rect.copy()
        rot_rect.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rot_rect).copy()
        self.centered_image = rotated_image.get_rect(center = (self.x,self.y))
        screen.blit(rotated_image, self.centered_image)
        self.rotate += self.rotate_rate

        # Draw hitbox
        self.hitbox = self.centered_image
        if Variables.hitboxshow:
            pygame.draw.circle(screen,(0,0,255),(self.x,self.y), 4)
            pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)

    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False

class PowerUp:
    def __init__(self,x,y,xvelocity,yvelocity,image,pueffect):
        self.pueffect = pueffect
        self.img = image
        self.img = pygame.transform.scale(self.img,(64,64))
        self.x, self.y = x, y
        self.xvelocity, self.yvelocity = xvelocity, yvelocity
        self.hitbox = self.img_rect = self.img.get_rect(center = (self.x, self.y))

    def update(self,player):
        self.x -= self.xvelocity * Variables.dt
        self.y += self.yvelocity * Variables.dt * math.sin(self.x/100)
        if self.x < -64:
            powerups.pop(powerups.index(self))

    def draw(self,screen):
        self.hitbox = self.img_rect = self.img.get_rect(center = (self.x, self.y))
        self.img.set_alpha(255)
        self.img_rect = self.img.get_rect(center = (self.x, self.y))
        screen.blit(self.img, self.img_rect)

        # Draw hitbox
        if Variables.hitboxshow:
            pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)

    def spawn(graphic,effect):
        powerups.append(PowerUp(WIDTH+64, random.randrange(128,HEIGHT-128,),100,random.randrange(100,200),graphic,effect))

    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False
    
    def effect(self,pueffect,player):
        if pueffect == "laser":
            if self.collide(player.spaceship_rect):
                powerups.pop(powerups.index(self))
                player.lasersight = True
                player.lasersightcounter = player.poweruptimelength
                pygame.mixer.Sound.play(powerup_sound)
        if pueffect == "speed":
            if self.collide(player.spaceship_rect):
                powerups.pop(powerups.index(self))
                player.speedboost = True
                player.speedboostcounter = player.poweruptimelength
                pygame.mixer.Sound.play(powerup_sound)
        
class Enemies:
    def __init__(self,typeof):
        self.type = typeof
        self.image = enemy_surfs[self.type]
        self.image = pygame.transform.scale(self.image,(64, 64))
        self.x, self.y = WIDTH, random.randrange(128,HEIGHT-128)
        self.velocity = random.randint(100,400)
        self.Yvelocity = random.randint(-50,50)
        self.last_enemy_pew = 0

    def calculate_angles(self,number_of_angles):
        if number_of_angles < 1:
            return []
        
        angle_step = 360 / number_of_angles
        angles = [i * angle_step for i in range(number_of_angles)]
        return angles

    def update(self):
        if self.type == 0 or self.type == 1:
            self.enemy_rect = self.image.get_rect(midleft = (self.x, self.y))
        elif self.type == 2:
            self.enemy_rect = self.image.get_rect(center = (self.x, self.y))
        self.x -= self.velocity * Variables.dt
        self.y += self.Yvelocity * Variables.dt
        if self.x < -128:
            enemies.pop(enemies.index(self))
    
    def findobjectangle(self,player):
            # Find angle of player
            dx = self.x - player.spaceship_rect.center[0]
            dy = self.y - player.spaceship_rect.center[1]
            self.theta = math.atan2(-dy,dx)
            return self.theta

    def shoot(self,player):
        angle = self.findobjectangle(player)
        if pygame.time.get_ticks() - self.last_enemy_pew >= random.randint(2000,10000):
            if self.type == 0: # AIMED SHOT
                if angle < math.pi/3 and angle > -math.pi/3:
                    pygame.mixer.Sound.play(enemypew_sound)
                    enemyprojectiles.append(EnemyProjectiles(self.x, self.y,angle))
            elif self.type == 1: # FORWARD SHOT
                pygame.mixer.Sound.play(enemypew_sound)
                enemyprojectiles.append(EnemyProjectiles(self.x, self.y,math.radians(random.randint(-10,10))))
            elif self.type == 2: #AoE SHOT
                pygame.mixer.Sound.play(enemypew_sound)
                for angle in self.calculate_angles(8):
                    enemyprojectiles.append(EnemyProjectiles(self.x, self.y,math.radians(angle)))
            self.last_enemy_pew = pygame.time.get_ticks()

    def draw(self,screen,player):
        self.update()
        screen.blit(self.image, self.enemy_rect)

        self.hitbox = self.enemy_rect
        if Variables.hitboxshow:
            pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)
            pygame.draw.line(screen, (255,255,0), (self.x, self.y),player.spaceship_rect.center)

    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False

    def spawn():
        # enemies.append(Enemies(random.randint(0,2)))
        enemies.append(Enemies(random.randint(0,2)))

class EnemyProjectiles:
    def __init__(self,x,y,direction):
        self.x, self.y = x, y
        self.direction = direction
        self.skewoffset = 20
        self.directionskew = random.randint(-self.skewoffset,self.skewoffset)/100
        self.image = enemy_pew_surf
        self.image = pygame.transform.scale(self.image,(32, 32))
        self.velocity = 500

    def objectdirection(self,direction):
        pewdir = direction - math.pi/2 + self.directionskew
        sin_a = math.sin(pewdir)
        cos_a = math.cos(pewdir)
        self.x += self.velocity * sin_a * Variables.dt
        self.y += self.velocity * cos_a * Variables.dt
        return self.x, self.y

    def update(self):
        self.x, self.y = self.objectdirection(self.direction)
        self.enemy_pew_rect = self.image.get_rect(center = (self.x, self.y))
        if self.x < 0 or self.y < 0 or self.y > HEIGHT:
            enemyprojectiles.pop(enemyprojectiles.index(self))

    def draw(self,screen):
        self.update()
        screen.blit(self.image, self.enemy_pew_rect)

        self.hitbox = self.enemy_pew_rect
        if Variables.hitboxshow:
            pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)

    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False
    
    def spawn():
        enemyprojectiles.append(EnemyProjectiles())