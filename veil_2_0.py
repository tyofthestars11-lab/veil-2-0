import asyncio
import pygame
import random
import sys
import math

# ---------------------------------------------------------
# VEIL 2.0 - phi EDITION
# Built from Tyree's pasted engine, completed whole:
# keyboard + touch screen + Bluetooth/Xbox controller.
# phi woven in as mechanics, not decoration:
#   - SKILLS is the Phi Strike: damage grows by Fibonacci steps
#   - Victory pays a golden-ratio bonus: 120 gold -> 194 (x phi)
#   - The lair floor carries the golden spiral
# ---------------------------------------------------------

# ---------------------------------------------------------
# 1. INITIALIZATION & SETUP
# ---------------------------------------------------------
pygame.init()
pygame.mixer.init()
pygame.joystick.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
TILE_SIZE = 50

PHI = (1 + math.sqrt(5)) / 2  # 1.618033988749895

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("VEIL 2.0 - phi Edition")
clock = pygame.time.Clock()

# Colors of the Veil expanse palette
COLOR_SAND = (194, 91, 61)
COLOR_SAND_DARK = (150, 60, 40)
COLOR_ROCK = (107, 44, 36)
COLOR_CACTUS = (48, 25, 34)
COLOR_UI_BG = (28, 14, 18)
COLOR_UI_BORDER = (166, 114, 86)
COLOR_TEXT = (240, 220, 200)
COLOR_HEALTH = (190, 38, 51)
COLOR_PHI_GOLD = (232, 184, 75)

# Game States
STATE_EXPLORE = "EXPLORE"
STATE_BATTLE = "BATTLE"
STATE_GAME_OVER = "GAME_OVER"
STATE_VICTORY = "VICTORY"

# ---------------------------------------------------------
# 2. AUTOMATED PIXEL-ART ASSET GENERATORS
# ---------------------------------------------------------
def create_hero_surf():
    surf = pygame.Surface((32, 40), pygame.SRCALPHA)
    pygame.draw.rect(surf, (40, 30, 45), (4, 28, 8, 12))  # Left leg
    pygame.draw.rect(surf, (40, 30, 45), (20, 28, 8, 12)) # Right leg
    pygame.draw.rect(surf, COLOR_ROCK, (2, 12, 28, 18))  # Tunic/Torso
    pygame.draw.rect(surf, (220, 160, 130), (8, 2, 16, 12)) # Head
    pygame.draw.rect(surf, (60, 35, 25), (6, 0, 20, 6))    # Hair
    pygame.draw.rect(surf, (200, 50, 50), (2, 14, 4, 14))   # Scarf/Cape
    return surf

def create_cactus_surf():
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(surf, COLOR_CACTUS, (22, 10, 6, 40)) # Main trunk
    pygame.draw.rect(surf, COLOR_CACTUS, (12, 18, 10, 6)) # Left arm base
    pygame.draw.rect(surf, COLOR_CACTUS, (12, 12, 6, 6))  # Left arm up
    pygame.draw.rect(surf, COLOR_CACTUS, (28, 24, 10, 6)) # Right arm base
    pygame.draw.rect(surf, COLOR_CACTUS, (32, 16, 6, 8))  # Right arm up
    return surf

def create_ruin_surf():
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(surf, COLOR_UI_BORDER, (10, 0, 30, 10))  # Pillar top
    pygame.draw.rect(surf, COLOR_ROCK, (15, 10, 20, 35))       # Shaft
    pygame.draw.rect(surf, COLOR_UI_BORDER, (5, 45, 40, 5))    # Base
    return surf

