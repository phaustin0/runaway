# settings file

# window settings
width = 900
height = 600
title = 'The Runaway - Made by Faustino'

# game settings
fps = 60

# colours
black = (0, 0, 0)
white = '#e4dfda'
light_grey = '#afafaf'
dark_grey = '#626267'
darker_grey = '#464646'
darkest_grey = '#2e2e2e'
red = '#fe5f55'
green = '#5fad41'
blue = (0, 0, 255)
yellow = '#ffb140'

# background settings
bg_layer = 1

# player settings
player_layer = 4
player_speed = 9
player_max_health = 200
player_heal_time = 2
player_heal_amount = player_max_health // 3.2
player_bullet_speed = 40
player_bullet_damage = 100
player_bullet_colour = yellow
player_bullet_shoot_interval = 50
player_time_in_planet = 10
player_kill_heal_amount = 10 / 100 * player_max_health

# bullet settings
bullet_layer = 3
bullet_time_to_kill = 1000

# enemy settings
enemy_layer = 5
enemy_speed = 5
enemy_max_health = 300
enemy_bullet_speed = 25
enemy_bullet_damage = 100
enemy_bullet_colour = red
enemy_bullet_shoot_interval = 100

# enemy spawner settings
enemy_spawn_interval = 4

# planet settings
planet_width = 100
planet_height = 100
planet_radius = planet_width // 2
planet_layer = 2

# quid settings
quid_multiplier = 10

