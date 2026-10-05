"""Drakens Pixelspel - Ralfs drakspel. Spela om du vågar!

Starta spelet med:  python drakspel.py

Styrning:
    Piltangenter (eller WASD)  = flytta
    Mellanslag                 = skjut
    Enter                      = starta / spela igen
    2 (på startskärmen)        = hoppa direkt till bana 2, djungeln
    Esc                        = avsluta
"""

import math
import random
import sys

import pygame

# ---------------------------------------------------------------------------
# Inställningar - ändra gärna här och se vad som händer!
# ---------------------------------------------------------------------------
W, H = 320, 180          # spelets "riktiga" storlek i pixlar (liten = pixligt)
SCALE = 3                # hur mycket varje pixel förstoras i fönstret
FPS = 60

HERO_SPEED = 90          # pixlar per sekund
HERO_LIVES = 3
HERO_MAX_X = 190         # så här långt åt höger får huvudpersonen gå
SHOT_SPEED = 220
SHOT_DELAY = 0.25        # sekunder mellan skotten
BOSS_HP = 30
FIREBALL_SPEED = 90

# Bana 2: djungeln
JUNGLE_LENGTH = 4000     # hur långt man måste gå för att komma till slutbossen
SCROLL_X = 120           # här på skärmen börjar världen rulla förbi
GROUND_Y = H - 14        # här börjar marken
SPIDER_HP = 40
ENEMY_HP = {"orm": 1, "geting": 1, "groda": 2, "spindel": 2, "kryp": 1}
HEART_CHANCE = 0.15      # chans att en besegrad fiende tappar ett hjärta

# Färger (röd, grön, blå)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (30, 80, 220)
NIGHT = (14, 14, 40)
MOUTH = (60, 8, 16)
JUNGLE_BACK = (10, 36, 22)
JUNGLE_FAR = (18, 58, 34)
LEAF = (50, 150, 60)
LEAF_DARK = (30, 100, 46)
TRUNK = (74, 48, 28)
TRUNK_DARK = (54, 34, 20)
SOIL = (60, 40, 24)
THREAD = (200, 200, 210)

# Varje bokstav i pixelbilderna nedan betyder en färg. Punkt = genomskinligt.
PALETTE = {
    "G": (70, 200, 90),     # grön
    "D": (40, 130, 60),     # mörkgrön
    "H": (240, 220, 130),   # horn
    "R": (200, 40, 40),     # röd
    "M": (130, 20, 30),     # mörkröd
    "Y": (255, 220, 60),    # gul
    "O": (255, 140, 30),    # orange
    "L": (150, 230, 80),    # ljusgrön
    "P": (160, 80, 200),    # lila
    "V": (80, 40, 110),     # mörklila
    "W": WHITE,
    "K": BLACK,
}

# ---------------------------------------------------------------------------
# Pixelbilder - rita om dem om du vill!
# ---------------------------------------------------------------------------
HERO = [
    "HH.....HH",
    ".HH...HH.",
    ".GGGGGGG.",
    ".GWKGWKG.",
    ".GGGGGGG.",
    ".GGKKKGG.",
    "..GGGGG..",
    "GGGGGGGGG",
    "G.GGGGG.G",
    "..GG.GG..",
    ".DDD.DDD.",
]

SHOT = [
    ".Y.",
    "YYY",
    ".Y.",
]

FIREBALL = [
    ".OO.",
    "OYYO",
    "OYYO",
    ".OO.",
]

HEART = [
    ".R.R.",
    "RRRRR",
    "RRRRR",
    ".RRR.",
    "..R..",
]

BOSS_TOP = [
    "...............HH....HH.",
    "...............HH....HH.",
    "...............HH....HH.",
    "........RRRRRRRRRRRRRRRR",
    "......RRRRRRRRRRRRRRRRRR",
    "....RRRRRRRRRRRRRRRRRRRR",
    "..RRRRRRRYYYRRRRRRRRRRRR",
    "..RRRRRRRKYYRRRRRRRRRRRR",
    "RRRRRRRRRRRRRRRRRRRRRRRR",
    "RKRRRRRRRRRRRRRRRRRRRRRR",
    "RRRRRRRRRRRRRRRRRRRRRRRR",
    ".W.W.W.W.W.W.W.W.W.MMMMM",
]

