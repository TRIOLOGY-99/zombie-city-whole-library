import pygame
import random
import math
import sys
from pathlib import Path

pygame.init()

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
FPS = 60

PLAYER_SPEED = 5
DASH_SPEED = 15
DASH_DURATION = 30
ROLL_SPEED = 13

BULLET_SPEED = 18
SHOTGUN_SPREAD = 0.25

SHOCK_RADIUS = 500
SHOCK_COOLDOWN = 300
SHOCK_DAMAGE = 6

# Orbital Strike constants
ORBITAL_WARNING = 120
ORBITAL_COOLDOWN = 3600
ORBITAL_DAMAGE = 200
ORBITAL_RADIUS = 180

# Resurrection Beacon constants
BEACON_DURATION = 600
BEACON_COOLDOWN = 1800
BEACON_RESPAWN_HEALTH = 0.5

# Adrenaline Rush (dash) constants
ADRENALINE_DURATION = 18
ADRENALINE_SPEED = 30
ADRENALINE_COOLDOWN = 600
ADRENALINE_DAMAGE = 10

# Immortality ability
IMMORTAL_DURATION = 10 * FPS
IMMORTAL_COOLDOWN = 30 * FPS  # 30 seconds cooldown as requested

UPGRADE_CARD_W = 250
UPGRADE_CARD_H = 180

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("CYBER ZOMBIE APOCALYPSE — NIGHTMARE EDITION")
clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 26)
big_font = pygame.font.SysFont("consolas", 80)
upgrade_font = pygame.font.SysFont("consolas", 32)

medkit_img = pygame.image.load(
    str(Path(__file__).with_name("medkit.jpeg"))
).convert_alpha()
medkit_img = pygame.transform.smoothscale(medkit_img, (24, 24))
shield_img = pygame.image.load(
    str(Path(__file__).with_name("shield.jpeg"))
).convert_alpha()
shield_img = pygame.transform.smoothscale(shield_img, (24, 24))
ammo_img = pygame.image.load(
    str(Path(__file__).with_name("bullets.png"))
).convert_alpha()
ammo_img = pygame.transform.smoothscale(ammo_img, (24, 24))

buff_descriptions = {
    "hp": "Increase max health by 20.",
    "firerate": "Fire rate increased by 15%.",
    "speed": "Player speed increased by 10%.",
    "dash": "Reduce dash cooldown by 20%.",
    "reload_less": "Reload time decreased by 10.",
    "explosive": "Bullets become explosive.",
    "crit": "Critical hit chance increased by 10%.",
    "shield": "Extra invincibility duration.",
    "poison": "Poison bullets cause damage over time.",
    "burn": "Bullets cause burn damage.",
    "homing": "Shots home in on enemies.",
    "slow": "Enemies are slowed down.",
    "regen": "Auto-heal 0.1 health per frame.",
    "pierce": "Bullets pierce through enemies.",
    "dmg": "Bullet damage increased by 50%.",
    "ammo": "Increase max ammo capacity for all weapons by 50%.",
    "ricochet": "Pump shotgun: 7 pellets bounce off walls, 2x damage + knockback at point blank.",
    "machinegun": "Rapid fire, cheap ammo.",
    "bazooka": "Huge explosive rocket.",
    "sniper": "Slow, high damage shots.",
    "laser": "Fast, accurate beams.",
    "flamethrower": "Short range stream of fire.",
    "plasma": "Heavy plasma bolts.",
    "lifesteal": "Heal a chunk on enemy kill.",
    "overcharge": "Explosive bullets do extra damage.",
    "shock_up": "Increase shockwave damage.",
    "double_hp": "Double your current and max health.",
    "extra_ammo": "Increase ammo capacity slightly for all weapons.",
    "kill_dmg": "Permanent +20% damage on pick.",
}

# ---------------------------------------------------------
# START SCREEN
# ---------------------------------------------------------
zombie_descriptions = {
    "normal": "Normal: Basic slow zombie. Easy to kill but comes in numbers.",
    "fast": "Fast: Quick and fragile. Watch your back!",
    "tank": "Tank: High health, slow. Hard to push back.",
    "exploder": "Exploder: Explodes on death, damaging nearby players.",
    "boss": "Boss: Spawns in some waves, shoots acid blasts.",
    "spitter": "Spitter: Ranged acid spitter that fires at the player.",
    "splitter": "Splitter: When killed, splits into several small fast zombies.",
    "shielded": "Shielded: Front-facing shield blocks frontal shots; flank or ricochet!",
    "teleporter": "Teleporter: Blinks around; will teleport near the player occasionally.",
    "healer": "Healer: Slowly heals nearby zombies; take it out first.",
    "charger": "Charger: Telegraphed dash attack—dashes at the player after a short warning.",
}

