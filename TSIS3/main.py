import pygame
import random
import json
import os
import sys

# --- CONFIG ---
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Arcade Pro")
clock = pygame.time.Clock()

# Fonts
font_s = pygame.font.SysFont("Verdana", 18)
font_m = pygame.font.SysFont("Verdana", 30)
font_l = pygame.font.SysFont("Verdana", 50)

# Colors
WHITE, BLACK, RED, GREEN, BLUE, GRAY, GOLD = (255,255,255), (0,0,0), (200,0,0), (0,200,0), (0,0,200), (50,50,50), (255,215,0)

# --- DATA HELPERS ---
def load_json(f, default):
    if not os.path.exists(f): return default
    with open(f, 'r') as file:
        try: return json.load(file)
        except: return default

def save_json(f, data):
    with open(f, 'w') as file: json.dump(data, file, indent=4)

# --- CLASSES ---
class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        colors = {"Red": RED, "Green": GREEN, "Blue": BLUE}
        self.image.fill(colors.get(color_name, RED))
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT-80))
        self.speed = 7

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH: self.rect.x += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill((100, 0, 150))
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH-40), -100))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT: self.kill()

class Obstacle(pygame.sprite.Sprite): # Масляное пятно (Oil Spill)
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (100, 100, 100, 150), [0, 0, 50, 30])
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH-50), -50))
    
    def update(self, speed):
        self.rect.y += speed
        if self.rect.top > HEIGHT: self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, kind):
        super().__init__()
        self.kind = kind
        self.image = pygame.Surface((30, 30))
        color = GOLD if kind=="nitro" else (0, 255, 255) if kind=="shield" else GREEN
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(random.randint(30, WIDTH-30), -50))

    def update(self, speed):
        self.rect.y += speed
        if self.rect.top > HEIGHT: self.kill()

# --- ENGINE ---
class GameApp:
    def __init__(self):
        self.settings = load_json('settings.json', {"sound": True, "color": "Red", "difficulty": 1})
        self.leaderboard = load_json('leaderboard.json', [])
        self.state = "MENU"
        self.username = ""

    def draw_text(self, text, font, color, x, y, center=False):
        img = font.render(text, True, color)
        rect = img.get_rect(topleft=(x, y))
        if center: rect.centerx = WIDTH//2
        screen.blit(img, rect)

    def input_name(self):
        self.username = ""
        entering = True
        while entering:
            screen.fill(BLACK)
            self.draw_text("Enter Your Name:", font_m, WHITE, 0, 200, True)
            self.draw_text(self.username + "_", font_m, GREEN, 0, 260, True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(self.username) > 0: entering = False
                    elif event.key == pygame.K_BACKSPACE: self.username = self.username[:-1]
                    else: 
                        if len(self.username) < 10: self.username += event.unicode
            pygame.display.update()

    def leaderboard_screen(self):
        while True:
            screen.fill(GRAY)
            self.draw_text("TOP 10", font_l, GOLD, 0, 50, True)
            for i, entry in enumerate(self.leaderboard[:10]):
                txt = f"{i+1}. {entry['name']} - {entry['score']} pts"
                self.draw_text(txt, font_s, WHITE, 50, 150 + i*35)
            
            self.draw_text("Press B for Menu", font_s, GREEN, 0, 550, True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_b: return
            pygame.display.update()

    def game_loop(self):
        self.input_name()
        diff = int(self.settings.get('difficulty', 1))
        base_speed = 4 + diff
        player = Player(self.settings['color'])
        enemies = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        obstacles = pygame.sprite.Group()
        
        score, distance = 0, 0
        active_buff = None
        buff_end = 0
        running = True

        while running:
            screen.fill((30, 30, 30))
            dt = clock.tick(60)

            # Начисление Score за движение
            speed_mult = 2 if active_buff == "nitro" else 1
            current_speed = base_speed * speed_mult
            distance += current_speed * 0.1
            score += speed_mult * 0.1 # Счёт теперь растет!

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()

            # Difficulty Scaling
            if int(distance) % 500 == 0 and distance > 1: base_speed += 0.005

            # Spawn logic
            if random.randint(1, 60) == 1: enemies.add(Enemy(current_speed + random.randint(1,3)))
            if random.randint(1, 150) == 1: obstacles.add(Obstacle())
            if random.randint(1, 400) == 1: powerups.add(PowerUp(random.choice(["nitro", "shield", "repair"])))

            # Updates
            player.move()
            enemies.update()
            obstacles.update(current_speed)
            powerups.update(current_speed)

            # Collisions
            if pygame.sprite.spritecollide(player, enemies, True) or pygame.sprite.spritecollide(player, obstacles, True):
                if active_buff == "shield":
                    active_buff = None
                else:
                    self.save_score(int(score), int(distance))
                    self.state = "GAMEOVER"
                    return

            p_col = pygame.sprite.spritecollide(player, powerups, True)
            for p in p_col:
                if p.kind == "repair": score += 100
                else:
                    active_buff = p.kind
                    buff_end = pygame.time.get_ticks() + 5000

            if active_buff and pygame.time.get_ticks() > buff_end: active_buff = None

            # Rendering
            obstacles.draw(screen)
            enemies.draw(screen)
            powerups.draw(screen)
            screen.blit(player.image, player.rect)
            
            # HUD
            self.draw_text(f"SCORE: {int(score)}", font_s, WHITE, 10, 10)
            self.draw_text(f"DIST: {int(distance)}m", font_s, WHITE, 10, 35)
            if active_buff: self.draw_text(f"BUFF: {active_buff.upper()}", font_s, GOLD, 10, 60)
            
            pygame.display.update()

    def settings_screen(self):
        while self.state == "SETTINGS":
            screen.fill(GRAY)
            self.draw_text("SETTINGS", font_m, WHITE, 0, 100, True)
            self.draw_text(f"1. Difficulty: {self.settings['difficulty']}", font_s, WHITE, 100, 250)
            self.draw_text(f"2. Color: {self.settings['color']}", font_s, WHITE, 100, 300)
            self.draw_text("Press M for Menu", font_s, GREEN, 0, 500, True)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.settings['difficulty'] = (self.settings['difficulty'] % 3) + 1
                    if event.key == pygame.K_2:
                        colors = ["Red", "Green", "Blue"]
                        self.settings['color'] = colors[(colors.index(self.settings['color'])+1)%3]
                    if event.key == pygame.K_m:
                        save_json('settings.json', self.settings)
                        self.state = "MENU"
            pygame.display.update()

    def save_score(self, s, d):
        self.leaderboard.append({"name": self.username, "score": s, "dist": d})
        self.leaderboard = sorted(self.leaderboard, key=lambda x: x['score'], reverse=True)[:10]
        save_json('leaderboard.json', self.leaderboard)

    def menu(self):
        while self.state == "MENU":
            screen.fill(BLACK)
            self.draw_text("RACER PRO", font_l, RED, 0, 100, True)
            self.draw_text("P - Play", font_m, WHITE, 150, 250)
            self.draw_text("S - Settings", font_m, WHITE, 150, 310)
            self.draw_text("L - Leaderboard", font_m, WHITE, 150, 370)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p: self.state = "GAME"
                    if event.key == pygame.K_s: self.state = "SETTINGS"
                    if event.key == pygame.K_l: self.leaderboard_screen()
            pygame.display.update()

    def run(self):
        while True:
            if self.state == "MENU": self.menu()
            elif self.state == "GAME": self.game_loop()
            elif self.state == "SETTINGS": self.settings_screen()
            elif self.state == "GAMEOVER": self.state = "MENU"

if __name__ == "__main__":
    GameApp().run()