# from Constants import off_screen_offset,min_kana_alpha,ui_font,question_font,GAME_OVER_font,debug_locationx,debug_locationy,enginesound,speed_powerup_surf,laser_powerup_surf,oneup_powerup_surf,enemy_surfs,biglaser_surf,correct_kana_dying_sound,correct_kana_lost_sound,explosion_surfs,badhit,pew_array,brick_surf,brickbreak_sound,goodhit,debris_surf,powerup_array,shiphit,tips,boss_spritesheet_surfs,bosses_array,shiplaser_sound,spaceship_surfs,spaceship_flame_surfs,screen,pew_surfs,pew_sounds,planet_surfs,menustarmessage,font_name,bridgewhoosh,bridge_surf,spacejunkfiles,biglaser_sound,biglaser_warning_surf,warning_sound,WARNING_font,kana_font,kana_ui_font,powerup_sound,enemy_spritesheet_surfs,enemypew_sound,enemy_pew_surf,wallsegment_surf
# from Graphicgroups import starfield_group,kanas,spacejunk,warnings,biglasers,wallsegments,enemies,enemyprojectiles,kanalist,correctkanas,bullets,planet_group,cuttoffline,explosion_group,bricks,debris,centerwarning,bridge_group,tip_group,powerups,shields,damagenumbers,bosses,laserpowerups,speedpowerups
# from Settings import ship_normal_top_speed,ship_screen_boundary,kanax_velocity,ship_boosted_top_speed,ship_boosted_acceleration,ship_boosted_deceleration,ship_normal_acceleration,ship_normal_deceleration,question_position,num_to_shoot_new_kana,kanay_velocity,enemy_knockback_recoveryx,enemy_knockback_recoveryy

import Variables
import Constants
import Settings
import Graphicgroups
import pygame
import math
import random
import os

