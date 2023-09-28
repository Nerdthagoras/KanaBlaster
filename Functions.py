import csv
from graphicgroups import *
import Variables

def read_csv(file_name):
    with open(file_name, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        all_questions = [[row[0], row[1], row[2], row[3]] for row in reader]
    return all_questions

def write_csv(file_name,csv_object):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(csv_object)


def reset_game():
    bullets.clear()
    kanas.clear()
    kanalist.clear()
    correctkanas.clear()
    bridge_group.empty()
    cuttoffline.clear()
    powerups.clear()
    laserpowerups.clear()
    speedpowerups.clear()
    planet_group.empty()
    spacejunk.clear()
    warnings.clear()
    biglasers.clear()
    enemies.clear()
    enemyprojectiles.clear()
    Variables.kananum = 0