def start_screen():
    start = False
    show_index = False
    while not start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not show_index:
                    start = True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_i:
                    show_index = not show_index
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                start_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 60)
                index_rect = pygame.Rect(WIDTH//2 - 100 - 240, HEIGHT//2 + 50, 200, 60)
                if start_rect.collidepoint(mx, my) and not show_index:
                    start = True
                if index_rect.collidepoint(mx, my):
                    show_index = not show_index

        screen.fill((10, 10, 20))
        title = big_font.render("ZOMBIE CITY SURVIVAL", True, (255, 50, 50))
        instruct1 = font.render("Press ENTER or Click 'Start' to Play", True, (255, 255, 255))
        instruct2 = font.render("WASD move | SPACE dash | SHIFT roll | R reload | E shockwave | P pause | ESC quit",
                                True, (180, 180, 180))
        start_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 60)
        pygame.draw.rect(screen, (50, 150, 50), start_button, border_radius=10)
        start_text = font.render("START", True, (255, 255, 255))
        index_button = pygame.Rect(WIDTH//2 - 100 - 240, HEIGHT//2 + 50, 200, 60)
        pygame.draw.rect(screen, (80, 100, 180), index_button, border_radius=10)
        index_text = font.render("INDEX (I)", True, (255, 255, 255))

        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
        screen.blit(instruct1, (WIDTH//2 - instruct1.get_width()//2, HEIGHT//3 + 100))
        screen.blit(instruct2, (WIDTH//2 - instruct2.get_width()//2, HEIGHT//2 + 140))
        screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 + 60))
        screen.blit(index_text, (WIDTH//2 - 100 - 240 + 20, HEIGHT//2 + 60))

        if show_index:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(220)
            overlay.fill((5, 5, 10))
            screen.blit(overlay, (0, 0))
            header = big_font.render("Zombie Index", True, (230, 230, 230))
            screen.blit(header, (WIDTH//2 - header.get_width()//2, 40))

            left = WIDTH//5
            top = 130
            line_h = 40
            i = 0
            for key, desc in zombie_descriptions.items():
                y = top + i * line_h
                name_surf = font.render(key.upper(), True, (200, 200, 255))
                desc_surf = font.render(desc, True, (230, 230, 230))
                screen.blit(name_surf, (left, y))
                screen.blit(desc_surf, (left + 160, y))
                i += 1

            hint = font.render("Click Index or press I to close", True, (150, 150, 150))
            screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 80))

        pygame.display.flip()
        clock.tick(60)

# ---------------------------------------------------------
# UTILS
# ---------------------------------------------------------
def distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

def draw_grid(offset):
    screen.fill((10, 10, 20))
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, (0, 60, 90),
                         (x + offset % 40, 0),
                         (x + offset % 40, HEIGHT))
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, (0, 60, 90),
                         (0, y + offset % 40),
                         (WIDTH, y + offset % 40))

def edge_spawn():
    side = random.choice(["l", "r", "t", "b"])
    if side == "l":
        return -40, random.randint(0, HEIGHT)
    if side == "r":
        return WIDTH + 40, random.randint(0, HEIGHT)
    if side == "t":
        return random.randint(0, WIDTH), -40
    return random.randint(0, WIDTH), HEIGHT + 40

# ---------------------------------------------------------
# PARTICLES
# ---------------------------------------------------------
class Particle:
    def __init__(self, x, y, color, size=4, life=40, vx=None, vy=None):
        self.x = x
        self.y = y
        self.life = life
        self.max_life = life
        self.size = size
        self.dx = vx if vx is not None else random.uniform(-2, 2)
        self.dy = vy if vy is not None else random.uniform(-2, 2)
        self.color = color

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1
        self.size = max(1, self.size - 0.05)

    def draw(self):
        pygame.draw.circle(screen, self.color,
                           (int(self.x), int(self.y)),
                           int(self.size))

# ---------------------------------------------------------
# BULLETS
# ---------------------------------------------------------
class Bullet:
    def __init__(self, x, y, angle, speed=BULLET_SPEED, life=120, damage=1, weapon=None, **kwargs):
        self.x = x
        self.y = y
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.angle = angle
        self.explosive = kwargs.get("explosive", False)
        self.piercing = kwargs.get("piercing", False)
        self.damage = damage
        self.life = life
        self.size = kwargs.get("size", 5)
        self.poison = kwargs.get("poison", False)
        self.burn = kwargs.get("burn", False)
        self.homing = kwargs.get("homing", False)
        self.slow = kwargs.get("slow", False)
        self.speed = speed
        self.weapon = weapon
        self.bounces = kwargs.get("bounces", 0)
        self.knockback = kwargs.get("knockback", 0)
        self.close_bonus = kwargs.get("close_bonus", False)
        self.traveled = 0.0
        self.hit = set()
        self.boomerang = kwargs.get("boomerang", False)
        self.returning = False
        self.max_travel = kwargs.get("max_travel", 400)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.traveled += math.hypot(self.dx, self.dy)
        self.life -= 1

        if self.boomerang and not self.returning and self.traveled >= self.max_travel:
            self.dx = -self.dx
            self.dy = -self.dy
            self.returning = True
            self.hit.clear()

    def bounce(self):
        if self.bounces <= 0:
            return
        bounced = False
        if self.x < 0 or self.x > WIDTH:
            self.dx = -self.dx
            self.x = max(0, min(WIDTH, self.x))
            bounced = True
        if self.y < 0 or self.y > HEIGHT:
            self.dy = -self.dy
            self.y = max(0, min(HEIGHT, self.y))
            bounced = True
        if bounced:
            self.bounces -= 2
            self.damage *= 1.25
            self.hit.clear()

    def draw(self):
        if self.weapon == "flamethrower":
            pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.size)
        elif self.weapon == "plasma":
            pygame.draw.circle(screen, (180, 0, 255), (int(self.x), int(self.y)), self.size)
        elif self.weapon == "laser" or self.weapon == "beam":
            w = max(4, int(self.size * 4))
            h = max(4, int(self.size * 2))
            rect = pygame.Rect(int(self.x - w // 2), int(self.y - h // 2), w, h)
            pygame.draw.rect(screen, (0, 150, 255), rect)
        elif self.weapon == "ricochet":
            pygame.draw.circle(screen, (255, 140, 0), (int(self.x), int(self.y)), self.size)
            pygame.draw.circle(screen, (255, 255, 200), (int(self.x), int(self.y)), max(1, self.size - 3))
        elif self.weapon == "railgun":
            pygame.draw.circle(screen, (200, 240, 255), (int(self.x), int(self.y)), self.size)
            pygame.draw.circle(screen, (120, 200, 255), (int(self.x), int(self.y)), max(1, self.size - 2))
        elif self.weapon == "boomerang":
            pygame.draw.circle(screen, (255, 220, 120), (int(self.x), int(self.y)), self.size)
        elif self.weapon == "tesla":
            pygame.draw.circle(screen, (180, 220, 255), (int(self.x), int(self.y)), self.size)
        else:
            pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.size)

    def off(self):
        if self.life <= 0:
            return True
        if self.boomerang:
            return not (-200 < self.x < WIDTH + 200 and -200 < self.y < HEIGHT + 200)
        if self.bounces > 0:
            return False
        return not (-100 < self.x < WIDTH + 100 and -100 < self.y < HEIGHT + 100)

# ---------------------------------------------------------
# ACID PROJECTILE
# ---------------------------------------------------------
class Acid:
    def __init__(self, x, y, angle, speed=10, damage=10):
        self.x = x
        self.y = y
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.damage = damage

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        pygame.draw.circle(screen, (2, 200, 255),
                           (int(self.x), int(self.y)), 7)

    def off(self):
        return not (-100 < self.x < WIDTH + 100 and -100 < self.y < HEIGHT + 100)

# ---------------------------------------------------------
# PLAYER
# ---------------------------------------------------------
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.max_health = 200
        self.health = 200
        self.speed = PLAYER_SPEED

        self.fire_rate = 15
        self.fire_delay = 0

        self.recoil = 0
        self.weapon = "pistol"

        self.ammo = 10
        self.max_ammo = 10
        self.ammo_per_shot = {
            "pistol": 1, "machinegun": 1, "shotgun": 3, "sniper": 1,
            "bazooka": 1, "laser": 1, "flamethrower": 5, "plasma": 1,
            "ricochet": 4,
            "railgun": 1, "tesla": 1, "cluster": 4, "boomerang": 1, "beam": 1
        }
        self.max_ammo_values = {
            "pistol": 10, "machinegun": 120, "shotgun": 24, "sniper": 5,
            "bazooka": 2, "laser": 50, "flamethrower": 500, "plasma": 30,
            "ricochet": 16,
            "railgun": 6, "tesla": 80, "cluster": 180, "boomerang": 8, "beam": 300
        }
        self.reload_time = {
            "pistol": 40, "machinegun": 100, "shotgun": 80, "sniper": 100,
            "bazooka": 120, "laser": 40, "flamethrower": 20, "plasma": 70,
            "ricochet": 90,
            "railgun": 140, "tesla": 40, "cluster": 100, "boomerang": 90, "beam": 40
        }
        self.is_reloading = False
        self.reload_counter = 0

        self.roll_cd = 0
        self.dash_cd = 0
        self.dash_cd_max = 120
        self.dash_active = False
        self.dash_duration = 0
        self.invincible = 0
        self.shock_cd = 0

        self.regen = 0
        self.piercing = False
        self.crit_chance = 0.0
        self.damage_mult = 1.0

        self.explosive_bullets = False
        self.poison = False
        self.burn = False
        self.homing = False
        self.slow_effect = False

        self.lifesteal = 0
        self.overcharge = False

    def move(self, keys, particles):
        speed = self.speed

        if keys[pygame.K_SPACE] and self.dash_cd <= 0 and not self.dash_active:
            self.dash_active = True
            self.dash_duration = DASH_DURATION
            self.dash_cd = self.dash_cd_max
            for _ in range(12):
                particles.append(Particle(self.x, self.y, (0, 180, 255), size=6, life=20))
        if self.dash_active:
            speed = DASH_SPEED
            self.dash_duration -= 1
            if self.dash_duration <= 0:
                self.dash_active = False
        if keys[pygame.K_LSHIFT] and self.roll_cd <= 0:
            speed = ROLL_SPEED
            self.roll_cd = 50
            self.invincible = 20
            for _ in range(10):
                particles.append(Particle(self.x, self.y, (255, 255, 255), size=6, life=15))
        if self.dash_cd > 0:
            self.dash_cd -= 1
        if self.roll_cd > 0:
            self.roll_cd -= 1
        if self.invincible > 0:
            self.invincible -= 1
        if self.shock_cd > 0:
            self.shock_cd -= 1
        if keys[pygame.K_w]: self.y -= speed
        if keys[pygame.K_s]: self.y += speed
        if keys[pygame.K_a]: self.x -= speed
        if keys[pygame.K_d]: self.x += speed
        self.clamp()

    def clamp(self):
        self.x = max(20, min(WIDTH - 20, self.x))
        self.y = max(20, min(HEIGHT - 20, self.y))

    def draw(self):
        color = (0, 255, 255) if self.invincible == 0 else (255, 255, 0)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 20)
        mx, my = pygame.mouse.get_pos()
        angle = math.atan2(my - self.y, mx - self.x)
        gun_x = self.x + math.cos(angle) * (35 + self.recoil)
        gun_y = self.y + math.sin(angle) * (35 + self.recoil)
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), (gun_x, gun_y), 6)
        if self.recoil > 0:
            self.recoil -= 1

    def regen_tick(self):
        if self.health < self.max_health:
            self.health = min(self.max_health, self.health + 0.2 / FPS)
            if self.regen > 0:
                self.health = min(self.max_health, self.health + 0.1 * self.regen)

    def start_reload(self):
        if not self.is_reloading and self.ammo < self.max_ammo:
            self.is_reloading = True
            self.reload_counter = self.reload_time.get(self.weapon, 40)

    def update_reload(self):
        if self.is_reloading:
            self.reload_counter -= 1
            if self.reload_counter <= 0:
                self.is_reloading = False
                self.ammo = self.max_ammo

    def can_shoot(self):
        ammo_cost = self.ammo_per_shot.get(self.weapon, 1)
        return self.ammo >= ammo_cost and not self.is_reloading

    def consume_ammo(self):
        self.ammo -= self.ammo_per_shot.get(self.weapon, 1)

    def switch_weapon(self, weapon_name):
        self.weapon = weapon_name
        self.max_ammo = self.max_ammo_values.get(weapon_name, self.max_ammo)
        self.ammo = self.max_ammo
        self.is_reloading = False

