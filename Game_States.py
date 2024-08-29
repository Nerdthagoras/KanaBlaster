from sys import exit

import Functions
import Game_Objects
import Constants
import Graphicgroups
import Settings
import os
import Variables
import math
import random
import time
import pygame

class IntroState:
    def __init__(self):
        self.introlength = 0
        self.done = False
        self.boss = False
        self.timer = 0
        self.lt = time.time()

    def manifest(self):
        Game_Objects.timer.stars(frequency=Settings.star_frequency,velocity=0)

    def update(self):
        Variables.STATE = "Intro"
        Graphicgroups.starfield_group.update(Game_Objects.player) # Update Stars
        if time.time() - self.lt >= self.introlength: self.done = True # End intro after 'introlength' seconds

    def draw(self,screen):
        # DEBUG
        if Variables.debugwindow: Debug.draw(Constants.debug_locationx,Constants.debug_locationy)

    def collision(self):
        pass

    def handle_events(self, events):
        pass

class MenuState:
    def __init__(self):
        self.done = False
        self.boss = False
        self.enemy_wait_timer = 3
        self.startbuttonsoundplayed = False
        from Game_Objects import AnimCenterWarning
        Graphicgroups.animcenterwarning.append(AnimCenterWarning("",Constants.spaceship_surfs,Variables.shiptype,4,fade=False))
        for _ in range(100): Graphicgroups.starfield_group.add(Game_Objects.Star(0,random.randrange(0,Constants.WIDTH+1000))) # Preload screen full of stars

    def manifest(self):
        Game_Objects.timer.stars(frequency=Settings.star_frequency,velocity=0)      # Stars Timer
        Game_Objects.timer.allkana(frequency=1)                                     # All Kana Timer
        Game_Objects.timer.biglaser(enemywaittimer=self.enemy_wait_timer)           # Big Laser Timer
        Game_Objects.timer.enemy(enemywaittimer=self.enemy_wait_timer)              # Enemy Timer

    def update(self):
        Variables.STATE = "Menu"
        pygame.mouse.set_visible(True)
        Variables.maxshiptype = int(len(Constants.spaceship_surfs)*Functions.getmaxship())

        for junk in Graphicgroups.spacejunk: junk.update(Game_Objects.player)                       # RANDOM JUNK
        Graphicgroups.starfield_group.update(Game_Objects.player)                                   # STARS
        for kana in Graphicgroups.kanas:  kana.update(Game_Objects.player)                          # Kana
        for warning in Graphicgroups.warnings: warning.update()                                     # Warning for BIG LASER
        for biglaser in Graphicgroups.biglasers: biglaser.update()                                  # BIG LASER
        for enemy in Graphicgroups.enemies: enemy.update();enemy.shoot(Game_Objects.player)         # Enemies
        for epew in Graphicgroups.enemyprojectiles: epew.update()                                   # Enemy Projectiles
        for wod in Graphicgroups.wallsegments: wod.update()                                         # Wall of Death
        for centerwarn in Graphicgroups.animcenterwarning: centerwarn.update()                      # Center Warning

    def draw(self,screen):
        # Must be in order of Top/Bottom = Background/Foreground
        screen.fill(('black'))                                                                      # Refresh screen

        for junk in Graphicgroups.spacejunk: junk.draw(screen)                                      # RANDOM JUNK
        Graphicgroups.starfield_group.draw(screen)                                                  # STARS
        for kana in Graphicgroups.kanas: kana.draw(screen)                                          # Kana
        #region Bottom KANA LIST                                                                    # Bottom Kana List
        Graphicgroups.kanalist.clear()
        for kana in range(int(Variables.levels[Variables.level])): Graphicgroups.kanalist.append(Variables.commasep[kana])
        for kana in range(int(Variables.levels[Variables.level])):
            kanakill = int(Variables.commasep[kana][3])*(255/Settings.num_to_shoot_new_kana)
            if kanakill >= 255: kanakill = 255
            kanalistthing = Constants.ui_font.render(Graphicgroups.kanalist[kana][Variables.gamemode], True, (kanakill,255,kanakill))
            screen.blit(kanalistthing,(25+(27*kana),Constants.HEIGHT-30))
        #endregion
        for epew in Graphicgroups.enemyprojectiles: epew.draw(screen)                               # Enemy Projectiles
        for enemy in Graphicgroups.enemies: enemy.draw(screen,Game_Objects.player)                  # Enemies
        for warning in Graphicgroups.warnings: warning.draw(screen)                                 # Warning for BIG LASER
        for biglaser in Graphicgroups.biglasers: biglaser.draw(screen)                              # BIG LASER
        for wod in Graphicgroups.wallsegments: wod.draw(screen)                                     # Wall of Death
        for centerwarn in Graphicgroups.animcenterwarning: centerwarn.draw()                        # Center Warning
        
        if Variables.debugwindow: Debug.draw(Constants.debug_locationx,Constants.debug_locationy)   # DEBUG

        #region Game Title
        TITLE_text = Constants.GAME_OVER_font.render('KANA BLASTER', True, 'white')
        screen.blit(TITLE_text, (10, Constants.HEIGHT/7))
        TITLE_shadow_text = Constants.GAME_OVER_font.render('KANA BLASTER', True, 'white')
        TITLE_shadow_text.set_alpha(100)
        offset = 8
        screen.blit(TITLE_shadow_text, (10+offset, Constants.HEIGHT/7+offset))
        #endregion Game Title

        #region BUTTONS                                                                             # BUTTONS
        # Starting Level
        self.level_number_location = (10, 10, 200, 40)
        self.level_number = pygame.Rect(self.level_number_location)
        level_text = Constants.ui_font.render('Level: ', True, 'white')
        pygame.draw.rect(screen, 'white', self.level_number, 2)
        screen.blit(level_text, (self.level_number_location[0]+10,self.level_number_location[1]+10))
        num_text = Constants.ui_font.render(str(Variables.level), True, 'white')
        screen.blit(num_text,(120, 20))

        # Game Mode Button
        self.game_mode_location = (10, 50, 200, 40)
        self.game_mode = pygame.Rect(self.game_mode_location)
        pygame.draw.rect(screen, 'white', self.game_mode, 2)
        if Variables.gamemode == 0:
            sound_state = Constants.ui_font.render('Hiragana', True, 'white')
            screen.blit(sound_state, (75, 60))
        else:
            sound_state = Constants.ui_font.render('Katakana', True, 'white')
            screen.blit(sound_state, (75, 60))

        # Ship Type
        self.shiptype_number_location = (10, 90, 200, 40)
        self.shiptype_number = pygame.Rect(self.shiptype_number_location)
        shiptype_text = Constants.ui_font.render('Ship: ', True, 'white')
        pygame.draw.rect(screen, 'white', self.shiptype_number, 2)
        screen.blit(shiptype_text, (self.shiptype_number_location[0]+10,self.shiptype_number_location[1]+10))
        num_text = Constants.ui_font.render(str(Variables.shiptype), True, 'white')
        screen.blit(num_text,(120, 100))

        # Start Button
        self.start_button_location = (Constants.WIDTH // 2-75, Constants.HEIGHT //2+150, 150, 70)
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
        #endregion BUTTONS

    def collision(self):
        pass

    def handle_events(self, events):
        for event in events:
            #Click the X to close window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Mouse Events
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Game Mode
                if self.game_mode.collidepoint(event.pos):
                    if Variables.gamemode == 0:
                        Variables.gamemode = 1
                    else:
                        Variables.gamemode = 0

                # start level
                if self.level_number.collidepoint(event.pos) and event.button == 1 or self.level_number.collidepoint(event.pos) and event.button == 4:
                    if Variables.level >= 9:
                        Variables.level = 0
                    else:
                        Variables.level += 1
                elif self.level_number.collidepoint(event.pos) and event.button == 3 or self.level_number.collidepoint(event.pos) and event.button == 5:
                    if Variables.level <= 0:
                        Variables.level = 9
                    else:
                        Variables.level -= 1
                elif self.level_number.collidepoint(event.pos) and event.button == 2: Variables.level = 0

                # Select Ship
                if self.shiptype_number.collidepoint(event.pos) and event.button == 1 or self.shiptype_number.collidepoint(event.pos) and event.button == 4:
                    if Variables.shiptype >= Variables.maxshiptype or Variables.shiptype >= len(Constants.spaceship_surfs)-1:
                        Variables.shiptype = 0
                    else:
                        Variables.shiptype +=1
                    from Game_Objects import AnimCenterWarning
                    Graphicgroups.animcenterwarning.clear()
                    Graphicgroups.animcenterwarning.append(AnimCenterWarning("",Constants.spaceship_surfs,Variables.shiptype,4,False))
                elif self.shiptype_number.collidepoint(event.pos) and event.button == 3 or self.shiptype_number.collidepoint(event.pos) and event.button == 5:
                    if Variables.shiptype <= 0:
                        if Variables.maxshiptype < len(Constants.spaceship_surfs)-1:
                            Variables.shiptype = Variables.maxshiptype
                        else:
                            Variables.shiptype = len(Constants.spaceship_surfs)-1
                    else:
                        Variables.shiptype -= 1
                    from Game_Objects import AnimCenterWarning
                    Graphicgroups.animcenterwarning.clear()
                    Graphicgroups.animcenterwarning.append(AnimCenterWarning("",Constants.spaceship_surfs,Variables.shiptype,4,False))
                elif self.shiptype_number.collidepoint(event.pos) and event.button == 2: 
                    Variables.shiptype = 0
                    from Game_Objects import AnimCenterWarning
                    Graphicgroups.animcenterwarning.clear()
                    Graphicgroups.animcenterwarning.append(AnimCenterWarning("",Constants.spaceship_surfs,Variables.shiptype,4,False))

                #start
                if self.start_button.collidepoint(event.pos):
                    Functions.reset_game()
                    game_state.enemy_wait_timer = 10
                    gameover_state.done = False
                    game_state.done = False
                    boss_state.done = False
                    Variables.BOSSSTATE = False
                    Variables.GAMESTATE = False
                    self.done = True

            # Key Events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_SPACE:
                    Functions.reset_game()
                    game_state.enemy_wait_timer = 10
                    gameover_state.done = False
                    game_state.done = False
                    boss_state.done = False
                    self.done = True
                if event.key == ord('h'):
                    if Variables.hitboxshow == True:
                        Variables.hitboxshow = False
                        Variables.debugwindow = False
                    else:
                        Variables.hitboxshow = True
                        Variables.debugwindow = True
                if event.key == ord('i'): 
                    for h in range(int(Constants.HEIGHT/32)):
                        Game_Objects.WallOfDeath.spawn(Constants.WIDTH,h*32)
                if event.key == ord('f'): pygame.display.toggle_fullscreen()
                if event.key == ord('e'): Game_Objects.Enemies.spawn()
                if event.key == ord('r'): Game_Objects.BigLaserWarning.spawn(Game_Objects.player)
                if event.key == ord('0'):
                    try: os.remove('data/userkana.csv')
                    except: pass

class GameState:
    def __init__(self):
        self.done = False
        self.boss = Variables.GAMESTATE
        self.bgfade_timer = time.time()
        self.enemy_wait_timer = 10
        self.prev_level = Variables.level
        self.extralife = Settings.ship_extra_life_increment

    def manifest(self):
        # Kanakill Variable
        kanakill = int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3])*(255/Settings.num_to_shoot_new_kana)

        Game_Objects.timer.stars(frequency=Settings.star_frequency,velocity=0)              # Stars Timer
        Game_Objects.timer.incorrectkana(kanakill=kanakill)                                 # Incorrect Kana Timer
        Game_Objects.timer.correctkana(kanakill=kanakill)                                   # Correct Kana Timer
        Game_Objects.timer.biglaser(enemywaittimer=self.enemy_wait_timer)                   # Big Laser Timer
        Game_Objects.timer.enemy(enemywaittimer=self.enemy_wait_timer)                      # Enemy Timer
        Game_Objects.timer.planet()                                                         # PLANET Timer
        Game_Objects.timer.junk()                                                           # JUNK Timer
        Game_Objects.timer.powerup()                                                        # POWERUP Timer
        Game_Objects.timer.bridge(frequency=30)                                             # Bridge Timer

    def gamefadeouttoboss(self):
        #region Fade out music and transition to Boss
        if Variables.TRANSITION == True: # Start the Music Fade
            if Variables.musicvolume <= 0:
                Variables.BOSSSTATE = False
                Variables.GAMESTATE = True
                Variables.bossexist = False
                boss_state.boss_message_displayed = False
                boss_state.get_ready_timer = Settings.get_ready_timer_max

                # Reset Timers for Boss Phase
                Game_Objects.timer.WoD_timer = time.time()
                Game_Objects.timer.incorrectkana_timer = time.time()
                Game_Objects.timer.junk_timer = time.time()
                Game_Objects.timer.correctkana_timer = time.time()
                Game_Objects.timer.biglaser_timer = time.time()
                Game_Objects.timer.enemy_timer = time.time()
                Game_Objects.timer.powerup_timer = time.time()
                Game_Objects.timer.bridge_timer = time.time()
                Game_Objects.timer.boss_message_timer = time.time()
                Game_Objects.timer.bonus_timer = time.time()
                Game_Objects.timer.boss_timer = time.time()
                Game_Objects.timer.boss_message_displayed = False

            Variables.musicvolume -= 0.05 * Variables.dt
        #endregion Fade out music and transition to Boss

    def warningmessages(self):
        if Variables.level == Settings.enemy_start_level and self.prev_level < Settings.enemy_start_level:
            Game_Objects.CenterWarning.spawn('Enemies Active',Constants.enemy_spritesheet_surfs[0].images[0],3)
            self.enemy_wait_timer = 3
            self.prev_level = Settings.enemy_start_level
        if Variables.level == Settings.biglaser_start_level and self.prev_level < Settings.biglaser_start_level:
            Game_Objects.CenterWarning.spawn('Big Laser Active',Constants.biglaser_surfs[0].images[0])
            self.enemy_wait_timer = 3
            self.prev_level = Settings.biglaser_start_level

    def lives(self):
        #region Extra Life
        if Variables.score >= self.extralife:
            Game_Objects.AnimatedPowerUp.spawn(
                Constants.powerup_array[0]["xvel"],
                Constants.powerup_array[0]["surfindx"],
                Constants.powerup_array[0]["pueffect"],
                )
            self.extralife += Settings.ship_extra_life_increment
        #endregion

        #region You lost all of your lives
        if Variables.lives <= 0:
            Functions.write_csv('data/userkana.csv',Variables.commasep) # Write your progress to a CSV file
            self.done = True
        #endregion

    def update(self):
        Variables.STATE = "Game"
        self.boss = Variables.GAMESTATE
        self.gamefadeouttoboss()
        self.warningmessages()
        self.lives()

        if self.enemy_wait_timer >= 0: self.enemy_wait_timer -= 1 * Variables.dt        #Stop enemies from showing up right at the start

        Graphicgroups.planet_group.update(Game_Objects.player)                          # PLANETS
        Graphicgroups.starfield_group.update(Game_Objects.player)                       # STARS
        Graphicgroups.bridge_group.update(Game_Objects.player)                          # BRIDGE WIPE
        Graphicgroups.tip_group.update()                                                # Tip Ticker
        Graphicgroups.debug_window.update()                                             # Debug Window
        Graphicgroups.explosion_group.update()                                          # EXPLOSION
        for bullet in Graphicgroups.bullets: bullet.update()                            # BULLETS
        for biglaser in Graphicgroups.biglasers: biglaser.update()                      # BIG LASER
        for junk in Graphicgroups.spacejunk: junk.update()                              # RANDOM JUNK
        for cutoff in Graphicgroups.cuttoffline: cutoff.update(Game_Objects.player)     # CUTOFF LINE
        for kana in Graphicgroups.correctkanas: kana.update(Game_Objects.player)        # Correct Kanas
        for kana in Graphicgroups.kanas: kana.update(Game_Objects.player)               # Incorrect kanas
        for warning in Graphicgroups.warnings: warning.update()                         # Big Laser Warning
        for epew in Graphicgroups.enemyprojectiles: epew.update()                       # Enemy Projectiles
        for enemy in Graphicgroups.enemies: enemy.update()                              # ENEMIES
        for wod in Graphicgroups.wallsegments: wod.update()                             # Wall of Death
        for brick in Graphicgroups.bricks: brick.update()                               # Brick debris
        for bits in Graphicgroups.debris: bits.update()                                 # Debris
        for powerup in Graphicgroups.animatedpowerup:                                   # Powerups
            powerup.update()
            powerup.effect(powerup.pueffect,Game_Objects.player)
        for centerwarn in Graphicgroups.centerwarning: centerwarn.update()              # UI
        Game_Objects.player.update()                                                    # Player

    def draw(self,screen):
        pygame.mouse.set_visible(False)
        # region SCREEN
        if time.time() - self.bgfade_timer >= 0.001:
            if Variables.RGB[0] > 10: Variables.RGB[0] -= 500 * Variables.dt
            else: Variables.RGB[0] = 0
            if Variables.RGB[1] > 10: Variables.RGB[1] -= 500 * Variables.dt
            else: Variables.RGB[1] = 0
            if Variables.RGB[2] > 10: Variables.RGB[2] -= 500 * Variables.dt
            else: Variables.RGB[2] = 0
            self.bgfade_timer = time.time()
        try: screen.fill((Variables.RGB[0],Variables.RGB[1],Variables.RGB[2]))
        except: pass
        #endregion

        #region KANA LIST
        for f in range(int(Variables.levels[Variables.level])): Graphicgroups.kanalist.append(Variables.commasep[f])
        for f in range(int(Variables.levels[Variables.level])):
            if Variables.gamemode == 0: kanalistthing = Constants.ui_font.render(Graphicgroups.kanalist[f][0], True, (20,20,20))
            else: kanalistthing = Constants.ui_font.render(Graphicgroups.kanalist[f][1], True, (20,20,20))
            screen.blit(kanalistthing,(25+(27*f),Constants.HEIGHT-30))
        #endregion

        Graphicgroups.planet_group.draw(screen)                                         # PLANETS
        for junk in Graphicgroups.spacejunk: junk.draw(screen)                          # RANDOM JUNK
        Graphicgroups.starfield_group.draw(screen)                                      # STARS
        for warning in Graphicgroups.warnings: warning.draw(screen)                     # WARNING for BIG LASER
        for bullet in Graphicgroups.bullets: bullet.draw(screen)                        # BULLETS
        for cutoff in Graphicgroups.cuttoffline: cutoff.draw(screen)                    # CUTOFF LINE
        for epew in Graphicgroups.enemyprojectiles: epew.draw(screen)                   # ENEMY PEW
        for bits in Graphicgroups.debris: bits.draw(screen)                             # Bits debris
        for enemy in Graphicgroups.enemies: enemy.draw(screen,Game_Objects.player)      # ENEMIES
        for kana in Graphicgroups.correctkanas: kana.draw(screen)                       # CORRECT KANA
        for kana in Graphicgroups.kanas: kana.draw(screen)                              # WRONG KANA
        Game_Objects.player.draw(screen)                                                # PLAYER
        for powerup in Graphicgroups.animatedpowerup: powerup.draw(screen)              # Powerup
        for biglaser in Graphicgroups.biglasers: biglaser.draw(screen)                  # BIG LASER
        for wod in Graphicgroups.wallsegments: wod.draw(screen)                         # Wall of Death
        for brick in Graphicgroups.bricks: brick.draw(screen)                           # Brick debirs
        for shield in Graphicgroups.shields: shield.draw(screen)                        # Shields
        for damagenumber in Graphicgroups.damagenumbers: damagenumber.draw(screen)      # Damage values 
        Graphicgroups.explosion_group.draw(screen)                                      # EXPLOSION
        Functions.question_text(screen)                                                 # QUESTION TEXT
        Functions.uitext(screen)                                                        # UI TEXT
        Graphicgroups.bridge_group.draw(screen)                                         # BRIDGE WIPE
        Graphicgroups.tip_group.draw(screen)                                            # Tip Ticker
        for centerwarn in Graphicgroups.centerwarning: centerwarn.draw()                # Center Warning Text

        if Variables.debugwindow: Debug.draw(Constants.debug_locationx,Constants.debug_locationy)   # DEBUG

    def collision(self):
        # If it is a projectile, then it will hit something, 
        # if it is not a projectile then the ship is considered the projectile
        # Space Junk will be treated like a projectile because it persists after collision

        #region Player Projectiles
        for bullet in Graphicgroups.bullets:

            # if player's bullet hits powerup
            for powerup in Graphicgroups.animatedpowerup:
                if powerup.collide(bullet.rect):
                    pygame.mixer.Sound.play(Constants.badhit)
                    explosion = Game_Objects.Explosion(powerup.x, powerup.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                    try:
                        persist = Constants.pew_array[Variables.pewtype]["persist"]
                        if not persist:
                            Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                    except: pass
                    Graphicgroups.animatedpowerup.pop(Graphicgroups.animatedpowerup.index(powerup))

            #if player's bullet hits Wall of Death
            for wod in Graphicgroups.wallsegments:
                if wod.collide(bullet.rect):
                    Graphicgroups.wallsegments.pop(Graphicgroups.wallsegments.index(wod))
                    try:
                        persist = Constants.pew_array[Variables.pewtype]["persist"]
                        if not persist:
                            Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                    except: pass
                    Game_Objects.Debris.spawn(wod.x,wod.y,math.radians(random.randint(-10,10)),random.randint(100,300),Constants.brick_surf,0)
                    pygame.mixer.Sound.play(Constants.brickbreak_sound)
                    explosion = Game_Objects.Explosion(wod.x, wod.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                    Variables.score += 1

            # if player's bullet hits CORRECT Kana
            for ckana in Graphicgroups.correctkanas:    
                if ckana.collide(bullet.rect):
                    Variables.RGB[0] = 128
                    pygame.mixer.Sound.play(Constants.badhit)
                    kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', ckana.kanasound + '.wav'))
                    pygame.mixer.Sound.play(kana_sound)
                    if ckana.x >= 2*Constants.WIDTH // 3:
                        Variables.score -= 3
                    elif ckana.x > Constants.WIDTH // 3 and ckana.x < 2*Constants.WIDTH // 3:
                        Variables.score -= 2
                    else:
                        Variables.score -= 1
                    explosion = Game_Objects.Explosion(ckana.x, ckana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                    try:
                        persist = Constants.pew_array[Variables.pewtype]["persist"]
                        if not persist:
                            Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                    except: pass
                    Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(ckana))
                    # kanaint = int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3])
                    # if kanaint <= num_to_shoot_new_kana: kanaint += 1
                    #Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3] = kanaint

            # if player's bullet hits WRONG kana
            for kana in Graphicgroups.kanas:
                if kana.collide(bullet.rect):
                    Variables.RGB[1] = 64
                    pygame.mixer.Sound.play(Constants.goodhit)
                    Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                    try:
                        persist = Constants.pew_array[Variables.pewtype]["persist"]
                        if not persist:
                            Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                    except: pass
                    kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', kana.kanasound + '.wav'))
                    pygame.mixer.Sound.play(kana_sound)
                    if kana.x >= 2*Constants.WIDTH // 3:
                        Variables.score += 3
                    elif kana.x > Constants.WIDTH // 3 and kana.x < 2*Constants.WIDTH // 3:
                        Variables.score += 2
                    else:
                        Variables.score += 1
                    maxexplode = random.randint(0,len(Constants.explosion_surfs)-1)
                    explosion = Game_Objects.Explosion(x=kana.x, y=kana.y,spritearray=Constants.explosion_surfs,scale=0.5,repeat=False,explosiontype=maxexplode)
                    Graphicgroups.explosion_group.add(explosion)

            # if player's bullet hits Enemy
            for enemy in Graphicgroups.enemies:
                if enemy.collide(bullet.rect):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    damage = 1 + random.randint(int(Game_Objects.player.laserpower/5),Game_Objects.player.laserpower)
                    enemy.health -= damage
                    Game_Objects.Debris.spawn(enemy.enemy_rect.centerx,enemy.y,math.radians(random.randint(80,280)),random.randint(50,200),Constants.debris_surf,Graphicgroups.enemies.index(enemy))
                    Game_Objects.Damagenum.spawn(enemy.enemy_rect.centerx,0,enemy.y,damage)
                    enemy.knockbackx = Settings.enemy_max_knockbackx
                    enemy.knockbacky = enemy.collide(bullet.rect)
                    if enemy.health <= 0:
                        Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                        explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.explosion_surfs,0.5,False)
                        Graphicgroups.explosion_group.add(explosion)
                        Variables.score += 1
                        powerup_chance = random.randint(0,Settings.enemy_powerup_freq)
                        if powerup_chance == 0:
                            Game_Objects.AnimatedPowerUp.spawn(
                                Constants.powerup_array[3]["xvel"],
                                Constants.powerup_array[3]["surfindx"],
                                Constants.powerup_array[3]["pueffect"],
                            )

                    try:
                        persist = Constants.pew_array[Variables.pewtype]["persist"]
                        if not persist:
                            Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                    except: pass

            # if player's bullet hits ship debirs
            for shipdeb in Graphicgroups.debris:
                if shipdeb.collide(bullet.rect):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    explosion = Game_Objects.Explosion(shipdeb.x, shipdeb.y,Constants.explosion_surfs,0.2,False)
                    Graphicgroups.explosion_group.add(explosion)
                    try:
                        persist = Constants.pew_array[Variables.pewtype]["persist"]
                        if not persist:
                            Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                    except: pass
                    Graphicgroups.debris.pop(Graphicgroups.debris.index(shipdeb))

        #endregion
        
        #region Enemy Projectiles
        for epew in Graphicgroups.enemyprojectiles:
            # if hit Player
            if Variables.shipcollision == True:
                if epew.collide(Game_Objects.player.spaceship_rect):
                    Graphicgroups.enemyprojectiles.pop(Graphicgroups.enemyprojectiles.index(epew))
                    explosion = Game_Objects.Explosion(epew.x, epew.y,Constants.explosion_surfs,0.5,False)
                    ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                    Graphicgroups.explosion_group.add(explosion)
                    Graphicgroups.explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(Constants.shiphit)
                    Game_Objects.player.respawn()

            # if WRONG kana
            for kana in Graphicgroups.kanas:
                if kana.collide(epew.hitbox):
                    Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                    Graphicgroups.enemyprojectiles.pop(Graphicgroups.enemyprojectiles.index(epew))
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                    pygame.mixer.Sound.play(Constants.goodhit)

            # if CORRECT kana
            for kana in Graphicgroups.correctkanas:
                if kana.collide(epew.hitbox):
                    Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(kana))
                    try: Graphicgroups.enemyprojectiles.pop(Graphicgroups.enemyprojectiles.index(epew))
                    except: pass
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                    pygame.mixer.Sound.play(Constants.goodhit)
        #endregion

        #region BIG LASER
        # if BIG LASER hits player
        for biglaser in Graphicgroups.biglasers:
            if Variables.shipcollision == True:
                if biglaser.collide(Game_Objects.player.spaceship_rect):
                    ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                    Graphicgroups.explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(Constants.shiphit)
                    Game_Objects.player.respawn()

            # correctKana hit by BIG LASER
            for kana in Graphicgroups.correctkanas:
                if kana.collide(biglaser.hitbox):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(kana))
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)

            # Wrong Kana hit by BIG LASER
            for kana in Graphicgroups.kanas:
                if kana.collide(biglaser.hitbox):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)

            # if enemy hit by BIG LASER
            for enemy in Graphicgroups.enemies:
                if enemy.collide(biglaser.hitbox):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    Variables.score += 1
                    explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                    Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))

            # if powerup hit by BIG LASER
            for powerup in Graphicgroups.powerups:
                if powerup.collide(biglaser.hitbox):
                    explosion = Game_Objects.Explosion(powerup.x, powerup.y,Constants.explosion_surfs,0.5,False)
                    pygame.mixer.Sound.play(Constants.goodhit)
                    Graphicgroups.explosion_group.add(explosion)
                    Graphicgroups.powerups.pop(Graphicgroups.powerups.index(powerup))

            #if BIG LASER hits wall segments
            for wod in Graphicgroups.wallsegments:
                if wod.collide(biglaser.hitbox):
                    Graphicgroups.wallsegments.pop(Graphicgroups.wallsegments.index(wod))
                    Game_Objects.Debris.spawn(wod.x,wod.y,math.radians(random.randint(-10,10)),random.randint(100,300),Constants.brick_surf,0)
                    pygame.mixer.Sound.play(Constants.brickbreak_sound)
                    explosion = Game_Objects.Explosion(wod.x, wod.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)

        #endregion

        #region Space Junk
        for junk in Graphicgroups.spacejunk:
            # correctKana hit by junk
            for kana in Graphicgroups.correctkanas:
                if kana.collide(junk.hitbox):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(kana))
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)

            # Wrong Kana hit by junk
            for kana in Graphicgroups.kanas:
                if kana.collide(junk.hitbox):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)

            # Wall segments hit by junk
            for wod in Graphicgroups.wallsegments:
                if wod.collide(junk.hitbox):
                    Graphicgroups.wallsegments.pop(Graphicgroups.wallsegments.index(wod))
                    Game_Objects.Debris.spawn(wod.x,wod.y,math.radians(random.randint(-10,10)),random.randint(100,300),Constants.brick_surf,0)
                    pygame.mixer.Sound.play(Constants.brickbreak_sound)
                    explosion = Game_Objects.Explosion(wod.x, wod.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)

        #endregion

        #region Enemy Debris
        for edebs in Graphicgroups.debris:
            # if enemy debris hits Enemy
            for enemy in Graphicgroups.enemies:
                if enemy.collide(edebs.hitbox) and edebs.origin != Graphicgroups.enemies.index(enemy):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    #Variables.score += 1
                    damage = 1 + int(Variables.enemy_health_multiplier * Settings.enemy_health * 0.2)
                    enemy.health -= damage
                    Game_Objects.Debris.spawn(enemy.enemy_rect.centerx,enemy.y,math.radians(random.randint(80,280)),random.randint(50,200),Constants.debris_surf,Graphicgroups.enemies.index(enemy))
                    Game_Objects.Damagenum.spawn(enemy.enemy_rect.centerx,enemy.velocity,enemy.y,damage)
                    if enemy.health == 0:
                        Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                        explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.explosion_surfs,0.5,False)
                        Graphicgroups.explosion_group.add(explosion)
                    try: Graphicgroups.debris.pop(Graphicgroups.debris.index(edebs))
                    except: pass
            pass
        #endregion Enemy Debris

        #region Ship
        # if player's ship hits correct kana
        for kana in Graphicgroups.correctkanas:
            if Variables.shipcollision == True:
                if kana.collide(Game_Objects.player.spaceship_rect):
                    Variables.RGB[1] = 64
                    Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(kana))
                    #explosion = Game_Objects.Explosion(kana.x, kana.y,explosion_surfs.images,0.5,False)
                    #ship_explosion = Game_Objects.Explosion(player.spaceship_rect.center[0], player.spaceship_rect.center[1],explosion_surfs.images,1,False)
                    #explosion_group.add(explosion)
                    #explosion_group.add(ship_explosion)
                    # pygame.mixer.Sound.play(goodhit)
                    if kana.x >= 2*Constants.WIDTH // 3:
                        Variables.score += 3
                    elif kana.x > Constants.WIDTH // 3 and kana.x < 2*Constants.WIDTH // 3:
                        Variables.score += 2
                    else:
                        Variables.score += 1
                    kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', Variables.gamekana[Variables.level][kana.kana][2] + '.wav'))
                    pygame.mixer.Sound.play(kana_sound)
                    kanaint = int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3])
                    if kanaint <= Settings.num_to_shoot_new_kana: kanaint += 1
                    Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3] = kanaint
                    #player.respawn()

            # if player hits kana
        
        # if player's ship hits wrong kana
        for kana in Graphicgroups.kanas:
            if Variables.shipcollision == True:
                if kana.collide(Game_Objects.player.spaceship_rect):
                    Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                    Graphicgroups.explosion_group.add(explosion)
                    Graphicgroups.explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(Constants.shiphit)
                    kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', Variables.gamekana[Variables.level][kana.kana][2] + '.wav'))
                    pygame.mixer.Sound.play(kana_sound)
                    Game_Objects.player.respawn()

        # if player hits Enemy
        for enemy in Graphicgroups.enemies:
            if Variables.shipcollision == True:
                if enemy.collide(Game_Objects.player.spaceship_rect):
                    Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                    explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.explosion_surfs,0.5,False)
                    ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                    Graphicgroups.explosion_group.add(explosion)
                    Graphicgroups.explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(Constants.shiphit)
                    Game_Objects.player.respawn()

        # if player hits enemy debris
        for bits in Graphicgroups.debris:
            if Variables.shipcollision == True:
                if bits.collide(Game_Objects.player.spaceship_rect):
                    Graphicgroups.debris.pop(Graphicgroups.debris.index(bits))
                    explosion = Game_Objects.Explosion(bits.x, bits.y,Constants.explosion_surfs,0.25,False)
                    ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                    Graphicgroups.explosion_group.add(explosion)
                    Graphicgroups.explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(Constants.shiphit)
                    Game_Objects.player.respawn()

        # if player hits Wall of Death
        for wod in Graphicgroups.wallsegments:
            if Variables.shipcollision == True:
                if wod.collide(Game_Objects.player.spaceship_rect):
                    ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                    Graphicgroups.explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(Constants.shiphit)
                    Game_Objects.player.respawn()

        # if player hits Animatedpowerup
            # handled in PUEFFECT method of Animatedpowerup Class
        #endregion
    
        #region Wrong Kana on Correct Kana
        for kana in Graphicgroups.kanas:
            for ckana in Graphicgroups.correctkanas:
                if kana.collide(ckana.centered_image):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
        #endregion

        #region Correct Kana
        for kana in Graphicgroups.correctkanas:
            for wod in Graphicgroups.wallsegments:
                if wod.collide(kana.hitbox):
                    Graphicgroups.wallsegments.pop(Graphicgroups.wallsegments.index(wod))
                    Game_Objects.Debris.spawn(wod.x,wod.y,math.radians(random.randint(-10,10)),random.randint(100,300),Constants.brick_surf,0)
                    pygame.mixer.Sound.play(Constants.brickbreak_sound)
                    explosion = Game_Objects.Explosion(wod.x, wod.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
        #endregion

    def handle_events(self, events):
        for event in events:
            # Click the X to close window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # KEYDOWN
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: Variables.lives = 0
                if event.key == ord('o'):
                    powerup_type = random.randint(0,3)
                    Game_Objects.AnimatedPowerUp.spawn(
                        Constants.powerup_array[powerup_type]["xvel"],
                        Constants.powerup_array[powerup_type]["surfindx"],
                        Constants.powerup_array[powerup_type]["pueffect"],
                        )
                    pass
                if event.key == ord('l'):
                    if Game_Objects.player.lasersight == True:
                        Game_Objects.player.lasersight = False
                        pygame.mixer.Sound.stop(Constants.shiplaser_sound)
                        Game_Objects.player.laserlength = 0
                    else:
                        Game_Objects.player.lasersight = True
                        pygame.mixer.Sound.play(Constants.shiplaser_sound)
                        Game_Objects.player.lasersightcounter = Game_Objects.player.poweruptimelength
                if event.key == ord('h'):
                    if Variables.hitboxshow == True:
                        Variables.hitboxshow = False
                        Variables.debugwindow = False
                    else:
                        Variables.hitboxshow = True
                        Variables.debugwindow = True
                if event.key == ord('k'):
                    selection = random.randint(0,Variables.levels[Variables.level]-1)
                    if selection != Variables.kananum:
                        Graphicgroups.kanas.append(Game_Objects.Kana(Constants.WIDTH+Constants.off_screen_offset, random.randrange(128,Constants.HEIGHT-200,),selection,random.randint(Constants.min_kana_alpha,256),random.randint(-Settings.kana_rotate_rate,Settings.kana_rotate_rate)))
                        self.incorrectkana_timer = time.time()
                        self.incorrectkana_thresh = random.randint(Settings.minimum_incorrect_kana_frequency,Settings.maximum_incorrect_kana_frequency)/10
                if event.key == ord('p'): pass
                if event.key == ord('i'): pass #Game_Objects.WallOfDeath.spawn(Constants.WIDTH,0)
                if event.key == ord('b'): Game_Objects.Bridge.spawn()
                if event.key == ord('q'): pass #Game_Objects.SpaceJunk.spawn()
                if event.key == ord('n'): Variables.TRANSITION = True
                if event.key == ord('e'): Game_Objects.Enemies.spawn()
                if event.key == ord('r'): Game_Objects.BigLaserWarning.spawn(Game_Objects.player)
                if event.key == ord('.'): 
                    if Variables.pewtype < len(Constants.pew_array)-1: Variables.pewtype += 1
                if event.key == ord(','): 
                    if Variables.pewtype > 0: Variables.pewtype -= 1
                if event.key == ord('='): Variables.score += 10
                if event.key == ord('-'): Variables.score -= 10
                if event.key == ord('9'): Variables.musicvolume -=0.01
                if event.key == ord('0'): Variables.musicvolume +=0.01
                if event.key == ord('8'): Game_Objects.TipTicker.spawn(Constants.tips[0],200)

class BossFight:
    def __init__(self):
        self.done = False
        self.boss = Variables.BOSSSTATE
        self.bgfade_timer = time.time()
        self.boss_end_state = "musicfade"
        self.enemy_wait_timer = 10
        self.bonus_timer = time.time()
        self.kana_blip = time.time()
        self.prev_level = Variables.level
        self.extralife = Settings.ship_extra_life_increment
        self.bonus_score = Settings.boss_bonus_score
        self.get_ready_timer = Settings.get_ready_timer_max

    def manifest(self):
        Game_Objects.timer.bossmessage(delay=0)                                 # Boss Message Timer
        Game_Objects.timer.boss(delay=3)                                        # Boss Timer
        Game_Objects.timer.stars(frequency=0.04,velocity=600)                   # Stars Timer
        Game_Objects.timer.biglaser(enemywaittimer=self.enemy_wait_timer)       # Big Laser Timer
        Game_Objects.timer.planet()                                             # PLANET Timer
        Game_Objects.timer.junk()                                               # JUNK Timer
        Game_Objects.timer.wallofdeath()                                        # Wall of Death Timer

    def bosstransitionout(self):
        #region Fade out music and transition back to Game
        if Variables.TRANSITION == False and self.boss_end_state == "musicfade":
            if Variables.musicvolume <= 0:
                self.boss_end_state = "bonusadd"
            Variables.musicvolume -= 0.05 * Variables.dt
        #endregion Fade out music and transition back to Game

        #region add bonus to score
        if Variables.TRANSITION == False and self.boss_end_state == "bonusadd":
            if self.bonus_score <= 0:
                self.boss_end_state = "getready"
                self.get_ready_timer = Settings.get_ready_timer_max
            else:
                if time.time() - self.bonus_timer >= 0.05:
                    self.bonus_score -= 1
                    Variables.score += 1
                    pygame.mixer.Sound.play(Constants.correct_kana_dying_sound)
                    self.bonus_timer = time.time()
        #endregion add bonus to score

        #region Rest period before re-entering game
        if Variables.TRANSITION == False and self.boss_end_state == "getready":
            if self.get_ready_timer <= 0:
                self.boss_end_state = "musicfade"                                   # Reset Transistion state to beginning (musicfade)
                Variables.GAMESTATE = False
                Variables.BOSSSTATE = True
                Variables.level += 1                                                # Increase Level
                Variables.musicvolume = Variables.maxmusicvolume                    # Set Music Volume Back to Default
                self.bonus_score = Settings.boss_bonus_score
                self.get_ready_timer = Settings.get_ready_timer_max

                # Reset Timers
                Game_Objects.timer.WoD_timer = time.time()
                Game_Objects.timer.incorrectkana_timer = time.time()
                Game_Objects.timer.junk_timer = time.time()
                Game_Objects.timer.correctkana_timer = time.time()
                Game_Objects.timer.biglaser_timer = time.time()
                Game_Objects.timer.enemy_timer = time.time()
                Game_Objects.timer.powerup_timer = time.time()
                Game_Objects.timer.bridge_timer = time.time()

            else: self.get_ready_timer -= Variables.dt
        #endregion Rest period before re-entering game

    def update(self):
        Variables.STATE = "Boss"
        self.boss = Variables.BOSSSTATE
        self.bosstransitionout()

        #region Extra Life
        if Variables.score >= self.extralife:
            Game_Objects.AnimatedPowerUp.spawn(
                Constants.powerup_array[2]["xvel"],
                Constants.powerup_array[2]["surfindx"],
                Constants.powerup_array[2]["pueffect"],
                )
            self.extralife += Settings.ship_extra_life_increment
        #endregion

        #region decrement bonus score every half second
        if time.time() - self.bonus_timer >= 1 and len(Graphicgroups.bosses) > 0:
            if self.bonus_score > 0: self.bonus_score -= 1
            self.bonus_timer = time.time()
        #endregion decrement bonus score every half second
            
        #region Warning Messages
        if Variables.level == Settings.enemy_start_level and self.prev_level < Settings.enemy_start_level:
            Game_Objects.CenterWarning.spawn('Enemies Active',Constants.enemy_spritesheet_surfs[0].images[0],3)
            self.enemy_wait_timer = 3
            self.prev_level = Settings.enemy_start_level
        #endregion

        #region You lost all of your lives
        if Variables.lives <= 0:
            pygame.mixer.Sound.stop(Constants.enginesound)
            Functions.write_csv('data/userkana.csv',Variables.commasep)
            self.done = True
        #endregion

        #region Stop enemies from showing up right at the start
        if self.enemy_wait_timer >= 0: self.enemy_wait_timer -= 1 * Variables.dt
        #endregion

        for bullet in Graphicgroups.bullets: bullet.update()                            # BULLETS
        for biglaser in Graphicgroups.biglasers: biglaser.update()                      # BIG LASER
        Graphicgroups.planet_group.update(Game_Objects.player)                          # PLANETS
        for junk in Graphicgroups.spacejunk: junk.update()                              # RANDOM JUNK
        Graphicgroups.starfield_group.update(Game_Objects.player)                       # STARS
        for cutoff in Graphicgroups.cuttoffline: cutoff.update(Game_Objects.player)     # CUTOFF LINE
        for kana in Graphicgroups.correctkanas: kana.update(Game_Objects.player)        # Correct Kanas
        for kana in Graphicgroups.kanas: kana.update(Game_Objects.player)               # Incorrect kanas
        for warning in Graphicgroups.warnings: warning.update()                         # Big Laser Warning
        for epew in Graphicgroups.enemyprojectiles: epew.update()                       # Enemy Projectiles
        for enemy in Graphicgroups.enemies: enemy.update()                              # ENEMIES
        for boss in Graphicgroups.bosses: boss.update()                                 # BOSS
        for wod in Graphicgroups.wallsegments: wod.update()                             # Wall of Death
        for brick in Graphicgroups.bricks: brick.update()                               # Brick debris
        for bits in Graphicgroups.debris: bits.update()                                 # Debris
        Game_Objects.player.update()                                                    # Player
        Graphicgroups.explosion_group.update()                                          # Explosion
        for powerup in Graphicgroups.animatedpowerup:                                   # Powerups
            powerup.update()
            powerup.effect(powerup.pueffect,Game_Objects.player)
        for centerwarn in Graphicgroups.centerwarning: centerwarn.update()              # UI
        Graphicgroups.bridge_group.update(Game_Objects.player)                          # BRIDGE WIPE
        Graphicgroups.tip_group.update()                                                # Tip Ticker

    def draw(self,screen):
        pygame.mouse.set_visible(False)
        # region SCREEN
        if time.time() - self.bgfade_timer >= 0.001:
            if Variables.RGB[0] > 10: Variables.RGB[0] -= 500 * Variables.dt
            else: Variables.RGB[0] = 0
            if Variables.RGB[1] > 10: Variables.RGB[1] -= 500 * Variables.dt
            else: Variables.RGB[1] = 0
            if Variables.RGB[2] > 10: Variables.RGB[2] -= 500 * Variables.dt
            else: Variables.RGB[2] = 0
            self.bgfade_timer = time.time()
        try: screen.fill((Variables.RGB[0],Variables.RGB[1],Variables.RGB[2]))
        except: pass
        #endregion

        #region KANA LIST
        for f in range(int(Variables.levels[Variables.level])): Graphicgroups.kanalist.append(Variables.commasep[f])
        for f in range(int(Variables.levels[Variables.level])):
            if Variables.gamemode == 0: kanalistthing = Constants.ui_font.render(Graphicgroups.kanalist[f][0], True, (20,20,20))
            else: kanalistthing = Constants.ui_font.render(Graphicgroups.kanalist[f][1], True, (20,20,20))
            screen.blit(kanalistthing,(25+(27*f),Constants.HEIGHT-30))
        #endregion

        Graphicgroups.planet_group.draw(screen)                                         # PLANETS
        for junk in Graphicgroups.spacejunk: junk.draw(screen)                          # RANDOM JUNK
        Graphicgroups.starfield_group.draw(screen)                                      # STARS
        for warning in Graphicgroups.warnings: warning.draw(screen)                     # WARNING for BIG LASER
        for bullet in Graphicgroups.bullets: bullet.draw(screen)                        # BULLETS
        for epew in Graphicgroups.enemyprojectiles: epew.draw(screen)                   # ENEMY PEW
        for bits in Graphicgroups.debris: bits.draw(screen)                             # Bits debris
        for enemy in Graphicgroups.enemies: enemy.draw(screen,Game_Objects.player)      # ENEMIES
        for boss in Graphicgroups.bosses: boss.draw(screen,Game_Objects.player)         # BOSS
        for kana in Graphicgroups.correctkanas: kana.draw(screen)                       # CORRECT KANA
        for kana in Graphicgroups.kanas: kana.draw(screen)                              # WRONG KANA
        Game_Objects.player.draw(screen)                                                # PLAYER
        for powerup in Graphicgroups.animatedpowerup: powerup.draw(screen)              # Powerup
        for biglaser in Graphicgroups.biglasers: biglaser.draw(screen)                  # BIG LASER
        for wod in Graphicgroups.wallsegments: wod.draw(screen)                         # Wall of Death
        for brick in Graphicgroups.bricks: brick.draw(screen)                           # Brick debirs
        for shield in Graphicgroups.shields: shield.draw(screen)                        # Shields
        for damagenumber in Graphicgroups.damagenumbers: damagenumber.draw(screen)      # Damage values 
        Graphicgroups.explosion_group.draw(screen)                                      # EXPLOSION
        Functions.question_text(screen)                                                 # QUESTION TEXT
        Functions.uitext(screen)                                                        # UI TEXT
        Graphicgroups.bridge_group.draw(screen)                                         # BRIDGE WIPE
        for centerwarn in Graphicgroups.centerwarning: centerwarn.draw()                # Center Warning
        
        if Variables.debugwindow: Debug.draw(Constants.debug_locationx,Constants.debug_locationy)   # DEBUG

    def collision(self):
        # If it is a projectile, then it will hit something, 
        # if it is not a projectile then the ship is considered the projectile
        # Space Junk will be treated like a projectile because it persists after collision

        #region Player Projectiles
        for bullet in Graphicgroups.bullets:

            #if player's bullet hits Wall of Death
            for wod in Graphicgroups.wallsegments:
                if wod.collide(bullet.rect):
                    Graphicgroups.wallsegments.pop(Graphicgroups.wallsegments.index(wod))
                    try:
                        persist = Constants.pew_array[Variables.pewtype]["persist"]
                        if not persist:
                            Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                    except: pass
                    Game_Objects.Debris.spawn(wod.x,wod.y,math.radians(random.randint(-10,10)),random.randint(100,300),Constants.brick_surf,0)
                    pygame.mixer.Sound.play(Constants.brickbreak_sound)
                    explosion = Game_Objects.Explosion(wod.x, wod.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                    Variables.score += 1

            # if player's bullet hits CORRECT Kana
            for ckana in Graphicgroups.correctkanas:    
                if ckana.collide(bullet.rect):
                    Variables.RGB[0] = 128
                    pygame.mixer.Sound.play(Constants.badhit)
                    kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', ckana.kanasound + '.wav'))
                    pygame.mixer.Sound.play(kana_sound)
                    if ckana.x >= 2*Constants.WIDTH // 3:
                        Variables.score -= 3
                    elif ckana.x > Constants.WIDTH // 3 and ckana.x < 2*Constants.WIDTH // 3:
                        Variables.score -= 2
                    else:
                        Variables.score -= 1
                    explosion = Game_Objects.Explosion(ckana.x, ckana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                    try:
                        persist = Constants.pew_array[Variables.pewtype]["persist"]
                        if not persist:
                            Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                    except: pass
                    Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(ckana))
                    # kanaint = int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3])
                    # if kanaint <= num_to_shoot_new_kana: kanaint += 1
                    #Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3] = kanaint

            # if player's bullet hits WRONG kana
            for kana in Graphicgroups.kanas:
                if kana.collide(bullet.rect):
                    Variables.RGB[1] = 64
                    pygame.mixer.Sound.play(Constants.goodhit)
                    Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                    try:
                        persist = Constants.pew_array[Variables.pewtype]["persist"]
                        if not persist:
                            Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                    except: pass
                    kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', kana.kanasound + '.wav'))
                    pygame.mixer.Sound.play(kana_sound)
                    if kana.x >= 2*Constants.WIDTH // 3:
                        Variables.score += 3
                    elif kana.x > Constants.WIDTH // 3 and kana.x < 2*Constants.WIDTH // 3:
                        Variables.score += 2
                    else:
                        Variables.score += 1
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)

            # if player's bullet hits Enemy
            for enemy in Graphicgroups.enemies:
                if enemy.collide(bullet.rect):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    damage = 1 + random.randint(int(Game_Objects.player.laserpower/5),Game_Objects.player.laserpower)
                    enemy.health -= damage
                    Game_Objects.Debris.spawn(enemy.enemy_rect.centerx,enemy.y,math.radians(random.randint(80,280)),random.randint(50,200),Constants.debris_surf,Graphicgroups.enemies.index(enemy))
                    Game_Objects.Damagenum.spawn(enemy.enemy_rect.centerx,enemy.velocity,enemy.y,damage)
                    if enemy.health <= 0:
                        Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                        explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.explosion_surfs,0.5,False)
                        Graphicgroups.explosion_group.add(explosion)
                        Variables.score += 1
                    try:
                        persist = Constants.pew_array[Variables.pewtype]["persist"]
                        if not persist:
                            Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                    except: pass

            # if player's bullet hits Boss
            for boss in Graphicgroups.bosses:
                if boss.collide(bullet.rect):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    damage = random.randint(int(Game_Objects.player.laserpower / 10),int(Game_Objects.player.laserpower))
                    boss.health -= damage
                    Game_Objects.Debris.spawn(boss.boss_rect.centerx,boss.y,math.radians(random.randint(80,280)),random.randint(50,200),Constants.debris_surf,Graphicgroups.bosses.index(boss))
                    Game_Objects.Damagenum.spawn(boss.boss_rect.centerx,boss.velocity,boss.y,damage)
                    if boss.health <= 0:
                        Graphicgroups.bosses.pop(Graphicgroups.bosses.index(boss))
                        explosion = Game_Objects.Explosion(boss.x, boss.y,Constants.explosion_surfs,8,False)
                        Graphicgroups.explosion_group.add(explosion)
                        Variables.score += 99
                        Variables.TRANSITION = False
                    try: Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                    except: pass

            # if player's bullet hits powerup
            for powerup in Graphicgroups.powerups:
                if powerup.collide(bullet.rect):
                    pygame.mixer.Sound.play(Constants.badhit)
                    explosion = Game_Objects.Explosion(powerup.x, powerup.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                    try:
                        persist = Constants.pew_array[Variables.pewtype]["persist"]
                        if not persist:
                            Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                    except: pass
                    Graphicgroups.powerups.pop(Graphicgroups.powerups.index(powerup))

            # if player's bullet hits ship debirs
            for shipdeb in Graphicgroups.debris:
                if shipdeb.collide(bullet.rect):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    explosion = Game_Objects.Explosion(shipdeb.x, shipdeb.y,Constants.explosion_surfs,0.2,False)
                    Graphicgroups.explosion_group.add(explosion)
                    try:
                        persist = Constants.pew_array[Variables.pewtype]["persist"]
                        if not persist:
                            Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                    except: pass
                    Graphicgroups.debris.pop(Graphicgroups.debris.index(shipdeb))

        #endregion
        
        #region Enemy Projectiles
        for epew in Graphicgroups.enemyprojectiles:
            # if hit Player
            if Variables.shipcollision == True:
                if epew.collide(Game_Objects.player.spaceship_rect):
                    Graphicgroups.enemyprojectiles.pop(Graphicgroups.enemyprojectiles.index(epew))
                    explosion = Game_Objects.Explosion(epew.x, epew.y,Constants.explosion_surfs,0.5,False)
                    ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                    Graphicgroups.explosion_group.add(explosion)
                    Graphicgroups.explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(Constants.shiphit)
                    Game_Objects.player.respawn()

            # if WRONG kana
            for kana in Graphicgroups.kanas:
                if kana.collide(epew.hitbox):
                    Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                    Graphicgroups.enemyprojectiles.pop(Graphicgroups.enemyprojectiles.index(epew))
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                    pygame.mixer.Sound.play(Constants.goodhit)

            # if CORRECT kana
            for kana in Graphicgroups.correctkanas:
                if kana.collide(epew.hitbox):
                    Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(kana))
                    try: Graphicgroups.enemyprojectiles.pop(Graphicgroups.enemyprojectiles.index(epew))
                    except: pass
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                    pygame.mixer.Sound.play(Constants.goodhit)
        #endregion

        #region BIG LASER
        # if BIG LASER hits player
        for biglaser in Graphicgroups.biglasers:
            if Variables.shipcollision == True:
                if biglaser.collide(Game_Objects.player.spaceship_rect):
                    ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                    Graphicgroups.explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(Constants.shiphit)
                    Game_Objects.player.respawn()

            # correctKana hit by BIG LASER
            for kana in Graphicgroups.correctkanas:
                if kana.collide(biglaser.hitbox):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(kana))
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)

            # Wrong Kana hit by BIG LASER
            for kana in Graphicgroups.kanas:
                if kana.collide(biglaser.hitbox):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)

            # if enemy hit by BIG LASER
            for enemy in Graphicgroups.enemies:
                if enemy.collide(biglaser.hitbox):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    Variables.score += 1
                    explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                    Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))

            # if powerup hit by BIG LASER
            for powerup in Graphicgroups.powerups:
                if powerup.collide(biglaser.hitbox):
                    explosion = Game_Objects.Explosion(powerup.x, powerup.y,Constants.explosion_surfs,0.5,False)
                    pygame.mixer.Sound.play(Constants.goodhit)
                    Graphicgroups.explosion_group.add(explosion)
                    Graphicgroups.powerups.pop(Graphicgroups.powerups.index(powerup))

            #if BIG LASER hits wall segments
            for wod in Graphicgroups.wallsegments:
                if wod.collide(biglaser.hitbox):
                    Graphicgroups.wallsegments.pop(Graphicgroups.wallsegments.index(wod))
                    Game_Objects.Debris.spawn(wod.x,wod.y,math.radians(random.randint(-10,10)),random.randint(100,300),Constants.brick_surf,0)
                    pygame.mixer.Sound.play(Constants.brickbreak_sound)
                    explosion = Game_Objects.Explosion(wod.x, wod.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)

        #endregion

        #region Space Junk
        for junk in Graphicgroups.spacejunk:
            # correctKana hit by junk
            for kana in Graphicgroups.correctkanas:
                if kana.collide(junk.hitbox):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(kana))
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)

            # Wrong Kana hit by junk
            for kana in Graphicgroups.kanas:
                if kana.collide(junk.hitbox):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)

            # Wall segments hit by junk
            for wod in Graphicgroups.wallsegments:
                if wod.collide(junk.hitbox):
                    Graphicgroups.wallsegments.pop(Graphicgroups.wallsegments.index(wod))
                    Game_Objects.Debris.spawn(wod.x,wod.y,math.radians(random.randint(-10,10)),random.randint(100,300),Constants.brick_surf,0)
                    pygame.mixer.Sound.play(Constants.brickbreak_sound)
                    explosion = Game_Objects.Explosion(wod.x, wod.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)

        #endregion

        #region Enemy Debris
        for edebs in Graphicgroups.debris:
            # if enemy debris hits Enemy
            for enemy in Graphicgroups.enemies:
                if enemy.collide(edebs.hitbox) and edebs.origin != Graphicgroups.enemies.index(enemy):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    #Variables.score += 1
                    damage = 1 + int(Variables.enemy_health_multiplier * Settings.enemy_health * 0.2)
                    enemy.health -= damage
                    Game_Objects.Debris.spawn(enemy.enemy_rect.centerx,enemy.y,math.radians(random.randint(80,280)),random.randint(50,200),Constants.debris_surf,Graphicgroups.enemies.index(enemy))
                    Game_Objects.Damagenum.spawn(enemy.enemy_rect.centerx,enemy.velocity,enemy.y,damage)
                    if enemy.health == 0:
                        Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                        explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.explosion_surfs,0.5,False)
                        Graphicgroups.explosion_group.add(explosion)
                    try: Graphicgroups.debris.pop(Graphicgroups.debris.index(edebs))
                    except: pass
            pass
        #endregion Enemy Debris

        #region Ship
        # if player's ship hits correct kana
        for kana in Graphicgroups.correctkanas:
            if Variables.shipcollision == True:
                if kana.collide(Game_Objects.player.spaceship_rect):
                    Variables.RGB[1] = 64
                    Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(kana))
                    #explosion = Game_Objects.Explosion(kana.x, kana.y,explosion_surfs.images,0.5,False)
                    #ship_explosion = Game_Objects.Explosion(player.spaceship_rect.center[0], player.spaceship_rect.center[1],explosion_surfs.images,1,False)
                    #explosion_group.add(explosion)
                    #explosion_group.add(ship_explosion)
                    # pygame.mixer.Sound.play(goodhit)
                    if kana.x >= 2*Constants.WIDTH // 3:
                        Variables.score += 3
                    elif kana.x > Constants.WIDTH // 3 and kana.x < 2*Constants.WIDTH // 3:
                        Variables.score += 2
                    else:
                        Variables.score += 1
                    kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', Variables.gamekana[Variables.level][kana.kana][2] + '.wav'))
                    pygame.mixer.Sound.play(kana_sound)
                    kanaint = int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3])
                    if kanaint <= Settings.num_to_shoot_new_kana: kanaint += 1
                    Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3] = kanaint
                    #player.respawn()

            # if player hits kana
        
        # if player's ship hits wrong kana
        for kana in Graphicgroups.kanas:
            if Variables.shipcollision == True:
                if kana.collide(Game_Objects.player.spaceship_rect):
                    Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                    Graphicgroups.explosion_group.add(explosion)
                    Graphicgroups.explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(Constants.shiphit)
                    kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', Variables.gamekana[Variables.level][kana.kana][2] + '.wav'))
                    pygame.mixer.Sound.play(kana_sound)
                    Game_Objects.player.respawn()

        # if player hits Enemy
        for enemy in Graphicgroups.enemies:
            if Variables.shipcollision == True:
                if enemy.collide(Game_Objects.player.spaceship_rect):
                    Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                    explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.explosion_surfs,0.5,False)
                    ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                    Graphicgroups.explosion_group.add(explosion)
                    Graphicgroups.explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(Constants.shiphit)
                    Game_Objects.player.respawn()

        # if player hits Boss
        for enemy in Graphicgroups.bosses:
            if Variables.shipcollision == True:
                if enemy.collide(Game_Objects.player.spaceship_rect):
                    # Graphicgroups.bosses.pop(Graphicgroups.bosses.index(enemy))
                    # explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.explosion_surfs,0.5,False)
                    ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                    # Graphicgroups.explosion_group.add(explosion)
                    Graphicgroups.explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(Constants.shiphit)
                    Game_Objects.player.respawn()

        # if player hits enemy debris
        for bits in Graphicgroups.debris:
            if Variables.shipcollision == True:
                if bits.collide(Game_Objects.player.spaceship_rect):
                    Graphicgroups.debris.pop(Graphicgroups.debris.index(bits))
                    explosion = Game_Objects.Explosion(bits.x, bits.y,Constants.explosion_surfs,0.25,False)
                    ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                    Graphicgroups.explosion_group.add(explosion)
                    Graphicgroups.explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(Constants.shiphit)
                    Game_Objects.player.respawn()

        # if player hits Wall of Death
        for wod in Graphicgroups.wallsegments:
            if Variables.shipcollision == True:
                if wod.collide(Game_Objects.player.spaceship_rect):
                    ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                    Graphicgroups.explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(Constants.shiphit)
                    Game_Objects.player.respawn()
        #endregion
    
        #region Wrong Kana on Correct Kana
        for kana in Graphicgroups.kanas:
            for ckana in Graphicgroups.correctkanas:
                if kana.collide(ckana.centered_image):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
        #endregion

        #region Correct Kana
        for kana in Graphicgroups.correctkanas:
            for wod in Graphicgroups.wallsegments:
                if wod.collide(kana.hitbox):
                    Graphicgroups.wallsegments.pop(Graphicgroups.wallsegments.index(wod))
                    Game_Objects.Debris.spawn(wod.x,wod.y,math.radians(random.randint(-10,10)),random.randint(100,300),Constants.brick_surf,0)
                    pygame.mixer.Sound.play(Constants.brickbreak_sound)
                    explosion = Game_Objects.Explosion(wod.x, wod.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
        #endregion

    def handle_events(self, events):
        for event in events:
            # Click the X to close window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # KEYDOWN
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: Variables.lives = 0
                if event.key == ord('o'): pass
                if event.key == ord('l'):
                    if Game_Objects.player.lasersight == True:
                        Game_Objects.player.lasersight = False
                        pygame.mixer.Sound.stop(Constants.shiplaser_sound)
                        Game_Objects.player.laserlength = 0
                    else:
                        Game_Objects.player.lasersight = True
                        pygame.mixer.Sound.play(Constants.shiplaser_sound)
                        Game_Objects.player.lasersightcounter = Game_Objects.player.poweruptimelength
                if event.key == ord('h'):
                    if Variables.hitboxshow == True:
                        Variables.hitboxshow = False
                    else:
                        Variables.hitboxshow = True
                if event.key == ord('v'):
                    if Variables.debugwindow:
                        Variables.debugwindow = False
                    else:
                        Variables.debugwindow = True
                if event.key == ord('k'):
                    selection = random.randint(0,Variables.levels[Variables.level]-1)
                    if selection != Variables.kananum:
                        Graphicgroups.kanas.append(Game_Objects.Kana(Constants.WIDTH+Constants.off_screen_offset, random.randrange(128,Constants.HEIGHT-200,),selection,random.randint(Constants.min_kana_alpha,256),random.randint(-Settings.kana_rotate_rate,Settings.kana_rotate_rate)))
                        self.incorrectkana_timer = time.time()
                        self.incorrectkana_thresh = random.randint(Settings.minimum_incorrect_kana_frequency,Settings.maximum_incorrect_kana_frequency)/10
                if event.key == ord('p'): Game_Objects.Planet.spawn()
                if event.key == ord('i'): Game_Objects.WallOfDeath.spawn(Constants.WIDTH,0)
                if event.key == ord('q'): Game_Objects.SpaceJunk.spawn()
                if event.key == ord('e'): Game_Objects.Bosses.spawn()
                if event.key == ord('r'): Game_Objects.BigLaserWarning.spawn(Game_Objects.player)
                if event.key == ord('='): Variables.score += 10
                if event.key == ord('-'): Variables.score -= 10

class GameOverState:
    def __init__(self):
        self.done = False
        self.boss = False
        self.star_timer = 0
        self.kana_timer = 0
        self.correct_kana_lost_sound_play = True
        self.kana_blip = time.time()
        self.kana_thresh = 1
        self.enemy_wait_timer = 10

    def manifest(self):
        Game_Objects.timer.stars(frequency=Settings.star_frequency,velocity=0)          # Stars Timer
        Game_Objects.timer.allkana(frequency=0.05)                                      # All Kana Timer

    def update(self):
        Variables.STATE = "GameOver"
        for bullet in Graphicgroups.bullets: bullet.update()                            # BULLETS
        for biglaser in Graphicgroups.biglasers: biglaser.update()                      # BIG LASER
        Graphicgroups.planet_group.update(Game_Objects.player)                          # PLANETS
        for junk in Graphicgroups.spacejunk: junk.update()                              # RANDOM JUNK
        Graphicgroups.starfield_group.update(Game_Objects.player)                       # STARS
        for cutoff in Graphicgroups.cuttoffline: cutoff.update(Game_Objects.player)     # CUTOFF LINE
        #region Correct Kanas                                                           # Correct Kanas
        for kana in Graphicgroups.correctkanas:
            kana.update(Game_Objects.player)

            # Grow Kana at 2/5th of the screen with
            if kana.x < 2 * (Constants.WIDTH // 5) and kana.x > 10:
                kana.kanascale += Variables.dt/5
                if time.time() - self.kana_blip >= kana.x/500:
                    pygame.mixer.Sound.play(Constants.correct_kana_dying_sound)
                    self.kana_blip = time.time()

            # Explode kana if touch left side of screen
            elif kana.x < 0:
                if self.correct_kana_lost_sound_play:
                    pygame.mixer.Sound.play(Constants.correct_kana_lost_sound)
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,3,False)
                    Graphicgroups.explosion_group.add(explosion)
                    Variables.score -= 10
                    self.correct_kana_lost_sound_play = False
        #endregion
        for kana in Graphicgroups.kanas: kana.update(Game_Objects.player)               # Incorrect kanas
        for warning in Graphicgroups.warnings: warning.update()                         # Big Laser Warning
        for epew in Graphicgroups.enemyprojectiles: epew.update()                       # Enemy Projectiles
        #region ENEMIES                                                                 # ENEMIES
        for enemy in Graphicgroups.enemies:
            enemy.update()
            enemy.shoot(Game_Objects.player)
        #endregion
        for wod in Graphicgroups.wallsegments: wod.update()                             # Wall of Death
        for brick in Graphicgroups.bricks: brick.update()                               # Brick debris
        for centerwarn in Graphicgroups.centerwarning: centerwarn.update()              # UI
        Graphicgroups.bridge_group.update(Game_Objects.player)                          # BRIDGE WIPE

    def draw(self,screen):
        screen.fill(('black'))

        Graphicgroups.planet_group.draw(screen)                                       # PLANETS
        for junk in Graphicgroups.spacejunk: junk.draw(screen)                        # RANDOM JUNK
        Graphicgroups.starfield_group.draw(screen)                                    # STARS
        for warning in Graphicgroups.warnings: warning.draw(screen)                   # WARNING for BIG LASER
        for bullet in Graphicgroups.bullets: bullet.draw(screen)                      # BULLETS
        for cutoff in Graphicgroups.cuttoffline: cutoff.draw(screen)                  # CUTOFF LINE
        for epew in Graphicgroups.enemyprojectiles: epew.draw(screen)                 # ENEMY PEW
        #region ENEMIES                                                               # ENEMIES
        for enemy in Graphicgroups.enemies:
            enemy.shoot(Game_Objects.player)
            enemy.draw(screen,Game_Objects.player)
        #endregion
        for kana in Graphicgroups.correctkanas: kana.draw(screen)                     # CORRECT KANA
        for kana in Graphicgroups.kanas: kana.draw(screen)                            # WRONG KANA
        #region POWERUP                                                               # POWERUP
        for powerup in Graphicgroups.powerups:
            powerup.update(Game_Objects.player)
            powerup.effect(powerup.pueffect,Game_Objects.player)
            powerup.draw(screen)
        #endregion
        for biglaser in Graphicgroups.biglasers: biglaser.draw(screen)                # BIG LASER
        for wod in Graphicgroups.wallsegments: wod.draw(screen)                       # Wall of Death
        for brick in Graphicgroups.bricks: brick.draw(screen)                         # Brick debirs
        #region EXPLOSION                                                             # EXPLOSION
        Graphicgroups.explosion_group.draw(screen)
        Graphicgroups.explosion_group.update()
        #endregion
        #region QUESTION TEXT                                                         # QUESTION TEXT
        def scale_surface_from_center(surface, scale_factor):
            original_rect = surface.get_rect()
            scaled_width = int(original_rect.width * scale_factor)
            scaled_height = int(original_rect.height * scale_factor)
            scaled_surface = pygame.transform.scale(surface, (scaled_width, scaled_height))
            scaled_rect = scaled_surface.get_rect(center=original_rect.center)
            return scaled_surface, scaled_rect
        
        # shoot_text = Constants.ui_font.render('Collect', True, 'white')
        # romajitext = Constants.question_font.render(Variables.gamekana[Variables.level][Variables.kananum][2], True, 'white')
        # Variables.theta += 5 * Variables.dt
        # theta_scale = math.sin(Variables.theta)
        # romaji_scaled, romaji_rect = scale_surface_from_center(romajitext, 1.5 + (theta_scale*.5))

        # screen.blit(shoot_text, (Settings.question_position[0]-120,Settings.question_position[1]+13))
        # screen.blit(romaji_scaled, (romaji_rect[0]+Settings.question_position[0],romaji_rect[1]+Settings.question_position[1]))
        #endregion
        #region UI TEXT                                                               # UI TEXT
        if Variables.score <=0: Variables.score = 0
        scoretext = Constants.ui_font.render("Score: " + str(Variables.score), True, 'white')
        screen.blit(scoretext, (Constants.WIDTH-200, 10))

        livestext = Constants.ui_font.render("Lives: " + str(Variables.lives), True, 'white')
        screen.blit(livestext, (Constants.WIDTH-400, 10))

        leveltext = Constants.ui_font.render("Level: " + str(Variables.level), True, 'white')
        screen.blit(leveltext, (Constants.WIDTH-600, 10))

        for centerwarn in Graphicgroups.centerwarning:
            centerwarn.draw()
        #endregion
        Graphicgroups.bridge_group.draw(screen)                                       # BRIDGE WIPE

        #region DEBUG                                                                 # DEBUG
        if Variables.debugwindow: Debug.draw(Constants.debug_locationx,Constants.debug_locationy)
        #endregion


        # Game Over 
        GAME_OVER_text = Constants.GAME_OVER_font.render('GAME OVER', True, 'white')
        screen.blit(GAME_OVER_text, (10, Constants.HEIGHT/2))

        GAME_OVER_Shadow_text = Constants.GAME_OVER_font.render('GAME OVER', True, 'white')
        GAME_OVER_Shadow_text.set_alpha(100)
        screen.blit(GAME_OVER_Shadow_text, (15, Constants.HEIGHT/2+5))

        # Score
        Score_text = Constants.question_font.render('Score: ' + str(Variables.score), True, 'white')
        screen.blit(Score_text, (400, Constants.HEIGHT/8))

    def collision(self):
        #CORRECT KANA
        for kana in Graphicgroups.correctkanas:
            # Kana hit by junk
            for junk in Graphicgroups.spacejunk:
                if kana.collide(junk.hitbox):
                    pygame.mixer.Sound.play(Constants.goodhit)
                    try: Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                    except: pass
                    explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)

    def handle_events(self, events):
        for event in events:
            #Click the X to close window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Game_Objects.player.movex, Game_Objects.player.movey = 0,0
                    Game_Objects.player.pullback = 1.5
                    Variables.lives = Variables.maxlives
                    menu_state.done = False
                    game_state.done = False
                    self.done = True
                if event.key == pygame.K_SPACE:
                    Game_Objects.player.movex, Game_Objects.player.movey = 0,0
                    Game_Objects.player.pullback = 1.5
                    Variables.lives = Variables.maxlives
                    menu_state.done = False
                    game_state.done = False
                    self.done = True                    

