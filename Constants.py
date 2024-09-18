import pygame, os
import Spritesheet

#region Initialize Pygame
pygame.init()                                                           # initialize pygame
fps = 0                                                                 # no framerate cap
clock = pygame.time.Clock()                                             # Create clock object
WIDTH, HEIGHT = 1440,900                                                # Screen Size
PAHEIGHT = HEIGHT-30
WCENTER, HCENTER = WIDTH // 2, PAHEIGHT // 2                              # Screen Centers
screen = pygame.display.set_mode((WIDTH, HEIGHT))                       # Create Screen
#endregion

tips = [
    "Collect the requested Kana, Shoot all other Kana",
]

debug_locationx,debug_locationy = WIDTH-300,100                         # Debug Location

#region FONTS
font_name = "MSGothic"
kana_font = pygame.font.SysFont(font_name, 60)
# kana_font = pygame.font.Font('fonts/Nikumaru.otf', 60)
question_font = pygame.font.SysFont(font_name, 50)
ui_font = pygame.font.SysFont(font_name, 30)
kana_ui_font = pygame.font.SysFont(font_name, 20)
GAME_OVER_font = pygame.font.SysFont(font_name, 200)
WARNING_font = pygame.font.SysFont(font_name, 100)
#endregion FONTS

# Graphics
off_screen_offset = 64                                                  # distance from vertical window border
min_kana_alpha = 200

#region Surfaces for static images
enemy_pew_surf = pygame.image.load(os.path.join('images', 'enemypew.png')).convert_alpha()
bridge_surf = pygame.image.load(os.path.join('images', 'bridge.png')).convert_alpha()
biglaser_warning_surf = pygame.image.load(os.path.join('images', 'warning.png')).convert_alpha()
wallsegment_surf = pygame.image.load(os.path.join('images', 'wallpiece.png')).convert_alpha()
brick_surf = pygame.image.load(os.path.join('images', 'brick.png')).convert_alpha()
debris_surf = pygame.image.load(os.path.join('images', 'debris.png')).convert_alpha()
spaceship_flame_surfs = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','Flames','flames.png')).convert_alpha(),128,64,0.75)
#endregion Surfaces for static images

#region Surfaces for Animated sprites
# Brew Animation
brewing_surf = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','electricball.png')).convert_alpha(),128,128,1)

# Dynamic pew files
dpew_surf = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('images','Pews','Bluelaser.png')).convert_alpha(),16,16,1)

# Scenery Files
ss = '-r'
open1h = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','BorderScenery','1h-Open'+ss+'.png')).convert_alpha(),64,64,1)
# open1h = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','BorderScenery','1h-Open-hrg.png')).convert_alpha(),64,64,1)
mid1h = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','BorderScenery','1h-Mid'+ss+'.png')).convert_alpha(),64,64,1)
# mid1h = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','BorderScenery','1h-Mid-hrg.png')).convert_alpha(),64,64,1)
close1h = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','BorderScenery','1h-Close'+ss+'.png')).convert_alpha(),64,64,1)

open2h = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','BorderScenery','2h-Open'+ss+'.png')).convert_alpha(),64,128,1)
mid2h = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','BorderScenery','2h-Mid'+ss+'.png')).convert_alpha(),64,128,1)
close2h = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','BorderScenery','2h-Close'+ss+'.png')).convert_alpha(),64,128,1)

#explosion Files
explosion_files = [f for f in os.listdir(os.getcwd() + '/sprites/Explosions')]
explosion_surfs = []
for explosion in explosion_files: explosion_surfs.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','Explosions',explosion)).convert_alpha(),256,256,1))

#SpaceShip Files
spaceship_files = [f for f in os.listdir(os.getcwd() + '/sprites/PlayerShips')]
spaceship_surfs = []
for spaceships in spaceship_files: spaceship_surfs.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','PlayerShips',spaceships)).convert_alpha(),64,64,1))

#BigLaser Files
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

#Missile Files
# missile_surf = pygame.image.load(os.path.join('sprites','Missiles','missile1.png')).convert_alpha()
missilefiles = [f for f in os.listdir(os.getcwd() + '/sprites/Missiles')]
missile_surfs = []
for missile in missilefiles: missile_surfs.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','Missiles',missile)).convert_alpha(),64,64,1))

#Planet Files
planetfiles = [f for f in os.listdir(os.getcwd() + '/images/Planets')]
planet_surfs = []
for plfile in planetfiles: planet_surfs.append(pygame.image.load(os.path.join('images','Planets',plfile)).convert_alpha())

#Enemy Spritesheets
enemyspritesheets = [f for f in os.listdir(os.getcwd() + '/sprites/enemies')]
enemy_spritesheet_surfs = []
for enemyfile in enemyspritesheets: enemy_spritesheet_surfs.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','enemies',enemyfile)).convert_alpha(),32,32,2))

#Boss Spritesheets
bossspritesheets = [f for f in os.listdir(os.getcwd() + '/sprites/bosses128')]
boss_spritesheet_surfs = []
for bossfile in bossspritesheets: boss_spritesheet_surfs.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','bosses128',bossfile)).convert_alpha(),128,128,2))

