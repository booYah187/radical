#!/usr/bin/env python3
import pygame
import random
import os
import math
import sys

# =========================
# CONFIG
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WIDTH, HEIGHT = 1338, 854
FPS = 60

ORANGE = (255, 140, 0)
BLACK = (0, 0, 0)
TEAL = (0, 200, 180)

FONT_NAME = "monospace"

FACE_DIR = os.path.join(BASE_DIR, "faces")
BEBOP_IMAGE = os.path.join(BASE_DIR, "bebop.png")
SWORDFISH_IMAGE = os.path.join(BASE_DIR, "swordfish.png")

SWORDFISH_SPAWN_CHANCE = 0.0003  # increase for testing, reduce later

# =========================
# INIT
# =========================

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("ED NODE SCREENSAVER")
clock = pygame.time.Clock()

font_small = pygame.font.SysFont(FONT_NAME, 18)
font_med = pygame.font.SysFont(FONT_NAME, 28)
font_chunky_default_size = 64  # will scale dynamically

# =========================
# CONTENT
# =========================

SMALL_TEXT = [
    "SPK-77: BEBOP SIGNAL LOCKED",
    "ED: I HACKED IT ^_^",
    "ERROR: NODE CORRUPTED",
    "SHIP: SWORD FISH II ONLINE",
    "FAYE MEMORY FRAGMENT DETECTED",
    "SPIKE STATUS: UNKNOWN",
    "The work, which becomes a new genre itself, will be called… COWBOY BEBOP.",
    "See You Space Cowboy…",
    "Are You Living in the Real World?",
    "Everything has a beginning and an end.",
    "Easy come, easy go.",
    "The words that came from the deep abyss.",
    "Life is but a dream.",
    "You are different from the others. The eyes tell.",
    "The blue eye perceives all things conjoined. The red eye perceives not the reality.", 
    "You’re gonna carry that weight.",
]

LARGE_TEXT = [
    "BEBOP SYSTEM LOG: Jazz interference detected across relay nodes.",
    "WULF CORP ARCHIVE: bounty records partially overwritten.",
    "NAVIGATION: drift pattern resembles improvisational jazz structure.",
    "They are sick and tired of the conventional styles.They are eager to break through the traditional styles and create new ones.The work, which becomes a new genre itself, will be called…COWBOY BEBOP.",
    "The bounty hunters who assemble in the spaceship Bebop will play freely without dangerous risks.They must create new dreams and films by breaking traditional styles.The work, which becomes a new genre itself, will be called Cowboy Bebop.",
    "All living things, every being that walks and breathes, each has its own star. When a life is born, a new star appears. That is the guardian star... And when a life ends, the star falls... and disappears.",
    "Do not fear death. Death is always at our side. When we show fear, it jumps at us faster than light. But if we do not show fear, it casts its eye upon us gently... and then guides us into... infinity.",
]

lines_left = []
lines_right = []

def random_binary():
    return "".join(random.choice("01") for _ in range(random.randint(20, 60)))

def random_line():
    r = random.random()
    if r < 0.35:
        return random.choice(SMALL_TEXT)
    elif r < 0.65:
        return random_binary()
    else:
        return random.choice(LARGE_TEXT)

def add_lines():
    lines_left.append(random_line())
    lines_right.append(random_line())

# =========================
# EXIT HANDLING
# =========================

def handle_exit(event):
    if event.type == pygame.QUIT:
        return True
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return True
    if event.type == pygame.MOUSEBUTTONDOWN:
        return True
    return False

# =========================
# WARNING POPUP
# =========================

warning_tick = 0

bebop_img = None
if os.path.exists(BEBOP_IMAGE):
    bebop_img = pygame.image.load(BEBOP_IMAGE).convert_alpha()
    bebop_img = pygame.transform.scale(bebop_img, (324, 170))