class Debug:
    def __init__(label,info,x,y):
        font = pygame.font.Font(None,30)
        display_surface = pygame.display.get_surface()
        debug_surf = font.render(label + ': ' + str(info),False,'white')
        debug_rect = debug_surf.get_rect(topleft = (x,y))
        pygame.draw.rect(display_surface,'Black',debug_rect)
        display_surface.blit(debug_surf,debug_rect)

    def draw(x,y):
        debugitems = [
            ["Game State",Variables.STATE],
            ["Boss Timer",time.time() - Game_Objects.timer.boss_timer],
            ["Boss Display Msg",boss_state.boss_message_displayed],
            ["Kanas",len(Graphicgroups.kanas)],
            # ["Num pew",len(Graphicgroups.bullets)],
            # ["PlayerXY",Game_Objects.player.location],
            # ["GetReady",boss_state.get_ready_timer],
            # ["Transition",Variables.TRANSITION],
            # ["BossEnd",boss_state.boss_end_state],
            # ["GMSFunc",str(int((Functions.getmaxship()*100)))+"%"],
            # ["TNS",len(Constants.spaceship_surfs)]
        ]
        currentline = y
        for item in debugitems:
            if len(item) == 3: Debug.__init__(item[0],item[1],x,currentline,item[2])
            else: Debug.__init__(item[0],item[1],x,currentline)
            currentline += 20

#region INSTANCING
# Instantiate Classes
intro_state = IntroState()
menu_state = MenuState()
game_state = GameState()
boss_state = BossFight()
gameover_state = GameOverState()
#endregion