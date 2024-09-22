import pygame, os

#region INITIALIZE PYGAME
pygame.init()                                                           # initialize pygame
FPS = 0                                                                 # no framerate cap
CLOCK = pygame.time.Clock()                                             # Create clock object
WIDTH, HEIGHT = 1440,900                                                # Screen Size
PAHEIGHT = HEIGHT-30
WCENTER, HCENTER = WIDTH // 2, PAHEIGHT // 2                              # Screen Centers
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))                       # Create Screen
#endregion INITIALIZE PYGAME





#region FONTS
DEFAULT_FONT_NAME = "MSGothic"
KANA_FONT = pygame.font.SysFont(DEFAULT_FONT_NAME, 60)
# KANA_FONT = pygame.font.Font('fonts/Nikumaru.otf', 60)
QUESTION_FONT = pygame.font.SysFont(DEFAULT_FONT_NAME, 50)
UI_FONT = pygame.font.SysFont(DEFAULT_FONT_NAME, 30)
KANA_UI_FONT = pygame.font.SysFont(DEFAULT_FONT_NAME, 20)
GAME_OVER_FONT = pygame.font.SysFont(DEFAULT_FONT_NAME, 200)
# GAME_OVER_FONT = pygame.font.Font('fonts/Nikumaru.otf', 160)
STARTING_LEVEL_FONT = pygame.font.SysFont(DEFAULT_FONT_NAME, 150)
WARNING_FONT = pygame.font.SysFont(DEFAULT_FONT_NAME, 100)
#endregion FONTS





#region GRAPHICS
off_screen_offset = 64                                                  # distance from vertical window border
min_kana_alpha = 200
DEBUG_LOC_X, DEBUG_LOC_Y = WIDTH-300,100                         # Debug Location
#endregion GRAPHICS





#region STATIC SURFACES
SURF_ENEMY_PEW = pygame.image.load(os.path.join('images', 'enemypew.png')).convert_alpha()
SURF_BRIDGE = pygame.image.load(os.path.join('images', 'bridge.png')).convert_alpha()
SURF_BIGLASER_WARN = pygame.image.load(os.path.join('images', 'warning.png')).convert_alpha()
SURF_WALLSEGMENT = pygame.image.load(os.path.join('images', 'wallpiece.png')).convert_alpha()
SURF_BRICK = pygame.image.load(os.path.join('images', 'brick.png')).convert_alpha()
SURF_DEBRIS = pygame.image.load(os.path.join('images', 'debris.png')).convert_alpha()
SURF_STARTING_LEVEL = pygame.image.load(os.path.join('images', 'Starting_Level.png')).convert_alpha()

#region Start Button
START_BUTTON_FILES = [f for f in os.listdir(os.getcwd() + '/images/StartButton')]
SURF_START_BUTTON = []
for startbutton in START_BUTTON_FILES: SURF_START_BUTTON.append(pygame.image.load(os.path.join('images','StartButton', startbutton)).convert_alpha())
#endregion Start Button




#region Kana Text
KANA_BUTTON_FILES= [f for f in os.listdir(os.getcwd() + '/images/KanaButton')]
SURF_KANA_BUTTON = []
for kanabutton in KANA_BUTTON_FILES: SURF_KANA_BUTTON.append(pygame.image.load(os.path.join('images','KanaButton', kanabutton)).convert_alpha())
#endregion Kana Text
#endregion STATIC SURFACES





#region ANIMATED SURFACES
import Spritesheet
# Ship Flames
SURF_SPACESHIP_FLAMES = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','Flames','flames.png')).convert_alpha(),128,64,0.75)

# Shield
SURF_SHIELD = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','Shield2.png')).convert_alpha(),128,128,3)

# Brew Animation
SURF_BREWING = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','electricball.png')).convert_alpha(),128,128,1)

# Dynamic pew files
SURF_DYNAMIC_PEW = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('images','Pews','Bluelaser.png')).convert_alpha(),16,16,1)

# Scenery Files
ss = '-r'
SURF_SCENERY_OPEN_1H = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','BorderScenery','1h-Open'+ss+'.png')).convert_alpha(),64,64,1)
SURF_SCENERY_MID_1H = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','BorderScenery','1h-Mid'+ss+'.png')).convert_alpha(),64,64,1)
SURF_SCENERY_CLOSE_1H = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','BorderScenery','1h-Close'+ss+'.png')).convert_alpha(),64,64,1)