BOSS_JAW = [
    ".W.W.W.W.W.W.W.W.W.MMMMM",
    "RRRRRRRRRRRRRRRRRRRRRRRR",
    "RRRRRRRRRRRRRRRRRRRRRRRR",
    "..RRRRRRRRRRRRRRRRRRRRRR",
    "....RRRRRRRRRRRRRRRRRRRR",
    "......RRRRRRRRRRRRRRRRRR",
]

# Fienderna i djungeln. De med två bilder växlar mellan dem.
ORM_1 = [
    ".OO.......",
    "OKOO..OO..",
    "OOOOOOOOOO",
    "..OOOO..OO",
]

ORM_2 = [
    ".OO.......",
    "OKOO...OO.",
    "OOOO.OOOOO",
    "..OOOOO...",
]

GETING_1 = [
    "...WW.W..",
    "...WWWW..",
    ".YYKYKYK.",
    "YKYKYKYKK",
    ".YYKYKYK.",
]

GETING_2 = [
    ".........",
    "...WWWW..",
    ".YYKYKYK.",
    "YKYKYKYKK",
    ".YYKYKYK.",
]

GRODA = [
    ".LL..LL.",
    "LKWLLKWL",
    "LLLLLLLL",
    "RRRRRLLL",
    "LLLLLLLL",
    "LL.LL.LL",
]

SMALL_SPIDER = [
    "P.P...P.P",
    ".P.PPP.P.",
    "..PRPRP..",
    ".PPPPPPP.",
    "P.PPPPP.P",
    "P.......P",
]

WEB = [
    ".WW.",
    "WWWW",
    "WWWW",
    ".WW.",
]

# Slutbossen i djungeln. Benen ritas för sig så att de kan röra sig.
SPIDER = [
    "....PPPPPP....",
    "..PPPPPPPPPP..",
    ".PPPPVPPVPPPP.",
    ".PPPVVPPVVPPP.",
    "PPPPPVPPVPPPPP",
    "PPPPPPPPPPPPPP",
    ".PPPPPPPPPPPP.",
    "..PPPPPPPPPP..",
    "...VVVVVVVV...",
    "..VRRVVVVRRV..",
    "..VRKVRRVKRV..",
    "..VVVVVVVVVV..",
    "...VWVVVVWV...",
    "....W....W....",
]

HERO_CELL = 2            # hur stor varje ruta i bilden blir
BOSS_CELL = 4
BOSS_X = W - len(BOSS_TOP[0]) * BOSS_CELL
BOSS_TOP_H = len(BOSS_TOP) * BOSS_CELL
BOSS_MAX_GAP = 14        # hur mycket bossen kan öppna munnen
BOSS_MIN_Y = 14
BOSS_MAX_Y = H - BOSS_TOP_H - BOSS_MAX_GAP - len(BOSS_JAW) * BOSS_CELL - 2

# ---------------------------------------------------------------------------
# Pixelbokstäver (5 x 5 rutor)
# ---------------------------------------------------------------------------
FONT = {
    "A": ".XXX./X...X/XXXXX/X...X/X...X",
    "B": "XXXX./X...X/XXXX./X...X/XXXX.",
    "C": ".XXXX/X..../X..../X..../.XXXX",
    "D": "XXXX./X...X/X...X/X...X/XXXX.",
    "E": "XXXXX/X..../XXXX./X..../XXXXX",
    "F": "XXXXX/X..../XXXX./X..../X....",
    "G": ".XXXX/X..../X..XX/X...X/.XXXX",
    "H": "X...X/X...X/XXXXX/X...X/X...X",
    "I": "XXXXX/..X../..X../..X../XXXXX",
    "J": "..XXX/....X/....X/X...X/.XXX.",
    "K": "X...X/X..X./XXX../X..X./X...X",
    "L": "X..../X..../X..../X..../XXXXX",
    "M": "X...X/XX.XX/X.X.X/X...X/X...X",
    "N": "X...X/XX..X/X.X.X/X..XX/X...X",
    "O": ".XXX./X...X/X...X/X...X/.XXX.",
    "P": "XXXX./X...X/XXXX./X..../X....",
    "Q": ".XXX./X...X/X.X.X/X..X./.XX.X",
    "R": "XXXX./X...X/XXXX./X..X./X...X",
    "S": ".XXXX/X..../.XXX./....X/XXXX.",
    "T": "XXXXX/..X../..X../..X../..X..",
    "U": "X...X/X...X/X...X/X...X/.XXX.",
    "V": "X...X/X...X/X...X/.X.X./..X..",
    "W": "X...X/X...X/X.X.X/XX.XX/X...X",
    "X": "X...X/.X.X./..X../.X.X./X...X",
    "Y": "X...X/.X.X./..X../..X../..X..",
    "Z": "XXXXX/...X./..X../.X.../XXXXX",
    "0": ".XXX./X..XX/X.X.X/XX..X/.XXX.",
    "1": "..X../.XX../..X../..X../.XXX.",
    "2": "XXXX./....X/.XXX./X..../XXXXX",
    "3": "XXXX./....X/.XXX./....X/XXXX.",
    "4": "X..X./X..X./XXXXX/...X./...X.",
    "5": "XXXXX/X..../XXXX./....X/XXXX.",
    "6": ".XXX./X..../XXXX./X...X/.XXX.",
    "7": "XXXXX/....X/...X./..X../..X..",
    "8": ".XXX./X...X/.XXX./X...X/.XXX.",
    "9": ".XXX./X...X/.XXXX/....X/.XXX.",
    "!": "..X../..X../..X../...../..X..",
    "?": ".XXX./X...X/...X./...../..X..",
    "=": "...../XXXXX/...../XXXXX/.....",
    "-": "...../...../XXXXX/...../.....",
    ".": "...../...../...../...../..X..",
    ":": "...../..X../...../..X../.....",
}
FONT = {char: rows.split("/") for char, rows in FONT.items()}

