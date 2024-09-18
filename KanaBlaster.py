import Constants, Game_States, Variables
import time, pygame, os

if __name__ == "__main__":
    # Set the beginning state e
    current_state = Game_States.intro_state
 
    allstates = [
        # Current_State, Next_State, Music for Next_State
        [Game_States.intro_state,Game_States.menu_state,'GameIntro'],
        [Game_States.menu_state,Game_States.game_state,'TimeDilation'],
        [Game_States.game_state,Game_States.gameover_state,'ColinTheme'],
        [Game_States.boss_state,Game_States.gameover_state,'ColinTheme'],
        [Game_States.gameover_state,Game_States.menu_state,'GameIntro'],
    ] 
 
    bossstates = [
        # Current_State, Next_State, Music for Next_State
        [Game_States.game_state,Game_States.boss_state],
        [Game_States.boss_state,Game_States.game_state,'TimeDilation'],
    ]

    # Initialize pygame
    pygame.init()
    pygame.mixer.set_num_channels(20)  # default is 8  # Number of simultaneous sounds
    pygame.mixer.music.set_volume(Variables.musicvolume)

    # Game loop
    while not current_state.done:
        import Functions
        pygame.mixer.music.set_volume(Variables.musicvolume)
        pygame.display.set_caption('Kana Blaster ' + str(int(Constants.clock.get_fps())))
        Constants.clock.tick(Constants.fps)
        Variables.delta_time = time.time() - Variables.previous_time; Variables.previous_time = time.time()

        if not Variables.PAUSED: current_state.manifest()                                       # Bring objects into existance 
        if not Variables.PAUSED: current_state.update()                                         # Update existing objects
        current_state.draw(Constants.screen)                                                    # Draw existing objects
        if not Variables.PAUSED: pygame.display.flip()                                          # Update the screen
        if not Variables.PAUSED: Functions.collision()                                          # Global Collision detections
        current_state.handle_events(pygame.event.get())                                         # Check for events such as key presses

        # Handle state changes when state is done
        if current_state.done:          
            for state in allstates:
                if current_state == state[0]:
                    current_state = state[1]
                    if len(state) == 3:
                        music = pygame.mixer.music.load(
                            os.path.join('music',str(state[2]) + '.wav')
                        )
                        pygame.mixer.music.play(-1)                                             # Play music upon state transition (-1 = loop forever)
                    break
        elif current_state.boss:
            for state in bossstates:
                if current_state == state[0]:
                    current_state = state[1]
                    if len(state) == 3:
                        music = pygame.mixer.music.load(
                            os.path.join('music',str(state[2]) + '.wav')
                        )
                        pygame.mixer.music.play(-1)                                             # Play music upon state transition (-1 = loop forever)
                    break

    pygame.quit()                                                                               # Quit
