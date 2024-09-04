import Variables, Constants, Settings, Graphicgroups
import pygame, math, random, os

# PLAYER
class Ship:
    def __init__(self,x,y):
        self.type = 0
        self.lives = 5
        self.shipcollision = False
        self.spritearray = Constants.spaceship_surfs
        self.flamearray = Constants.spaceship_flame_surfs
        self.animindex = 0
        self.animspeed = 10
        self.image = self.spritearray[self.type].images[self.animindex]
        self.location = pygame.math.Vector2(x,y)
        self.spaceship_rect = self.image.get_rect(center = self.location)
        self.deadzone = 20
        self.Xvelocity, self.Yvelocity = 0, 0
        self.speed = Settings.ship_normal_top_speed
        self.acceleration, self.deceleration = self.speed*3, self.speed*4
        self.shiprest = 100
        self.pewtype = 0
        self.speedup, self.slowdown = 2, 1
        self.last_pewtimer = 0
        self.maxnumpew = 2
        self.shipborder = Settings.ship_screen_boundary
        self.respawn_timer = -1
        self.hitbox = [0,0,0,0]
        self.shield = False
        self.shieldradius = 64
        self.laserpower = int(Variables.score) * Constants.pew_array[self.pewtype]["laserpower"] + 1
        self.power_grapic = Constants.ui_font.render(str(self.laserpower), True, 'green')

        # Flames
        self.xflamedir, self.yflamedir = 0, 0
        self.xflameindex, self.yflameindex = 0, 0
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

    def flame(self,xdir,ydir):
        if xdir != None:
            self.xflameindex += self.flamespeed * Variables.delta_time
            if self.xflameindex > 12: self.xflameindex = 5
            self.xflameimage = pygame.transform.rotate(self.flamearray.images[int(self.xflameindex)],xdir)
            if xdir == 0:self.xflame_rect = self.xflameimage.get_rect(midleft = self.spaceship_rect.center)
            elif xdir == 180:self.xflame_rect = self.xflameimage.get_rect(midright = self.spaceship_rect.center)
        if ydir != None:
            self.yflameindex += self.flamespeed * Variables.delta_time
            if self.yflameindex > 12: self.yflameindex = 5
            self.yflameimage = pygame.transform.rotate(self.flamearray.images[int(self.yflameindex)],ydir)
            if ydir == -90:self.yflame_rect = self.yflameimage.get_rect(midtop = self.spaceship_rect.center)
            elif ydir == 90:self.yflame_rect = self.yflameimage.get_rect(midbottom = self.spaceship_rect.center)

    def animate(self):
        import Functions
        Functions.moanimate(self)

    def movement(self):
        keys = pygame.key.get_pressed()
        self.temp_acc = self.acceleration * Variables.delta_time
        self.temp_dec = self.deceleration * Variables.delta_time

        #region Vecors
        # Horizontal
        if keys[pygame.K_a]: 
            self.flame(0,None)
            Constants.screen.blit(self.xflameimage, self.xflame_rect)
            if self.Xvelocity <= self.speed:
                self.Xvelocity += self.temp_acc
        elif keys[pygame.K_d] and self.location[0] < Constants.WIDTH-200:
            self.flame(180,None)
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
            self.flame(None,-90)
            Constants.screen.blit(self.yflameimage, self.yflame_rect)
            if self.Yvelocity <= self.speed:
                self.Yvelocity += self.temp_acc
        elif keys[pygame.K_s]:
            self.flame(None,90)
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

        # Pew #TODO Add functionality to allow for longer presses of K_SPACE
        if keys[pygame.K_SPACE]:
            Pew.spawn(self)    

    def move(self):
        self.location[0] -= (self.Xvelocity + Settings.ship_fallbackspeed) * Variables.delta_time       # Movement in the X direction
        self.location[1] -= self.Yvelocity * Variables.delta_time                                       # Movement in the Y direction
        if self.location[1] < self.shipborder:                                                          # Do not move too far Up out of the screen
            self.location[1] = self.shipborder                                                          # Reset position to Up screen border
            self.Yvelocity = 0                                                                          # Reset Velocity to 0
        elif self.location[1] > Constants.HEIGHT-self.shipborder:                                       # Do not move too far Down out of the screen
            self.location[1] = Constants.HEIGHT-self.shipborder                                         # Reset position to Down screen border
            self.Yvelocity = 0                                                                          # Reset Velocity to 0
        elif self.location[0] <= 48:                                                                    # Do not move too far Left out of the screen
            self.location[0] = 48                                                                       # Reset position to Left screen border
        self.spaceship_rect.center = self.location                                                      # Set the position of the center of the ship sprite

    def respawn_checker(self):
        # RESPAWN
        if self.respawn_timer == 3:
            pygame.mixer.Sound.stop(Constants.shiplaser_sound)
            self.shipcollision = False
            self.lasersight = False
            self.speedboost = False
            self.location = pygame.math.Vector2(100, Constants.HCENTER)
            self.respawn_timer -= 1 * Variables.delta_time
        elif self.respawn_timer > 0:
            self.respawn_timer -= 1 * Variables.delta_time
        elif self.respawn_timer <= 0 and self.respawn_timer > -1:
            if Variables.STATE != "intro": self.shipcollision = True
            self.respawn_timer -= 1 * Variables.delta_time
        elif self.respawn_timer < -1: self.respawn_timer = -1

    def apply_powerups(self):
        #region SPEED BOOST PowerUp
        if self.speedboost and self.speedboostcounter > 0:
            self.speed = Settings.ship_boosted_top_speed
            self.acceleration = self.speed*Settings.ship_boosted_acceleration
            self.deceleration = self.speed*Settings.ship_boosted_deceleration
            self.speedboostcounter -= 100 * Variables.delta_time
        else:
            self.speed = Settings.ship_normal_top_speed
            self.acceleration = self.speed*Settings.ship_normal_acceleration
            self.deceleration = self.speed*Settings.ship_normal_deceleration
            self.speedboost = False
        #endregion SPEED BOOST PowerUp

        #region LASER PowerUp
        if self.lasersight and self.lasersightcounter > 256:                                    # Lasersight activated
            self.laser = pygame.Surface((self.laserlength,2))
            self.laser.set_alpha(128)
            self.laser.fill((255,0,0))
            self.lasersightcounter -= 100 * Variables.delta_time
            self.laserlength += 3000 * Variables.delta_time
        elif self.lasersight and self.lasersightcounter <= 256 and self.lasersightcounter > 0:  # Lasersight maintain
            self.laser = pygame.Surface((Constants.WIDTH,2))
            self.laser.fill((self.lasersightcounter/2,0,0))
            self.lasersightcounter -= 100 * Variables.delta_time
        elif self.lasersight and self.lasersightcounter <= 0:                                   # Lasersight has ended
            self.lasersight = False
            self.laserlength = 0
        #endregion LASER PowerUp

        #region KANASWITCH PowerUp
        if self.kanaswitch and self.kanaswitchcounter == 1000:
            TipTicker.spawn("Kanaswitch: Do you remember the other Kana?", 300)
            Variables.RGB = [255,255,255]
            self.kanaswitchcounter -= 100 * Variables.delta_time
            if Variables.gamemode == 0:
                Variables.gamemode = 1
            else:
                Variables.gamemode = 0
        elif self.kanaswitch and self.kanaswitchcounter >= 0:
            self.kanaswitchcounter -= 100 * Variables.delta_time
        elif self.kanaswitch and self.kanaswitchcounter <= 0:
            if Variables.gamemode == 0:
                Variables.gamemode = 1
                self.kanaswitchcounter = 1000
            else:
                Variables.gamemode = 0
                self.kanaswitchcounter = 1000
            self.kanaswitch = False
            Variables.RGB = [255,255,255]
        #endregion KANASWITCH PowerUp

    def update(self):
        self.animate()
        self.move()
        self.respawn_checker()
        self.apply_powerups()

        # self.laserpower = int(Variables.score) + 1
        self.laserpower = int(Variables.score) * Constants.pew_array[player.pewtype]["laserpower"] + 1
        self.power_grapic = Constants.ui_font.render(str(self.laserpower), True, 'green')

    def draw(self,screen):
        self.movement()
        if self.shipcollision == False:
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
        self.lives -= 1
        self.respawn_timer = 3
        player.pewtype = 0