# PLAYER
class Ship:
    def __init__(self,x,y,spritearray):
        self.spritearray = spritearray
        self.flamearray = Constants.spaceship_flame_surfs
        self.animindex = 0
        self.animspeed = 10
        self.image = self.spritearray.images[self.animindex]
        self.location = pygame.math.Vector2(x,y)
        self.spaceship_rect = self.image.get_rect(center = self.location)
        self.deadzone = 20
        self.Xvelocity, self.Yvelocity = 0, 0
        self.speed = Settings.ship_normal_top_speed
        self.acceleration, self.deceleration = self.speed*3, self.speed*4
        self.shiprest = 100
        self.speedup, self.slowdown = 2, 1
        self.last_pewtimer = 0
        self.maxnumpew = 2
        self.shipborder = Settings.ship_screen_boundary
        self.respawn_timer = -1
        self.hitbox = [0,0,0,0]
        self.shield = False
        self.shieldradius = 64
        self.laserpower = int(Variables.score) * Constants.pew_array[Variables.pewtype]["laserpower"] + 1
        self.power_grapic = Constants.ui_font.render(str(self.laserpower), True, 'green')
        # Flames
        self.xflamedir = 0
        self.yflamedir = 0
        self.xflameindex = 0
        self.yflameindex = 0
        self.flamespeed = 30
        self.xflameimage = pygame.transform.rotate(self.flamearray.images[self.xflameindex],0)
        self.xflame_rect = self.xflameimage.get_rect(center = self.location)
        self.yflameimage = pygame.transform.rotate(self.flamearray.images[self.yflameindex],90)
        self.yflame_rect = self.yflameimage.get_rect(center = self.location)

        #region Powerups
        self.poweruptimelength = 1000
        self.speedboost = False
        self.speedboostcounter = self.poweruptimelength

        self.lasersight = False
        self.lasersightcounter = self.poweruptimelength
        self.laserlength = 0
        self.laser = pygame.Surface((self.laserlength,2))

        self.kanaswitch = False
        self.kanaswitchcounter = self.poweruptimelength
        #endregion

    def xflame(self,dir):
        self.xflameindex += self.flamespeed * Variables.dt
        if self.xflameindex > 12: self.xflameindex = 5
        self.xflameimage = pygame.transform.rotate(self.flamearray.images[int(self.xflameindex)],dir)
        if dir == 0:self.xflame_rect = self.xflameimage.get_rect(midleft = self.spaceship_rect.center)
        elif dir == 180:self.xflame_rect = self.xflameimage.get_rect(midright = self.spaceship_rect.center)

    def yflame(self,dir):
        self.yflameindex += self.flamespeed * Variables.dt
        if self.yflameindex > 12: self.yflameindex = 5
        self.yflameimage = pygame.transform.rotate(self.flamearray.images[int(self.yflameindex)],dir)
        if dir == -90:self.yflame_rect = self.yflameimage.get_rect(midtop = self.spaceship_rect.center)
        elif dir == 90:self.yflame_rect = self.yflameimage.get_rect(midbottom = self.spaceship_rect.center)

    def animate(self):
        self.animindex += self.animspeed * Variables.dt
        if self.animindex > len(self.spritearray.images)-1: self.animindex = 0
        self.image = self.spritearray.images[int(self.animindex)]

    def movement(self):
        keys = pygame.key.get_pressed()
        self.temp_acc = self.acceleration * Variables.dt
        self.temp_dec = self.deceleration * Variables.dt

        #region Vecors
        # Horizontal
        if keys[pygame.K_a]: 
            self.xflame(0)
            Constants.screen.blit(self.xflameimage, self.xflame_rect)
            if self.Xvelocity <= self.speed:
                self.Xvelocity += self.temp_acc
        elif keys[pygame.K_d] and self.location[0] < Constants.WIDTH-200:
            self.xflame(180)
            Constants.screen.blit(self.xflameimage, self.xflame_rect)
            if self.Xvelocity >= -self.speed:
                self.Xvelocity -= self.temp_acc
        else:
            self.xflameindex = 0
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

        # Vertical
        if keys[pygame.K_w]:
            self.yflame(-90)
            Constants.screen.blit(self.yflameimage, self.yflame_rect)
            if self.Yvelocity <= self.speed:
                self.Yvelocity += self.temp_acc
        elif keys[pygame.K_s]:
            self.yflame(90)
            Constants.screen.blit(self.yflameimage, self.yflame_rect)
            if self.Yvelocity >= -self.speed:
                self.Yvelocity -= self.temp_acc
        else:
            self.yflameindex = 0
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
        #endregion

        # Pew
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYUP:
        #         if event.key == pygame.K_SPACE:
        #             Pew.spawn(self)

        if keys[pygame.K_SPACE]:
            Pew.spawn(self)    

    def move(self):
        self.location[0] -= (self.Xvelocity + 2*Settings.kanax_velocity/3) * Variables.dt
        self.location[1] -= self.Yvelocity * Variables.dt
        if self.location[1] < self.shipborder:
            self.location[1] = self.shipborder
            self.Yvelocity = 0
        elif self.location[1] > Constants.HEIGHT-self.shipborder:
            self.location[1] = Constants.HEIGHT-self.shipborder
            self.Yvelocity = 0
        elif self.location[0] <= 48:
            self.location[0] = 48
            # self.Xvelocity = 0
        # elif self.direction[0] > WIDTH-500: self.direction[0] = WIDTH-500
        self.spaceship_rect.center = self.location

    def update(self):
        self.animate()
        # self.movement()
        self.move()

        # RESPAWN
        if self.respawn_timer == 3:
            pygame.mixer.Sound.stop(Constants.shiplaser_sound)
            Variables.shipcollision = False
            self.lasersight = False
            self.speedboost = False
            self.location = pygame.math.Vector2(100, Constants.HEIGHT // 2)
            self.respawn_timer -= 1 * Variables.dt
        elif self.respawn_timer > 0:
            self.respawn_timer -= 1 * Variables.dt
        elif self.respawn_timer <= 0 and self.respawn_timer > -1:
            Variables.shipcollision = True
            self.respawn_timer -= 1 * Variables.dt
        elif self.respawn_timer < -1: self.respawn_timer = -1

        # # SPEED BOOST PowerUp
        if self.speedboost and self.speedboostcounter > 0:
            self.speed = Settings.ship_boosted_top_speed
            self.acceleration = self.speed*Settings.ship_boosted_acceleration
            self.deceleration = self.speed*Settings.ship_boosted_deceleration
            self.speedboostcounter -= 100 * Variables.dt
        else:
            self.speed = Settings.ship_normal_top_speed
            self.acceleration = self.speed*Settings.ship_normal_acceleration
            self.deceleration = self.speed*Settings.ship_normal_deceleration
            self.speedboost = False

        # LASER PowerUp
        if self.lasersight and self.lasersightcounter > 256:
            self.laser = pygame.Surface((self.laserlength,2))
            self.laser.set_alpha(128)
            self.laser.fill((255,0,0))
            self.lasersightcounter -= 100 * Variables.dt
            self.laserlength += 3000 * Variables.dt
        elif self.lasersight and self.lasersightcounter <= 256 and self.lasersightcounter > 0:
            self.laser = pygame.Surface((Constants.WIDTH,2))
            self.laser.fill((self.lasersightcounter/2,0,0))
            self.lasersightcounter -= 100 * Variables.dt
        elif self.lasersight and self.lasersightcounter <= 0:
            self.lasersight = False
            self.laserlength = 0

        # KANASWITCH PowerUp
        if self.kanaswitch and self.kanaswitchcounter == 1000:
            Variables.RGB = [255,255,255]
            self.kanaswitchcounter -= 100 * Variables.dt
            if Variables.gamemode == 0:
                Variables.gamemode = 1
            else:
                Variables.gamemode = 0
        elif self.kanaswitch and self.kanaswitchcounter >= 0:
            self.kanaswitchcounter -= 100 * Variables.dt
        elif self.kanaswitch and self.kanaswitchcounter <= 0:
            if Variables.gamemode == 0:
                Variables.gamemode = 1
            else:
                Variables.gamemode = 0
            self.kanaswitch = False
            Variables.RGB = [255,255,255]

        # self.laserpower = int(Variables.score) + 1
        self.laserpower = int(Variables.score) * Constants.pew_array[Variables.pewtype]["laserpower"] + 1
        self.power_grapic = Constants.ui_font.render(str(self.laserpower), True, 'green')

    def draw(self,screen):
        self.movement()
        if Variables.shipcollision == False:
            if int(self.respawn_timer*100) % 3 == 0: self.image.set_alpha(200)
            elif int(self.respawn_timer*100) % 3 == 1: self.image.set_alpha(128)
            elif int(self.respawn_timer*100) % 3 == 2: self.image.set_alpha(16)
        else:
            self.image.set_alpha(255)
        screen.blit(self.image, self.spaceship_rect)
        if self.lasersight: screen.blit(self.laser,self.spaceship_rect.midright)

        # Draw hitbox
        if Variables.hitboxshow:
            screen.blit(self.power_grapic, self.spaceship_rect.topleft)
            pygame.draw.rect(screen, (255,0,0),self.spaceship_rect, 2)

    def collide(self,rect):
        if Variables.shipforcefield:
            x = abs(self.location[0] - (rect[0] + rect[2] / 2))
            y = abs(self.location[1] - (rect[1] + rect[3] / 2))

            if x > (rect[2] / 2 + self.shieldradius): return False
            if y > (rect[3] / 2 + self.shieldradius): return False

            if x <= (rect[2] / 2): return True
            if y <= (rect[3] / 2): return True

            corner_distance = (x - rect[2] / 2)**2 + (y - rect[3] / 2)**2
            return corner_distance <= self.shieldradius**2

        else:
            if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
                if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                    return True
        return False

    def respawn(self):
        Variables.lives -= 1
        self.respawn_timer = 3

class Pew:
    def __init__(self,x,y,image):
        self.x, self.y = x, y
        self.image = pygame.transform.scale(image,(Constants.pew_array[Variables.pewtype]["width"],Constants.pew_array[Variables.pewtype]["height"]))
        self.rect = self.image.get_rect(midleft = (self.x, self.y))
        self.velocity = Constants.pew_array[Variables.pewtype]["pewspeed"]
        self.hitbox = [0,0,0,0]

    def update(self):
        self.rect = self.image.get_rect(midleft = (self.x, self.y))
        self.hitbox = self.rect
        self.x += self.velocity * Variables.dt
        if self.x > Constants.WIDTH+500: Graphicgroups.bullets.pop(Graphicgroups.bullets.index(self))

    def draw(self,screen):
        screen.blit(self.image, self.rect)
        if Variables.hitboxshow: pygame.draw.rect(screen, (0,255,0),self.hitbox, 2)

    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False

    def spawn(player):
        if len(Graphicgroups.bullets) < Constants.pew_array[Variables.pewtype]["maxnumpew"]:
            if pygame.time.get_ticks() - player.last_pewtimer >= Constants.pew_array[Variables.pewtype]["pewrate"]:
                Graphicgroups.bullets.append(Pew(player.spaceship_rect.center[0],player.spaceship_rect.center[1],Constants.pew_surfs[Constants.pew_array[Variables.pewtype]["imgindx"]]))
                # pygame.mixer.Sound.play(pewsound)
                pygame.mixer.Sound.play(Constants.pew_sounds[Constants.pew_array[Variables.pewtype]["pewsound"]])
                player.last_pewtimer = pygame.time.get_ticks()

# ENVIRONMENT
class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x, self.y = Constants.WIDTH+500, random.randrange(0,Constants.HEIGHT)
        self.scale = random.randint(5,15)/10
        self.num = random.randint(0,len(Constants.planet_surfs)-1)
        self.image = Constants.planet_surfs[self.num]
        self.image = pygame.transform.scale(self.image,(self.image.get_width()*self.scale,self.image.get_height()*self.scale))
        self.rect = self.image.get_rect(center = (self.x,self.y))
        self.velocity = 50
    
    def update(self,player):
        self.rect = self.image.get_rect(center = (self.x,self.y))
        self.x -= self.velocity * Variables.dt
        if self.x < -500: self.kill()
    
    def spawn():
        Graphicgroups.planet_group.add(Planet())

class Star(pygame.sprite.Sprite):
    def __init__(self,velocity,x=Constants.WIDTH + 100):
        super().__init__()
        self.x, self.y = x, random.randrange(50,Constants.HEIGHT-50)
        self.kana = random.randint(0,45)
        self.menustar = random.randint(0,len(Constants.menustarmessage)*20)
        fontsize = 15
        star_font = pygame.font.SysFont(Constants.font_name, fontsize)
        if Variables.STATE == "GameOver": self.image = star_font.render('GAME OVER', True, 'white')
        elif Variables.STATE == "Menu" and self.menustar < len(Constants.menustarmessage): self.image = star_font.render(Constants.menustarmessage[self.menustar], True, 'white')
        else: self.image = star_font.render(Variables.commasep[self.kana][(Variables.gamemode+1)%2], False, 'white')
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.depth = random.randrange(100+velocity,1000+velocity)
        self.image.set_alpha((self.depth-velocity)/900*255)
        # self.gamemode = Variables.gamemode
        self.velocity = float(self.depth)

    def update(self,player):
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.x -= self.velocity * Variables.dt
        if self.x < -100: self.kill()

    def spawn(velocity):
        Graphicgroups.starfield_group.add(Star(velocity))

class Bridge(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        super().__init__()
        self.image = image
        self.x, self.y = x, y
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.velocity = 3000
        self.drawn = False
        self.sound = True
        TipTicker.spawn("Kana Swap",200)

    def update(self,player):
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.x -= self.velocity * Variables.dt
        Variables.last_kananum = Variables.kananum
        Variables.last_level = Variables.level
        if self.sound == True:
            pygame.mixer.Sound.play(Constants.bridgewhoosh)
            self.sound = False
        if self.x < Settings.question_position[0]-40 and self.x > Settings.question_position[0]-80 and self.drawn == False:
            Variables.kananum += 1
            if Variables.kananum >= len(Variables.gamekana[Variables.level]):
                Variables.kananum = 0
                if Variables.level < 9:
                    Variables.TRANSITION = True
                else:
                    random.shuffle(Variables.gamekana[Variables.level])
            self.drawn = True
            CutOffLine.spawn()

        if self.x < -1000:
            self.kill
            self.drawn = False

    def draw(self,screen):
        screen.blit(self.image, self.rect)

    def spawn():
        Variables.enemy_health_multiplier += 1
        Graphicgroups.bridge_group.add(Bridge(Constants.WIDTH,0,Constants.bridge_surf))

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, spritearray, scale, repeat):
        super().__init__()
        self.x, self.y = x, y
        self.animspeed = random.randint(40,100)
        self.index = 0
        self.counter = 0
        self.explosion_speed = 1
        self.spritearray = spritearray
        self.image = self.spritearray[self.index]
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.scale = scale
        self.repeat = repeat

    def update(self):
        self.counter += self.animspeed * Variables.dt
        if self.counter >= self.explosion_speed and self.index < len(self.spritearray) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.spritearray[self.index]
            self.image = pygame.transform.scale(self.image,(256 * self.scale,256 * self.scale))
            self.rect = self.image.get_rect(center = (self.x, self.y))
            
        if self.index >= len(self.spritearray) - 1 and self.counter >= self.explosion_speed:
            if self.repeat: self.index = 0
            else: self.kill()

class TipTicker(pygame.sprite.Sprite):
    def __init__(self,message,velocity):
        super().__init__()
        self.message = message
        tip_font = pygame.font.SysFont(Constants.font_name, 30)
        self.image = tip_font.render(self.message, True, 'yellow')
        self.messagebox = self.image.get_rect()
        self.x, self.y = Constants.WIDTH + self.messagebox.centerx, 60
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.velocity = velocity

    def update(self):
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.x -= self.velocity * Variables.dt
        if self.x < -1000: self.kill()

    def spawn(message,velocity):
        Graphicgroups.tip_group.add(TipTicker(message,velocity))

class SpaceJunk:
    def __init__(self,num,rotate,scale):
        self.image = pygame.image.load(os.getcwd() + Constants.spacejunkfiles[num][0]).convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.image.get_width()*scale,self.image.get_height()*scale))
        self.x, self.y = Constants.WIDTH+50, random.randrange(128,Constants.HEIGHT-128)
        self.velocity = 600
        self.rotate = 0
        self.rotate_rate = rotate / 100
        self.hitbox = None

    def update(self):
        orig_rect = self.image.get_rect()
        self.rotated_image = pygame.transform.rotate(self.image,self.rotate)
        rot_rect = orig_rect.copy()
        rot_rect.center = self.rotated_image.get_rect().center
        self.rotated_image = self.rotated_image.subsurface(rot_rect).copy()
        self.rect = self.rotated_image.get_rect(center = (self.x,self.y))
        self.hitbox = self.rect
        self.x -= self.velocity * Variables.dt
        self.rotate += self.rotate_rate
        if self.x < -100: Graphicgroups.spacejunk.pop(Graphicgroups.spacejunk.index(self))

    def draw(self,screen):
        screen.blit(self.rotated_image, self.rect)
        if Variables.hitboxshow == True: pygame.draw.rect(screen,'red',self.hitbox,2)

    def spawn():
        whichjunk = random.randint(0,len(Constants.spacejunkfiles)-1)
        junksize = random.randrange(2,10)
        Graphicgroups.spacejunk.append(SpaceJunk(whichjunk,random.randrange(-100,100),junksize*0.1))
        junkobject = pygame.mixer.Sound(os.getcwd() + Constants.spacejunkfiles[whichjunk][1])
        junkobject.set_volume(junksize*0.1)
        pygame.mixer.Sound.play(junkobject)

