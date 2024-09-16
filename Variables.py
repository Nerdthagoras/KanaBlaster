# from Functions import read_csv
import Functions, Settings
import time
import random
import os

previous_time = time.time()
delta_time = 0

# Kanas CSV
if os.path.isfile('data/userkana.csv'): commasep = Functions.read_csv('data/userkana.csv')
else: commasep = Functions.read_csv('data/kana.csv')

levels = (5,10,15,20,25,30,35,38,43,46)
gamekana = []
for i in range(len(levels)):    # Shuffle Kana and create levels
    level = commasep[0:levels[i]]
    random.shuffle(level)
    gamekana.append(level)

STATE = "intro"

#changables
maxshiptype = 0
level = 0
gamemode = 0
score = 0
kananum = 0
enemy_health_multiplier = 0

#trackables
PAUSED = False
BOSSSTATE = False
GAMESTATE = False
TRANSSTATE= False
TRANSITION = False
bossexist = False
debugwindow = False
hitboxshow = False
player_cannot_die = False
musicvolume = Settings.maxmusicvolume
last_kananum = 0
last_level = 0
generatedcorrectkanacounter = 0
generatedincorrectkanacounter = 0
brewanimindex = 0
scenerytype = 0
sceneryheight = 1

RGB = [0,0,0]
theta = 0
