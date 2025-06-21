
import pygame
import random
import time
from scripts.config import *
from scripts.player import Player
from scripts.entities import Platform, Enemy, Collectible

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Super Ziom")
        self.clock = pygame.time.Clock()
        
        # Stan gry
        self.state = GameState.MENU
        self.selected_character = "seba"
        
        # Grupy sprite'ów
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        
        # Statystyki gry
        self.score = 0
        self.keys_collected = 0
        self.total_keys = DEFAULT_TOTAL_KEYS
        self.time_limit = DEFAULT_TIME_LIMIT
        self.start_time = 0
        
        # Czcionki
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # Dźwięk
        self.sound_enabled = True
        self.load_music()
        
        # Tło
        self.load_background()
        
        # Gracz
        self.player = None
        
        # System poziomów
        self.current_level = 0
        self.level_presets = self.create_level_presets()
        
        # Tworzenie poziomu
        self.create_level()
        
    def load_music(self):
        """Ładuje muzykę gry"""
        try:
            pygame.mixer.music.load("lady-of-the-80x27s-128379.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except:
            print("Nie można załadować muzyki")
            
    def load_background(self):
        """Ładuje tło gry"""
        try:
            self.background = pygame.image.load("images/background.png")
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except:
            print("Nie można załadować tła, używam czarnego tła")
            self.background = None
            
    def toggle_sound(self):
        """Przełącza dźwięk gry"""
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            pygame.mixer.music.set_volume(0.5)
            print("Dźwięk: ON")
        else:
            pygame.mixer.music.set_volume(0.0)
            print("Dźwięk: OFF")
            
    def create_level_presets(self):
        """Tworzy predefiniowane presety poziomów"""
        presets = []
        
        # Preset 1 - Klasyczny poziom
        preset1 = {
            'platforms': [
                (0, HEIGHT - 50, WIDTH, 50, "grass"),
                (200, HEIGHT - 150, 200, 20, "stone"),
                (500, HEIGHT - 250, 150, 20, "dirt"),
                (750, HEIGHT - 180, 180, 20, "grass"),
                (100, HEIGHT - 350, 120, 20, "ice"),
                (400, HEIGHT - 400, 200, 20, "metal"),
                (650, HEIGHT - 320, 100, 20, "wood")
            ],
            'enemies': [
                (250, HEIGHT - 200),
                (550, HEIGHT - 300),
                (800, HEIGHT - 230),
                (150, HEIGHT - 400)
            ],
            'collectibles': [
                (300, HEIGHT - 200, "coin"),
                (600, HEIGHT - 300, "coin"),
                (120, HEIGHT - 100, "key"),
                (450, HEIGHT - 450, "key"),
                (900, HEIGHT - 500, "key"),
                (180, HEIGHT - 380, "powerup")
            ]
        }
        
        # Preset 2 - Poziom z lodowymi platformami
        preset2 = {
            'platforms': [
                (0, HEIGHT - 50, WIDTH, 50, "grass"),
                (150, HEIGHT - 200, 150, 20, "ice"),
                (400, HEIGHT - 300, 200, 20, "ice"),
                (700, HEIGHT - 150, 120, 20, "stone"),
                (300, HEIGHT - 450, 180, 20, "metal"),
                (600, HEIGHT - 380, 150, 20, "ice"),
                (50, HEIGHT - 350, 100, 20, "wood")
            ],
            'enemies': [
                (200, HEIGHT - 250),
                (450, HEIGHT - 350),
                (750, HEIGHT - 200),
                (350, HEIGHT - 500),
                (650, HEIGHT - 430)
            ],
            'collectibles': [
                (200, HEIGHT - 250, "coin"),
                (500, HEIGHT - 350, "coin"),
                (800, HEIGHT - 200, "coin"),
                (100, HEIGHT - 100, "key"),
                (400, HEIGHT - 500, "key"),
                (750, HEIGHT - 430, "key"),
                (350, HEIGHT - 500, "powerup"),
                (700, HEIGHT - 430, "powerup")
            ]
        }
        
        # Preset 3 - Poziom pionowy (wieża)
        preset3 = {
            'platforms': [
                (0, HEIGHT - 50, WIDTH, 50, "grass"),
                (400, HEIGHT - 150, 200, 20, "stone"),
                (300, HEIGHT - 250, 200, 20, "dirt"),
                (500, HEIGHT - 350, 200, 20, "metal"),
                (200, HEIGHT - 450, 200, 20, "wood"),
                (600, HEIGHT - 550, 200, 20, "ice"),
                (100, HEIGHT - 200, 100, 20, "stone"),
                (800, HEIGHT - 300, 100, 20, "grass")
            ],
            'enemies': [
                (450, HEIGHT - 200),
                (350, HEIGHT - 300),
                (550, HEIGHT - 400),
                (250, HEIGHT - 500)
            ],
            'collectibles': [
                (450, HEIGHT - 200, "coin"),
                (350, HEIGHT - 300, "coin"),
                (150, HEIGHT - 250, "key"),
                (650, HEIGHT - 600, "key"),
                (850, HEIGHT - 350, "key"),
                (300, HEIGHT - 500, "powerup"),
                (700, HEIGHT - 400, "powerup")
            ]
        }
        
        # Preset 4 - Poziom z przeszkodami
        preset4 = {
            'platforms': [
                (0, HEIGHT - 50, WIDTH, 50, "grass"),
                (100, HEIGHT - 180, 120, 20, "metal"),
                (300, HEIGHT - 220, 100, 20, "stone"),
                (500, HEIGHT - 160, 150, 20, "dirt"),
                (750, HEIGHT - 280, 120, 20, "wood"),
                (200, HEIGHT - 380, 180, 20, "ice"),
                (600, HEIGHT - 420, 200, 20, "metal"),
                (50, HEIGHT - 320, 80, 20, "stone")
            ],
            'enemies': [
                (150, HEIGHT - 230),
                (350, HEIGHT - 270),
                (575, HEIGHT - 210),
                (800, HEIGHT - 330),
                (290, HEIGHT - 430),
                (700, HEIGHT - 470)
            ],
            'collectibles': [
                (160, HEIGHT - 230, "coin"),
                (350, HEIGHT - 270, "coin"),
                (575, HEIGHT - 210, "coin"),
                (130, HEIGHT - 100, "key"),
                (450, HEIGHT - 470, "key"),
                (850, HEIGHT - 330, "key"),
                (250, HEIGHT - 430, "powerup")
            ]
        }
        
        presets.extend([preset1, preset2, preset3, preset4])
        return presets
    
    def create_level(self):
        """Tworzy poziom z predefiniowanych presetów"""
        # Wyczyść istniejące sprite'y
        self.all_sprites.empty()
        self.platforms.empty()
        self.enemies.empty()
        self.collectibles.empty()
        
        # Wybierz losowy preset
        preset = random.choice(self.level_presets)
        
        # Tworzenie platform z presetu
        for x, y, width, height, terrain_type in preset['platforms']:
            platform = Platform(x, y, width, height, terrain_type)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
            
        # Tworzenie wrogów z presetu
        for x, y in preset['enemies']:
            enemy = Enemy(x, y)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            
        # Tworzenie przedmiotów z presetu
        for x, y, item_type in preset['collectibles']:
            collectible = Collectible(x, y, item_type)
            self.collectibles.add(collectible)
            self.all_sprites.add(collectible)
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.CHARACTER_SELECT
                    elif event.key == pygame.K_ESCAPE:
                        return False
                        
                elif self.state == GameState.CHARACTER_SELECT:
                    if event.key == pygame.K_1:
                        self.selected_character = "seba"
                    elif event.key == pygame.K_2:
                        self.selected_character = "adi"
                    elif event.key == pygame.K_SPACE:
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                        
                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.PAUSED
                    elif event.key == pygame.K_m:
                        self.toggle_sound()
                        
                elif self.state == GameState.PAUSED:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_m:
                        self.toggle_sound()
                        
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                        
                elif self.state == GameState.VICTORY:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                        
        return True
        
    def start_game(self):
        self.state = GameState.PLAYING
        self.score = 0
        self.keys_collected = 0
        self.start_time = time.time()
        self.create_level()
        self.player = Player(self.selected_character)
        self.all_sprites.add(self.player)
        
    def restart_game(self):
        """Restartuje grę"""
        if self.player:
            self.all_sprites.remove(self.player)
        self.start_game()
        
    def update(self):
        if self.state == GameState.PLAYING:
            # Aktualizuj gracza
            if self.player:
                self.player.update()
            
            # Aktualizuj przedmioty do zebrania
            self.collectibles.update()
            
            # Aktualizuj wrogów z platformami
            for enemy in self.enemies:
                enemy.update(self.platforms)
                
            # Kolizje gracza z platformami
            self.player.on_ground = False
            for platform in self.platforms:
                if self.player.rect.colliderect(platform.rect):
                    if self.player.vel_y > 0:  # Spadanie
                        self.player.rect.bottom = platform.rect.top
                        self.player.vel_y = 0
                        self.player.on_ground = True
                        
            # Kolizje gracza z wrogami
            for enemy in self.enemies:
                if self.player.rect.colliderect(enemy.rect):
                    # Sprawdź czy gracz skacze na wroga (spadanie z góry)
                    player_center_y = self.player.rect.centery
                    enemy_center_y = enemy.rect.centery
                    
                    # Gracz musi spadać (vel_y > 0) i być wyżej od wroga
                    if (self.player.vel_y > 0 and 
                        player_center_y < enemy_center_y and
                        self.player.rect.bottom <= enemy.rect.centery + 10):
                        # Gracz zabija wroga
                        self.enemies.remove(enemy)
                        self.all_sprites.remove(enemy)
                        self.score += POINTS_ENEMY_KILL
                        self.player.vel_y = JUMP_STRENGTH // 2  
                    else:
                        # Gracz otrzymuje obrażenia
                        result = self.player.take_damage()
                        if result == "GAME_OVER":
                            self.state = GameState.GAME_OVER
                            
            # Kolizje gracza z przedmiotami
            collected = pygame.sprite.spritecollide(self.player, self.collectibles, True)
            for item in collected:
                self.score += item.points
                if item.item_type == "key":
                    self.keys_collected += 1
                elif item.item_type == "powerup":
                    self.player.heal(20)
                    
            # Sprawdź warunki zwycięstwa
            if self.keys_collected >= self.total_keys:
                self.state = GameState.VICTORY
                
            # Sprawdź limit czasu
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= self.time_limit:
                self.state = GameState.GAME_OVER
                
            # Sprawdź czy gracz spadł poza ekran
            if self.player.rect.top > HEIGHT:
                result = self.player.take_damage(self.player.health)  # Zabij gracza
                if result == "GAME_OVER":
                    self.state = GameState.GAME_OVER
                    
    def get_remaining_time(self):
        """Zwraca pozostały czas"""
        if self.state == GameState.PLAYING:
            elapsed = time.time() - self.start_time
            remaining = max(0, self.time_limit - elapsed)
            return int(remaining)
        return self.time_limit
        
    def run(self):
        """Główna pętla gry"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        
    def draw(self):
        """Rysuje wszystkie elementy gry"""
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.CHARACTER_SELECT:
            self.draw_character_select()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.PAUSED:
            self.draw_pause()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.state == GameState.VICTORY:
            self.draw_victory()
            
        pygame.display.flip()
        
    def draw_menu(self):
        """Rysuje menu główne"""
        self.screen.fill(BROWN)
        
        title = self.big_font.render("Super Ziom", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        self.screen.blit(title, title_rect)
        
        start_text = self.font.render("Naciśnij SPACJĘ aby rozpocząć", True, WHITE)
        start_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(start_text, start_rect)
        
        quit_text = self.font.render("ESC - Wyjście", True, WHITE)
        quit_rect = quit_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        self.screen.blit(quit_text, quit_rect)
        
    def draw_character_select(self):
        """Rysuje ekran wyboru postaci"""
        self.screen.fill(BROWN)
        
        title = self.big_font.render("Wybierz postać", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Seba
        seba_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 50, 100, 100)
        seba_color = RED if self.selected_character == "seba" else GRAY
        pygame.draw.rect(self.screen, seba_color, seba_rect)
        if self.selected_character == "seba":
            pygame.draw.rect(self.screen, YELLOW, seba_rect, 5)
        seba_text = self.font.render("1 - Seba", True, WHITE)
        seba_text_rect = seba_text.get_rect(center=(seba_rect.centerx, seba_rect.bottom + 30))
        self.screen.blit(seba_text, seba_text_rect)
        
        # Adi
        adi_rect = pygame.Rect(WIDTH//2 + 50, HEIGHT//2 - 50, 100, 100)
        adi_color = GREEN if self.selected_character == "adi" else GRAY
        pygame.draw.rect(self.screen, adi_color, adi_rect)
        if self.selected_character == "adi":
            pygame.draw.rect(self.screen, YELLOW, adi_rect, 5)
        adi_text = self.font.render("2 - Adi", True, WHITE)
        adi_text_rect = adi_text.get_rect(center=(adi_rect.centerx, adi_rect.bottom + 30))
        self.screen.blit(adi_text, adi_text_rect)
        
        # Instrukcje
        start_text = self.font.render("SPACJA - Start", True, WHITE)
        start_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT - 100))
        self.screen.blit(start_text, start_rect)
        
        back_text = self.font.render("ESC - Powrót", True, WHITE)
        back_rect = back_text.get_rect(center=(WIDTH//2, HEIGHT - 60))
        self.screen.blit(back_text, back_rect)
        
    def draw_game(self):
        """Rysuje grę"""
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_hud()
        
    def draw_hud(self):
        """Rysuje interfejs użytkownika"""
        # Wynik
        score_text = self.font.render(f"Wynik: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Klucze
        keys_text = self.font.render(f"Klucze: {self.keys_collected}/{self.total_keys}", True, WHITE)
        self.screen.blit(keys_text, (10, 50))
        
        # Czas
        time_text = self.font.render(f"Czas: {self.get_remaining_time()}", True, WHITE)
        self.screen.blit(time_text, (10, 90))
        
        # Zdrowie gracza
        if self.player:
            health_text = self.font.render(f"Zdrowie: {self.player.health}", True, WHITE)
            self.screen.blit(health_text, (10, 130))
            
            lives_text = self.font.render(f"Życia: {self.player.lives}", True, WHITE)
            self.screen.blit(lives_text, (10, 170))
            
        # Status dźwięku
        sound_status = "ON" if self.sound_enabled else "OFF"
        sound_text = self.font.render(f"Dźwięk: {sound_status}", True, WHITE)
        self.screen.blit(sound_text, (WIDTH - 150, 10))
        
        # Sterowanie
        controls = [
            "Strzałki/WASD - ruch",
            "SPACJA - skok",
            "ESC - pauza",
            "R (w pauzie) - restart",
            "M - dźwięk"
        ]
        
        for i, control in enumerate(controls):
            control_text = pygame.font.Font(None, 24).render(control, True, WHITE)
            self.screen.blit(control_text, (WIDTH - 200, 50 + i * 25))
            
    def draw_pause(self):
        """Rysuje ekran pauzy"""
        self.draw_game()  # Rysuj grę w tle
        
        # Półprzezroczyste tło
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Tekst pauzy
        pause_text = self.big_font.render("PAUZA", True, WHITE)
        pause_rect = pause_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        self.screen.blit(pause_text, pause_rect)
        
        # Instrukcje
        instructions = [
            "ESC - Kontynuuj",
            "R - Restart",
            "M - Przełącz dźwięk"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + i * 40))
            self.screen.blit(text, text_rect)
            
    def draw_game_over(self):
        """Rysuje ekran końca gry"""
        self.screen.fill(BLACK)
        
        game_over_text = self.big_font.render("KONIEC GRY", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font.render(f"Twój wynik: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        self.screen.blit(score_text, score_rect)
        
        restart_text = self.font.render("R - Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = self.font.render("ESC - Menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
        self.screen.blit(menu_text, menu_rect)
        
    def draw_victory(self):
        """Rysuje ekran zwycięstwa"""
        self.screen.fill(BLACK)
        
        victory_text = self.big_font.render("ZWYCIĘSTWO!", True, GREEN)
        victory_rect = victory_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        self.screen.blit(victory_text, victory_rect)
        
        score_text = self.font.render(f"Twój wynik: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        self.screen.blit(score_text, score_rect)
        
        time_text = self.font.render(f"Czas: {self.time_limit - self.get_remaining_time()}s", True, WHITE)
        time_rect = time_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(time_text, time_rect)
        
        restart_text = self.font.render("R - Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = self.font.render("ESC - Menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
        self.screen.blit(menu_text, menu_rect)