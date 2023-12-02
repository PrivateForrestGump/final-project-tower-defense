import pgzrun
from helper import *
import random

WIDTH = 1000
HEIGHT = 600

MOVE_STATE = 'move'
ATTACK_STATE = 'attack'


cursor = Actor('powerups/cursor1.png')

dmg = Actor('powerups/up_dmg.png')
dmg.scale = 4.25
dmg.x = WIDTH/2-40
dmg.y = HEIGHT-40

heart = Actor('powerups/heart.png')
heart.scale = 0.175
heart.x = WIDTH/2+40
heart.y = HEIGHT-40

clock = Actor('powerups/clock.png')
clock.scale = 0.14
clock.x = WIDTH/2+120
clock.y = HEIGHT-40


tower = Actor('tower/tower.png')
tower.x = WIDTH/2 
tower.y = HEIGHT/2
tower.hp = 200
tower.max_hp = 200
tower.dmg = 10
coins = 0
firerate = 60

ENEMY_TYPES = [
    'dark_knight',
    'samurai',
    'slime',
    'wizard'
]

dark_knights = []
samurais = []
slimes = []
wizards = []
orbs = []


dkattack_anim = [
    'characters/dark_knight/attack/tile016',
    'characters/dark_knight/attack/tile017',
    'characters/dark_knight/attack/tile018',
    'characters/dark_knight/attack/tile019',
    'characters/dark_knight/attack/tile020',
    'characters/dark_knight/attack/tile021',
    'characters/dark_knight/attack/tile022'
]

dkmove_anim = [
    'characters/dark_knight/move/tile001',
    'characters/dark_knight/move/tile002',
    'characters/dark_knight/move/tile003',
    'characters/dark_knight/move/tile004',
    'characters/dark_knight/move/tile005',
    'characters/dark_knight/move/tile006',
    'characters/dark_knight/move/tile007'
]

samattack_anim = [
    'characters/samurai/attack/tile016',
    'characters/samurai/attack/tile017',
    'characters/samurai/attack/tile018',
    'characters/samurai/attack/tile019',
    'characters/samurai/attack/tile020',
    'characters/samurai/attack/tile021',
    'characters/samurai/attack/tile022'
]

sammove_anim = [
    'characters/samurai/move/tile001',
    'characters/samurai/move/tile002',
    'characters/samurai/move/tile003',
    'characters/samurai/move/tile004',
    'characters/samurai/move/tile005',
    'characters/samurai/move/tile006',
    'characters/samurai/move/tile007'
]

slidie_anim = [
    'characters/slime/die/tile028',
    'characters/slime/die/tile029',
    'characters/slime/die/tile030',
    'characters/slime/die/tile031',
    'characters/slime/die/tile032'
]

slimove_anim = [
    'characters/slime/move/tile007',
    'characters/slime/move/tile008',
    'characters/slime/move/tile009',
    'characters/slime/move/tile010',
    'characters/slime/move/tile011',
    'characters/slime/move/tile012'
]

wizattack_anim = [
    'characters/wizard/attack/tile016',
    'characters/wizard/attack/tile017',
    'characters/wizard/attack/tile018',
    'characters/wizard/attack/tile019',
    'characters/wizard/attack/tile020',
    'characters/wizard/attack/tile021',
    'characters/wizard/attack/tile022',
    'characters/wizard/attack/tile023',
    'characters/wizard/attack/tile024',
    'characters/wizard/attack/tile025',
    'characters/wizard/attack/tile026'
]

wizmove_anim = [
    'characters/wizard/move/tile001',
    'characters/wizard/move/tile002',
    'characters/wizard/move/tile003',
    'characters/wizard/move/tile004',
    'characters/wizard/move/tile005',
    'characters/wizard/move/tile006',
    'characters/wizard/move/tile007'
]

def on_mouse_move(pos):
    cursor.pos = pos
    
def on_mouse_down():
    global coins,firerate
    if cursor.collide_pixel(dmg) and coins >= 10:
        tower.dmg += 1
        coins -= 10

    
    if cursor.collide_pixel(heart) and coins >= 10:
        tower.max_hp += 10
        coins -= 10

    if cursor.collide_pixel(clock) and coins >= 20:
        firerate -= 0.5
        coins -= 20
        

def all_enemies():
    enemies = []
    enemies.extend(dark_knights)
    enemies.extend(samurais)
    enemies.extend(wizards)
    enemies.extend(slimes)

    return enemies

def fire():
    enemies = all_enemies()
    if len(enemies) <= 0: return

    orb = Actor('tower/attack.png')
    orb.x = tower.x
    orb.bottom = tower.top


    # Find the nearest enemy
    enemy = None
    min_dis = 999999
    for e in enemies:
        dis = tower.distance_to(e)
        if dis < min_dis:
            min_dis = dis
            enemy = e
    
    #autoaim
    orb.angle = orb.angle_to(enemy)
    orb.target = enemy

    orbs.append(orb)

