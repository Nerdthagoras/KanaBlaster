from Functions import read_csv
import time
import random

lt = time.time()
dt = 0

# Kanas CSV
commasep = read_csv('data/kana.csv')
levels = (5,10,15,20,25,30,35,38,43,46)
gamekana = []
for i in range(len(levels)):
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

#trackables
last_question_num = 0
last_kananum = 0
last_level = 0
bridgewipecounter = 0
debugwindow = False
hitboxshow = False
shipcollision = True
shipdistance = 1

RGB = [0,0,0]
theta = 0
