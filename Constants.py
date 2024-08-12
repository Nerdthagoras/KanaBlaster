import pygame
import os
import Spritesheet

# Initialize Pygame
pygame.init()
fps = 0
clock = pygame.time.Clock()

# Screen Size
WIDTH, HEIGHT = 1440,900

# Debug Location
debug_locationx,debug_locationy = WIDTH-300,100

# Menu Starfield Messages
menustarmessage = [
    "Music by Nerdthagoras",
    "SUBSCRIBE",
    "Also on Twtich",
    "Please Donate!",
]

# Define some font sizes
font_name = "MSGothic"
kana_font = pygame.font.SysFont(font_name, 60)
question_font = pygame.font.SysFont(font_name, 50)
ui_font = pygame.font.SysFont(font_name, 30)
kana_ui_font = pygame.font.SysFont(font_name, 20)
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
bridge_surf = pygame.image.load(os.path.join('images', 'bridge.png')).convert_alpha()
biglaser_warning_surf = pygame.image.load(os.path.join('images', 'warning.png')).convert_alpha()
wallsegment_surf = pygame.image.load(os.path.join('images', 'wallpiece.png')).convert_alpha()
brick_surf = pygame.image.load(os.path.join('images', 'brick.png')).convert_alpha()
debris_surf = pygame.image.load(os.path.join('images', 'debris.png')).convert_alpha()
explosion_surfs = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','explode.png')).convert_alpha(),256,256,1)
spaceship_surfs = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','ArpShip.png')).convert_alpha(),64,64,1)
spaceship_flame_surfs = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','flames.png')).convert_alpha(),128,64,0.75)

#BigLaser Files
# biglaser_surf = pygame.image.load(os.path.join('images', 'biglaser.png')).convert_alpha()
biglaser_spritesheet_surf = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('images', 'biglaser.png')).convert_alpha(),1024,360,1)

blfiles = [f for f in os.listdir(os.getcwd() + '/sprites/BigLasers')]
biglaser_surfs = []
for bl in blfiles: biglaser_surfs.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','BigLasers',bl)).convert_alpha(),1024,360,1))

#PowerUp Files
pufiles = [f for f in os.listdir(os.getcwd() + '/sprites/PowerUps')]
powerup_surfs = []
for pu in pufiles: powerup_surfs.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','PowerUps',pu)).convert_alpha(),64,64,1))

#Pew Files
pew_surf = pygame.image.load(os.path.join('images', 'laser.png')).convert_alpha()
pewfiles = [f for f in os.listdir(os.getcwd() + '/images/Pews')]
pew_surfs = []
for pew in pewfiles: pew_surfs.append(pygame.image.load(os.path.join('images','Pews',pew)).convert_alpha())

#Planet Files
planetfiles = [f for f in os.listdir(os.getcwd() + '/images/Planets')]
planet_surfs = []
for plfile in planetfiles: planet_surfs.append(pygame.image.load(os.path.join('images','Planets',plfile)).convert_alpha())

#Enemy Files (this is only used for the graphic showing enemies are enabled)
# enemyfiles = [f for f in os.listdir(os.getcwd() + '/images/Enemies')]
# enemy_surfs = []
# for enemyfile in enemyfiles: enemy_surfs.append(pygame.image.load(os.path.join('images','Enemies',enemyfile)).convert_alpha())

#Enemy Spritesheets
enemyspritesheets = [f for f in os.listdir(os.getcwd() + '/sprites/enemies')]
enemy_spritesheet_surfs = []
for enemyfile in enemyspritesheets: enemy_spritesheet_surfs.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','enemies',enemyfile)).convert_alpha(),32,32,2))

#Boss Spritesheets
bossspritesheets = [f for f in os.listdir(os.getcwd() + '/sprites/bosses128')]
boss_spritesheet_surfs = []
for bossfile in bossspritesheets: boss_spritesheet_surfs.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','bosses128',bossfile)).convert_alpha(),128,128,2))

#powerups
powerup_array = [
    {"xvel":100,"surfindx":0,"pueffect":"1up"},
    {"xvel":100,"surfindx":1,"pueffect":"laser"},
    {"xvel":100,"surfindx":2,"pueffect":"speed"},
    {"xvel":100,"surfindx":3,"pueffect":"powerup"},
]

#pews
pew_array = [
    {"imgindx":2,"pewsound":1,"laserpower":1,"maxnumpew":2,"pewrate":200,"pewspeed":3000,"width":256,"height":16,"persist":False},
    {"imgindx":0,"pewsound":1,"laserpower":1,"maxnumpew":4,"pewrate":200,"pewspeed":4000,"width":256,"height":16,"persist":False},
    {"imgindx":1,"pewsound":1,"laserpower":1,"maxnumpew":1000,"pewrate":1,"pewspeed":3000,"width":16,"height":16,"persist":False},
    {"imgindx":1,"pewsound":0,"laserpower":10,"maxnumpew":1,"pewrate":1000,"pewspeed":6000,"width":512,"height":128,"persist":True},
]

#Bosses
bosses_array = [
    {"imgindx":0,"type":1,"healthmultiplier":10,"numofbullets":10,"Xvel":50,"Yvel":50,"anglenum":16,"animspeed":10},
    {"imgindx":1,"type":1,"healthmultiplier":10,"numofbullets":20,"Xvel":100,"Yvel":100,"anglenum":16,"animspeed":10},
    {"imgindx":2,"type":0,"healthmultiplier":10,"numofbullets":25,"Xvel":200,"Yvel":200,"anglenum":16,"animspeed":10},
    {"imgindx":3,"type":0,"healthmultiplier":10,"numofbullets":30,"Xvel":300,"Yvel":300,"anglenum":16,"animspeed":10},
    # {"imgindx":4,"type":2,"healthmultiplier":10,"numofbullets":40,"Xvel":300,"Yvel":300,"anglenum":28,"animspeed":10},
    ]
# Space Junk
spacejunkfiles = [
    ['/images/SpaceJunk/spaaace.png','/sounds/SpaceJunk/spaaace.wav'],
    ['/images/SpaceJunk/spaaace.png','/sounds/SpaceJunk/lovebeinginspace.wav'],
    ['/images/SpaceJunk/Kerbal.png','/sounds/SpaceJunk/kerbal.wav'],
    ['/images/SpaceJunk/asteroid.png','/sounds/SpaceJunk/spaaace.wav'],
    ['/images/SpaceJunk/asteroid.png','/sounds/SpaceJunk/spaaace.wav'],
    ['/images/SpaceJunk/asteroid.png','/sounds/SpaceJunk/spaaace.wav'],
    ['/images/SpaceJunk/asteroid.png','/sounds/SpaceJunk/spaaace.wav'],
]

tips = [
    "Collect the requested Kana, Shoot all other Kana",
]

# Sounds
pewsound = pygame.mixer.Sound(os.path.join('sounds','pew.wav'))
pewsoundfiles = [f for f in os.listdir(os.getcwd() + '/sounds/Pewsounds')]
pew_sounds = []
for pew in pewsoundfiles: pew_sounds.append(pygame.mixer.Sound(os.path.join('sounds','Pewsounds',pew)))

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