def spawn_enemy():
    enemy_type = random.choice(ENEMY_TYPES)
    if (enemy_type == 'dark_knight'):
        enemy = Actor(dkmove_anim[0])
        enemy.images = dkmove_anim
        dark_knights.append(enemy)
    elif (enemy_type == 'samurai'):
        enemy = Actor(sammove_anim[0])
        enemy.images = sammove_anim
        samurais.append(enemy)
    elif (enemy_type == 'slime'):
        enemy = Actor(slimove_anim[0])
        enemy.images = slimove_anim
        slimes.append(enemy)
    elif (enemy_type == 'wizard'):
        enemy = Actor(wizmove_anim[0])
        enemy.images = wizmove_anim
        wizards.append(enemy)

    EDGES = ['top', 'bottom', 'left', 'right']
    edge = random.choice(EDGES)
    if edge == 'top':
        enemy.bottom = 0
        enemy.x = random.randint(0, WIDTH)
    elif edge == 'bottom':
        enemy.top = HEIGHT
        enemy.x = random.randint(0, WIDTH)
    elif edge == 'left':
        enemy.right = 0
        enemy.y = random.randint(0, HEIGHT)
    elif edge == 'right':
        enemy.left = WIDTH
        enemy.y = random.randint(0, HEIGHT)

    enemy.state = MOVE_STATE
    enemy.hp = 10 * round_num
    enemy.damage = 10
    enemy.attack_rate = 60
    enemy.attack_timer = 0

def enemy_hit(enemy):
    global coins
    enemy.hp -= tower.dmg
    if enemy.hp <= 0:
        if enemy in dark_knights:
            dark_knights.remove(enemy)
            tower.hp += 1
            coins += 1
        elif enemy in samurais:
            samurais.remove(enemy)
            tower.hp += 2
            coins += 2
        elif enemy in slimes:
            slimes.remove(enemy)
            tower.hp += 5
            coins += 3
        elif enemy in wizards:
            wizards.remove(enemy)
            tower.hp += 10
            coins += 4
    
    if tower.hp > tower.max_hp:
        tower.hp = tower.max_hp

def update_orbs():
    for orb in orbs:
        if orb.target in all_enemies():
            orb.move_towards(orb.target, 15)
        else:
            orb.move_forward(15)
        if orb.bottom < 0 or orb.top > HEIGHT or orb.left < 0 or orb.right > WIDTH:
            orbs.remove(orb)
            continue
        
        for enemy in all_enemies():
            if orb.collide_pixel(enemy):
                enemy_hit(enemy)
                orbs.remove(orb)
                break
            

def update_enemies():
    for enemy in all_enemies():
        enemy.animate()
        
        enemy.attack_timer += 1
        
        is_last_frame = enemy.image == enemy.images[-1]
        is_attacking = enemy.state == ATTACK_STATE and not is_last_frame
        can_attack = enemy.attack_timer >= enemy.attack_rate and not is_attacking
        
        if enemy.state == MOVE_STATE and not enemy.collide_pixel(tower):
            enemy.point_towards(tower)
            enemy.move_towards(tower, 1)
        
        if enemy.collide_pixel(tower) and enemy.state != ATTACK_STATE:
            enemy.state = ATTACK_STATE
        
        if enemy.state == ATTACK_STATE and can_attack:
            enemy.attack_timer = 0
            if enemy in dark_knights:
                enemy.images = dkattack_anim
            elif enemy in samurais:
                enemy.images = samattack_anim
            elif enemy in slimes:
                enemy.images = slidie_anim
            elif enemy in wizards:
                enemy.images = wizattack_anim
                
        if enemy.state == ATTACK_STATE and is_last_frame:
            enemy.state = MOVE_STATE
            if enemy in dark_knights:
                enemy.images = dkmove_anim
            elif enemy in samurais:
                enemy.images = sammove_anim
            elif enemy in slimes:
                enemy.images = slimove_anim
            elif enemy in wizards:
                enemy.images = wizmove_anim
            
            tower.hp -= enemy.damage
            print(tower.hp)
                

def draw():
    screen.clear()
    tower.draw()
    
    # TODO: Place this at top left corner done
    screen.draw.text('Round '+str(round_num), (0, 0), fontsize=30, color='white')
    screen.draw.text('Max HP: '+str(tower.max_hp), (0, 20), fontsize=30, color='white')
    screen.draw.text('Orb damage: '+str(tower.dmg), (0, 40), fontsize=30, color='white')
    screen.draw.text('Coins: '+str(coins), (0, 60), fontsize=30, color='white')
    screen.draw.text('Firerate: 1 orb every '+str(firerate/60)+' sec', (0, 80), fontsize=30, color='white')

    for orb in orbs:
        orb.draw()

    for e in dark_knights:
        e.draw()

    for e in slimes:
        e.draw()

    for e in wizards:
        e.draw()

    for e in samurais:
        e.draw()

    cursor.draw()
    dmg.draw()
    heart.draw()
    clock.draw()
    
    if tower.hp <= 0:
        screen.draw.text('GAME OVER', (WIDTH/2, HEIGHT/2), fontsize=100, color='red')
        return
    
    hp_bar_left = tower.x - 50
    hp_bar_w = tower.hp / tower.max_hp * 100
    hp_right = hp_bar_left + hp_bar_w
    tower_hp_bar = Rect(hp_bar_left,tower.y - 50, hp_bar_w, 15)
    
    lost_hp_bar = Rect(hp_right, tower.y-50, (tower.max_hp - tower.hp)/tower.max_hp*100, 15)
    hp_bar_outline = Rect(tower.x-50-1.5,tower.y-50-2.5, 100+3, 20)
    
    screen.draw.filled_rect(tower_hp_bar,('green'))
    screen.draw.filled_rect(lost_hp_bar,('red'))
    screen.draw.rect(hp_bar_outline,('white'))
    
frame_count = 0
round_num = 1

def update():
    global frame_count, round_num
    frame_count += 1
    
    can_fire = frame_count % firerate == 0
    one_min_passed = frame_count % 3600 == 0
    should_spawn_enemy = frame_count % 40 == 0
    can_fire = frame_count % firerate == 0

    if one_min_passed:
        round_num += 1
    
    if should_spawn_enemy:
        spawn_enemy()
    
    update_enemies()
    
    if can_fire:
        fire()
    update_orbs()
    

pgzrun.go()