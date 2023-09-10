from pygame.locals import USEREVENT
from Constants import *
from graphicgroups import *
from Game_Objects import *
from spritesheet import PlayAnimation
from debug import debug
from Functions import reset_game,write_csv
from Settings import *

import Variables
import math
import random
import time

class MenuState:
    def __init__(self):
        self.done = False
        self.star_timer = 0
        self.kana_timer = 0
        self.kana_thresh = 1
        self.enemy_wait_timer = 0
        self.biglaser_timer = 0
        self.biglaser_randomness = 5
        self.enemy_timer = time.time()
        self.enemy_randomness = 5
        self.paused = False

    def manifest(self):
        # Stars Timer
        if time.time() - self.star_timer >= star_frequency:
            Star.spawn()
            self.star_timer = time.time()

        # All Kana Timer
        if time.time() - self.kana_timer >= self.kana_thresh:
            selection = random.randint(0,Variables.levels[Variables.level]-1)
            kanas.append(Kana(WIDTH+off_screen_offset, random.randrange(300,HEIGHT-128,),selection,random.randint(min_kana_alpha,256),random.randint(-kana_rotate_rate,kana_rotate_rate)))
            self.kana_timer = time.time()
            self.kana_thresh = random.randint(minimum_incorrect_kana_frequency,maximum_incorrect_kana_frequency)/10

        #Big Laser Timer
        if Variables.level >= 3 and self.enemy_wait_timer <= 0:
            if time.time() - self.biglaser_timer >= self.biglaser_randomness:
                BigLaserWarning.spawn(player)
                self.biglaser_timer = time.time()
                self.biglaser_randomness = random.randint(5,30)

        # Enemy Timer
        if Variables.level >= 1 and self.enemy_wait_timer <= 0:
            if time.time() - self.enemy_timer >= self.enemy_randomness:
                Enemies.spawn()
                self.enemy_timer = time.time()
                self.enemy_randomness = random.randint(5,30)

    def update(self,screen):
        pygame.mouse.set_visible(True)

        # RANDOM JUNK
        for junk in spacejunk: junk.update(player)

        # STARS
        for star in starfield: star.update(player)

        # Kana
        for kana in kanas: kana.update(player)

        # Warning for BIG LASER
        for warning in warnings: warning.update()

        # BIG LASER
        for biglaser in biglasers: biglaser.update()

        # ENEMIES
        for enemy in enemies:
            enemy.update()
            enemy.shoot(player)

        # enemy Pew
        for epew in enemyprojectiles: epew.update()

    def draw(self,screen):
        screen.fill(('black'))

        for junk in spacejunk: junk.draw(screen)
        for star in starfield: star.draw(screen)
        for kana in kanas: kana.draw(screen)

        #KANA LIST
        kanalist.clear()
        for kana in range(int(Variables.levels[Variables.level])): kanalist.append(Variables.commasep[kana])
        for kana in range(int(Variables.levels[Variables.level])):
            kanakill = int(Variables.commasep[kana][3])*(255/num_to_shoot_new_kana)
            if kanakill >= 255: kanakill = 255
            kanalistthing = ui_font.render(kanalist[kana][Variables.gamemode], True, (kanakill,255,kanakill))
            screen.blit(kanalistthing,(25+(27*kana),HEIGHT-30))

        for epew in enemyprojectiles: epew.draw(screen)
        for enemy in enemies: enemy.draw(screen,player)
        for warning in warnings: warning.draw(screen)
        for biglaser in biglasers: biglaser.draw(screen)

        #region BUTTONS
        # Game Mode Button
        self.game_mode_location = (10, 50, 200, 40)
        self.game_mode = pygame.Rect(self.game_mode_location)
        pygame.draw.rect(screen, 'white', self.game_mode, 2)
        if Variables.gamemode == 0:
            sound_state = ui_font.render('Hiragana', True, 'white')
            screen.blit(sound_state, (75, 60))
        else:
            sound_state = ui_font.render('Katakana', True, 'white')
            screen.blit(sound_state, (75, 60))

        # Start Level
        self.level_number_location = (10, 10, 200, 40)
        self.level_number = pygame.Rect(self.level_number_location)
        level_text = ui_font.render('Level: ', True, 'white')
        pygame.draw.rect(screen, 'white', self.level_number, 2)
        screen.blit(level_text, (self.level_number_location[0]+10,self.level_number_location[1]+10))
        num_text = ui_font.render(str(Variables.level), True, 'white')
        screen.blit(num_text,(120, 20))            

        # Start Button
        self.start_button_location = (WIDTH // 2-75, HEIGHT //2-80, 150, 70)
        self.start_button = pygame.Rect(self.start_button_location)
        self.start_text = question_font.render('START', True, 'white')
        pygame.draw.rect(screen, 'white', self.start_button, 2)
        screen.blit(self.start_text, (self.start_button_location[0]+10, self.start_button_location[1]+10))                      

        # Game Title
        TITLE_text = GAME_OVER_font.render('KANA BLASTER', True, 'white')
        screen.blit(TITLE_text, (10, HEIGHT/8))
        #endregion

        #region DEBUG
        if Variables.debugwindow:
            displaydebug(debug_locationx,debug_locationy)
        #endregion

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

                #start
                if self.start_button.collidepoint(event.pos):
                    reset_game()
                    game_state.enemy_wait_timer = 10
                    gameover_state.done = False
                    game_state.done = False
                    self.done = True
                    # player.spaceship_rect.center[0],player.spaceship_rect.center[1] = (0,HEIGHT-128)

            # Key Events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_SPACE:
                    reset_game()
                    pygame.mixer.Sound.stop(enginesound)
                    game_state.enemy_wait_timer = 10
                    gameover_state.done = False
                    game_state.done = False
                    self.done = True
                if event.key == ord('p'):
                    if self.paused == False:
                        self.paused = True
                    else:
                        self.paused = False
                if event.key == ord('v'):
                    if Variables.debugwindow:
                        Variables.debugwindow = False
                    else:
                        Variables.debugwindow = True
                if event.key == ord('f'): pygame.display.toggle_fullscreen()
                if event.key == ord('e'): Enemies.spawn()
                if event.key == ord('r'): BigLaserWarning.spawn(player)
                if event.key == ord('s'): write_csv('data/userkana',Variables.commasep)

class GameState:
    def __init__(self):
        self.done = False
        self.bgfade_timer = time.time()
        self.enemy_wait_timer = 10
        self.star_timer = time.time()
        self.incorrectkana_timer = time.time()
        self.incorrectkana_thresh = 1
        self.correctkana_timer = time.time()
        self.correctkana_thresh = 4
        self.junk_timer = time.time()
        self.junk_thresh = 60
        self.planet_timer = time.time()
        self.planet_thresh = 60
        self.powerup_timer = time.time()
        self.powerup_thresh = 40
        self.bridge_timer = time.time()
        self.bridge_thresh = 30
        self.biglaser_timer = time.time()
        self.biglaser_randomness = 60
        self.enemy_timer = time.time()
        self.enemy_randomness = 0
        self.correct_kana_lost_sound_play = True
        self.kana_blip = time.time()
        self.prev_level = Variables.level
        self.extralife = ship_extra_life_increment
        self.paused = False

    def manifest(self):
        # Stars Timer
        if time.time() - self.star_timer >= 0.05 and not self.paused:
            Star.spawn()
            self.star_timer = time.time()

        # Incorrect Kana Timer
        if time.time() - self.incorrectkana_timer >= self.incorrectkana_thresh:
            selection = random.randint(0,Variables.levels[Variables.level]-1)
            if selection != Variables.kananum:
                kanas.append(Kana(WIDTH+off_screen_offset, random.randrange(128,HEIGHT-200,),selection,random.randint(min_kana_alpha,256),random.randint(-kana_rotate_rate,kana_rotate_rate)))
                self.incorrectkana_timer = time.time()
                self.incorrectkana_thresh = random.randint(minimum_incorrect_kana_frequency,maximum_incorrect_kana_frequency)/10

        # Correct Kana Timer
        kanakill = int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3])*(255/num_to_shoot_new_kana)
        if kanakill >= 255: kanakill = 255
        if time.time() - self.correctkana_timer >= self.correctkana_thresh:
            if int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3]) < num_to_shoot_new_kana+1:
                correctkanas.append(Kana(WIDTH+off_screen_offset, random.randrange(128,HEIGHT-200,),Variables.kananum,random.randint(min_kana_alpha,256),random.randint(-kana_rotate_rate,kana_rotate_rate),(kanakill,255,kanakill),True))
            else:
                correctkanas.append(Kana(WIDTH+off_screen_offset, random.randrange(128,HEIGHT-200,),Variables.kananum,random.randint(min_kana_alpha,256),random.randint(-kana_rotate_rate,kana_rotate_rate)))
            self.correctkana_timer = time.time()
            self.correctkana_thresh = random.randint(minimum_correct_kana_frequency,maximum_correct_kana_frequency)/10
            self.correct_kana_lost_sound_play = True

        # Big Laser Timer
        if Variables.level >= biglaser_start_level and self.enemy_wait_timer <= 0:
            if time.time() - self.biglaser_timer >= self.biglaser_randomness:
                BigLaserWarning.spawn(player)
                self.biglaser_timer = time.time()
                self.biglaser_randomness = random.randint(5,30)

        # Enemy Timer
        if Variables.level >= enemy_start_level and self.enemy_wait_timer <= 0:
            if time.time() - self.enemy_timer >= self.enemy_randomness:
                Enemies.spawn()
                self.enemy_timer = time.time()
                self.enemy_randomness = random.randint(minimum_enemy_frequency,maximum_enemy_frequency)

        # PLANET Timer
        if time.time() - self.planet_timer >= self.planet_thresh:
            Planet.spawn()
            self.planet_timer = time.time()
            self.planet_thresh = random.randint(60,90)

        # JUNK Timer
        if time.time() - self.junk_timer >= self.junk_thresh:
            SpaceJunk.spawn()
            self.junk_timer = time.time()
            self.junk_thresh = random.randint(60,90)

        # POWERUP Timer
        if time.time() - self.powerup_timer >= self.powerup_thresh:
            powerup_type = random.randint(0,1)
            if powerup_type == 0:
                PowerUp.spawn(speed_powerup_surf,"speed")
            elif powerup_type == 1:
                PowerUp.spawn(laser_powerup_surf,"laser")
            self.powerup_timer = time.time()
            self.powerup_thresh = random.randint(30,40)
                
        # Bridge Timer
        if time.time() - self.bridge_timer >= self.bridge_thresh:
            Bridge.spawn()
            self.bridge_timer = time.time()
            self.bridge_thresh = random.randint(minimum_bridge_frequency,maximum_bridge_frequency)

    def update(self,screen):
        # Extra Life
        if Variables.score >= self.extralife:
            Variables.lives += 1
            self.extralife += ship_extra_life_increment

        # Warning Messages
        if Variables.level == enemy_start_level and self.prev_level < enemy_start_level:
            CenterWarning.spawn('Enemies Active',enemy_surfs[0],3)
            self.enemy_wait_timer = 3
            self.prev_level = enemy_start_level
        if Variables.level == biglaser_start_level and self.prev_level < biglaser_start_level:
            CenterWarning.spawn('Big Laser Active',biglaser_surf)
            self.enemy_wait_timer = 3
            self.prev_level = biglaser_start_level

        # You lost all of your lives
        if Variables.lives <= 0:
            pygame.mixer.Sound.stop(enginesound)
            write_csv('data/userkana.csv',Variables.commasep)
            self.done = True

        # Stop enemies from showing up right at the start
        if self.enemy_wait_timer >= 0:
            self.enemy_wait_timer -= 1 * Variables.dt

        # BULLETS
        for bullet in bullets: bullet.update()

        # BIG LASER
        for biglaser in biglasers: biglaser.update()

        # PLANETS
        for planet in planets: planet.update(player)

        # RANDOM JUNK
        for junk in spacejunk: junk.update(player)

        # STARS
        for star in starfield: star.update(player)

        # CUTOFF LINE
        for cutoff in cuttoffline: cutoff.update(player)

        # Correct Kanas
        for kana in correctkanas:
            kana.update(player)

            # remove kana if off screen
            if kana.x < -64: correctkanas.pop(correctkanas.index(kana))

            # Grow Kana at 2/5th of the screen with
            elif kana.x < 2 * (WIDTH // 5) and kana.x > 10:
                kana.kanascale += Variables.dt/5
                if time.time() - self.kana_blip >= kana.x/500:
                    pygame.mixer.Sound.play(correct_kana_dying_sound)
                    self.kana_blip = time.time()

            # Explode kana if touch left side of screen
            elif kana.x < 0:
                if self.correct_kana_lost_sound_play:
                    pygame.mixer.Sound.play(correct_kana_lost_sound)
                    explosion = PlayAnimation(kana.x, kana.y,explosion_surfs.images,3,False)
                    explosion_group.add(explosion)
                    Variables.score -= 10
                    self.correct_kana_lost_sound_play = False

            # if player hits kana
            if Variables.shipcollision == True:
                if kana.collide(player.spaceship_rect):
                    correctkanas.pop(correctkanas.index(kana))
                    explosion = PlayAnimation(kana.x, kana.y,explosion_surfs.images,0.5,False)
                    ship_explosion = PlayAnimation(player.spaceship_rect.center[0], player.spaceship_rect.center[1],explosion_surfs.images,1,False)
                    explosion_group.add(explosion)
                    explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(shiphit)
                    kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', Variables.gamekana[Variables.level][kana.kana][2] + '.wav'))
                    pygame.mixer.Sound.play(kana_sound)
                    player.respawn()

            # if player's bullet hits CORRECT kana
            for bullet in bullets:
                if kana.collide(bullet.pew_rect):
                    pygame.mixer.Sound.play(goodhit)
                    kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', Variables.gamekana[Variables.level][kana.kana][2] + '.wav'))
                    pygame.mixer.Sound.play(kana_sound)
                    if kana.x >= 2*WIDTH // 3:
                        Variables.score += 3
                    elif kana.x > WIDTH // 3 and kana.x < 2*WIDTH // 3:
                        Variables.score += 2
                    else:
                        Variables.score += 1
                    explosion = PlayAnimation(kana.x, kana.y,explosion_surfs.images,0.5,False)
                    explosion_group.add(explosion)
                    bullets.pop(bullets.index(bullet))
                    correctkanas.pop(correctkanas.index(kana))

                    kanaint = int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3])
                    if kanaint <= num_to_shoot_new_kana: kanaint += 1
                    Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3] = kanaint

            # Kana hit by junk
            for junk in spacejunk:
                if kana.collide(junk.centered_image):
                    pygame.mixer.Sound.play(goodhit)
                    correctkanas.pop(correctkanas.index(kana))
                    explosion = PlayAnimation(kana.x, kana.y,explosion_surfs.images,0.5,False)
                    explosion_group.add(explosion)

        # Incorrect kanas
        for kana in kanas:
            kana.update(player)
            # remove kana if off screen
            if kana.x < -64: kanas.pop(kanas.index(kana))

            # if player hits kana
            if Variables.shipcollision == True:
                if kana.collide(player.spaceship_rect):
                    kanas.pop(kanas.index(kana))
                    explosion = PlayAnimation(kana.x, kana.y,explosion_surfs.images,0.5,False)
                    ship_explosion = PlayAnimation(player.spaceship_rect.center[0], player.spaceship_rect.center[1],explosion_surfs.images,1,False)
                    explosion_group.add(explosion)
                    explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(shiphit)
                    kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', Variables.gamekana[Variables.level][kana.kana][2] + '.wav'))
                    pygame.mixer.Sound.play(kana_sound)
                    player.respawn()

            # if player's bullet hits WRONG kana
            for bullet in bullets:
                if kana.collide(bullet.pew_rect):
                    Variables.RGB[0] = 128
                    kanas.pop(kanas.index(kana))
                    bullets.pop(bullets.index(bullet))
                    kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', Variables.gamekana[Variables.level][kana.kana][2] + '.wav'))
                    pygame.mixer.Sound.play(kana_sound)
                    if kana.x >= 2*WIDTH // 3:
                        Variables.score -= 3
                    elif kana.x > WIDTH // 3 and kana.x < 2*WIDTH // 3:
                        Variables.score -= 2
                    else:
                        Variables.score -= 1
                    explosion = PlayAnimation(kana.x, kana.y,explosion_surfs.images,0.5,False)
                    explosion_group.add(explosion)

            # Stop Kana's from intersecting
            for ckana in correctkanas:
                if kana.collide(ckana.centered_image):
                    pygame.mixer.Sound.play(goodhit)
                    kanas.pop(kanas.index(kana))
                    explosion = PlayAnimation(kana.x, kana.y,explosion_surfs.images,0.5,False)
                    explosion_group.add(explosion)

            # Kana hit by junk
            for junk in spacejunk:
                if kana.collide(junk.centered_image):
                    pygame.mixer.Sound.play(goodhit)
                    kanas.pop(kanas.index(kana))
                    explosion = PlayAnimation(kana.x, kana.y,explosion_surfs.images,0.5,False)
                    explosion_group.add(explosion)

        # Big Laser Warning
        for warning in warnings: warning.update()

        # Enemy Projectiles
        for epew in enemyprojectiles:
            epew.update()
            # if player hits Enemy pew
            if Variables.shipcollision == True:
                if epew.collide(player.spaceship_rect):
                    enemyprojectiles.pop(enemyprojectiles.index(epew))
                    explosion = PlayAnimation(epew.x, epew.y,explosion_surfs.images,0.5,False)
                    ship_explosion = PlayAnimation(player.spaceship_rect.center[0], player.spaceship_rect.center[1],explosion_surfs.images,1,False)
                    explosion_group.add(explosion)
                    explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(shiphit)
                    player.respawn()

        # ENEMIES
        for enemy in enemies:
            enemy.update()
            enemy.shoot(player)

        # Player
        # player.update()

        # UI
        for centerwarn in centerwarning:
            centerwarn.update()

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
        screen.fill((Variables.RGB[0],Variables.RGB[1],Variables.RGB[2]))
        #endregion

        #region KANA LIST
        for f in range(int(Variables.levels[Variables.level])): kanalist.append(Variables.commasep[f])
        for f in range(int(Variables.levels[Variables.level])):
            if Variables.gamemode == 0: kanalistthing = ui_font.render(kanalist[f][0], True, (20,20,20))
            else: kanalistthing = ui_font.render(kanalist[f][1], True, (20,20,20))
            screen.blit(kanalistthing,(25+(27*f),HEIGHT-30))
        #endregion

        # PLANETS
        for planet in planets: planet.draw(screen)

        # RANDOM JUNK
        for junk in spacejunk: junk.draw(screen)

        # STARS
        for star in starfield: star.draw(screen)

        # WARNING for BIG LASER
        for warning in warnings: warning.draw(screen)

        # BULLETS
        for bullet in bullets: bullet.draw(screen)

        # CUTOFF LINE
        for cutoff in cuttoffline: cutoff.draw(screen)

        # ENEMY PEW
        for epew in enemyprojectiles: epew.draw(screen)

        # ENEMIES
        for enemy in enemies:
            enemy.shoot(player)
            enemy.draw(screen,player)

            # if player hits Enemy
            if Variables.shipcollision == True:
                if enemy.collide(player.spaceship_rect):
                    enemies.pop(enemies.index(enemy))
                    explosion = PlayAnimation(enemy.x, enemy.y,explosion_surfs.images,0.5,False)
                    ship_explosion = PlayAnimation(player.spaceship_rect.center[0], player.spaceship_rect.center[1],explosion_surfs.images,1,False)
                    explosion_group.add(explosion)
                    explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(shiphit)
                    player.respawn()

            # if player's bullet hits Enemy
            for bullet in bullets:
                if enemy.collide(bullet.pew_rect):
                    pygame.mixer.Sound.play(goodhit)
                    Variables.score += 1
                    explosion = PlayAnimation(enemy.x, enemy.y,explosion_surfs.images,0.5,False)
                    explosion_group.add(explosion)
                    bullets.pop(bullets.index(bullet))
                    enemies.pop(enemies.index(enemy))

        #region KANA
        #region CORRECT KANA
        for kana in correctkanas: kana.draw(screen)
        #endregion 

        #region WRONG KANA
        for kana in kanas: kana.draw(screen)
        #endregion
        #endregion KANA

        # PLAYER
        player.update()
        player.draw(screen)

        # POWERUP
        for powerup in powerups:
            powerup.update(player)
            powerup.effect(powerup.pueffect,player)
            powerup.draw(screen)

        # BIG LASER
        for biglaser in biglasers:
            biglaser.draw(screen)

            #if laser hits player
            if Variables.shipcollision == True:
                if biglaser.collide(player.spaceship_rect):
                    ship_explosion = PlayAnimation(player.spaceship_rect.center[0], player.spaceship_rect.center[1],explosion_surfs.images,1,False)
                    explosion_group.add(ship_explosion)
                    pygame.mixer.Sound.play(shiphit)
                    player.respawn()

        # EXPLOSION
        explosion_group.draw(screen)
        explosion_group.update()

        #region QUESTION TEXT
        def scale_surface_from_center(surface, scale_factor):
            original_rect = surface.get_rect()
            scaled_width = int(original_rect.width * scale_factor)
            scaled_height = int(original_rect.height * scale_factor)
            scaled_surface = pygame.transform.scale(surface, (scaled_width, scaled_height))
            scaled_rect = scaled_surface.get_rect(center=original_rect.center)
            return scaled_surface, scaled_rect
        
        shoot_text = ui_font.render('Shoot', True, 'white')
        romajitext = question_font.render(Variables.gamekana[Variables.level][Variables.kananum][2], True, 'white')
        Variables.theta += 5 * Variables.dt
        theta_scale = math.sin(Variables.theta)
        romaji_scaled, romaji_rect = scale_surface_from_center(romajitext, 1.5 + (theta_scale*.5))

        screen.blit(shoot_text, (question_position[0]-90,question_position[1]+13))
        screen.blit(romaji_scaled, (romaji_rect[0]+question_position[0],romaji_rect[1]+question_position[1]))
        #endregion

        #region UI TEXT
        if Variables.score <=0: Variables.score = 0
        scoretext = ui_font.render("Score: " + str(Variables.score), True, 'white')
        screen.blit(scoretext, (WIDTH-200, 10))

        livestext = ui_font.render("Lives: " + str(Variables.lives), True, 'white')
        screen.blit(livestext, (WIDTH-400, 10))

        leveltext = ui_font.render("Level: " + str(Variables.level), True, 'white')
        screen.blit(leveltext, (WIDTH-600, 10))

        for centerwarn in centerwarning:
            centerwarn.draw()
        #endregion

        # BRIDGE WIPE
        for bridge in bridges:
            bridge.update(player)
            bridge.draw(screen)

        #region DEBUG
        if Variables.debugwindow: displaydebug(debug_locationx,debug_locationy)
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
                if event.key == ord('p'):
                    if self.paused == False:
                        self.paused = True
                    else:
                        self.paused = False
                if event.key == ord('o'):
                    powerup_type = random.randint(0,2)
                    if powerup_type == 0:
                        PowerUp.spawn(speed_powerup_surf,"speed")
                    elif powerup_type == 1:
                        PowerUp.spawn(laser_powerup_surf,"laser")
                    elif powerup_type == 2:
                        PowerUp.spawn(kanaswitch_powerup_surf,"switch")
                if event.key == ord('l'):
                    if player.lasersight == True:
                        player.lasersight = False
                        pygame.mixer.Sound.stop(shiplaser_sound)
                        player.laserlength = 0
                    else:
                        player.lasersight = True
                        pygame.mixer.Sound.play(shiplaser_sound)
                        player.lasersightcounter = player.poweruptimelength
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
                    if Variables.gamemode == 0:
                        Variables.gamemode = 1
                    else:
                        Variables.gamemode = 0
                if event.key == ord('b'): Bridge.spawn()
                if event.key == ord('q'): SpaceJunk.spawn()
                if event.key == ord('n'): CenterWarning.spawn('Big Laser Active',biglaser_surf,0.5)
                if event.key == ord('e'): Enemies.spawn()
                if event.key == ord('r'): BigLaserWarning.spawn(player)

