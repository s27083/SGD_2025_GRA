"""Klasa gracza dla gry Super Ziom"""

import pygame
from scripts.config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, character_type="seba"):
        super().__init__()
        self.character_type = character_type
        self.load_animations()
        
        # Stan gracza
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = HEIGHT - 200
        
        # Fizyka
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        
        # Animacje
        self.current_animation = "idle"
        self.animation_frame = 0
        self.animation_timer = 0
        
        # Statystyki
        self.lives = DEFAULT_PLAYER_LIVES
        self.health = DEFAULT_PLAYER_HEALTH
        self.invulnerable = False
        self.invulnerable_timer = 0
        
    def load_animations(self):
        """Ładuje animacje gracza"""
        try:
            # Próbuj załadować specyficzne assety dla postaci
            char_prefix = self.character_type
            self.animations = {
                "idle": [pygame.image.load(f"images/{char_prefix}_idle.png")],
                "run": [pygame.image.load(f"images/{char_prefix}_run.png")],
                "jump": [pygame.image.load(f"images/{char_prefix}_jump.png")],
                "fall": [pygame.image.load(f"images/{char_prefix}_fall.png")]
            }
        except:
            try:
                # Fallback do oryginalnych assetów
                self.animations = {
                    "idle": [pygame.image.load("images/player_idle.png")],
                    "run": [pygame.image.load("images/player_run.png")],
                    "jump": [pygame.image.load("images/player_jump.png")],
                    "fall": [pygame.image.load("images/player_fall.png")]
                }
            except:
                # Ostateczny fallback - prostokąty kolorowe
                self.animations = {
                    "idle": [pygame.Surface((32, 48))],
                    "run": [pygame.Surface((32, 48))],
                    "jump": [pygame.Surface((32, 48))],
                    "fall": [pygame.Surface((32, 48))]
                }
                for anim in self.animations.values():
                    anim[0].fill(RED if self.character_type == "seba" else GREEN)
        
        self.image = self.animations["idle"][0]
        
    def update(self):
        """Aktualizuje gracza"""
        # Obsługa klawiatury
        keys = pygame.key.get_pressed()
        
        # Ruch poziomy
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
            self.facing_right = False
            self.current_animation = "run"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
            self.facing_right = True
            self.current_animation = "run"
        else:
            self.current_animation = "idle"
            
        # Skok
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
            
        # Animacje w powietrzu
        if not self.on_ground:
            if self.vel_y < 0:
                self.current_animation = "jump"
            else:
                self.current_animation = "fall"
                
        # Aktualizuj pozycję
        self.rect.x += self.vel_x
        
        # Grawitacja
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        
        # Ograniczenia ekranu
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
            
        # Aktualizuj animację
        self.update_animation()
        
        # Aktualizuj nietykalność
        if self.invulnerable:
            self.invulnerable_timer -= 1/FPS
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                
    def update_animation(self):
        """Aktualizuje animację gracza"""
        self.animation_timer += 1
        if self.animation_timer >= 10:  # Zmień klatkę co 10 klatek gry
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % len(self.animations[self.current_animation])
            
        # Ustaw aktualną klatkę
        self.image = self.animations[self.current_animation][self.animation_frame]
        
        # Odbij obraz jeśli gracz idzie w lewo
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
            
    def take_damage(self, damage=20):
        """Gracz otrzymuje obrażenia"""
        if not self.invulnerable:
            self.health -= damage
            self.invulnerable = True
            self.invulnerable_timer = INVULNERABILITY_TIME
            
            if self.health <= 0:
                self.health = 0
                self.lives -= 1
                if self.lives > 0:
                    self.health = DEFAULT_PLAYER_HEALTH  # Odnów zdrowie
                    # Resetuj pozycję gracza
                    self.rect.x = 100
                    self.rect.y = HEIGHT - 200
                else:
                    return "GAME_OVER"
        return None
        
    def heal(self, amount=20):
        """Leczy gracza"""
        self.health = min(self.health + amount, DEFAULT_PLAYER_HEALTH)
        
    def add_life(self):
        """Dodaje życie graczowi"""
        self.lives += 1