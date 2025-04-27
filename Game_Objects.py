import Variables, CONST, Settings, Graphicgroups
import pygame, math, random, os

#region PLAYER THINGS




#region ship
class Ship:
    def __init__(self,x,y):
        self.type = 0
        self.lives = 5
        self.shipcollision = False
        self.spritearray = CONST.SURF_SPACESHIP
        self.flamearray = CONST.SURF_SPACESHIP_FLAMES
        self.animindex = 0
        self.animspeed = 10
        self.image = self.spritearray[self.type].images[self.animindex]
        self.location = pygame.math.Vector2(x,y)
        self.x, self.y = self.location[0], self.location[1]
        self.spaceship_rect = self.image.get_rect(center = self.location)
        self.deadzone = 20
        self.Xvelocity, self.Yvelocity = 0, 0
        self.speed = Settings.ship_normal_top_speed
        self.acceleration, self.deceleration = self.speed*3, self.speed*4
        self.shiprest = 100
        self.pewtype = 0
        self.speedup, self.slowdown = 2, 1
        self.last_pewtimer = 0
        self.last_missiletimer = 0
        self.maxnumpew = 2
        self.shipborder = Settings.ship_screen_boundary
        self.respawn_timer = -1
        self.hitbox = [0,0,0,0]
        self.shield = False
        self.shieldradius = 64
        self.laserpower = int(Variables.score) * CONST.ARRAY_PLAYER_PEW[self.pewtype]["laserpower"] + 1
        self.power_grapic = CONST.UI_FONT.render(str(self.laserpower), True, 'green')
        self.laserbuild = 1
        self.buildupsoundplayed = False
        self.bigpewreadyplayed = False
        self.hasfired = True
        self.defaultpersist = CONST.ARRAY_PLAYER_PEW[self.pewtype]["persist"]
        self.targetindex = 0

        # Flames
        self.xflamedir, self.yflamedir = 0, 0
        self.xflameindex, self.yflameindex = 0, 0
        self.flamespeed = 30
        self.xflameimage = pygame.transform.rotate(self.flamearray.images[self.xflameindex],0)
        self.xflame_rect = self.xflameimage.get_rect(center = self.location)
        self.yflameimage = pygame.transform.rotate(self.flamearray.images[self.yflameindex],90)
        self.yflame_rect = self.yflameimage.get_rect(center = self.location)

        # Healthbar stuff
        self.maxhealth = 9
        self.health = self.maxhealth
        self.healthbar_height = 2
        self.healthbar = pygame.Surface((self.spaceship_rect.width,self.healthbar_height)).convert_alpha()
        self.healthbar_Color = (255-(255/self.maxhealth*self.health),255/self.maxhealth*self.health,0)

        #region Powerups
        self.poweruptimelength = 1000
        self.speedboost = False
        self.speedboostcounter = self.poweruptimelength

        self.lasersight = False
        self.lasersightcounter = self.poweruptimelength
        self.laserlength = 0
        self.laser = pygame.Surface((self.laserlength,2)).convert_alpha()

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
        Functions.moanimate(self,loopstart=0,loopend=999)

    def movement(self):
        keys = pygame.key.get_pressed()
        self.temp_acc = self.acceleration * Variables.delta_time
        self.temp_dec = self.deceleration * Variables.delta_time

        #region Vecors
        # Horizontal
        if keys[pygame.K_a]: 
            self.flame(0,None)
            CONST.SCREEN.blit(self.xflameimage, self.xflame_rect)
            if self.Xvelocity <= self.speed:
                self.Xvelocity += self.temp_acc
        elif keys[pygame.K_d] and self.location[0] < CONST.WIDTH-200:
            self.flame(180,None)
            CONST.SCREEN.blit(self.xflameimage, self.xflame_rect)
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
            CONST.SCREEN.blit(self.yflameimage, self.yflame_rect)
            if self.Yvelocity <= self.speed:
                self.Yvelocity += self.temp_acc
        elif keys[pygame.K_s]:
            self.flame(None,90)
            CONST.SCREEN.blit(self.yflameimage, self.yflame_rect)
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

        #region Pew
        import Functions
        Functions.longpew(
            keys=keys,
            buildupsound=CONST.SOUND_BIG_PEW_BREWING,
            bigpewready=CONST.SOUND_BIG_PEW_READY,
            brewsprite=CONST.SURF_BREWING,
            pewsprite=CONST.SURF_DYNAMIC_PEW
        )
        if Variables.current_game_state == 'Boss': rnd = random.randint(4,6)
        if Variables.current_game_state == 'Game': rnd = random.randint(1,4)
        if Variables.missiles_enabled == True:
            match rnd:
                case 1:
                    Functions.missilepew(
                        keys=keys,
                        target=Graphicgroups.incorrectkanas
                    )
                case 2:
                    Functions.missilepew(
                        keys=keys,
                        target=Graphicgroups.turrets
                    )
                case 3:
                    Functions.missilepew(
                        keys=keys,
                        target=Graphicgroups.enemies
                    )
                case 4:
                    Functions.missilepew(
                        keys=keys,
                        target=Graphicgroups.debris
                    )
                case 5:
                    Functions.missilepew(
                        keys=keys,
                        target=Graphicgroups.bossmodeincorrectkana
                    )
                case 6:
                    Functions.missilepew(
                        keys=keys,
                        target=Graphicgroups.bosses
                    )
        #endregion Pew

    def move(self):
        if Variables.current_game_state == "Boss":
            self.location[0] -= self.Xvelocity * Variables.delta_time
        else:
            self.location[0] -= (self.Xvelocity + Settings.ship_fallbackspeed) * Variables.delta_time       # Movement in the X direction
        self.location[1] -= self.Yvelocity * Variables.delta_time                                       # Movement in the Y direction
        if self.location[1] < self.shipborder:                                                          # Do not move too far Up out of the screen
            self.location[1] = self.shipborder                                                          # Reset position to Up screen border
            self.Yvelocity = 0                                                                          # Reset Velocity to 0
        elif self.location[1] > CONST.PAHEIGHT-self.shipborder:                                       # Do not move too far Down out of the screen
            self.location[1] = CONST.PAHEIGHT-self.shipborder                                         # Reset position to Down screen border
            self.Yvelocity = 0                                                                          # Reset Velocity to 0
        elif self.location[0] <= 48:                                                                    # Do not move too far Left out of the screen
            self.location[0] = 48                                                                       # Reset position to Left screen border
        self.spaceship_rect.center = self.location                                                      # Set the position of the center of the ship sprite

    def respawn_checker(self):
        # RESPAWN
        if self.respawn_timer == 3:
            pygame.mixer.Sound.stop(CONST.SOUND_SHIP_LASER)
            self.shipcollision = False
            self.lasersight = False
            self.speedboost = False
            self.location = pygame.math.Vector2(100, CONST.HCENTER)
            self.respawn_timer -= 1 * Variables.delta_time
        elif self.respawn_timer > 0:
            self.respawn_timer -= 1 * Variables.delta_time
        elif self.respawn_timer <= 0 and self.respawn_timer > -1:
            if Variables.current_game_state != "intro": self.shipcollision = True
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
            self.laser = pygame.Surface((self.laserlength,3)).convert_alpha()
            self.laser.set_alpha(128)
            self.laser.fill((255,0,0))
            self.lasersightcounter -= 100 * Variables.delta_time
            self.laserlength += 3000 * Variables.delta_time
        elif self.lasersight and self.lasersightcounter <= 256 and self.lasersightcounter > 0:  # Lasersight maintain
            self.laser = pygame.Surface((CONST.WIDTH,2)).convert_alpha()
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

        self.healthdisplay = self.spaceship_rect.width/self.maxhealth*self.health
        self.healthbar_Color = (255-(255/self.maxhealth*self.health),255/self.maxhealth*self.health,0)
        self.curhealth_grapic = CONST.UI_FONT.render(str(self.health), True, 'yellow')

        self.animate()
        self.move()
        self.respawn_checker()
        self.apply_powerups()
        self.x, self.y = self.location[0], self.location[1]
        if self.health <= 0: self.respawn()

        # self.laserpower = int(Variables.score) + 1
        self.laserpower = int(Variables.score) * CONST.ARRAY_PLAYER_PEW[player.pewtype]["laserpower"] + 1
        self.power_grapic = CONST.UI_FONT.render(str(self.laserpower), True, 'green')

    def draw(self,screen):

        screen.blit(self.healthbar, (self.spaceship_rect.left,self.spaceship_rect.top+74,self.spaceship_rect.width,10))
        self.healthbar.fill((0,0,0,0))
        try: pygame.draw.rect(self.healthbar,self.healthbar_Color,(0,0,self.healthdisplay,self.healthbar_height))
        except: pass

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
        import Functions
        self.hitbox = Functions.shrink_hitbox(self.spaceship_rect,8)
        if Variables.hitboxshow:
            screen.blit(self.power_grapic, self.spaceship_rect.topleft)
            pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)

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
        self.health = 9
        self.respawn_timer = 3
        player.pewtype = 0
        Variables.missiles_enabled = False