# ---------------------------------------------------------
# PICKUPS
# ---------------------------------------------------------
class HealthPack:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self):
        rect = medkit_img.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(medkit_img, rect)

class ShieldPU:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self):
        rect = shield_img.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(shield_img, rect)

class AmmoPack:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self):
        rect = ammo_img.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(ammo_img, rect)

# ---------------------------------------------------------
# ZOMBIES
# ---------------------------------------------------------
class Zombie:
    def __init__(self, type_, wave=1):
        self.type = type_
        self.x, self.y = edge_spawn()
        if type_ == "normal":
            self.hp, self.speed, self.color, self.size = 3, 1.5, (0, 200, 0), 25
        elif type_ == "fast":
            self.hp, self.speed, self.color, self.size = 2, 2.9, (0, 255, 120), 20
        elif type_ == "tank":
            self.hp, self.speed, self.color, self.size = 10, 0.95, (150, 90, 0), 35
        elif type_ == "exploder":
            self.hp, self.speed, self.color, self.size = 3, 2.4, (255, 120, 0), 22
        elif type_ == "boss":
            self.hp, self.speed, self.color, self.size = 70, 1.2, (255, 0, 255), 55
        else:
            self.hp, self.speed, self.color, self.size = 3, 1.5, (0, 200, 0), 25

        self.hp *= 1 + 0.18 * (wave - 1)
        self.speed *= min(1.9, 1 + 0.04 * (wave - 1))

        self.max_hp = self.hp
        self.poison_damage = 0
        self.burn_damage = 0
        self.slow_timer = 0
        self.kx = 0.0
        self.ky = 0.0
        self.wave = wave
        self.shoot_cd = 100
        self.flash_timer = 0
        self.facing_angle = 0.0
        self.teleport_cd = 0

    def update(self, player, game=None):
        mult = 1.0
        if self.slow_timer > 0:
            self.slow_timer -= 1
            mult = 0.5
        angle = math.atan2(player.y - self.y, player.x - self.x)
        self.facing_angle = angle
        self.x += math.cos(angle) * self.speed * mult + self.kx
        self.y += math.sin(angle) * self.speed * mult + self.ky
        self.kx *= 0.85
        self.ky *= 0.85

        if self.poison_damage > 0:
            self.hp -= 0.05
            self.poison_damage -= 1
        if self.burn_damage > 0:
            self.hp -= 0.03
            self.burn_damage -= 1

        shots = []
        if self.type == "boss":
            self.shoot_cd -= 1
            if self.shoot_cd <= 0:
                self.shoot_cd = 110
                n = 14
                off = random.uniform(0, math.pi)
                for i in range(n):
                    shots.append(Acid(self.x, self.y, off + i * (2 * math.pi / n), speed=9))
        if self.flash_timer > 0:
            self.flash_timer -= 1
        return shots

    def draw(self):
        if self.flash_timer > 0:
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size)
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        if self.type == "exploder":
            pygame.draw.circle(screen, (255, 255, 120), (int(self.x), int(self.y)), self.size // 2)
            pygame.draw.circle(screen, (255, 60, 0), (int(self.x), int(self.y)), self.size + 4, 2)
        if self.type == "shielded":
            arc_color = (180, 220, 255)
            ex = self.x + math.cos(self.facing_angle) * (self.size + 8)
            ey = self.y + math.sin(self.facing_angle) * (self.size + 8)
            pygame.draw.line(screen, arc_color, (self.x, self.y), (ex, ey), 4)
        self.draw_health_bar()

    def draw_health_bar(self):
        bar_width = 50
        bar_height = 5
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.size - 15
        pygame.draw.rect(screen, (200, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        health_ratio = max(0, self.hp / self.max_hp)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

class SpitterZombie(Zombie):
    def __init__(self, wave=1):
        super().__init__("normal", wave)
        self.type = "spitter"
        self.hp = 5 * (1 + 0.18 * (wave - 1))
        self.max_hp = self.hp
        self.speed = 1.2
        self.color = (0, 150, 255)
        self.size = 28
        self.shoot_cd = random.randint(50, 110)

    def update(self, player, game=None):
        super().update(player, game)
        shots = []
        self.shoot_cd -= 1
        if self.shoot_cd <= 0:
            self.shoot_cd = max(35, random.randint(70, 130) - self.wave * 4)
            angle = math.atan2(player.y - self.y, player.x - self.x)
            if self.wave >= 8:
                spreads = [-0.3, -0.15, 0, 0.15, 0.3]
            elif self.wave >= 4:
                spreads = [-0.2, 0, 0.2]
            else:
                spreads = [0]
            for s in spreads:
                shots.append(Acid(self.x, self.y, angle + s))
        return shots

class SplitterZombie(Zombie):
    def __init__(self, wave=1):
        super().__init__("splitter", wave)
        self.type = "splitter"
        self.hp = 4 * (1 + 0.12 * (wave - 1))
        self.max_hp = self.hp
        self.speed = 1.8
        self.color = (200, 120, 200)
        self.size = 18

class ShieldedZombie(Zombie):
    def __init__(self, wave=1):
        super().__init__("shielded", wave)
        self.type = "shielded"
        self.hp = 8 * (1 + 0.18 * (wave - 1))
        self.max_hp = self.hp
        self.speed = 1.1
        self.color = (120, 180, 200)
        self.size = 30

    def update(self, player, game=None):
        super().update(player, game)
        return []

class TeleporterZombie(Zombie):
    def __init__(self, wave=1):
        super().__init__("teleporter", wave)
        self.type = "teleporter"
        self.hp = 4 * (1 + 0.12 * (wave - 1))
        self.max_hp = self.hp
        self.speed = 1.6
        self.color = (255, 180, 40)
        self.size = 20
        self.teleport_cd = random.randint(90, 200)

    def update(self, player, game=None):
        super().update(player, game)
        self.teleport_cd -= 1
        if self.teleport_cd <= 0:
            rx = player.x + random.randint(-160, 160)
            ry = player.y + random.randint(-160, 160)
            self.x = max(40, min(WIDTH - 40, rx))
            self.y = max(40, min(HEIGHT - 40, ry))
            self.teleport_cd = random.randint(120, 260)
            if game:
                for _ in range(8):
                    game.particles.append(Particle(self.x, self.y, (255, 200, 50), size=5, life=18))
        return []

class HealerZombie(Zombie):
    def __init__(self, wave=1):
        super().__init__("healer", wave)
        self.type = "healer"
        self.hp = 6 * (1 + 0.12 * (wave - 1))
        self.max_hp = self.hp
        self.speed = 1.0
        self.color = (160, 255, 160)
        self.size = 24
        self.heal_timer = 0

    def update(self, player, game=None):
        super().update(player, game)
        if game:
            self.heal_timer += 1
            if self.heal_timer >= 30:
                self.heal_timer = 0
                for other in game.zombies:
                    if other is not self and distance(self.x, self.y, other.x, other.y) < 120:
                        other.hp = min(other.max_hp, other.hp + 0.6)
        return []

class ChargerZombie(Zombie):
    def __init__(self, wave=1):
        super().__init__("charger", wave)
        self.type = "charger"
        self.hp = 5 * (1 + 0.12 * (wave - 1))
        self.max_hp = self.hp
        self.speed = 1.1
        self.color = (255, 90, 90)
        self.size = 22
        self.telegraph = 0
        self.dashing = 0
        self.target_angle = 0

    def update(self, player, game=None):
        if self.dashing > 0:
            self.x += math.cos(self.target_angle) * 12
            self.y += math.sin(self.target_angle) * 12
            self.dashing -= 1
        else:
            if self.telegraph <= 0:
                self.telegraph = random.randint(40, 90)
                self.target_angle = math.atan2(player.y - self.y, player.x - self.x)
            else:
                self.telegraph -= 1
                if self.telegraph <= 0:
                    self.dashing = 18
        if self.dashing == 0:
            super().update(player, game)
        if self.flash_timer > 0:
            self.flash_timer -= 1
        return []

    def draw(self):
        super().draw()
        if self.telegraph > 0:
            ex = self.x + math.cos(self.target_angle) * 160
            ey = self.y + math.sin(self.target_angle) * 160
            pygame.draw.line(screen, (255, 80, 80), (self.x, self.y), (ex, ey), 2)

# ---------------------------------------------------------
# GAME ENGINE
# ---------------------------------------------------------
class Game:
    def __init__(self):
        self.player = Player()

        self.zombies = []
        self.bullets = []
        self.acid = []
        self.particles = []
        self.packs = []
        self.shields = []
        self.ammo_packs = []

        self.wave = 1
        self.score = 0
        self.grid_offset = 0

        self.auto_fire = False
        self.show_upgrades = False
        self.upgrade_choices = []

        self.game_over = False
        self.paused = False
        self.pause_counter = 0

        self.reinforcements_left = 0
        self.reinforce_timer = 0
        self.shock_ring = None

        self.combo_count = 0
        self.combo_timer = 0
        self.combo_timeout = 240
        self.shake = 0

        self.shock_damage = SHOCK_DAMAGE

        self.pending_strikes = []
        self.orbital_cd = 0

        self.beacons = []
        self.beacon_cd = 0

        self.adrenaline_cd = 0
        self.adrenaline_timer = 0
        self.adrenaline_dx = 0.0
        self.adrenaline_dy = 0.0
        self.adrenaline_hits = set()

        self.immortal_cd = 0

    def reset_combo(self):
        self.combo_count = 0
        self.combo_timer = 0

    def player_took_damage(self):
        self.reset_combo()
        self.player.damage_mult = 1.0

    def combo_multiplier(self):
        return round(1.0 + min(10, self.combo_count) * 0.12, 2)

    def call_orbital_strike(self, x, y):
        if self.orbital_cd > 0:
            return False
        self.pending_strikes.append({'x': x, 'y': y, 'timer': ORBITAL_WARNING})
        self.orbital_cd = ORBITAL_COOLDOWN
        return True

    def place_beacon(self, x, y):
        if self.beacon_cd > 0:
            return False
        self.beacons.append({'x': x, 'y': y, 'timer': BEACON_DURATION, 'used': False})
        self.beacon_cd = BEACON_COOLDOWN
        return True

    def explode_orbital(self, strike):
        sx, sy = strike['x'], strike['y']
        for _ in range(120):
            self.particles.append(Particle(sx + random.uniform(-40, 40), sy + random.uniform(-40, 40),
                                           (255, 160, 30), size=random.uniform(6, 14),
                                           life=random.randint(30, 60),
                                           vx=random.uniform(-6, 6), vy=random.uniform(-6, 6)))
        for z in self.zombies[:]:
            if distance(sx, sy, z.x, z.y) <= ORBITAL_RADIUS:
                z.hp -= ORBITAL_DAMAGE
                z.flash_timer = 12
                if z.hp <= 0:
                    self.kill_zombie(z)
        if distance(sx, sy, self.player.x, self.player.y) <= ORBITAL_RADIUS and self.player.invincible == 0:
            self.player.health -= ORBITAL_DAMAGE // 2
            self.player_took_damage()
        self.shake = max(self.shake, 40)

    def spawn_wave(self):
        w = self.wave
        count = 4 + w * 4
        types = ["normal", "fast", "tank"]
        weights = [4, 3, 2]
        if w >= 2:
            types.append("exploder")
            weights.append(3)
        if w >= 3:
            types += ["splitter", "shielded"]
            weights += [2, 2]
        if w >= 4:
            types += ["teleporter", "healer", "charger"]
            weights += [1, 1, 2]

        for _ in range(count):
            t = random.choices(types, weights)[0]
            if t == "spitter":
                self.zombies.append(SpitterZombie(w))
            elif t == "splitter":
                self.zombies.append(SplitterZombie(w))
            elif t == "shielded":
                self.zombies.append(ShieldedZombie(w))
            elif t == "teleporter":
                self.zombies.append(TeleporterZombie(w))
            elif t == "healer":
                self.zombies.append(HealerZombie(w))
            elif t == "charger":
                self.zombies.append(ChargerZombie(w))
            else:
                self.zombies.append(Zombie(t, w))

        for _ in range(min(16, 3 + w * 2)):
            self.zombies.append(SpitterZombie(w))

        if w % 3 == 0:
            for _ in range(w // 3):
                self.zombies.append(Zombie("boss", w))

        self.reinforcements_left = w * 3
        self.reinforce_timer = 120

    def reinforce(self):
        if self.reinforcements_left <= 0:
            return
        self.reinforce_timer -= 1
        if self.reinforce_timer <= 0:
            self.reinforce_timer = max(30, 120 - self.wave * 4)
            self.reinforcements_left -= 1
            r = random.random()
            if r < 0.35:
                self.zombies.append(SpitterZombie(self.wave))
            elif r < 0.55 and self.wave >= 2:
                self.zombies.append(Zombie("exploder", self.wave))
            else:
                t = random.choice(["normal", "fast", "tank"])
                self.zombies.append(Zombie(t, self.wave))

    def shoot(self):
        p = self.player
        if p.fire_delay > 0:
            return

        if p.weapon == "beam":
            if p.ammo <= 0 or p.is_reloading:
                if p.ammo == 0 and not p.is_reloading:
                    p.start_reload()
                p.fire_delay = 2
                return
            mx, my = pygame.mouse.get_pos()
            angle = math.atan2(my - p.y, mx - p.x)
            beam_length = 900
            for z in self.zombies[:]:
                vx = z.x - p.x
                vy = z.y - p.y
                dist = math.hypot(vx, vy)
                if dist > beam_length:
                    continue
                ang = math.atan2(vy, vx)
                diff = abs((ang - angle + math.pi) % (2 * math.pi) - math.pi)
                if diff < 0.12:
                    dmg = 3 * p.damage_mult
                    z.hp -= dmg
                    z.flash_timer = 6
                    for _ in range(3):
                        self.particles.append(Particle(z.x + random.uniform(-6, 6), z.y + random.uniform(-6, 6),
                                                       (100, 200, 255), size=3, life=12))
                    if z.hp <= 0:
                        self.kill_zombie(z)
            p.ammo = max(0, p.ammo - 1)
            p.fire_delay = 2
            return

        if not p.can_shoot():
            if p.ammo == 0 and not p.is_reloading:
                p.start_reload()
            return

        p.fire_delay = p.fire_rate
        mx, my = pygame.mouse.get_pos()
        angle = math.atan2(my - p.y, mx - p.x)
        p.recoil = 5
        w = p.weapon

        if w == "pistol":
            self.make_bullet(angle)
        elif w == "machinegun":
            self.make_bullet(angle)
        elif w == "shotgun":
            for s in [-SHOTGUN_SPREAD, 0, SHOTGUN_SPREAD]:
                self.make_bullet(angle + s)
        elif w == "ricochet":
            p.fire_delay = int(p.fire_rate * 2.2)
            for _ in range(7):
                spread = random.uniform(-0.35, 0.35)
                b = self.make_bullet(angle + spread, damage=1.2, speed=random.uniform(15, 20), life=80)
                b.bounces = 2
                b.knockback = 9
                b.close_bonus = True
                b.size = 4
            p.x -= math.cos(angle) * 14
            p.y -= math.sin(angle) * 14
            p.clamp()
            p.recoil = 12
            for _ in range(8):
                self.particles.append(Particle(p.x + math.cos(angle) * 35, p.y + math.sin(angle) * 35,
                                               (255, 160, 0), size=5, life=12))
        elif w == "sniper":
            b = Bullet(p.x, p.y, angle, speed=25, life=150, damage=5, weapon=w)
            b.size = 8
            self.bullets.append(b)
        elif w == "bazooka":
            b = Bullet(p.x, p.y, angle, speed=16, life=300, damage=100, weapon=w)
            b.explosive = True
            b.size = 12
            self.bullets.append(b)
        elif w == "laser":
            b = Bullet(p.x, p.y, angle, speed=60, life=60, damage=1.5, weapon=w)
            b.size = 4
            self.bullets.append(b)
        elif w == "flamethrower":
            for s in [-0.3, -0.15, 0, 0.15, 0.3]:
                self.make_bullet(angle + s, damage=0.5, speed=12)
        elif w == "plasma":
            b = Bullet(p.x, p.y, angle, speed=20, life=100, damage=3, weapon=w)
            b.size = 8
            self.bullets.append(b)
        elif w == "railgun":
            b = Bullet(p.x + math.cos(angle) * 28, p.y + math.sin(angle) * 28,
                       angle, speed=60, life=220, damage=40 * p.damage_mult, weapon="railgun",
                       size=6, piercing=True)
            self.bullets.append(b)
            p.recoil = 18
        elif w == "tesla":
            b = Bullet(p.x, p.y, angle, speed=40, life=120, damage=8 * p.damage_mult, weapon="tesla", size=6)
            self.bullets.append(b)
        elif w == "cluster":
            for i in range(4):
                spread = random.uniform(-0.08, 0.08)
                b = Bullet(p.x, p.y, angle + spread, speed=26, life=80, damage=2.5 * p.damage_mult,
                           weapon="cluster", size=4)
                self.bullets.append(b)
            p.fire_delay = 36
        elif w == "boomerang":
            b = Bullet(p.x, p.y, angle, speed=22, life=500, damage=10 * p.damage_mult, weapon="boomerang",
                       size=8, boomerang=True, max_travel=360)
            self.bullets.append(b)
            p.recoil = 8

        p.consume_ammo()
        if p.ammo == 0:
            p.start_reload()

    def make_bullet(self, angle, damage=1, speed=BULLET_SPEED, life=120, **kwargs):
        b = Bullet(self.player.x, self.player.y, angle, speed=speed, life=life,
                   damage=damage, weapon=self.player.weapon, **kwargs)
        b.damage *= self.player.damage_mult

        if self.player.explosive_bullets:
            b.explosive = True
        if self.player.piercing:
            b.piercing = True
        if self.player.poison:
            b.poison = True
        if self.player.burn:
            b.burn = True
        if self.player.homing:
            b.homing = True
        if self.player.slow_effect:
            b.slow = True
        if random.random() < self.player.crit_chance:
            b.damage *= 2

        self.bullets.append(b)
        return b

    def chain_lightning(self, start_pos_x, start_pos_y, initial_z, base_damage, bounces=3, radius=140):
        hit_ids = set()
        last_x, last_y = initial_z.x, initial_z.y
        dmg = base_damage
        for bounce in range(bounces):
            nearest = None
            nearest_d = 9999
            for z in self.zombies:
                if id(z) in hit_ids:
                    continue
                d = distance(last_x, last_y, z.x, z.y)
                if d <= radius and d < nearest_d:
                    nearest = z
                    nearest_d = d
            if nearest is None:
                break
            nearest.hp -= dmg
            nearest.flash_timer = 8
            for _ in range(6):
                self.particles.append(Particle(nearest.x + random.uniform(-6, 6), nearest.y + random.uniform(-6, 6),
                                               (180, 230, 255), size=4, life=18))
            if nearest.hp <= 0:
                self.kill_zombie(nearest)
            hit_ids.add(id(nearest))
            last_x, last_y = nearest.x, nearest.y
            dmg *= 0.6

    def use_shockwave(self):
        p = self.player
        if p.shock_cd > 0 or self.game_over or self.paused:
            return
        p.shock_cd = SHOCK_COOLDOWN
        p.invincible = max(p.invincible, 15)
        self.shock_ring = [p.x, p.y, 0]
        for z in self.zombies[:]:
            d = distance(p.x, p.y, z.x, z.y)
            if d < SHOCK_RADIUS:
                z.hp -= self.shock_damage * p.damage_mult
                z.slow_timer = 120
                ang = math.atan2(z.y - p.y, z.x - p.x)
                force = 28 if z.type not in ("boss", "tank") else 14
                z.kx += math.cos(ang) * force
                z.ky += math.sin(ang) * force
                z.flash_timer = 8
                if z.hp <= 0:
                    self.kill_zombie(z)
        self.acid = [a for a in self.acid if distance(p.x, p.y, a.x, a.y) >= SHOCK_RADIUS]
        self.shake = max(self.shake, 18)

    def drop_item(self, x, y):
        r = random.random()
        if r < 0.07:
            self.packs.append(HealthPack(x, y))
        elif r < 0.12:
            self.shields.append(ShieldPU(x, y))
        elif r < 0.24:
            self.ammo_packs.append(AmmoPack(x, y))

    def get_upgrade_choices(self):
        weapons = [
            ("Machine Gun", "weapon", "machinegun"),
            ("Bazooka", "weapon", "bazooka"),
            ("Sniper Rifle", "weapon", "sniper"),
            ("Laser Gun", "weapon", "laser"),
            ("Flamethrower", "weapon", "flamethrower"),
            ("Plasma Gun", "weapon", "plasma"),
            ("Ricochet Shotgun", "weapon", "ricochet"),
            ("Railgun", "weapon", "railgun"),
            ("Tesla Rifle", "weapon", "tesla"),
            ("Cluster Rifle", "weapon", "cluster"),
            ("Boomerang", "weapon", "boomerang"),
            ("Beam", "weapon", "beam"),
        ]
        stats = [
            ("Max HP +20", "stat", "hp"),
            ("Fire Rate +15%", "stat", "firerate"),
            ("Speed +10%", "stat", "speed"),
            ("Dash CD -20%", "stat", "dash"),
            ("Damage +50%", "stat", "dmg"),
            ("Ammo Cap +50%", "stat", "ammo")
        ]
        passives = [
            ("Reload Faster", "passive", "reload_less"),
            ("Explosive Bullets", "passive", "explosive"),
            ("Crit +10%", "passive", "crit"),
            ("Shield Boost", "passive", "shield"),
            ("Poison Bullets", "passive", "poison"),
            ("Burn Damage", "passive", "burn"),
            ("Homing Shots", "passive", "homing"),
            ("Slow Enemies", "passive", "slow"),
            ("Auto-Heal", "passive", "regen"),
            ("Piercing Shots", "passive", "pierce"),
            ("Lifesteal on Kill", "passive", "lifesteal"),
            ("Overcharge Explosions", "passive", "overcharge"),
            ("Shock Boost", "passive", "shock_up"),
            ("Double Health", "passive", "double_hp"),
            ("Extra Ammo", "passive", "extra_ammo"),
            ("Permanent +20% Damage", "passive", "kill_dmg"),
        ]
        choices = []
        choices += random.sample(weapons, 2)
        choices += random.sample(stats, 2)
        choices += random.sample(passives, 1)
        return random.sample(choices, 3)

    def draw_upgrade_menu(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        cx = WIDTH // 2
        cy = HEIGHT // 2
        total_width = 3 * UPGRADE_CARD_W + 2 * 40
        start_x = cx - total_width // 2
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered_index = None

        for i, (name, cat, val) in enumerate(self.upgrade_choices):
            x = start_x + i * (UPGRADE_CARD_W + 40)
            y = cy - UPGRADE_CARD_H // 2
            rect = pygame.Rect(x, y, UPGRADE_CARD_W, UPGRADE_CARD_H)
            pygame.draw.rect(screen, (40, 40, 60), rect, border_radius=18)
            pygame.draw.rect(screen, (90, 90, 140), rect, 4, border_radius=18)
            text = font.render(name, True, (255, 255, 255))
            text_rect = text.get_rect(center=(x + UPGRADE_CARD_W // 2, y + UPGRADE_CARD_H // 2))
            screen.blit(text, text_rect)
            if rect.collidepoint(mouse_x, mouse_y):
                hovered_index = i

        if hovered_index is not None:
            _, _, val = self.upgrade_choices[hovered_index]
            desc = buff_descriptions.get(val, "")
            desc_surface = font.render(desc, True, (255, 255, 255))
            desc_rect = desc_surface.get_rect()
            desc_rect.topleft = (mouse_x + 10, mouse_y + 10)
            bg_rect = desc_rect.inflate(10, 10)
            pygame.draw.rect(screen, (0, 0, 0), bg_rect)
            screen.blit(desc_surface, desc_rect)

    def handle_upgrade_click(self, mx, my):
        cx = WIDTH // 2
        cy = HEIGHT // 2
        total_width = 3 * UPGRADE_CARD_W + 2 * 40
        start_x = cx - total_width // 2
        for i, (name, cat, val) in enumerate(self.upgrade_choices):
            x = start_x + i * (UPGRADE_CARD_W + 40)
            y = cy - UPGRADE_CARD_H // 2
            rect = pygame.Rect(x, y, UPGRADE_CARD_W, UPGRADE_CARD_H)
            if rect.collidepoint(mx, my):
                self.apply_upgrade(cat, val)
                self.show_upgrades = False
                self.paused = False
                return

    def apply_upgrade(self, cat, val):
        p = self.player
        if cat == "weapon":
            p.switch_weapon(val)
        elif cat == "stat":
            if val == "hp":
                p.max_health += 20
                p.health += 20
            elif val == "firerate":
                p.fire_rate = max(4, int(p.fire_rate * 0.85))
            elif val == "speed":
                p.speed *= 1.1
            elif val == "dash":
                p.dash_cd_max = max(20, int(p.dash_cd_max * 0.8))
            elif val == "dmg":
                p.damage_mult *= 1.5
            elif val == "ammo":
                for k, v in p.max_ammo_values.items():
                    p.max_ammo_values[k] = max(1, int(v * 1.5))
                p.max_ammo = p.max_ammo_values.get(p.weapon, p.max_ammo)
                p.ammo = p.max_ammo
        elif cat == "passive":
            if val == "reload_less":
                p.reload_time = {k: max(10, v - 10) for k, v in p.reload_time.items()}
            elif val == "explosive":
                p.explosive_bullets = True
            elif val == "crit":
                p.crit_chance += 0.10
            elif val == "shield":
                p.invincible += 120
            elif val == "poison":
                p.poison = True
            elif val == "burn":
                p.burn = True
            elif val == "homing":
                p.homing = True
            elif val == "slow":
                p.slow_effect = True
            elif val == "regen":
                p.regen += 1
            elif val == "pierce":
                p.piercing = True
            elif val == "lifesteal":
                p.lifesteal += 8
            elif val == "overcharge":
                p.overcharge = True
            elif val == "shock_up":
                self.shock_damage += 2
            elif val == "double_hp":
                p.max_health *= 2
                p.health = p.max_health
            elif val == "extra_ammo":
                for k, v in p.max_ammo_values.items():
                    p.max_ammo_values[k] = int(v * 1.3)
                p.max_ammo = p.max_ammo_values.get(p.weapon, p.max_ammo)
                p.ammo = p.max_ammo
            elif val == "kill_dmg":
                p.damage_mult *= 1.2

    def hit_zombie(self, z, b):
        if z.type == "shielded":
            ball_angle = math.atan2(b.dy, b.dx)
            diff = abs((ball_angle - z.facing_angle + math.pi) % (2 * math.pi) - math.pi)
            if diff < math.pi / 2:
                for _ in range(6):
                    self.particles.append(Particle(b.x, b.y, (200, 220, 255), size=4, life=18,
                                                   vx=random.uniform(-1.5, 1.5), vy=random.uniform(-1.5, 1.5)))
                b.dx *= -0.25
                b.dy *= -0.25
                b.bounces = max(b.bounces, 0)
                return
        dmg = b.damage
        if b.close_bonus and b.traveled < 160:
            dmg *= 2
        z.hp -= dmg
        z.flash_timer = 6
        if b.poison:
            z.poison_damage += 30
        if b.burn:
            z.burn_damage += 30
        if b.slow:
            z.slow_timer = 120
        if b.knockback:
            ang = math.atan2(b.dy, b.dx)
            kb = b.knockback * (2 if (b.close_bonus and b.traveled < 160) else 1)
            if z.type in ("boss", "tank"):
                kb *= 0.4
            z.kx += math.cos(ang) * kb
            z.ky += math.sin(ang) * kb
        b.hit.add(id(z))

    def detonate(self, z):
        p = self.player
        for _ in range(50):
            self.particles.append(Particle(z.x, z.y, (255, 120, 0), size=10, life=30,
                                           vx=random.uniform(-6, 6), vy=random.uniform(-6, 6)))
        if distance(z.x, z.y, p.x, p.y) < 140 and p.invincible == 0:
            p.health -= 25
            self.player_took_damage()
        self.shake = max(self.shake, 20)

    def kill_zombie(self, z):
        if z not in self.zombies:
            return
        self.player.damage_mult += 0.1
        self.combo_count += 1
        self.combo_timer = self.combo_timeout
        multiplier = self.combo_multiplier()
        base = 10
        if z.type == "splitter":
            n = random.randint(2, 3)
            for _ in range(n):
                s = Zombie("fast", z.wave)
                s.x = z.x + random.randint(-18, 18)
                s.y = z.y + random.randint(-18, 18)
                s.hp = max(1, s.hp * 0.6)
                s.max_hp = s.hp
                s.size = 14
                self.zombies.append(s)
        self.score += int(base * multiplier)
        if self.player.lifesteal > 0:
            self.player.health = min(self.player.max_health, self.player.health + self.player.lifesteal)
        self.drop_item(z.x, z.y)
        self.zombies.remove(z)
        for _ in range(20):
            self.particles.append(Particle(z.x, z.y, (200, 0, 0)))
        if z.type == "exploder":
            self.detonate(z)

    def update(self):
        if self.game_over or self.paused:
            return

        keys = pygame.key.get_pressed()
        self.player.move(keys, self.particles)
        self.player.regen_tick()
        self.player.update_reload()

        if self.orbital_cd > 0:
            self.orbital_cd -= 1
        if self.beacon_cd > 0:
            self.beacon_cd -= 1
        if self.adrenaline_cd > 0:
            self.adrenaline_cd -= 1
        if self.immortal_cd > 0:
            self.immortal_cd -= 1

        if self.adrenaline_timer > 0:
            self.player.x += self.adrenaline_dx
            self.player.y += self.adrenaline_dy
            self.player.clamp()
            for z in self.zombies[:]:
                if id(z) in self.adrenaline_hits:
                    continue
                if distance(self.player.x, self.player.y, z.x, z.y) < z.size + 15:
                    z.hp -= ADRENALINE_DAMAGE
                    z.flash_timer = 8
                    self.adrenaline_hits.add(id(z))
                    if z.hp <= 0:
                        self.kill_zombie(z)
            self.adrenaline_timer -= 1

        if self.auto_fire and self.player.weapon == "beam":
            self.shoot()

        if keys[pygame.K_r]:
            self.player.start_reload()
        if keys[pygame.K_e]:
            self.use_shockwave()

        if self.auto_fire and self.player.weapon != "beam":
            self.shoot()

        if self.player.fire_delay > 0:
            self.player.fire_delay -= 1

        self.reinforce()

        for strike in self.pending_strikes[:]:
            strike['timer'] -= 1
            if strike['timer'] <= 0:
                self.explode_orbital(strike)
                self.pending_strikes.remove(strike)

        for b in self.beacons[:]:
            b['timer'] -= 1
            if b['timer'] <= 0 or b.get('used', False):
                try:
                    self.beacons.remove(b)
                except ValueError:
                    pass

        if self.shock_ring:
            self.shock_ring[2] += SHOCK_RADIUS / 14
            if self.shock_ring[2] >= SHOCK_RADIUS:
                self.shock_ring = None

        if self.combo_timer > 0:
            self.combo_timer -= 1
            if self.combo_timer <= 0:
                self.reset_combo()

        for b in self.bullets[:]:
            b.update()

            if b.homing and len(self.zombies) > 0:
                cz = min(self.zombies, key=lambda z: distance(b.x, b.y, z.x, z.y))
                angle = math.atan2(cz.y - b.y, cz.x - b.x)
                b.dx = math.cos(angle) * b.speed
                b.dy = math.sin(angle) * b.speed

            b.bounce()

            if b.boomerang and b.returning and distance(b.x, b.y, self.player.x, self.player.y) < 26:
                if b in self.bullets:
                    self.bullets.remove(b)
                continue

            if b.off():
                if b in self.bullets:
                    self.bullets.remove(b)
                continue

            if b.explosive:
                hit = False
                for z in self.zombies[:]:
                    if distance(b.x, b.y, z.x, z.y) < 100:
                        extra_damage = b.damage
                        if self.player.overcharge:
                            extra_damage *= 1.25
                        z.hp -= extra_damage
                        z.flash_timer = 8
                        if b.poison:
                            z.poison_damage += 50
                        if b.burn:
                            z.burn_damage += 50
                        if z.hp <= 0:
                            self.kill_zombie(z)
                        hit = True
                if hit:
                    for _ in range(40):
                        self.particles.append(Particle(b.x, b.y, (255, 80, 0), size=10, life=30))
                    if b in self.bullets:
                        self.bullets.remove(b)
                    self.shake = max(self.shake, 18)
                continue

            if b.weapon == "tesla":
                for z in self.zombies[:]:
                    if id(z) in b.hit:
                        continue
                    if distance(b.x, b.y, z.x, z.y) < max(30, z.size + 5):
                        z.hp -= b.damage
                        z.flash_timer = 8
                        if z.hp <= 0:
                            self.kill_zombie(z)
                        self.chain_lightning(b.x, b.y, z, b.damage, bounces=3, radius=140)
                        for _ in range(12):
                            self.particles.append(Particle(z.x + random.uniform(-4, 4), z.y + random.uniform(-4, 4),
                                                           (180, 230, 255), size=4, life=16))
                        if b in self.bullets:
                            self.bullets.remove(b)
                        break
                continue

            for z in self.zombies[:]:
                if id(z) in b.hit:
                    continue
                if distance(b.x, b.y, z.x, z.y) < max(30, z.size + 5):
                    self.hit_zombie(z, b)
                    if not b.piercing and not b.boomerang:
                        if b in self.bullets:
                            self.bullets.remove(b)
                    if z.hp <= 0:
                        self.kill_zombie(z)
                    break

        for a in self.acid[:]:
            a.update()
            if a.off():
                self.acid.remove(a)
                continue
            if distance(a.x, a.y, self.player.x, self.player.y) < 25 and self.player.invincible == 0:
                self.player.health -= a.damage
                self.player_took_damage()
                self.acid.remove(a)

        contact_dmg = 1.5 + 0.05 * self.wave
        for z in self.zombies[:]:
            self.acid.extend(z.update(self.player, self))
            if z.hp <= 0:
                self.kill_zombie(z)
                continue
            if distance(z.x, z.y, self.player.x, self.player.y) < z.size + 15:
                if z.type == "exploder":
                    self.detonate(z)
                    self.score += 5
                    self.zombies.remove(z)
                    continue
                if self.player.invincible == 0:
                    self.player.health -= contact_dmg
                    self.player_took_damage()

        for h in self.packs[:]:
            if distance(self.player.x, self.player.y, h.x, h.y) < 30:
                self.player.health = min(self.player.max_health, self.player.health + 25)
                self.packs.remove(h)
        for s in self.shields[:]:
            if distance(self.player.x, self.player.y, s.x, s.y) < 30:
                self.player.invincible += 120
                self.shields.remove(s)
        for a in self.ammo_packs[:]:
            if distance(self.player.x, self.player.y, a.x, a.y) < 30:
                self.player.ammo = self.player.max_ammo
                self.player.is_reloading = False
                self.ammo_packs.remove(a)

        if len(self.zombies) == 0 and self.reinforcements_left == 0 and not self.show_upgrades:
            self.wave += 1
            self.score += 50
            self.spawn_wave()
            self.upgrade_choices = self.get_upgrade_choices()
            self.show_upgrades = True
            self.paused = True

        if self.player.health <= 0:
            active_beacon = None
            for b in self.beacons:
                if not b.get('used', False) and b['timer'] > 0:
                    active_beacon = b
                    break
            if active_beacon:
                bx, by = active_beacon['x'], active_beacon['y']
                self.player.x, self.player.y = bx, by
                self.player.health = max(1, int(self.player.max_health * BEACON_RESPAWN_HEALTH))
                self.player.invincible = 60
                active_beacon['used'] = True
                for _ in range(30):
                    self.particles.append(Particle(bx + random.uniform(-12, 12), by + random.uniform(-12, 12),
                                                   (100, 200, 255), size=random.uniform(4, 8), life=30,
                                                   vx=random.uniform(-2, 2), vy=random.uniform(-2, 2)))
            else:
                self.game_over = True

    def draw(self):
        draw_grid(self.grid_offset)

        for strike in self.pending_strikes:
            x, y, t = strike['x'], strike['y'], strike['timer']
            radius = int(ORBITAL_RADIUS * (1.0 - (t / ORBITAL_WARNING) * 0.4)) + 20
            pygame.draw.circle(screen, (200, 40, 40), (int(x), int(y)), radius, 4)
            warn_text = font.render(f"{max(0, t // FPS + 1)}", True, (255, 220, 220))
            screen.blit(warn_text, (int(x - warn_text.get_width() // 2), int(y - warn_text.get_height() // 2 - radius // 2)))

        for b in self.beacons:
            bx, by = b['x'], b['y']
            used = b.get('used', False)
            color = (120, 200, 255) if not used else (80, 120, 160)
            pygame.draw.circle(screen, color, (int(bx), int(by)), 18, 3)
            pygame.draw.circle(screen, (60, 120, 200), (int(bx), int(by)), 6)

        for z in self.zombies:
            z.draw()
        for b in self.bullets:
            b.draw()
        for a in self.acid:
            a.draw()
        for p in self.particles[:]:
            p.update()
            p.draw()
        self.particles = [p for p in self.particles if p.life > 0]
        for h in self.packs:
            h.draw()
        for s in self.shields:
            s.draw()
        for a in self.ammo_packs:
            a.draw()

        if self.shock_ring:
            x, y, r = self.shock_ring
            pygame.draw.circle(screen, (120, 220, 255), (int(x), int(y)), int(r), 6)
            pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), max(1, int(r * 0.85)), 2)

        self.player.draw()
        self.draw_ui()

        if self.show_upgrades:
            self.draw_upgrade_menu()

        if self.game_over:
            t = big_font.render("YOU DIED", True, (255, 0, 0))
            screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//2 - 50))
            r = font.render(f"Wave {self.wave}  Score {self.score}  -  ENTER to restart", True, (255, 255, 255))
            screen.blit(r, (WIDTH//2 - r.get_width()//2, HEIGHT//2 + 50))
        elif self.paused and self.show_upgrades:
            msg = font.render("Choose an upgrade!", True, (255, 255, 255))
            screen.blit(msg, msg.get_rect(center=(WIDTH//2, 50)))
        elif self.paused and not self.show_upgrades:
            msg = big_font.render("PAUSED", True, (200, 200, 255))
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 50))
            hint = font.render("Press P to resume", True, (180, 180, 180))
            screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT//2 + 50))

        if self.shake > 0:
            temp = screen.copy()
            ox = random.randint(-self.shake, self.shake)
            oy = random.randint(-self.shake, self.shake)
            screen.fill((10, 10, 20))
            screen.blit(temp, (ox, oy))
            self.shake = max(0, self.shake - 1)

    def draw_ui(self):
        p = self.player
        pygame.draw.rect(screen, (255, 0, 0), (20, 20, 220, 20))
        green_width = int(220 * max(0, p.health) / p.max_health)
        pygame.draw.rect(screen, (0, 255, 0), (20, 20, green_width, 20))
        pygame.draw.rect(screen, (100, 100, 100), (20, 50, 220, 20))
        ammo_width = int(220 * (p.ammo / p.max_ammo))
        ammo_color = (255, 200, 0) if not p.is_reloading else (255, 100, 100)
        pygame.draw.rect(screen, ammo_color, (20, 50, ammo_width, 20))

        pygame.draw.rect(screen, (40, 40, 70), (20, 80, 220, 12))
        ready = 1 - p.shock_cd / SHOCK_COOLDOWN
        pygame.draw.rect(screen, (120, 220, 255) if p.shock_cd == 0 else (60, 110, 140),
                         (20, 80, int(220 * ready), 12))

        s = font.render(f"Score: {self.score}", True, (255, 255, 255))
        w = font.render(f"Wave: {self.wave}", True, (255, 255, 255))
        weapon_text = font.render(f"Weapon: {p.weapon.upper()}", True, (255, 255, 255))
        ammo_text = font.render(f"Ammo: {p.ammo}/{p.max_ammo}", True, (255, 200, 0))
        shock_text = font.render("SHOCKWAVE [E]: " + ("READY" if p.shock_cd == 0 else f"{p.shock_cd // 60 + 1}s"),
                                 True, (120, 220, 255))
        left = font.render(f"Enemies: {len(self.zombies) + self.reinforcements_left}", True, (255, 120, 120))

        screen.blit(s, (20, 100))
        screen.blit(w, (20, 130))
        screen.blit(weapon_text, (20, 160))
        screen.blit(ammo_text, (20, 190))
        screen.blit(shock_text, (20, 220))
        screen.blit(left, (20, 250))

        if p.is_reloading:
            screen.blit(font.render("RELOADING...", True, (255, 100, 100)), (20, 280))

        if self.combo_count > 0:
            combo_s = font.render(f"COMBO x{self.combo_multiplier()}  ({self.combo_count})", True, (255, 215, 40))
            screen.blit(combo_s, (WIDTH - 20 - combo_s.get_width(), 20))
        dmg_s = font.render(f"Dmg Mult: {round(p.damage_mult,2)}", True, (220, 180, 40))
        screen.blit(dmg_s, (WIDTH - 20 - dmg_s.get_width(), 50))

        ax = WIDTH - 260
        ay = HEIGHT - 190
        pygame.draw.rect(screen, (40, 40, 40), (ax, ay, 240, 24))
        if self.adrenaline_cd <= 0:
            pygame.draw.rect(screen, (220, 90, 40), (ax + 4, ay + 4, 232, 16))
            screen.blit(font.render("ADRENALINE [F] READY", True, (255, 220, 180)), (ax + 6, ay - 22))
        else:
            frac = 1 - (self.adrenaline_cd / ADRENALINE_COOLDOWN)
            fillw = int(232 * frac)
            pygame.draw.rect(screen, (140, 60, 30), (ax + 4, ay + 4, max(0, fillw), 16))
            screen.blit(font.render(f"ADRENALINE [F]: {self.adrenaline_cd//60}s", True, (200, 180, 160)), (ax + 6, ay - 22))

        imx = WIDTH - 260
        imy = HEIGHT - 150
        pygame.draw.rect(screen, (40, 40, 40), (imx, imy, 240, 24))
        if self.immortal_cd <= 0:
            pygame.draw.rect(screen, (80, 200, 120), (imx + 4, imy + 4, 232, 16))
            screen.blit(font.render("IMMORTAL [I] READY", True, (200, 255, 220)), (imx + 6, imy - 22))
        else:
            frac = 1 - (self.immortal_cd / IMMORTAL_COOLDOWN)
            fillw = int(232 * frac)
            pygame.draw.rect(screen, (60, 140, 90), (imx + 4, imy + 4, max(0, fillw), 16))
            screen.blit(font.render(f"IMMORTAL [I]: {self.immortal_cd//60}s", True, (160, 200, 180)), (imx + 6, imy - 22))

        orbx = WIDTH - 260
        orby = HEIGHT - 110
        pygame.draw.rect(screen, (40, 40, 40), (orbx, orby, 240, 28))
        if self.orbital_cd <= 0:
            pygame.draw.rect(screen, (200, 40, 40), (orbx + 4, orby + 4, 232, 20))
            orb_text = font.render("ORBITAL [X] READY", True, (255, 220, 220))
            screen.blit(orb_text, (orbx + 6, orby - 24))
        else:
            frac = 1 - (self.orbital_cd / ORBITAL_COOLDOWN)
            fillw = int(232 * frac)
            pygame.draw.rect(screen, (120, 40, 40), (orbx + 4, orby + 4, max(0, fillw), 20))
            orb_text = font.render(f"ORBITAL [X]: {self.orbital_cd//60}s", True, (200, 180, 180))
            screen.blit(orb_text, (orbx + 6, orby - 24))

        bx = WIDTH - 260
        by = HEIGHT - 70
        pygame.draw.rect(screen, (40, 40, 40), (bx, by, 240, 28))
        if self.beacon_cd <= 0:
            pygame.draw.rect(screen, (40, 120, 200), (bx + 4, by + 4, 232, 20))
            bc_text = font.render("BEACON [V] READY", True, (200, 230, 255))
            screen.blit(bc_text, (bx + 6, by - 24))
        else:
            frac = 1 - (self.beacon_cd / BEACON_COOLDOWN)
            fillw = int(232 * frac)
            pygame.draw.rect(screen, (40, 80, 150), (bx + 4, by + 4, max(0, fillw), 20))
            bc_text = font.render(f"BEACON [V]: {self.beacon_cd//60}s", True, (180, 200, 220))
            screen.blit(bc_text, (bx + 6, by - 24))

    def restart(self):
        self.__init__()
        self.spawn_wave()

    def run(self):
        self.spawn_wave()
        while True:
            clock.tick(FPS)
            self.grid_offset += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RETURN and self.game_over:
                        self.restart()
                        continue
                    if event.key == pygame.K_p:
                        if not self.show_upgrades and not self.game_over:
                            self.paused = not self.paused
                    if event.key == pygame.K_x and not self.paused and not self.show_upgrades:
                        mx, my = pygame.mouse.get_pos()
                        if self.call_orbital_strike(mx, my):
                            for _ in range(12):
                                self.particles.append(Particle(mx + random.uniform(-6,6), my + random.uniform(-6,6),
                                                               (255, 160, 60), size=5, life=18))
                    if event.key == pygame.K_v and not self.paused and not self.show_upgrades:
                        mx, my = pygame.mouse.get_pos()
                        if self.place_beacon(mx, my):
                            for _ in range(10):
                                self.particles.append(Particle(mx + random.uniform(-6,6), my + random.uniform(-6,6),
                                                               (100, 200, 255), size=5, life=22))
                    if event.key == pygame.K_f and not self.paused and not self.show_upgrades and self.adrenaline_cd <= 0:
                        mx, my = pygame.mouse.get_pos()
                        angle = math.atan2(my - self.player.y, mx - self.player.x)
                        self.adrenaline_dx = math.cos(angle) * ADRENALINE_SPEED
                        self.adrenaline_dy = math.sin(angle) * ADRENALINE_SPEED
                        self.adrenaline_timer = ADRENALINE_DURATION
                        self.adrenaline_cd = ADRENALINE_COOLDOWN
                        self.adrenaline_hits = set()
                        self.player.invincible = max(self.player.invincible, 12)
                        for _ in range(16):
                            self.particles.append(Particle(self.player.x, self.player.y, (255, 80, 80),
                                                           size=6, life=18,
                                                           vx=self.adrenaline_dx * 0.08 + random.uniform(-2, 2),
                                                           vy=self.adrenaline_dy * 0.08 + random.uniform(-2, 2)))
                    if event.key == pygame.K_i and not self.paused and not self.show_upgrades and self.immortal_cd <= 0:
                        self.player.invincible = max(self.player.invincible, IMMORTAL_DURATION)
                        self.immortal_cd = IMMORTAL_COOLDOWN
                        for _ in range(24):
                            self.particles.append(Particle(self.player.x + random.uniform(-12, 12),
                                                           self.player.y + random.uniform(-12, 12),
                                                           (180, 250, 200),
                                                           size=random.uniform(4, 8),
                                                           life=random.randint(30, 60),
                                                           vx=random.uniform(-2, 2),
                                                           vy=random.uniform(-2, 2)))
                        self.shake = max(self.shake, 6)

                if self.show_upgrades:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        self.handle_upgrade_click(mx, my)
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.auto_fire = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.auto_fire = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.player.switch_weapon("pistol")
                    if event.key == pygame.K_2:
                        self.player.switch_weapon("shotgun")
                    if event.key == pygame.K_3:
                        self.player.switch_weapon("machinegun")
                    if event.key == pygame.K_4:
                        self.player.switch_weapon("railgun")
                    if event.key == pygame.K_5:
                        self.player.switch_weapon("tesla")
                    if event.key == pygame.K_6:
                        self.player.switch_weapon("cluster")
                    if event.key == pygame.K_7:
                        self.player.switch_weapon("boomerang")
                    if event.key == pygame.K_8:
                        self.player.switch_weapon("beam")

            if not self.game_over:
                self.update()

            self.draw()
            pygame.display.flip()

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
if __name__ == "__main__":
    start_screen()
    Game().run()