SURF_SCENERY_OPEN_2H = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','BorderScenery','2h-Open'+ss+'.png')).convert_alpha(),64,128,1)
SURF_SCENERY_MID_2H = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','BorderScenery','2h-Mid'+ss+'.png')).convert_alpha(),64,128,1)
SURF_SCENERY_CLOSE_2H = Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','BorderScenery','2h-Close'+ss+'.png')).convert_alpha(),64,128,1)

#explosion Files
EXPLOSION_FILES = [f for f in os.listdir(os.getcwd() + '/sprites/Explosions')]
SURF_EXPLOSION = []
for explosion in EXPLOSION_FILES: SURF_EXPLOSION.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','Explosions',explosion)).convert_alpha(),256,256,1))

#SpaceShip Files
SPACESHIP_FILES = [f for f in os.listdir(os.getcwd() + '/sprites/PlayerShips')]
SURF_SPACESHIP = []
for spaceships in SPACESHIP_FILES: SURF_SPACESHIP.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','PlayerShips',spaceships)).convert_alpha(),64,64,1))

#BigLaser Files
BIG_LASER_FILES = [f for f in os.listdir(os.getcwd() + '/sprites/BigLasers')]
SURF_BIG_LASER = []
for bl in BIG_LASER_FILES: SURF_BIG_LASER.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','BigLasers',bl)).convert_alpha(),1024,360,1))

#PowerUp Files
POWER_UP_FILES = [f for f in os.listdir(os.getcwd() + '/sprites/PowerUps')]
SURF_POWER_UP = []
for pu in POWER_UP_FILES: SURF_POWER_UP.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','PowerUps',pu)).convert_alpha(),64,64,1))

#Pew Files
# pew_surf = pygame.image.load(os.path.join('images', 'laser.png')).convert_alpha()
PEW_FILES = [f for f in os.listdir(os.getcwd() + '/images/Pews')]
SURF_PEW = []
for pew in PEW_FILES: SURF_PEW.append(pygame.image.load(os.path.join('images','Pews',pew)).convert_alpha())

#Missile Files
# missile_surf = pygame.image.load(os.path.join('sprites','Missiles','missile1.png')).convert_alpha()
MISSILE_FILES = [f for f in os.listdir(os.getcwd() + '/sprites/Missiles')]
SURF_MISSILE = []
for missile in MISSILE_FILES: SURF_MISSILE.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','Missiles',missile)).convert_alpha(),64,64,1))

#Planet Files
PLANET_FILES = [f for f in os.listdir(os.getcwd() + '/images/Planets')]
SURF_PLANET = []
for plfile in PLANET_FILES: SURF_PLANET.append(pygame.image.load(os.path.join('images','Planets',plfile)).convert_alpha())

#Enemy Spritesheets
ENEMY_FILES = [f for f in os.listdir(os.getcwd() + '/sprites/enemies')]
SURF_ENEMY = []
for enemyfile in ENEMY_FILES: SURF_ENEMY.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','enemies',enemyfile)).convert_alpha(),32,32,2))

#Boss Spritesheets
BOSS_FILES = [f for f in os.listdir(os.getcwd() + '/sprites/bosses128')]
SURF_BOSS = []
for bossfile in BOSS_FILES: SURF_BOSS.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','bosses128',bossfile)).convert_alpha(),128,128,2))

#Turret Spritesheets
TURRET_FILES = [f for f in os.listdir(os.getcwd() + '/sprites/Turrets')]
SURF_TURRET = []
for turret in TURRET_FILES: SURF_TURRET.append(Spritesheet.LoadSpritesheet(pygame.image.load(os.path.join('sprites','Turrets',turret)).convert_alpha(),64,64,1))
#endregion Surfaces for Animated sprites





#region OBJECT ARRAYS
#tips
TIPS = [
    "Collect the requested Kana, Shoot all other Kana",
]

#powerups
ARRAY_POWERUP = [
    {"xvel":120,"surfindx":0,"pueffect":"1up"},
    {"xvel":120,"surfindx":1,"pueffect":"laser"},
    {"xvel":120,"surfindx":2,"pueffect":"speed"},
    {"xvel":240,"surfindx":3,"pueffect":"powerup"},
]