#region Pew
class Pew:
    def __init__(self,x,y,image):
        self.x, self.y = x, y
        self.image = pygame.transform.scale(image,(CONST.ARRAY_PLAYER_PEW[player.pewtype]["width"],CONST.ARRAY_PLAYER_PEW[player.pewtype]["height"]))
        self.rect = self.image.get_rect(midleft = (self.x, self.y))
        self.velocity = CONST.ARRAY_PLAYER_PEW[player.pewtype]["pewspeed"]
        self.hitbox = [0,0,0,0]

    def animate(self):
        self.animindex += self.animspeed * Variables.delta_time #length of ime before we advance the animation frame
        if self.animindex > len(self.spritearray.images)-1: self.animindex = 0 # reset the frame to 0 if we try to go beyond the array
        self.image = self.spritearray.images[int(self.animindex)] # update the current frame

    def update(self):
        self.rect = self.image.get_rect(midleft = (self.x, self.y))
        self.hitbox = self.rect
        self.x += self.velocity * Variables.delta_time
        if self.x > CONST.WIDTH+500: Graphicgroups.bullets.pop(Graphicgroups.bullets.index(self))

    def draw(self,screen):
        screen.blit(self.image, self.rect)
        if Variables.hitboxshow: pygame.draw.rect(screen, (0,255,0),self.hitbox, 2)

    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False

    def spawn(player):
        if len(Graphicgroups.bullets) < CONST.ARRAY_PLAYER_PEW[player.pewtype]["maxnumpew"]:
            if pygame.time.get_ticks() - player.last_pewtimer >= CONST.ARRAY_PLAYER_PEW[player.pewtype]["pewrate"]:
                Graphicgroups.bullets.append(Pew(
                    player.spaceship_rect.center[0],
                    player.spaceship_rect.center[1],
                    CONST.SURF_PEW[CONST.ARRAY_PLAYER_PEW[player.pewtype]["imgindx"]]
                ))
                pygame.mixer.Channel(8).play(CONST.PLAYER_PEW_SOUNDS[CONST.ARRAY_PLAYER_PEW[player.pewtype]["pewsound"]])
                player.last_pewtimer = pygame.time.get_ticks()



#region Homing Misile
class HomingMissile:
    def __init__(self,x,y,target,targetgroup,ypos,image):
        self.spritearray = image
        self.x, self.y = x, y
        self.type = 0
        self.animindex = 0
        self.animspeed = 10
        self.image = self.spritearray.images[int(self.animindex)]
        self.missile_rect = self.image.get_rect(center = (self.x, self.y))
        self.target = target
        self.targetgroup = targetgroup
        self.velocity = 1000
        self.hitradius = 16
        self.originx, self.originy = self.x, self.y
        self.hitbox = [0,0,0,0]
        self.rotate = 0
        self.direction = 0
        self.directionoffset = ypos

    def findobjectangle(self,thing):
            # Find angle of thing
            dx = self.originx - thing.x
            dy = self.originy - thing.y
            self.theta = math.atan2(-dy,dx)
            return self.theta

    def objectdirection(self,direction):
        pewdir = direction - math.pi/2
        sin_a = math.sin(pewdir)
        cos_a = math.cos(pewdir)
        self.x += self.velocity * sin_a * Variables.delta_time
        self.y += self.velocity * cos_a * Variables.delta_time
        return self.x, self.y

    def animate(self):
        import Functions
        Functions.soanimate(self)

    def update(self):
        self.animate()
        try:
            self.targetgroup.index(self.target)
            self.direction = self.findobjectangle(self.target) - self.directionoffset
            if self.directionoffset > 0: self.directionoffset -= self.velocity/125*Variables.delta_time
            elif self.directionoffset < 0: self.directionoffset += self.velocity/125*Variables.delta_time
        except: pass
        orig_rect = self.image.get_rect()
        self.rotated_image = pygame.transform.rotate(self.image,self.direction*180/3.14)
        rot_rect = orig_rect.copy()
        rot_rect.center = self.rotated_image.get_rect().center
        self.rotated_image = self.rotated_image.subsurface(rot_rect).copy()

        self.velocity * Variables.delta_time
        self.originx, self.originy = self.x, self.y
        self.x, self.y = self.objectdirection(self.direction)
        self.missile_rect = self.image.get_rect(center = (self.x, self.y))
        if self.x > CONST.WIDTH+32 or self.y < 0 or self.y > CONST.PAHEIGHT:
            Graphicgroups.missiles.pop(Graphicgroups.missiles.index(self))

    def draw(self,screen):
        screen.blit(self.rotated_image, self.missile_rect)

        self.hitbox = self.missile_rect
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



#region Crosshair
class Crosshair:
    def __init__(self,targetgroup,target):
        self.image = CONST.SURF_CORSSHAIR
        self.targetgroup = targetgroup
        self.target = target
        self.x, self.y = self.targetgroup[self.target].x, self.targetgroup[self.target].y
        self.crosshair_rect = self.image.get_rect(center=(self.x, self.y))
        self.hitbox = self.crosshair_rect
        self.hitradius = self.image.get_rect().centerx

    def update(self):
        try:
            self.x, self.y = self.targetgroup[self.target].x, self.targetgroup[self.target].y
            self.crosshair_rect = self.image.get_rect(center=(self.x, self.y))
        except: Graphicgroups.crosshair.pop(Graphicgroups.crosshair.index(self))


    def draw(self,screen):
        screen.blit(self.image,self.crosshair_rect)
        self.hitbox = self.crosshair_rect
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



#region Dynamic Pew
class DynamicPew:
    def __init__(self,x,y,spritearray,startframe,sizex,sizey,parent=False,loopstart=0,loopend=999,velocity=10):
        self.x, self.y = x, y
        self.parent = parent
        self.sizex, self.sizey = sizex, sizey
        self.type = 0
        self.spritearray = spritearray
        self.animindex, self.animspeed, self.loopstart, self.loopend = startframe, 20, loopstart, loopend
        self.image = pygame.transform.scale(self.spritearray.images[int(self.animindex)],(16*self.sizex,16*self.sizey))
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.velocity = 500 * velocity
        self.hitbox = [0,0,0,0]

    def animate(self):
        self.animindex += self.animspeed * Variables.delta_time #length of ime before we advance the animation frame
        if self.animindex > len(self.spritearray.images)-1 or self.animindex > self.loopend: self.animindex = self.loopstart # reset the frame to 0 if we try to go beyond the array
        self.image = pygame.transform.scale(self.spritearray.images[int(self.animindex)],(8*self.sizex,8*self.sizey)) # update the current frame

    def update(self):
        self.animate()
        self.hitbox = self.rect
        if self.parent == False:
            self.rect = self.image.get_rect(midleft = (self.x, self.y))
            self.x += self.velocity * Variables.delta_time
            if self.x > CONST.WIDTH+500: Graphicgroups.dynamicpew.pop(Graphicgroups.dynamicpew.index(self))
        else:
            self.rect = self.image.get_rect(center = (self.x, self.y))
            self.x = player.location[0]+32
            self.y = player.location[1]

    def draw(self,screen):
        import Functions
        self.hitbox = self.rect
        self.hitbox = Functions.shrink_hitbox(self.hitbox,10)
        screen.blit(self.image, self.rect)
        if Variables.hitboxshow: pygame.draw.rect(screen, (0,255,0),self.hitbox, 2)

    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False

    def spawn(player,sizex,sizey,pewsprite,velocity):
        if len(Graphicgroups.dynamicpew) < 1:
            if pygame.time.get_ticks() - player.last_pewtimer >= 200:
                Graphicgroups.dynamicpew.append(DynamicPew(
                    x=player.spaceship_rect.center[0],
                    y=player.spaceship_rect.center[1],
                    spritearray=pewsprite,
                    startframe=0,
                    sizex=sizex,
                    sizey=sizey,
                    velocity=velocity
                ))
                pygame.mixer.Channel(8).play(CONST.PLAYER_PEW_SOUNDS[1])
                player.last_pewtimer = pygame.time.get_ticks()




#region ENVIRONMENT




#region Planet
class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x, self.y = CONST.WIDTH+500, random.randrange(0,CONST.PAHEIGHT)
        self.scale = random.randint(5,15)/10
        self.num = random.randint(0,len(CONST.SURF_PLANET)-1)
        self.image = CONST.SURF_PLANET[self.num]
        self.image = pygame.transform.scale(self.image,(self.image.get_width()*self.scale,self.image.get_height()*self.scale))
        self.rect = self.image.get_rect(center = (self.x,self.y))
        self.velocity = 50
    
    def update(self,player):
        self.rect = self.image.get_rect(center = (self.x,self.y))
        self.x -= self.velocity * Variables.delta_time
        if self.x < -500: self.kill()
    
    def spawn():
        Graphicgroups.planet_group.add(Planet())



#region Star
class Star(pygame.sprite.Sprite):
    def __init__(self,velocity,x=CONST.WIDTH + 100):
        super().__init__()
        self.menustarmessage = [
            "Music by Nerdthagoras",
            "SUBSCRIBE",
            "Also on Twtich",
            "Please Donate!",
            "This is a long string of text",
        ]
        self.x, self.y = x, random.randrange(50,CONST.PAHEIGHT-50)
        self.kana = random.randint(0,45)
        self.menustar = random.randint(0,len(self.menustarmessage)*20)
        fontsize = 15
        star_font = pygame.font.SysFont(CONST.DEFAULT_FONT_NAME, fontsize)
        if Variables.current_game_state == "GameOver": self.image = star_font.render('GAME OVER', True, 'white')
        elif Variables.current_game_state == "Menu" and self.menustar < len(self.menustarmessage): self.image = star_font.render(self.menustarmessage[self.menustar], True, 'white')
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



