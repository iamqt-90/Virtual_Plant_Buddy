"""
UI Components and Drawing Functions
Handles all visual rendering
"""

import pygame
import math
from .settings import *
from .utils import create_gradient_background


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.setup_fonts()
    
    def setup_fonts(self):
        """Initialize all fonts"""
        self.fonts = {
            'title': pygame.font.SysFont("Arial", 48, bold=True),
            'subtitle': pygame.font.SysFont("Arial", 24),
            'large': pygame.font.SysFont("Arial", 28, bold=True),
            'medium': pygame.font.SysFont("Arial", 20),
            'small': pygame.font.SysFont("Arial", 16)
        }
    
    def draw_game_background(self):
        """Draw the game background with gradient and ground"""
        # Gradient background
        create_gradient_background(
            self.screen, 
            COLORS['background_start'], 
            COLORS['background_end']
        )
        
        # Ground
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)
        pygame.draw.rect(self.screen, COLORS['ground'], ground_rect)
    
    def draw_plant(self, plant, animation_time, water_effect_time):
        """Draw the plant with all effects"""
        current_stage, next_stage, transition_progress = plant.get_current_stage_info()
        
        # Calculate position with sway
        sway = 5 * math.sin(animation_time * 0.8)
        plant_x = SCREEN_WIDTH // 2 + sway
        plant_y = SCREEN_HEIGHT // 2 + 50
        
        # Draw current stage
        self._draw_plant_stage(
            plant, current_stage, plant_x, plant_y, 
            animation_time, water_effect_time, transition_progress
        )
        
        # Draw next stage during transition
        if transition_progress > 0.3 and next_stage:
            self._draw_plant_stage(
                plant, next_stage, plant_x, plant_y,
                animation_time, water_effect_time, transition_progress, 
                is_next_stage=True
            )
        
        # Draw growth effects
        if plant.should_show_sparkles():
            self._draw_growth_effects(plant_x, plant_y, animation_time)
    
    def _draw_plant_stage(self, plant, stage, x, y, animation_time, 
                         water_effect_time, transition_progress, is_next_stage=False):
        """Draw a single plant stage"""
        img = plant.images[stage["name"]]
        scale = plant.calculate_scale(1.0, animation_time, water_effect_time)
        
        if is_next_stage:
            scale *= transition_progress
        
        # Scale image
        scaled_size = (int(img.get_width() * scale), int(img.get_height() * scale))
        scaled_img = pygame.transform.scale(img, scaled_size)
        
        # Apply transparency
        if is_next_stage:
            alpha = int(255 * (transition_progress - 0.3) / 0.7)
        elif transition_progress > 0 and not is_next_stage:
            alpha = int(255 * (1 - transition_progress * 0.7))
        else:
            alpha = 255
        
        scaled_img.set_alpha(alpha)
        
        # Draw
        rect = scaled_img.get_rect(center=(x, y))
        self.screen.blit(scaled_img, rect)
    
    def _draw_growth_effects(self, x, y, animation_time):
        """Draw sparkle effects during growth"""
        for i in range(5):
            sparkle_x = x + 40 * math.cos(animation_time * 3 + i)
            sparkle_y = y + 40 * math.sin(animation_time * 3 + i)
            
            color_intensity = int(128 + 127 * math.sin(animation_time * 5 + i))
            color = (255, color_intensity, 100)
            
            pygame.draw.circle(self.screen, color, (int(sparkle_x), int(sparkle_y)), 3)
    
    def draw_stats_panel(self, plant):
        """Draw the stats panel with progress bars"""
        # Background panel
        panel_rect = pygame.Rect(20, 20, 300, 120)
        pygame.draw.rect(self.screen, COLORS['panel_bg'], panel_rect)
        pygame.draw.rect(self.screen, COLORS['panel_border'], panel_rect, 2)
        
        y_offset = 35
        
        # Water bar
        self._draw_stat_bar(
            "💧 Water", plant.state["water"], plant.get_water_color(),
            30, y_offset, 150
        )
        y_offset += 30
        
        # Age and stage info
        current_stage, _, _ = plant.get_current_stage_info()
        age_text = self.fonts['medium'].render(
            f"🌱 Age: {plant.state['age']}s ({current_stage['name'].title()})", 
            True, (0, 150, 0)
        )
        self.screen.blit(age_text, (30, y_offset))
        y_offset += 25
        
        # Happiness indicator
        happiness_text = self.fonts['medium'].render(
            f"😊 Happiness: {plant.state['happiness']}/100", 
            True, (255, 100, 150)
        )
        self.screen.blit(happiness_text, (30, y_offset))
    
    def _draw_stat_bar(self, label, value, color, x, y, width):
        """Draw a progress bar for stats"""
        # Label
        label_text = self.fonts['medium'].render(label, True, (0, 100, 200))
        self.screen.blit(label_text, (x, y))
        
        # Bar background
        bar_rect = pygame.Rect(x + 90, y + 5, width, 15)
        pygame.draw.rect(self.screen, (200, 200, 200), bar_rect)
        
        # Bar fill
        fill_width = int(width * value / 100)
        fill_rect = pygame.Rect(x + 90, y + 5, fill_width, 15)
        pygame.draw.rect(self.screen, color, fill_rect)
        
        # Bar border
        pygame.draw.rect(self.screen, COLORS['panel_border'], bar_rect, 1)
    
    def draw_instructions(self):
        """Draw game instructions"""
        instruction_bg = pygame.Rect(SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT - 60, 360, 40)
        pygame.draw.rect(self.screen, (255, 255, 255, 180), instruction_bg)
        pygame.draw.rect(self.screen, COLORS['panel_border'], instruction_bg, 2)
        
        instructions = self.fonts['medium'].render(
            "W/SPACE: Water 💧  R: Reset 🔄  ESC: Menu", 
            True, COLORS['text_dark']
        )
        self.screen.blit(instructions, (SCREEN_WIDTH//2 - 170, SCREEN_HEIGHT - 50))
    
    def draw_growth_indicator(self, plant):
        """Draw growth stage transition indicator"""
        current_stage, next_stage, transition_progress = plant.get_current_stage_info()
        
        if next_stage and transition_progress > 0:
            growth_text = self.fonts['small'].render(
                f"Growing into {next_stage['name']}... {int(transition_progress * 100)}%", 
                True, (0, 150, 0)
            )
            self.screen.blit(growth_text, (SCREEN_WIDTH//2 - 100, 150))