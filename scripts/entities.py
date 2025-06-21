
import pygame
import random
from scripts.config import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, terrain_type="grass"):
        super().__init__()
        
        try:
            # Próbuj załadować odpowiedni SVG
            terrain_file = TERRAIN_FILES.get(terrain_type, "grass_terrain.svg")
            self.image = pygame.image.load(terrain_file)
            self.image = pygame.transform.scale(self.image, (width, height))
        except:
            # Fallback do kolorowej powierzchni
            self.image = pygame.Surface((width, height))
            color = TERRAIN_COLORS.get(terrain_type, GREEN)
            self.image.fill(color)
            
        self.rect = pygame.Rect(x, y, width, height)
        self.terrain_type = terrain_type

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load("images/enemy.png")
        except:
            self.image = pygame.Surface((32, 32))
            self.image.fill(RED)
        self.rect = pygame.Rect(x, y, 32, 32)
        self.vel_x = random.choice([-2, 2])
        self.vel_y = 0
        
    def update(self, platforms):
        # Sprawdź czy wróg stoi na platformie przed ruchem
        on_platform = False
        current_platform = None
        
        for platform in platforms:
            if (self.rect.bottom == platform.rect.top and 
                self.rect.centerx >= platform.rect.left and 
                self.rect.centerx <= platform.rect.right):
                on_platform = True
                current_platform = platform
                break
        
        # Sprawdź czy wróg nie spadnie z platformy po ruchu
        if on_platform and current_platform:
            future_x = self.rect.centerx + self.vel_x
            if (future_x < current_platform.rect.left + 16 or 
                future_x > current_platform.rect.right - 16):
                self.vel_x = -self.vel_x  # Zmień kierunek
        
        # Ruch wroga
        self.rect.x += self.vel_x
        
        # Grawitacja
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        
        # Kolizje z platformami
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Spadanie
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    
        # Odbicie od krawędzi ekranu
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vel_x = -self.vel_x

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type="coin"):
        super().__init__()
        self.item_type = item_type
        
        # Próbuj załadować odpowiedni asset
        try:
            if item_type == "coin":
                self.image = pygame.image.load("images/coin.png")
                self.points = POINTS_COIN
            elif item_type == "key":
                self.image = pygame.image.load("images/key.png")
                self.points = POINTS_KEY
            elif item_type == "powerup":
                self.image = pygame.image.load("images/powerup.png")
                self.points = POINTS_POWERUP
        except:
            # Fallback do prostych kształtów
            if item_type == "coin":
                self.image = pygame.Surface((20, 20))
                self.image.fill(YELLOW)
                self.points = POINTS_COIN
            elif item_type == "key":
                self.image = pygame.Surface((16, 24))
                self.image.fill(ORANGE)
                self.points = POINTS_KEY
            elif item_type == "powerup":
                self.image = pygame.Surface((24, 24))
                self.image.fill(GREEN)
                self.points = POINTS_POWERUP
            
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.bob_timer = 0
        self.original_y = y
        
    def update(self):
        # Efekt "bobowania"
        self.bob_timer += 0.2
        self.rect.y = self.original_y + int(5 * pygame.math.Vector2(0, 1).rotate(self.bob_timer * 10).y)