#region Bridge
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
            pygame.mixer.Sound.play(CONST.SOUND_BRIDGE_WHOOSH)
            self.sound = False
        if self.x < Settings.question_position[0]-40 and self.x > Settings.question_position[0]-80 and self.drawn == False:
            Variables.kananum += 1
            if Variables.kananum >= len(Variables.gamekana[Variables.level]) or Variables.kananum > Settings.max_bridge_wipes_per_level:
                Variables.kananum = 0
                if Variables.level < 9:
                    Variables.transition = True
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
        Graphicgroups.bridge_group.add(Bridge(CONST.WIDTH,0,CONST.SURF_BRIDGE))



#region Explosion
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



#region Tip Ticker
class TipTicker(pygame.sprite.Sprite):
    def __init__(self,message,velocity):
        super().__init__()
        self.message = message
        tip_font = pygame.font.SysFont(CONST.DEFAULT_FONT_NAME, 30)
        self.image = tip_font.render(self.message, True, 'yellow')
        self.messagebox = self.image.get_rect()
        self.x, self.y = CONST.WIDTH + self.messagebox.centerx, 100
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.velocity = velocity

    def update(self):
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.x -= self.velocity * Variables.delta_time
        if self.x < -1000: self.kill()

    def spawn(message,velocity=200):
        Graphicgroups.tip_group.add(TipTicker(message,velocity))



#region Space Junk
class SpaceJunk:
    def __init__(self,num,rotate,scale):
        self.image = pygame.image.load(os.getcwd() + CONST.SPACE_JUNK_FILES[num][0]).convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.image.get_width()*scale,self.image.get_height()*scale))
        self.x, self.y = CONST.WIDTH+50, random.randrange(128,CONST.PAHEIGHT-128)
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
        whichjunk = random.randint(0,len(CONST.SPACE_JUNK_FILES)-1)
        junksize = random.randrange(2,10)
        Graphicgroups.spacejunk.append(SpaceJunk(whichjunk,random.randrange(-100,100),junksize*0.1))
        try:
            junkobject = pygame.mixer.Sound(os.getcwd() + CONST.SPACE_JUNK_FILES[whichjunk][1])
            junkobject.set_volume(junksize*0.1)
            pygame.mixer.Sound.play(junkobject)
        except: pass



#region Cut Off Line
class CutOffLine:
    def __init__(self,x,y,kanatohit,lastkana):
        self.x, self.y = x, y
        self.lastkana = lastkana
        self.kanatohit = kanatohit
        self.last_kana_text = CONST.QUESTION_FONT.render(self.lastkana, True, 'white')
        self.next_kana_text = CONST.QUESTION_FONT.render(self.kanatohit, True, 'white')
        self.lkt_rect = self.last_kana_text.get_rect()
        self.nkt_rect = self.next_kana_text.get_rect()
        self.velocity = Settings.kanax_velocity
        self.kanaoffset = 40
        self.box = pygame.Rect(self.x,0,2,CONST.PAHEIGHT)

    def update(self,player):
        self.x -= self.velocity * Variables.delta_time
        self.box = pygame.Rect(self.x,0,2,CONST.PAHEIGHT)
        if self.x < -50: Graphicgroups.cuttoffline.pop(Graphicgroups.cuttoffline.index(self))

    def draw(self,screen):
        pygame.draw.rect(screen, (128,0,0), self.box, 2)
        screen.blit(self.last_kana_text, (self.x-self.kanaoffset-(self.lkt_rect.centerx), CONST.PAHEIGHT-128))
        screen.blit(self.next_kana_text, (self.x+self.kanaoffset-(self.nkt_rect.centerx), CONST.PAHEIGHT-128))
        screen.blit(self.last_kana_text, (self.x-self.kanaoffset-(self.lkt_rect.centerx), 8))
        screen.blit(self.next_kana_text, (self.x+self.kanaoffset-(self.nkt_rect.centerx), 8))

    def spawn():
        Graphicgroups.cuttoffline.append(CutOffLine(CONST.WIDTH+CONST.off_screen_offset,0,Variables.gamekana[Variables.level][Variables.kananum][2],Variables.gamekana[Variables.last_level][Variables.last_kananum][2]))



#region Big Laser
class BigLaser:
    def __init__(self,x,y):
        self.type = 0
        self.spritearray = CONST.SURF_BIG_LASER #Sprite Animation
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
        Functions.moanimate(self,loopstart=0,loopend=999)

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
        Graphicgroups.biglasers.append(BigLaser(CONST.WIDTH+1000,y))
        pygame.mixer.Sound.play(CONST.SOUND_BIG_LASER)



#region Big Laser Warning
class BigLaserWarning:
    def __init__(self,y):
        self.last_warn_timer = 0
        self.opacity = True
        self.y = y
        self.image_flash_delay = 100
        self.warning_length = 10
        self.image = CONST.SURF_BIGLASER_WARN

    def update(self):
        if self.warning_length > 0:
            if pygame.time.get_ticks() - self.last_warn_timer >= self.image_flash_delay:
                if self.opacity == True:
                    self.opacity = False
                else:
                    self.opacity = True
                    pygame.mixer.Sound.play(CONST.SOUND_BIG_LASER_WARN)
                self.warning_length -= 1
                self.last_warn_timer = pygame.time.get_ticks()
        if self.warning_length <= 0:
            pygame.mixer.Sound.stop(CONST.SOUND_BIG_LASER_WARN)
            BigLaser.spawn(self.y)
            Graphicgroups.warnings.pop(Graphicgroups.warnings.index(self))

    def draw(self,screen):
        if self.opacity == True:
            self.warning_rect = self.image.get_rect(midright = (CONST.WIDTH, self.y))
            screen.blit(self.image, self.warning_rect)

    def spawn(player):
        Graphicgroups.warnings.append(BigLaserWarning(random.randint(player.spaceship_rect.center[1]-64,player.spaceship_rect.center[1]+64)))



#region Anim Center Warn
class AnimCenterWarning:
    def __init__(self,message,surface,typeof,scale,fade=True,pos=(CONST.WCENTER, CONST.HCENTER)):
        self.spritearray = surface #Sprite Animation
        self.pos = pos
        self.type = typeof
        self.animindex = 0  #Sprite Animation
        self.animspeed = 10
        self.scale = scale
        self.image = self.spritearray[self.type].images[self.animindex] #Sprite Animation
        self.image_scaled = pygame.transform.scale(self.image,(self.image.get_rect().width*self.scale,self.image.get_rect().height*self.scale))
        self.centered_image = self.image_scaled.get_rect(center = self.pos)
        self.fade = fade
        self.alpha = 255
        self.message = message

    def animate(self):
        import Functions
        Functions.moanimate(self,loopstart=0,loopend=999)
        
    def update(self):
        self.animate()
        if self.fade:
            self.alpha -= 100 * Variables.delta_time
            if self.alpha <= 0: Graphicgroups.animcenterwarning.pop(Graphicgroups.animcenterwarning.index(self))

    def draw(self):
        self.warning_text = CONST.WARNING_FONT.render(self.message, True, 'white')
        self.warning_text.set_alpha(self.alpha)
        self.image_scaled = pygame.transform.scale(self.image,(self.image.get_rect().width*self.scale,self.image.get_rect().height*self.scale))
        self.image_scaled.set_alpha(self.alpha)
        self.centered_warning = self.warning_text.get_rect(center = self.pos)
        self.centered_image = self.image_scaled.get_rect(center = self.pos)
        CONST.SCREEN.blit(self.image_scaled, self.centered_image)
        CONST.SCREEN.blit(self.warning_text, self.centered_warning)

    def spawn(message,surface,scale=1):
        Graphicgroups.animcenterwarning.append(CenterWarning(message,surface,scale))



#region Center Warning
class CenterWarning:
    def __init__(self,message,surface,scale,fade=True,pos=(CONST.WCENTER, CONST.HCENTER)):
        self.pos = pos
        self.fade = fade
        self.alpha = 1024
        self.message = message
        self.surf = surface
        self.scale = scale

    def update(self):
        if self.fade:
            self.alpha -= 400 * Variables.delta_time
            if self.alpha <= 0: Graphicgroups.centerwarning.pop(Graphicgroups.centerwarning.index(self))

    def draw(self):
        warning_text = CONST.WARNING_FONT.render(self.message, True, 'white')
        warning_text.set_alpha(self.alpha)
        self.surf_scaled = pygame.transform.scale(self.surf,(self.surf.get_rect().width*self.scale,self.surf.get_rect().height*self.scale))
        self.surf_scaled.set_alpha(self.alpha)
        centered_warning = warning_text.get_rect(center = self.pos)
        centered_image = self.surf_scaled.get_rect(center = self.pos)
        CONST.SCREEN.blit(self.surf_scaled,centered_image)
        CONST.SCREEN.blit(warning_text, centered_warning)

    def spawn(message,surface,scale=1):
        Graphicgroups.centerwarning.append(CenterWarning(message,surface,scale))



