import Constants
import Game_States
import time
import Variables
import pygame
import os

if __name__ == "__main__":
    # Set current state
    current_state = Game_States.intro_state

    allstates = [
        [Game_States.intro_state,Game_States.menu_state,'GameIntro'],
        [Game_States.menu_state,Game_States.game_state,'TimeDilation'],
        [Game_States.game_state,Game_States.gameover_state,'ColinTheme'],
        [Game_States.boss_state,Game_States.gameover_state,'ColinTheme'],
        [Game_States.gameover_state,Game_States.menu_state,'GameIntro'],
    ]

    bossstates = [
        [Game_States.game_state,Game_States.boss_state,'Moog'],
        [Game_States.boss_state,Game_States.game_state,'TimeDilation'],
    ]

    # Initialize pygame
    pygame.init()
    pygame.mixer.music.set_volume(Variables.musicvolume)

    # Game loop
    while not current_state.done:
        #pygame.display.set_caption(str(clock.get_fps()))
        # print(Variables.STATE)
        pygame.mixer.music.set_volume(Variables.musicvolume)
        pygame.display.set_caption('Kana Blaster')
        Constants.clock.tick(Constants.fps)
        Variables.dt = time.time() - Variables.lt; Variables.lt = time.time()

        current_state.manifest() # Bring objects into existance 
        current_state.update(Constants.screen) # Update existing objects
        current_state.draw(Constants.screen) # Draw existing objects
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