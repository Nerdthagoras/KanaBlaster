from spritesheet import LoadSpritesheet

import pygame
from pygame.locals import USEREVENT
import os
import random

# Initialize Pygame
pygame.init()
fps = 60
clock = pygame.time.Clock()

# Screen Size
WIDTH, HEIGHT = 1440,900

# Debug Location
debug_locationx,debug_locationy = WIDTH-200,100

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define some font sizes
font_name = "MSGothic"
kana_font = pygame.font.SysFont(font_name, 60)
question_font = pygame.font.SysFont(font_name, 50)
ui_font = pygame.font.SysFont(font_name, 30)
star_font = pygame.font.SysFont(font_name, 10)
GAME_OVER_font = pygame.font.SysFont(font_name, 200)

# Create the window and define screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Kana Blaster')

# Graphics
off_screen_offset = 64
min_kana_alpha = 200
question_position = (100, 20)
spaceship_surf = pygame.image.load(os.path.join('images', 'ship.png')).convert_alpha()
pew_surf = pygame.image.load(os.path.join('images', 'laser.png')).convert_alpha()
bridge_surf = pygame.image.load(os.path.join('images', 'bridge.png')).convert_alpha()
laser_powerup_surf = pygame.image.load(os.path.join('images', 'laserpowerup.png')).convert_alpha()
speed_powerup_surf = pygame.image.load(os.path.join('images', 'speedpowerup.png')).convert_alpha()
explosion_surfs = LoadSpritesheet(pygame.image.load(os.path.join('sprites','explode.png')).convert_alpha(),256,256,1)
ship_surfs = LoadSpritesheet(pygame.image.load(os.path.join('sprites','explode.png')).convert_alpha(),256,256,1)

planetfiles = [f for f in os.listdir(os.getcwd() + '/images/Planets')]
planet_surfs = []
for plfile in planetfiles: planet_surfs.append(pygame.image.load(os.path.join('images','Planets',plfile)).convert_alpha())

# Space Junk
spacejunkfiles = [
    ['/images/SpaceJunk/spaaace.png','/sounds/SpaceJunk/spaaace.wav'],
    ['/images/SpaceJunk/spaaace.png','/sounds/SpaceJunk/lovebeinginspace.wav'],
    ['/images/SpaceJunk/Kerbal.png','/sounds/SpaceJunk/kerbal.wav']
]

# Sounds
pewsound = pygame.mixer.Sound(os.path.join('sounds','pew.wav'))
enginesound = pygame.mixer.Sound(os.path.join('sounds','engine.wav'))
goodhit = pygame.mixer.Sound(os.path.join('sounds','goodhit.wav'))
badhit = pygame.mixer.Sound(os.path.join('sounds','badhit.wav'))
bridgewhoosh = pygame.mixer.Sound(os.path.join('sounds','bridgewhoosh.wav'))
shiphit = pygame.mixer.Sound(os.path.join('sounds','ShipHit.wav'))

# Timings
pygame.time.set_timer(USEREVENT+1, random.randrange(1000, 2000)) # Incorrect Kana
pygame.time.set_timer(USEREVENT+4, random.randrange(2000, 4000)) # Correct Kana
pygame.time.set_timer(USEREVENT+2, random.randrange(50, 100)) # Stars
pygame.time.set_timer(USEREVENT+3, random.randrange(20000, 40000)) # Bridge
pygame.time.set_timer(USEREVENT+5, random.randrange(20000, 40000)) # LaserPowerups
pygame.time.set_timer(USEREVENT+6, random.randrange(20000, 40000)) # SpeedPowerups
pygame.time.set_timer(USEREVENT+7, random.randrange(30000,60000)) # Planet background
pygame.time.set_timer(USEREVENT+8, random.randrange(60000,120000)) # Junk background
# pygame.time.set_timer(USEREVENT+9, 5000) # Score decrease by 1