#region Border Scenery
class BorderScenery:
    def __init__(self,image,y=192):
        self.image = image
        self.x, self.y = CONST.WIDTH+64, CONST.PAHEIGHT-y
        self.velocity = 120
        self.type = Variables.scenerytype           # 0 = Nothing, 1 = Opening, 2 = Middle, 3 = End
        self.height = Variables.sceneryheight         # 1 = Short, 2 = Medium, 3 = High
        self.hitbox = [0,0,0,0]

    def picknext(self):
        match self.type:
            case 0:
                Variables.scenerytype = random.randint(0,1)
                Variables.sceneryheight = random.randint(1,1)
            case 1:
                Variables.scenerywaittime = .5
                match self.height:
                    case 1:
                        max = len(CONST.SURF_SCENERY_OPEN_1H.images)-1
                        Graphicgroups.scenery.append(BorderScenery(
                            CONST.SURF_SCENERY_OPEN_1H.images[random.randint(0,max)],
                            64
                        ))
                        Variables.scenerytype = random.randint(2,2)
                    case 2:
                        max = len(CONST.SURF_SCENERY_OPEN_2H.images)-1
                        Graphicgroups.scenery.append(BorderScenery(
                            CONST.SURF_SCENERY_OPEN_2H.images[random.randint(0,max)],
                            128
                        ))
                        Variables.scenerytype = random.randint(2,3)
                    case 3:
                        Variables.scenerytype = random.randint(2,3)
            case 2:
                match self.height:
                    case 1:
                        max = len(CONST.SURF_SCENERY_MID_1H.images)-1
                        Graphicgroups.scenery.append(BorderScenery(
                            CONST.SURF_SCENERY_MID_1H.images[random.randint(0,max)],
                            64
                        ))
                        Variables.scenerytype = random.randint(2,3)
                    case 2:
                        max = len(CONST.SURF_SCENERY_MID_2H.images)-1
                        Graphicgroups.scenery.append(BorderScenery(
                            CONST.SURF_SCENERY_MID_2H.images[random.randint(0,max)],
                            128
                        ))
                        Variables.scenerytype = random.randint(2,3)
                    case 3:
                        Variables.scenerytype = random.randint(2,3)
            case 3:
                chance = random.randint(0,8)
                match self.height:
                    case 1:
                        if chance == 0: Graphicgroups.turrets.append(GroundTurret(CONST.WIDTH+32,CONST.PAHEIGHT-64,0))
                        max = len(CONST.SURF_SCENERY_CLOSE_1H.images)-1
                        Graphicgroups.scenery.append(BorderScenery(
                            CONST.SURF_SCENERY_CLOSE_1H.images[random.randint(0,max)],
                            64
                        ))
                        Variables.scenerytype = random.randint(0,1)
                        Variables.sceneryheight = random.randint(0,2)
                    case 2:
                        if chance == 0: Graphicgroups.turrets.append(GroundTurret(CONST.WIDTH+32,CONST.PAHEIGHT-128,0))
                        max = len(CONST.SURF_SCENERY_CLOSE_2H.images)-1
                        Graphicgroups.scenery.append(BorderScenery(
                            CONST.SURF_SCENERY_CLOSE_2H.images[random.randint(0,max)],
                            128
                        ))
                        Variables.scenerytype = random.randint(1,1)
                    case 3:
                        Variables.scenerytype = random.randint(0,1)
                Variables.sceneryheight = random.randint(1,2)

    def update(self):
        self.scenery_rect = self.image.get_rect(topleft = (self.x, self.y))
        self.hitbox = self.scenery_rect
        self.x -= self.velocity * Variables.delta_time
        if self.x < -64: Graphicgroups.scenery.pop(Graphicgroups.scenery.index(self))

    def draw(self,screen):
        screen.blit(self.image, self.scenery_rect)
        if Variables.hitboxshow:
            pygame.draw.rect(screen, (255,0,0),self.scenery_rect, 2)

    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False



#region INTERACTABLES




#region Kans
class Kana:
    def __init__(self,x,y,kana,group,fade,rotate,newmessage="",color='white',new=False):
        # self.kananum, self.last_kananum = 0, 0
        self.x, self.y = x, y
        self.bounced = False
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
        self.kanatext = CONST.KANA_FONT.render(Variables.gamekana[self.level][self.kana][Variables.gamemode], True, self.color)
        self.kana_graphic = CONST.UI_FONT.render(Variables.gamekana[self.level][self.kana][0] + Variables.gamekana[self.level][self.kana][1] + Variables.gamekana[self.level][self.kana][2],True,'yellow')
        self.kanascale = 1
        self.orig_rect = self.kanatext.get_rect()
        self.rotated_image = pygame.transform.rotate(self.kanatext,self.rotate)
        self.rot_rect = self.orig_rect.copy()
        self.rot_rect.center = self.rotated_image.get_rect().center
        self.rotated_image = self.rotated_image.subsurface(self.rot_rect).copy()
        self.scale_image = pygame.transform.scale(self.rotated_image,(self.kanatext.get_rect().width*self.kanascale,self.kanatext.get_rect().height*self.kanascale))
        self.centered_image = self.scale_image.get_rect(center = (self.x,self.y))
        self.hitbox = [0,0,0,0]
        self.graphicgroup = group
        self.kana_blip = 0
        self.correct_kana_lost_sound_play = True

    def update(self,player):
        self.rotate += self.rotate_rate * Variables.delta_time
        self.kanatext = CONST.KANA_FONT.render(Variables.gamekana[self.level][self.kana][Variables.gamemode], True, self.color)
        self.kana_graphic = CONST.UI_FONT.render(Variables.gamekana[self.level][self.kana][0] + Variables.gamekana[self.level][self.kana][1] + Variables.gamekana[self.level][self.kana][2],True,'yellow')
        self.x -= self.xvelocity * Variables.delta_time
        if self.y > Settings.ship_screen_boundary and self.y < CONST.PAHEIGHT - Settings.ship_screen_boundary:
            self.y += self.yvelocity * Variables.delta_time
        if self.x < -64: self.graphicgroup.pop(self.graphicgroup.index(self))

        if self.graphicgroup == Graphicgroups.correctkanas:
            # Grow Kana at 2/5th of the screen with
            if self.x < 2 * (CONST.WIDTH // 5) and self.x > 10:
                self.kanascale += Variables.delta_time/5
                if self.kana_blip >= self.x/500:
                    pygame.mixer.Sound.play(CONST.SOUND_CORRECT_KANA_LOSING)
                    self.kana_blip = 0
                self.kana_blip += 1 * Variables.delta_time
            elif self.x < 0:
                if self.correct_kana_lost_sound_play:
                    pygame.mixer.Sound.play(CONST.SOUND_CORRECT_KANA_LOST)
                    explosion = Explosion(x=self.x, y=self.y,spritearray=CONST.SURF_EXPLOSION,scale=1,repeat=False,explosiontype=1)
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
            shoot_text = CONST.KANA_UI_FONT.render(self.newmessage,True,(255,0,0))
            shoot_here_surf.set_alpha(alpha)
            shoot_here_surf.blit(shoot_text,(0,25))

            screen.blit(shoot_here_surf, shoot_here_pos)

        # Draw hitbox
        import Functions
        self.hitbox = self.centered_image
        self.hitbox = Functions.shrink_hitbox(self.hitbox,8)
        if Variables.hitboxshow:
            screen.blit(self.kana_graphic,self.centered_image.bottomleft)
            pygame.draw.circle(screen,(0,0,255),(self.x,self.y), 4)
            pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)

    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False



