from sys import exit

import Graphicgroups, CONST, Functions, Game_Objects, Settings, Variables
import os, random, time, pygame

#region INTRO STATE
class IntroState:
    def __init__(self):
        pygame.mixer.music.load(os.path.join('music','DefendingTheirWorld.wav'))
        pygame.mixer.music.play(0)
        self.introlength = 0
        self.done = False
        self.boss = False

        # Star Wars Scroll Test
        Surf_Width, Surf_Height = 900, 3200
        SWOrange = (255,200,0)
        Text_delay_offset = 100
        self.SWSurface = pygame.Surface((Surf_Width, Surf_Height)).convert_alpha()
        self.SWSurface.fill((0,0,0,0))
        TITLE_text = CONST.STARWARS_TITLE_FONT.render('KANA BLASTER', True, SWOrange)
        TITLE_shadow_text = CONST.STARWARS_TITLE_FONT.render('KANA BLASTER', True, SWOrange)
        TITLE_shadow_text.set_alpha(128)
        Title_rect = TITLE_text.get_rect(center = (0, 0))
        self.SWSurface.blit(TITLE_shadow_text, ((Title_rect[0]+Surf_Width//2, Text_delay_offset+10)))
        self.SWSurface.blit(TITLE_text, (Title_rect[0]+Surf_Width//2, Text_delay_offset))
        # text = "According to all known laws of aviation, there is no way that a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible.\n\n\nCut to Barry's room, where he's picking out what to wear.\n\n\nYellow, black. Yellow, black. Yellow, black. Yellow, black. Ooh, black and yellow! Yeah, let's shake it up a little.\n\nBarry uses honey from a dispenser to style his hair, rinse his mouth, and then applies it to his armpits."
        text = "You seek company with the emperor of the Galaxy, but before you do, you have been tasked with writing a letter of proof of your love.\n\nThroughout the galaxy a vast array of characters have been scattered and you are to collect the correct characters in each of the zones.\n\nAs further proof of your devotion to the Galaxy's finest entity you are to learn which symbols are required by first observing their phonetics in your common language.\n\nAt first you will be guided by the colouring of what is required and which should be disposed of, but as you correctly collect enough of any character, you will have to rely on the memory of thier shape as their colour will have been washed out.\n\nBeware, for it seems you are not the only one that seeks the company of the emperor, others have been summoned to give resistance to your task, and will only get more intense as you continue.\n\nYes, they do resemble Earth Japanese, but I assure you this is just a weird coincidence."
        Functions.display_text(
            surface=self.SWSurface,
            text=text,
            pos=(0,Text_delay_offset+250),
            linespacing=15,
            font=CONST.STARWARS_FONT,
            color=SWOrange
        )


        for i in range(200):
            x = 0
            height = 4
            width = 2
            Graphicgroups.starwarsscroll.append(Game_Objects.StarWarsScroll(
                image=self.SWSurface,
                x=x+(i*10//(width*2)),
                y=CONST.HEIGHT-(i*height),
                width=CONST.WIDTH-(i*10//width),
                height=height,
                speed=20,
                ix=0,
                iy=height,
                offset=i,
                fade=1.4
            ))

    def manifest(self):
        Game_Objects.timer.stars(frequency=Settings.star_frequency,velocity=0)                      # Stars Timer

    def update(self):
        Graphicgroups.starfield_group.update(Game_Objects.player)                                   # STARS
        for segment in Graphicgroups.starwarsscroll: segment.update()                               # STARWARS

    def draw(self,screen):
        screen.fill(('black'))                                                                      # Refresh screen
        Graphicgroups.starfield_group.draw(screen)                                                  # STARS
        for segment in Graphicgroups.starwarsscroll: segment.draw(screen)                           # STARWARS

    def handle_events(self, events):
        if not pygame.mixer.music.get_busy(): self.done = True
        for event in events:
            #Click the X to close window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            # KEYDOWN
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: self.done = True




#region MENU STATE
class MenuState:
    def __init__(self):
        self.done = False
        self.boss = False
        self.startbuttonsoundplayed = False
        from Game_Objects import AnimCenterWarning
        Graphicgroups.animcenterwarning.append(AnimCenterWarning("",CONST.SURF_SPACESHIP,Game_Objects.player.type,4,fade=False))
        for _ in range(100): Graphicgroups.starfield_group.add(Game_Objects.Star(0,random.randrange(0,CONST.WIDTH+1000))) # Preload screen full of stars

    def manifest(self):
        Game_Objects.timer.stars(frequency=Settings.star_frequency,velocity=0)                      # Stars Timer
        Game_Objects.timer.allkana()                                                                # All Kana Timer
        Game_Objects.timer.biglaser(enemywaittimer=0)                                               # Big Laser Timer
        Game_Objects.timer.enemy(enemywaittimer=0)                                                  # Enemy Timer
        Game_Objects.timer.scenery()

    def update(self):
        Variables.current_game_state = "Menu"
        pygame.mouse.set_visible(True)
        Variables.maxshiptype = int(len(CONST.SURF_SPACESHIP)*Functions.getmaxship())

        for junk in Graphicgroups.spacejunk: junk.update(Game_Objects.player)                       # RANDOM JUNK
        Graphicgroups.starfield_group.update(Game_Objects.player)                                   # STARS
        Graphicgroups.explosion_group.update()                                                      # EXPLOSION
        for kana in Graphicgroups.incorrectkanas:  kana.update(Game_Objects.player)                          # Kana
        for bullet in Graphicgroups.enemymissiles: bullet.update()                                  # Enemy Missiles
        for warning in Graphicgroups.warnings: warning.update()                                     # Warning for BIG LASER
        for biglaser in Graphicgroups.biglasers: biglaser.update()                                  # BIG LASER
        for enemy in Graphicgroups.enemies: enemy.update();enemy.shoot(Game_Objects.player)         # Enemies
        for epew in Graphicgroups.enemyprojectiles: epew.update()                                   # Enemy Projectiles
        for wod in Graphicgroups.wallsegments: wod.update()                                         # Wall of Death
        for centerwarn in Graphicgroups.animcenterwarning: centerwarn.update()                      # Center Warning
        for powerup in Graphicgroups.animatedpowerup: powerup.update()                              # Powerups
        for segment in Graphicgroups.scenery: segment.update()
        for turret in Graphicgroups.turrets: turret.update()

    def draw(self,screen):
        # Must be in order of Top/Bottom = Background/Foreground
        screen.fill(('black'))                                                                      # Refresh screen

        for junk in Graphicgroups.spacejunk: junk.draw(screen)                                      # RANDOM JUNK
        Graphicgroups.starfield_group.draw(screen)                                                  # STARS
        for kana in Graphicgroups.incorrectkanas: kana.draw(screen)                                          # Kana
        for epew in Graphicgroups.enemyprojectiles: epew.draw(screen)                               # Enemy Projectiles
        for enemy in Graphicgroups.enemies: enemy.draw(screen,Game_Objects.player)                  # Enemies
        for bullet in Graphicgroups.enemymissiles: bullet.draw(screen)                              # Enemy Missiles
        for warning in Graphicgroups.warnings: warning.draw(screen)                                 # Warning for BIG LASER
        for biglaser in Graphicgroups.biglasers: biglaser.draw(screen)                              # BIG LASER
        for powerup in Graphicgroups.animatedpowerup: powerup.draw(screen)                          # Powerups
        for wod in Graphicgroups.wallsegments: wod.draw(screen)                                     # Wall of Death
        Graphicgroups.explosion_group.draw(screen)                                                  # EXPLOSION
        for damagenumber in Graphicgroups.damagenumbers: damagenumber.draw(screen)                  # Damage values 
        for centerwarn in Graphicgroups.animcenterwarning: centerwarn.draw()                        # Center Warning
        for turret in Graphicgroups.turrets: turret.draw(screen)
        for segment in Graphicgroups.scenery: segment.draw(screen)
        Functions.kanalist(screen,256)
        
        if Variables.debugwindow: Debug.draw(CONST.DEBUG_LOC_X,CONST.DEBUG_LOC_Y)   # DEBUG

        #region Game Title
        TITLE_text = CONST.GAME_OVER_FONT.render('KANA BLASTER', True, 'white')
        screen.blit(TITLE_text, (10, CONST.PAHEIGHT/7))
        TITLE_shadow_text = CONST.GAME_OVER_FONT.render('KANA BLASTER', True, 'white')
        TITLE_shadow_text.set_alpha(100)
        offset = 8
        screen.blit(TITLE_shadow_text, (10+offset, CONST.PAHEIGHT/7+offset))

        ship_num_shadow = CONST.UI_FONT.render(str(Game_Objects.player.type+1) + '/' + str(Variables.maxshiptype+1), True, 'black')
        ship_num_shadow_rect = ship_num_shadow.get_rect(center=(CONST.WCENTER+15,CONST.HCENTER+5))
        ship_num_shadow.set_alpha(128)
        ship_num = CONST.UI_FONT.render(str(Game_Objects.player.type+1) + '/' + str(Variables.maxshiptype+1), True, 'white')
        ship_num_rect = ship_num.get_rect(center=(CONST.WCENTER+10,CONST.HCENTER))
        CONST.SCREEN.blit(ship_num_shadow,ship_num_shadow_rect)   
        CONST.SCREEN.blit(ship_num,ship_num_rect)
        #endregion Game Title





        #region Buttons
        # Starting Level
        Game_Objects.menu_buttons.startinglevel(screen,x=-500,y=0)                                            # Starting Level
        Game_Objects.menu_buttons.gamemode(screen,x=400,y=0)                                                  # Game Mode Button
        Game_Objects.menu_buttons.start(screen,x=0,y=200)                                                     # Start Button
        #endregion BUTTONS

    def handle_events(self, events):
        for event in events:
            #Click the X to close window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            #region Mouse Events




            if event.type == pygame.MOUSEBUTTONDOWN:
                #region Game Mode
                if Game_Objects.menu_buttons.game_mode_button_rect.collidepoint(event.pos):
                    if Variables.gamemode == 0:
                        Variables.gamemode = 1
                    else:
                        Variables.gamemode = 0




                #region start level
                if Game_Objects.menu_buttons.startinglevel_rect.collidepoint(event.pos) and event.button == 1 or Game_Objects.menu_buttons.startinglevel_rect.collidepoint(event.pos) and event.button == 4:
                    if Variables.level >= 9:
                        Variables.level = 0
                    else:
                        Variables.level += 1
                elif Game_Objects.menu_buttons.startinglevel_rect.collidepoint(event.pos) and event.button == 3 or Game_Objects.menu_buttons.startinglevel_rect.collidepoint(event.pos) and event.button == 5:
                    if Variables.level <= 0:
                        Variables.level = 9
                    else:
                        Variables.level -= 1
                elif Game_Objects.menu_buttons.startinglevel_rect.collidepoint(event.pos) and event.button == 2: Variables.level = 0


                #region Select Ship
                if Graphicgroups.animcenterwarning[0].centered_image.collidepoint(event.pos) and event.button == 1:
                    if Game_Objects.player.type >= Variables.maxshiptype or Game_Objects.player.type >= len(CONST.SURF_SPACESHIP)-1:
                        Game_Objects.player.type = 0
                    else:
                        Game_Objects.player.type +=1
                    from Game_Objects import AnimCenterWarning
                    Graphicgroups.animcenterwarning.clear()
                    Graphicgroups.animcenterwarning.append(AnimCenterWarning("",CONST.SURF_SPACESHIP,Game_Objects.player.type,4,False))
                elif Graphicgroups.animcenterwarning[0].centered_image.collidepoint(event.pos) and event.button == 3:
                    if Game_Objects.player.type <= 0:
                        if Variables.maxshiptype < len(CONST.SURF_SPACESHIP)-1:
                            Game_Objects.player.type = Variables.maxshiptype
                        else:
                            Game_Objects.player.type = len(CONST.SURF_SPACESHIP)-1
                    else:
                        Game_Objects.player.type -= 1
                    from Game_Objects import AnimCenterWarning
                    Graphicgroups.animcenterwarning.clear()
                    Graphicgroups.animcenterwarning.append(AnimCenterWarning("",CONST.SURF_SPACESHIP,Game_Objects.player.type,4,False))
                elif Graphicgroups.animcenterwarning[0].centered_image.collidepoint(event.pos) and event.button == 2:
                    Game_Objects.player.type = 0
                    from Game_Objects import AnimCenterWarning
                    Graphicgroups.animcenterwarning.clear()
                    Graphicgroups.animcenterwarning.append(AnimCenterWarning("",CONST.SURF_SPACESHIP,Game_Objects.player.type,4,False))



                #region start game
                if Game_Objects.menu_buttons.start_button_rect.collidepoint(event.pos):
                    Functions.reset_game()
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
                    for h in range(int(CONST.PAHEIGHT/32)):
                        Game_Objects.WallOfDeath.spawn(CONST.WIDTH,h*32)
                if event.key == ord('f'): pygame.display.toggle_fullscreen()
                if event.key == ord('e'): Game_Objects.Enemies.spawn()
                if event.key == ord('r'): Game_Objects.BigLaserWarning.spawn(Game_Objects.player)
                if event.key == ord('0'):
                    try: os.remove('data/userkana.csv')
                    except: pass
                if event.key == ord('g'):
                    Game_Objects.BorderScenery(Variables.scenerytype).picknext()
                if event.key == ord('u'):
                    powerup_type = random.randint(1,2)
                    Game_Objects.AnimatedPowerUp.spawn(
                        CONST.ARRAY_POWERUP[powerup_type]["xvel"],
                        CONST.ARRAY_POWERUP[powerup_type]["surfindx"],
                        CONST.ARRAY_POWERUP[powerup_type]["pueffect"],
                        )
                if event.key == ord('t'):
                    Graphicgroups.turrets.append(Game_Objects.GroundTurret(CONST.WIDTH+32,CONST.PAHEIGHT-64,0))




#region GAME STATE
class GameState:
    def __init__(self):
        self.done = False
        self.boss = Variables.gamestate
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
        Game_Objects.timer.weaponupgrade()                                                  # Weapon Upgrade Timer
        Game_Objects.timer.bridge(frequency=30)                                             # Bridge Timer
        Game_Objects.timer.scenery(frequency=Variables.scenerywaittime)                     # Scenery

    def gamefadeouttoboss(self):
        #region Fade out music and transition to Boss
        if Variables.transition == True: # Start the Music Fade
            if Variables.musicvolume <= 0:
                Variables.bossstate = False
                Variables.gamestate = True
                Variables.bossexist = False
                boss_state.boss_message_displayed = False
                boss_state.get_ready_timer = Settings.get_ready_timer_max

                # Clear Group Arrays
                Graphicgroups.cuttoffline.clear()

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

                # Reset Kananum
                Variables.kananum = 0

            Variables.musicvolume -= 0.05 * Variables.delta_time
        #endregion Fade out music and transition to Boss

    def warningmessages(self):
        if Variables.level == Settings.enemy_start_level and self.prev_level < Settings.enemy_start_level:
            Game_Objects.CenterWarning.spawn('Enemies Active',CONST.SURF_ENEMY[0].images[0],3)
            self.enemy_wait_timer = 3
            self.prev_level = Settings.enemy_start_level
        if Variables.level == Settings.biglaser_start_level and self.prev_level < Settings.biglaser_start_level:
            Game_Objects.CenterWarning.spawn('Big Laser Active',CONST.SURF_BIG_LASER[0].images[0])
            self.enemy_wait_timer = 3
            self.prev_level = Settings.biglaser_start_level

    def lives(self):
        #region Extra Life
        if Variables.score >= self.extralife:
            Game_Objects.AnimatedPowerUp.spawn(
                CONST.ARRAY_POWERUP[0]["xvel"],
                CONST.ARRAY_POWERUP[0]["surfindx"],
                CONST.ARRAY_POWERUP[0]["pueffect"],
                )
            self.extralife += Settings.ship_extra_life_increment
        #endregion

        #region You lost all of your lives
        if Game_Objects.player.lives <= 0:
            Functions.write_csv('data/userkana.csv',Variables.commasep) # Write your progress to a CSV file
            self.done = True
        #endregion

    def update(self):
        Variables.current_game_state = "Game"
        self.boss = Variables.gamestate
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
        for bullet in Graphicgroups.missiles: bullet.update()                           # Missiles
        for bullet in Graphicgroups.enemymissiles: bullet.update()
        for pew in Graphicgroups.dynamicpew: pew.update()                               # Big Pew
        for biglaser in Graphicgroups.biglasers: biglaser.update()                      # BIG LASER
        for junk in Graphicgroups.spacejunk: junk.update()                              # RANDOM JUNK
        for cutoff in Graphicgroups.cuttoffline: cutoff.update(Game_Objects.player)     # CUTOFF LINE
        for kana in Graphicgroups.correctkanas: kana.update(Game_Objects.player)        # Correct Kanas
        for kana in Graphicgroups.incorrectkanas: kana.update(Game_Objects.player)               # Incorrect kanas
        for kana in Graphicgroups.bossmodecorrectkana: kana.update(Game_Objects.player)
        for kana in Graphicgroups.bossmodeincorrectkana: kana.update(Game_Objects.player)
        for warning in Graphicgroups.warnings: warning.update()                         # Big Laser Warning
        for epew in Graphicgroups.enemyprojectiles: epew.update()                       # Enemy Projectiles
        for enemy in Graphicgroups.enemies: enemy.update()                              # ENEMIES
        for wod in Graphicgroups.wallsegments: wod.update()                             # Wall of Death
        for brick in Graphicgroups.bricks: brick.update()                               # Brick debris
        for bits in Graphicgroups.debris: bits.update()                                 # Debris
        for powerup in Graphicgroups.animatedpowerup: powerup.update()                  # Powerups
        for centerwarn in Graphicgroups.centerwarning: centerwarn.update()              # UI
        for crosshair in Graphicgroups.crosshair: crosshair.update()                    # Crosshair
        for brew in Graphicgroups.brew: brew.update()
        for segment in Graphicgroups.scenery: segment.update()
        for turret in Graphicgroups.turrets: turret.update()
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
        for bullet in Graphicgroups.missiles: bullet.draw(screen)                       # Missiles
        for bullet in Graphicgroups.enemymissiles: bullet.draw(screen)                  # Enemy Missiles
        for pew in Graphicgroups.dynamicpew: pew.draw(screen)                           # Big Pew
        for cutoff in Graphicgroups.cuttoffline: cutoff.draw(screen)                    # CUTOFF LINE
        for epew in Graphicgroups.enemyprojectiles: epew.draw(screen)                   # ENEMY PEW
        for bits in Graphicgroups.debris: bits.draw(screen)                             # Bits debris
        for enemy in Graphicgroups.enemies: enemy.draw(screen,Game_Objects.player)      # ENEMIES
        for kana in Graphicgroups.correctkanas: kana.draw(screen)                       # CORRECT KANA
        for kana in Graphicgroups.incorrectkanas: kana.draw(screen)                     # WRONG KANA
        for kana in Graphicgroups.bossmodecorrectkana: kana.draw(screen)
        for kana in Graphicgroups.bossmodeincorrectkana: kana.draw(screen)
        for brew in Graphicgroups.brew: brew.draw(screen)
        Game_Objects.player.draw(screen)                                                # PLAYER
        for powerup in Graphicgroups.animatedpowerup: powerup.draw(screen)              # Powerup
        for biglaser in Graphicgroups.biglasers: biglaser.draw(screen)                  # BIG LASER
        for wod in Graphicgroups.wallsegments: wod.draw(screen)                         # Wall of Death
        for brick in Graphicgroups.bricks: brick.draw(screen)                           # Brick debirs
        for shield in Graphicgroups.shields: shield.draw(screen)                        # Shields
        for damagenumber in Graphicgroups.damagenumbers: damagenumber.draw(screen)      # Damage values 
        Graphicgroups.explosion_group.draw(screen)                                      # EXPLOSION
        for crosshair in Graphicgroups.crosshair: crosshair.draw(screen)                # Crosshair
        Functions.question_text(screen)                                                 # QUESTION TEXT
        Functions.uitext(screen)                                                        # UI TEXT
        Graphicgroups.bridge_group.draw(screen)                                         # BRIDGE WIPE
        Graphicgroups.tip_group.draw(screen)                                            # Tip Ticker
        for centerwarn in Graphicgroups.centerwarning: centerwarn.draw()                # Center Warning Text
        for turret in Graphicgroups.turrets: turret.draw(screen)
        for segment in Graphicgroups.scenery: segment.draw(screen)
        Functions.kanalist(screen,128)

        if Variables.debugwindow: Debug.draw(CONST.DEBUG_LOC_X,CONST.DEBUG_LOC_Y)   # DEBUG

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




#region BOSS STATE
class BossFight:
    def __init__(self):
        self.done = False
        self.boss = Variables.bossstate
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
        # kanakill = int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3])*(255/Settings.num_to_shoot_new_kana)

        Game_Objects.timer.bossmessage(delay=0)                                 # Boss Message Timer
        Game_Objects.timer.boss(delay=3)                                        # Boss Timer
        Game_Objects.timer.stars(frequency=0.04,velocity=600)                   # Stars Timer
        Game_Objects.timer.biglaser(enemywaittimer=self.enemy_wait_timer)       # Big Laser Timer
        Game_Objects.timer.planet()                                             # PLANET Timer
        Game_Objects.timer.junk()                                               # JUNK Timer
        if CONST.ARRAY_BOSSES[Variables.level]["shield"] > 0:
            Game_Objects.timer.bosskana(frequency=10)                           # Boss Kana
        # Game_Objects.timer.scenery(frequency=.5)
        # Game_Objects.timer.wallofdeath()                                        # Wall of Death Timer

    def decreasebonus(self):
        #region decrement bonus score every half second
        if time.time() - self.bonus_timer >= 1 and len(Graphicgroups.bosses) > 0:
            if self.bonus_score > 0: self.bonus_score -= 1
            self.bonus_timer = time.time()
        #endregion decrement bonus score every half second

    def bosstransitionout(self):
        #region Fade out music and transition back to Game
        if Variables.transition == False and self.boss_end_state == "musicfade":
            if Variables.musicvolume <= 0:
                self.boss_end_state = "bonusadd"
            Variables.musicvolume -= 0.05 * Variables.delta_time
        #endregion Fade out music and transition back to Game

        #region add bonus to score
        if Variables.transition == False and self.boss_end_state == "bonusadd":
            if self.bonus_score <= 0:
                self.boss_end_state = "getready"
                self.get_ready_timer = Settings.get_ready_timer_max
            else:
                if time.time() - self.bonus_timer >= 0.05:
                    self.bonus_score -= 1
                    Variables.score += 1
                    pygame.mixer.Sound.play(CONST.SOUND_CORRECT_KANA_LOSING)
                    self.bonus_timer = time.time()
        #endregion add bonus to score

        #region Rest period before re-entering game
        if Variables.transition == False and self.boss_end_state == "getready":
            if self.get_ready_timer <= 0:
                self.boss_end_state = "musicfade"                                   # Reset Transistion state to beginning (musicfade)
                Variables.gamestate = False
                Variables.bossstate = True
                Variables.level += 1                                                # Increase Level
                Variables.musicvolume = Settings.maxmusicvolume                    # Set Music Volume Back to Default
                Variables.kananum = 0
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

                # Clear Graphic Groups
                Graphicgroups.bossmodecorrectkana.clear()
                Graphicgroups.bossmodeincorrectkana.clear()

            else: self.get_ready_timer -= Variables.delta_time
        #endregion Rest period before re-entering game

    def warningmessages(self):
        if Variables.level == Settings.enemy_start_level and self.prev_level < Settings.enemy_start_level:
            Game_Objects.CenterWarning.spawn('Enemies Active',CONST.SURF_ENEMY[0].images[0],3)
            self.enemy_wait_timer = 3
            self.prev_level = Settings.enemy_start_level
        if Variables.level == Settings.biglaser_start_level and self.prev_level < Settings.biglaser_start_level:
            Game_Objects.CenterWarning.spawn('Big Laser Active',CONST.SURF_BIG_LASER[0].images[0])
            self.enemy_wait_timer = 3
            self.prev_level = Settings.biglaser_start_level

    def lives(self):
        #region Extra Life
        if Variables.score >= self.extralife:
            Game_Objects.AnimatedPowerUp.spawn(
                CONST.ARRAY_POWERUP[0]["xvel"],
                CONST.ARRAY_POWERUP[0]["surfindx"],
                CONST.ARRAY_POWERUP[0]["pueffect"],
                )
            self.extralife += Settings.ship_extra_life_increment
        #endregion

        #region You lost all of your lives
        if Game_Objects.player.lives <= 0:
            Functions.write_csv('data/userkana.csv',Variables.commasep) # Write your progress to a CSV file
            self.done = True
        #endregion

    def update(self):
        Variables.current_game_state = "Boss"
        self.boss = Variables.bossstate
        self.bosstransitionout()
        self.warningmessages()
        self.decreasebonus()
        self.lives()

        if self.enemy_wait_timer >= 0: self.enemy_wait_timer -= 1 * Variables.delta_time        # Stop enemies from showing up right at the start

        for bullet in Graphicgroups.bullets: bullet.update()                            # BULLETS
        for bullet in Graphicgroups.missiles: bullet.update()                           # Missiles
        for pew in Graphicgroups.dynamicpew: pew.update()                               # Big Pew
        for biglaser in Graphicgroups.biglasers: biglaser.update()                      # BIG LASER
        Graphicgroups.planet_group.update(Game_Objects.player)                          # PLANETS
        for junk in Graphicgroups.spacejunk: junk.update()                              # RANDOM JUNK
        Graphicgroups.starfield_group.update(Game_Objects.player)                       # STARS
        for cutoff in Graphicgroups.cuttoffline: cutoff.update(Game_Objects.player)     # CUTOFF LINE
        for kana in Graphicgroups.correctkanas: kana.update(Game_Objects.player)        # Correct Kanas
        for kana in Graphicgroups.incorrectkanas: kana.update(Game_Objects.player)               # Incorrect kanas
        for kana in Graphicgroups.bossmodecorrectkana: kana.update(Game_Objects.player)
        for kana in Graphicgroups.bossmodeincorrectkana: kana.update(Game_Objects.player)
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
        for brew in Graphicgroups.brew: brew.update()
        Graphicgroups.tip_group.update()                                                # Tip Ticker
        for segment in Graphicgroups.scenery: segment.update()
        for turret in Graphicgroups.turrets: turret.update()

    def draw(self,screen):
        pygame.mouse.set_visible(False)
        # region Screen
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

        #region Kana List
        for f in range(int(Variables.levels[Variables.level])): Graphicgroups.kanalist.append(Variables.commasep[f])
        for f in range(int(Variables.levels[Variables.level])):
            if Variables.gamemode == 0: kanalistthing = CONST.UI_FONT.render(Graphicgroups.kanalist[f][0], True, (20,20,20))
            else: kanalistthing = CONST.UI_FONT.render(Graphicgroups.kanalist[f][1], True, (20,20,20))
            screen.blit(kanalistthing,(25+(27*f),CONST.PAHEIGHT-30))
        #endregion

        Graphicgroups.planet_group.draw(screen)                                         # PLANETS
        for junk in Graphicgroups.spacejunk: junk.draw(screen)                          # RANDOM JUNK
        Graphicgroups.starfield_group.draw(screen)                                      # STARS
        for warning in Graphicgroups.warnings: warning.draw(screen)                     # WARNING for BIG LASER
        for bullet in Graphicgroups.bullets: bullet.draw(screen)                        # BULLETS
        for bullet in Graphicgroups.missiles: bullet.draw(screen)                       # Missiles
        for pew in Graphicgroups.dynamicpew: pew.draw(screen)                           # Big Pew
        for epew in Graphicgroups.enemyprojectiles: epew.draw(screen)                   # ENEMY PEW
        for bits in Graphicgroups.debris: bits.draw(screen)                             # Bits debris
        for enemy in Graphicgroups.enemies: enemy.draw(screen,Game_Objects.player)      # ENEMIES
        for boss in Graphicgroups.bosses: boss.draw(screen,Game_Objects.player)         # BOSS
        for kana in Graphicgroups.correctkanas: kana.draw(screen)                       # CORRECT KANA
        for kana in Graphicgroups.incorrectkanas: kana.draw(screen)                              # WRONG KANA
        for kana in Graphicgroups.bossmodecorrectkana: kana.draw(screen)
        for kana in Graphicgroups.bossmodeincorrectkana: kana.draw(screen)
        for brew in Graphicgroups.brew: brew.draw(screen)
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
        for turret in Graphicgroups.turrets: turret.draw(screen)
        for segment in Graphicgroups.scenery: segment.draw(screen)
        
        if Variables.debugwindow: Debug.draw(CONST.DEBUG_LOC_X,CONST.DEBUG_LOC_Y)   # DEBUG

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




#region GAME OVER STATE
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
        Variables.current_game_state = "GameOver"
        Game_Objects.player.shipcollision = False
        for bullet in Graphicgroups.bullets: bullet.update()                            # BULLETS
        for biglaser in Graphicgroups.biglasers: biglaser.update()                      # BIG LASER
        Graphicgroups.planet_group.update(Game_Objects.player)                          # PLANETS
        for junk in Graphicgroups.spacejunk: junk.update()                              # RANDOM JUNK
        Graphicgroups.starfield_group.update(Game_Objects.player)                       # STARS
        for cutoff in Graphicgroups.cuttoffline: cutoff.update(Game_Objects.player)     # CUTOFF LINE
        for kana in Graphicgroups.correctkanas: kana.update(Game_Objects.player)        # Correct Kanas
        for kana in Graphicgroups.incorrectkanas: kana.update(Game_Objects.player)               # Incorrect kanas
        for warning in Graphicgroups.warnings: warning.update()                         # Big Laser Warning
        for epew in Graphicgroups.enemyprojectiles: epew.update()                       # Enemy Projectiles
        for enemy in Graphicgroups.enemies: enemy.update()                              # ENEMIES
        for wod in Graphicgroups.wallsegments: wod.update()                             # Wall of Death
        for brick in Graphicgroups.bricks: brick.update()                               # Brick debris
        for centerwarn in Graphicgroups.centerwarning: centerwarn.update()              # UI
        Graphicgroups.bridge_group.update(Game_Objects.player)                          # BRIDGE WIPE
        for powerup in Graphicgroups.animatedpowerup: powerup.update()                  # Powerups
        for segment in Graphicgroups.scenery: segment.update()
        for turret in Graphicgroups.turrets: turret.update()

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
        for kana in Graphicgroups.incorrectkanas: kana.draw(screen)                              # WRONG KANA
        for powerup in Graphicgroups.animatedpowerup: powerup.draw(screen)              # Powerup
        for biglaser in Graphicgroups.biglasers: biglaser.draw(screen)                  # BIG LASER
        for wod in Graphicgroups.wallsegments: wod.draw(screen)                         # Wall of Death
        for brick in Graphicgroups.bricks: brick.draw(screen)                           # Brick debirs
        #region Explosion
        Graphicgroups.explosion_group.draw(screen)
        Graphicgroups.explosion_group.update()
        #endregion
        #region Question Text
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
        #region UI Text
        if Variables.score <=0: Variables.score = 0
        scoretext = CONST.UI_FONT.render("Score: " + str(Variables.score), True, 'white')
        screen.blit(scoretext, (CONST.WIDTH-200, 10))

        livestext = CONST.UI_FONT.render("Lives: " + str(Game_Objects.player.lives), True, 'white')
        screen.blit(livestext, (CONST.WIDTH-400, 10))

        leveltext = CONST.UI_FONT.render("Level: " + str(Variables.level), True, 'white')
        screen.blit(leveltext, (CONST.WIDTH-600, 10))

        for centerwarn in Graphicgroups.centerwarning:
            centerwarn.draw()
        #endregion
        Graphicgroups.bridge_group.draw(screen)                                         # BRIDGE WIPE
        for turret in Graphicgroups.turrets: turret.draw(screen)
        for segment in Graphicgroups.scenery: segment.draw(screen)

        #region DEBUG                                                                   # DEBUG
        if Variables.debugwindow: Debug.draw(CONST.DEBUG_LOC_X,CONST.DEBUG_LOC_Y)
        #endregion


        # Game Over 
        GAME_OVER_text = CONST.GAME_OVER_FONT.render('GAME OVER', True, 'white')
        screen.blit(GAME_OVER_text, (10, CONST.PAHEIGHT/2))

        GAME_OVER_Shadow_text = CONST.GAME_OVER_FONT.render('GAME OVER', True, 'white')
        GAME_OVER_Shadow_text.set_alpha(100)
        screen.blit(GAME_OVER_Shadow_text, (15, CONST.PAHEIGHT/2+5))

        # Score
        Score_text = CONST.QUESTION_FONT.render('Score: ' + str(Variables.score), True, 'white')
        screen.blit(Score_text, (400, CONST.PAHEIGHT/8))

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




#region DEBUG CLASS
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
            ["#Enemies",len(Graphicgroups.enemies)],
            ["#Correct Boss Kana",len(Graphicgroups.bossmodecorrectkana)],
            ["#Incorrect Boss Kana",len(Graphicgroups.bossmodeincorrectkana)],
            ["#Turrets",len(Graphicgroups.turrets)],
            ["Boss Kana Timer",Game_Objects.timer.bosskana_timer - Game_Objects.timer.bosskana_frequency],
            ["Kana Num",Variables.kananum],
            ["#Missiles",len(Graphicgroups.missiles)],
            ["HEALTH",Game_Objects.player.health]
            # ["Game State",Variables.STATE],
            # ["Transition",Variables.TRANSITION],
            # ["Boss Shield",(Constants.bosses_array[Variables.level]["shield"]+1)],
            # ["Bullets",len(Graphicgroups.bullets)],
            # ["Persis?",Constants.pew_array[Game_Objects.player.pewtype]["persist"]],
            # ["DefaultPersis?",Game_Objects.player.defaultpersist],
            # ["LaserSize",round(Game_Objects.player.laserbuild,1)],
            # ["Missiles",len(Graphicgroups.missiles)],
            # ["Missile timer",pygame.time.get_ticks() - Game_Objects.player.last_missiletimer],
            # ["Scenery Array",len(Graphicgroups.scenery)],
            # ["Menu Kana Timer",round(Game_Objects.timer.kana_frequency - Game_Objects.timer.kana_timer,1)],
            # ["Star Timer",round(Game_Objects.timer.star_frequency - Game_Objects.timer.star_timer,1)],
            # ["BigLaser Timer",round(Game_Objects.timer.biglaser_randomness - Game_Objects.timer.biglaser_timer)],
            # ["Enemy Timer",round(Game_Objects.timer.enemy_randomness - Game_Objects.timer.enemy_timer)],
            # ["Boss Timer",round(Game_Objects.timer.boss_delay - Game_Objects.timer.boss_timer)],
            # ["IK Timer",round(Game_Objects.timer.incorrectkana_thresh - Game_Objects.timer.incorrectkana_timer)],
            # ["CK Timer",round(Game_Objects.timer.correctkana_thresh - Game_Objects.timer.correctkana_timer)],
            # ["Bridge Timer",round(Game_Objects.timer.bridge_thresh - Game_Objects.timer.bridge_timer)],
            # ["Planet Timer",round(Game_Objects.timer.planet_thresh - Game_Objects.timer.planet_timer)],
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