class CutOffLine:
    def __init__(self,x,y,kanatohit,lastkana):
        self.x, self.y = x, y
        self.lastkana = lastkana
        self.kanatohit = kanatohit
        self.last_kana_text = Constants.question_font.render(self.lastkana, True, 'white')
        self.next_kana_text = Constants.question_font.render(self.kanatohit, True, 'white')
        self.lkt_rect = self.last_kana_text.get_rect()
        self.nkt_rect = self.next_kana_text.get_rect()
        self.velocity = Settings.kanax_velocity
        self.kanaoffset = 40
        self.box = pygame.Rect(self.x,0,2,Constants.HEIGHT)

    def update(self,player):
        self.x -= self.velocity * Variables.dt
        self.box = pygame.Rect(self.x,0,2,Constants.HEIGHT)
        if self.x < -50: Graphicgroups.cuttoffline.pop(Graphicgroups.cuttoffline.index(self))

    def draw(self,screen):
        pygame.draw.rect(screen, (128,0,0), self.box, 2)
        screen.blit(self.last_kana_text, (self.x-self.kanaoffset-(self.lkt_rect.centerx), Constants.HEIGHT-64))
        screen.blit(self.next_kana_text, (self.x+self.kanaoffset-(self.nkt_rect.centerx), Constants.HEIGHT-64))
        screen.blit(self.last_kana_text, (self.x-self.kanaoffset-(self.lkt_rect.centerx), 64))
        screen.blit(self.next_kana_text, (self.x+self.kanaoffset-(self.nkt_rect.centerx), 64))

    def spawn():
        Graphicgroups.cuttoffline.append(CutOffLine(Constants.WIDTH+Constants.off_screen_offset,0,Variables.gamekana[Variables.level][Variables.kananum][2],Variables.gamekana[Variables.last_level][Variables.last_kananum][2]))

