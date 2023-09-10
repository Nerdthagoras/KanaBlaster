from Constants import clock,fps,screen
from Game_States import current_state,menu_state,game_state,gameover_state
import time
import Variables
import pygame
import os


# Initialize pygame
pygame.init()
pygame.mixer.music.set_volume(.3)
music = pygame.mixer.music.load(os.path.join('sounds','GameIntro.wav'))
pygame.mixer.music.play(-1)

# Game loop
while not current_state.done:
    pygame.display.set_caption(str(clock.get_fps()))
    clock.tick(fps)
    Variables.dt = time.time() - Variables.lt; Variables.lt = time.time()

    current_state.manifest() # Bring objects into existance 
    current_state.update(screen) # Update existing objects
    current_state.draw(screen) # Draw existing objects
    pygame.display.flip() # update the screen
    current_state.handle_events(pygame.event.get()) # Check for events such as key presses

    # Handle state changes when state is done
    if current_state.done:
        if current_state == menu_state:
            current_state = game_state
            music = pygame.mixer.music.load(os.path.join('sounds','TimeDilation.wav'))
            pygame.mixer.music.play(-1)
        elif current_state == game_state:
            current_state = gameover_state
            music = pygame.mixer.music.load(os.path.join('sounds','ColinTheme.wav'))
            pygame.mixer.music.play(-1)
        elif current_state == gameover_state:
            current_state = menu_state
            music = pygame.mixer.music.load(os.path.join('sounds','GameIntro.wav'))
            pygame.mixer.music.play(-1)
    
# Quit
pygame.quit() 