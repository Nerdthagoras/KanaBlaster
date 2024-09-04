from sys import exit

import Graphicgroups, Constants, Functions, Game_Objects, Settings, Variables
import os, math, random, time, pygame

class IntroState:
    def __init__(self):
        self.introlength = 0
        self.done = False
        self.boss = False
        self.timer = 0
        self.lt = time.time()

    def manifest(self):
        pass

    def update(self):
        Variables.STATE = "Intro"
        if time.time() - self.lt >= self.introlength: self.done = True # End intro after 'introlength' seconds

    def draw(self,screen):
        pass

    def handle_events(self, events):
        pass

class MenuState:
    def __init__(self):
        self.done = False
        self.boss = False
        self.startbuttonsoundplayed = False
        from Game_Objects import AnimCenterWarning
        Graphicgroups.animcenterwarning.append(AnimCenterWarning("",Constants.spaceship_surfs,Game_Objects.player.type,4,fade=False))
        for _ in range(100): Graphicgroups.starfield_group.add(Game_Objects.Star(0,random.randrange(0,Constants.WIDTH+1000))) # Preload screen full of stars

    def manifest(self):
        Game_Objects.timer.stars(frequency=Settings.star_frequency,velocity=0)                      # Stars Timer
        Game_Objects.timer.allkana()                                                                # All Kana Timer
        Game_Objects.timer.biglaser(enemywaittimer=0)                                               # Big Laser Timer
        Game_Objects.timer.enemy(enemywaittimer=0)                                                  # Enemy Timer

    def update(self):
        Variables.STATE = "Menu"
        pygame.mouse.set_visible(True)
        Variables.maxshiptype = int(len(Constants.spaceship_surfs)*Functions.getmaxship())

        for junk in Graphicgroups.spacejunk: junk.update(Game_Objects.player)                       # RANDOM JUNK
        Graphicgroups.starfield_group.update(Game_Objects.player)                                   # STARS
        Graphicgroups.explosion_group.update()                                                      # EXPLOSION
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
        for epew in Graphicgroups.enemyprojectiles: epew.draw(screen)                               # Enemy Projectiles
        for enemy in Graphicgroups.enemies: enemy.draw(screen,Game_Objects.player)                  # Enemies
        for warning in Graphicgroups.warnings: warning.draw(screen)                                 # Warning for BIG LASER
        for biglaser in Graphicgroups.biglasers: biglaser.draw(screen)                              # BIG LASER
        for wod in Graphicgroups.wallsegments: wod.draw(screen)                                     # Wall of Death
        Graphicgroups.explosion_group.draw(screen)                                                  # EXPLOSION
        for damagenumber in Graphicgroups.damagenumbers: damagenumber.draw(screen)                  # Damage values 
        for centerwarn in Graphicgroups.animcenterwarning: centerwarn.draw()                        # Center Warning
        Functions.kanalist(screen,256)
        
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
        Game_Objects.menu_buttons.startinglevel(screen)                                             # Starting Level
        Game_Objects.menu_buttons.gamemode(screen)                                                  # Game Mode Button
        Game_Objects.menu_buttons.shiptype(screen)                                                  # Ship Type
        Game_Objects.menu_buttons.start(screen)                                                     # Start Button
        #endregion BUTTONS

    def handle_events(self, events):
        for event in events:
            #Click the X to close window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Mouse Events
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Game Mode
                if Game_Objects.menu_buttons.game_mode.collidepoint(event.pos):
                    if Variables.gamemode == 0:
                        Variables.gamemode = 1
                    else:
                        Variables.gamemode = 0

                # start level
                if Game_Objects.menu_buttons.level_number.collidepoint(event.pos) and event.button == 1 or Game_Objects.menu_buttons.level_number.collidepoint(event.pos) and event.button == 4:
                    if Variables.level >= 9:
                        Variables.level = 0
                    else:
                        Variables.level += 1
                elif Game_Objects.menu_buttons.level_number.collidepoint(event.pos) and event.button == 3 or Game_Objects.menu_buttons.level_number.collidepoint(event.pos) and event.button == 5:
                    if Variables.level <= 0:
                        Variables.level = 9
                    else:
                        Variables.level -= 1
                elif Game_Objects.menu_buttons.level_number.collidepoint(event.pos) and event.button == 2: Variables.level = 0

                # Select Ship
                if Game_Objects.menu_buttons.shiptype_number.collidepoint(event.pos) and event.button == 1 or Game_Objects.menu_buttons.shiptype_number.collidepoint(event.pos) and event.button == 4:
                    if Game_Objects.player.type >= Variables.maxshiptype or Game_Objects.player.type >= len(Constants.spaceship_surfs)-1:
                        Game_Objects.player.type = 0
                    else:
                        Game_Objects.player.type +=1
                    from Game_Objects import AnimCenterWarning
                    Graphicgroups.animcenterwarning.clear()
                    Graphicgroups.animcenterwarning.append(AnimCenterWarning("",Constants.spaceship_surfs,Game_Objects.player.type,4,False))
                elif Game_Objects.menu_buttons.shiptype_number.collidepoint(event.pos) and event.button == 3 or Game_Objects.menu_buttons.shiptype_number.collidepoint(event.pos) and event.button == 5:
                    if Game_Objects.player.type <= 0:
                        if Variables.maxshiptype < len(Constants.spaceship_surfs)-1:
                            Game_Objects.player.type = Variables.maxshiptype
                        else:
                            Game_Objects.player.type = len(Constants.spaceship_surfs)-1
                    else:
                        Game_Objects.player.type -= 1
                    from Game_Objects import AnimCenterWarning
                    Graphicgroups.animcenterwarning.clear()
                    Graphicgroups.animcenterwarning.append(AnimCenterWarning("",Constants.spaceship_surfs,Game_Objects.player.type,4,False))
                elif Game_Objects.menu_buttons.shiptype_number.collidepoint(event.pos) and event.button == 2: 
                    Game_Objects.player.type = 0
                    from Game_Objects import AnimCenterWarning
                    Graphicgroups.animcenterwarning.clear()
                    Graphicgroups.animcenterwarning.append(AnimCenterWarning("",Constants.spaceship_surfs,Game_Objects.player.type,4,False))

                #start
                if Game_Objects.menu_buttons.start_button.collidepoint(event.pos):
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
                # if event.key == pygame.K_SPACE:
                #     Functions.reset_game()
                #     game_state.enemy_wait_timer = 10
                #     gameover_state.done = False
                #     game_state.done = False
                #     boss_state.done = False
                #     self.done = True
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
                Game_Objects.timer.WoD_timer = 0
                Game_Objects.timer.incorrectkana_timer = 0
                Game_Objects.timer.junk_timer = 0
                Game_Objects.timer.correctkana_timer = 0
                Game_Objects.timer.biglaser_timer = 0
                Game_Objects.timer.enemy_timer = 0
                Game_Objects.timer.powerup_timer = 0
                Game_Objects.timer.bridge_timer = 0
                Game_Objects.timer.boss_message_timer = 0
                Game_Objects.timer.bonus_timer = 0
                Game_Objects.timer.boss_timer = 0
                Game_Objects.timer.boss_message_displayed = False

            Variables.musicvolume -= 0.05 * Variables.delta_time
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
        if Game_Objects.player.lives <= 0:
            Functions.write_csv('data/userkana.csv',Variables.commasep) # Write your progress to a CSV file
            self.done = True
        #endregion

    def update(self):
        Variables.STATE = "Game"
        self.boss = Variables.GAMESTATE
        Game_Objects.achievements.tingtang()
        self.gamefadeouttoboss()
        self.warningmessages()
        self.lives()

        if self.enemy_wait_timer >= 0: self.enemy_wait_timer -= 1 * Variables.delta_time        #Stop enemies from showing up right at the start

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
        for powerup in Graphicgroups.animatedpowerup: powerup.update()                  # Powerups
        for centerwarn in Graphicgroups.centerwarning: centerwarn.update()              # UI
        Game_Objects.player.update()                                                    # Player

    def draw(self,screen):
        pygame.mouse.set_visible(False)
        # region SCREEN
        if time.time() - self.bgfade_timer >= 0.001:
            if Variables.RGB[0] > 10: Variables.RGB[0] -= 500 * Variables.delta_time
            else: Variables.RGB[0] = 0
            if Variables.RGB[1] > 10: Variables.RGB[1] -= 500 * Variables.delta_time
            else: Variables.RGB[1] = 0
            if Variables.RGB[2] > 10: Variables.RGB[2] -= 500 * Variables.delta_time
            else: Variables.RGB[2] = 0
            self.bgfade_timer = time.time()
        try: screen.fill((Variables.RGB[0],Variables.RGB[1],Variables.RGB[2]))
        except: pass
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
        Functions.kanalist(screen,128)

        if Variables.debugwindow: Debug.draw(Constants.debug_locationx,Constants.debug_locationy)   # DEBUG

    def handle_events(self, events):
        for event in events:
            # Click the X to close window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # KEYDOWN
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: Game_Objects.player.lives = 0
                Functions.sharedcontrols(event)

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
        # Game_Objects.timer.wallofdeath()                                        # Wall of Death Timer

    def decreasebonus(self):
        #region decrement bonus score every half second
        if time.time() - self.bonus_timer >= 1 and len(Graphicgroups.bosses) > 0:
            if self.bonus_score > 0: self.bonus_score -= 1
            self.bonus_timer = time.time()
        #endregion decrement bonus score every half second

    def bosstransitionout(self):
        #region Fade out music and transition back to Game
        if Variables.TRANSITION == False and self.boss_end_state == "musicfade":
            if Variables.musicvolume <= 0:
                self.boss_end_state = "bonusadd"
            Variables.musicvolume -= 0.05 * Variables.delta_time
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
                Variables.musicvolume = Settings.maxmusicvolume                    # Set Music Volume Back to Default
                self.bonus_score = Settings.boss_bonus_score
                self.get_ready_timer = Settings.get_ready_timer_max

                # Reset Timers
                Game_Objects.timer.WoD_timer = 0
                Game_Objects.timer.incorrectkana_timer = 0
                Game_Objects.timer.junk_timer = 0
                Game_Objects.timer.correctkana_timer = 0
                Game_Objects.timer.biglaser_timer = 0
                Game_Objects.timer.enemy_timer = 0
                Game_Objects.timer.powerup_timer = 0
                Game_Objects.timer.bridge_timer = 0

            else: self.get_ready_timer -= Variables.delta_time
        #endregion Rest period before re-entering game

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
        if Game_Objects.player.lives <= 0:
            Functions.write_csv('data/userkana.csv',Variables.commasep) # Write your progress to a CSV file
            self.done = True
        #endregion

    def update(self):
        Variables.STATE = "Boss"
        self.boss = Variables.BOSSSTATE
        self.bosstransitionout()
        self.warningmessages()
        self.decreasebonus()
        self.lives()

        if self.enemy_wait_timer >= 0: self.enemy_wait_timer -= 1 * Variables.delta_time        # Stop enemies from showing up right at the start

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
        for powerup in Graphicgroups.animatedpowerup: powerup.update()                  # Powerups
        for centerwarn in Graphicgroups.centerwarning: centerwarn.update()              # UI
        Graphicgroups.bridge_group.update(Game_Objects.player)                          # BRIDGE WIPE
        Graphicgroups.tip_group.update()                                                # Tip Ticker

    def draw(self,screen):
        pygame.mouse.set_visible(False)
        # region SCREEN
        if time.time() - self.bgfade_timer >= 0.001:
            if Variables.RGB[0] > 10: Variables.RGB[0] -= 500 * Variables.delta_time
            else: Variables.RGB[0] = 0
            if Variables.RGB[1] > 10: Variables.RGB[1] -= 500 * Variables.delta_time
            else: Variables.RGB[1] = 0
            if Variables.RGB[2] > 10: Variables.RGB[2] -= 500 * Variables.delta_time
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

    def handle_events(self, events):
        for event in events:
            # Click the X to close window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # KEYDOWN
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: Game_Objects.player.lives = 0
                Functions.sharedcontrols(event)

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
        Game_Objects.timer.allkana()                                                    # All Kana Timer

    def update(self):
        Variables.STATE = "GameOver"
        Game_Objects.player.shipcollision = False
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
        for wod in Graphicgroups.wallsegments: wod.update()                             # Wall of Death
        for brick in Graphicgroups.bricks: brick.update()                               # Brick debris
        for centerwarn in Graphicgroups.centerwarning: centerwarn.update()              # UI
        Graphicgroups.bridge_group.update(Game_Objects.player)                          # BRIDGE WIPE
        for powerup in Graphicgroups.animatedpowerup: powerup.update()                  # Powerups

    def draw(self,screen):
        screen.fill(('black'))

        Graphicgroups.planet_group.draw(screen)                                         # PLANETS
        for junk in Graphicgroups.spacejunk: junk.draw(screen)                          # RANDOM JUNK
        Graphicgroups.starfield_group.draw(screen)                                      # STARS
        for warning in Graphicgroups.warnings: warning.draw(screen)                     # WARNING for BIG LASER
        for bullet in Graphicgroups.bullets: bullet.draw(screen)                        # BULLETS
        for cutoff in Graphicgroups.cuttoffline: cutoff.draw(screen)                    # CUTOFF LINE
        for epew in Graphicgroups.enemyprojectiles: epew.draw(screen)                   # ENEMY PEW
        for enemy in Graphicgroups.enemies: enemy.draw(screen,Game_Objects.player)      # ENEMIES
        for kana in Graphicgroups.correctkanas: kana.draw(screen)                       # CORRECT KANA
        for kana in Graphicgroups.kanas: kana.draw(screen)                              # WRONG KANA
        for powerup in Graphicgroups.animatedpowerup: powerup.draw(screen)              # Powerup
        for biglaser in Graphicgroups.biglasers: biglaser.draw(screen)                  # BIG LASER
        for wod in Graphicgroups.wallsegments: wod.draw(screen)                         # Wall of Death
        for brick in Graphicgroups.bricks: brick.draw(screen)                           # Brick debirs
        #region EXPLOSION                                                               # EXPLOSION
        Graphicgroups.explosion_group.draw(screen)
        Graphicgroups.explosion_group.update()
        #endregion
        #region QUESTION TEXT                                                           # QUESTION TEXT
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
        #region UI TEXT                                                                 # UI TEXT
        if Variables.score <=0: Variables.score = 0
        scoretext = Constants.ui_font.render("Score: " + str(Variables.score), True, 'white')
        screen.blit(scoretext, (Constants.WIDTH-200, 10))

        livestext = Constants.ui_font.render("Lives: " + str(Game_Objects.player.lives), True, 'white')
        screen.blit(livestext, (Constants.WIDTH-400, 10))

        leveltext = Constants.ui_font.render("Level: " + str(Variables.level), True, 'white')
        screen.blit(leveltext, (Constants.WIDTH-600, 10))

        for centerwarn in Graphicgroups.centerwarning:
            centerwarn.draw()
        #endregion
        Graphicgroups.bridge_group.draw(screen)                                         # BRIDGE WIPE

        #region DEBUG                                                                   # DEBUG
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
                    Game_Objects.player.lives = Settings.maxlives
                    menu_state.done = False
                    game_state.done = False
                    self.done = True
                if event.key == pygame.K_SPACE:
                    Game_Objects.player.movex, Game_Objects.player.movey = 0,0
                    Game_Objects.player.pullback = 1.5
                    Game_Objects.player.lives = Settings.maxlives
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
            ["Menu Kana Timer",round(Game_Objects.timer.kana_frequency - Game_Objects.timer.kana_timer,1)],
            ["Star Timer",round(Game_Objects.timer.star_frequency - Game_Objects.timer.star_timer,1)],
            ["BigLaser Timer",round(Game_Objects.timer.biglaser_randomness - Game_Objects.timer.biglaser_timer)],
            ["Enemy Timer",round(Game_Objects.timer.enemy_randomness - Game_Objects.timer.enemy_timer)],
            ["Boss Timer",round(Game_Objects.timer.boss_delay - Game_Objects.timer.boss_timer)],
            ["IK Timer",round(Game_Objects.timer.incorrectkana_thresh - Game_Objects.timer.incorrectkana_timer)],
            ["CK Timer",round(Game_Objects.timer.correctkana_thresh - Game_Objects.timer.correctkana_timer)],
            ["Bridge Timer",round(Game_Objects.timer.bridge_thresh - Game_Objects.timer.bridge_timer)],
            ["Planet Timer",round(Game_Objects.timer.planet_thresh - Game_Objects.timer.planet_timer)],
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