class BigLaser:
    def __init__(self,x,y):
        self.x, self.y = x, y
        self.image = Constants.biglaser_surf
        self.biglaser_rect = self.image.get_rect(center = (self.x, self.y))
        self.velocity = 8000
        self.hitboxYshrink = 50
        self.hitbox = [0,0,0,0]
    
    def update(self):
        self.x -= self.velocity * Variables.dt
        self.hitbox = self.biglaser_rect
        self.hitbox[1] += self.hitboxYshrink
        self.hitbox[3] -= (self.hitboxYshrink*2)
        if self.x < -512:
            Graphicgroups.biglasers.pop(Graphicgroups.biglasers.index(self))
            self.laserdelay = 100

    def draw(self,screen):
        self.image = pygame.transform.scale(self.image,(2048,256))
        self.biglaser_rect = self.image.get_rect(center = (self.x, self.y))
        screen.blit(self.image, self.biglaser_rect)
        if Variables.hitboxshow:
            pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)

    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False

    def spawn(y):
        Graphicgroups.biglasers.append(BigLaser(Constants.WIDTH+1000,y))
        pygame.mixer.Sound.play(Constants.biglaser_sound)

class BigLaserWarning:
    def __init__(self,y):
        self.last_warn_timer = 0
        self.opacity = True
        self.y = y
        self.image_flash_delay = 100
        self.warning_length = 10
        self.image = Constants.biglaser_warning_surf

    def update(self):
        if self.warning_length > 0:
            if pygame.time.get_ticks() - self.last_warn_timer >= self.image_flash_delay:
                if self.opacity == True:
                    self.opacity = False
                else:
                    self.opacity = True
                    pygame.mixer.Sound.play(Constants.warning_sound)
                self.warning_length -= 1
                self.last_warn_timer = pygame.time.get_ticks()
        if self.warning_length <= 0:
            pygame.mixer.Sound.stop(Constants.warning_sound)
            BigLaser.spawn(self.y)
            Graphicgroups.warnings.pop(Graphicgroups.warnings.index(self))

    def draw(self,screen):
        if self.opacity == True:
            self.warning_rect = self.image.get_rect(midright = (Constants.WIDTH, self.y))
            screen.blit(self.image, self.warning_rect)

    def spawn(player):
        Graphicgroups.warnings.append(BigLaserWarning(random.randint(player.spaceship_rect.center[1]-64,player.spaceship_rect.center[1]+64)))