#Turret Spritesheets
turret_files = [f for f in os.listdir(os.getcwd() + '/sprites/Turrets')]
turret_surfs = []
for turret in turret_files: turret_surfs.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','Turrets',turret)).convert_alpha(),64,64,1))
#endregion Surfaces for Animated sprites

#region Arrays for objects
#powerups
powerup_array = [
    {"xvel":120,"surfindx":0,"pueffect":"1up"},
    {"xvel":120,"surfindx":1,"pueffect":"laser"},
    {"xvel":120,"surfindx":2,"pueffect":"speed"},
    {"xvel":240,"surfindx":3,"pueffect":"powerup"},
]

#pews
pew_array = [
    {"imgindx":3,"pewsound":2,"laserpower":1,"maxnumpew":3,"pewrate":500,"pewspeed":800,"width":16,"height":16,"persist":False},
    {"imgindx":2,"pewsound":1,"laserpower":1,"maxnumpew":2,"pewrate":200,"pewspeed":3000,"width":256,"height":16,"persist":False},
    {"imgindx":0,"pewsound":1,"laserpower":1,"maxnumpew":4,"pewrate":200,"pewspeed":4000,"width":256,"height":16,"persist":False},
    {"imgindx":1,"pewsound":1,"laserpower":1,"maxnumpew":1000,"pewrate":50,"pewspeed":3000,"width":16,"height":16,"persist":False},
    {"imgindx":1,"pewsound":0,"laserpower":10,"maxnumpew":1,"pewrate":1000,"pewspeed":6000,"width":512,"height":128,"persist":True},
]

#Bosses
bosses_array = [
    {"imgindx":0,"type":1,"healthmultiplier":10,"numofbullets":10,"Xvel":50,"Yvel":50,"anglenum":16,"animspeed":10,"shield":100,"music":"moog"},
    {"imgindx":1,"type":1,"healthmultiplier":10,"numofbullets":20,"Xvel":100,"Yvel":100,"anglenum":16,"animspeed":10,"shield":100,"music":"bossfight"},
    {"imgindx":2,"type":0,"healthmultiplier":10,"numofbullets":25,"Xvel":200,"Yvel":200,"anglenum":16,"animspeed":10,"shield":100,"music":"moog"},
    {"imgindx":3,"type":0,"healthmultiplier":10,"numofbullets":30,"Xvel":300,"Yvel":300,"anglenum":16,"animspeed":10,"shield":100,"music":"moog"},
    {"imgindx":3,"type":0,"healthmultiplier":10,"numofbullets":30,"Xvel":300,"Yvel":300,"anglenum":16,"animspeed":10,"shield":100,"music":"moog"},
    {"imgindx":3,"type":0,"healthmultiplier":10,"numofbullets":30,"Xvel":300,"Yvel":300,"anglenum":16,"animspeed":10,"shield":100,"music":"moog"},
    {"imgindx":3,"type":0,"healthmultiplier":10,"numofbullets":30,"Xvel":300,"Yvel":300,"anglenum":16,"animspeed":10,"shield":100,"music":"moog"},
    {"imgindx":3,"type":0,"healthmultiplier":10,"numofbullets":30,"Xvel":300,"Yvel":300,"anglenum":16,"animspeed":10,"shield":100,"music":"moog"},
    {"imgindx":3,"type":0,"healthmultiplier":10,"numofbullets":30,"Xvel":300,"Yvel":300,"anglenum":16,"animspeed":10,"shield":100,"music":"moog"},
    {"imgindx":3,"type":0,"healthmultiplier":10,"numofbullets":30,"Xvel":300,"Yvel":300,"anglenum":16,"animspeed":10,"shield":100,"music":"moog"},
    ]

# Space Junk
spacejunkfiles = [
    ['/images/SpaceJunk/spaaace.png','/sounds/SpaceJunk/spaaace.wav'],
    ['/images/SpaceJunk/spaaace.png','/sounds/SpaceJunk/lovebeinginspace.wav'],
    ['/images/SpaceJunk/Kerbal.png','/sounds/SpaceJunk/kerbal.wav'],
    ['/images/SpaceJunk/asteroid.png'],
]
#endregion Arrays for objects

#region Sounds
pewsound = pygame.mixer.Sound(os.path.join('sounds','pew.wav'))
pewsoundfiles = [f for f in os.listdir(os.getcwd() + '/sounds/Pewsounds')]
pew_sounds = []
for pew in pewsoundfiles: pew_sounds.append(pygame.mixer.Sound(os.path.join('sounds','Pewsounds',pew)))

# enginesound = pygame.mixer.Sound(os.path.join('sounds','engine.wav'))
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
bigpewbuildup = pygame.mixer.Sound(os.path.join('sounds','BigPewBuildup.wav'))
bigpewready = pygame.mixer.Sound(os.path.join('sounds','BigPewReady.wav'))
bigpewhold = pygame.mixer.Sound(os.path.join('sounds','BigPewHold.wav'))
turretfire = pygame.mixer.Sound(os.path.join('sounds','turretfire.wav'))
missilelaunch = pygame.mixer.Sound(os.path.join('sounds','missilelaunch.wav'))

#endregion Sounds