class GameOverState:
    def __init__(self):
        self.done = False
        self.star_timer = 0
        self.kana_timer = 0
        self.paused = False

    def manifest(self):
        pass

    def update(self,screen):
        # STARS
        for star in starfield: star.update(player)

        # PLANETS
        for planet in planets: planet.update(player)

        # RANDOM JUNK
        for junk in spacejunk: junk.update(player)

        #CORRECT KANA
        for kana in correctkanas:
            # Kana hit by junk
            for junk in spacejunk:
                if kana.collide(junk.centered_image):
                    pygame.mixer.Sound.play(goodhit)
                    kanas.pop(kanas.index(kana))
                    explosion = PlayAnimation(kana.x, kana.y,explosion_surfs.images,0.5,False)
                    explosion_group.add(explosion)
            kana.update(player)

        # WRONG KANA
        for kana in kanas:
            kana.update(player)
    
            # Stop Kana's from intersecting
            for ckana in correctkanas:
                if kana.collide(ckana.centered_image):
                    pygame.mixer.Sound.play(goodhit)
                    kanas.pop(kanas.index(kana))
                    explosion = PlayAnimation(kana.x, kana.y,explosion_surfs.images,0.5,False)
                    explosion_group.add(explosion)

            # Kana hit by junk
            for junk in spacejunk:
                if kana.collide(junk.centered_image):
                    pygame.mixer.Sound.play(goodhit)
                    kanas.pop(kanas.index(kana))
                    explosion = PlayAnimation(kana.x, kana.y,explosion_surfs.images,0.5,False)
                    explosion_group.add(explosion)

        # EXPLOSION
        explosion_group.update()

    def draw(self,screen):
        screen.fill(('black'))

        # PLANETS
        for planet in planets: planet.draw(screen)

        # RANDOM JUNK
        for junk in spacejunk: junk.draw(screen)

        #STARS
        for star in starfield: star.draw(screen)

        # CORRECT KANA
        for kana in correctkanas: kana.draw(screen)

        # WRONG KANA
        for kana in kanas: kana.draw(screen)
        
        # EXPLOSION
        explosion_group.draw(screen)

        # Game Over 
        GAME_OVER_text = GAME_OVER_font.render('GAME OVER', True, 'white')
        screen.blit(GAME_OVER_text, (10, HEIGHT/2))

        # Score
        Score_text = question_font.render('Score: ' + str(Variables.score), True, 'white')
        screen.blit(Score_text, (400, HEIGHT/8))

        #region DEBUG
        if Variables.debugwindow: displaydebug(debug_locationx,debug_locationy)
        #endregion

    def handle_events(self, events):
        for event in events:
            #Click the X to close window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Stars Timer
            if event.type == USEREVENT+2: Star.spawn()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    player.movex, player.movey = 0,0
                    player.pullback = 1.5
                    Variables.lives = Variables.maxlives
                    menu_state.done = False
                    game_state.done = False
                    self.done = True
                if event.key == pygame.K_SPACE:
                    player.movex, player.movey = 0,0
                    player.pullback = 1.5
                    Variables.lives = Variables.maxlives
                    menu_state.done = False
                    game_state.done = False
                    self.done = True                    