class CenterWarning:
    def __init__(self,message,surface,scale):
        self.pos = (Constants.WIDTH // 2, Constants.HEIGHT // 2)
        self.alpha = 255
        self.message = message
        self.surf = surface
        self.scale = scale

    def update(self):
        self.alpha -= 100 * Variables.dt
        if self.alpha <= 0: Graphicgroups.centerwarning.pop(Graphicgroups.centerwarning.index(self))

    def draw(self):
        warning_text = Constants.WARNING_font.render(self.message, True, 'white')
        warning_text.set_alpha(self.alpha)
        self.surf_scaled = pygame.transform.scale(self.surf,(self.surf.get_rect().width*self.scale,self.surf.get_rect().height*self.scale))
        self.surf_scaled.set_alpha(self.alpha)
        centered_warning = warning_text.get_rect(center = self.pos)
        centered_image = self.surf_scaled.get_rect(center = self.pos)
        Constants.screen.blit(self.surf_scaled,centered_image)
        Constants.screen.blit(warning_text, centered_warning)

    def spawn(message,surface,scale=1):
        Graphicgroups.centerwarning.append(CenterWarning(message,surface,scale))

# INTERACTABLES
class Kana:
    def __init__(self,x,y,kana,fade,rotate,newmessage="",color='white',new=False):
        self.x, self.y = x, y
        self.newmessage = newmessage
        self.kanakill = int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3])*(255/Settings.num_to_shoot_new_kana)
        self.new = new
        if self.new: self.color = color
        else: self.color = 'white'
        self.xvelocity, self.yvelocity = Settings.kanax_velocity, random.randint(-Settings.kanay_velocity,Settings.kanay_velocity)
        self.shrink = 5
        self.kana = kana
        self.level = Variables.level
        self.fade = fade
        self.rotate = 0
        self.rotate_rate = (rotate * Variables.level) / 2
        self.kanasound = Variables.gamekana[self.level][self.kana][2]
        self.kanatext = Constants.kana_font.render(Variables.gamekana[self.level][self.kana][Variables.gamemode], True, self.color)
        self.kana_graphic = Constants.ui_font.render(Variables.gamekana[self.level][self.kana][0] + Variables.gamekana[self.level][self.kana][1] + Variables.gamekana[self.level][self.kana][2],True,'yellow')
        self.kanascale = 1
        self.orig_rect = self.kanatext.get_rect()
        self.rotated_image = pygame.transform.rotate(self.kanatext,self.rotate)
        self.rot_rect = self.orig_rect.copy()
        self.rot_rect.center = self.rotated_image.get_rect().center
        self.rotated_image = self.rotated_image.subsurface(self.rot_rect).copy()
        self.scale_image = pygame.transform.scale(self.rotated_image,(self.kanatext.get_rect().width*self.kanascale,self.kanatext.get_rect().height*self.kanascale))
        self.centered_image = self.scale_image.get_rect(center = (self.x,self.y))
        self.hitbox = [0,0,0,0]

    def update(self,player):
        self.kanatext = Constants.kana_font.render(Variables.gamekana[self.level][self.kana][Variables.gamemode], True, self.color)
        self.kana_graphic = Constants.ui_font.render(Variables.gamekana[self.level][self.kana][0] + Variables.gamekana[self.level][self.kana][1] + Variables.gamekana[self.level][self.kana][2],True,'yellow')
        self.x -= self.xvelocity * Variables.dt
        if self.y > Settings.ship_screen_boundary and self.y < Constants.HEIGHT - Settings.ship_screen_boundary:
            self.y += self.yvelocity * Variables.dt

    def draw(self,screen):
        # self.kanatext = pygame.transform.scale(self.kanatext,(self.kanatext.get_rect().width*self.kanascale,self.kanatext.get_rect().height*self.kanascale))
        self.orig_rect = self.kanatext.get_rect()
        self.rotated_image = pygame.transform.rotate(self.kanatext,self.rotate)
        self.rot_rect = self.orig_rect.copy()
        self.rot_rect.center = self.rotated_image.get_rect().center
        self.rotated_image = self.rotated_image.subsurface(self.rot_rect).copy()
        self.scale_image = pygame.transform.scale(self.rotated_image,(self.kanatext.get_rect().width*self.kanascale,self.kanatext.get_rect().height*self.kanascale))
        self.centered_image = self.scale_image.get_rect(center = (self.x,self.y))
        screen.blit(self.scale_image, self.centered_image)
        self.rotate += self.rotate_rate * Variables.dt

        # Highlight new
        if self.new:
            # pygame.draw.circle(screen,(0,0,255),self.centered_image.topright, 4)
            top_right_of_kana = (self.centered_image.topright[0],self.centered_image.topright[1])
            alpha = 255 - self.kanakill
            if alpha <= 0: alpha = 0

            shoot_here_surf = pygame.Surface((200,100),pygame.SRCALPHA)
            shoot_here_pos = shoot_here_surf.get_rect(bottomleft = (top_right_of_kana))
            # pygame.draw.circle(screen,'blue',top_right_of_kana,3)
            pygame.draw.line(shoot_here_surf,'red',(0,125),(25,50),1)
            shoot_text = Constants.kana_ui_font.render(self.newmessage,True,(255,0,0))
            shoot_here_surf.set_alpha(alpha)
            shoot_here_surf.blit(shoot_text,(0,25))

            screen.blit(shoot_here_surf, shoot_here_pos)

        # Draw hitbox
        self.hitbox = self.centered_image
        if Variables.hitboxshow:
            screen.blit(self.kana_graphic,self.centered_image.bottomleft)
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
        self.hitbox = [0,0,0,0]
        self.shieldradius = 32

    def update(self,player):
        self.x -= self.xvelocity * Variables.dt
        self.y += self.yvelocity * Variables.dt * math.sin(self.x/100)
        if self.x < -64:
            Graphicgroups.powerups.pop(Graphicgroups.powerups.index(self))

# class PowerUp:
#     def __init__(self,x,y,xvelocity,yvelocity,image,pueffect):
#         self.spritearray = Constants.enemy_spritesheet_surfs #Sprite Animation
#         self.animindex = 0  #Sprite Animation
#         self.animspeed = random.randint(10,20) #Sprite Animation
#         self.image = self.spritearray.images[self.animindex] #Sprite Animation
#         self.pueffect = pueffect
#         self.img = image
#         self.img = pygame.transform.scale(self.img,(64,64))
#         self.x, self.y = x, y
#         self.xvelocity, self.yvelocity = xvelocity, yvelocity
#         self.hitbox = [0,0,0,0]
#         self.shieldradius = 32