#region Boss Mode Kanas
class BossModeKana:
    def __init__(self,x,y,kana,group,fade,rotate):
        self.x, self.y = x, y
        self.kanakill = int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3])*(255/Settings.num_to_shoot_new_kana)
        self.color = 'white'
        self.xvelocity, self.yvelocity = Settings.kanax_velocity, Settings.kanay_velocity
        self.shrink = 5
        self.kana = kana
        self.level = Variables.level
        self.fade = fade
        self.rotate = 0
        self.rotate_rate = (rotate * Variables.level) / 2
        self.kanasound = Variables.gamekana[self.level][self.kana][2]
        self.kanatext = CONST.KANA_FONT.render(Variables.gamekana[self.level][self.kana][Variables.gamemode], True, self.color)
        self.kana_graphic = CONST.UI_FONT.render(Variables.gamekana[self.level][self.kana][0] + Variables.gamekana[self.level][self.kana][1] + Variables.gamekana[self.level][self.kana][2],True,'yellow')
        self.kanascale = 1
        self.orig_rect = self.kanatext.get_rect()
        self.rotated_image = pygame.transform.rotate(self.kanatext,self.rotate)
        self.rot_rect = self.orig_rect.copy()
        self.rot_rect.center = self.rotated_image.get_rect().center
        self.rotated_image = self.rotated_image.subsurface(self.rot_rect).copy()
        self.scale_image = pygame.transform.scale(self.rotated_image,(self.kanatext.get_rect().width*self.kanascale,self.kanatext.get_rect().height*self.kanascale))
        self.centered_image = self.scale_image.get_rect(center = (self.x,self.y))
        self.hitbox = [0,0,0,0]
        self.graphicgroup = group
        self.kana_blip = 0
        self.correct_kana_lost_sound_play = True

    def update(self,player):
        self.kanatext = CONST.KANA_FONT.render(Variables.gamekana[self.level][self.kana][Variables.gamemode], True, self.color)
        self.kana_graphic = CONST.UI_FONT.render(Variables.gamekana[self.level][self.kana][0] + Variables.gamekana[self.level][self.kana][1] + Variables.gamekana[self.level][self.kana][2],True,'yellow')
        self.y += self.xvelocity * Variables.delta_time
        if self.y > CONST.PAHEIGHT+64: self.graphicgroup.pop(self.graphicgroup.index(self))

        if self.graphicgroup == Graphicgroups.bossmodecorrectkana:
            # Grow Kana at 3/5th of the screen height
            if self.y > 3 * (CONST.PAHEIGHT // 5) and self.y < CONST.PAHEIGHT+32:
                self.kanascale += Variables.delta_time/5
                if self.kana_blip >= self.x/500:
                    pygame.mixer.Sound.play(CONST.SOUND_CORRECT_KANA_LOSING)
                    self.kana_blip = 0
                self.kana_blip += 1 * Variables.delta_time
            elif self.y > CONST.PAHEIGHT+32:
                if self.correct_kana_lost_sound_play:
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



#region Anim Powerup
class AnimatedPowerUp:
    def __init__(self,x,y,xvelocity,typeof,pueffect):
        self.type = typeof #Sprite Animation
        self.spritearray = CONST.SURF_POWER_UP #Sprite Animation
        self.animindex = 0  #Sprite Animation
        self.animspeed = 10 #Sprite Animation
        self.image = self.spritearray[self.type].images[self.animindex] #Sprite Animation
        self.x, self.y = x, y
        self.powerup_rect = self.image.get_rect(center = (self.x, self.y))
        self.xvelocity = xvelocity # Check Constants.powerup_array
        self.hitbox = []
        self.shieldradius = 32
        self.pueffect = pueffect

    def animate(self):
        import Functions
        Functions.moanimate(self,loopstart=0,loopend=999)

    def effect(self,pueffect,player):
        if pueffect == "laser":
            if self.collide(player.spaceship_rect):
                Graphicgroups.animatedpowerup.pop(Graphicgroups.animatedpowerup.index(self))
                player.lasersight = True
                player.lasersightcounter = player.poweruptimelength
                pygame.mixer.Sound.play(CONST.SOUND_POWER_UP)
                pygame.mixer.Sound.play(CONST.SOUND_SHIP_LASER)
        if pueffect == "speed":
            if self.collide(player.spaceship_rect):
                Graphicgroups.animatedpowerup.pop(Graphicgroups.animatedpowerup.index(self))
                player.speedboost = True
                player.speedboostcounter = player.poweruptimelength
                pygame.mixer.Sound.play(CONST.SOUND_POWER_UP)
        if pueffect == "switch":
            if self.collide(player.spaceship_rect):
                Graphicgroups.animatedpowerup.pop(Graphicgroups.animatedpowerup.index(self))
                player.kanaswitch = True
                player.kanaswitchcounter = player.poweruptimelength
                pygame.mixer.Sound.play(CONST.SOUND_POWER_UP)
        if pueffect == "1up":
            if self.collide(player.spaceship_rect):
                Graphicgroups.animatedpowerup.pop(Graphicgroups.animatedpowerup.index(self))
                player.lives += 1
                pygame.mixer.Sound.play(CONST.SOUND_POWER_UP)
        if pueffect == "powerup":
            if self.collide(player.spaceship_rect):
                Graphicgroups.animatedpowerup.pop(Graphicgroups.animatedpowerup.index(self))
                if player.pewtype < len(CONST.ARRAY_PLAYER_PEW)-1:
                    player.pewtype += 1
                    Variables.missiles_enabled = CONST.ARRAY_PLAYER_PEW[player.pewtype]["missiles"]
                    pygame.mixer.Sound.play(CONST.SOUND_POWER_UP)
                else: player.pewtype = 0

    def update(self):
        amplitude = .2
        frequency = 200
        phase = random.randint(0,120)
        self.effect(self.pueffect,player)
        self.x -= self.xvelocity * Variables.delta_time
        self.y += amplitude * math.sin((self.x-phase)/frequency)                    # Sine wave for the y axis
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
        x = CONST.WIDTH+64
        y = random.randrange(96,CONST.PAHEIGHT-220)
        xvelocity = xvel
        Graphicgroups.animatedpowerup.append(AnimatedPowerUp(x, y,xvelocity,typeof,pueffect))



#region Ground Turrets
class GroundTurret:
    def __init__(self,x,y,typeof):
        self.type = typeof #Sprite Animation
        self.spritearray = CONST.SURF_TURRET #Sprite Animation
        self.animindex = 0  #Sprite Animation
        self.animspeed = 20 #Sprite Animation
        self.missilechance = 5
        self.image = self.spritearray[self.type].images[self.animindex] #Sprite Animation
        self.x, self.y = x, y-32
        self.turretopening = self.image.get_rect(topleft = (self.x, self.y))
        self.xvelocity = 120
        self.last_turret_pew = 0
        self.hitbox = [0,0,0,0]
        self.turretfiring = False

    def animate(self):
        if self.turretfiring == True:
            self.animindex += self.animspeed * Variables.delta_time #length of ime before we advance the animation frame
            if self.animindex > len(self.spritearray[self.type].images)-1:
                self.animindex = 0 # reset the frame to 0 if we try to go beyond the array
                self.turretfiring = False
        self.image = self.spritearray[self.type].images[int(self.animindex)] # update the current frame

    def findobjectangle(self,player):
        # Find angle of player
        dx = self.x - player.spaceship_rect.center[0]
        dy = self.y - player.spaceship_rect.center[1]
        self.theta = math.atan2(-dy,dx)
        return self.theta

    def shoot(self,player):
        if player.location[0] < self.x-300:
            angle = self.findobjectangle(player)
            if pygame.time.get_ticks() - self.last_turret_pew >= random.randint(2000,10000):
                self.turretfiring = True
                rnd = (random.randint(1,self.missilechance))
                if rnd != self.missilechance:
                    pygame.mixer.Sound.play(CONST.SOUND_TURRET_FIRING)
                    try: Graphicgroups.enemyprojectiles.append(EnemyProjectiles(
                        x=self.turretopening[0],
                        y=self.turretopening[1],
                        direction=angle,
                        origin=Graphicgroups.turrets.index(self)
                    ))
                    except: pass
                if rnd == self.missilechance:
                    pygame.mixer.Sound.play(CONST.SOUND_MISSILE_LAUNCHED)
                    try: Graphicgroups.enemymissiles.append(EnemyHomingMissile(
                        x=self.turretopening[0],
                        y=self.turretopening[1],
                        playerloc= player,
                        ypos=1,
                        image=CONST.SURF_ENEMY_MISSILE[0]
                    ))
                    except: pass
                self.last_turret_pew = pygame.time.get_ticks()

    def update(self):
        self.animate()
        if self.x < -64: Graphicgroups.turrets.pop(Graphicgroups.turrets.index(self))
        self.x -= self.xvelocity * Variables.delta_time
        self.turretopening = self.image.get_rect(topleft = (self.x, self.y))
        self.shoot(player)

    def draw(self,screen):
        self.hitbox = self.image.get_rect(center = (self.x, self.y))
        screen.blit(self.image, self.hitbox)

        # Draw hitbox
        if Variables.hitboxshow:
            pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)

    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False



#region Enemy Homing Misile
class EnemyHomingMissile:
    def __init__(self,x,y,playerloc,ypos,image):
        self.spritearray = image
        self.x, self.y = x, y
        self.target = playerloc
        self.type = 0
        self.animindex = 0
        self.animspeed = 10
        self.image = self.spritearray.images[int(self.animindex)]
        self.missile_rect = self.image.get_rect(center = (self.x, self.y))
        self.velocity = 600
        self.hitradius = 16
        self.originx, self.originy = self.x, self.y
        self.hitbox = [0,0,0,0]
        self.rotate = 0
        self.direction = 0
        self.directionoffset = 0
        self.rotated_image = pygame.transform.rotate(self.image,self.direction*180/3.14)

    def findobjectangle(self,thing):
            # Find angle of thing
            dx = self.originx - thing.x
            dy = self.originy - thing.y
            self.theta = math.atan2(-dy,dx)
            return self.theta

    def objectdirection(self,direction):
        pewdir = direction - math.pi/2
        sin_a = math.sin(pewdir)
        cos_a = math.cos(pewdir)
        self.x += self.velocity * sin_a * Variables.delta_time
        self.y += self.velocity * cos_a * Variables.delta_time
        return self.x, self.y

    def animate(self):
        import Functions
        Functions.soanimate(self)

    def update(self):
        self.animate()
        try:
            self.direction = self.findobjectangle(self.target) - self.directionoffset
            if self.directionoffset > 0: self.directionoffset -= self.velocity/125*Variables.delta_time
            elif self.directionoffset < 0: self.directionoffset += self.velocity/125*Variables.delta_time
        except: pass
        orig_rect = self.image.get_rect()
        self.rotated_image = pygame.transform.rotate(self.image,self.direction*180/3.14)
        rot_rect = orig_rect.copy()
        rot_rect.center = self.rotated_image.get_rect().center
        self.rotated_image = self.rotated_image.subsurface(rot_rect).copy()

        self.velocity * Variables.delta_time
        # self.originx, self.originy = self.x, self.y
        self.x, self.y = self.objectdirection(self.direction)
        self.missile_rect = self.image.get_rect(center = (self.x, self.y))
        if self.x > CONST.WIDTH+32 or self.y < 0 or self.y > CONST.PAHEIGHT:
            Graphicgroups.enemymissiles.pop(Graphicgroups.enemymissiles.index(self))

    def draw(self,screen):
        screen.blit(self.rotated_image, self.missile_rect)

        self.hitbox = self.missile_rect
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



