# from Constants import enginesound,WIDTH,HEIGHT,screen,pew_surf,pewsound,planet_surfs,spacejunkfiles,small_font,WHITE,bridgewhoosh,question_position,bridge_surf,question_font,off_screen_offset,large_font
from Constants import *
from graphicgroups import *
import Variables

import math
import random
import os

# PLAYER
class Ship:
    def __init__(self,x,y,image):
        self.x, self.y = x, y
        self.image = image
        self.spaceship_rect = self.image.get_rect(center = (self.x, self.y))
        self.movex, self.movey = 0, 0
        self.speed = 5
        self.pullback = 1.5
        self.last_pewtimer = 0
        self.maxnumpew = 2
        self.can_play = True
        self.shiprestpoint = 100
        self.shipborder = 128

        self.poweruptimelength = 1000
        self.speedboost = False
        self.speedboostcounter = self.poweruptimelength

        self.lasersight = False
        self.lasersightcounter = self.poweruptimelength

    def movement(self):
        keys = pygame.key.get_pressed()

        # Vertical
        if keys[pygame.K_w] and keys[pygame.K_s]: self.movey = 0
        elif keys[pygame.K_w]: self.movey = -self.speed
        elif keys[pygame.K_s]: self.movey = self.speed
        else: self.movey = 0

        # Horizontal
        if keys[pygame.K_a] and keys[pygame.K_d]: self.movex = 0
        elif keys[pygame.K_a] and self.x > 0: self.movex = -self.speed
        elif keys[pygame.K_d]:
            self.movex = self.speed
            if self.can_play:
                pygame.mixer.Sound.play(enginesound)
                self.can_play = False
        else:
            self.movex = 0
            pygame.mixer.Sound.stop(enginesound)
            self.can_play = True

        # Pew
        if keys[pygame.K_SPACE]:
            Pew.spawn(self)

    def update(self):
        self.movement()
        self.y += self.movey
        self.x += self.movex
        
        # Ship restpoint
        if self.x > self.shiprestpoint: self.x -= self.pullback
        elif self.x <= self.shiprestpoint-1: self.x += self.pullback

        # Ship Border
        if self.y > HEIGHT-self.shipborder: self.y = HEIGHT-self.shipborder
        elif self.y < self.shipborder: self.y = self.shipborder

        # Ship Pullback Rate
        if self.x > 500: self.pullback += 0.1
        elif self.x < 500: self.pullback -= 0.05
        if self.pullback <= 1.5: self.pullback = 1.5

        self.x = int(self.x) # Convert X position to integer

        if self.speedboost and self.speedboostcounter > 0:
            self.speed = 8
            self.speedboostcounter -= 1
        else:
            self.speed = 5
            self.speedboost = False

        if self.lasersight and self.lasersightcounter > 200:
            laser = pygame.Surface((WIDTH,2))
            laser.set_alpha(128)
            laser.fill((255,0,0))
            screen.blit(laser,(self.x,self.y))
            self.lasersightcounter -= 1
        elif self.lasersight and self.lasersightcounter <= 200 and self.lasersightcounter > 0:
            laser = pygame.Surface((WIDTH,2))
            laser.fill((255,0,0))
            if self.lasersightcounter/2 % 2 == 0:
                laser.set_alpha(96)
            else:
                laser.set_alpha(16)
            screen.blit(laser,(self.x,self.y))
            self.lasersightcounter -= 1
        elif self.lasersight and self.lasersightcounter <= 0:
            self.lasersight = False

    def draw(self,screen):
        from Variables import hitboxshow
        self.update()
        self.spaceship_rect = self.image.get_rect(center = (self.x, self.y))
        screen.blit(self.image, self.spaceship_rect)

        # Draw hitbox
        # if Variables.hitboxshow:
        if hitboxshow:
            pygame.draw.rect(screen, (255,0,0),self.spaceship_rect, 2)

class Pew:
    def __init__(self,x,y,image):
        self.x, self.y = x, y
        self.image = image
        self.velocity = 60

    def update(self):
        self.x += self.velocity
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
                bullets.append(Pew(player.x,player.y,pew_surf))
                pygame.mixer.Sound.play(pewsound)
                player.last_pewtimer = pygame.time.get_ticks()

# ENVIRONMENT
class Planet:
    def __init__(self,x,y,num,scale):
        self.planet_surf = planet_surfs[num]
        self.planet_surf = pygame.transform.scale(self.planet_surf,(self.planet_surf.get_width()*scale,self.planet_surf.get_height()*scale))
        self.x = x
        self.y = y
        self.velocity = 0.5
    
    def update(self,player):
        self.x -= self.velocity + 0.2 * (player.x/100)
        if self.x < -1000:
            planets.pop(planets.index(self))

    def draw(self,screen):
        self.planet_surf.set_alpha(255)
        self.planet_rect = self.planet_surf.get_rect(center = (self.x,self.y))
        screen.blit(self.planet_surf, self.planet_rect)
    
    def spawn():
        planets.append(Planet(WIDTH+500, random.randrange(0,HEIGHT/2,),random.randint(0,len(planet_surfs)-1),random.randint(5,15)/10))