#     def update(self,player):
#         self.x -= self.xvelocity * Variables.dt
#         self.y += self.yvelocity * Variables.dt * math.sin(self.x/100)
#         if self.x < -64:
#             Graphicgroups.powerups.pop(Graphicgroups.powerups.index(self))

    def draw(self,screen):
        self.hitbox = self.img_rect = self.img.get_rect(center = (self.x, self.y))
        self.img.set_alpha(255)
        self.img_rect = self.img.get_rect(center = (self.x, self.y))
        screen.blit(self.img, self.img_rect)

        # Draw hitbox
        if Variables.hitboxshow:
            pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)

    def spawn(graphic,effect):
        Graphicgroups.powerups.append(PowerUp(Constants.WIDTH+64, random.randrange(128,Constants.HEIGHT-128,),100,random.randrange(100,200),graphic,effect))

    def collide(self,rect):
        x = abs(self.x - (rect[0] + rect[2] / 2))
        y = abs(self.y - (rect[1] + rect[3] / 2))

        if x > (rect[2] / 2 + self.shieldradius): return False
        if y > (rect[3] / 2 + self.shieldradius): return False

        if x <= (rect[2] / 2): return True
        if y <= (rect[3] / 2): return True

        corner_distance = (x - rect[2] / 2)**2 + (y - rect[3] / 2)**2
        return corner_distance <= self.shieldradius**2
    
    def effect(self,pueffect,player):
        if pueffect == "laser":
            if self.collide(player.spaceship_rect):
                Graphicgroups.powerups.pop(Graphicgroups.powerups.index(self))
                player.lasersight = True
                player.lasersightcounter = player.poweruptimelength
                pygame.mixer.Sound.play(Constants.powerup_sound)
                pygame.mixer.Sound.play(Constants.shiplaser_sound)
        if pueffect == "speed":
            if self.collide(player.spaceship_rect):
                Graphicgroups.powerups.pop(Graphicgroups.powerups.index(self))
                player.speedboost = True
                player.speedboostcounter = player.poweruptimelength
                pygame.mixer.Sound.play(Constants.powerup_sound)
        if pueffect == "switch":
            if self.collide(player.spaceship_rect):
                Graphicgroups.powerups.pop(Graphicgroups.powerups.index(self))
                player.kanaswitch = True
                player.kanaswitchcounter = player.poweruptimelength
                pygame.mixer.Sound.play(Constants.powerup_sound)
        if pueffect == "1up":
            if self.collide(player.spaceship_rect):
                Graphicgroups.powerups.pop(Graphicgroups.powerups.index(self))
                Variables.lives += 1
                pygame.mixer.Sound.play(Constants.powerup_sound)
        if pueffect == "powerup":
            if self.collide(player.spaceship_rect):
                Graphicgroups.powerups.pop(Graphicgroups.powerups.index(self))
                if Variables.pewtype < len(Constants.pew_array)-1:
                    Variables.pewtype += 1
                    pygame.mixer.Sound.play(Constants.powerup_sound)
                else: Variables.pewtype = 0

class Enemies:
    def __init__(self,typeof):
        self.type = typeof
        self.spritearray = Constants.enemy_spritesheet_surfs #Sprite Animation
        self.animindex = 0  #Sprite Animation
        self.animspeed = random.randint(10,20) #Sprite Animation
        self.image = self.spritearray[self.type].images[self.animindex] #Sprite Animation
        self.x, self.y = Constants.WIDTH, random.randrange(128,Constants.HEIGHT-128)
        self.enemy_rect = self.image.get_rect(midleft = (self.x, self.y))
        self.velocity = random.randint(50,200)
        self.Yvelocity = random.randint(-50,50)
        self.knockbackx = 0
        self.knockbacky = 0
        self.last_enemy_pew = 0

        # self.maxhealth = random.randint(int((Variables.enemy_health_multiplier * enemy_health)*0.8) + 1,Variables.enemy_health_multiplier * enemy_health + 1)
        self.maxhealth = Variables.generatedcorrectkanacounter + 1
        self.health = self.maxhealth
        self.maxhealth_grapic = Constants.ui_font.render(str(self.maxhealth), True, 'green')
        self.curhealth_grapic = Constants.ui_font.render(str(self.health), True, 'yellow')
        self.healthbar_height = 5
        self.healthbar = pygame.Surface((self.enemy_rect.width,5))
        self.healthbar_Color = (255-(255/self.maxhealth*self.health),255/self.maxhealth*self.health,0)

    def calculate_angles(self,number_of_angles):
        if number_of_angles < 1:
            return []
        
        angle_step = 360 / number_of_angles
        angles = [i * angle_step for i in range(number_of_angles)]
        return angles

    def animate(self):
        self.animindex += self.animspeed * Variables.dt
        if self.animindex > len(self.spritearray[self.type].images)-1: self.animindex = 0
        self.image = self.spritearray[self.type].images[int(self.animindex)]

    def update(self):
        self.healthdisplay = self.enemy_rect.width/self.maxhealth*self.health
        self.healthbar_Color = (255-(255/self.maxhealth*self.health),255/self.maxhealth*self.health,0)
        self.curhealth_grapic = Constants.ui_font.render(str(self.health), True, 'yellow')
        self.animate()
        if self.type%3 == 0 or self.type%3 == 1:
            self.enemy_rect = self.image.get_rect(midleft = (self.x, self.y))
        elif self.type%3 == 2:
            self.enemy_rect = self.image.get_rect(center = (self.x, self.y))
        self.x -= (self.velocity - self.knockbackx) * Variables.dt
        self.y -= (self.Yvelocity - self.knockbacky) * Variables.dt
        if self.knockbackx > 0: self.knockbackx -= Settings.enemy_knockback_recoveryx * Variables.dt
        if self.knockbacky > 0: self.knockbacky -= Settings.enemy_knockback_recoveryy * Variables.dt
        if self.knockbacky < 0: self.knockbacky += Settings.enemy_knockback_recoveryy * Variables.dt
        if self.x < -128:
            Graphicgroups.enemies.pop(Graphicgroups.enemies.index(self))
    
    def findobjectangle(self,player):
            # Find angle of player
            dx = self.x - player.spaceship_rect.center[0]
            dy = self.y - player.spaceship_rect.center[1]
            self.theta = math.atan2(-dy,dx)
            return self.theta

    def shoot(self,player):
        angle = self.findobjectangle(player)
        if pygame.time.get_ticks() - self.last_enemy_pew >= random.randint(2000,10000):
            if self.type%3 == 0: # AIMED SHOT
                if angle < math.pi/3 and angle > -math.pi/3:
                    pygame.mixer.Sound.play(Constants.enemypew_sound)
                    Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,angle))
            elif self.type%3 == 1: # FORWARD SHOT
                pygame.mixer.Sound.play(Constants.enemypew_sound)
                Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,math.radians(random.randint(-10,10))))
            elif self.type%3 == 2: #AoE SHOT
                pygame.mixer.Sound.play(Constants.enemypew_sound)
                for angle in self.calculate_angles(8):
                    Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,math.radians(random.randint(angle-10,angle+10))))
            self.last_enemy_pew = pygame.time.get_ticks()

    def draw(self,screen,player):
        screen.blit(self.image, self.enemy_rect)
        
        screen.blit(self.healthbar, (self.enemy_rect.left,self.enemy_rect.top-20,self.enemy_rect.width,10))
        self.healthbar.fill('black')
        try: pygame.draw.rect(self.healthbar,self.healthbar_Color,(0,0,self.healthdisplay,self.healthbar_height))
        except: pass

        self.hitbox = self.enemy_rect
        if Variables.hitboxshow:
            screen.blit(self.maxhealth_grapic, self.enemy_rect.topright)
            screen.blit(self.curhealth_grapic, self.enemy_rect.topleft)
            pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)
            pygame.draw.line(screen, (255,255,0), (self.x, self.y),player.spaceship_rect.center)

    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return (self.hitbox[1]-rect[1]+32)*8
        return False

    def spawn():
        # enemies.append(Enemies(random.randint(0,2)))
        Graphicgroups.enemies.append(Enemies(random.randint(0,3)))

