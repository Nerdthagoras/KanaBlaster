from spritesheet import LoadSpritesheet

import pygame
import os

# Initialize Pygame
pygame.init()
fps = 0
clock = pygame.time.Clock()

# Screen Size
WIDTH, HEIGHT = 1440,900

# Debug Location
debug_locationx,debug_locationy = WIDTH-300,100

# Define some font sizes
font_name = "MSGothic"
kana_font = pygame.font.SysFont(font_name, 60)
question_font = pygame.font.SysFont(font_name, 50)
ui_font = pygame.font.SysFont(font_name, 30)
GAME_OVER_font = pygame.font.SysFont(font_name, 200)
WARNING_font = pygame.font.SysFont(font_name, 100)

# Create the window and define screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Kana Blaster')

# Graphics
off_screen_offset = 64
min_kana_alpha = 200
spaceship_surf = pygame.image.load(os.path.join('images', 'ship.png')).convert_alpha()
enemy_pew_surf = pygame.image.load(os.path.join('images', 'enemypew.png')).convert_alpha()
pew_surf = pygame.image.load(os.path.join('images', 'laser.png')).convert_alpha()
bridge_surf = pygame.image.load(os.path.join('images', 'bridge.png')).convert_alpha()
biglaser_warning_surf = pygame.image.load(os.path.join('images', 'warning.png')).convert_alpha()
biglaser_surf = pygame.image.load(os.path.join('images', 'biglaser.png')).convert_alpha()
wallsegment_surf = pygame.image.load(os.path.join('images', 'wallpiece.png')).convert_alpha()
brick_surf = pygame.image.load(os.path.join('images', 'brick.png')).convert_alpha()
debris_surf = pygame.image.load(os.path.join('images', 'debris.png')).convert_alpha()
explosion_surfs = LoadSpritesheet(pygame.image.load(os.path.join('sprites','explode.png')).convert_alpha(),256,256,1)
spaceship_surfs = LoadSpritesheet(pygame.image.load(os.path.join('sprites','ArpShip.png')).convert_alpha(),64,64,1)
spaceship_flame_surfs = LoadSpritesheet(pygame.image.load(os.path.join('sprites','flames.png')).convert_alpha(),128,64,0.75)

#PowerUp Files
laser_powerup_surf = pygame.image.load(os.path.join('images', 'PowerUps', 'laserpowerup.png')).convert_alpha()
speed_powerup_surf = pygame.image.load(os.path.join('images', 'PowerUps', 'speedpowerup.png')).convert_alpha()
oneup_powerup_surf = pygame.image.load(os.path.join('images', 'PowerUps', '1up.png')).convert_alpha()

#Planet Files
planetfiles = [f for f in os.listdir(os.getcwd() + '/images/Planets')]
planet_surfs = []
for plfile in planetfiles: planet_surfs.append(pygame.image.load(os.path.join('images','Planets',plfile)).convert_alpha())

#Enemy Files (this is only used for the graphic showing enemies are enabled)
enemyfiles = [f for f in os.listdir(os.getcwd() + '/images/Enemies')]
enemy_surfs = []
for enemyfile in enemyfiles: enemy_surfs.append(pygame.image.load(os.path.join('images','Enemies',enemyfile)).convert_alpha())

#Enemy Spritesheets
enemyspritesheets = [f for f in os.listdir(os.getcwd() + '/sprites/enemies')]
enemy_spritesheet_surfs = []
for enemyfile in enemyspritesheets: enemy_spritesheet_surfs.append(LoadSpritesheet(pygame.image.load(os.path.join('sprites','enemies',enemyfile)).convert_alpha(),32,32,2))

#Boss Files
#bossfiles = [f for f in os.listdir(os.getcwd() + '/images/Bosses')]
#enemy_surfs = []
#for enemyfile in enemyfiles: enemy_surfs.append(pygame.image.load(os.path.join('images','Enemies',enemyfile)).convert_alpha())

#Boss Spritesheets
bossspritesheets = [f for f in os.listdir(os.getcwd() + '/sprites/bosses')]
boss_spritesheet_surfs = []
for bossfile in bossspritesheets: boss_spritesheet_surfs.append(LoadSpritesheet(pygame.image.load(os.path.join('sprites','bosses',bossfile)).convert_alpha(),32,32,8))

# Space Junk
spacejunkfiles = [
    ['/images/SpaceJunk/spaaace.png','/sounds/SpaceJunk/spaaace.wav'],
    ['/images/SpaceJunk/spaaace.png','/sounds/SpaceJunk/lovebeinginspace.wav'],
    ['/images/SpaceJunk/Kerbal.png','/sounds/SpaceJunk/kerbal.wav'],
]

# Sounds
pewsound = pygame.mixer.Sound(os.path.join('sounds','pew.wav'))
enginesound = pygame.mixer.Sound(os.path.join('sounds','engine.wav'))
goodhit = pygame.mixer.Sound(os.path.join('sounds','goodhit.wav'))
badhit = pygame.mixer.Sound(os.path.join('sounds','badhit.wav'))
bridgewhoosh = pygame.mixer.Sound(os.path.join('sounds','bridgewhoosh.wav'))
shiphit = pygame.mixer.Sound(os.path.join('sounds','ShipHit.wav'))
biglaser_sound = pygame.mixer.Sound(os.path.join('sounds','biglaser.wav'))
warning_sound = pygame.mixer.Sound(os.path.join('sounds','WarningBeep.wav'))
enemypew_sound = pygame.mixer.Sound(os.path.join('sounds','enemypew.wav'))
powerup_sound = pygame.mixer.Sound(os.path.join('sounds','powerup.wav'))
shiplaser_sound = pygame.mixer.Sound(os.path.join('sounds','shiplaser.wav'))
correct_kana_lost_sound = pygame.mixer.Sound(os.path.join('sounds','kanalost.wav'))
correct_kana_dying_sound = pygame.mixer.Sound(os.path.join('sounds','kanagonnadie.wav'))
brickbreak_sound = pygame.mixer.Sound(os.path.join('sounds','brickbreaks.wav'))