#region Enemies
class Enemies:
    def __init__(self,typeof,loopstart=0,loopend=999):
        self.type = typeof
        self.loopstart, self.loopend = loopstart, loopend
        self.spritearray = CONST.SURF_ENEMY #Sprite Animation
        self.animindex = 0  #Sprite Animation
        self.animspeed = random.randint(10,20) #Sprite Animation
        self.image = self.spritearray[self.type].images[self.animindex] #Sprite Animation
        self.x, self.y = CONST.WIDTH, random.randrange(128,CONST.PAHEIGHT-128)
        self.enemy_rect = self.image.get_rect(midleft = (self.x, self.y))
        self.velocity = random.randint(50,200)
        self.Yvelocity = random.randint(-50,50)
        self.knockbackx = 0
        self.knockbacky = 0
        self.last_enemy_pew = 0

        self.maxhealth = Variables.generatedcorrectkanacounter + 1
        self.health = self.maxhealth
        self.maxhealth_grapic = CONST.UI_FONT.render(str(self.maxhealth), True, 'green')
        self.curhealth_grapic = CONST.UI_FONT.render(str(self.health), True, 'yellow')
        self.healthbar_height = 5
        self.healthbar = pygame.Surface((self.enemy_rect.width,5)).convert_alpha()
        self.healthbar_Color = (255-(255/self.maxhealth*self.health),255/self.maxhealth*self.health,0)

    def calculate_angles(self,number_of_angles):
        if number_of_angles < 1:
            return []
        
        angle_step = 360 / number_of_angles
        angles = [i * angle_step for i in range(number_of_angles)]
        return angles

    def animate(self):
        import Functions
        Functions.moanimate(self,loopstart=0,loopend=999)

    def shoot(self,player):
        angle = self.findobjectangle(player)
        if pygame.time.get_ticks() - self.last_enemy_pew >= random.randint(2000,10000):
            if self.type%3 == 0: # AIMED SHOT
                if angle < math.pi/3 and angle > -math.pi/3:
                    pygame.mixer.Sound.play(CONST.SOUND_ENEMY_PEW)
                    Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,angle,Graphicgroups.enemies.index(self)))
            elif self.type%3 == 1: # FORWARD SHOT
                pygame.mixer.Sound.play(CONST.SOUND_ENEMY_PEW)
                Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,math.radians(random.randint(-10,10)),Graphicgroups.enemies.index(self)))
            elif self.type%3 == 2: #AoE SHOT
                pygame.mixer.Sound.play(CONST.SOUND_ENEMY_PEW)
                for angle in self.calculate_angles(8):
                    Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,math.radians(random.randint(angle-10,angle+10)),Graphicgroups.enemies.index(self)))
            self.last_enemy_pew = pygame.time.get_ticks()

    def update(self):
        self.healthdisplay = self.enemy_rect.width/self.maxhealth*self.health
        self.healthbar_Color = (255-(255/self.maxhealth*self.health),255/self.maxhealth*self.health,0)
        self.curhealth_grapic = CONST.UI_FONT.render(str(self.health), True, 'yellow')
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
        if self.x < -128 or self.y > CONST.PAHEIGHT + 128 or self.y < -128: Graphicgroups.enemies.pop(Graphicgroups.enemies.index(self))
        self.shoot(player)
    
    def findobjectangle(self,player):
            # Find angle of player
            dx = self.x - player.spaceship_rect.center[0]
            dy = self.y - player.spaceship_rect.center[1]
            self.theta = math.atan2(-dy,dx)
            return self.theta

    def draw(self,screen,player):
        import Functions
        screen.blit(self.image, self.enemy_rect)
        screen.blit(self.healthbar, (self.enemy_rect.left,self.enemy_rect.top-20,self.enemy_rect.width,10))
        self.healthbar.fill((0,0,0,0))
        try: pygame.draw.rect(self.healthbar,self.healthbar_Color,(0,0,self.healthdisplay,self.healthbar_height))
        except: pass
        self.hitbox = self.enemy_rect
        self.hitbox = Functions.shrink_hitbox(self.enemy_rect,5)
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



#region Bosses
class Bosses:
    def __init__(self,typeof,health,bossimage,numofbullets,Xvel,Yvel,anglenum,animspeed):
        # Music Settings
        self.music = CONST.ARRAY_BOSSES[Variables.level]["music"]
        Variables.musicvolume = Settings.maxmusicvolume
        pygame.mixer.music.load(os.path.join('music',str(self.music) + '.wav'))
        pygame.mixer.music.play(-1)

        # Shooting Settings
        self.rapidfire = 0
        self.lastrapidfire = 0
        self.numberofbullets = numofbullets
        self.bulletfrequency = 1
        self.anglenum = anglenum
        self.type = typeof
        self.last_boss_pew = 0

        # Animation Settings
        self.animspeed = animspeed
        self.bossimage = bossimage
        self.animindex = 0
        self.spritearray = CONST.SURF_BOSS
        self.image = self.spritearray[self.bossimage].images[self.animindex]
        self.shieldanimindex = 0
        self.shieldarray = CONST.SURF_SHIELD
        self.shield = self.shieldarray.images[self.shieldanimindex]

        # Movement Settings
        self.enter_screen = False
        self.x, self.y = CONST.WIDTH, random.randrange(128,CONST.PAHEIGHT-128)
        self.boss_rect = self.image.get_rect(midleft = (self.x, self.y))
        self.velocity = random.randint(Xvel/2,Xvel)
        self.Yvelocity = random.randint(-Yvel,Yvel)

        # Health Settings
        self.maxhealth = health+1
        self.flash = 0
        self.health = self.maxhealth
        self.maxhealth_grapic = CONST.UI_FONT.render(str(self.maxhealth), True, 'green')
        self.curhealth_grapic = CONST.UI_FONT.render(str(self.health), True, 'yellow')
        self.healthbar_height = 5
        self.healthbar = pygame.Surface((self.boss_rect.width,self.healthbar_height)).convert_alpha()
        self.healthbar_Color = (255-(255/self.maxhealth*self.health),255/self.maxhealth*self.health,0)

        # Shield Settings
        self.shieldbar_height = 5
        self.shieldbar = pygame.Surface((500,self.shieldbar_height)).convert_alpha()
        self.shieldbar_Color = 'cyan'

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

    def animateshield(self):
        self.shieldanimindex += self.animspeed * Variables.delta_time #length of ime before we advance the animation frame
        if self.shieldanimindex > len(self.shieldarray.images)-1: self.shieldanimindex = 0 # reset the frame to 0 if we try to go beyond the array
        self.shield = self.shieldarray.images[int(self.shieldanimindex)] # update the current frame

    def shoot(self,player):
        angle = self.findobjectangle(player)
        if self.rapidfire > self.numberofbullets:
            self.rapidfire = 0
            self.lastrapidfire = 0
        if pygame.time.get_ticks() - self.last_boss_pew >= random.randint(2000,10000) or self.rapidfire != 0:
            if self.type%3 == 0: # AIMED SHOT
                if angle < math.pi/3 and angle > -math.pi/3:
                    if int(self.rapidfire) - self.lastrapidfire == self.bulletfrequency:
                        pygame.mixer.Sound.play(CONST.SOUND_ENEMY_PEW)
                        Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,angle,Graphicgroups.bosses.index(self)))
                        self.lastrapidfire = int(self.rapidfire)
                    self.rapidfire += 10 * Variables.delta_time
            elif self.type%3 == 1: # FORWARD SHOT
                if int(self.rapidfire) - self.lastrapidfire == self.bulletfrequency:
                    pygame.mixer.Sound.play(CONST.SOUND_ENEMY_PEW)
                    Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,math.radians(random.randint(-10,10)),Graphicgroups.bosses.index(self)))
                    self.lastrapidfire = int(self.rapidfire)
                self.rapidfire += 10 * Variables.delta_time
            elif self.type%3 == 2: #AoE SHOT
                if int(self.rapidfire) - self.lastrapidfire == 5*self.bulletfrequency:
                    pygame.mixer.Sound.play(CONST.SOUND_ENEMY_PEW)
                    for angle in self.calculate_angles(self.anglenum):
                        Graphicgroups.enemyprojectiles.append(EnemyProjectiles(self.x, self.y,math.radians(angle),Graphicgroups.bosses.index(self)))
                    self.lastrapidfire = int(self.rapidfire)
                self.rapidfire += 10 * Variables.delta_time                
            self.last_boss_pew = pygame.time.get_ticks()

    def update(self):
        if self.flash > 0: self.flash -= 3
        if self.flash < 0: self.flash = 0
        shieldalpha = CONST.ARRAY_BOSSES[Variables.level]["shield"]/100*200
        self.shield.set_alpha(shieldalpha)
        self.cp = self.image.copy()
        self.cp.fill((self.flash,self.flash,self.flash,0),None, pygame.BLEND_RGBA_ADD)
        self.healthdisplay = self.boss_rect.width/self.maxhealth*self.health
        self.healthbar_Color = (255-(255/self.maxhealth*self.health),255/self.maxhealth*self.health,0)
        self.curhealth_grapic = CONST.UI_FONT.render(str(self.health), True, 'yellow')
        self.animate()
        self.animateshield()
        if self.type%3 == 0 or self.type%3 == 1: self.boss_rect = self.image.get_rect(midleft = (self.x, self.y))
        elif self.type%3 == 2: self.boss_rect = self.image.get_rect(center = (self.x, self.y))
        self.x -= self.velocity * Variables.delta_time
        self.y += self.Yvelocity * Variables.delta_time
        if self.y <= 256 or self.y >= CONST.PAHEIGHT-50: self.Yvelocity *= -1
        if self.x < CONST.WIDTH-256: self.enter_screen = True
        if self.x <= 3*CONST.WIDTH/5: self.velocity *= -1
        if self.x > CONST.WIDTH-256 and self.enter_screen == True: self.velocity *= -1
        self.shoot(player)

    def findobjectangle(self,player):
            # Find angle of player
            dx = self.x - player.spaceship_rect.center[0]
            dy = self.y - player.spaceship_rect.center[1]
            self.theta = math.atan2(-dy,dx)
            return self.theta

    def draw(self,screen,player):
        screen.blit(self.cp, self.boss_rect)
        screen.blit(self.shield, (self.boss_rect[0]-64,self.boss_rect[1]-64))
        
        # Health Bar
        screen.blit(self.healthbar, (
            self.boss_rect.left,        # X
            self.boss_rect.top-20,      # Y
            self.boss_rect.width,       # Width
            10                          # Height
            )
        )
        self.healthbar.fill((0,0,0,0))
        try: pygame.draw.rect(self.healthbar,self.healthbar_Color,(0,0,self.healthdisplay,self.healthbar_height))
        except: pass

        # Shield
        x = Settings.boss_shield_bar
        barwidth = 500
        screen.blit(self.shieldbar, (
            CONST.WCENTER-(barwidth//2),
            x,
            barwidth,
            10
        ))
        self.shieldbar.fill((0,0,0,0))
        try: pygame.draw.rect(self.shieldbar,'cyan',(0,0,barwidth/100 * (CONST.ARRAY_BOSSES[Variables.level]["shield"]),self.healthbar_height))
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
                CONST.ARRAY_BOSSES[Variables.level]["type"],
                (Variables.generatedincorrectkanacounter + Variables.generatedcorrectkanacounter)*CONST.ARRAY_BOSSES[Variables.level]["healthmultiplier"],
                CONST.ARRAY_BOSSES[Variables.level]["imgindx"],
                CONST.ARRAY_BOSSES[Variables.level]["numofbullets"],
                CONST.ARRAY_BOSSES[Variables.level]["Xvel"],
                CONST.ARRAY_BOSSES[Variables.level]["Yvel"],
                CONST.ARRAY_BOSSES[Variables.level]["anglenum"],
                CONST.ARRAY_BOSSES[Variables.level]["animspeed"],
            )
        )