class Bosses:
    def __init__(self,typeof,health,bossimage,numofbullets,Xvel,Yvel,anglenum,animspeed):
        self.spritearray = Constants.boss_spritesheet_surfs
        self.bossimage = bossimage
        self.enter_screen = False
        self.animindex = 0
        self.animspeed = animspeed
        self.rapidfire = 0
        self.lastrapidfire = 0
        self.numberofbullets = numofbullets
        self.bulletfrequency = 1
        self.anglenum = anglenum
        self.x, self.y = Constants.WIDTH, random.randrange(128,Constants.HEIGHT-128)
        self.type = typeof
        self.image = self.spritearray[self.bossimage].images[self.animindex]
        self.boss_rect = self.image.get_rect(midleft = (self.x, self.y))
        self.velocity = random.randint(Xvel/10,Xvel)
        self.Yvelocity = random.randint(-Yvel,Yvel)
        self.last_enemy_pew = 0
        self.maxhealth = health
        self.health = self.maxhealth
        self.maxhealth_grapic = Constants.ui_font.render(str(self.maxhealth), True, 'green')
        self.curhealth_grapic = Constants.ui_font.render(str(self.health), True, 'yellow')
        self.healthbar_height = 5
        self.healthbar = pygame.Surface((self.boss_rect.width,5))
        self.healthbar_Color = (255-(255/self.maxhealth*self.health),255/self.maxhealth*self.health,0)

    def calculate_angles(self,number_of_angles):
        if number_of_angles < 1:
            return []
        
        angle_step = 360 / number_of_angles
        angles = [i * angle_step for i in range(number_of_angles)]
        return angles

    def animate(self):
        self.animindex += self.animspeed * Variables.dt
        if self.animindex > len(self.spritearray[self.bossimage].images)-1: self.animindex = 0
        self.image = self.spritearray[self.bossimage].images[int(self.animindex)]

    def update(self):
        self.healthdisplay = self.boss_rect.width/self.maxhealth*self.health
        self.healthbar_Color = (255-(255/self.maxhealth*self.health),255/self.maxhealth*self.health,0)
        self.curhealth_grapic = Constants.ui_font.render(str(self.health), True, 'yellow')
        self.animate()
        if self.type%3 == 0 or self.type%3 == 1: self.boss_rect = self.image.get_rect(midleft = (self.x, self.y))
        elif self.type%3 == 2: self.boss_rect = self.image.get_rect(center = (self.x, self.y))
        self.x -= self.velocity * Variables.dt
        self.y += self.Yvelocity * Variables.dt
        if self.y <= 50 or self.y >= Constants.HEIGHT-50: self.Yvelocity *= -1
        if self.x <= 3*Constants.WIDTH/5:
            self.enter_screen = True
            self.velocity *= -1
        if self.x > Constants.WIDTH and self.enter_screen == True:
            self.velocity *= -1
    
    def findobjectangle(self,player):
            # Find angle of player
            dx = self.x - player.spaceship_rect.center[0]
            dy = self.y - player.spaceship_rect.center[1]
            self.theta = math.atan2(-dy,dx)
            return self.theta

    def shoot(self,player):
        angle = self.findobjectangle(player)
        if self.rapidfire > self.numberofbullets:
            self.rapidfire = 0
            self.lastrapidfire = 0
        if pygame.time.get_ticks() - self.last_enemy_pew >= random.randint(2000,10000) or self.rapidfire != 0:
            if self.type%3 == 0: # AIMED SHOT
                if angle < math.pi/3 and angle > -math.pi/3:
                    if int(self.rapidfire) - self.lastrapidfire == self.bulletfrequency:
                        pygame.mixer.Sound.play(Constants.enemypew_sound)
                        Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,angle))
                        self.lastrapidfire = int(self.rapidfire)
                    self.rapidfire += 10 * Variables.dt
            elif self.type%3 == 1: # FORWARD SHOT
                if int(self.rapidfire) - self.lastrapidfire == self.bulletfrequency:
                    pygame.mixer.Sound.play(Constants.enemypew_sound)
                    Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,math.radians(random.randint(-10,10))))
                    self.lastrapidfire = int(self.rapidfire)
                self.rapidfire += 10 * Variables.dt
            elif self.type%3 == 2: #AoE SHOT
                if int(self.rapidfire) - self.lastrapidfire == 5*self.bulletfrequency:
                    pygame.mixer.Sound.play(Constants.enemypew_sound)
                    for angle in self.calculate_angles(self.anglenum):
                        Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,math.radians(angle)))
                    self.lastrapidfire = int(self.rapidfire)
                self.rapidfire += 10 * Variables.dt                
            self.last_enemy_pew = pygame.time.get_ticks()

    def draw(self,screen,player):
        screen.blit(self.image, self.boss_rect)
        
        screen.blit(self.healthbar, (self.boss_rect.left,self.boss_rect.top-20,self.boss_rect.width,10))
        self.healthbar.fill('black')
        try: pygame.draw.rect(self.healthbar,self.healthbar_Color,(0,0,self.healthdisplay,self.healthbar_height))
        except: pass

        self.hitbox = self.boss_rect
        if Variables.hitboxshow:
            screen.blit(self.maxhealth_grapic, self.boss_rect.topright)
            screen.blit(self.curhealth_grapic, self.boss_rect.topleft)
            pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)
            pygame.draw.line(screen, (255,255,0), (self.x, self.y),player.spaceship_rect.center)

    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False

    def spawn():
        Graphicgroups.bosses.append(
            Bosses(
                Constants.bosses_array[Variables.level]["type"],
                (Variables.generatedincorrectkanacounter + Variables.generatedcorrectkanacounter)*Constants.bosses_array[Variables.level]["healthmultiplier"],
                Constants.bosses_array[Variables.level]["imgindx"],
                Constants.bosses_array[Variables.level]["numofbullets"],
                Constants.bosses_array[Variables.level]["Xvel"],
                Constants.bosses_array[Variables.level]["Yvel"],
                Constants.bosses_array[Variables.level]["anglenum"],
                Constants.bosses_array[Variables.level]["animspeed"],
            )
        )