# Å, Ä och Ö ritas som A eller O med prickar ovanför.
ACCENTS = {"Å": ("A", "..X.."), "Ä": ("A", ".X.X."), "Ö": ("O", ".X.X.")}


def draw_text(surface, text, x, y, color, size=1):
    """Ritar pixeltext. size = hur stor varje ruta i bokstaven är."""
    for char in text.upper():
        char, accent = ACCENTS.get(char, (char, None))
        for r, row in enumerate(FONT.get(char, [])):
            for c, pixel in enumerate(row):
                if pixel == "X":
                    surface.fill(color, (x + c * size, y + r * size, size, size))
        if accent:
            for c, pixel in enumerate(accent):
                if pixel == "X":
                    surface.fill(color, (x + c * size, y - 2 * size, size, size))
        x += 6 * size


def text_width(text, size=1):
    return len(text) * 6 * size - size


def draw_text_centered(surface, text, y, color, size=1):
    draw_text(surface, text, (W - text_width(text, size)) // 2, y, color, size)


class Sprite:
    """En pixelbild som byggts av en lista med textrader."""

    def __init__(self, rows, cell):
        self.w = max(len(row) for row in rows) * cell
        self.h = len(rows) * cell
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        for r, row in enumerate(rows):
            for c, char in enumerate(row):
                if char in PALETTE:
                    self.image.fill(PALETTE[char], (c * cell, r * cell, cell, cell))
        self.mask = pygame.mask.from_surface(self.image)
        # Helvit version som visas ett ögonblick när något blir träffat.
        self.white = self.mask.to_surface(setcolor=WHITE, unsetcolor=(0, 0, 0, 0))

    def draw(self, surface, x, y, flash=False):
        surface.blit(self.white if flash else self.image, (int(x), int(y)))

    def hits(self, x, y, other, other_x, other_y):
        """Sant om den här bilden och en annan bild överlappar varandra."""
        offset = (int(other_x) - int(x), int(other_y) - int(y))
        return self.mask.overlap(other.mask, offset) is not None


def clamp(value, low, high):
    return max(low, min(high, value))


def scrolling(scroll, spacing):
    """Ger (nummer, x) för saker som står med jämna mellanrum och rullar förbi."""
    first = int(scroll // spacing)
    for n in range(first - 1, first + W // spacing + 2):
        yield n, int(n * spacing - scroll)


class Enemy:
    """En liten fiende i djungeln."""

    def __init__(self, kind, x, y):
        self.kind = kind         # "orm", "geting", "groda", "spindel" eller "kryp"
        self.x = x
        self.y = y
        self.start_y = y
        self.speed_y = 0.0
        self.hp = ENEMY_HP[kind]
        self.time = random.uniform(0, 6)
        self.flash = 0.0


class Game:
    def __init__(self):
        self.hero = Sprite(HERO, HERO_CELL)
        self.shot = Sprite(SHOT, 2)
        self.fireball = Sprite(FIREBALL, 2)
        self.web = Sprite(WEB, 2)
        self.heart = Sprite(HEART, 2)
        self.boss_top = Sprite(BOSS_TOP, BOSS_CELL)
        self.boss_jaw = Sprite(BOSS_JAW, BOSS_CELL)
        self.spider = Sprite(SPIDER, 4)
        small_spider = [Sprite(SMALL_SPIDER, 2)]
        # Fiender med två bilder växlar mellan dem så att de ser ut att röra sig.
        self.enemy_sprites = {
            "orm": [Sprite(ORM_1, 2), Sprite(ORM_2, 2)],
            "geting": [Sprite(GETING_1, 2), Sprite(GETING_2, 2)],
            "groda": [Sprite(GRODA, 2)],
            "spindel": small_spider,
            "kryp": small_spider,
        }

        stars = random.Random(7)
        self.stars = [(stars.randrange(W), stars.randrange(H)) for _ in range(40)]

        self.time = 0.0
        self.start_level(1)
        self.state = "start"     # "start", "play", "clear", "win" eller "lose"

    def start_level(self, level):
        self.level = level       # 1 = draken, 2 = djungeln
        self.state = "play"
        self.play_time = 0.0
        self.banner = "BANA 1: DRAKEN" if level == 1 else "BANA 2: DJUNGELN"
        self.banner_time = 3.0

        self.hero_x = 40.0
        self.hero_y = H / 2 - self.hero.h / 2
        self.lives = HERO_LIVES
        self.invincible = 0.0    # sekunder kvar som man inte kan bli träffad
        self.shot_wait = 0.0
        self.shots = []          # varje skott är [x, y]
        self.fireballs = []      # allt som bossarna skjuter: [x, y, fart_x, fart_y, bild]
        self.particles = []      # [x, y, fart_x, fart_y, tid_kvar, färg]

        # Draken
        self.boss_y = float(BOSS_MIN_Y + 20)
        self.boss_hp = BOSS_HP
        self.boss_flash = 0.0
        self.boss_timer = 0.0
        self.boss_fired = False
        self.boss_gap = 0.0

        # Djungeln
        self.scroll = 0.0        # hur långt man har gått
        self.next_spawn = 150.0  # när nästa fiende dyker upp
        self.enemies = []
        self.pickups = []        # hjärtan man kan plocka upp: [x, y]
        self.spider_active = False
        self.spider_x = 228.0
        self.spider_y = -70.0
        self.spider_hp = SPIDER_HP
        self.spider_flash = 0.0
        self.spider_time = 0.0
        self.spider_timer = 0.0
        self.spider_attacks = 0

    # -- händelser ---------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            enter = event.key in (pygame.K_RETURN, pygame.K_KP_ENTER)
            if self.state == "start":
                if enter or event.key == pygame.K_SPACE:
                    self.start_level(1)
                elif event.key == pygame.K_2:      # genväg direkt till djungeln
                    self.start_level(2)
            elif enter:
                if self.state == "clear":
                    self.start_level(2)
                elif self.state == "lose":
                    self.start_level(self.level)
                elif self.state == "win":
                    self.state = "start"
        elif event.type == pygame.MOUSEBUTTONDOWN and self.state == "start":
            self.start_level(1)

    # -- uppdatering -------------------------------------------------------
    def update(self, dt, keys):
        self.time += dt
        self.update_particles(dt)
        if self.state == "play":
            self.play_time += dt
            self.banner_time = max(0.0, self.banner_time - dt)
            self.update_hero(dt, keys)
            if self.level == 1:
                self.update_boss(dt)
            else:
                self.update_jungle(dt)
                self.update_enemies(dt)
                self.update_pickups(dt)
                if self.spider_active:
                    self.update_spider(dt)
            self.update_shots(dt)
            self.update_fireballs(dt)

    def update_hero(self, dt, keys):
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])

        # På väg genom djungeln rullar världen förbi när man går åt höger.
        walking = self.level == 2 and not self.spider_active
        max_x = SCROLL_X if walking else HERO_MAX_X
        new_x = self.hero_x + dx * HERO_SPEED * dt
        if walking and new_x > max_x:
            self.scroll_world(new_x - max_x)
        self.hero_x = clamp(new_x, 2, max_x)
        floor = GROUND_Y if self.level == 2 else H - 2
        self.hero_y = clamp(self.hero_y + dy * HERO_SPEED * dt, 14, floor - self.hero.h)

        self.invincible = max(0.0, self.invincible - dt)
        self.shot_wait = max(0.0, self.shot_wait - dt)
        if keys[pygame.K_SPACE] and self.shot_wait == 0:
            self.shots.append([self.hero_x + self.hero.w, self.hero_y + 8])
            self.shot_wait = SHOT_DELAY

    def hurt_hero(self):
        self.lives -= 1
        self.invincible = 1.5
        self.burst(self.hero_x + 9, self.hero_y + 11, PALETTE["G"], 10)
        if self.lives <= 0:
            self.state = "lose"

    def shoot_at_hero(self, x, y, sprite, speed, spreads):
        """En boss skjuter något mot huvudpersonen. spreads = vinklar åt sidan."""
        aim = math.atan2(self.hero_y + self.hero.h / 2 - (y + sprite.h / 2),
                         self.hero_x + self.hero.w / 2 - x)
        for spread in spreads:
            self.fireballs.append([x, y, math.cos(aim + spread) * speed, math.sin(aim + spread) * speed, sprite])

    # -- bana 1: draken ----------------------------------------------------
    def update_boss(self, dt):
        angry = self.boss_hp <= BOSS_HP / 2
        self.boss_flash = max(0.0, self.boss_flash - dt)

        # Bossen följer långsamt efter huvudpersonen upp och ner.
        mouth_y = self.boss_y + BOSS_TOP_H + self.boss_gap / 2
        target = self.hero_y + self.hero.h / 2
        step = (45 if angry else 28) * dt
        self.boss_y = clamp(self.boss_y + clamp(target - mouth_y, -step, step), BOSS_MIN_Y, BOSS_MAX_Y)

        # Munnen öppnas, bossen sprutar eld, munnen stängs. Sedan börjar det om.
        self.boss_timer += dt
        phase = self.boss_timer / (1.8 if angry else 2.2)
        if phase < 0.55:
            opening = 0.0
        elif phase < 0.8:
            opening = (phase - 0.55) / 0.25
        else:
            opening = max(0.0, 1 - (phase - 0.8) / 0.2)
            if not self.boss_fired:
                self.boss_fired = True
                y = self.boss_y + BOSS_TOP_H + BOSS_MAX_GAP / 2 - self.fireball.h / 2
                self.shoot_at_hero(BOSS_X + 30, y, self.fireball, FIREBALL_SPEED * (1.3 if angry else 1),
                                   (-0.3, 0, 0.3) if angry else (0,))
        self.boss_gap = BOSS_MAX_GAP * opening
        if phase >= 1:
            self.boss_timer = 0.0
            self.boss_fired = False

    # -- bana 2: djungeln --------------------------------------------------
    def scroll_world(self, distance):
        self.scroll += distance
        for enemy in self.enemies:
            enemy.x -= distance
        for thing in self.pickups + self.fireballs + self.particles:
            thing[0] -= distance

    def update_jungle(self, dt):
        if self.spider_active:
            return
        if self.scroll >= JUNGLE_LENGTH:
            # Framme! Slutbossen kommer och man får tillbaka alla hjärtan.
            self.spider_active = True
            self.lives = HERO_LIVES
            self.banner = "SPINDELN KOMMER!"
            self.banner_time = 2.5
        elif self.next_spawn <= self.scroll < JUNGLE_LENGTH - 200:
            kind = random.choice(["orm", "geting", "groda", "spindel"])
            if kind in ("orm", "groda"):
                y = GROUND_Y - self.enemy_sprites[kind][0].h
            else:
                y = random.uniform(40, 95)
            self.enemies.append(Enemy(kind, W + 10, y))
            self.next_spawn = self.scroll + random.uniform(70, 130)

    def enemy_sprite(self, enemy):
        frames = self.enemy_sprites[enemy.kind]
        return frames[int(enemy.time * 6) % len(frames)]

    def update_enemies(self, dt):
        for enemy in self.enemies[:]:
            enemy.time += dt
            enemy.flash = max(0.0, enemy.flash - dt)
            sprite = self.enemy_sprite(enemy)

            if enemy.kind == "orm":            # ormen ringlar längs marken
                enemy.x -= 30 * dt
            elif enemy.kind == "geting":       # getingen flyger i vågor
                enemy.x -= 55 * dt
                enemy.y = enemy.start_y + math.sin(enemy.time * 4) * 18
            elif enemy.kind == "groda":        # grodan hoppar
                ground = GROUND_Y - sprite.h
                if enemy.y >= ground and enemy.speed_y >= 0:
                    if enemy.speed_y > 0:      # har precis landat, vila en stund
                        enemy.speed_y = 0.0
                        enemy.time = 0.0
                    elif enemy.time > 0.7:
                        enemy.speed_y = -200.0
                else:
                    enemy.x -= 60 * dt
                    enemy.speed_y += 400 * dt
                    enemy.y = min(ground, enemy.y + enemy.speed_y * dt)
            elif enemy.kind == "spindel":      # småspindeln hänger i en tråd
                enemy.y = enemy.start_y + math.sin(enemy.time * 2) * 25
            elif enemy.kind == "kryp":         # bossens småspindlar jagar huvudpersonen
                angle = math.atan2(self.hero_y - enemy.y, self.hero_x - enemy.x)
                enemy.x += math.cos(angle) * 40 * dt
                enemy.y += math.sin(angle) * 40 * dt

            if enemy.x < -30:
                self.enemies.remove(enemy)
            elif self.invincible == 0 and sprite.hits(enemy.x, enemy.y, self.hero, self.hero_x, self.hero_y):
                self.hurt_hero()

    def update_pickups(self, dt):
        for pickup in self.pickups[:]:
            pickup[1] = min(GROUND_Y - self.heart.h - 2, pickup[1] + 40 * dt)
            if pickup[0] < -20:
                self.pickups.remove(pickup)
            elif self.lives < HERO_LIVES and self.hero.hits(self.hero_x, self.hero_y,
                                                            self.heart, pickup[0], pickup[1]):
                self.pickups.remove(pickup)
                self.lives += 1

    def update_spider(self, dt):
        angry = self.spider_hp <= SPIDER_HP / 2
        self.spider_flash = max(0.0, self.spider_flash - dt)
        self.spider_time += dt

        # Spindeln firar ner sig i sin tråd och följer efter huvudpersonen.
        target = clamp(self.hero_y + self.hero.h / 2 - self.spider.h / 2, 16, GROUND_Y - self.spider.h - 14)
        step = (60 if self.spider_y < 16 else 50 if angry else 32) * dt
        self.spider_y += clamp(target - self.spider_y, -step, step)
        self.spider_x = 228 + math.sin(self.spider_time * 0.8) * 14

        self.spider_timer += dt
        if self.spider_y >= 10 and self.spider_timer >= (1.4 if angry else 2.0):
            self.spider_timer = 0.0
            self.spider_attacks += 1
            self.shoot_at_hero(self.spider_x + 10, self.spider_y + 44, self.web, 125 if angry else 100,
                               (-0.3, 0, 0.3) if angry else (0,))
            # Var tredje gång släpper den också loss en liten spindel.
            crawlers = sum(enemy.kind == "kryp" for enemy in self.enemies)
            if self.spider_attacks % 3 == 0 and crawlers < 4:
                self.enemies.append(Enemy("kryp", self.spider_x + 20, self.spider_y + 40))

    # -- skott, eldklot och gnistor ----------------------------------------
    def update_shots(self, dt):
        for shot in self.shots[:]:
            shot[0] += SHOT_SPEED * dt
            if shot[0] > W:
                self.shots.remove(shot)
            elif self.shot_hits_something(shot[0], shot[1]):
                self.shots.remove(shot)
                self.burst(shot[0], shot[1], PALETTE["Y"], 5)
                if self.state != "play":
                    return

    def shot_hits_something(self, x, y):
        if self.level == 1:
            jaw_y = self.boss_y + BOSS_TOP_H + self.boss_gap
            if not (self.boss_top.hits(BOSS_X, self.boss_y, self.shot, x, y)
                    or self.boss_jaw.hits(BOSS_X, jaw_y, self.shot, x, y)):
                return False
            self.boss_hp -= 1
            self.boss_flash = 0.08
            if self.boss_hp <= 0:
                self.state = "clear"
                self.explode(BOSS_X, self.boss_y, 96, 80, "ROY")
            return True

        for enemy in self.enemies:
            if self.enemy_sprite(enemy).hits(enemy.x, enemy.y, self.shot, x, y):
                enemy.hp -= 1
                enemy.flash = 0.08
                if enemy.hp <= 0:
                    self.enemies.remove(enemy)
                    self.burst(enemy.x + 8, enemy.y + 5, WHITE, 8)
                    if enemy.kind != "kryp" and random.random() < HEART_CHANCE:
                        self.pickups.append([enemy.x, enemy.y])
                return True
        if self.spider_active and self.spider.hits(self.spider_x, self.spider_y, self.shot, x, y):
            self.spider_hp -= 1
            self.spider_flash = 0.08
            if self.spider_hp <= 0:
                self.state = "win"
                self.enemies.clear()
                self.fireballs.clear()
                self.explode(self.spider_x, self.spider_y, self.spider.w, self.spider.h, "PVW")
            return True
        return False

    def update_fireballs(self, dt):
        for ball in self.fireballs[:]:
            ball[0] += ball[2] * dt
            ball[1] += ball[3] * dt
            if not (-10 < ball[0] < W + 10 and -10 < ball[1] < H + 10):
                self.fireballs.remove(ball)
            elif self.invincible == 0 and self.hero.hits(self.hero_x, self.hero_y, ball[4], ball[0], ball[1]):
                self.fireballs.remove(ball)
                self.hurt_hero()

    def burst(self, x, y, color, count):
        for _ in range(count):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(20, 90)
            self.particles.append([x, y, math.cos(angle) * speed, math.sin(angle) * speed,
                                   random.uniform(0.3, 0.8), color])

    def explode(self, x, y, w, h, colors):
        """Stor explosion när en boss besegras. colors = bokstäver ur PALETTE."""
        for _ in range(25):
            self.burst(x + random.randrange(w), y + random.randrange(h), PALETTE[random.choice(colors)], 4)

    def update_particles(self, dt):
        for p in self.particles:
            p[0] += p[2] * dt
            p[1] += p[3] * dt
            p[4] -= dt
        self.particles = [p for p in self.particles if p[4] > 0]

    # -- ritning -----------------------------------------------------------
    def draw(self, surface):
        if self.state == "start":
            self.draw_start(surface)
            return
        if self.level == 1:
            self.draw_dragon_level(surface)
        else:
            self.draw_jungle(surface)
        self.draw_hero_and_hud(surface)

        messages = {"clear": ("BANA 1 KLAR!", PALETTE["Y"]), "win": ("DU VANN!", PALETTE["Y"]),
                    "lose": ("GAME OVER", PALETTE["R"])}
        if self.state in messages:
            text, color = messages[self.state]
            surface.fill(BLACK, (0, 50, W, 70))     # svart band bakom texten
            draw_text_centered(surface, text, 60, color, 4)
            if self.time % 1 < 0.6:
                draw_text_centered(surface, "TRYCK ENTER", 100, WHITE, 2)

    def draw_start(self, surface):
        surface.fill(BLACK)
        box = pygame.Rect(16, 12, W - 32, H - 24)
        pygame.draw.rect(surface, WHITE, box)
        pygame.draw.rect(surface, BLUE, box, 2)
        draw_text_centered(surface, "START", 100, BLUE, 6)
        if self.time % 1 < 0.6:
            draw_text_centered(surface, "TRYCK ENTER", 144, BLUE, 1)

    def draw_dragon_level(self, surface):
        surface.fill(NIGHT)
        for i, (x, y) in enumerate(self.stars):
            if (self.time + i * 0.37) % 3 > 0.3:      # stjärnorna blinkar lite
                surface.fill((150, 150, 190), (x, y, 1, 1))

        if self.state != "clear":
            jaw_y = self.boss_y + BOSS_TOP_H + self.boss_gap
            surface.fill(MOUTH, (BOSS_X + 4, int(self.boss_y) + BOSS_TOP_H - 4, 92, int(self.boss_gap) + 8))
        for ball in self.fireballs:
            ball[4].draw(surface, ball[0], ball[1])
        if self.state != "clear":
            flash = self.boss_flash > 0 and self.state == "play"
            self.boss_top.draw(surface, BOSS_X, self.boss_y, flash)
            self.boss_jaw.draw(surface, BOSS_X, jaw_y, flash)
        self.draw_bar(surface, "DRAKE", self.boss_hp / BOSS_HP, PALETTE["R"])

    def draw_jungle(self, surface):
        far = self.scroll * 0.3      # det som är långt bort rullar långsammare
        surface.fill(JUNGLE_BACK)
        for n, x in scrolling(far, 64):
            surface.fill(JUNGLE_FAR, (x + n * 29 % 20, 0, 10 + n * 7 % 6, GROUND_Y))
        for n, x in scrolling(far, 24):
            surface.fill(JUNGLE_FAR, (x, 0, 24, 12 + n * 37 % 18))
        for n, x in scrolling(self.scroll, 150):
            trunk = x + n * 53 % 60
            surface.fill(TRUNK, (trunk, 0, 16, GROUND_Y))
            surface.fill(TRUNK_DARK, (trunk + 12, 0, 4, GROUND_Y))
        for n, x in scrolling(self.scroll, 90):          # lianer
            vine, length = x + n * 31 % 50, 30 + n * 17 % 50
            surface.fill(LEAF, (vine, 0, 2, length))
            surface.fill(LEAF, (vine - 2, length - 4, 6, 4))
        for n, x in scrolling(self.scroll, 20):          # lövverk högst upp
            surface.fill(LEAF_DARK, (x, 0, 20, 4 + n * 23 % 8))
        surface.fill(SOIL, (0, GROUND_Y, W, H - GROUND_Y))
        surface.fill(LEAF, (0, GROUND_Y, W, 3))
        for n, x in scrolling(self.scroll, 14):          # grästuvor
            surface.fill(LEAF, (x + n * 5 % 9, GROUND_Y - 2 - n % 2, 2, 3))

        for enemy in self.enemies:
            sprite = self.enemy_sprite(enemy)
            if enemy.kind == "spindel":
                surface.fill(THREAD, (int(enemy.x) + sprite.w // 2, 0, 1, int(enemy.y) + 2))
            sprite.draw(surface, enemy.x, enemy.y, enemy.flash > 0)
        for x, y in self.pickups:
            self.heart.draw(surface, x, y + math.sin(self.time * 5) * 2)

        if self.spider_active and self.state != "win":
            middle = int(self.spider_x) + self.spider.w // 2
            surface.fill(THREAD, (middle, 0, 1, max(0, int(self.spider_y) + 4)))
            for side in (-1, 1):                         # åtta ben som sprattlar
                for i in range(4):
                    wiggle = math.sin(self.spider_time * 6 + i * 1.3 + side) * 3
                    hip = (middle + side * 16, self.spider_y + 34 + i * 2)
                    knee = (middle + side * (34 + i * 4), self.spider_y + 8 + i * 10 + wiggle)
                    foot = (middle + side * (44 + i * 2), self.spider_y + 30 + i * 9 + wiggle)
                    pygame.draw.lines(surface, PALETTE["P"], False, [hip, knee, foot], 2)
            self.spider.draw(surface, self.spider_x, self.spider_y, self.spider_flash > 0 and self.state == "play")
        for ball in self.fireballs:
            ball[4].draw(surface, ball[0], ball[1])

        if self.spider_active:
            self.draw_bar(surface, "SPINDEL", self.spider_hp / SPIDER_HP, PALETTE["P"])
        else:
            self.draw_bar(surface, "VÄG", self.scroll / JUNGLE_LENGTH, PALETTE["L"])

    def draw_bar(self, surface, label, fraction, color):
        """Mätaren uppe till höger: bossens hälsa eller hur långt man har gått."""
        draw_text(surface, label, 210 - text_width(label), 4, WHITE)
        pygame.draw.rect(surface, WHITE, (214, 3, 102, 7), 1)
        surface.fill(color, (215, 4, int(100 * clamp(fraction, 0, 1)), 5))

    def draw_hero_and_hud(self, surface):
        # Huvudpersonen blinkar en stund efter att ha blivit träffad.
        if self.state != "lose" and int(self.invincible * 10) % 2 == 0:
            self.hero.draw(surface, self.hero_x, self.hero_y)
        for shot in self.shots:
            self.shot.draw(surface, shot[0], shot[1])
        for x, y, _, _, _, color in self.particles:
            surface.fill(color, (int(x), int(y), 2, 2))

        for i in range(self.lives):
            self.heart.draw(surface, 4 + i * 12, 2)
        if self.state == "play" and self.banner_time > 0:
            draw_text_centered(surface, self.banner, 40, WHITE, 2)
        if self.state == "play" and self.level == 1 and self.play_time < 6:
            draw_text_centered(surface, "PILAR = FLYTTA   MELLANSLAG = SKJUT", H - 8, WHITE)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W * SCALE, H * SCALE))
    pygame.display.set_caption("Drakens Pixelspel")
    canvas = pygame.Surface((W, H))      # här ritar vi smått, sedan förstoras allt
    clock = pygame.time.Clock()
    game = Game()

    while True:
        dt = min(clock.tick(FPS) / 1000, 0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            game.handle_event(event)

        game.update(dt, pygame.key.get_pressed())
        game.draw(canvas)
        pygame.transform.scale(canvas, screen.get_size(), screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
