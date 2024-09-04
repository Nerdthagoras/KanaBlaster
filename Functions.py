import csv

def collision():
    import Graphicgroups, Constants, Game_Objects, Variables, Settings
    import pygame, random, math, os
    # If it is a projectile, then it will hit something, 
    # if it is not a projectile then the ship is considered the projectile
    # Space Junk will be treated like a projectile because it persists after collision
    
    maxexplode = random.randint(0,len(Constants.explosion_surfs)-1) # pick random explosion type
    
    #region Player Projectiles
    for bullet in Graphicgroups.bullets:

        #if player's bullet hits Wall of Death
        for wod in Graphicgroups.wallsegments:
            if wod.collide(bullet.rect):
                Graphicgroups.wallsegments.pop(Graphicgroups.wallsegments.index(wod))
                try:
                    persist = Constants.pew_array[Game_Objects.player.pewtype]["persist"]
                    if not persist:
                        Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                except: pass
                Game_Objects.Debris.spawn(wod.x,wod.y,math.radians(random.randint(-10,10)),random.randint(100,300),Constants.brick_surf,0)
                pygame.mixer.Sound.play(Constants.brickbreak_sound)
                explosion = Game_Objects.Explosion(wod.x, wod.y,Constants.explosion_surfs,0.5,False)
                Graphicgroups.explosion_group.add(explosion)
                Variables.score += 1

        # if player's bullet hits CORRECT Kana
        for ckana in Graphicgroups.correctkanas:    
            if ckana.collide(bullet.rect):
                Variables.RGB[0] = 128
                pygame.mixer.Sound.play(Constants.badhit)
                kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', ckana.kanasound + '.wav'))
                pygame.mixer.Sound.play(kana_sound)
                if ckana.x >= 2*Constants.WIDTH // 3:
                    Variables.score -= 3
                elif ckana.x > Constants.WIDTH // 3 and ckana.x < 2*Constants.WIDTH // 3:
                    Variables.score -= 2
                else:
                    Variables.score -= 1
                explosion = Game_Objects.Explosion(ckana.x, ckana.y,Constants.explosion_surfs,0.5,False,explosiontype=maxexplode,xvel=(Constants.pew_array[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                Graphicgroups.explosion_group.add(explosion)
                try:
                    persist = Constants.pew_array[Game_Objects.player.pewtype]["persist"]
                    if not persist:
                        Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                except: pass
                Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(ckana))
                # kanaint = int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3])
                # if kanaint <= num_to_shoot_new_kana: kanaint += 1
                #Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3] = kanaint

        # if player's bullet hits WRONG kana
        for kana in Graphicgroups.kanas:
            if kana.collide(bullet.rect):
                Variables.RGB[1] = 64
                pygame.mixer.Sound.play(Constants.goodhit)
                Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                try:
                    persist = Constants.pew_array[Game_Objects.player.pewtype]["persist"]
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
                            Constants.powerup_array[3]["xvel"],
                            Constants.powerup_array[3]["surfindx"],
                            Constants.powerup_array[3]["pueffect"],
                        )
                elif kana.x > Constants.WIDTH // 3 and kana.x < 2*Constants.WIDTH // 3:
                    Variables.score += 2
                else:
                    Variables.score += 1
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False,explosiontype=maxexplode,xvel=(Constants.pew_array[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                Graphicgroups.explosion_group.add(explosion)
                Game_Objects.achievements.tingtangarray.append(kana.kanasound)
                Game_Objects.achievements.tingtangshow = True

        # if player's bullet hits Enemy
        for enemy in Graphicgroups.enemies:
            if enemy.collide(bullet.rect):
                pygame.mixer.Sound.play(Constants.goodhit)
                damage = 1 + random.randint(int(Game_Objects.player.laserpower/5),Game_Objects.player.laserpower)
                enemy.health -= damage
                Game_Objects.Debris.spawn(enemy.enemy_rect.centerx,enemy.y,math.radians(random.randint(80,280)),random.randint(50,200),Constants.debris_surf,Graphicgroups.enemies.index(enemy))
                Game_Objects.Damagenum.spawn(enemy.enemy_rect.centerx,0,enemy.y,damage)
                enemy.knockbackx = Settings.enemy_max_knockbackx
                enemy.knockbacky = enemy.collide(bullet.rect)
                if enemy.health <= 0:
                    Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                    explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                    Variables.score += 1
                    powerup_chance = random.randint(0,Settings.enemy_powerup_freq)
                    if powerup_chance == 0:
                        Game_Objects.AnimatedPowerUp.spawn(
                            Constants.powerup_array[3]["xvel"],
                            Constants.powerup_array[3]["surfindx"],
                            Constants.powerup_array[3]["pueffect"],
                        )

                try:
                    persist = Constants.pew_array[Game_Objects.player.pewtype]["persist"]
                    if not persist:
                        Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                except: pass

        # if player's bullet hits Boss
        for boss in Graphicgroups.bosses:
            if boss.collide(bullet.rect):
                pygame.mixer.Sound.play(Constants.goodhit)
                damage = random.randint(int(Game_Objects.player.laserpower / 10),int(Game_Objects.player.laserpower))
                boss.health -= damage
                Game_Objects.Debris.spawn(boss.boss_rect.centerx,boss.y,math.radians(random.randint(80,280)),random.randint(50,200),Constants.debris_surf,Graphicgroups.bosses.index(boss))
                Game_Objects.Damagenum.spawn(boss.boss_rect.centerx,boss.velocity,boss.y,damage)
                if boss.health <= 0:
                    Graphicgroups.bosses.pop(Graphicgroups.bosses.index(boss))
                    explosion = Game_Objects.Explosion(boss.x, boss.y,Constants.explosion_surfs,8,False,xvel=(Constants.pew_array[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                    Graphicgroups.explosion_group.add(explosion)
                    Variables.score += 99
                    Variables.TRANSITION = False
                try: Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                except: pass

        # if player's bullet hits powerup
        for powerup in Graphicgroups.animatedpowerup:
            if powerup.collide(bullet.rect):
                pygame.mixer.Sound.play(Constants.badhit)
                explosion = Game_Objects.Explosion(powerup.x, powerup.y,Constants.explosion_surfs,0.5,False,xvel=(Constants.pew_array[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                Graphicgroups.explosion_group.add(explosion)
                try:
                    persist = Constants.pew_array[Game_Objects.player.pewtype]["persist"]
                    if not persist:
                        Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                except: pass
                Graphicgroups.animatedpowerup.pop(Graphicgroups.animatedpowerup.index(powerup))

        # if player's bullet hits ship debirs
        for shipdeb in Graphicgroups.debris:
            if shipdeb.collide(bullet.rect):
                pygame.mixer.Sound.play(Constants.goodhit)
                explosion = Game_Objects.Explosion(shipdeb.x, shipdeb.y,Constants.explosion_surfs,0.2,False,xvel=(Constants.pew_array[Game_Objects.player.pewtype]["pewspeed"])/Settings.explode_vel_frac*-1)
                Graphicgroups.explosion_group.add(explosion)
                try:
                    persist = Constants.pew_array[Game_Objects.player.pewtype]["persist"]
                    if not persist:
                        Graphicgroups.bullets.pop(Graphicgroups.bullets.index(bullet))
                except: pass
                Graphicgroups.debris.pop(Graphicgroups.debris.index(shipdeb))

    #endregion
    
    #region Enemy Projectiles
    for epew in Graphicgroups.enemyprojectiles:
        # if hit Player
        if Game_Objects.player.shipcollision == True:
            if epew.collide(Game_Objects.player.spaceship_rect):
                Graphicgroups.enemyprojectiles.pop(Graphicgroups.enemyprojectiles.index(epew))
                explosion = Game_Objects.Explosion(epew.x, epew.y,Constants.explosion_surfs,0.5,False)
                ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                Graphicgroups.explosion_group.add(explosion)
                Graphicgroups.explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(Constants.shiphit)
                Game_Objects.player.respawn()

        # if hit other enemy
        for enemy in Graphicgroups.enemies:
            if Settings.enemiescanshooteachother and enemy.collide(epew.hitbox) and epew.origin != Graphicgroups.enemies.index(enemy):
                pygame.mixer.Sound.play(Constants.goodhit)
                damage = 1 + int(Variables.enemy_health_multiplier * Settings.enemy_health * 0.2)
                enemy.health -= damage
                Game_Objects.Debris.spawn(enemy.enemy_rect.centerx,enemy.y,math.radians(random.randint(80,280)),random.randint(50,200),Constants.debris_surf,Graphicgroups.enemies.index(enemy))
                Game_Objects.Damagenum.spawn(enemy.enemy_rect.centerx,enemy.velocity,enemy.y,damage)
                if enemy.health == 0:
                    Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                    explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                try: Graphicgroups.enemyprojectiles.pop(Graphicgroups.enemyprojectiles.index(epew))
                except: pass

        # if WRONG kana
        for kana in Graphicgroups.kanas:
            if kana.collide(epew.hitbox):
                Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                try: Graphicgroups.enemyprojectiles.pop(Graphicgroups.enemyprojectiles.index(epew))
                except: pass
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                Graphicgroups.explosion_group.add(explosion)
                pygame.mixer.Sound.play(Constants.goodhit)

        # if CORRECT kana
        for kana in Graphicgroups.correctkanas:
            if kana.collide(epew.hitbox):
                Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(kana))
                try: Graphicgroups.enemyprojectiles.pop(Graphicgroups.enemyprojectiles.index(epew))
                except: pass
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                Graphicgroups.explosion_group.add(explosion)
                pygame.mixer.Sound.play(Constants.goodhit)
    #endregion

    #region BIG LASER
    # if BIG LASER hits player
    for biglaser in Graphicgroups.biglasers:
        if Game_Objects.player.shipcollision == True:
            if biglaser.collide(Game_Objects.player.spaceship_rect):
                ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                Graphicgroups.explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(Constants.shiphit)
                Game_Objects.player.respawn()

        # correctKana hit by BIG LASER
        for kana in Graphicgroups.correctkanas:
            if kana.collide(biglaser.hitbox):
                pygame.mixer.Sound.play(Constants.goodhit)
                try: Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(kana))
                except: pass
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False,xvel=biglaser.velocity/12)
                Graphicgroups.explosion_group.add(explosion)

        # Wrong Kana hit by BIG LASER
        for kana in Graphicgroups.kanas:
            if kana.collide(biglaser.hitbox):
                pygame.mixer.Sound.play(Constants.goodhit)
                try: Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                except: pass
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False,xvel=biglaser.velocity/12)
                Graphicgroups.explosion_group.add(explosion)

        # if enemy hit by BIG LASER
        for enemy in Graphicgroups.enemies:
            if enemy.collide(biglaser.hitbox):
                pygame.mixer.Sound.play(Constants.goodhit)
                Variables.score += 1
                explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.explosion_surfs,0.5,False,xvel=biglaser.velocity/12)
                Graphicgroups.explosion_group.add(explosion)
                try: Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                except: pass

        # if powerup hit by BIG LASER
        for powerup in Graphicgroups.powerups:
            if powerup.collide(biglaser.hitbox):
                explosion = Game_Objects.Explosion(powerup.x, powerup.y,Constants.explosion_surfs,0.5,False,xvel=biglaser.velocity/12)
                pygame.mixer.Sound.play(Constants.goodhit)
                Graphicgroups.explosion_group.add(explosion)
                try: Graphicgroups.powerups.pop(Graphicgroups.powerups.index(powerup))
                except: pass

        #if BIG LASER hits wall segments
        for wod in Graphicgroups.wallsegments:
            if wod.collide(biglaser.hitbox):
                Graphicgroups.wallsegments.pop(Graphicgroups.wallsegments.index(wod))
                Game_Objects.Debris.spawn(wod.x,wod.y,math.radians(random.randint(-10,10)),random.randint(100,300),Constants.brick_surf,0)
                pygame.mixer.Channel(0).play(Constants.brickbreak_sound)
                explosion = Game_Objects.Explosion(wod.x, wod.y,Constants.explosion_surfs,0.5,False,xvel=biglaser.velocity/12)
                Graphicgroups.explosion_group.add(explosion)

    #endregion

    #region Space Junk
    for junk in Graphicgroups.spacejunk:
        # correctKana hit by junk
        for kana in Graphicgroups.correctkanas:
            if kana.collide(junk.hitbox):
                pygame.mixer.Sound.play(Constants.goodhit)
                Graphicgroups.correctkanas.pop(Graphicgroups.correctkanas.index(kana))
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                Graphicgroups.explosion_group.add(explosion)

        # Wrong Kana hit by junk
        for kana in Graphicgroups.kanas:
            if kana.collide(junk.hitbox):
                pygame.mixer.Sound.play(Constants.goodhit)
                Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                Graphicgroups.explosion_group.add(explosion)

        # Wall segments hit by junk
        for wod in Graphicgroups.wallsegments:
            if wod.collide(junk.hitbox):
                Graphicgroups.wallsegments.pop(Graphicgroups.wallsegments.index(wod))
                Game_Objects.Debris.spawn(wod.x,wod.y,math.radians(random.randint(-10,10)),random.randint(100,300),Constants.brick_surf,0)
                pygame.mixer.Sound.play(Constants.brickbreak_sound)
                explosion = Game_Objects.Explosion(wod.x, wod.y,Constants.explosion_surfs,0.5,False)
                Graphicgroups.explosion_group.add(explosion)

    #endregion

    #region Enemy Debris
    for edebs in Graphicgroups.debris:
        # if enemy debris hits Enemy
        for enemy in Graphicgroups.enemies:
            if enemy.collide(edebs.hitbox) and edebs.origin != Graphicgroups.enemies.index(enemy):
                pygame.mixer.Sound.play(Constants.goodhit)
                damage = 1 + int(Variables.enemy_health_multiplier * Settings.enemy_health * 0.2)
                enemy.health -= damage
                Game_Objects.Debris.spawn(enemy.enemy_rect.centerx,enemy.y,math.radians(random.randint(80,280)),random.randint(50,200),Constants.debris_surf,Graphicgroups.enemies.index(enemy))
                Game_Objects.Damagenum.spawn(enemy.enemy_rect.centerx,enemy.velocity,enemy.y,damage)
                if enemy.health == 0:
                    Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                    explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.explosion_surfs,0.5,False)
                    Graphicgroups.explosion_group.add(explosion)
                try: Graphicgroups.debris.pop(Graphicgroups.debris.index(edebs))
                except: pass
        pass
    #endregion Enemy Debris

    #region Ship
    # if player's ship hits correct kana
    for kana in Graphicgroups.correctkanas:
        if Game_Objects.player.shipcollision == True:
            if kana.collide(Game_Objects.player.spaceship_rect):
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
                kanaint = int(Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3])
                if kanaint <= Settings.num_to_shoot_new_kana: kanaint += 1
                Variables.commasep[Variables.commasep.index(Variables.gamekana[Variables.level][Variables.kananum])][3] = kanaint
                Game_Objects.achievements.tingtangarray.append(kana.kanasound)
                Game_Objects.achievements.tingtangshow = True
                #player.respawn()

        # if player hits kana
    
    # if player's ship hits wrong kana
    for kana in Graphicgroups.kanas:
        if Game_Objects.player.shipcollision == True:
            if kana.collide(Game_Objects.player.spaceship_rect):
                Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                Graphicgroups.explosion_group.add(explosion)
                Graphicgroups.explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(Constants.shiphit)
                kana_sound = pygame.mixer.Sound(os.path.join('sounds','kana', Variables.gamekana[Variables.level][kana.kana][2] + '.wav'))
                pygame.mixer.Sound.play(kana_sound)
                Game_Objects.player.respawn()

    # if player hits Enemy
    for enemy in Graphicgroups.enemies:
        if Game_Objects.player.shipcollision == True:
            if enemy.collide(Game_Objects.player.spaceship_rect):
                Graphicgroups.enemies.pop(Graphicgroups.enemies.index(enemy))
                explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.explosion_surfs,0.5,False)
                ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                Graphicgroups.explosion_group.add(explosion)
                Graphicgroups.explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(Constants.shiphit)
                Game_Objects.player.respawn()

    # if player hits Boss
    for enemy in Graphicgroups.bosses:
        if Game_Objects.player.shipcollision == True:
            if enemy.collide(Game_Objects.player.spaceship_rect):
                # Graphicgroups.bosses.pop(Graphicgroups.bosses.index(enemy))
                # explosion = Game_Objects.Explosion(enemy.x, enemy.y,Constants.explosion_surfs,0.5,False)
                ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                # Graphicgroups.explosion_group.add(explosion)
                Graphicgroups.explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(Constants.shiphit)
                Game_Objects.player.respawn()

    # if player hits enemy debris
    for bits in Graphicgroups.debris:
        if Game_Objects.player.shipcollision == True:
            if bits.collide(Game_Objects.player.spaceship_rect):
                Graphicgroups.debris.pop(Graphicgroups.debris.index(bits))
                explosion = Game_Objects.Explosion(bits.x, bits.y,Constants.explosion_surfs,0.25,False)
                ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                Graphicgroups.explosion_group.add(explosion)
                Graphicgroups.explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(Constants.shiphit)
                Game_Objects.player.respawn()

    # if player hits Wall of Death
    for wod in Graphicgroups.wallsegments:
        if Game_Objects.player.shipcollision == True:
            if wod.collide(Game_Objects.player.spaceship_rect):
                ship_explosion = Game_Objects.Explosion(Game_Objects.player.spaceship_rect.center[0], Game_Objects.player.spaceship_rect.center[1],Constants.explosion_surfs,1,False)
                Graphicgroups.explosion_group.add(ship_explosion)
                pygame.mixer.Sound.play(Constants.shiphit)
                Game_Objects.player.respawn()
    #endregion

    #region Wrong Kana on Correct Kana
    for kana in Graphicgroups.kanas:
        for ckana in Graphicgroups.correctkanas:
            if kana.collide(ckana.centered_image):
                pygame.mixer.Sound.play(Constants.goodhit)
                Graphicgroups.kanas.pop(Graphicgroups.kanas.index(kana))
                explosion = Game_Objects.Explosion(kana.x, kana.y,Constants.explosion_surfs,0.5,False)
                Graphicgroups.explosion_group.add(explosion)
    #endregion

    #region Correct Kana
    for kana in Graphicgroups.correctkanas:
        for wod in Graphicgroups.wallsegments:
            if wod.collide(kana.hitbox):
                Graphicgroups.wallsegments.pop(Graphicgroups.wallsegments.index(wod))
                Game_Objects.Debris.spawn(wod.x,wod.y,math.radians(random.randint(-10,10)),random.randint(100,300),Constants.brick_surf,0)
                pygame.mixer.Sound.play(Constants.brickbreak_sound)
                explosion = Game_Objects.Explosion(wod.x, wod.y,Constants.explosion_surfs,0.5,False)
                Graphicgroups.explosion_group.add(explosion)
    #endregion

def find_sublist_by_character(matrix, character):
    for index, sublist in enumerate(matrix):
        if character in sublist:
            return sublist
    return None

def is_slice_in_list(s,l):
    len_s = len(s) #so we don't recompute length of s on every iteration
    return any(s == l[i:len_s+i] for i in range(len(l) - len_s+1))

def sharedcontrols(event):
    import Constants, Game_Objects, Variables, Graphicgroups, Settings
    import pygame, random, time

    if event.key == ord('l'):
        if Game_Objects.player.lasersight == True:
            Game_Objects.player.lasersight = False
            pygame.mixer.Sound.stop(Constants.shiplaser_sound)
            Game_Objects.player.laserlength = 0
        else:
            Game_Objects.player.lasersight = True
            pygame.mixer.Sound.play(Constants.shiplaser_sound)
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
        if Variables.PAUSED == False:
            Variables.PAUSED = True
            pygame.mixer.music.pause()
        else:
            Variables.PAUSED = False
            pygame.mixer.music.unpause()
    if event.key == ord('j'): Game_Objects.SpaceJunk.spawn()
    if event.key == ord('i'): Game_Objects.WallOfDeath.spawn(Constants.WIDTH,0)
    if event.key == ord('b'): Game_Objects.Bridge.spawn()
    if event.key == ord('q'): Game_Objects.achievements.tingtangarray = ['u', 'i', 'u', 'a', 'a']
    if event.key == ord('n'): Variables.TRANSITION = True
    if event.key == ord('e'): Game_Objects.Enemies.spawn()
    if event.key == ord('r'): Game_Objects.BigLaserWarning.spawn(Game_Objects.player)
    if event.key == ord('.'): 
        if Game_Objects.player.pewtype < len(Constants.pew_array)-1: Game_Objects.player.pewtype += 1
    if event.key == ord(','): 
        if Game_Objects.player.pewtype > 0: Game_Objects.player.pewtype -= 1
    if event.key == ord('='): Variables.score += 10
    if event.key == ord('-'): Variables.score -= 10
    if event.key == ord('9'): Variables.musicvolume -=0.01
    if event.key == ord('0'): Variables.musicvolume +=0.01
    if event.key == ord('8'): Game_Objects.TipTicker.spawn(Constants.tips[0],200)

def read_csv(file_name):
    with open(file_name, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        all_questions = [[row[0], row[1], row[2], row[3]] for row in reader]
    return all_questions

def write_csv(file_name,csv_object):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(csv_object)

def uitext(screen):
    import Variables, Constants, Settings, Game_States, Game_Objects

    #region SCORE
    if Variables.score <=0: Variables.score = 0
    scoretext = Constants.ui_font.render("Score: " + str(Variables.score), True, 'white')
    screen.blit(scoretext, Settings.score_position)
    #endregion SCORE

    #region LIVES
    livestext = Constants.ui_font.render("Lives: " + str(Game_Objects.player.lives), True, 'white')
    screen.blit(livestext, Settings.lives_position)
    #endregion

    #region LEVEL
    leveltext = Constants.ui_font.render("Level: " + str(Variables.level), True, 'white')
    screen.blit(leveltext, Settings.level_position)
    #endregion

    #region Last 5 Kana
    position = [Constants.WIDTH-300,30]
    if len(Game_Objects.achievements.tingtangarray) > 0:
        output = []
        for element in range(len(Game_Objects.achievements.tingtangarray)):
            output.append(find_sublist_by_character(Variables.commasep, Game_Objects.achievements.tingtangarray[element]))
    else: output = "None"

    titletext = Constants.ui_font.render("Previous Kana",True,'white')
    screen.blit(titletext, (position[0],position[1]-30))
    for n in range(len(output)):
        uikanatext = Constants.ui_font.render(str(output[n][0]),True, 'white').convert_alpha()
        uikanatext.set_alpha(100+(n*50))
        screen.blit(uikanatext, position)
        position[0] += 25
    #endregion

    #region Boss
    if Variables.STATE == "Boss":
        bonustext = Constants.ui_font.render("Bonus: " + str(Game_States.boss_state.bonus_score), True, 'white')
        screen.blit(bonustext, Settings.bonus_position)
    #endregion

def scale_surface_from_center(surface, scale_factor):
    import pygame
    original_rect = surface.get_rect()
    scaled_width = int(original_rect.width * scale_factor)
    scaled_height = int(original_rect.height * scale_factor)
    scaled_surface = pygame.transform.scale(surface, (scaled_width, scaled_height))
    scaled_rect = scaled_surface.get_rect(center=original_rect.center)
    return scaled_surface, scaled_rect

def question_text(screen):
    import Graphicgroups, Constants, Variables, math, Settings
    if Variables.STATE == "Boss":
        shoot_text = Constants.ui_font.render('Boss Fight', True, 'white')
        screen.blit(shoot_text, (Settings.question_position[0]-120,Settings.question_position[1]+13))
    else:
        if len(Graphicgroups.cuttoffline) < 1:
            shoot_text = Constants.ui_font.render('Collect', True, 'white')
            romajitext = Constants.question_font.render(Variables.gamekana[Variables.level][Variables.kananum][2], True, 'white')
            Variables.theta += 5 * Variables.delta_time
            theta_scale = math.sin(Variables.theta)
            romaji_scaled, romaji_rect = scale_surface_from_center(romajitext, 1.5 + (theta_scale*.5))
            screen.blit(shoot_text, (Settings.question_position[0]-120,Settings.question_position[1]+13))
            screen.blit(romaji_scaled, (romaji_rect[0]+Settings.question_position[0],romaji_rect[1]+Settings.question_position[1]))

def soanimate(self):
    import Variables
    self.animindex += self.animspeed * Variables.delta_time #length of ime before we advance the animation frame
    if self.animindex > len(self.spritearray.images)-1: self.animindex = 0 # reset the frame to 0 if we try to go beyond the array
    self.image = self.spritearray.images[int(self.animindex)] # update the current frame

def moanimate(self):
    import Variables
    self.animindex += self.animspeed * Variables.delta_time #length of ime before we advance the animation frame
    if self.animindex > len(self.spritearray[self.type].images)-1: self.animindex = 0 # reset the frame to 0 if we try to go beyond the array
    self.image = self.spritearray[self.type].images[int(self.animindex)] # update the current frame

def getmaxship():
    TotalKanaPoints = 0
    import Variables, Settings
    for sep in Variables.commasep:
        TotalKanaPoints += int(sep[3])
    return TotalKanaPoints / ((Settings.num_to_shoot_new_kana+1)*len(Variables.commasep))

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

def kanalist(screen,alpha):
    import Graphicgroups, Variables, Settings, Constants
    #region Bottom KANA LIST                                                                    # Bottom Kana List
    Graphicgroups.kanalist.clear()
    for kana in range(int(Variables.levels[Variables.level])): Graphicgroups.kanalist.append(Variables.commasep[kana])
    for kana in range(int(Variables.levels[Variables.level])):
        kanakill = int(Variables.commasep[kana][3])*(255/Settings.num_to_shoot_new_kana)
        if kanakill >= 255: kanakill = 255
        kanalistthing = Constants.ui_font.render(Graphicgroups.kanalist[kana][Variables.gamemode], True, (kanakill,255,kanakill))
        kanalistthing.set_alpha(alpha)
        screen.blit(kanalistthing,(25+(27*kana),Constants.HEIGHT-30))
    #endregion

def reset_game(): #Executed when pressing START
    import Variables, Graphicgroups, Game_Objects, Settings

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
    Graphicgroups.explosion_group.clear
    #endregion Clear Object Arrays

    #region Reset Flags
    Variables.BOSSSTATE = False
    Variables.GAMESTATE = False
    Variables.bossexist = False
    Game_Objects.player.shipcollision = True
    #endregion Reset Flags

    #region Reset Values
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
