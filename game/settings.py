"""
Game Settings and Constants
All configurable values in one place
"""

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Growth stage configuration
GROWTH_STAGES = [
    {
        "name": "seed", 
        "image": "seed.png.webp", 
        "start_age": 0, 
        "full_size_age": 5, 
        "base_scale": 0.3
    },
    {
        "name": "sprout", 
        "image": "sprout.png.webp", 
        "start_age": 8, 
        "full_size_age": 15, 
        "base_scale": 0.6
    },
    {
        "name": "flower", 
        "image": "flower.png.webp", 
        "start_age": 18, 
        "full_size_age": 25, 
        "base_scale": 1.0
    }
]

# File paths
SAVE_FILE = "data/savegame.json"
ASSET_PATH = "assets/images"

# Animation settings
GROWTH_ANIMATION_SPEED = 2.0
WATER_EFFECT_DURATION = 1.0
BREATHING_SPEED = 1.5

# Game states
MENU = "menu"
PLAYING = "playing"

# Colors
COLORS = {
    'background_start': (135, 206, 235),
    'background_end': (200, 255, 200),
    'ground': (101, 67, 33),
    'water_high': (0, 150, 255),
    'water_medium': (255, 200, 0),
    'water_low': (255, 100, 100),
    'text_dark': (50, 50, 50),
    'text_light': (255, 255, 255),
    'panel_bg': (255, 255, 255, 200),
    'panel_border': (100, 100, 100),
    'button_normal': (34, 139, 34),
    'button_hover': (50, 180, 50)
}

# Plant care settings
WATER_GAIN_PER_ACTION = 25
HAPPINESS_GAIN_PER_WATER = 10
WATER_LOSS_NORMAL = 1
WATER_LOSS_STRESSED = 2
HAPPINESS_THRESHOLD_STRESSED = 30
HAPPINESS_THRESHOLD_HAPPY = 60
NEGLECT_TIME_THRESHOLD = 15