class Pew:
    def __init__(self,x,y,image):
        self.x, self.y = x, y
        self.image = pygame.transform.scale(image,(Constants.pew_array[player.pewtype]["width"],Constants.pew_array[player.pewtype]["height"]))
        self.rect = self.image.get_rect(midleft = (self.x, self.y))
        self.velocity = Constants.pew_array[player.pewtype]["pewspeed"]
        self.hitbox = [0,0,0,0]

    def animate(self):
        self.animindex += self.animspeed * Variables.delta_time #length of ime before we advance the animation frame
        if self.animindex > len(self.spritearray.images)-1: self.animindex = 0 # reset the frame to 0 if we try to go beyond the array
        self.image = self.spritearray.images[int(self.animindex)] # update the current frame

    def update(self):
        self.rect = self.image.get_rect(midleft = (self.x, self.y))
        self.hitbox = self.rect
        self.x += self.velocity * Variables.delta_time
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
        if len(Graphicgroups.bullets) < Constants.pew_array[player.pewtype]["maxnumpew"]:
            if pygame.time.get_ticks() - player.last_pewtimer >= Constants.pew_array[player.pewtype]["pewrate"]:
                Graphicgroups.bullets.append(Pew(
                    player.spaceship_rect.center[0],
                    player.spaceship_rect.center[1],
                    Constants.pew_surfs[Constants.pew_array[player.pewtype]["imgindx"]]
                ))
                pygame.mixer.Channel(8).play(Constants.pew_sounds[Constants.pew_array[player.pewtype]["pewsound"]])
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
        self.x -= self.velocity * Variables.delta_time
        if self.x < -500: self.kill()
    
    def spawn():
        Graphicgroups.planet_group.add(Planet())

class Star(pygame.sprite.Sprite):
    def __init__(self,velocity,x=Constants.WIDTH + 100):
        super().__init__()
        self.menustarmessage = [
            "Music by Nerdthagoras",
            "SUBSCRIBE",
            "Also on Twtich",
            "Please Donate!",
            "This is a long string of text",
        ]
        self.x, self.y = x, random.randrange(50,Constants.HEIGHT-50)
        self.kana = random.randint(0,45)
        self.menustar = random.randint(0,len(self.menustarmessage)*20)
        fontsize = 15
        star_font = pygame.font.SysFont(Constants.font_name, fontsize)
        if Variables.STATE == "GameOver": self.image = star_font.render('GAME OVER', True, 'white')
        elif Variables.STATE == "Menu" and self.menustar < len(self.menustarmessage): self.image = star_font.render(self.menustarmessage[self.menustar], True, 'white')
        else: self.image = star_font.render(Variables.commasep[self.kana][(Variables.gamemode+1)%2], False, 'white')
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.depth = random.randrange(100+velocity,1000+velocity)
        self.image.set_alpha((self.depth-velocity)/900*255)
        # self.gamemode = Variables.gamemode
        self.velocity = float(self.depth)

    def update(self,player):
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.x -= self.velocity * Variables.delta_time
        if self.x < -100: self.kill()

    def spawn(velocity):
        Graphicgroups.starfield_group.add(Star(velocity))