def draw_warning(surface, bebop_img):
    global warning_tick
    warning_tick += 1

    w = int(WIDTH * 0.7)
    h = int(HEIGHT * 0.35)
    x = (WIDTH - w) // 3
    y = (HEIGHT - h) // 2

    container = pygame.Surface((w, h), pygame.SRCALPHA)

    glitch = random.random() < 0.01
    flicker = 160 + int(80 * math.sin(warning_tick * 0.12))
    container.fill((0, 0, 0, 160 if not glitch else 90))
    pygame.draw.rect(container, TEAL + (flicker,), container.get_rect(), 6)

    # title bar
    title = font_small.render("[ BEBOP SYSTEM NODE COMPROMISED ]", True, TEAL)
    container.blit(title, (w//2 - title.get_width()//2, 12))

    # =========================
    # THREE COLUMN LAYOUT
    # =========================
    col_w = w // 3
    left_x = col_w // 2
    center_x = col_w + col_w // 2
    right_x = col_w * 2 + col_w // 2

    lines = ["WARNING", "CONTAINMENT", "FAILURE"]

    # dynamic scaling to fit columns
    max_text_width = int(col_w * 0.75)
    dynamic_size = font_chunky_default_size

    while dynamic_size > 20:
        test_font = pygame.font.SysFont(FONT_NAME, dynamic_size, bold=True)
        widest = max(test_font.size(word)[0] for word in lines)
        if widest <= max_text_width:
            break
        dynamic_size -= 2

    warning_font = pygame.font.SysFont(FONT_NAME, dynamic_size, bold=True)
    line_spacing = dynamic_size + 18
    start_y = h // 2 - line_spacing

    for i, t in enumerate(lines):
        txt = warning_font.render(t, True, TEAL)
        y_pos = start_y + i * line_spacing
        r_left = txt.get_rect(center=(left_x, y_pos))
        container.blit(txt, r_left)
        r_right = txt.get_rect(center=(right_x, y_pos))
        container.blit(txt, r_right)

    # center image
    if bebop_img:
        img = bebop_img.copy()
        img.set_alpha(255 if not glitch else 120)
        rect = img.get_rect(center=(center_x, h//2))
        container.blit(img, rect)

    # global flash
    if warning_tick % 10 < 5:
        flash = pygame.Surface((w, h), pygame.SRCALPHA)
        flash.fill((0, 0, 0, 40))
        container.blit(flash, (0, 0))

    surface.blit(container, (x, y))

# =========================
# WRAP TEXT HELPER
# =========================

def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        test = current + word + " "
        if font.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = word + " "
    if current:
        lines.append(current)
    return lines

# =========================
# FACES
# =========================

class Face:
    def __init__(self, img, idx):
        self.base = img
        self.img = img
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.vx = random.choice([-3, -2, 2, 3])
        self.vy = random.choice([-3, -2, 2, 3])
        self.idx = idx
        self.visible = True
        self.timer = random.randint(300, 900)
        self.scale_phase = random.random() * 10

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 or self.x > WIDTH:
            self.vx *= -1
        if self.y < 0 or self.y > HEIGHT:
            self.vy *= -1

        if self.idx in [1,2,3]:
            self.timer -= 1
            if self.timer <= 0:
                self.visible = not self.visible
                self.timer = random.randint(300, 900)

        self.scale_phase += 0.05
        scale = 1.0 + 0.15 * math.sin(self.scale_phase)
        size = int(160 * scale)
        self.img = pygame.transform.scale(self.base, (size, size))

    def draw(self, surface):
        if self.visible:
            surface.blit(self.img, (self.x, self.y))

faces = []

def load_faces():
    if not os.path.exists(FACE_DIR):
        return
    files = sorted([f for f in os.listdir(FACE_DIR) if f.endswith(".png")])
    for i, f in enumerate(files):
        img = pygame.image.load(os.path.join(FACE_DIR, f)).convert_alpha()
        img = pygame.transform.scale(img, (160, 160))
        faces.append(Face(img, i))

load_faces()

# =========================
# SWORDFISH
# =========================

swordfish_img = None
if os.path.exists(SWORDFISH_IMAGE):
    swordfish_img = pygame.image.load(SWORDFISH_IMAGE).convert_alpha()
    swordfish_img = pygame.transform.scale(swordfish_img, (107,619))

swordfish_ships = []

class Swordfish:
    def __init__(self, img):
        self.base = img
        side = random.choice(["top","bottom","left","right"])
        if side=="top":
            self.x = random.randint(0,WIDTH)
            self.y = -150
            target_x = random.randint(0,WIDTH)
            target_y = HEIGHT+150
        elif side=="bottom":
            self.x = random.randint(0,WIDTH)
            self.y = HEIGHT+150
            target_x = random.randint(0,WIDTH)
            target_y = -150


        elif side=="left":
            self.x = -150
            self.y = random.randint(0,HEIGHT)
            target_x = WIDTH + 150
            target_y = random.randint(0,HEIGHT)

        else:
            self.x = WIDTH + 150
            self.y = random.randint(0,HEIGHT)
            target_x = -150
            target_y = random.randint(0,HEIGHT)

        dx = target_x - self.x
        dy = target_y - self.y

        dist = math.hypot(dx, dy)

        speed = random.uniform(3, 6)

        self.vx = dx / dist * speed
        self.vy = dy / dist * speed

        # rotate sprite to movement direction
        self.angle = math.degrees(math.atan2(-dy, dx)) - 90

        self.dead = False

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if (
            self.x < -300 or
            self.x > WIDTH + 300 or
            self.y < -300 or
            self.y > HEIGHT + 300
        ):
            self.dead = True

    def draw(self, surface):
        rotated = pygame.transform.rotate(self.base, self.angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        surface.blit(rotated, rect)

# =========================
# MAIN LOOP
# =========================

tick = 0
running = True

while running:

    screen.fill(BLACK)

    for event in pygame.event.get():
        if handle_exit(event):
            running = False

    # =========================
    # TERMINAL STREAM
    # =========================

    if tick % 6 == 0:
        add_lines()

    lines_left[:] = lines_left[-45:]
    lines_right[:] = lines_right[-45:]

    left_y = 20
    right_y = 20

    max_width = WIDTH // 2 - 80

    for line in lines_left:
        wrapped = wrap_text(line, font_small, max_width)

        for sub in wrapped:
            txt = font_small.render(sub, True, ORANGE)
            screen.blit(txt, (40, left_y))
            left_y += 20

    for line in lines_right:
        wrapped = wrap_text(line, font_small, max_width)

        for sub in wrapped:
            txt = font_small.render(sub, True, ORANGE)
            screen.blit(txt, (WIDTH//2 + 40, right_y))
            right_y += 20

    # =========================
    # WARNING POPUP
    # =========================

    draw_warning(screen, bebop_img)

    # =========================
    # FACES
    # =========================

    for f in faces:
        f.update()
        f.draw(screen)

    # =========================
    # SWORDFISH SPAWNING
    # =========================

    # LOWER THIS VALUE FOR LESS FREQUENCY
    if swordfish_img and random.random() < SWORDFISH_SPAWN_CHANCE:
        swordfish_ships.append(Swordfish(swordfish_img))

    for ship in swordfish_ships[:]:
        ship.update()
        ship.draw(screen)

        if ship.dead:
            swordfish_ships.remove(ship)

    pygame.display.flip()

    tick += 1
    clock.tick(FPS)

pygame.quit()
sys.exit()