#pews
ARRAY_PLAYER_PEW = [
    {"imgindx":3,"pewsound":2,"laserpower":1,"maxnumpew":3,"pewrate":500,"pewspeed":800,"width":16,"height":16,"persist":False},
    {"imgindx":2,"pewsound":1,"laserpower":1,"maxnumpew":2,"pewrate":200,"pewspeed":3000,"width":256,"height":16,"persist":False},
    {"imgindx":0,"pewsound":1,"laserpower":1,"maxnumpew":4,"pewrate":200,"pewspeed":4000,"width":256,"height":16,"persist":False},
    {"imgindx":1,"pewsound":1,"laserpower":1,"maxnumpew":1000,"pewrate":50,"pewspeed":3000,"width":16,"height":16,"persist":False},
    {"imgindx":1,"pewsound":0,"laserpower":10,"maxnumpew":1,"pewrate":1000,"pewspeed":6000,"width":512,"height":128,"persist":True},
]

#Bosses
ARRAY_BOSSES = [
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
SPACE_JUNK_FILES = [
    ['/images/SpaceJunk/spaaace.png','/sounds/SpaceJunk/spaaace.wav'],
    ['/images/SpaceJunk/spaaace.png','/sounds/SpaceJunk/lovebeinginspace.wav'],
    ['/images/SpaceJunk/Kerbal.png','/sounds/SpaceJunk/kerbal.wav'],
    ['/images/SpaceJunk/asteroid.png'],
]
#endregion Arrays for objects





#region SOUNDS
#pewsounds
PLAYER_PEW_SOUND = pygame.mixer.Sound(os.path.join('sounds','pew.wav'))
PLAYER_PEW_SOUND_FILES = [f for f in os.listdir(os.getcwd() + '/sounds/Pewsounds')]
PLAYER_PEW_SOUNDS = []
for pew in PLAYER_PEW_SOUND_FILES: PLAYER_PEW_SOUNDS.append(pygame.mixer.Sound(os.path.join('sounds','Pewsounds',pew)))

# enginesound = pygame.mixer.Sound(os.path.join('sounds','engine.wav'))
SOUND_GOODHIT = pygame.mixer.Sound(os.path.join('sounds','goodhit.wav'))
SOUND_BADHIT = pygame.mixer.Sound(os.path.join('sounds','badhit.wav'))
SOUND_BRIDGE_WHOOSH = pygame.mixer.Sound(os.path.join('sounds','bridgewhoosh.wav'))
SOUND_SHIP_WAS_HIT = pygame.mixer.Sound(os.path.join('sounds','ShipHit.wav'))
SOUND_BIG_LASER = pygame.mixer.Sound(os.path.join('sounds','biglaser.wav'))
SOUND_BIG_LASER_WARN = pygame.mixer.Sound(os.path.join('sounds','WarningBeep.wav'))
SOUND_ENEMY_PEW = pygame.mixer.Sound(os.path.join('sounds','enemypew.wav'))
SOUND_POWER_UP = pygame.mixer.Sound(os.path.join('sounds','powerup.wav'))
SOUND_SHIP_LASER = pygame.mixer.Sound(os.path.join('sounds','shiplaser.wav'))
SOUND_CORRECT_KANA_LOST = pygame.mixer.Sound(os.path.join('sounds','kanalost.wav'))
SOUND_CORRECT_KANA_LOSING = pygame.mixer.Sound(os.path.join('sounds','kanagonnadie.wav'))
SOUND_BRICK_BREAK = pygame.mixer.Sound(os.path.join('sounds','brickbreaks.wav'))
SOUND_BIG_PEW_BREWING = pygame.mixer.Sound(os.path.join('sounds','BigPewBuildup.wav'))
SOUND_BIG_PEW_READY = pygame.mixer.Sound(os.path.join('sounds','BigPewReady.wav'))
SOUND_BIG_PEW_HOLDING = pygame.mixer.Sound(os.path.join('sounds','BigPewHold.wav'))
SOUND_TURRET_FIRING = pygame.mixer.Sound(os.path.join('sounds','turretfire.wav'))
SOUND_MISSILE_LAUNCHED = pygame.mixer.Sound(os.path.join('sounds','missilelaunch.wav'))
#endregion Sounds