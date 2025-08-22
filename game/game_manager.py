"""
Game Manager
Main game loop and state management
"""

import pygame
import sys
from .settings import *
from .utils import load_game_state, save_game_state, load_plant_images
from .plant import Plant
from .ui import UI
from .menu import Menu


class GameManager:
    def __init__(self):
        self.setup_pygame()
        self.setup_game_objects()
        self.setup_game_state()
    
    def setup_pygame(self):
        """Initialize Pygame and create window"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🌱 Virtual Plant Buddy - Enhanced Growth")
        self.clock = pygame.time.Clock()
    
    def setup_game_objects(self):
        """Initialize game objects"""
        # Load assets
        self.plant_images = load_plant_images()
        
        # Create game objects
        self.plant = Plant(self.plant_images)
        self.ui = UI(self.screen)
        self.menu = Menu(self.screen)
    
    def setup_game_state(self):
        """Initialize game state"""
        self.game_state = MENU
        self.animation_time = 0
        self.water_effect_time = 0
        self.elapsed_time = 0
        
        # Load saved plant state
        saved_state = load_game_state()
        self.plant.load_state(saved_state)
    
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == MENU:
                    if self.menu.handle_click(event.pos):
                        self.game_state = PLAYING
            
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
    
    def handle_keydown(self, key):
        """Handle keyboard input"""
        if self.game_state == MENU:
            if key in (pygame.K_SPACE, pygame.K_RETURN):
                self.game_state = PLAYING
        
        elif self.game_state == PLAYING:
            if key in (pygame.K_w, pygame.K_SPACE):
                if self.plant.water():
                    self.water_effect_time = WATER_EFFECT_DURATION
            
            elif key == pygame.K_r:
                self.plant.reset()
            
            elif key == pygame.K_ESCAPE:
                save_game_state(self.plant.get_state())
                self.game_state = MENU
    
    def update(self, dt):
        """Update game logic"""
        self.animation_time += dt
        
        # Update water effect timer
        if self.water_effect_time > 0:
            self.water_effect_time -= dt
        
        # Update plant if playing
        if self.game_state == PLAYING:
            self.elapsed_time += dt
            if self.elapsed_time >= 1:  # Update every second
                self.elapsed_time = 0
                self.plant.update(dt)
    
    def render(self):
        """Render the current game state"""
        if self.game_state == MENU:
            self.menu.draw(self.animation_time)
        
        elif self.game_state == PLAYING:
            self.render_game()
        
        pygame.display.flip()
    
    def render_game(self):
        """Render the main game"""
        # Background
        self.ui.draw_game_background()
        
        # Plant
        self.ui.draw_plant(self.plant, self.animation_time, self.water_effect_time)
        
        # UI elements
        self.ui.draw_stats_panel(self.plant)
        self.ui.draw_instructions()
        self.ui.draw_growth_indicator(self.plant)
    
    def quit_game(self):
        """Clean shutdown"""
        if self.game_state == PLAYING:
            save_game_state(self.plant.get_state())
        pygame.quit()
        sys.exit()
    
    def run(self):
        """Main game loop"""
        while True:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.render()