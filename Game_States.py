from pygame.locals import USEREVENT

# from Constants import BLACK,WHITE,GAME_OVER_font,ui_font,question_font,question_position,WIDTH,HEIGHT,clock,off_screen_offset,min_kana_alpha,spacejunkfiles,explosion_surfs,shiphit,goodhit,badhit,speed_powerup_surf,laser_powerup_surf,spaceship_surf,enginesound,debug_locationx,debug_locationy
from Constants import *
from graphicgroups import *
from Game_Objects import Ship,Planet,SpaceJunk,Star,Bridge,Kana,PowerUp
from spritesheet import PlayAnimation
from debug import debug

import Variables
import math
import random

class MenuState:
    def __init__(self):
        self.done = False

    def update(self,screen):
        pygame.mouse.set_visible(True)

    def draw(self,screen):
        screen.fill((BLACK))

        #region RANDOM JUNK
        for junk in spacejunk:
            junk.update(player)
            junk.draw(screen)
        #endregion 

        #region STARS
        for star in starfield:
            star.update(player)
            star.draw(screen)
        #endregion

        #region FLOATY KANA
        for kana in kanas:
            kana.update(player)

            # remove kana if off screen
            if kana.x < -64:
                kanas.pop(kanas.index(kana))
            kana.draw(screen)
        #endregion        

        #region KANA LIST
        kanalist.clear()
        for f in range(int(Variables.levels[Variables.level])): kanalist.append(Variables.commasep[f])
        for f in range(int(Variables.levels[Variables.level])):
            kanalistthing = ui_font.render(kanalist[f][Variables.gamemode], True, WHITE)
            screen.blit(kanalistthing,(25+(27*f),HEIGHT-30))
        #endregion

        #region BRIDGE WIPE
        for bridge in bridges:
            bridge.x -= bridge.velocity + 1 * (player.x/100)
            if bridge.x < -1000:
                bridges.pop(bridges.index(bridge))
            bridge.draw(screen)
        #endregion 

        #region BUTTONS
        # Game Mode Button
        self.game_mode_location = (10, 50, 200, 40)
        self.game_mode = pygame.Rect(self.game_mode_location)
        pygame.draw.rect(screen, WHITE, self.game_mode, 2)
        if Variables.gamemode == 0:
            sound_state = ui_font.render('Hiragana', True, WHITE)
            screen.blit(sound_state, (75, 60))
        else:
            sound_state = ui_font.render('Katakana', True, WHITE)
            screen.blit(sound_state, (75, 60))

        # Start Level
        self.level_number_location = (10, 10, 200, 40)
        self.level_number = pygame.Rect(self.level_number_location)
        level_text = ui_font.render('Level: ', True, WHITE)
        pygame.draw.rect(screen, WHITE, self.level_number, 2)
        screen.blit(level_text, (self.level_number_location[0]+10,self.level_number_location[1]+10))
        num_text = ui_font.render(str(Variables.level), True, WHITE)
        screen.blit(num_text,(120, 20))            

        # Start Button
        self.start_button_location = (WIDTH // 2-75, HEIGHT //2-80, 150, 70)
        self.start_button = pygame.Rect(self.start_button_location)
        self.start_text = question_font.render('START', True, WHITE)
        pygame.draw.rect(screen, WHITE, self.start_button, 2)
        screen.blit(self.start_text, (self.start_button_location[0]+10, self.start_button_location[1]+10))                      

        # Game Title
        TITLE_text = GAME_OVER_font.render('KANA BLASTER', True, WHITE)
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

            # Stars Timer
            if event.type == USEREVENT+2:
                starfield.append(Star(WIDTH,random.randrange(0,HEIGHT),1,random.randint(0,45),Variables.gamemode))

            # Incorrect Kana Timer
            if event.type == USEREVENT+1:
                selection = random.randint(0,Variables.levels[Variables.level]-1)
                if selection != Variables.kananum:
                    kanas.append(Kana(WIDTH+off_screen_offset, random.randrange(300,HEIGHT-128,),selection,2,random.randint(-10,10)/100,random.randint(min_kana_alpha,256),random.randint(-10,10)))

            # Mouse Events
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Game Mode
                if self.game_mode.collidepoint(event.pos):
                    if Variables.gamemode == 0:
                        Variables.gamemode = 1
                    else:
                        Variables.gamemode = 0

                # start level
                if self.level_number.collidepoint(event.pos):
                    if Variables.level >= 8:
                        Variables.level = 0
                    else:
                        Variables.level += 1

                #start
                if self.start_button.collidepoint(event.pos):
                    kanas.clear()
                    correctkanas.clear()
                    gameover_state.done = False
                    game_state.done = False
                    self.done = True
                    player.x,player.y = (0,HEIGHT-128)

            # Key Events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    kanas.clear()
                    correctkanas.clear()
                    gameover_state.done = False
                    game_state.done = False
                    self.done = True
                    player.x,player.y = (0,HEIGHT-128)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == ord('f'):
                    pygame.display.toggle_fullscreen()

            # Junk Timer
            if event.type == USEREVENT+5:
                whichjunk = random.randint(0,len(spacejunkfiles)-1)
                spacejunk.append(SpaceJunk(WIDTH,random.randrange(0,HEIGHT/2),whichjunk,random.randrange(-10,10),random.randrange(2,8)*0.1))

            # Bridge Timer
            if event.type == USEREVENT+3:
                Bridge.spawn()

class GameState:
    def __init__(self):
        self.done = False

    def update(self,screen):
        if Variables.lives <= 0:
            pygame.mixer.Sound.stop(enginesound)
            self.done = True

    def draw(self,screen):
        pygame.mouse.set_visible(False)

        # region SCREEN
        color_fade_speed = 40
        if Variables.RGB[0] > color_fade_speed:
            Variables.RGB[0] -= color_fade_speed
        else:
            Variables.RGB[0] = 0
        if Variables.RGB[1] > color_fade_speed:
            Variables.RGB[1] -= color_fade_speed
        else:
            Variables.RGB[1] = 0
        if Variables.RGB[2] > color_fade_speed:
            Variables.RGB[2] -= color_fade_speed
        else:
            Variables.RGB[2] = 0
        screen.fill((Variables.RGB[0],Variables.RGB[1],Variables.RGB[2]))
        #endregion

        #region KANA LIST
        for f in range(int(Variables.levels[Variables.level])):
            kanalist.append(Variables.commasep[f])
        for f in range(int(Variables.levels[Variables.level])):
            if Variables.gamemode == 0:
                kanalistthing = ui_font.render(kanalist[f][0], True, (20,20,20))
            else:
                kanalistthing = ui_font.render(kanalist[f][1], True, (20,20,20))
            screen.blit(kanalistthing,(25+(27*f),HEIGHT-30))
        #endregion

        # PLANETS
        for planet in planets:
            planet.update(player)
            planet.draw(screen)

        # RANDOM JUNK
        for junk in spacejunk:
            junk.update(player)
            junk.draw(screen)

        # STARS
        for star in starfield:
            star.update(player)
            star.draw(screen)

        # BULLETS
        for bullet in bullets:
            bullet.draw(screen)

        # CUTOFF LINE
        for cutoff in cuttoffline:
            cutoff.update(player)
            cutoff.draw(screen)

        #region KANA
        #region CORRECT KANA
        for kana in correctkanas:
            kana.update(player)

            # remove kana if off screen
            if kana.x < -64:
                correctkanas.pop(correctkanas.index(kana))
            kana.draw(screen)

            # if player hits kana
            if kana.collide(player.spaceship_rect):
                correctkanas.pop(correctkanas.index(kana))
                explosion = PlayAnimation(kana.x, kana.y,explosion_surfs.images,0.5,False)
                ship_explosion = PlayAnimation(player.x, player.y,explosion_surfs.images,1,False)
                explosion_group.add(explosion)
                explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(shiphit)
                Variables.lives -= 1
                player.x, player.y = 0, HEIGHT-128

            # if player's bullet hits CORRECT kana
            for bullet in bullets:
                if kana.collide(bullet.pew_rect):
                    # Variables.RGB = [255,255,128] # FLASH
                    pygame.mixer.Sound.play(goodhit)
                    Variables.score += 1
                    explosion = PlayAnimation(kana.x, kana.y,explosion_surfs.images,0.5,False)
                    explosion_group.add(explosion)
                    bullets.pop(bullets.index(bullet))
                    correctkanas.pop(correctkanas.index(kana))
        #endregion 

        #region WRONG KANA
        for kana in kanas:
            kana.x -= kana.xvelocity + 1 * (player.x/100)
            kana.y += kana.yvelocity * 2

            # remove kana if off screen
            if kana.x < -64:
                kanas.pop(kanas.index(kana))
            kana.draw(screen)

            # if player hits kana
            if kana.collide(player.spaceship_rect):
                kanas.pop(kanas.index(kana))
                explosion = PlayAnimation(kana.x, kana.y,explosion_surfs.images,0.5,False)
                ship_explosion = PlayAnimation(player.x, player.y,explosion_surfs.images,1,False)
                explosion_group.add(explosion)
                explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(shiphit)
                Variables.lives -= 1
                player.x, player.y = 0, HEIGHT

            # if player's bullet hits WRONG kana
            for bullet in bullets:
                if kana.collide(bullet.pew_rect):
                    Variables.RGB[0] = 128
                    kanas.pop(kanas.index(kana))
                    bullets.pop(bullets.index(bullet))
                    pygame.mixer.Sound.play(badhit)
                    Variables.score -= 2
                    explosion = PlayAnimation(kana.x, kana.y,explosion_surfs.images,0.5,False)
                    explosion_group.add(explosion)
        #endregion
        #endregion KANA

        # PLAYER
        player.draw(screen)

        # POWERUP
        for powerup in powerups:
            powerup.update(player)
            powerup.effect(powerup.pueffect,player)
            powerup.draw(screen)

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
        
        shoot_text = ui_font.render('Shoot', True, WHITE)
        romajitext = question_font.render(Variables.gamekana[Variables.level][Variables.kananum][2], True, WHITE)
        Variables.theta +=0.05
        theta_scale = math.sin(Variables.theta)
        romaji_scaled, romaji_rect = scale_surface_from_center(romajitext, 1.5 + (theta_scale*.5))

        screen.blit(shoot_text, (question_position[0]-90,question_position[1]+13))
        screen.blit(romaji_scaled, (romaji_rect[0]+question_position[0],romaji_rect[1]+question_position[1]))
        #endregion

        #region UI TEXT
        if Variables.score <=0: Variables.score = 0
        scoretext = ui_font.render("Score: " + str(Variables.score), True, WHITE)
        screen.blit(scoretext, (WIDTH-200, 10))

        livestext = ui_font.render("Lives: " + str(Variables.lives), True, WHITE)
        screen.blit(livestext, (WIDTH-400, 10))

        leveltext = ui_font.render("Level: " + str(Variables.level), True, WHITE)
        screen.blit(leveltext, (WIDTH-600, 10))
        #endregion

        # BRIDGE WIPE
        for bridge in bridges:
            bridge.update(player)
            bridge.draw(screen)

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

            # PLANET
            if event.type == USEREVENT+7: Planet.spawn()

            # JUNK
            if event.type == USEREVENT+8: SpaceJunk.spawn()

            # Stars Timer
            if event.type == USEREVENT+2: Star.spawn()

            #region KANA
            #region Correct Kana Timer
            Variables.correctkana_timer -= 1+(player.x)/100
            if Variables.correctkana_timer <= 0:
                correctkanas.append(Kana(WIDTH+off_screen_offset, random.randrange(128,HEIGHT-200,),Variables.kananum,2,random.randint(-10,10)/100,random.randint(min_kana_alpha,256),random.randint(-10,10)))
                Variables.correctkana_timer = random.randint(150,300)
            #endregion

            # Incorrect Kana Timer
            Variables.kana_timer -= 1+(player.x)/100
            if Variables.kana_timer <= 0:
                selection = random.randint(0,Variables.levels[Variables.level]-1)
                if selection != Variables.kananum:
                    kanas.append(Kana(WIDTH+off_screen_offset, random.randrange(128,HEIGHT-200,),selection,2,random.randint(-10,10)/100,random.randint(min_kana_alpha,256),random.randint(-10,10)))
                    Variables.kana_timer = random.randint(50,100)
                
            #endregion KANA

            #region POWERUP
            if event.type == USEREVENT+5:
                powerup_type = random.randint(0,1)
                if powerup_type == 0:
                    PowerUp.spawn(speed_powerup_surf,"speed")
                elif powerup_type == 1:
                    PowerUp.spawn(laser_powerup_surf,"laser")
            #endregion

            # Bridge Timer
            if event.type == USEREVENT+3: Bridge.spawn()
            
            #region CONTROLS
            # KEYDOWN
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: Variables.lives = 0
                if event.key == ord('p'):
                    powerup_type = random.randint(0,1)
                    if powerup_type == 0:
                        PowerUp.spawn(speed_powerup_surf,"speed")
                    elif powerup_type == 1:
                        PowerUp.spawn(laser_powerup_surf,"laser")
                if event.key == ord('e'): Planet.spawn()
                if event.key == ord('q'): SpaceJunk.spawn()
                if event.key == ord('l'):
                    if player.lasersight == True:
                        player.lasersight = False
                    else:
                        player.lasersight = True
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
                if event.key == ord('b'): Bridge.spawn()
            #endregion
            
class GameOverState:
    def __init__(self):
        self.done = False

    def update(self,screen):
        pass

    def draw(self,screen):
        screen.fill((BLACK))

        #region Planets
        for planet in planets:
            planet.x -= planet.velocity * (player.x/100)
            if planet.x < -1000:
                planets.pop(planets.index(planet))
            planet.draw(screen)
        #endregion

        #region Random Junk
        for junk in spacejunk:
            junk.x -= junk.velocity * (player.x/100)
            if junk.x < -1000:
                spacejunk.pop(spacejunk.index(junk))
            junk.draw(screen)
        #endregion 

        #region STARS
        for star in starfield:
            star.x -= star.velocity / 2
            if star.x < 0:
                starfield.pop(starfield.index(star))
            star.draw(screen)
        #endregion

        #region CORRECT KANA
        for kana in correctkanas:
            kana.update(player)

            # remove kana if off screen
            if kana.x < -64:
                correctkanas.pop(correctkanas.index(kana))
            kana.draw(screen)
        #endregion

        #region WRONG KANA
        for kana in kanas:
            kana.update(player)
            
            # remove kana if off screen
            if kana.x < -64:
                kanas.pop(kanas.index(kana))
            kana.draw(screen)
        #endregion        
        
        # EXPLOSION
        explosion_group.draw(screen)
        explosion_group.update()

        # Game Over 
        GAME_OVER_text = GAME_OVER_font.render('GAME OVER', True, WHITE)
        screen.blit(GAME_OVER_text, (10, HEIGHT/2))

        # Score
        Score_text = question_font.render('Score: ' + str(Variables.score), True, WHITE)
        screen.blit(Score_text, (400, HEIGHT/8))

    def handle_events(self, events):
        for event in events:
            #Click the X to close window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Stars Timer
            if event.type == USEREVENT+2: Star.spawn()

            # Incorrect Kana Timer
            Variables.kana_timer -= 1+(player.x)/100
            if Variables.kana_timer <= 0:
                selection = random.randint(0,Variables.levels[Variables.level]-1)
                if selection != Variables.kananum:
                    kanas.append(Kana(WIDTH+off_screen_offset, random.randrange(128,HEIGHT-128,),selection,2,random.randint(-10,10)/100,random.randint(min_kana_alpha,256),random.randint(-10,10)))
                    Variables.kana_timer = random.randint(50,100)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    player.movex, player.movey = 0,0
                    player.pullback = 1.5
                    Variables.lives = Variables.maxlives
                    menu_state.done = False
                    game_state.done = False
                    self.done = True

def displaydebug(x,y):
    debug('level ' + str(Variables.kananum+1) + '\\' + str(len(Variables.gamekana[Variables.level])),x,0+y)
    debug((player.x,player.y),x,20+y)
    debug('FPS: ' + str(round(clock.get_fps(),1)),x,40+y)

# Instantiate Classes
menu_state = MenuState()
game_state = GameState()
gameover_state = GameOverState()
player = Ship(-100,HEIGHT//2,spaceship_surf)

# Set current state
current_state = menu_state