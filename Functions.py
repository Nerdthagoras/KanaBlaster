import csv
from graphicgroups import *

def read_csv(file_name):
    with open(file_name, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)
        all_questions = [(row[0], row[1], row[2]) for row in reader]
    return all_questions

def reset_game():
    bullets.clear()
    kanas.clear()
    kanalist.clear()
    correctkanas.clear()
    bridges.clear()
    cuttoffline.clear()
    powerups.clear()
    laserpowerups.clear()
    speedpowerups.clear()
    planets.clear()
    spacejunk.clear()
    warnings.clear()
    biglasers.clear()
    enemies.clear()
    enemyprojectiles.clear()