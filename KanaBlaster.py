from Constants import clock,fps,screen
from Game_States import current_state,menu_state,game_state,gameover_state

import pygame
import os

# Initialize pygame
pygame.init()
pygame.mixer.music.set_volume(.1)
music = pygame.mixer.music.load(os.path.join('sounds','GameIntro.wav'))
pygame.mixer.music.play(-1)

# Game loop
while not current_state.done:
    clock.tick(fps)
    current_state.handle_events(pygame.event.get())
    current_state.update(screen)
    current_state.draw(screen)
    pygame.display.update()

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