#region Enemy Projectiles
class EnemyProjectiles:
    def __init__(self,x,y,direction,origin):
        self.x, self.y = x, y
        self.direction = direction
        self.skewoffset = 20
        self.directionskew = random.randint(-self.skewoffset,self.skewoffset)/100
        self.image = CONST.SURF_ENEMY_PEW
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
        if self.x < 0 or self.y < 0 or self.y > CONST.PAHEIGHT:
            Graphicgroups.enemyprojectiles.pop(Graphicgroups.enemyprojectiles.index(self))

    def draw(self,screen):
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



#region Wall Of Death
class WallOfDeath:
    def __init__(self,x,y):
        self.x, self.y = x, y
        self.velocity = 50
        self.image = CONST.SURF_WALLSEGMENT

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
            for h in range(int(CONST.PAHEIGHT/32)):
                Graphicgroups.wallsegments.append(WallOfDeath(x+w*32,y+h*32))



#region Debris
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
        direction = math.radians(direction)
        pewdir = direction - math.pi/2 + self.directionskew
        sin_a = math.sin(pewdir)
        cos_a = math.cos(pewdir)
        self.x += self.velocity * sin_a * Variables.delta_time
        self.y += self.velocity * cos_a * Variables.delta_time
        return self.x, self.y

    def update(self):
        # self.x -= self.velocity * Variables.dt
        self.x, self.y = self.objectdirection(self.direction)
        if self.x < -32 or self.x > CONST.WIDTH or self.y < -10 or self.y > CONST.PAHEIGHT: Graphicgroups.debris.pop(Graphicgroups.debris.index(self))
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

    def spawn(x,y,mindir,maxdir,minvel,maxvel,image,origin,numdebris=random.randint(1,3)):
        for _ in range(numdebris):
            Graphicgroups.debris.append(Debris(
                x=x,
                y=y,
                direction=random.randint(mindir,maxdir),
                velocity=random.randint(minvel,maxvel),
                image=image,
                origin=origin
            ))



#region THINGS




#region Star Wars Scroller
class StarWarsScroll:
    def __init__(self,image,x,y,width,height,speed,ix,iy,offset,fade):
        self.offset = offset
        self.fade = fade
        self.x, self.y, self.w, self.h = x, y, width, height
        self.ix, self.iy = ix, iy
        self.speed = speed
        self.image = image
        self.image_rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image,(self.w, self.image_rect.h))
        self.segment = pygame.Surface((self.w, self.h)).convert_alpha()

    def update(self):
        self.iy -= self.speed * Variables.delta_time

    def draw(self,screen):
        self.segment.fill((0,0,0,0))
        self.segment.set_alpha(255-(self.offset*self.fade))
        self.segment.blit(self.image,(self.ix, self.iy+(self.h*self.offset), self.w, self.h))
        screen.blit(self.segment,(self.x,self.y,self.w,self.h))



#region Health Bar
class Healthbar:        # Work In Progress
    def __init__(self,maxhealth,health,barheight,rect):
        self.maxhealth = maxhealth
        self.health = health
        self.healthbar_height = barheight
        self.rect = rect
        self.healthbar = pygame.Surface((self.rect.width,self.healthbar_height)).convert_alpha()
        self.healthbar_Color = (255-(255/self.maxhealth*self.health),255/self.maxhealth*self.health,0)

    def update(self):
        self.healthdisplay = self.rect.width/self.maxhealth*self.health
        self.healthbar_Color = (255-(255/self.maxhealth*self.health),255/self.maxhealth*self.health,0)
        self.curhealth_grapic = CONST.UI_FONT.render(str(self.health), True, 'yellow')

    def draw(self,screen):
        screen.blit(self.healthbar, (self.rect.left,self.rect.top-5,self.rect.width,10))
        self.healthbar.fill((0,0,0,0))
        try: pygame.draw.rect(self.healthbar,self.healthbar_Color,(0,0,self.healthdisplay,self.healthbar_height))
        except: pass



#region Damage Numbers
class Damagenum:
    def __init__(self,x,xvel,y,damage):
        self.x, self.y, self.orgy = x, y-32, y-32
        self.xvelocity, self.yvelocity = xvel, 50
        damage_font = pygame.font.SysFont(CONST.DEFAULT_FONT_NAME, Settings.damage_num_font_size)
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



