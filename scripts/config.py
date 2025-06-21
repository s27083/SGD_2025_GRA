"""Konfiguracja gry Super Ziom"""

import pygame
from enum import Enum

pygame.init()
pygame.mixer.init()

# Stałe gry
WIDTH = 1024
HEIGHT = 768
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)

class GameState(Enum):
    MENU = 1
    CHARACTER_SELECT = 2
    PLAYING = 3
    GAME_OVER = 4
    PAUSED = 5
    VICTORY = 6

# Ustawienia gry
DEFAULT_TIME_LIMIT = 30  # sekundy
DEFAULT_TOTAL_KEYS = 3
DEFAULT_PLAYER_LIVES = 1
DEFAULT_PLAYER_HEALTH = 100

# Punkty za różne akcje
POINTS_COIN = 100
POINTS_KEY = 500
POINTS_POWERUP = 200
POINTS_ENEMY_KILL = 200

# Czas nietykalności po otrzymaniu obrażeń (w sekundach)
INVULNERABILITY_TIME = 2.0

# Kolory terenu
TERRAIN_COLORS = {
    "grass": (34, 139, 34),     # Forest Green
    "stone": (105, 105, 105),   # Dim Gray
    "dirt": (139, 69, 19),      # Saddle Brown
    "ice": (173, 216, 230),     # Light Blue
    "lava": (255, 69, 0),       # Red Orange
    "sand": (238, 203, 173),    # Peach Puff
    "metal": (192, 192, 192),   # Silver
    "wood": (160, 82, 45)       # Saddle Brown
}

# Pliki terenu
TERRAIN_FILES = {
    "grass": "images/grass_terrain.svg",
    "stone": "images/stone_terrain.svg",
    "dirt": "images/dirt_terrain.svg",
    "ice": "images/ice_terrain.svg",
    "lava": "images/lava_terrain.svg",
    "sand": "images/sand_terrain.svg",
    "metal": "images/metal_terrain.svg",
    "wood": "images/wood_terrain.svg"
}

# Typy terenu
TERRAIN_TYPES = ["grass", "stone", "dirt", "ice", "lava", "sand", "metal", "wood"]