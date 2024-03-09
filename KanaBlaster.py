from Constants import clock,fps,screen
from Game_States import intro_state,menu_state,game_state,boss_state,gameover_state
import time
import Variables
import pygame
import os

# Set current state
current_state = intro_state

allstates = [
    [intro_state,menu_state,'GameIntro'],
    [menu_state,game_state,'TimeDilation'],
    [game_state,gameover_state,'ColinTheme'],
    [boss_state,gameover_state,'ColinTheme'],
    [gameover_state,menu_state,'GameIntro'],
]

bossstates = [
    [game_state,boss_state,'BossFight'],
    [boss_state,game_state,'TimeDilation'],
]

# Initialize pygame
pygame.init()
pygame.mixer.music.set_volume(.1)

# Game loop
while not current_state.done:
    #pygame.display.set_caption(str(clock.get_fps()))
    pygame.display.set_caption('Kana Blaster')
    clock.tick(fps)
    Variables.dt = time.time() - Variables.lt; Variables.lt = time.time()

    current_state.manifest() # Bring objects into existance 
    current_state.update(screen) # Update existing objects
    current_state.draw(screen) # Draw existing objects
    pygame.display.flip() # update the screen
    current_state.collision() # collision detection
    current_state.handle_events(pygame.event.get()) # Check for events such as key presses

    # Handle state changes when state is done
    if current_state.done:
        for state in allstates:
            if current_state == state[0]:
                current_state = state[1]
                if len(state) == 3:
                    music = pygame.mixer.music.load(os.path.join('music',str(state[2]) + '.wav'))
                    pygame.mixer.music.play(-1)
                break
    elif current_state.boss:
        for state in bossstates:
            if current_state == state[0]:
                current_state = state[1]
                if len(state) == 3:
                    music = pygame.mixer.music.load(os.path.join('music',str(state[2]) + '.wav'))
                    pygame.mixer.music.play(-1)
                break

# Quit
pygame.quit() 