class SpaceJunk:
    def __init__(self,x,y,num,rotate,scale):
        self.img = pygame.image.load(os.getcwd() + spacejunkfiles[num][0]).convert_alpha()
        self.img = pygame.transform.scale(self.img,(self.img.get_width()*scale,self.img.get_height()*scale))
        self.x = x
        self.y = y
        self.velocity = 8
        self.rotate = 0
        self.rotate_rate = rotate / 10

    def update(self,player):
        self.x -= self.velocity + 0.2 * (player.x/100)
        if self.x < -1000:
            spacejunk.pop(spacejunk.index(self))

    def draw(self,screen):
        self.img.set_alpha(255)
        orig_rect = self.img.get_rect()
        rotated_image = pygame.transform.rotate(self.img,self.rotate)
        rot_rect = orig_rect.copy()
        rot_rect.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rot_rect).copy()
        screen.blit(rotated_image, (self.x,self.y))
        self.rotate += self.rotate_rate

    def spawn():
        whichjunk = random.randint(0,len(spacejunkfiles)-1)
        junksize = random.randrange(2,10)
        spacejunk.append(SpaceJunk(WIDTH,random.randrange(0,HEIGHT/2),whichjunk,random.randrange(-10,10),junksize*0.1))
        junkobject = pygame.mixer.Sound(os.getcwd() + spacejunkfiles[whichjunk][1])
        junkobject.set_volume(junksize*0.1)
        pygame.mixer.Sound.play(junkobject)

class Star:
    def __init__(self,x,y,fade,kana,gamemode):
        self.depth = random.randrange(1,9)
        self.x, self.y = x, y
        self.gamemode = gamemode
        self.fade = fade
        self.kana = kana
        self.velocity = float(self.depth)
        self.startext = star_font.render(Variables.commasep[self.kana][(gamemode+1)%2], True, WHITE)
        if Variables.lives <= 0: self.startext = star_font.render('GAME OVER', True, WHITE)

    def update(self,player):
        self.x -= self.velocity + 1 * (player.x/100)
        if self.x < 0: starfield.pop(starfield.index(self))

    def draw(self,screen):
        self.startext.set_alpha(self.depth*20)
        screen.blit(self.startext, (self.x,self.y))

    def spawn():
        starfield.append(Star(WIDTH,random.randrange(50,HEIGHT-50),1,random.randint(0,45),Variables.gamemode))

class Bridge:
    def __init__(self,x,y,image):
        self.img = image
        self.x, self.y = x, y
        self.velocity = 30
        self.drawn = False
        self.sound = True

    def update(self,player):
        self.x -= self.velocity + 1 * (player.x/100)
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
        self.velocity = 2

    def update(self,player):
        self.x -= self.velocity + 1 * (player.x/100)
        if self.x < -200: cuttoffline.pop(cuttoffline.index(self))

    def draw(self,screen):
        self.box = pygame.Rect(self.x,0,2,HEIGHT)
        kanaoffset = 40
        pygame.draw.rect(screen, (128,0,0), self.box, 2)
        last_kana_text = question_font.render(self.lastkana, True, WHITE)
        next_kana_text = question_font.render(self.kanatohit, True, WHITE)
        lkt_rect = last_kana_text.get_rect()
        nkt_rect = next_kana_text.get_rect()
        screen.blit(last_kana_text, (self.x-kanaoffset-(lkt_rect.centerx), HEIGHT-64))
        screen.blit(next_kana_text, (self.x+kanaoffset-(nkt_rect.centerx), HEIGHT-64))

    def spawn():
        cuttoffline.append(CutOffLine(WIDTH+off_screen_offset,0,Variables.gamekana[Variables.level][Variables.kananum][2],Variables.gamekana[Variables.last_level][Variables.last_kananum][2]))

# INTERACTABLES
class Kana:
    def __init__(self,x,y,kana,xvelocity,yvelocity,fade,rotate):
        self.x, self.y = x, y
        self.xvelocity, self.yvelocity = xvelocity, yvelocity
        self.shrink = 5
        self.kana = kana
        self.fade = fade
        self.rotate = 0
        self.rotate_rate = rotate * 0.02
        self.kanatext = kana_font.render(Variables.gamekana[Variables.level][self.kana][Variables.gamemode], True, WHITE)

    def update(self,player):
        self.x -= self.xvelocity + 1 * (player.x/100)
        self.y += self.yvelocity

    def draw(self,screen):
        orig_rect = self.kanatext.get_rect()
        rotated_image = pygame.transform.rotate(self.kanatext,self.rotate)
        rot_rect = orig_rect.copy()
        rot_rect.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rot_rect).copy()
        centered_image = rotated_image.get_rect(center = (self.x,self.y))
        screen.blit(rotated_image, centered_image)
        self.rotate += self.rotate_rate

        # Draw hitbox
        self.hitbox = centered_image
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
        self.x, self.y = x, y
        self.xvelocity, self.yvelocity = xvelocity, yvelocity
        self.hitbox = self.img_rect = self.img.get_rect(center = (self.x, self.y))

    def update(self,player):
        self.x -= self.xvelocity + 1 * (player.x/100)
        self.y += self.yvelocity * math.sin(self.x/100)
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
        powerups.append(PowerUp(WIDTH+64, random.randrange(128,HEIGHT-128,),1,random.randrange(100,200)/100,graphic,effect))

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
        if pueffect == "speed":
            if self.collide(player.spaceship_rect):
                powerups.pop(powerups.index(self))
                player.speedboost = True
                player.speedboostcounter = player.poweruptimelength

