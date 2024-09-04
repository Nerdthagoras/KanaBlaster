import Constants

#region Kana
num_to_shoot_new_kana = 10
kanax_velocity = 100
kanay_velocity = 15

kana_rotate_rate = 5

minimum_incorrect_kana_frequency = 20
maximum_incorrect_kana_frequency = 30

minimum_correct_kana_frequency = 10
maximum_correct_kana_frequency = 60
#endregion

#region Ship
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

ship_extra_life_increment = 100
#endregion

#region Stars
star_frequency = 0.05
#endregion

#region Boss Ships
bosshealthmultiplier = 10
boss_bonus_score = 50
get_ready_timer_max = 3
#endregion Boss Ships

#region Enemy Ships
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

#region Big Laser
biglaser_start_level = 3
#endregion

#region Junk
#endregion

#region UI
maxmusicvolume = 0.1
score_position = (0, 10)
lives_position = (200, 10)
level_position = (400, 10)
bonus_position = (Constants.WIDTH/2-60, 60)
question_position = (Constants.WIDTH/2+60, 20)
#endregion