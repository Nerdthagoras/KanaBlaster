import csv
#region SHRINK HITBOX
def shrink_hitbox(rect,pixels):
    rect = [
        rect[0]+pixels,
        rect[1]+pixels,
        rect[2]-2*pixels,
        rect[3]-2*pixels
    ]
    return rect




#region COLLISIONS
def collision():
    import Graphicgroups, Constants, Game_Objects, Variables, Settings
    import pygame, random, math, os
    # If it is a projectile, then it will hit something, 
    # if it is not a projectile then the ship is considered the projectile
    # Space Junk will be treated like a projectile because it persists after collision
    
    maxexplode = random.randint(0,len(Constants.SURF_EXPLOSION)-1) # pick random explosion type
    
    #region Player Projectiles
    for bullet in Graphicgroups.bullets:

        #if player's bullet hits Wall of Death
        for wod in Graphicgroups.wallsegments:
            if wod.collide(bullet.hitbox):
                Graphicgroups.wallsegments.pop(Graphicgroups.wallsegments.index(wod))
                try:
                    persist = Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["persist"]
                    if not persist:
                        Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                except: pass
                Game_Objects.Debris.spawn(
                    x=wod.x,
                    y=wod.y,
                    mindir=-10,
                    maxdir=10,
                    minvel=100,
                    maxvel=300,
                    image=Constants.SURF_BRICK,
                    origin=Constants.SCREEN
                )
                pygame.mixer.Sound.play(Constants.SOUND_BRICK_BREAK)
                explosion = Game_Objects.Explosion(wod.x, wod.y,Constants.SURF_EXPLOSION,0.5,False)
                Graphicgroups.explosion_group.add(explosion)
                Variables.score += 1

        # if player's bullet hits CORRECT Kana
        for ckana in Graphicgroups.correctkanas:    
            if ckana.collide(bullet.hitbox):
                Variables.RGB[0] = 128
                pygame.mixer.Sound.play(Constants.SOUND_BADHIT)
                kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', ckana.kanasound + '.wav'))
                pygame.mixer.Sound.play(kana_sound)
                if ckana.x >= 2*Constants.WIDTH // 3:
                    Variables.score -= 3
                elif ckana.x > Constants.WIDTH // 3 and ckana.x < 2*Constants.WIDTH // 3:
                    Variables.score -= 2
                else:
                    Variables.score -= 1
                explosion = Game_Objects.Explosion(ckana.x, ckana.y,Constants.SURF_EXPLOSION,0.5,False,explosiontype=maxexplode,xvel=(Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                Graphicgroups.explosion_group.add(explosion)
                try:
                    persist = Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["persist"]
                    if not persist:
                        Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                except: pass
                Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(ckana))

        # if player's bullet hits CORRECT boss Kana
        for ckana in Graphicgroups.bossmodecorrectkana:    
            if ckana.collide(bullet.hitbox):
                Variables.RGB[0] = 128
                pygame.mixer.Sound.play(Constants.SOUND_BADHIT)
                kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', ckana.kanasound + '.wav'))
                pygame.mixer.Sound.play(kana_sound)
                if ckana.x >= 2*Constants.WIDTH // 3:
                    Variables.score -= 3
                elif ckana.x > Constants.WIDTH // 3 and ckana.x < 2*Constants.WIDTH // 3:
                    Variables.score -= 2
                else:
                    Variables.score -= 1
                explosion = Game_Objects.Explosion(ckana.x, ckana.y,Constants.SURF_EXPLOSION,0.5,False,explosiontype=maxexplode,xvel=(Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                Graphicgroups.explosion_group.add(explosion)
                try:
                    persist = Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["persist"]
                    if not persist:
                        Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                except: pass
                Graphicgroups.bossmodecorrectkana.pop(Graphicgroups.bossmodecorrectkana.index(ckana))

        # if player's bullet hits WRONG kana
        for kana in Graphicgroups.incorrectkanas:
            if kana.collide(bullet.hitbox):
                Variables.RGB[1] = 64
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                Graphicgroups.incorrectkanas.pop(Graphicgroups.incorrectkanas.index(kana))
                try:
                    persist = Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["persist"]
                    if not persist:
                        Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                except: pass
                kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', kana.kanasound + '.wav'))
                pygame.mixer.Sound.play(kana_sound)
                if kana.x >= 2*Constants.WIDTH // 3:
                    Variables.score += 3
                    powerup_chance = random.randint(0,Settings.enemy_powerup_freq)
                    if powerup_chance == 0:
                        Game_Objects.AnimatedPowerUp.spawn(
                            Constants.ARRAY_POWERUP[3]["xvel"],
                            Constants.ARRAY_POWERUP[3]["surfindx"],
                            Constants.ARRAY_POWERUP[3]["pueffect"],
                        )
                elif kana.x > Constants.WIDTH // 3 and kana.x < 2*Constants.WIDTH // 3:
                    Variables.score += 2
                else:
                    Variables.score += 1
                explosion = Game_Objects.Explosion(
                    x=kana.x,
                    y=kana.y,
                    spritearray=Constants.SURF_EXPLOSION,
                    scale=0.5,
                    repeat=False,
                    explosiontype=maxexplode,
                    xvel=(Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1
                )
                Graphicgroups.explosion_group.add(explosion)
                Game_Objects.achievements.tingtangarray.append(kana.kanasound)
                Game_Objects.achievements.tingtangshow = True

        # if player's bullet hits WRONG boss kana
        for kana in Graphicgroups.bossmodeincorrectkana:
            if kana.collide(bullet.hitbox):
                Variables.RGB[1] = 64
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                Graphicgroups.bossmodeincorrectkana.pop(Graphicgroups.bossmodeincorrectkana.index(kana))
                try:
                    persist = Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["persist"]
                    if not persist:
                        Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                except: pass
                kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', kana.kanasound + '.wav'))
                pygame.mixer.Sound.play(kana_sound)
                if kana.x >= 2*Constants.WIDTH // 3:
                    Variables.score += 3
                    powerup_chance = random.randint(0,Settings.enemy_powerup_freq)
                    if powerup_chance == 0:
                        Game_Objects.AnimatedPowerUp.spawn(
                            Constants.ARRAY_POWERUP[3]["xvel"],
                            Constants.ARRAY_POWERUP[3]["surfindx"],
                            Constants.ARRAY_POWERUP[3]["pueffect"],
                        )
                elif kana.x > Constants.WIDTH // 3 and kana.x < 2*Constants.WIDTH // 3:
                    Variables.score += 2
                else:
                    Variables.score += 1
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.SURF_EXPLOSION,0.5,False,explosiontype=maxexplode,xvel=(Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                Graphicgroups.explosion_group.add(explosion)
                Game_Objects.achievements.tingtangarray.append(kana.kanasound)
                Game_Objects.achievements.tingtangshow = True

        # if player's bullet hits Enemy
        for enemy in Graphicgroups.enemies:
            if enemy.collide(bullet.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                damage = 1 + random.randint(int(Game_Objects.player.laserpower/5),Game_Objects.player.laserpower)
                enemy.health -= damage
                Game_Objects.Debris.spawn(
                    x=enemy.enemy_rect.centerx,
                    y=enemy.y,
                    mindir=80,
                    maxdir=280,
                    minvel=50,
                    maxvel=200,
                    image=Constants.SURF_DEBRIS,
                    origin=Graphicgroups.enemies.index(enemy)
                )
                Game_Objects.Damagenum.spawn(enemy.enemy_rect.centerx,0,enemy.y,damage)
                enemy.knockbackx = Settings.enemy_max_knockbackx
                enemy.knockbacky = enemy.collide(bullet.hitbox)
                if enemy.health <= 0:
                    Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                    explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.SURF_EXPLOSION,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                    Variables.score += 1
                    powerup_chance = random.randint(0,Settings.enemy_powerup_freq)
                    if powerup_chance == 0:
                        Game_Objects.AnimatedPowerUp.spawn(
                            Constants.ARRAY_POWERUP[3]["xvel"],
                            Constants.ARRAY_POWERUP[3]["surfindx"],
                            Constants.ARRAY_POWERUP[3]["pueffect"],
                        )

                try:
                    persist = Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["persist"]
                    if not persist:
                        Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                except: pass

        # if player's bullet hits Boss
        for boss in Graphicgroups.bosses:
            if boss.collide(bullet.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                # damage = random.randint(
                #     int(Game_Objects.player.laserpower / 10),           # Minimum
                #     int(Game_Objects.player.laserpower)                 # Maximum
                # )
                damage = int(Game_Objects.player.laserpower / (Constants.ARRAY_BOSSES[Variables.level]["shield"]+1))
                boss.health -= damage
                # boss.bossalpha = 50
                boss.flash = 255
                Constants.ARRAY_BOSSES[Variables.level]["shield"] -= 1
                if Constants.ARRAY_BOSSES[Variables.level]["shield"] < 0: Constants.ARRAY_BOSSES[Variables.level]["shield"] = 0
                Game_Objects.Debris.spawn(
                    x=boss.boss_rect.centerx,
                    y=boss.y,
                    mindir=80,
                    maxdir=280,
                    minvel=50,
                    maxvel=200,
                    image=Constants.SURF_DEBRIS,
                    origin=Constants.SCREEN
                )
                Game_Objects.Damagenum.spawn(boss.boss_rect.centerx,boss.velocity,boss.y,damage)
                if boss.health <= 0:
                    Game_Objects.Debris.spawn(
                        x=boss.boss_rect.centerx,
                        y=boss.y,
                        mindir=0,
                        maxdir=359,
                        minvel=50,
                        maxvel=200,
                        image=Constants.SURF_DEBRIS,
                        origin=Constants.SCREEN,
                        numdebris=100
                    )
                    Graphicgroups.bosses.pop(Graphicgroups.bosses.index(boss))
                    explosion = Game_Objects.Explosion(boss.x, boss.y,Constants.SURF_EXPLOSION,8,False,xvel=(Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                    Graphicgroups.explosion_group.add(explosion)
                    Variables.score += 99
                    Variables.transition = False
                try: Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                except: pass

        # if player's bullet hits powerup
        for powerup in Graphicgroups.animatedpowerup:
            if powerup.collide(bullet.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_BADHIT)
                explosion = Game_Objects.Explosion(powerup.x, powerup.y,Constants.SURF_EXPLOSION,0.5,False,xvel=(Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                Graphicgroups.explosion_group.add(explosion)
                try:
                    persist = Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["persist"]
                    if not persist:
                        Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                except: pass
                Graphicgroups.animatedpowerup.pop(Graphicgroups.animatedpowerup.index(powerup))

        # if player's bullet hits ship debirs
        for shipdeb in Graphicgroups.debris:
            if shipdeb.collide(bullet.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                explosion = Game_Objects.Explosion(shipdeb.x, shipdeb.y,Constants.SURF_EXPLOSION,0.2,False,xvel=(Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                Graphicgroups.explosion_group.add(explosion)
                try:
                    persist = Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["persist"]
                    if not persist:
                        Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                except: pass
                Graphicgroups.debris.pop(Graphicgroups.debris.index(shipdeb))

        # if player's bullet hits scenery
        for scenery in Graphicgroups.scenery:
            if scenery.collide(bullet.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                try: Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                except: pass
                explosion = Game_Objects.Explosion(scenery.x, scenery.y,Constants.SURF_EXPLOSION,0.5,False,xvel=120)
                Graphicgroups.explosion_group.add(explosion)

        #if player's bullet hits turret
        for turret in Graphicgroups.turrets:
            if turret.collide(bullet.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                try: Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                except: pass
                explosion = Game_Objects.Explosion(turret.x, turret.y,Constants.SURF_EXPLOSION,0.5,False,xvel=120)
                Graphicgroups.explosion_group.add(explosion)
                Graphicgroups.turrets.pop(Graphicgroups.turrets.index(turret))

    #endregion

    #region Player Big Pew
    for bullet in Graphicgroups.dynamicpew:

        #if player's bullet hits Wall of Death
        for wod in Graphicgroups.wallsegments:
            if wod.collide(bullet.hitbox):
                Graphicgroups.wallsegments.pop(Graphicgroups.wallsegments.index(wod))
                try:
                    persist = True
                    if not persist:
                        Graphicgroups.dynamicpew.pop(Graphicgroups.dynamicpew.index(bullet))
                except: pass
                Game_Objects.Debris.spawn(
                    x=wod.x,
                    y=wod.y,
                    mindir=-10,
                    maxdir=10,
                    minvel=100,
                    maxvel=300,
                    image=Constants.SURF_BRICK,
                    origin=Constants.SCREEN
                )
                pygame.mixer.Sound.play(Constants.SOUND_BRICK_BREAK)
                explosion = Game_Objects.Explosion(wod.x, wod.y,Constants.SURF_EXPLOSION,0.5,False)
                Graphicgroups.explosion_group.add(explosion)
                Variables.score += 1

        # if player's bullet hits CORRECT Kana
        for ckana in Graphicgroups.correctkanas:
            if ckana.collide(bullet.hitbox):
                Variables.RGB[0] = 128
                pygame.mixer.Sound.play(Constants.SOUND_BADHIT)
                kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', ckana.kanasound + '.wav'))
                pygame.mixer.Sound.play(kana_sound)
                if ckana.x >= 2*Constants.WIDTH // 3:
                    Variables.score -= 3
                elif ckana.x > Constants.WIDTH // 3 and ckana.x < 2*Constants.WIDTH // 3:
                    Variables.score -= 2
                else:
                    Variables.score -= 1
                explosion = Game_Objects.Explosion(
                    x=ckana.x,
                    y=ckana.y,
                    spritearray=Constants.SURF_EXPLOSION,
                    scale=0.5,
                    repeat=False,
                    explosiontype=maxexplode,
                    xvel=bullet.velocity/Settings.explode_vel_frac*-1)
                Graphicgroups.explosion_group.add(explosion)
                try:
                    persist = True
                    if not persist:
                        Graphicgroups.dynamicpew.pop(Graphicgroups.dynamicpew.index(bullet))
                except: pass
                Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(ckana))

        # if player's bullet hits CORRECT boss Kana
        for ckana in Graphicgroups.bossmodecorrectkana:
            if ckana.collide(bullet.hitbox):
                Variables.RGB[0] = 128
                pygame.mixer.Sound.play(Constants.SOUND_BADHIT)
                kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', ckana.kanasound + '.wav'))
                pygame.mixer.Sound.play(kana_sound)
                if ckana.x >= 2*Constants.WIDTH // 3:
                    Variables.score -= 3
                elif ckana.x > Constants.WIDTH // 3 and ckana.x < 2*Constants.WIDTH // 3:
                    Variables.score -= 2
                else:
                    Variables.score -= 1
                explosion = Game_Objects.Explosion(ckana.x, ckana.y,Constants.SURF_EXPLOSION,0.5,False,explosiontype=maxexplode,xvel=(Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                Graphicgroups.explosion_group.add(explosion)
                try:
                    persist = True
                    if not persist:
                        Graphicgroups.dynamicpew.pop(Graphicgroups.dynamicpew.index(bullet))
                except: pass
                Graphicgroups.bossmodecorrectkana.pop(Graphicgroups.bossmodecorrectkana.index(ckana))

        # if player's bullet hits WRONG kana
        for kana in Graphicgroups.incorrectkanas:
            if kana.collide(bullet.hitbox):
                Variables.RGB[1] = 64
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                Graphicgroups.incorrectkanas.pop(Graphicgroups.incorrectkanas.index(kana))
                try:
                    persist = True
                    if not persist:
                        Graphicgroups.dynamicpew.pop(Graphicgroups.dynamicpew.index(bullet))
                except: pass
                kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', kana.kanasound + '.wav'))
                pygame.mixer.Sound.play(kana_sound)
                if kana.x >= 2*Constants.WIDTH // 3:
                    Variables.score += 3
                    powerup_chance = random.randint(0,Settings.enemy_powerup_freq)
                    if powerup_chance == 0:
                        Game_Objects.AnimatedPowerUp.spawn(
                            Constants.ARRAY_POWERUP[3]["xvel"],
                            Constants.ARRAY_POWERUP[3]["surfindx"],
                            Constants.ARRAY_POWERUP[3]["pueffect"],
                        )
                elif kana.x > Constants.WIDTH // 3 and kana.x < 2*Constants.WIDTH // 3:
                    Variables.score += 2
                else:
                    Variables.score += 1
                explosion = Game_Objects.Explosion(
                    x=kana.x,
                    y=kana.y,
                    spritearray=Constants.SURF_EXPLOSION,
                    scale=0.5,
                    repeat=False,
                    explosiontype=maxexplode,
                    xvel=bullet.velocity/Settings.explode_vel_frac*-1)
                Graphicgroups.explosion_group.add(explosion)
                Game_Objects.achievements.tingtangarray.append(kana.kanasound)
                Game_Objects.achievements.tingtangshow = True

        # if player's bullet hits WRONG boss kana
        for kana in Graphicgroups.bossmodeincorrectkana:
            if kana.collide(bullet.hitbox):
                Variables.RGB[1] = 64
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                Graphicgroups.bossmodeincorrectkana.pop(Graphicgroups.bossmodeincorrectkana.index(kana))
                try:
                    persist = True
                    if not persist:
                        Graphicgroups.dynamicpew.pop(Graphicgroups.dynamicpew.index(bullet))
                except: pass
                kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', kana.kanasound + '.wav'))
                pygame.mixer.Sound.play(kana_sound)
                if kana.x >= 2*Constants.WIDTH // 3:
                    Variables.score += 3
                    powerup_chance = random.randint(0,Settings.enemy_powerup_freq)
                    if powerup_chance == 0:
                        Game_Objects.AnimatedPowerUp.spawn(
                            Constants.ARRAY_POWERUP[3]["xvel"],
                            Constants.ARRAY_POWERUP[3]["surfindx"],
                            Constants.ARRAY_POWERUP[3]["pueffect"],
                        )
                elif kana.x > Constants.WIDTH // 3 and kana.x < 2*Constants.WIDTH // 3:
                    Variables.score += 2
                else:
                    Variables.score += 1
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.SURF_EXPLOSION,0.5,False,explosiontype=maxexplode,xvel=(Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                Graphicgroups.explosion_group.add(explosion)
                Game_Objects.achievements.tingtangarray.append(kana.kanasound)
                Game_Objects.achievements.tingtangshow = True

        # if player's bullet hits Enemy
        for enemy in Graphicgroups.enemies:
            if enemy.collide(bullet.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                damage = 1 + random.randint(int(Game_Objects.player.laserpower/5),Game_Objects.player.laserpower)
                enemy.health -= damage
                Game_Objects.Debris.spawn(
                    x=enemy.enemy_rect.centerx,
                    y=enemy.y,
                    mindir=80,
                    maxdir=280,
                    minvel=50,
                    maxvel=200,
                    image=Constants.SURF_DEBRIS,
                    origin=Graphicgroups.enemies.index(enemy)
                )
                Game_Objects.Damagenum.spawn(enemy.enemy_rect.centerx,0,enemy.y,damage)
                enemy.knockbackx = Settings.enemy_max_knockbackx
                enemy.knockbacky = enemy.collide(bullet.hitbox)
                if enemy.health <= 0:
                    Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                    explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.SURF_EXPLOSION,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                    Variables.score += 1
                    powerup_chance = random.randint(0,Settings.enemy_powerup_freq)
                    if powerup_chance == 0:
                        Game_Objects.AnimatedPowerUp.spawn(
                            Constants.ARRAY_POWERUP[3]["xvel"],
                            Constants.ARRAY_POWERUP[3]["surfindx"],
                            Constants.ARRAY_POWERUP[3]["pueffect"],
                        )

                try:
                    persist = True
                    if not persist:
                        Graphicgroups.dynamicpew.pop(Graphicgroups.dynamicpew.index(bullet))
                except: pass

        # if player's bullet hits Boss
        for boss in Graphicgroups.bosses:
            if boss.collide(bullet.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                # damage = random.randint(
                #     int(Game_Objects.player.laserpower / 10),           # Minimum
                #     int(Game_Objects.player.laserpower)                 # Maximum
                # )
                damage = int(Game_Objects.player.laserpower / (Constants.ARRAY_BOSSES[Variables.level]["shield"]+1))
                boss.health -= damage
                boss.flash = 255
                Constants.ARRAY_BOSSES[Variables.level]["shield"] -= 1
                if Constants.ARRAY_BOSSES[Variables.level]["shield"] < 0: Constants.ARRAY_BOSSES[Variables.level]["shield"] = 0
                Game_Objects.Debris.spawn(
                    x=boss.boss_rect.centerx,
                    y=boss.y,
                    mindir=80,
                    maxdir=280,
                    minvel=50,
                    maxvel=200,
                    image=Constants.SURF_DEBRIS,
                    origin=Graphicgroups.bosses.index(boss)
                )
                Game_Objects.Damagenum.spawn(boss.boss_rect.centerx,boss.velocity,boss.y,damage)
                if boss.health <= 0:
                    Game_Objects.Debris.spawn(
                        x=boss.boss_rect.centerx,
                        y=boss.y,
                        mindir=0,
                        maxdir=359,
                        minvel=50,
                        maxvel=200,
                        image=Constants.SURF_DEBRIS,
                        origin=Constants.SCREEN,
                        numdebris=100
                    )
                    Graphicgroups.bosses.pop(Graphicgroups.bosses.index(boss))
                    explosion = Game_Objects.Explosion(boss.x, boss.y,Constants.SURF_EXPLOSION,8,False,xvel=(Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                    Graphicgroups.explosion_group.add(explosion)
                    Variables.score += 99
                    Variables.transition = False
                try: Graphicgroups.dynamicpew.pop(Graphicgroups.dynamicpew.index(bullet))
                except: pass

        # if player's bullet hits powerup
        for powerup in Graphicgroups.animatedpowerup:
            if powerup.collide(bullet.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_BADHIT)
                explosion = Game_Objects.Explosion(powerup.x, powerup.y,Constants.SURF_EXPLOSION,0.5,False,xvel=(Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                Graphicgroups.explosion_group.add(explosion)
                try:
                    persist = True
                    if not persist:
                        Graphicgroups.dynamicpew.pop(Graphicgroups.dynamicpew.index(bullet))
                except: pass
                Graphicgroups.animatedpowerup.pop(Graphicgroups.animatedpowerup.index(powerup))

        # if player's bullet hits ship debirs
        for shipdeb in Graphicgroups.debris:
            if shipdeb.collide(bullet.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                explosion = Game_Objects.Explosion(shipdeb.x, shipdeb.y,Constants.SURF_EXPLOSION,0.2,False,xvel=(Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                Graphicgroups.explosion_group.add(explosion)
                try:
                    persist = True
                    if not persist:
                        Graphicgroups.dynamicpew.pop(Graphicgroups.dynamicpew.index(bullet))
                except: pass
                Graphicgroups.debris.pop(Graphicgroups.debris.index(shipdeb))

        # if player's bullet hits scenery
        for scenery in Graphicgroups.scenery:
            if scenery.collide(bullet.hitbox):
                # channel = pygame.mixer.Channel(8)
                # channel.play(Constants.goodhit)
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                try: Graphicgroups.dynamicpew.pop(Graphicgroups.dynamicpew.index(bullet))
                except: pass
                explosion = Game_Objects.Explosion(scenery.x, scenery.y,Constants.SURF_EXPLOSION,0.25,False,xvel=120)
                Graphicgroups.explosion_group.add(explosion)

        #if player's bullet hits turret
        for turret in Graphicgroups.turrets:
            if turret.collide(bullet.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                # try: Graphicgroups.dynamicpew.pop(Graphicgroups.dynamicpew.index(bullet))
                # except: pass
                explosion = Game_Objects.Explosion(turret.x, turret.y,Constants.SURF_EXPLOSION,0.5,False,xvel=120)
                Graphicgroups.explosion_group.add(explosion)
                Graphicgroups.turrets.pop(Graphicgroups.turrets.index(turret))

    #endregion

    #region Player Missiles
    for bullet in Graphicgroups.missiles:

        # if player's missile hits WRONG kana
        for kana in Graphicgroups.incorrectkanas:
            if kana.collide(bullet.hitbox):
                Variables.RGB[1] = 64
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                pygame.mixer.Sound.stop(Constants.SOUND_MISSILE_LAUNCHED)
                Graphicgroups.incorrectkanas.pop(Graphicgroups.incorrectkanas.index(kana))
                try:
                    persist = Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["persist"]
                    if not persist:
                        Graphicgroups.missiles.pop(Graphicgroups.missiles.index(bullet))
                except: pass
                kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', kana.kanasound + '.wav'))
                pygame.mixer.Sound.play(kana_sound)
                if kana.x >= 2*Constants.WIDTH // 3:
                    Variables.score += 3
                    powerup_chance = random.randint(0,Settings.enemy_powerup_freq)
                    if powerup_chance == 0:
                        Game_Objects.AnimatedPowerUp.spawn(
                            Constants.ARRAY_POWERUP[3]["xvel"],
                            Constants.ARRAY_POWERUP[3]["surfindx"],
                            Constants.ARRAY_POWERUP[3]["pueffect"],
                        )
                elif kana.x > Constants.WIDTH // 3 and kana.x < 2*Constants.WIDTH // 3:
                    Variables.score += 2
                else:
                    Variables.score += 1
                explosion = Game_Objects.Explosion(
                    x=kana.x,
                    y=kana.y,
                    spritearray=Constants.SURF_EXPLOSION,
                    scale=0.5,
                    repeat=False,
                    explosiontype=maxexplode,
                    xvel=(Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1
                )
                Graphicgroups.explosion_group.add(explosion)
                Game_Objects.achievements.tingtangarray.append(kana.kanasound)
                Game_Objects.achievements.tingtangshow = True

        # if player's bullet hits WRONG boss kana
        for kana in Graphicgroups.bossmodeincorrectkana:
            if kana.collide(bullet.hitbox):
                Variables.RGB[1] = 64
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                Graphicgroups.bossmodeincorrectkana.pop(Graphicgroups.bossmodeincorrectkana.index(kana))
                try: Graphicgroups.missiles.pop(Graphicgroups.missiles.index(bullet))
                except: pass
                kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', kana.kanasound + '.wav'))
                pygame.mixer.Sound.play(kana_sound)
                if kana.x >= 2*Constants.WIDTH // 3:
                    Variables.score += 3
                    powerup_chance = random.randint(0,Settings.enemy_powerup_freq)
                    if powerup_chance == 0:
                        Game_Objects.AnimatedPowerUp.spawn(
                            Constants.ARRAY_POWERUP[3]["xvel"],
                            Constants.ARRAY_POWERUP[3]["surfindx"],
                            Constants.ARRAY_POWERUP[3]["pueffect"],
                        )
                elif kana.x > Constants.WIDTH // 3 and kana.x < 2*Constants.WIDTH // 3:
                    Variables.score += 2
                else:
                    Variables.score += 1
                Constants.ARRAY_BOSSES[Variables.level]["shield"] -= 2
                if Constants.ARRAY_BOSSES[Variables.level]["shield"] < 0: Constants.ARRAY_BOSSES[Variables.level]["shield"] = 0
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.SURF_EXPLOSION,0.5,False,explosiontype=maxexplode,xvel=(Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                Graphicgroups.explosion_group.add(explosion)
                Game_Objects.achievements.tingtangarray.append(kana.kanasound)
                Game_Objects.achievements.tingtangshow = True

        #if player's missile hits turret
        for turret in Graphicgroups.turrets:
            if turret.collide(bullet.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                pygame.mixer.Sound.stop(Constants.SOUND_MISSILE_LAUNCHED)
                try: Graphicgroups.missiles.pop(Graphicgroups.missiles.index(bullet))
                except: pass
                explosion = Game_Objects.Explosion(turret.x, turret.y,Constants.SURF_EXPLOSION,0.5,False,xvel=120)
                Graphicgroups.explosion_group.add(explosion)
                Graphicgroups.turrets.pop(Graphicgroups.turrets.index(turret))

        # if player's missile hits Enemy
        for enemy in Graphicgroups.enemies:
            if enemy.collide(bullet.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                pygame.mixer.Sound.stop(Constants.SOUND_MISSILE_LAUNCHED)
                damage = 1 + random.randint(int(Game_Objects.player.laserpower/5),Game_Objects.player.laserpower)
                enemy.health -= damage
                Game_Objects.Debris.spawn(
                    x=enemy.enemy_rect.centerx,
                    y=enemy.y,
                    mindir=80,
                    maxdir=280,
                    minvel=50,
                    maxvel=200,
                    image=Constants.SURF_DEBRIS,
                    origin=Graphicgroups.enemies.index(enemy)
                )
                Game_Objects.Damagenum.spawn(enemy.enemy_rect.centerx,0,enemy.y,damage)
                enemy.knockbackx = Settings.enemy_max_knockbackx
                enemy.knockbacky = enemy.collide(bullet.hitbox)
                if enemy.health <= 0:
                    Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                    explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.SURF_EXPLOSION,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                    Variables.score += 1
                    powerup_chance = random.randint(0,Settings.enemy_powerup_freq)
                    if powerup_chance == 0:
                        Game_Objects.AnimatedPowerUp.spawn(
                            Constants.ARRAY_POWERUP[3]["xvel"],
                            Constants.ARRAY_POWERUP[3]["surfindx"],
                            Constants.ARRAY_POWERUP[3]["pueffect"],
                        )
                try: Graphicgroups.missiles.pop(Graphicgroups.missiles.index(bullet))
                except: pass

        # if player's missile hits Boss
        for boss in Graphicgroups.bosses:
            if boss.collide(bullet.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                # damage = random.randint(
                #     int(Game_Objects.player.laserpower / 10),           # Minimum
                #     int(Game_Objects.player.laserpower)                 # Maximum
                # )
                damage = int(Game_Objects.player.laserpower / (Constants.ARRAY_BOSSES[Variables.level]["shield"]+1))
                boss.health -= damage
                # boss.bossalpha = 50
                boss.flash = 255
                Constants.ARRAY_BOSSES[Variables.level]["shield"] -= 1
                if Constants.ARRAY_BOSSES[Variables.level]["shield"] < 0: Constants.ARRAY_BOSSES[Variables.level]["shield"] = 0
                Game_Objects.Debris.spawn(
                    x=boss.boss_rect.centerx,
                    y=boss.y,
                    mindir=80,
                    maxdir=280,
                    minvel=50,
                    maxvel=200,
                    image=Constants.SURF_DEBRIS,
                    origin=Graphicgroups.bosses.index(boss)
                )
                Game_Objects.Damagenum.spawn(boss.boss_rect.centerx,boss.velocity,boss.y,damage)
                if boss.health <= 0:
                    Game_Objects.Debris.spawn(
                        x=boss.boss_rect.centerx,
                        y=boss.y,
                        mindir=0,
                        maxdir=359,
                        minvel=50,
                        maxvel=200,
                        image=Constants.SURF_DEBRIS,
                        origin=Constants.SCREEN,
                        numdebris=100
                    )
                    Graphicgroups.bosses.pop(Graphicgroups.bosses.index(boss))
                    explosion = Game_Objects.Explosion(boss.x, boss.y,Constants.SURF_EXPLOSION,8,False,xvel=(Constants.ARRAY_PLAYER_PEW[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                    Graphicgroups.explosion_group.add(explosion)
                    Variables.score += 99
                    Variables.transition = False
                try: Graphicgroups.missiles.pop(Graphicgroups.missiles.index(bullet))
                except: pass

        # if player's missile hits scenery
        for scenery in Graphicgroups.scenery:
            if scenery.collide(bullet.hitbox):
                # channel = pygame.mixer.Channel(8)
                # channel.play(Constants.goodhit)
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                try: Graphicgroups.missiles.pop(Graphicgroups.missiles.index(bullet))
                except: pass
                explosion = Game_Objects.Explosion(scenery.x, scenery.y,Constants.SURF_EXPLOSION,0.25,False,xvel=120)
                Graphicgroups.explosion_group.add(explosion)

    #endregion Player Missiles

    #region Enemy Projectiles
    for epew in Graphicgroups.enemyprojectiles:
        # if hit Player
        if Game_Objects.player.shipcollision == True and Variables.player_cannot_die == False:
            if epew.collide(Game_Objects.player.hitbox):
                Graphicgroups.enemyprojectiles.pop(Graphicgroups.enemyprojectiles.index(epew))
                explosion = Game_Objects.Explosion(epew.x, epew.y,Constants.SURF_EXPLOSION,0.5,False)
                ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.SURF_EXPLOSION,1,False)
                Graphicgroups.explosion_group.add(explosion)
                Graphicgroups.explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(Constants.SOUND_SHIP_WAS_HIT)
                Game_Objects.player.respawn()

        # if hit other enemy
        for enemy in Graphicgroups.enemies:
            if Settings.enemiescanshooteachother and enemy.collide(epew.hitbox) and epew.origin != Graphicgroups.enemies.index(enemy):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                damage = 1 + int(Variables.enemy_health_multiplier * Settings.enemy_health * 0.2)
                enemy.health -= damage
                Game_Objects.Debris.spawn(
                    x=enemy.enemy_rect.centerx,
                    y=enemy.y,
                    mindir=80,
                    maxdir=280,
                    minvel=50,
                    maxvel=200,
                    image=Constants.SURF_DEBRIS,
                    origin=Graphicgroups.enemies.index(enemy)
                )
                Game_Objects.Damagenum.spawn(enemy.enemy_rect.centerx,enemy.velocity,enemy.y,damage)
                if enemy.health == 0:
                    Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                    explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.SURF_EXPLOSION,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                try: Graphicgroups.enemyprojectiles.pop(Graphicgroups.enemyprojectiles.index(epew))
                except: pass

        # if WRONG kana
        for kana in Graphicgroups.incorrectkanas:
            if kana.collide(epew.hitbox):
                Graphicgroups.incorrectkanas.pop(Graphicgroups.incorrectkanas.index(kana))
                try: Graphicgroups.enemyprojectiles.pop(Graphicgroups.enemyprojectiles.index(epew))
                except: pass
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.SURF_EXPLOSION,0.5,False)
                Graphicgroups.explosion_group.add(explosion)
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)

        # if CORRECT kana
        for kana in Graphicgroups.correctkanas:
            if kana.collide(epew.hitbox):
                Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(kana))
                try: Graphicgroups.enemyprojectiles.pop(Graphicgroups.enemyprojectiles.index(epew))
                except: pass
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.SURF_EXPLOSION,0.5,False)
                Graphicgroups.explosion_group.add(explosion)
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)

        for scenery in Graphicgroups.scenery:
            if scenery.collide(epew.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                try: Graphicgroups.enemyprojectiles.pop(Graphicgroups.enemyprojectiles.index(epew))
                except: pass
                explosion = Game_Objects.Explosion(scenery.x, scenery.y,Constants.SURF_EXPLOSION,0.5,False,xvel=120)
                Graphicgroups.explosion_group.add(explosion)
    #endregion

    #region Big Laser
    # if BIG LASER hits player
    for biglaser in Graphicgroups.biglasers:
        if Game_Objects.player.shipcollision == True:
            if biglaser.collide(Game_Objects.player.hitbox):
                ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.SURF_EXPLOSION,1,False)
                Graphicgroups.explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(Constants.SOUND_SHIP_WAS_HIT)
                Game_Objects.player.respawn()

        # correctKana hit by BIG LASER
        for kana in Graphicgroups.correctkanas:
            if kana.collide(biglaser.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                try: Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(kana))
                except: pass
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.SURF_EXPLOSION,0.5,False,xvel=biglaser.velocity/12)
                Graphicgroups.explosion_group.add(explosion)

        # Wrong Kana hit by BIG LASER
        for kana in Graphicgroups.incorrectkanas:
            if kana.collide(biglaser.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                try: Graphicgroups.incorrectkanas.pop(Graphicgroups.incorrectkanas.index(kana))
                except: pass
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.SURF_EXPLOSION,0.5,False,xvel=biglaser.velocity/12)
                Graphicgroups.explosion_group.add(explosion)

        # if enemy hit by BIG LASER
        for enemy in Graphicgroups.enemies:
            if enemy.collide(biglaser.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                Variables.score += 1
                explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.SURF_EXPLOSION,0.5,False,xvel=biglaser.velocity/12)
                Graphicgroups.explosion_group.add(explosion)
                try: Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                except: pass

        # if powerup hit by BIG LASER
        for powerup in Graphicgroups.powerups:
            if powerup.collide(biglaser.hitbox):
                explosion = Game_Objects.Explosion(powerup.x, powerup.y,Constants.SURF_EXPLOSION,0.5,False,xvel=biglaser.velocity/12)
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                Graphicgroups.explosion_group.add(explosion)
                try: Graphicgroups.powerups.pop(Graphicgroups.powerups.index(powerup))
                except: pass

        #if BIG LASER hits wall segments
        for wod in Graphicgroups.wallsegments:
            if wod.collide(biglaser.hitbox):
                Graphicgroups.wallsegments.pop(Graphicgroups.wallsegments.index(wod))
                Game_Objects.Debris.spawn(
                    x=wod.x,
                    y=wod.y,
                    mindir=-10,
                    maxdir=10,
                    minvel=100,
                    maxvel=300,
                    image=Constants.SURF_BRICK,
                    origin=Constants.SCREEN
                )
                pygame.mixer.Channel(0).play(Constants.SOUND_BRICK_BREAK)
                explosion = Game_Objects.Explosion(wod.x, wod.y,Constants.SURF_EXPLOSION,0.5,False,xvel=biglaser.velocity/12)
                Graphicgroups.explosion_group.add(explosion)

    #endregion

    #region Space Junk
    for junk in Graphicgroups.spacejunk:
        # correctKana hit by junk
        for kana in Graphicgroups.correctkanas:
            if kana.collide(junk.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(kana))
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.SURF_EXPLOSION,0.5,False)
                Graphicgroups.explosion_group.add(explosion)

        # Wrong Kana hit by junk
        for kana in Graphicgroups.incorrectkanas:
            if kana.collide(junk.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                Graphicgroups.incorrectkanas.pop(Graphicgroups.incorrectkanas.index(kana))
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.SURF_EXPLOSION,0.5,False)
                Graphicgroups.explosion_group.add(explosion)

        # Wall segments hit by junk
        for wod in Graphicgroups.wallsegments:
            if wod.collide(junk.hitbox):
                Graphicgroups.wallsegments.pop(Graphicgroups.wallsegments.index(wod))
                Game_Objects.Debris.spawn(
                    x=wod.x,
                    y=wod.y,
                    mindir=-10,
                    maxdir=10,
                    minvel=100,
                    maxvel=300,
                    image=Constants.SURF_BRICK,
                    origin=Constants.SCREEN
                )
                pygame.mixer.Sound.play(Constants.SOUND_BRICK_BREAK)
                explosion = Game_Objects.Explosion(wod.x, wod.y,Constants.SURF_EXPLOSION,0.5,False)
                Graphicgroups.explosion_group.add(explosion)

    #endregion

    #region Enemy Ship
    for enemy in Graphicgroups.enemies:
        for scenery in Graphicgroups.scenery:
            if scenery.collide(enemy.hitbox):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                try: Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                except: pass
                explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.SURF_EXPLOSION,0.5,False)
                Graphicgroups.explosion_group.add(explosion)
    #endregion Enemy Ship

    #region Enemy Debris
    for edebs in Graphicgroups.debris:
        # if enemy debris hits Enemy
        for enemy in Graphicgroups.enemies:
            if enemy.collide(edebs.hitbox) and edebs.origin != Graphicgroups.enemies.index(enemy):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                damage = 1 + int(Variables.enemy_health_multiplier * Settings.enemy_health * 0.2)
                enemy.health -= damage
                Game_Objects.Debris.spawn(
                    x=enemy.enemy_rect.centerx,
                    y=enemy.y,
                    mindir=80,
                    maxdir=280,
                    minvel=50,
                    maxvel=200,
                    image=Constants.SURF_DEBRIS,
                    origin=Graphicgroups.enemies.index(enemy)
                )
                Game_Objects.Damagenum.spawn(enemy.enemy_rect.centerx,enemy.velocity,enemy.y,damage)
                if enemy.health == 0:
                    Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                    explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.SURF_EXPLOSION,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                try: Graphicgroups.debris.pop(Graphicgroups.debris.index(edebs))
                except: pass
        pass
    #endregion Enemy Debris

    #region Ship
    # if player's ship hits correct kana
    for kana in Graphicgroups.correctkanas:
        if Game_Objects.player.shipcollision == True:
            if kana.collide(Game_Objects.player.hitbox):
                Variables.RGB[1] = 64
                Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(kana))
                #explosion = Game_Objects.Explosion(kana.x, kana.y,explosion_surfs.images,0.5,False)
                #ship_explosion = Game_Objects.Explosion(player.spaceship_rect.center[0], player.spaceship_rect.center[1],explosion_surfs.images,1,False)
                #explosion_group.add(explosion)
                #explosion_group.add(ship_explosion)
                # pygame.mixer.Sound.play(goodhit)
                if kana.x >= 2*Constants.WIDTH // 3:
                    Variables.score += 3
                elif kana.x > Constants.WIDTH // 3 and kana.x < 2*Constants.WIDTH // 3:
                    Variables.score += 2
                else:
                    Variables.score += 1
                kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', Variables.gamekana[Variables.level][kana.kana][2] + '.wav'))
                pygame.mixer.Sound.play(kana_sound)
                timeskanashot = int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3])      # Get the value of the kana from csv
                if timeskanashot <= Settings.num_to_shoot_new_kana: timeskanashot += 1                                                                  # Increase number to csv value when collected
                Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3] = timeskanashot           # Store Incremented value back into csv
                Game_Objects.achievements.tingtangarray.append(kana.kanasound)
                Game_Objects.achievements.tingtangshow = True
                #player.respawn()

        # if player hits kana

    # if player's ship hits correct boss kana
    for kana in Graphicgroups.bossmodecorrectkana:
        if Game_Objects.player.shipcollision == True:
            if kana.collide(Game_Objects.player.hitbox):
                Variables.RGB[1] = 64
                Graphicgroups.bossmodecorrectkana.pop(Graphicgroups.bossmodecorrectkana.index(kana))
                kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', Variables.gamekana[Variables.level][kana.kana][2] + '.wav'))
                pygame.mixer.Sound.play(kana_sound)
                pygame.mixer.Sound.play(Constants.SOUND_SHIP_WAS_HIT)
                Constants.ARRAY_BOSSES[Variables.level]["shield"] -= 10
                if Constants.ARRAY_BOSSES[Variables.level]["shield"] < 0: Constants.ARRAY_BOSSES[Variables.level]["shield"] = 0
                Variables.kananum = random.randint(0,len(Variables.gamekana[Variables.level])-1)
                for boss in Graphicgroups.bosses:
                    explosion = Game_Objects.Explosion(boss.x+random.randint(0,256), boss.y+random.randint(-128,128),Constants.SURF_EXPLOSION,1,False)
                    Graphicgroups.explosion_group.add(explosion)

    # if player's ship hits wrong kana
    for kana in Graphicgroups.incorrectkanas:
        if Game_Objects.player.shipcollision == True and Variables.player_cannot_die == False:
            if kana.collide(Game_Objects.player.hitbox):
                Graphicgroups.incorrectkanas.pop(Graphicgroups.incorrectkanas.index(kana))
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.SURF_EXPLOSION,0.5,False)
                ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.SURF_EXPLOSION,1,False)
                Graphicgroups.explosion_group.add(explosion)
                Graphicgroups.explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(Constants.SOUND_SHIP_WAS_HIT)
                kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', Variables.gamekana[Variables.level][kana.kana][2] + '.wav'))
                pygame.mixer.Sound.play(kana_sound)
                Game_Objects.player.respawn()

    # if player's ship hits wrong boss kana
    for kana in Graphicgroups.bossmodeincorrectkana:
        if Game_Objects.player.shipcollision == True and Variables.player_cannot_die == False:
            if kana.collide(Game_Objects.player.hitbox):
                Graphicgroups.bossmodeincorrectkana.pop(Graphicgroups.bossmodeincorrectkana.index(kana))
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.SURF_EXPLOSION,0.5,False)
                ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.SURF_EXPLOSION,1,False)
                Graphicgroups.explosion_group.add(explosion)
                Graphicgroups.explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(Constants.SOUND_SHIP_WAS_HIT)
                kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', Variables.gamekana[Variables.level][kana.kana][2] + '.wav'))
                pygame.mixer.Sound.play(kana_sound)
                Game_Objects.player.respawn()

    # if player hits Enemy
    for enemy in Graphicgroups.enemies:
        if Game_Objects.player.shipcollision == True and Variables.player_cannot_die == False:
            if enemy.collide(Game_Objects.player.hitbox):
                Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.SURF_EXPLOSION,0.5,False)
                ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.SURF_EXPLOSION,1,False)
                Graphicgroups.explosion_group.add(explosion)
                Graphicgroups.explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(Constants.SOUND_SHIP_WAS_HIT)
                Game_Objects.player.respawn()

    # if player hits Boss
    for enemy in Graphicgroups.bosses:
        if Game_Objects.player.shipcollision == True and Variables.player_cannot_die == False:
            if enemy.collide(Game_Objects.player.hitbox):
                # Graphicgroups.bosses.pop(Graphicgroups.bosses.index(enemy))
                # explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.explosion_surfs,0.5,False)
                ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.SURF_EXPLOSION,1,False)
                # Graphicgroups.explosion_group.add(explosion)
                Graphicgroups.explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(Constants.SOUND_SHIP_WAS_HIT)
                Game_Objects.player.respawn()

    # if player hits enemy debris
    for bits in Graphicgroups.debris:
        if Game_Objects.player.shipcollision == True and Variables.player_cannot_die == False:
            if bits.collide(Game_Objects.player.hitbox):
                Graphicgroups.debris.pop(Graphicgroups.debris.index(bits))
                explosion = Game_Objects.Explosion(bits.x, bits.y,Constants.SURF_EXPLOSION,0.25,False)
                ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.SURF_EXPLOSION,1,False)
                Graphicgroups.explosion_group.add(explosion)
                Graphicgroups.explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(Constants.SOUND_SHIP_WAS_HIT)
                Game_Objects.player.respawn()

    # if player hits Wall of Death
    for wod in Graphicgroups.wallsegments:
        if Game_Objects.player.shipcollision == True and Variables.player_cannot_die == False:
            if wod.collide(Game_Objects.player.hitbox):
                ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.SURF_EXPLOSION,1,False)
                Graphicgroups.explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(Constants.SOUND_SHIP_WAS_HIT)
                Game_Objects.player.respawn()

    # if player hits scenery
    for scenery in Graphicgroups.scenery:
        if Game_Objects.player.shipcollision == True and Variables.player_cannot_die == False:
            if scenery.collide(Game_Objects.player.hitbox):
                ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.SURF_EXPLOSION,1,False,xvel=120)
                Graphicgroups.explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(Constants.SOUND_SHIP_WAS_HIT)
                Game_Objects.player.respawn()
    #endregion

    #region Wrong Kana on Correct Kana
    for kana in Graphicgroups.incorrectkanas:
        for ckana in Graphicgroups.correctkanas:
            if kana.collide(ckana.centered_image):
                pygame.mixer.Sound.play(Constants.SOUND_GOODHIT)
                Graphicgroups.incorrectkanas.pop(Graphicgroups.incorrectkanas.index(kana))
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.SURF_EXPLOSION,0.5,False)
                Graphicgroups.explosion_group.add(explosion)
    #endregion

    #region Kana
    # If Correct kana hits scenery
    for kana in Graphicgroups.correctkanas:
        for scenery in Graphicgroups.scenery:
            if scenery.collide(kana.hitbox):
                if kana.bounced == False:
                    kana.yvelocity *= -1
                    kana.bounced = True

    # If Incorrect kana hits scenery
    for kana in Graphicgroups.incorrectkanas:
        for scenery in Graphicgroups.scenery:
            if scenery.collide(kana.hitbox):
                if kana.bounced == False:
                    kana.yvelocity *= -1
                    kana.bounced = True
    #endregion




#region FIND SUBLIST BY CHARACTER
def find_sublist_by_character(matrix, character):
    for index, sublist in enumerate(matrix):
        if character in sublist:
            return sublist
    return None




#region IS SLICE IN LIST
def is_slice_in_list(slice,list):
    len_s = len(slice) #so we don't recompute length of s on every iteration
    return any(slice == list[i:len_s+i] for i in range(len(list) - len_s+1))




#region SHARED CONTROLS
def sharedcontrols(event):
    import Constants, Game_Objects, Variables, Graphicgroups, Settings
    import pygame, random

    if event.key == ord('l'):
        if Game_Objects.player.lasersight == True:
            Game_Objects.player.lasersight = False
            pygame.mixer.Sound.stop(Constants.SOUND_SHIP_LASER)
            Game_Objects.player.laserlength = 0
        else:
            Game_Objects.player.lasersight = True
            pygame.mixer.Sound.play(Constants.SOUND_SHIP_LASER)
            Game_Objects.player.lasersightcounter = Game_Objects.player.poweruptimelength
    if event.key == ord('h'):
        if Variables.hitboxshow == True:
            Variables.hitboxshow = False
            Variables.debugwindow = False
        else:
            Variables.hitboxshow = True
            Variables.debugwindow = True
    if event.key == ord('k'): Game_Objects.player.kanaswitch = True
    if event.key == ord('p'): 
        if Variables.paused == False:
            Variables.paused = True
            pygame.mixer.music.pause()
        else:
            Variables.paused = False
            pygame.mixer.music.unpause()
    if event.key == ord('j'): Game_Objects.SpaceJunk.spawn()
    if event.key == ord('i'): Game_Objects.WallOfDeath.spawn(Constants.WIDTH,0)
    if event.key == ord('b'): 
        segment = 15
        columns = [1,2,3,4,5,6,7,8]
        random.shuffle(columns)
        Graphicgroups.bossmodecorrectkana.append(
            Game_Objects.BossModeKana(
                x=columns[0] * Constants.WIDTH/segment, 
                y=-100,
                kana=Variables.kananum,
                group=Graphicgroups.bossmodecorrectkana,
                fade=random.randint(Constants.min_kana_alpha,256),
                rotate=random.randint(-Settings.kana_rotate_rate,Settings.kana_rotate_rate))
        )
        columns.pop(0)
        for f in columns:
            selection = random.randint(0,Variables.levels[Variables.level]-1)
            if selection != Variables.kananum:
                Graphicgroups.bossmodeincorrectkana.append(
                    Game_Objects.BossModeKana(
                        x=f * Constants.WIDTH/segment, 
                        y=-100,
                        kana=selection,
                        group=Graphicgroups.bossmodeincorrectkana,
                        fade=random.randint(Constants.min_kana_alpha,256),
                        rotate=random.randint(-Settings.kana_rotate_rate,Settings.kana_rotate_rate))
                )
    if event.key == ord('q'): Game_Objects.achievements.tingtangarray = ['u', 'i', 'u', 'a', 'a']
    if event.key == ord('n'): Variables.transition = True
    if event.key == ord('u'):
        powerup_type = random.randint(1,2)
        Game_Objects.AnimatedPowerUp.spawn(
            Constants.ARRAY_POWERUP[powerup_type]["xvel"],
            Constants.ARRAY_POWERUP[powerup_type]["surfindx"],
            Constants.ARRAY_POWERUP[powerup_type]["pueffect"],
            )
    if event.key == ord('e'): Game_Objects.Enemies.spawn()
    if event.key == ord('r'): Game_Objects.BigLaserWarning.spawn(Game_Objects.player)
    if event.key == ord('.'): 
        if Game_Objects.player.pewtype < len(Constants.ARRAY_PLAYER_PEW)-1: Game_Objects.player.pewtype += 1
    if event.key == ord(','): 
        if Game_Objects.player.pewtype > 0: Game_Objects.player.pewtype -= 1
    if event.key == ord('='): Variables.score += 10
    if event.key == ord('-'): Variables.score -= 10
    if event.key == ord('9'): Variables.musicvolume -=0.01
    if event.key == ord('0'): Variables.musicvolume +=0.01
    if event.key == ord('8'): Game_Objects.TipTicker.spawn(Constants.TIPS[0],200)
    if event.key == ord('1'):
        if Constants.ARRAY_BOSSES[Variables.level]["shield"] >= 1:
            Constants.ARRAY_BOSSES[Variables.level]["shield"] -= 10
    if event.key == ord('t'):
        Graphicgroups.turrets.append(Game_Objects.GroundTurret(Constants.WIDTH+32,Constants.PAHEIGHT-64,0))
    if event.key == ord('m'): 
        if Variables.missiles_enabled == True:
            Variables.missiles_enabled = False
        else:
            Variables.missiles_enabled = True
    if event.key == ord('5'):
        Game_Objects.Debris.spawn(
            x=Constants.WCENTER,
            y=Constants.HCENTER,
            mindir=0,
            maxdir=359,
            minvel=50,
            maxvel=200,
            image=Constants.SURF_DEBRIS,
            origin=Constants.SCREEN,
            numdebris=100
        )




#region READ FROM CSV
def read_csv(file_name):
    with open(file_name, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        all_questions = [[row[0], row[1], row[2], row[3]] for row in reader]
    return all_questions




#region WRITE TO CSV
def write_csv(file_name,csv_object):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(csv_object)




#region UI TEXT
def uitext(screen):
    import Variables, Constants, Settings, Game_States, Game_Objects

    #region Score
    if Variables.score <=0: Variables.score = 0
    scoretext = Constants.UI_FONT.render("Score: " + str(Variables.score), True, 'white')
    screen.blit(scoretext, Settings.score_position)
    #endregion Score

    #region Lives
    livestext = Constants.UI_FONT.render("Lives: " + str(Game_Objects.player.lives), True, 'white')
    screen.blit(livestext, Settings.lives_position)
    #endregion

    #region Level
    leveltext = Constants.UI_FONT.render("Level: " + str(Variables.level+1), True, 'white')
    screen.blit(leveltext, Settings.level_position)
    #endregion

    #region Last 5 Kana
    position = [Constants.WIDTH-150,Constants.HEIGHT-Settings.uitop]
    if len(Game_Objects.achievements.tingtangarray) > 0:
        output = []
        for element in range(len(Game_Objects.achievements.tingtangarray)):
            output.append(find_sublist_by_character(Variables.commasep, Game_Objects.achievements.tingtangarray[element]))
    else: output = "None"

    titletext = Constants.UI_FONT.render("Previous Kana:",True,'white')
    screen.blit(titletext, (position[0]-210,position[1]))
    for n in range(len(output)):
        uikanatext = Constants.UI_FONT.render(str(output[n][0]),True, 'white').convert_alpha()
        uikanatext.set_alpha(100+(n*50))
        screen.blit(uikanatext, position)
        position[0] += 25
    #endregion

    #region Boss
    if Variables.current_game_state == "Boss":
        bonustext = Constants.UI_FONT.render("Bonus: " + str(Game_States.boss_state.bonus_score), True, 'white')
        screen.blit(bonustext, Settings.bonus_position)
        shieldtext = Constants.UI_FONT.render("BOSS SHIELD", True, 'white')
        screen.blit(shieldtext, Settings.shieldtext_position)
    #endregion




#region SCALE SURFACE FROM CENTER
def scale_surface_from_center(surface, scale_factor):
    import pygame
    original_rect = surface.get_rect()
    scaled_width = int(original_rect.width * scale_factor)
    scaled_height = int(original_rect.height * scale_factor)
    scaled_surface = pygame.transform.scale(surface, (scaled_width, scaled_height))
    scaled_rect = scaled_surface.get_rect(center=original_rect.center)
    return scaled_surface, scaled_rect




#region QUESTION TEXT
def question_text(screen):
    import Graphicgroups, Constants, Variables, math, Settings
    # if Variables.STATE == "Boss":
    #     shoot_text = Constants.ui_font.render('Boss Fight', True, 'white')
    #     screen.blit(shoot_text, (Settings.question_position[0]-120,Settings.question_position[1]+13))
    # else:
    if len(Graphicgroups.cuttoffline) < 1:
        shoot_text = Constants.UI_FONT.render('Collect', True, 'white')
        romajitext = Constants.QUESTION_FONT.render(Variables.gamekana[Variables.level][Variables.kananum][2], True, 'white')
        Variables.theta += 5 * Variables.delta_time
        theta_scale = math.sin(Variables.theta)
        romaji_scaled, romaji_rect = scale_surface_from_center(romajitext, 1.5 + (theta_scale*.5))
        screen.blit(shoot_text, (Settings.question_position[0]-120,Settings.question_position[1]+13))
        screen.blit(romaji_scaled, (romaji_rect[0]+Settings.question_position[0],romaji_rect[1]+Settings.question_position[1]))




#region SINGLE OBJECT ANIMATE
def soanimate(self,loopstart=0,loopend=9999):
    import Variables
    self.animindex += self.animspeed * Variables.delta_time #length of ime before we advance the animation frame
    if self.animindex > len(self.spritearray.images)-1 or self.animindex > loopend: self.animindex = loopstart # reset the frame to 0 if we try to go beyond the array
    self.image = self.spritearray.images[int(self.animindex)] # update the current frame




#region MULTI OBJECT ANIMATE
def moanimate(self,loopstart=0,loopend=9999):
    import Variables
    self.animindex += self.animspeed * Variables.delta_time #length of ime before we advance the animation frame
    if self.animindex > len(self.spritearray[self.type].images)-1 or self.animindex > loopend: self.animindex = loopstart # reset the frame to 0 if we try to go beyond the array
    self.image = self.spritearray[self.type].images[int(self.animindex)] # update the current frame




#region GET MAX SHIP?
def getmaxship():
    TotalKanaPoints = 0
    import Variables, Settings
    for sep in Variables.commasep:
        TotalKanaPoints += int(sep[3])
    return TotalKanaPoints / ((Settings.num_to_shoot_new_kana+1)*len(Variables.commasep))




#region PLAYSOUND (defunct)
def playsound(sound,channel,maxchannel=2,bleed=True):
    import pygame
    soundchannel = pygame.mixer.Channel(channel)
    if bleed == False:
        soundchannel.play(sound)
    else:
        while soundchannel.get_busy():
            print(soundchannel,channel)
            if channel <= maxchannel:
                soundchannel = pygame.mixer.Channel(channel)
                channel += 1
        soundchannel.play(sound)




#region KANALIST (bottom of screen)
def kanalist(screen,alpha):
    import Graphicgroups, Variables, Settings, Constants

    Graphicgroups.kanalist.clear()
    upperbound = Variables.level
    lowerbound = upperbound - 2
    if lowerbound < 0:
        for kana in range(int(Variables.levels[upperbound])): Graphicgroups.kanalist.append(Variables.commasep[kana])
        for kana in range(int(Variables.levels[upperbound])):
            kanakill = int(Variables.commasep[kana][3])*(255/Settings.num_to_shoot_new_kana)
            if kanakill >= 255: kanakill = 255
            kanalistthing = Constants.UI_FONT.render(Graphicgroups.kanalist[kana][Variables.gamemode], True, (kanakill,255,kanakill))
            kanalistthing.set_alpha(alpha)
            screen.blit(kanalistthing,(25+(27*kana),Constants.PAHEIGHT-30))
    else:
        for kana in range(int(Variables.levels[upperbound])): Graphicgroups.kanalist.append(Variables.commasep[kana])
        char = 0
        for kana in range(int(Variables.levels[lowerbound]),int(Variables.levels[upperbound])):
            kanakill = int(Variables.commasep[kana][3])*(255/Settings.num_to_shoot_new_kana)
            if kanakill >= 255: kanakill = 255
            kanalistthing = Constants.UI_FONT.render(Graphicgroups.kanalist[kana][Variables.gamemode], True, (kanakill,255,kanakill))
            kanalistthing.set_alpha(alpha)
            screen.blit(kanalistthing,(25+(27*char),Constants.PAHEIGHT-30))
            char += 1




#region LONG PEW
def longpew(keys,buildupsound,bigpewready,brewsprite,pewsprite):
    import Graphicgroups, Variables, Game_Objects
    import pygame
    if keys[pygame.K_SPACE]:                                                                                # We press a key
        Game_Objects.player.hasfired = False                                                                # Reset the flag showing the bullet has not been fired
        if Game_Objects.player.laserbuild <=10: Game_Objects.player.laserbuild += 3 * Variables.delta_time  # If the build time is <= 10, build the value for the size of the bullet whil the key is still pressed
        else: pygame.mixer.Sound.stop(buildupsound)                                                         # If the build time is > 10, Stop the sound of the build up
        if Game_Objects.player.laserbuild >= 5 and Game_Objects.player.bigpewreadyplayed == False:           # If both 5 has gone by and bigpewready has not been played yet
            pygame.mixer.Sound.play(bigpewready)                                                            # Play the (donk) sound
            Game_Objects.player.bigpewreadyplayed = True                                                    # Set the flag showing that bigpewready has been played
        if Game_Objects.player.buildupsoundplayed == False and Game_Objects.player.laserbuild > 1.5:        # Check to see if we have started playing the sound yet
            Graphicgroups.brew.append(Game_Objects.DynamicPew(
                x=Game_Objects.player.location[0],
                y=Game_Objects.player.location[1],
                spritearray=brewsprite,
                startframe=0,
                sizex=Game_Objects.player.laserbuild,
                sizey=Game_Objects.player.laserbuild,
                parent=True,
                loopstart=30,
                loopend=70
            ))
            pygame.mixer.Sound.play(buildupsound)                                                           # Play the sound
            Game_Objects.player.buildupsoundplayed = True                                                   # Set the flag showing we have played the sound
        try: 
            for brew in Graphicgroups.brew: brew.sizex = Game_Objects.player.laserbuild
            for brew in Graphicgroups.brew: brew.sizey = Game_Objects.player.laserbuild
        except: pass
    else:                                                                                                   # The key is not being pressed
        try: Graphicgroups.brew.clear()
        except: pass
        pygame.mixer.Sound.stop(buildupsound)                                                               # Stop the sound of the build up
        Game_Objects.player.buildupsoundplayed = False                                                      # Reset the flag that the build up sound can be played again
        Game_Objects.player.bigpewreadyplayed = False                                                       # Reset the confirmation sound can be played again
        if Game_Objects.player.hasfired == False and Game_Objects.player.laserbuild > 5:                    # check to see if the bullet has been fired 
            Game_Objects.DynamicPew.spawn(
                Game_Objects.player,                # players X and Y position as a tuple
                Game_Objects.player.laserbuild*5,   # Sizex * 5
                Game_Objects.player.laserbuild,     # Size Y
                pewsprite,                          # Sprite to show for Pew
                Game_Objects.player.laserbuild
            )                                                                                               # Create a bullet with the size set by holding the key down
            Game_Objects.player.hasfired = True                                                             # Set the flag stating the bullet has been fired
        else:
            if Game_Objects.player.hasfired == False:
                Game_Objects.Pew.spawn(Game_Objects.player)
            Game_Objects.player.hasfired = True
        Game_Objects.player.laserbuild = 1                                                                  # Reset the size




#region MISSILE PEW
def missilepew(keys,target):
    import Graphicgroups, Constants, Game_Objects
    import pygame, random
    if keys[pygame.K_SPACE]:
        if pygame.time.get_ticks() - Game_Objects.player.last_missiletimer >= 1000:
            if len(Graphicgroups.missiles) < 1:
                try:
                    maxnum = len(target)
                    rndobject = random.randint(0,maxnum-1)
                    if Game_Objects.player.location[1] > target[rndobject].y: ypos = -2
                    if Game_Objects.player.location[1] < target[rndobject].y: ypos = 2
                    pygame.mixer.Sound.play(Constants.SOUND_MISSILE_LAUNCHED)
                    Graphicgroups.missiles.append(Game_Objects.HomingMissile(
                        x=Game_Objects.player.location[0],
                        y=Game_Objects.player.location[1],
                        target=target[rndobject],
                        targetgroup = target,
                        ypos=ypos,
                        image=Constants.SURF_MISSILE[0]
                    ))
                    Game_Objects.player.last_missiletimer = pygame.time.get_ticks()
                except: pass




#region RESET GAME VARs
def reset_game(): #Executed when pressing START
    import Variables, Graphicgroups, Game_Objects, Settings, Game_States

    #region Clear Object Arrays
    Graphicgroups.animatedpowerup.clear()
    Graphicgroups.centerwarning.clear()
    Graphicgroups.bullets.clear()
    Graphicgroups.incorrectkanas.clear()
    Graphicgroups.kanalist.clear()
    Graphicgroups.correctkanas.clear()
    Graphicgroups.bridge_group.empty()
    Graphicgroups.cuttoffline.clear()
    # Graphicgroups.powerups.clear()
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
    Graphicgroups.explosion_group.clear
    Graphicgroups.bossmodecorrectkana.clear()
    Graphicgroups.bossmodeincorrectkana.clear()
    #endregion Clear Object Arrays

    #region Reset Flags
    Variables.bossstate = False
    Variables.gamestate = False
    Variables.transition = False
    Variables.bossexist = False
    Game_Objects.player.shipcollision = True
    Game_States.game_state.done = False
    Game_States.boss_state.done = False
    Game_States.gameover_state.done = False
    #endregion Reset Flags

    #region Reset Values
    Game_States.game_state.enemy_wait_timer = 10
    Variables.kananum = 0
    Game_Objects.player.pewtype = 0
    Variables.laserpower = 1
    Variables.enemy_health_multiplier = 0
    Variables.score = 0
    Variables.generatedcorrectkanacounter = 0
    Variables.generatedincorrectkanacounter = 0
    Game_Objects.player.lives = Settings.maxlives
    #endregion Reset Values

    #region Reset Timers
    Game_Objects.timer.bridge_timer = 0
    Game_Objects.timer.powerup_timer = 0
    #endregion Reset Timers