#region Timers
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
        self.bosskana_timer, self.bosskana_frequency = 0, 5
        self.scenery_timer, self.scenery_thresh = 0, 0

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
            # selection = random.randint(0,Variables.levels[Variables.level]-1)
            selection = random.randint(0,len(Variables.gamekana[Variables.level])-1)
            Graphicgroups.incorrectkanas.append(Kana(
                x = CONST.WIDTH+CONST.off_screen_offset, 
                y = random.randrange(300,CONST.PAHEIGHT-128,),
                kana = selection,
                group = Graphicgroups.incorrectkanas,
                fade = random.randint(CONST.min_kana_alpha,256),
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
                surface = CONST.SURF_BOSS[CONST.ARRAY_BOSSES[Variables.level]["imgindx"]].images[0],
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
            # selection = random.randint(0,Variables.levels[Variables.level]-1)
            selection = random.randint(0,len(Variables.gamekana[Variables.level])-1)
            if selection != Variables.kananum:
                if int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3]) < Settings.num_to_shoot_new_kana+1:
                    Graphicgroups.incorrectkanas.append(Kana(CONST.WIDTH+CONST.off_screen_offset, random.randrange(128,CONST.PAHEIGHT-200,),selection,Graphicgroups.incorrectkanas,random.randint(CONST.min_kana_alpha,256),random.randint(-Settings.kana_rotate_rate,Settings.kana_rotate_rate),"Shoot",(255,kanakill,kanakill),True))
                else:
                    Graphicgroups.incorrectkanas.append(Kana(
                        x=CONST.WIDTH+CONST.off_screen_offset, 
                        y=random.randrange(128,CONST.PAHEIGHT-200,),
                        kana=selection,
                        group=Graphicgroups.incorrectkanas,
                        fade=random.randint(CONST.min_kana_alpha,256),
                        rotate=random.randint(-Settings.kana_rotate_rate,Settings.kana_rotate_rate)))
                self.incorrectkana_timer = 0
                self.incorrectkana_thresh = random.randint(Settings.minimum_incorrect_kana_frequency,Settings.maximum_incorrect_kana_frequency)/10
        self.incorrectkana_timer += 1 * Variables.delta_time

    def correctkana(self, kanakill):
        if kanakill >= 255: kanakill = 255
        if self.correctkana_timer > self.correctkana_thresh:
            Variables.generatedcorrectkanacounter += 3
            if int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3]) < Settings.num_to_shoot_new_kana+1:
                Graphicgroups.correctkanas.append(Kana(
                    x=CONST.WIDTH+CONST.off_screen_offset, 
                    y=random.randrange(128,CONST.PAHEIGHT-200,),
                    kana=Variables.kananum,
                    group=Graphicgroups.correctkanas,
                    fade=random.randint(CONST.min_kana_alpha,256),
                    rotate=random.randint(-Settings.kana_rotate_rate,Settings.kana_rotate_rate),
                    newmessage="Collect",
                    color=(kanakill,255,kanakill),
                    new=True))
            else:
                Graphicgroups.correctkanas.append(Kana(
                    x=CONST.WIDTH+CONST.off_screen_offset, 
                    y=random.randrange(128,CONST.PAHEIGHT-200,),
                    kana=Variables.kananum,
                    group=Graphicgroups.correctkanas,
                    fade=random.randint(CONST.min_kana_alpha,256),
                    rotate=random.randint(-Settings.kana_rotate_rate,Settings.kana_rotate_rate)))
            self.correctkana_timer = 0
            self.correctkana_thresh = random.randint(Settings.minimum_correct_kana_frequency,Settings.maximum_correct_kana_frequency)/10
            self.correct_kana_lost_sound_play = True
        self.correctkana_timer += 1 * Variables.delta_time

    def bosskana(self, frequency):
        # BossMode Kana Timer
        if self.bosskana_timer > self.bosskana_frequency:
            #region Spawn boss mode kana drop
            segment = 15                                                                                # Divide whole screen into sections
            columns = [1,2,3,4,5,6,7,8]                                                                 # Create an array of indexes for those sections
            random.shuffle(columns)                                                                     # Shuffle those indexes around randomly
            Graphicgroups.bossmodecorrectkana.append(
                BossModeKana(
                    x=100 + (columns[0] * (CONST.WIDTH/segment)),                                  # Spawn Correct Kana at the first index of the shuffled array
                    y=-20,                                                                             # Spawn Correct kana off screen
                    kana=Variables.kananum,
                    group=Graphicgroups.bossmodecorrectkana,
                    fade=random.randint(CONST.min_kana_alpha,256),
                    rotate=random.randint(-Settings.kana_rotate_rate,Settings.kana_rotate_rate))
            )
            columns.pop(0)                                                                              # Remove first indes from shuffled array so not to re-use it
            for f in columns:
                # selection = random.randint(0,Variables.levels[Variables.level]-1)
                selection = random.randint(0,len(Variables.gamekana[Variables.level])-1)
                if selection != Variables.kananum:
                    Graphicgroups.bossmodeincorrectkana.append(
                        BossModeKana(
                            x=100 + (f * CONST.WIDTH/segment), 
                            y=-20,
                            kana=selection,
                            group=Graphicgroups.bossmodeincorrectkana,
                            fade=random.randint(CONST.min_kana_alpha,256),
                            rotate=random.randint(-Settings.kana_rotate_rate,Settings.kana_rotate_rate))
                    )
            #endregion Spawn boss mode kana drop
            self.bosskana_timer = 0
            self.bosskana_frequency = frequency
        self.bosskana_timer += 1 * Variables.delta_time

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
                CONST.ARRAY_POWERUP[powerup_type]["xvel"],
                CONST.ARRAY_POWERUP[powerup_type]["surfindx"],
                CONST.ARRAY_POWERUP[powerup_type]["pueffect"],
                )
            self.powerup_timer = 0
            self.powerup_thresh = random.randint(30,40)
        self.powerup_timer += 1 * Variables.delta_time

    def weaponupgrade(self):
        if self.powerup_timer >= self.powerup_thresh:
            powerup_type = 3
            AnimatedPowerUp.spawn(
                CONST.ARRAY_POWERUP[powerup_type]["xvel"],
                CONST.ARRAY_POWERUP[powerup_type]["surfindx"],
                CONST.ARRAY_POWERUP[powerup_type]["pueffect"],
                )
            self.powerup_timer = 0
            self.powerup_thresh = random.randint(110,130)
        self.powerup_timer += 1 * Variables.delta_time

    def bridge(self, frequency):
        if self.bridge_timer > frequency:
            Bridge.spawn()
            self.bridge_timer = 0
            self.bridge_thresh = frequency
        self.bridge_timer += 1 * Variables.delta_time

    def wallofdeath(self):
        if self.WoD_timer >= self.WoD_thresh:
            WallOfDeath.spawn(CONST.WIDTH,0)
            self.WoD_timer = 0
            self.WoD_thresh = random.randint(30,60)
        self.WoD_timer += 1 * Variables.delta_time

    def scenery(self,frequency=.5):
        if self.scenery_timer > frequency:
            BorderScenery(Variables.scenerytype).picknext()
            self.scenery_timer = 0
            self.scenery_thresh = frequency
        self.scenery_timer += 1 * Variables.delta_time



#region Menu Buttons
class Buttons:
    def __init__(self):
        self.startbuttonsoundplayed = False



    #region Start
    def start(self,screen,x=0,y=200):
        self.start_button = CONST.SURF_START_BUTTON[0]                                  # Select Start button image from array
        self.start_button = pygame.transform.scale(self.start_button,(256,128))             # Scale the image to x,y dimensions
        self.start_button_rect = self.start_button.get_rect(center=(CONST.WCENTER+x,CONST.HCENTER+y))                   # Get rect dimensions from the x,y arguments to center graphic
        if self.start_button_rect.collidepoint(pygame.mouse.get_pos()):                     # check to see if the mouse position is in the rect dimensions
            self.start_button = CONST.SURF_START_BUTTON[1]                              # replace start button image with another image from the array
            self.start_button = pygame.transform.scale(self.start_button,(256,128))         # Scale the image to x,y dimensions
            if self.startbuttonsoundplayed == False:                                        # Check to see if the sound has played
                pygame.mixer.Sound.play(CONST.SOUND_CORRECT_KANA_LOSING)                # Play sound when mouse enters rect dimensions
                self.startbuttonsoundplayed = True                                          # Set flag that sound has played already
        else: self.startbuttonsoundplayed = False                                           # Else reset the sound played flag to False
        screen.blit(self.start_button, self.start_button_rect)                              # Finally draw the image to the screen at the rect position




    #region Game Mode
    def gamemode(self,screen,x=500,y=0):
        self.game_mode_button = CONST.SURF_KANA_BUTTON[0]                                  # Select Start button image from array
        # Toggle
        if Variables.gamemode == 0:
            self.game_mode_button = CONST.SURF_KANA_BUTTON[0]
        else:
            self.game_mode_button = CONST.SURF_KANA_BUTTON[1]
        self.game_mode_button = pygame.transform.scale(self.game_mode_button,(256,256))             # Scale the image to x,y dimensions
        self.game_mode_button_rect = self.game_mode_button.get_rect(center=(CONST.WCENTER+x,CONST.HCENTER+y))                   # Get rect dimensions from the x,y arguments to center graphic
        screen.blit(self.game_mode_button, self.game_mode_button_rect)




    #region Starting Level
    def startinglevel(self,screen,x=-500,y=0):
        self.startinglevel_graphic = CONST.SURF_STARTING_LEVEL
        self.startinglevel_graphic = pygame.transform.scale(self.startinglevel_graphic,(256,256))           # Scale the image to x,y dimensions
        self.startinglevel_rect = self.startinglevel_graphic.get_rect(center=(CONST.WCENTER+x,CONST.HCENTER+y))                         # Get rect dimensions from the x,y arguments to center graphic
        screen.blit(self.startinglevel_graphic, self.startinglevel_rect)                                    # Finally draw the image to the screen at the rect position
        num_text = CONST.STARTING_LEVEL_FONT.render(str(Variables.level+1), True, 'white')
        num_text_shadow = CONST.STARTING_LEVEL_FONT.render(str(Variables.level+1), True, 'black')
        num_text_rect = num_text.get_rect(center=(CONST.WCENTER+x,CONST.HCENTER+y))                                                     # Get rect dimensions from the x,y arguments to center graphic
        num_text_shadow_rect = num_text_shadow.get_rect(center=(CONST.WCENTER+x+5,CONST.HCENTER+y+5))                                   # Get rect dimensions from the x,y arguments to center graphic
        num_text_shadow.set_alpha(128)
        screen.blit(num_text_shadow,num_text_shadow_rect)
        screen.blit(num_text,num_text_rect)



#region ACHIEVEMENTS
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



#region INSTANCING
player = Ship(0,CONST.HCENTER)              # Instance player to center left of screen
timer = Timers()                                # Create a timer object
menu_buttons = Buttons()                        # Create a button object
achievements = Achievements()                   # Achievements system
#endregion Instancing