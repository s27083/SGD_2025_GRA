# Super Ziom - Platformer 2D

Platformówka 2D w stylu Super Ziom napisana w Pythonie z użyciem biblioteki Pygame.

## Funkcjonalności

✅ **Obsługa klawiatury** - pełna kontrola nad postacią (ruch, skok, atak)
✅ **Wykrywanie kolizji** - między graczem, platformami, wrogami i przedmiotami
✅ **Wybór postaci** - Seba lub Adi przed rozpoczęciem gry
✅ **System punktacji** - zbieraj monety i przedmioty aby zdobywać punkty
✅ **System żyć i zdrowia** - pasek zdrowia i system żyć
✅ **Zbieranie przedmiotów** - monety (100 pkt), klucze (500 pkt), power-upy (200 pkt + regeneracja zdrowia)
✅ **Ograniczenie czasowe** - 5 minut na ukończenie poziomu
✅ **Animacje postaci** - różne animacje dla stania, biegu, skoku i spadania
✅ **Muzyka w tle** - automatyczne odtwarzanie muzyki (jeśli dostępna)
✅ **Ekran powitalny** - menu główne z tytułem gry
✅ **Losowo generowane poziomy** - losowe generowanie nowych poziomów

## Sterowanie

### Menu
- **ENTER** - Rozpocznij grę / Potwierdź wybór
- **ESC** - Wyjście / Powrót
- **Strzałki lewo/prawo** - Wybór postaci

### Gra
- **WASD** lub **Strzałki** - Ruch postaci
- **SPACJA** - Skok
- **ESC** - Pauza
- **R** - Restart gry

## Instalacja i uruchomienie

### Wymagania
- Python 3.7+
- Pygame 2.0+

### Kroki instalacji

1. **Sklonuj lub pobierz projekt**
```bash
git clone <repository-url>
cd GRA_SGD
```

2. **Utwórz środowisko wirtualne**
```bash
python3 -m venv game_env
```

3. **Zainstaluj zależności**
```bash
game_env/bin/pip install -r requirements.txt
```

4. **Uruchom grę**
```bash
game_env/bin/python main.py
```

### Alternatywny sposób uruchomienia

1. **Aktywuj środowisko wirtualne**
```bash
source game_env/bin/activate
```

2. **Uruchom grę**
```bash
python main.py
```

3. **Deaktywuj środowisko (po zakończeniu)**
```bash
deactivate
```

## Struktura gry

### Klasy główne:
- **Game** - Główna klasa zarządzająca grą
- **Player** - Klasa gracza z animacjami i fizyką
- **Platform** - Klasa platform do skakania
- **Enemy** - Klasa wrogów z AI
- **Collectible** - Klasa przedmiotów do zbierania

### Stany gry:
- **MENU** - Menu główne
- **CHARACTER_SELECT** - Wybór postaci
- **PLAYING** - Rozgrywka
- **PAUSED** - Pauza
- **GAME_OVER** - Koniec gry

## Rozszerzenia

Gra została zaprojektowana w sposób modularny, co pozwala na łatwe dodawanie:
- Nowych poziomów
- Nowych typów wrogów
- Nowych power-upów
- Nowych mechanik rozgrywki
- Systemu zapisywania wyników
- Multiplayer lokalny

