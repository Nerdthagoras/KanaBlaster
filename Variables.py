import Functions, Settings
import time
import random
import os

previous_time = time.time()
delta_time = None

#region BUILD KANA ARRAY
if os.path.isfile('data/userkana.csv'): commasep = Functions.read_csv('data/userkana.csv')
else: commasep = Functions.read_csv('data/kana.csv')

levels = (5,10,15,20,25,30,35,38,43,46)
gamekana = []
for upperbound in range(len(levels)):    # Shuffle Kana and create levels
    # level = commasep[0:levels[i]]
    lowerbound = upperbound - 2
    if lowerbound < 0 :
        level = commasep[0:levels[upperbound]]
    else:
        level = commasep[levels[lowerbound]:levels[upperbound]]
    random.shuffle(level)
    gamekana.append(level)
#endregion BUILD KANA ARRAY




#region MAIN GAME THINGS
maxshiptype = 0
level = 0
gamemode = 0
score = 0
kananum = 0
enemy_health_multiplier = 0
#endregion MAIN GAME THINGS




#region TRACKABLES
current_game_state = "intro"
paused = False
bossstate = False
gamestate = False
transstate = False
transition = False
bossexist = False
debugwindow = False
hitboxshow = False
player_cannot_die = False
missiles_enabled = False
musicvolume = Settings.maxmusicvolume
last_kananum = 0
last_level = 0
generatedcorrectkanacounter = 0
generatedincorrectkanacounter = 0
brewanimindex = 0
scenerytype = 0
sceneryheight = 1
scenerywaittime = 0.5
RGB = [0,0,0]
theta = 0
#endregion TRACKABLES