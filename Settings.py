import Constants

#region KANA
num_to_shoot_new_kana = 10
kanax_velocity = 100
kanay_velocity = 15

kana_rotate_rate = 5

minimum_incorrect_kana_frequency = 20
maximum_incorrect_kana_frequency = 30

minimum_correct_kana_frequency = 10
maximum_correct_kana_frequency = 60
#endregion




#region SHIP
ship_normal_top_speed = 800
ship_boosted_top_speed = 1000

ship_normal_acceleration = 4
ship_normal_deceleration = 3

ship_boosted_acceleration = 6
ship_boosted_deceleration = 7

ship_screen_boundary = 64
explode_vel_frac = 20
maxlives = 5
ship_fallbackspeed = 100
# ship_screen_boundary_X = 100

ship_bullet_speed = 3000
max_bridge_wipes_per_level = 10
ship_extra_life_increment = 100
#endregion




#region STARS
star_frequency = 0.05
#endregion




#region BOSS SHIP
bosshealthmultiplier = 10
boss_bonus_score = 50
get_ready_timer_max = 3
#endregion Boss Ships




#region ENEMY SHIP
enemy_max_knockbackx = 300
enemy_knockbackx = 0
enemy_knockbacky = 0
enemy_knockback_recoveryx = 300
enemy_knockback_recoveryy = 400
enemy_start_level = 1
minimum_enemy_frequency = 5
maximum_enemy_frequency = 10
enemy_health = 10
enemy_powerup_freq = 3
damage_num_font_size = 40
enemiescanshooteachother = True
#endregion




#region BIG LASER
biglaser_start_level = 3
#endregion




#region USER INTERFACE
uitop = 30
maxmusicvolume = 0.2
score_position = (0, Constants.HEIGHT-uitop)
lives_position = (200, Constants.HEIGHT-uitop)
level_position = (400, Constants.HEIGHT-uitop)
bonus_position = (Constants.WCENTER-60, 80)
question_position = (Constants.WCENTER+60, 20)
shieldtext_position = (Constants.WCENTER-80,120)
boss_shield_bar = 150
#endregion