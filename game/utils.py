"""
Utility Functions
Helper functions used across the game
"""

import pygame
import json
import os
import math
from .settings import SAVE_FILE, ASSET_PATH, GROWTH_STAGES


def load_game_state():
    """Load game state from save file with proper defaults"""
    default_state = {
        "age": 0, 
        "water": 100, 
        "growth_progress": 0.0,
        "last_watered": 0,
        "happiness": 50
    }
    
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                loaded_state = json.load(f)
            
            # Merge with defaults to ensure all keys exist
            for key, default_value in default_state.items():
                if key not in loaded_state:
                    loaded_state[key] = default_value
            
            return loaded_state
        except (json.JSONDecodeError, FileNotFoundError):
            return default_state
    
    return default_state


def save_game_state(state):
    """Save game state to file"""
    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def load_plant_images():
    """Load plant images with fallback placeholders"""
    plant_images = {}
    
    for stage in GROWTH_STAGES:
        try:
            img_path = os.path.join(ASSET_PATH, stage["image"])
            img = pygame.image.load(img_path).convert_alpha()
            plant_images[stage["name"]] = img
        except pygame.error:
            # Create placeholder if image doesn't exist
            placeholder = create_placeholder_image(stage["name"])
            plant_images[stage["name"]] = placeholder
    
    return plant_images


def create_placeholder_image(stage_name):
    """Create placeholder images for missing assets"""
    placeholder = pygame.Surface((100, 100), pygame.SRCALPHA)
    
    if stage_name == "seed":
        pygame.draw.circle(placeholder, (139, 69, 19), (50, 50), 20)
    elif stage_name == "sprout":
        pygame.draw.rect(placeholder, (34, 139, 34), (40, 20, 20, 60))
        pygame.draw.circle(placeholder, (0, 100, 0), (50, 20), 15)
    else:  # flower
        pygame.draw.rect(placeholder, (34, 139, 34), (45, 30, 10, 50))
        for i in range(6):
            angle = i * 60
            x = 50 + 20 * math.cos(math.radians(angle))
            y = 30 + 20 * math.sin(math.radians(angle))
            pygame.draw.circle(placeholder, (255, 20, 147), (int(x), int(y)), 8)
    
    return placeholder


def create_gradient_background(screen, start_color, end_color):
    """Create a vertical gradient background"""
    height = screen.get_height()
    for y in range(height):
        ratio = y / height
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (screen.get_width(), y))


def clamp(value, min_val, max_val):
    """Clamp a value between min and max"""
    return max(min_val, min(value, max_val))


def ease_out_quad(t):
    """Ease-out quadratic function for smooth animations"""
    return 1 - (1 - t) ** 2


def lerp(start, end, t):
    """Linear interpolation between two values"""
    return start + (end - start) * t