class Bridge(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        super().__init__()
        TipTicker.spawn("Kana Swap",400)
        self.image = image
        self.x, self.y = x, y
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.velocity = 3000
        self.drawn = False
        self.sound = True

    def update(self,player):
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.x -= self.velocity * Variables.delta_time
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
    def __init__(self, x, y, spritearray, scale, repeat, explosiontype=0, xvel=0):
        super().__init__()
        self.x, self.y = x, y
        self.xvel = xvel
        self.animspeed = random.randint(40,100)
        self.explosion_type = explosiontype
        self.index = 0
        self.counter = 0
        self.explosion_speed = 1
        self.spritearray = spritearray
        self.image = self.spritearray[self.explosion_type].images[self.index]
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.scale = scale
        self.repeat = repeat

    def update(self):
        self.counter += self.animspeed * Variables.delta_time
        self.x -= self.xvel * Variables.delta_time
        if self.counter >= self.explosion_speed and self.index < len(self.spritearray[self.explosion_type].images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.spritearray[self.explosion_type].images[self.index]
            self.image = pygame.transform.scale(self.image,(256 * self.scale,256 * self.scale))
            self.rect = self.image.get_rect(center = (self.x, self.y))
            
        if self.index >= len(self.spritearray[self.explosion_type].images) - 1 and self.counter >= self.explosion_speed:
            if self.repeat: self.index = 0
            else: self.kill()

class TipTicker(pygame.sprite.Sprite):
    def __init__(self,message,velocity):
        super().__init__()
        self.message = message
        tip_font = pygame.font.SysFont(Constants.font_name, 30)
        self.image = tip_font.render(self.message, True, 'yellow')
        self.messagebox = self.image.get_rect()
        self.x, self.y = Constants.WIDTH + self.messagebox.centerx, 100
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.velocity = velocity

    def update(self):
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.x -= self.velocity * Variables.delta_time
        if self.x < -1000: self.kill()

    def spawn(message,velocity=200):
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
        self.x -= self.velocity * Variables.delta_time
        self.rotate += self.rotate_rate
        if self.x < -100: Graphicgroups.spacejunk.pop(Graphicgroups.spacejunk.index(self))

    def draw(self,screen):
        screen.blit(self.rotated_image, self.rect)
        if Variables.hitboxshow == True: pygame.draw.rect(screen,'red',self.hitbox,2)

    def spawn():
        whichjunk = random.randint(0,len(Constants.spacejunkfiles)-1)
        junksize = random.randrange(2,10)
        Graphicgroups.spacejunk.append(SpaceJunk(whichjunk,random.randrange(-100,100),junksize*0.1))
        try:
            junkobject = pygame.mixer.Sound(os.getcwd() + Constants.spacejunkfiles[whichjunk][1])
            junkobject.set_volume(junksize*0.1)
            pygame.mixer.Sound.play(junkobject)
        except: pass

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
        self.x -= self.velocity * Variables.delta_time
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
        self.type = 0
        self.spritearray = Constants.biglaser_surfs #Sprite Animation
        self.animindex = 0  #Sprite Animation
        self.animspeed = random.randint(10,20) #Sprite Animation
        self.image = self.spritearray[self.type].images[self.animindex] #Sprite Animation
        self.x, self.y = x, y
        # self.image = Constants.biglaser_surf
        self.biglaser_rect = self.image.get_rect(center = (self.x, self.y))
        self.velocity = 8000
        self.hitboxYshrink = 50
        self.hitbox = [0,0,0,0]

    def animate(self):
        import Functions
        Functions.moanimate(self)

    def update(self):
        self.x -= self.velocity * Variables.delta_time
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

class AnimCenterWarning:
    def __init__(self,message,surface,typeof,scale,fade=True,pos=(Constants.WCENTER, Constants.HCENTER)):
        self.spritearray = surface #Sprite Animation
        self.type = typeof
        self.animindex = 0  #Sprite Animation
        self.animspeed = 10
        self.image = self.spritearray[self.type].images[self.animindex] #Sprite Animation
        self.pos = pos
        self.fade = fade
        self.alpha = 255
        self.message = message
        self.scale = scale

    def animate(self):
        import Functions
        Functions.moanimate(self)
        
    def update(self):
        self.animate()
        if self.fade:
            self.alpha -= 100 * Variables.delta_time
            if self.alpha <= 0: Graphicgroups.animcenterwarning.pop(Graphicgroups.animcenterwarning.index(self))

    def draw(self):
        warning_text = Constants.WARNING_font.render(self.message, True, 'white')
        warning_text.set_alpha(self.alpha)
        self.image_scaled = pygame.transform.scale(self.image,(self.image.get_rect().width*self.scale,self.image.get_rect().height*self.scale))
        self.image_scaled.set_alpha(self.alpha)
        centered_warning = warning_text.get_rect(center = self.pos)
        centered_image = self.image_scaled.get_rect(center = self.pos)
        Constants.screen.blit(self.image_scaled,centered_image)
        Constants.screen.blit(warning_text, centered_warning)

    def spawn(message,surface,scale=1):
        Graphicgroups.animcenterwarning.append(CenterWarning(message,surface,scale))

class CenterWarning:
    def __init__(self,message,surface,scale,fade=True,pos=(Constants.WCENTER, Constants.HCENTER)):
        self.pos = pos
        self.fade = fade
        self.alpha = 255
        self.message = message
        self.surf = surface
        self.scale = scale

    def update(self):
        if self.fade:
            self.alpha -= 100 * Variables.delta_time
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
    def __init__(self,x,y,kana,group,fade,rotate,newmessage="",color='white',new=False):
        self.kananum, self.last_kananum = 0, 0
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
        self.grapicgroup = group
        self.kana_blip = 0
        self.correct_kana_lost_sound_play = True

    def update(self,player):
        self.kanatext = Constants.kana_font.render(Variables.gamekana[self.level][self.kana][Variables.gamemode], True, self.color)
        self.kana_graphic = Constants.ui_font.render(Variables.gamekana[self.level][self.kana][0] + Variables.gamekana[self.level][self.kana][1] + Variables.gamekana[self.level][self.kana][2],True,'yellow')
        self.x -= self.xvelocity * Variables.delta_time
        if self.y > Settings.ship_screen_boundary and self.y < Constants.HEIGHT - Settings.ship_screen_boundary:
            self.y += self.yvelocity * Variables.delta_time
        if self.x < -64: self.grapicgroup.pop(self.grapicgroup.index(self))

        if self.grapicgroup == Graphicgroups.correctkanas:
            # Grow Kana at 2/5th of the screen with
            if self.x < 2 * (Constants.WIDTH // 5) and self.x > 10:
                self.kanascale += Variables.delta_time/5
                if self.kana_blip >= self.x/500:
                    pygame.mixer.Sound.play(Constants.correct_kana_dying_sound)
                    self.kana_blip = 0
                self.kana_blip += 1 * Variables.delta_time
            elif self.x < 0:
                if self.correct_kana_lost_sound_play:
                    pygame.mixer.Sound.play(Constants.correct_kana_lost_sound)
                    explosion = Explosion(x=self.x, y=self.y,spritearray=Constants.explosion_surfs,scale=1,repeat=False,explosiontype=1)
                    Graphicgroups.explosion_group.add(explosion)
                    Variables.score -= 10
                    self.correct_kana_lost_sound_play = False

    def draw(self,screen):
        self.orig_rect = self.kanatext.get_rect()
        self.rotated_image = pygame.transform.rotate(self.kanatext,self.rotate)
        self.rot_rect = self.orig_rect.copy()
        self.rot_rect.center = self.rotated_image.get_rect().center
        self.rotated_image = self.rotated_image.subsurface(self.rot_rect).copy()
        self.scale_image = pygame.transform.scale(self.rotated_image,(self.kanatext.get_rect().width*self.kanascale,self.kanatext.get_rect().height*self.kanascale))
        self.centered_image = self.scale_image.get_rect(center = (self.x,self.y))
        screen.blit(self.scale_image, self.centered_image)
        self.rotate += self.rotate_rate * Variables.delta_time

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

class AnimatedPowerUp:
    def __init__(self,x,y,xvelocity,yvelocity,typeof,pueffect):
        self.type = typeof #Sprite Animation
        self.spritearray = Constants.powerup_surfs #Sprite Animation
        self.animindex = 0  #Sprite Animation
        self.animspeed = 10 #Sprite Animation
        self.image = self.spritearray[self.type].images[self.animindex] #Sprite Animation
        self.x, self.y = x, y
        self.powerup_rect = self.image.get_rect(center = (self.x, self.y))
        self.xvelocity, self.yvelocity = xvelocity, yvelocity
        self.hitbox = [0,0,0,0]
        self.shieldradius = 32
        self.pueffect = pueffect

    def animate(self):
        import Functions
        Functions.moanimate(self)

    def effect(self,pueffect,player):
        if pueffect == "laser":
            if self.collide(player.spaceship_rect):
                Graphicgroups.animatedpowerup.pop(Graphicgroups.animatedpowerup.index(self))
                player.lasersight = True
                player.lasersightcounter = player.poweruptimelength
                pygame.mixer.Sound.play(Constants.powerup_sound)
                pygame.mixer.Sound.play(Constants.shiplaser_sound)
        if pueffect == "speed":
            if self.collide(player.spaceship_rect):
                Graphicgroups.animatedpowerup.pop(Graphicgroups.animatedpowerup.index(self))
                player.speedboost = True
                player.speedboostcounter = player.poweruptimelength
                pygame.mixer.Sound.play(Constants.powerup_sound)
        if pueffect == "switch":
            if self.collide(player.spaceship_rect):
                Graphicgroups.animatedpowerup.pop(Graphicgroups.animatedpowerup.index(self))
                player.kanaswitch = True
                player.kanaswitchcounter = player.poweruptimelength
                pygame.mixer.Sound.play(Constants.powerup_sound)
        if pueffect == "1up":
            if self.collide(player.spaceship_rect):
                Graphicgroups.animatedpowerup.pop(Graphicgroups.animatedpowerup.index(self))
                player.lives += 1
                pygame.mixer.Sound.play(Constants.powerup_sound)
        if pueffect == "powerup":
            if self.collide(player.spaceship_rect):
                Graphicgroups.animatedpowerup.pop(Graphicgroups.animatedpowerup.index(self))
                if player.pewtype < len(Constants.pew_array)-1:
                    player.pewtype += 1
                    pygame.mixer.Sound.play(Constants.powerup_sound)
                else: player.pewtype = 0

    def update(self):
        self.effect(self.pueffect,player)
        self.x -= (self.xvelocity) * Variables.delta_time
        self.y += self.yvelocity * Variables.delta_time * math.sin(self.x/100)
        self.powerup_rect = self.image.get_rect(center = (self.x, self.y))
        if self.x < -128: Graphicgroups.animatedpowerup.pop(Graphicgroups.animatedpowerup.index(self))
        self.animate()

    def draw(self,screen):
        self.hitbox = self.image.get_rect(center = (self.x, self.y))
        screen.blit(self.image, self.powerup_rect)

        # Draw hitbox
        if Variables.hitboxshow:
            pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)

    def collide(self,rect):
        x = abs(self.x - (rect[0] + rect[2] / 2))
        y = abs(self.y - (rect[1] + rect[3] / 2))

        if x > (rect[2] / 2 + self.shieldradius): return False
        if y > (rect[3] / 2 + self.shieldradius): return False

        if x <= (rect[2] / 2): return True
        if y <= (rect[3] / 2): return True

        corner_distance = (x - rect[2] / 2)**2 + (y - rect[3] / 2)**2
        return corner_distance <= self.shieldradius**2

    def spawn(xvel,typeof,pueffect):
        x = Constants.WIDTH+64
        y = random.randrange(128,Constants.HEIGHT-128)
        xvelocity = xvel
        yvelocity = random.randrange(100,200)
        Graphicgroups.animatedpowerup.append(AnimatedPowerUp(x, y,xvelocity,yvelocity,typeof,pueffect))

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
        import Functions
        Functions.moanimate(self)

    def shoot(self,player):
        angle = self.findobjectangle(player)
        if pygame.time.get_ticks() - self.last_enemy_pew >= random.randint(2000,10000):
            if self.type%3 == 0: # AIMED SHOT
                if angle < math.pi/3 and angle > -math.pi/3:
                    pygame.mixer.Sound.play(Constants.enemypew_sound)
                    Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,angle,Graphicgroups.enemies.index(self)))
            elif self.type%3 == 1: # FORWARD SHOT
                pygame.mixer.Sound.play(Constants.enemypew_sound)
                Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,math.radians(random.randint(-10,10)),Graphicgroups.enemies.index(self)))
            elif self.type%3 == 2: #AoE SHOT
                pygame.mixer.Sound.play(Constants.enemypew_sound)
                for angle in self.calculate_angles(8):
                    Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,math.radians(random.randint(angle-10,angle+10)),Graphicgroups.enemies.index(self)))
            self.last_enemy_pew = pygame.time.get_ticks()

    def update(self):
        self.healthdisplay = self.enemy_rect.width/self.maxhealth*self.health
        self.healthbar_Color = (255-(255/self.maxhealth*self.health),255/self.maxhealth*self.health,0)
        self.curhealth_grapic = Constants.ui_font.render(str(self.health), True, 'yellow')
        self.animate()
        if self.type%3 == 0 or self.type%3 == 1:
            self.enemy_rect = self.image.get_rect(midleft = (self.x, self.y))
        elif self.type%3 == 2:
            self.enemy_rect = self.image.get_rect(center = (self.x, self.y))
        self.x -= (self.velocity - self.knockbackx) * Variables.delta_time
        self.y -= (self.Yvelocity - self.knockbacky) * Variables.delta_time
        if self.knockbackx > 0: self.knockbackx -= Settings.enemy_knockback_recoveryx * Variables.delta_time
        if self.knockbacky > 0: self.knockbacky -= Settings.enemy_knockback_recoveryy * Variables.delta_time
        if self.knockbacky < 0: self.knockbacky += Settings.enemy_knockback_recoveryy * Variables.delta_time
        if self.x < -128 or self.y > Constants.HEIGHT + 128 or self.y < -128: Graphicgroups.enemies.pop(Graphicgroups.enemies.index(self))
        self.shoot(player)
    
    def findobjectangle(self,player):
            # Find angle of player
            dx = self.x - player.spaceship_rect.center[0]
            dy = self.y - player.spaceship_rect.center[1]
            self.theta = math.atan2(-dy,dx)
            return self.theta

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
            # pygame.draw.line(screen, (255,255,0), (self.x, self.y),player.spaceship_rect.center)

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
        self.music = Constants.bosses_array[Variables.level]["music"]
        Variables.musicvolume = Settings.maxmusicvolume
        pygame.mixer.music.load(os.path.join('music',str(self.music) + '.wav'))
        pygame.mixer.music.play(-1)
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
        self.maxhealth = health+1
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
        self.animindex += self.animspeed * Variables.delta_time #length of ime before we advance the animation frame
        if self.animindex > len(self.spritearray[self.bossimage].images)-1: self.animindex = 0 # reset the frame to 0 if we try to go beyond the array
        self.image = self.spritearray[self.bossimage].images[int(self.animindex)] # update the current frame

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
                        Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,angle,Graphicgroups.bosses.index(self)))
                        self.lastrapidfire = int(self.rapidfire)
                    self.rapidfire += 10 * Variables.delta_time
            elif self.type%3 == 1: # FORWARD SHOT
                if int(self.rapidfire) - self.lastrapidfire == self.bulletfrequency:
                    pygame.mixer.Sound.play(Constants.enemypew_sound)
                    Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,math.radians(random.randint(-10,10)),Graphicgroups.bosses.index(self)))
                    self.lastrapidfire = int(self.rapidfire)
                self.rapidfire += 10 * Variables.delta_time
            elif self.type%3 == 2: #AoE SHOT
                if int(self.rapidfire) - self.lastrapidfire == 5*self.bulletfrequency:
                    pygame.mixer.Sound.play(Constants.enemypew_sound)
                    for angle in self.calculate_angles(self.anglenum):
                        Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,math.radians(angle),Graphicgroups.bosses.index(self)))
                    self.lastrapidfire = int(self.rapidfire)
                self.rapidfire += 10 * Variables.delta_time                
            self.last_enemy_pew = pygame.time.get_ticks()

    def update(self):
        self.healthdisplay = self.boss_rect.width/self.maxhealth*self.health
        self.healthbar_Color = (255-(255/self.maxhealth*self.health),255/self.maxhealth*self.health,0)
        self.curhealth_grapic = Constants.ui_font.render(str(self.health), True, 'yellow')
        self.animate()
        if self.type%3 == 0 or self.type%3 == 1: self.boss_rect = self.image.get_rect(midleft = (self.x, self.y))
        elif self.type%3 == 2: self.boss_rect = self.image.get_rect(center = (self.x, self.y))
        self.x -= self.velocity * Variables.delta_time
        self.y += self.Yvelocity * Variables.delta_time
        if self.y <= 50 or self.y >= Constants.HEIGHT-50: self.Yvelocity *= -1
        if self.x <= 3*Constants.WIDTH/5:
            self.enter_screen = True
            self.velocity *= -1
        if self.x > Constants.WIDTH and self.enter_screen == True:
            self.velocity *= -1
        self.shoot(player)

    def findobjectangle(self,player):
            # Find angle of player
            dx = self.x - player.spaceship_rect.center[0]
            dy = self.y - player.spaceship_rect.center[1]
            self.theta = math.atan2(-dy,dx)
            return self.theta

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
    def __init__(self,x,y,direction,origin):
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
        self.origin = origin

    def objectdirection(self,direction):
        pewdir = direction - math.pi/2 + self.directionskew
        sin_a = math.sin(pewdir)
        cos_a = math.cos(pewdir)
        self.x += self.velocity * sin_a * Variables.delta_time
        self.y += self.velocity * cos_a * Variables.delta_time
        return self.x, self.y

    def animate(self):
        import Functions
        Functions.soanimate(self)

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
        self.x -= self.velocity * Variables.delta_time
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
        for w in range(random.randint(1,2)):
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
        self.x += self.velocity * sin_a * Variables.delta_time
        self.y += self.velocity * cos_a * Variables.delta_time
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
        self.rotate += self.rotate_rate * Variables.delta_time

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

