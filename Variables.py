from Functions import read_csv
import time
import random
import os

lt = time.time()
dt = 0

# Kanas CSV
if os.path.isfile('data/userkana.csv'): commasep = read_csv('data/userkana.csv')
else: commasep = read_csv('data/kana.csv')

levels = (5,10,15,20,25,30,35,38,43,46)
gamekana = []
for i in range(len(levels)):    # Shuffle Kana and create levels
    level = commasep[0:levels[i]]
    random.shuffle(level)
    gamekana.append(level)

#changables
level = 0
gamemode = 0
maxlives = 5
lives = 5
score = 0
kananum = 0
laserpower = 1
enemy_health_multiplier = 0

#trackables
BOSSSTATE = False
GAMESTATE = False
last_question_num = 0
last_kananum = 0
last_level = 0
bridgewipecounter = 0
debugwindow = False
hitboxshow = False
shipcollision = True

RGB = [0,0,0]
theta = 0
