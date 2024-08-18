import csv

def read_csv(file_name):
    with open(file_name, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        all_questions = [[row[0], row[1], row[2], row[3]] for row in reader]
    return all_questions

def write_csv(file_name,csv_object):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(csv_object)

def soanimate(self):
    import Variables
    self.animindex += self.animspeed * Variables.dt #length of ime before we advance the animation frame
    if self.animindex > len(self.spritearray.images)-1: self.animindex = 0 # reset the frame to 0 if we try to go beyond the array
    self.image = self.spritearray.images[int(self.animindex)] # update the current frame

def moanimate(self):
    import Variables
    self.animindex += self.animspeed * Variables.dt #length of ime before we advance the animation frame
    if self.animindex > len(self.spritearray[self.type].images)-1: self.animindex = 0 # reset the frame to 0 if we try to go beyond the array
    self.image = self.spritearray[self.type].images[int(self.animindex)] # update the current frame

def getmaxship():
    TotalKanaPoints = 0
    import Variables, Settings, Constants
    for sep in Variables.commasep:
        TotalKanaPoints += int(sep[3])
    return TotalKanaPoints / (Settings.num_to_shoot_new_kana*len(Variables.commasep))


def reset_game(): #Executed when pressing START
    import Variables
    import Graphicgroups
    import time
    import Game_States
    #region Clear Object Arrays
    Graphicgroups.centerwarning.clear()
    Graphicgroups.bullets.clear()
    Graphicgroups.kanas.clear()
    Graphicgroups.kanalist.clear()
    Graphicgroups.correctkanas.clear()
    Graphicgroups.bridge_group.empty()
    Graphicgroups.cuttoffline.clear()
    Graphicgroups.powerups.clear()
    # Graphicgroups.laserpowerups.clear()
    # Graphicgroups.speedpowerups.clear()
    Graphicgroups.planet_group.empty()
    Graphicgroups.spacejunk.clear()
    Graphicgroups.warnings.clear()
    Graphicgroups.wallsegments.clear()
    Graphicgroups.biglasers.clear()
    Graphicgroups.enemies.clear()
    Graphicgroups.bosses.clear()
    Graphicgroups.debris.clear()
    Graphicgroups.enemyprojectiles.clear()
    #endregion Clear Object Arrays

    #region Reset Flags
    Variables.BOSSSTATE = False
    Variables.GAMESTATE = False
    Variables.bossexist = False
    #endregion Reset Flags

    #region Reset Values
    Variables.kananum = 0
    Variables.pewtype = 0
    Variables.laserpower = 1
    Variables.enemy_health_multiplier = 0
    Variables.score = 0
    Variables.generatedcorrectkanacounter = 0
    Variables.generatedincorrectkanacounter = 0
    #endregion Reset Values

    #region Reset Timers
    Game_States.game_state.bridge_timer = time.time()
    #endregion Reset Timers