# THINGS
class Damagenum:
    def __init__(self,x,xvel,y,damage):
        self.x, self.y, self.orgy = x, y-32, y-32
        self.xvelocity, self.yvelocity = xvel, 50
        damage_font = pygame.font.SysFont(Constants.font_name, Settings.damage_num_font_size)
        self.image = damage_font.render(str(damage), True, 'yellow')
        self.alpha = 255

    def update(self):
        self.y -= self.yvelocity * Variables.delta_time
        self.x -= (self.xvelocity - 50) * Variables.delta_time
        self.alpha -= 0.5
        if self.y < self.orgy - 200: Graphicgroups.damagenumbers.pop(Graphicgroups.damagenumbers.index(self))

    def draw(self, screen):
        self.update()
        self.image.set_alpha(int(self.alpha))
        screen.blit(self.image, (self.x, self.y))

    def spawn(x,xvel,y,damage):
        Graphicgroups.damagenumbers.append(Damagenum(x,xvel,y,damage))

class Timers:
    def __init__(self):
        self.star_timer, self.star_frequency = 0, 0
        self.kana_timer, self.kana_frequency = 0, 0
        self.biglaser_timer, self.biglaser_randomness = 0, 0
        self.enemy_timer, self.enemy_randomness = 0, 0
        self.incorrectkana_timer, self.incorrectkana_thresh = 0, random.randint(Settings.minimum_incorrect_kana_frequency,Settings.maximum_incorrect_kana_frequency)/10
        self.correctkana_timer, self.correctkana_thresh = 0, random.randint(Settings.minimum_correct_kana_frequency,Settings.maximum_correct_kana_frequency)/10
        self.boss_message_timer, self.boss_message_thresh, self.boss_message_displayed = 0, 0, False
        self.boss_timer, self.boss_delay = 0, 3
        self.planet_timer, self.planet_thresh = 0, random.randint(60,90)
        self.junk_timer, self.junk_thresh = 0, random.randint(60,90)
        self.powerup_timer, self.powerup_thresh = 0, random.randint(30,40)
        self.bridge_timer, self.bridge_thresh = 0, 30
        self.WoD_timer, self.WoD_thresh = 0, random.randint(30,60)

    def stars(self, frequency, velocity):
        # Stars Timer
        if self.star_timer > self.star_frequency:
            Star.spawn(velocity)
            self.star_timer = 0
            self.star_frequency = frequency
        self.star_timer += 1 * Variables.delta_time
    
    def allkana(self):
        # All Kana Timer
        if self.kana_timer > self.kana_frequency:
            selection = random.randint(0,Variables.levels[Variables.level]-1)
            Graphicgroups.kanas.append(Kana(
                x = Constants.WIDTH+Constants.off_screen_offset, 
                y = random.randrange(300,Constants.HEIGHT-128,),
                kana = selection,
                group = Graphicgroups.kanas,
                fade = random.randint(Constants.min_kana_alpha,256),
                rotate = random.randint(-Settings.kana_rotate_rate,Settings.kana_rotate_rate))
            )
            self.kana_timer = 0
            self.kana_frequency = random.randint(Settings.minimum_incorrect_kana_frequency,Settings.maximum_incorrect_kana_frequency)/10
        self.kana_timer += 1 * Variables.delta_time
    
    def biglaser(self, enemywaittimer,min=5,max=30):
        if Variables.level >= 3 and enemywaittimer <= 0:
            if self.biglaser_timer > self.biglaser_randomness:
                BigLaserWarning.spawn(player)
                self.biglaser_timer = 0
                self.biglaser_randomness = random.randint(min,max)
            self.biglaser_timer += 1 * Variables.delta_time

    def enemy(self, enemywaittimer,min=5,max=20):
        if Variables.level >= Settings.enemy_start_level and enemywaittimer <= 0:
            if self.enemy_timer > self.enemy_randomness:
                Enemies.spawn()
                self.enemy_timer = 0
                self.enemy_randomness = random.randint(min,max)
            self.enemy_timer += 1 * Variables.delta_time

    def bossmessage(self,delay):
        if self.boss_message_timer >= delay and self.boss_message_displayed == False:
            CenterWarning.spawn(
                message = 'BossFight',
                surface = Constants.boss_spritesheet_surfs[Constants.bosses_array[Variables.level]["imgindx"]].images[0],
                scale = 3
            )
            self.boss_message_displayed = True
        self.boss_message_timer += 1 * Variables.delta_time

    def boss(self, delay):
        if self.boss_timer >= delay:
            if Variables.bossexist == False:
                Bosses.spawn()
                Variables.bossexist = True
        self.boss_timer += 1 * Variables.delta_time

    def incorrectkana(self, kanakill):
        if self.incorrectkana_timer > self.incorrectkana_thresh:
            Variables.generatedincorrectkanacounter += 3
            selection = random.randint(0,Variables.levels[Variables.level]-1)
            if selection != Variables.kananum:
                if int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3]) < Settings.num_to_shoot_new_kana+1:
                    Graphicgroups.kanas.append(Kana(Constants.WIDTH+Constants.off_screen_offset, random.randrange(128,Constants.HEIGHT-200,),selection,Graphicgroups.kanas,random.randint(Constants.min_kana_alpha,256),random.randint(-Settings.kana_rotate_rate,Settings.kana_rotate_rate),"Shoot",(255,kanakill,kanakill),True))
                else:
                    Graphicgroups.kanas.append(Kana(Constants.WIDTH+Constants.off_screen_offset, random.randrange(128,Constants.HEIGHT-200,),selection,Graphicgroups.kanas,random.randint(Constants.min_kana_alpha,256),random.randint(-Settings.kana_rotate_rate,Settings.kana_rotate_rate)))
                self.incorrectkana_timer = 0
                self.incorrectkana_thresh = random.randint(Settings.minimum_incorrect_kana_frequency,Settings.maximum_incorrect_kana_frequency)/10
        self.incorrectkana_timer += 1 * Variables.delta_time

    def correctkana(self, kanakill):
        if kanakill >= 255: kanakill = 255
        if self.correctkana_timer > self.correctkana_thresh:
            Variables.generatedcorrectkanacounter += 3
            if int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3]) < Settings.num_to_shoot_new_kana+1:
                Graphicgroups.correctkanas.append(Kana(
                    x=Constants.WIDTH+Constants.off_screen_offset, 
                    y=random.randrange(128,Constants.HEIGHT-200,),
                    kana=Variables.kananum,
                    group=Graphicgroups.correctkanas,
                    fade=random.randint(Constants.min_kana_alpha,256),
                    rotate=random.randint(-Settings.kana_rotate_rate,Settings.kana_rotate_rate),
                    newmessage="Collect",
                    color=(kanakill,255,kanakill),
                    new=True))
            else:
                Graphicgroups.correctkanas.append(Kana(
                    x=Constants.WIDTH+Constants.off_screen_offset, 
                    y=random.randrange(128,Constants.HEIGHT-200,),
                    kana=Variables.kananum,
                    group=Graphicgroups.correctkanas,
                    fade=random.randint(Constants.min_kana_alpha,256),
                    rotate=random.randint(-Settings.kana_rotate_rate,Settings.kana_rotate_rate)))
            self.correctkana_timer = 0
            self.correctkana_thresh = random.randint(Settings.minimum_correct_kana_frequency,Settings.maximum_correct_kana_frequency)/10
            self.correct_kana_lost_sound_play = True
        self.correctkana_timer += 1 * Variables.delta_time

    def planet(self):
        if self.planet_timer > self.planet_thresh:
            Planet.spawn()
            self.planet_timer = 0
            self.planet_thresh = random.randint(60,90)
        self.planet_timer += 1 * Variables.delta_time

    def junk(self):
        if self.junk_timer > self.junk_thresh:
            SpaceJunk.spawn()
            self.junk_timer = 0
            self.junk_thresh = random.randint(60,90)
        self.junk_timer += 1 * Variables.delta_time

    def powerup(self):
        if self.powerup_timer >= self.powerup_thresh:
            powerup_type = random.randint(1,2)
            AnimatedPowerUp.spawn(
                Constants.powerup_array[powerup_type]["xvel"],
                Constants.powerup_array[powerup_type]["surfindx"],
                Constants.powerup_array[powerup_type]["pueffect"],
                )
            self.powerup_timer = 0
            self.powerup_thresh = random.randint(30,40)
        self.powerup_timer += 1 * Variables.delta_time

    def bridge(self, frequency):
        if self.bridge_timer > frequency:
            Bridge.spawn()
            self.bridge_timer = 0
            self.bridge_thresh = frequency
        self.bridge_timer += 1 * Variables.delta_time

    def wallofdeath(self):
        if self.WoD_timer >= self.WoD_thresh:
            WallOfDeath.spawn(Constants.WIDTH,0)
            self.WoD_timer = 0
            self.WoD_thresh = random.randint(30,60)
        self.WoD_timer += 1 * Variables.delta_time