#region DEBUG

def displaydebug(x,y):
    debugitems = [
        ["NEL",game_state.extralife],
        ['NumCK',len(correctkanas)],
        ['NumIK',len(kanas)],
        # ['Sub Level',Variables.kananum],
        # ["Player Pos",player.spaceship_rect.center],
        # ['Respawn',round(player.respawn_timer,1)],
        # ["XVel",round(player.Xvelocity,2)],
        # ["YVel",round(player.Yvelocity,2)],
        # ['Laser Counter',player.lasersightcounter],
        # ["Enemy Wait Timer",game_state.enemy_wait_timer],
        # ['Enemy Timer',round(game_state.enemy_randomness - (time.time() - game_state.enemy_timer),1)],
        # ['Big Laser Timer',round(game_state.biglaser_randomness - (time.time() - game_state.biglaser_timer),1)],
        # ['Kana Switch Timer',round(player.kanaswitchcounter,1)],
        ['Bridge Timer',round(game_state.bridge_thresh - (time.time() - game_state.bridge_timer),1)]
    ]
    currentline = y
    for item in debugitems:
        if len(item) == 3: debug(item[0],item[1],x,currentline,item[2])
        else: debug(item[0],item[1],x,currentline)
        currentline += 20
#endregion

#region INSTANCING
# Instantiate Classes
menu_state = MenuState()
game_state = GameState()
gameover_state = GameOverState()
player = Ship(0,HEIGHT//2,spaceship_surf)

# Set current state
current_state = menu_state
#endregion