class EnemyProjectiles:
    def __init__(self,x,y,direction):
        self.x, self.y = x, y
        self.direction = direction
        self.skewoffset = 20
        self.directionskew = random.randint(-self.skewoffset,self.skewoffset)/100
        self.image = Constants.enemy_pew_surf
        self.image = pygame.transform.scale(self.image,(32, 32))
        self.enemy_pew_rect = self.image.get_rect(center = (self.x, self.y))
        self.velocity = 500
        self.hitradius = 16
        self.hitbox = [0,0,0,0]

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
        if self.x < 0 or self.y < 0 or self.y > Constants.HEIGHT:
            Graphicgroups.enemyprojectiles.pop(Graphicgroups.enemyprojectiles.index(self))

    def draw(self,screen):
        # self.update()
        screen.blit(self.image, self.enemy_pew_rect)

        self.hitbox = self.enemy_pew_rect
        if Variables.hitboxshow:
            # pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)
            pygame.draw.circle(screen,'red',(self.x,self.y),self.hitradius,2)

    def collide(self,rect):
        x = abs(self.x - (rect[0] + rect[2] / 2))
        y = abs(self.y - (rect[1] + rect[3] / 2))

        if x > (rect[2] / 2 + self.hitbox[2]/2): return False
        if y > (rect[3] / 2 + self.hitbox[3]/2): return False

        if x <= (rect[2] / 2): return True
        if y <= (rect[3] / 2): return True

        corner_distance = (x - rect[2] / 2)**2 + (y - rect[3] / 2)**2
        return corner_distance <= self.hitradius**2
    
    def spawn():
        Graphicgroups.enemyprojectiles.append(EnemyProjectiles())

class WallOfDeath:
    def __init__(self,x,y):
        self.x, self.y = x, y
        self.velocity = 50
        self.image = Constants.wallsegment_surf

    def update(self):
        self.x -= self.velocity * Variables.dt
        if self.x < -32: Graphicgroups.wallsegments.pop(Graphicgroups.wallsegments.index(self))
        self.wallpiece_rect = self.image.get_rect(topleft = (self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.wallpiece_rect)

        self.hitbox = self.wallpiece_rect
        if Variables.hitboxshow:
            pygame.draw.circle(screen,(0,0,255),(self.x,self.y), 4)
            pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False

    def spawn(x,y):
        for w in range(random.randint(1,5)):
            for h in range(int(Constants.HEIGHT/32)):
                Graphicgroups.wallsegments.append(WallOfDeath(x+w*32,y+h*32))

class Debris:
    def __init__(self,x,y,direction,velocity,image,origin):
        self.x, self.y = x, y
        self.direction = direction
        self.skewoffset = 20
        self.directionskew = random.randint(-self.skewoffset,self.skewoffset)/100
        self.velocity = velocity
        self.image = image
        self.rotate = 0
        self.rotate_rate = random.randint(-100,100)
        self.debrisscale = 1
        self.debris_rect = self.image.get_rect(center = (self.x, self.y))
        self.hitradius = self.image.get_rect().centerx
        self.hitbox = [0,0,0,0]
        self.origin = origin

    def objectdirection(self,direction):
        pewdir = direction - math.pi/2 + self.directionskew
        sin_a = math.sin(pewdir)
        cos_a = math.cos(pewdir)
        self.x += self.velocity * sin_a * Variables.dt
        self.y += self.velocity * cos_a * Variables.dt
        return self.x, self.y

    def update(self):
        # self.x -= self.velocity * Variables.dt
        self.x, self.y = self.objectdirection(self.direction)
        if self.x < -32 or self.x > Constants.WIDTH or self.y < -10 or self.y > Constants.HEIGHT: Graphicgroups.debris.pop(Graphicgroups.debris.index(self))
        self.debris_rect = self.image.get_rect(center = (self.x, self.y))

    def draw(self, screen):
        self.orig_rect = self.image.get_rect()
        self.rotated_image = pygame.transform.rotate(self.image,self.rotate)
        self.rot_rect = self.orig_rect.copy()
        self.rot_rect.center = self.rotated_image.get_rect().center
        self.rotated_image = self.rotated_image.subsurface(self.rot_rect).copy()
        self.scale_image = pygame.transform.scale(self.rotated_image,(self.image.get_rect().width*self.debrisscale,self.image.get_rect().height*self.debrisscale))
        self.centered_image = self.scale_image.get_rect(center = (self.x,self.y))
        screen.blit(self.scale_image, self.centered_image)
        self.rotate += self.rotate_rate * Variables.dt

        self.hitbox = self.debris_rect
        if Variables.hitboxshow:
            pygame.draw.circle(screen,(0,0,255),(self.x,self.y), 4)
            pygame.draw.circle(screen,'red',(self.x,self.y),self.hitradius,2)

    def collide(self, rect):
        x = abs(self.x - (rect[0] + rect[2] / 2))
        y = abs(self.y - (rect[1] + rect[3] / 2))

        if x > (rect[2] / 2 + self.hitbox[2]/2): return False
        if y > (rect[3] / 2 + self.hitbox[3]/2): return False

        if x <= (rect[2] / 2): return True
        if y <= (rect[3] / 2): return True

        corner_distance = (x - rect[2] / 2)**2 + (y - rect[3] / 2)**2
        return corner_distance <= self.hitradius**2

    def spawn(x,y,direction,velocity,image,origin):
        for _ in range(random.randint(1,3)):
            Graphicgroups.debris.append(Debris(x,y,direction,velocity,image,origin))

class Damagenum:
    def __init__(self,x,xvel,y,damage):
        self.x, self.y, self.orgy = x, y-32, y-32
        self.xvelocity, self.yvelocity = xvel, 100
        damage_font = pygame.font.SysFont(Constants.font_name, 20)
        self.image = damage_font.render(str(damage), True, 'yellow')
        self.alpha = 255

    def update(self):
        self.y -= self.yvelocity * Variables.dt
        self.x -= (self.xvelocity - 50) * Variables.dt
        self.alpha -= 0.5
        if self.y < self.orgy - 200: Graphicgroups.damagenumbers.pop(Graphicgroups.damagenumbers.index(self))

    def draw(self, screen):
        self.update()
        self.image.set_alpha(int(self.alpha))
        screen.blit(self.image, (self.x, self.y))

    def spawn(x,xvel,y,damage):
        Graphicgroups.damagenumbers.append(Damagenum(x,xvel,y,damage))

player = Ship(0,Constants.HEIGHT//2,Constants.spaceship_surfs)