class Buttons:
    def __init__(self):
        self.startbuttonsoundplayed = False

    def start(self,screen):
        button_width = 150
        self.start_button_location = (Constants.WCENTER-(button_width/2), Constants.HEIGHT //2+150, button_width, 70)
        self.start_button = pygame.Rect(self.start_button_location)
        if self.start_button.collidepoint(pygame.mouse.get_pos()):
            self.start_text = Constants.question_font.render('START', True, 'Green')
            if self.startbuttonsoundplayed == False:
                pygame.mixer.Sound.play(Constants.correct_kana_dying_sound)
                self.startbuttonsoundplayed = True
        else:
            self.start_text = Constants.question_font.render('START', True, 'Red')
            self.startbuttonsoundplayed = False
        pygame.draw.rect(screen, 'white', self.start_button, 2)
        screen.blit(self.start_text, (self.start_button_location[0]+10, self.start_button_location[1]+10))

    def shiptype(self,screen):
        self.shiptype_number_location = (10, 90, 200, 40)
        self.shiptype_number = pygame.Rect(self.shiptype_number_location)
        shiptype_text = Constants.ui_font.render('Ship: ', True, 'white')
        pygame.draw.rect(screen, 'white', self.shiptype_number, 2)
        screen.blit(shiptype_text, (self.shiptype_number_location[0]+10,self.shiptype_number_location[1]+10))
        num_text = Constants.ui_font.render(str(player.type), True, 'white')
        screen.blit(num_text,(120, 100))

    def gamemode(self,screen):
        self.game_mode_location = (10, 50, 200, 40)
        self.game_mode = pygame.Rect(self.game_mode_location)
        pygame.draw.rect(screen, 'white', self.game_mode, 2)
        if Variables.gamemode == 0:
            sound_state = Constants.ui_font.render('Hiragana', True, 'white')
            screen.blit(sound_state, (75, 60))
        else:
            sound_state = Constants.ui_font.render('Katakana', True, 'white')
            screen.blit(sound_state, (75, 60))

    def startinglevel(self,screen):
        self.level_number_location = (10, 10, 200, 40)
        self.level_number = pygame.Rect(self.level_number_location)
        level_text = Constants.ui_font.render('Level: ', True, 'white')
        pygame.draw.rect(screen, 'white', self.level_number, 2)
        screen.blit(level_text, (self.level_number_location[0]+10,self.level_number_location[1]+10))
        num_text = Constants.ui_font.render(str(Variables.level), True, 'white')
        screen.blit(num_text,(120, 20))

class Achievements:
    def __init__(self) -> None:
        self.tingtangshow = True
        self.tingtangarray = []

    def tingtang(self):
        if len(self.tingtangarray) > 5: self.tingtangarray.pop(0)               # If array gets larger than 5, pop off the first element
        match self.tingtangarray:
            case ['u', 'i', 'u', 'a', 'a']:
                if self.tingtangshow == True:                                   # Check to see if the message is allowed to be displayed
                    TipTicker.spawn("Ting, Tang, Walla Walla Bing Bang!", 500)  # Spawn Ticker Message
                    self.tingtangshow = False                                   # stop message from being generated each frame after
            case ['a', 'a', 'a', 'a', 'a']:
                if self.tingtangshow == True:                                   # Check to see if the message is allowed to be displayed
                    TipTicker.spawn("AAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHHH!", 500)  # Spawn Ticker Message
                    self.tingtangshow = False                                   # stop message from being generated each frame after
            case ['o', 'o', 'o', 'o', 'o']:
                if self.tingtangshow == True:                                   # Check to see if the message is allowed to be displayed
                    TipTicker.spawn("ooooooooooOOOOOOOOOOOOOoooooooooo!", 500)  # Spawn Ticker Message
                    self.tingtangshow = False                                   # stop message from being generated each frame after
            case ['e', 'e', 'e', 'e', 'e']:
                if self.tingtangshow == True:                                   # Check to see if the message is allowed to be displayed
                    TipTicker.spawn("ええええええええええええええええええ?", 500)  # Spawn Ticker Message
                    self.tingtangshow = False                                   # stop message from being generated each frame after

#region Instancing
player = Ship(0,Constants.HCENTER)              # Instance player to center left of screen
timer = Timers()                                # Create a timer object
menu_buttons = Buttons()                        # Create a button object
achievements = Achievements()                   # Achievements system
#endregion Instancing