import CONST, Game_States, Variables
import time, pygame, os

class Game:
    def __init__(self) -> None:
    #region Initialize pygame
        pygame.init()
        pygame.mixer.set_num_channels(20)  # default is 8  # Number of simultaneous sounds
        pygame.mixer.music.set_volume(Variables.musicvolume)

        # Set the beginning state
        self.current_state = Game_States.intro_state
        self.allstates = [
            # Current_State, Next_State, Music for Next_State
            [Game_States.intro_state,Game_States.menu_state,'GameIntro'],
            [Game_States.menu_state,Game_States.game_state,'TimeDilation'],
            [Game_States.game_state,Game_States.gameover_state,'ColinTheme'],
            [Game_States.boss_state,Game_States.gameover_state,'ColinTheme'],
            [Game_States.gameover_state,Game_States.menu_state,'GameIntro'],
        ]
        self.bossstates = [
            # Current_State, Next_State, Music for Next_State
            [Game_States.game_state,Game_States.boss_state],
            [Game_States.boss_state,Game_States.game_state,'TimeDilation'],
        ]

    def run(self):
        #region Game loop
        while not self.current_state.done:
            import Functions
            pygame.mixer.music.set_volume(Variables.musicvolume)
            pygame.display.set_caption('Kana Blaster ' + str(int(CONST.CLOCK.get_fps())))
            CONST.CLOCK.tick(CONST.FPS)
            Variables.delta_time = time.time() - Variables.previous_time; Variables.previous_time = time.time()

            if not Variables.paused: self.current_state.manifest()                                       # Bring objects into existance 
            if not Variables.paused: self.current_state.update()                                         # Update existing objects
            self.current_state.draw(CONST.SCREEN)                                                    # Draw existing objects
            if not Variables.paused: pygame.display.flip()                                          # Update the screen
            if not Variables.paused: Functions.collision()                                          # Global Collision detections
            self.current_state.handle_events(pygame.event.get())                                         # Check for events such as key presses

            #region Handle state changes when state is done
            if self.current_state.done:          
                for state in self.allstates:
                    if self.current_state == state[0]:
                        self.current_state = state[1]
                        if len(state) == 3:
                            pygame.mixer.music.load(
                                os.path.join('music',str(state[2]) + '.wav')
                            )
                            pygame.mixer.music.play(-1)                                             # Play music upon state transition (-1 = loop forever)
                        break
            elif self.current_state.boss:
                for state in self.bossstates:
                    if self.current_state == state[0]:
                        self.current_state = state[1]
                        if len(state) == 3:
                            pygame.mixer.music.load(
                                os.path.join('music',str(state[2]) + '.wav')
                            )
                            pygame.mixer.music.play(-1)                                             # Play music upon state transition (-1 = loop forever)
                        break
        #region QUIT
        pygame.quit()                                                                               # Quit

class GameStatemanager:
    def __init__(self,currentstate) -> None:
        self.currentstate = currentstate

    def get_state(self):
        return self.currentstate

    def set_state(self, state):
        self.currentstate = state

if __name__ == "__main__":
    game = Game()
    game.run()

#region OLD_MAIN
# if __name__ == "__main__":
#     # Set the beginning state
#     current_state = Game_States.intro_state
 
#     allstates = [
#         # Current_State, Next_State, Music for Next_State
#         [Game_States.intro_state,Game_States.menu_state,'GameIntro'],
#         [Game_States.menu_state,Game_States.game_state,'TimeDilation'],
#         [Game_States.game_state,Game_States.gameover_state,'ColinTheme'],
#         [Game_States.boss_state,Game_States.gameover_state,'ColinTheme'],
#         [Game_States.gameover_state,Game_States.menu_state,'GameIntro'],
#     ]
 
#     bossstates = [
#         # Current_State, Next_State, Music for Next_State
#         [Game_States.game_state,Game_States.boss_state],
#         [Game_States.boss_state,Game_States.game_state,'TimeDilation'],
#     ]

#     #region Initialize pygame
#     pygame.init()
#     pygame.mixer.set_num_channels(20)  # default is 8  # Number of simultaneous sounds
#     pygame.mixer.music.set_volume(Variables.musicvolume)
#     #endregion Initialize pygame
#     #region Game loop
#     while not current_state.done:
#         import Functions
#         pygame.mixer.music.set_volume(Variables.musicvolume)
#         pygame.display.set_caption('Kana Blaster ' + str(int(CONST.CLOCK.get_fps())))
#         CONST.CLOCK.tick(CONST.FPS)
#         Variables.delta_time = time.time() - Variables.previous_time; Variables.previous_time = time.time()

#         if not Variables.paused: current_state.manifest()                                       # Bring objects into existance 
#         if not Variables.paused: current_state.update()                                         # Update existing objects
#         current_state.draw(CONST.SCREEN)                                                    # Draw existing objects
#         if not Variables.paused: pygame.display.flip()                                          # Update the screen
#         if not Variables.paused: Functions.collision()                                          # Global Collision detections
#         current_state.handle_events(pygame.event.get())                                         # Check for events such as key presses

#         #region Handle state changes when state is done
#         if current_state.done:          
#             for state in allstates:
#                 if current_state == state[0]:
#                     current_state = state[1]
#                     if len(state) == 3:
#                         music = pygame.mixer.music.load(
#                             os.path.join('music',str(state[2]) + '.wav')
#                         )
#                         pygame.mixer.music.play(-1)                                             # Play music upon state transition (-1 = loop forever)
#                     break
#         elif current_state.boss:
#             for state in bossstates:
#                 if current_state == state[0]:
#                     current_state = state[1]
#                     if len(state) == 3:
#                         music = pygame.mixer.music.load(
#                             os.path.join('music',str(state[2]) + '.wav')
#                         )
#                         pygame.mixer.music.play(-1)                                             # Play music upon state transition (-1 = loop forever)
#                     break
#         #endregion Handle state changes when state is done
#         #endregion Game loop



#     #region QUIT
#     pygame.quit()                                                                               # Quit
#     #endregion QUIT

#endregion OLD_MAIN