def create_dragon_surf():
    surf = pygame.Surface((180, 140), pygame.SRCALPHA)
    # Wings
    pygame.draw.polygon(surf, COLOR_SAND_DARK, [(20, 70), (70, 10), (110, 50)])
    pygame.draw.polygon(surf, COLOR_SAND_DARK, [(160, 70), (110, 10), (70, 50)])
    # Body & Tail
    pygame.draw.ellipse(surf, COLOR_ROCK, (40, 50, 100, 60))
    pygame.draw.rect(surf, COLOR_ROCK, (120, 80, 40, 15))
    # Head & Neck
    pygame.draw.polygon(surf, COLOR_ROCK, [(45, 60), (30, 20), (60, 40)])
    pygame.draw.polygon(surf, COLOR_HEALTH, [(30, 20), (10, 15), (25, 35)]) # Head
    pygame.draw.circle(surf, (240, 220, 50), (20, 22), 3) # Glowing eye
    return surf

# Pre-render structures
hero_img = create_hero_surf()
cactus_img = create_cactus_surf()
ruin_img = create_ruin_surf()
dragon_img = create_dragon_surf()
font_game = pygame.font.SysFont("Courier", 18, bold=True)
font_big = pygame.font.SysFont("Courier", 40, bold=True)

# ---------------------------------------------------------
# 3. ENGINE OBJECTS & CLASSES
# ---------------------------------------------------------
def fib(n):
    """Fibonacci, the integer shadow of phi."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

class GameEngine:
    def __init__(self):
        self.state = STATE_EXPLORE
        # Player attributes
        self.player_x = 100
        self.player_y = 200
        self.player_speed = 4
        self.player_hp = 100
        self.player_max_hp = 100
        self.player_potions = 3
        self.player_gold = 0
        self.player_attack = 20

        # Enemy attributes
        self.enemy_name = "VEIL WARDEN"
        self.enemy_hp = 120
        self.enemy_max_hp = 120
        self.enemy_attack = 18

        self.godmode = '--godmode' in sys.argv

        # Phi Strike counter: each SKILLS use climbs one Fibonacci step
        self.phi_step = 5

        # UI Selection Index
        self.battle_selection = 0
        self.battle_options = ["ATTACK", "SKILLS", "ITEM (Potion)", "DEFEND"]
        self.combat_log = ["A wild VEIL WARDEN appears!", "The ground trembles..."]

        # Generate Procedural Veil Expanse Map
        self.map_width = SCREEN_WIDTH // TILE_SIZE
        self.map_height = SCREEN_HEIGHT // TILE_SIZE
        self.obstacles = []
        self.trigger_zone = pygame.Rect(750, 150, 150, 200) # Lair core

        self.generate_map()

    def generate_map(self):
        random.seed(42)  # Keep consistent layout
        for r in range(self.map_height):
            for c in range(self.map_width):
                # Don't spawn objects right at start or inside warden lair
                rect = pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if rect.collidelist([pygame.Rect(50,150,150,150), self.trigger_zone]) == -1:
                    if random.random() < 0.12:
                        self.obstacles.append(('cactus', rect))
                    elif random.random() < 0.05:
                        self.obstacles.append(('ruin', rect))

    def log_message(self, msg):
        self.combat_log.append(msg)
        if len(self.combat_log) > 2:
            self.combat_log.pop(0)

    def execute_battle_turn(self):
        action = self.battle_options[self.battle_selection]

        if action == "ATTACK":
            dmg = random.randint(self.player_attack - 4, self.player_attack + 6)
            if self.godmode:
                dmg = int(dmg * PHI * PHI)
            self.enemy_hp -= dmg
            self.log_message(f"You slash the Warden for {dmg} damage!")
        elif action == "SKILLS":
            step = fib(self.phi_step)
            self.phi_step += 1
            dmg = self.player_attack + step + random.randint(0, 4)
            if self.godmode:
                dmg = int(dmg * PHI * PHI)
            self.enemy_hp -= dmg
            self.log_message(f"Phi Strike (fib {step}) deals {dmg} damage!")
        elif action == "ITEM (Potion)":
            if self.player_potions > 0:
                self.player_hp = min(self.player_max_hp, self.player_hp + 40)
                if not self.godmode:
                    self.player_potions -= 1
                self.log_message("You drank a Potion! Recovered 40 HP.")
            else:
                self.log_message("Out of potions!")
                return
        elif action == "DEFEND":
            self.log_message("You take a defensive stance.")

        # Check Win condition - victory pays in golden ratio: 120 x phi = 194
        if self.enemy_hp <= 0:
            self.enemy_hp = 0
            bonus = int(120 * PHI) - 120
            self.player_gold += 120 + bonus
            self.state = STATE_VICTORY
            return

        # Enemy counter-attack - GODMODE absorbs every blow
        if self.godmode:
            self.log_message("GODMODE absorbs the Warden's blow!")
            return
        enemy_dmg = random.randint(self.enemy_attack - 3, self.enemy_attack + 4)
        if action == "DEFEND":
            enemy_dmg = max(1, enemy_dmg // 3)
        self.player_hp -= enemy_dmg
        self.log_message(f"Veil Warden counters for {enemy_dmg} damage!")

        # Check Lose Condition
        if self.player_hp <= 0:
            self.player_hp = 0
            self.state = STATE_GAME_OVER

# ---------------------------------------------------------
# 4. INPUT - KEYBOARD + TOUCH + BLUETOOTH / XBOX PAD
# ---------------------------------------------------------
joysticks = {}

def refresh_joysticks():
    for i in range(pygame.joystick.get_count()):
        joy = pygame.joystick.Joystick(i)
        joy.init()
        joysticks[joy.get_instance_id()] = joy

refresh_joysticks()

# Touch d-pad (also clickable with a mouse). Drawn in EXPLORE state.
DPAD = {
    'up':    pygame.Rect(70, 330, 54, 54),
    'left':  pygame.Rect(10, 390, 54, 54),
    'down':  pygame.Rect(70, 390, 54, 54),
    'right': pygame.Rect(130, 390, 54, 54),
}
touch_held = set()       # d-pad directions currently held by touch/mouse
finger_points = {}       # finger id -> (x, y) for real touch screens

def point_in_rect(x, y, rect):
    return rect.collidepoint(int(x), int(y))

def touch_press(x, y):
    for name, rect in DPAD.items():
        if point_in_rect(x, y, rect):
            touch_held.add(name)

def touch_release(x, y):
    for name, rect in DPAD.items():
        if point_in_rect(x, y, rect):
            touch_held.discard(name)

def get_move_input():
    """Merge keyboard + gamepad stick/dpad + touch d-pad into (dx, dy)."""
    dx, dy = 0, 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:  dx -= 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += 1
    if keys[pygame.K_UP] or keys[pygame.K_w]:    dy -= 1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:  dy += 1

    for joy in joysticks.values():
        try:
            ax = joy.get_axis(0)
            ay = joy.get_axis(1)
            if abs(ax) > 0.35: dx += 1 if ax > 0 else -1
            if abs(ay) > 0.35: dy += 1 if ay > 0 else -1
            hx, hy = joy.get_hat(0)
            dx += hx
            dy += -hy
        except pygame.error:
            pass

    if 'left' in touch_held:  dx -= 1
    if 'right' in touch_held: dx += 1
    if 'up' in touch_held:    dy -= 1
    if 'down' in touch_held:  dy += 1
    return dx, dy

class PadNav:
    """Edge detection so one d-pad/stick flick = one menu step."""
    def __init__(self):
        self.prev = (0, 0)
    def poll(self):
        cur = (0, 0)
        for joy in joysticks.values():
            try:
                hx, hy = joy.get_hat(0)
                ax, ay = joy.get_axis(0), joy.get_axis(1)
                x = hx + (1 if ax > 0.6 else -1 if ax < -0.6 else 0)
                y = -hy + (1 if ay > 0.6 else -1 if ay < -0.6 else 0)
                cur = (max(-1, min(1, x)), max(-1, min(1, y)))
            except pygame.error:
                pass
        step = (cur[0] if cur[0] != self.prev[0] else 0,
                cur[1] if cur[1] != self.prev[1] else 0)
        self.prev = cur
        return step

pad_nav = PadNav()

# Battle option tap targets (filled each battle render)
battle_option_rects = []
restart_rect = pygame.Rect(SCREEN_WIDTH//2 - 130, 320, 260, 56)
GOD_RECT = pygame.Rect(SCREEN_WIDTH - 152, 42, 140, 40)

def draw_bar(x, y, w, h, value, maximum, color):
    pygame.draw.rect(screen, (10, 10, 10), (x - 2, y - 2, w + 4, h + 4))
    pygame.draw.rect(screen, (70, 30, 30), (x, y, w, h))
    if maximum > 0:
        fill = int(w * max(0, value) / maximum)
        pygame.draw.rect(screen, color, (x, y, fill, h))

def draw_golden_spiral(rect):
    """Golden spiral from nested golden rectangles, drawn on the lair floor."""
    x, y, w, h = rect.x, rect.y, rect.width, rect.height
    a = min(w, h)
    for _ in range(5):
        pygame.draw.arc(screen, COLOR_PHI_GOLD, (x, y, a, a), 0, math.pi / 2, 2)
        na = a / PHI
        x, y, a = x + (a - na), y, na

# ---------------------------------------------------------
# 5. GAME RUN ENGINE LOOP
# ---------------------------------------------------------
async def main():
    battle_option_rects = []
    game = GameEngine()

    while True:
        dt = clock.tick(60)
        await asyncio.sleep(0)

        # --- EVENT PROCESSING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Controller hot-plug (Bluetooth pads connect mid-game)
            if event.type == pygame.JOYDEVICEADDED:
                refresh_joysticks()
            if event.type == pygame.JOYDEVICEREMOVED:
                joysticks.pop(event.instance_id, None)

            # --- Touch screen ---
            if event.type == pygame.FINGERDOWN:
                fx, fy = event.x * SCREEN_WIDTH, event.y * SCREEN_HEIGHT
                finger_points[event.finger_id] = (fx, fy)
                if game.state in (STATE_EXPLORE, STATE_BATTLE) and GOD_RECT.collidepoint(int(fx), int(fy)):
                    game.godmode = not game.godmode
                elif game.state == STATE_EXPLORE:
                    touch_press(fx, fy)
                elif game.state == STATE_BATTLE:
                    for i, r in enumerate(battle_option_rects):
                        if r.collidepoint(int(fx), int(fy)):
                            game.battle_selection = i
                            game.execute_battle_turn()
                            break
                elif game.state in (STATE_GAME_OVER, STATE_VICTORY):
                    if restart_rect.collidepoint(int(fx), int(fy)):
                        game = GameEngine()
            if event.type == pygame.FINGERUP:
                fx, fy = event.x * SCREEN_WIDTH, event.y * SCREEN_HEIGHT
                finger_points.pop(event.finger_id, None)
                touch_release(fx, fy)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if game.state in (STATE_EXPLORE, STATE_BATTLE) and GOD_RECT.collidepoint(mx, my):
                    game.godmode = not game.godmode
                elif game.state == STATE_EXPLORE:
                    touch_press(mx, my)
                elif game.state == STATE_BATTLE:
                    for i, r in enumerate(battle_option_rects):
                        if r.collidepoint(mx, my):
                            game.battle_selection = i
                            game.execute_battle_turn()
                            break
                elif game.state in (STATE_GAME_OVER, STATE_VICTORY):
                    if restart_rect.collidepoint(mx, my):
                        game = GameEngine()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                touch_release(*event.pos)

            # --- Controller buttons: A (0) confirms, Start (7) restarts ---
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 3:
                    game.godmode = not game.godmode
                elif game.state == STATE_BATTLE and event.button == 0:
                    game.execute_battle_turn()
                elif game.state in (STATE_GAME_OVER, STATE_VICTORY) and event.button in (0, 7):
                    game = GameEngine()

            # --- Keyboard ---
            if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                game.godmode = not game.godmode
            if game.state == STATE_BATTLE and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.battle_selection = (game.battle_selection - 1) % len(game.battle_options)
                elif event.key == pygame.K_DOWN:
                    game.battle_selection = (game.battle_selection + 1) % len(game.battle_options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    game.execute_battle_turn()

            elif game.state in [STATE_GAME_OVER, STATE_VICTORY] and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game = GameEngine() # Restart engine

        # --- Controller menu navigation (battle) ---
        if game.state == STATE_BATTLE:
            _, ny = pad_nav.poll()
            if ny < 0:
                game.battle_selection = (game.battle_selection - 1) % len(game.battle_options)
            elif ny > 0:
                game.battle_selection = (game.battle_selection + 1) % len(game.battle_options)

        # --- STATE SIMULATION ENGINE ---
        if game.state == STATE_EXPLORE:
            mx, my = get_move_input()
            dx = mx * game.player_speed
            dy = my * game.player_speed

            # Test Boundaries & Collisions
            new_rect = pygame.Rect(game.player_x + dx, game.player_y + dy, 32, 40)
            collided = False
            if new_rect.left < 0 or new_rect.right > SCREEN_WIDTH or new_rect.top < 0 or new_rect.bottom > SCREEN_HEIGHT:
                collided = True

            for obs_type, obs_rect in game.obstacles:
                if new_rect.colliderect(obs_rect):
                    collided = True
                    break

            if not collided:
                game.player_x += dx
                game.player_y += dy

            # Trigger Warden Boss Arena
            if new_rect.colliderect(game.trigger_zone):
                game.state = STATE_BATTLE

        # --- RENDERING ENGINE ---
        screen.fill(COLOR_SAND)

        if game.state == STATE_EXPLORE:
            # Draw background ground grid detailing
            for r in range(game.map_height):
                for c in range(game.map_width):
                    if (r + c) % 2 == 0:
                        pygame.draw.rect(screen, COLOR_SAND_DARK, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

            # Draw Objects
            for obs_type, obs_rect in game.obstacles:
                if obs_type == 'cactus':
                    screen.blit(cactus_img, obs_rect.topleft)
                else:
                    screen.blit(ruin_img, obs_rect.topleft)

            # Draw Warden lair entrance warning zone + golden spiral floor
            pygame.draw.rect(screen, COLOR_ROCK, game.trigger_zone, 3)
            draw_golden_spiral(game.trigger_zone)
            lbl = font_game.render("WARDEN LAIR", True, COLOR_ROCK)
            screen.blit(lbl, (game.trigger_zone.x + 10, game.trigger_zone.y + 90))

            # Draw Player character (gold aura in GODMODE)
            if game.godmode:
                pygame.draw.rect(screen, COLOR_PHI_GOLD, (game.player_x - 3, game.player_y - 3, 38, 46), 2)
            screen.blit(hero_img, (game.player_x, game.player_y))

            # HUD
            pygame.draw.rect(screen, COLOR_UI_BG, (0, 0, SCREEN_WIDTH, 34))
            hud = font_game.render(
                f"HP {game.player_hp}/{game.player_max_hp}   Potions {game.player_potions}   Gold {game.player_gold}",
                True, COLOR_TEXT)
            screen.blit(hud, (12, 8))
            if game.godmode:
                g = font_game.render("GODMODE", True, COLOR_PHI_GOLD)
                screen.blit(g, (SCREEN_WIDTH - 110, 8))

            # Touch d-pad (semi-transparent, works with finger or mouse)
            pad_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            arrows = {'up': '^', 'down': 'v', 'left': '<', 'right': '>'}
            for name, rect in DPAD.items():
                pygame.draw.rect(pad_surf, (28, 14, 18, 150), rect, border_radius=10)
                pygame.draw.rect(pad_surf, (166, 114, 86, 200), rect, 2, border_radius=10)
                t = font_big.render(arrows[name], True, COLOR_TEXT)
                pad_surf.blit(t, t.get_rect(center=rect.center))
            screen.blit(pad_surf, (0, 0))
            pygame.draw.rect(screen, COLOR_PHI_GOLD if game.godmode else COLOR_UI_BORDER, GOD_RECT, border_radius=8)
            gt = font_game.render("GOD", True, COLOR_UI_BG if game.godmode else COLOR_TEXT)
            screen.blit(gt, gt.get_rect(center=GOD_RECT.center))

        elif game.state == STATE_BATTLE:
            screen.fill(COLOR_UI_BG)
            # Arena
            pygame.draw.rect(screen, COLOR_SAND_DARK, (0, 0, SCREEN_WIDTH, 300))
            draw_golden_spiral(pygame.Rect(410, 60, 180, 180))
            screen.blit(dragon_img, (410, 60))
            screen.blit(hero_img, (120, 220))

            # Enemy plate
            lbl = font_game.render(game.enemy_name, True, COLOR_TEXT)
            screen.blit(lbl, (390, 20))
            draw_bar(390, 44, 240, 16, game.enemy_hp, game.enemy_max_hp, COLOR_HEALTH)
            lbl = font_game.render(f"{game.enemy_hp}/{game.enemy_max_hp}", True, COLOR_TEXT)
            screen.blit(lbl, (640, 42))

            # Hero plate
            lbl = font_game.render("HERO", True, COLOR_TEXT)
            screen.blit(lbl, (60, 300))
            draw_bar(60, 324, 240, 16, game.player_hp, game.player_max_hp, COLOR_HEALTH)
            lbl = font_game.render(
                f"{game.player_hp}/{game.player_max_hp}   Potions {game.player_potions}", True, COLOR_TEXT)
            screen.blit(lbl, (60, 346))

            # Battle options - tappable / clickable / selectable
            battle_option_rects = []
            for i, opt in enumerate(game.battle_options):
                r = pygame.Rect(420, 306 + i * 44, 300, 38)
                battle_option_rects.append(r)
                if i == game.battle_selection:
                    pygame.draw.rect(screen, COLOR_UI_BORDER, r, border_radius=6)
                label = ("> " if i == game.battle_selection else "  ") + opt
                screen.blit(font_game.render(label, True, COLOR_TEXT), (r.x + 10, r.y + 9))

            if game.godmode:
                g = font_game.render("GODMODE", True, COLOR_PHI_GOLD)
                screen.blit(g, (60, 376))

            pygame.draw.rect(screen, COLOR_PHI_GOLD if game.godmode else COLOR_UI_BORDER, GOD_RECT, border_radius=8)
            gt = font_game.render("GOD", True, COLOR_UI_BG if game.godmode else COLOR_TEXT)
            screen.blit(gt, gt.get_rect(center=GOD_RECT.center))

            # Combat log
            for j, line in enumerate(game.combat_log):
                screen.blit(font_game.render(line, True, COLOR_PHI_GOLD), (60, 420 + j * 24))

        elif game.state in (STATE_GAME_OVER, STATE_VICTORY):
            screen.fill(COLOR_UI_BG)
            if game.state == STATE_VICTORY:
                title = font_big.render("VICTORY!", True, COLOR_PHI_GOLD)
                msg = f"The Veil Warden falls. Gold earned: {game.player_gold} (120 x phi)"
            else:
                title = font_big.render("GAME OVER", True, COLOR_HEALTH)
                msg = "The Veil keeps its secrets... this time."
            screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 170)))
            m = font_game.render(msg, True, COLOR_TEXT)
            screen.blit(m, m.get_rect(center=(SCREEN_WIDTH // 2, 240)))
            pygame.draw.rect(screen, COLOR_UI_BORDER, restart_rect, border_radius=8)
            r = font_game.render("PLAY AGAIN", True, COLOR_TEXT)
            screen.blit(r, r.get_rect(center=restart_rect.center))
            hint = font_game.render("ENTER / tap / controller A", True, COLOR_TEXT)
            screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, 420)))

        pygame.display.flip()

if __name__ == "__main__":
    asyncio.run(main())
