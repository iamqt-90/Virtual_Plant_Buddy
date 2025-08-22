"""
Menu System
Handles the main menu and navigation
"""

import pygame
import math
from .settings import *


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.setup_fonts()
        self.button_rect = None
    
    def setup_fonts(self):
        """Initialize menu fonts"""
        self.fonts = {
            'title': pygame.font.SysFont("Arial", 48, bold=True),
            'subtitle': pygame.font.SysFont("Arial", 24),
            'button': pygame.font.SysFont("Arial", 28, bold=True),
            'instruction': pygame.font.SysFont("Arial", 16)
        }
    
    def draw(self, animation_time):
        """Draw the main menu"""
        self._draw_animated_background(animation_time)
        self._draw_floating_particles(animation_time)
        self._draw_title()
        self._draw_subtitle(animation_time)
        self.button_rect = self._draw_play_button()
        self._draw_instructions()
        
        return self.button_rect
    
    def _draw_animated_background(self, animation_time):
        """Draw animated gradient background"""
        height = self.screen.get_height()
        width = self.screen.get_width()
        
        for y in range(height):
            color_ratio = y / height
            wave = math.sin(animation_time * 0.5 + y * 0.01) * 20
            
            r = int(100 + (180 - 100) * color_ratio + wave)
            g = int(150 + (255 - 150) * color_ratio + wave)
            b = int(200 + (180 - 200) * color_ratio + wave)
            
            # Clamp colors
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            pygame.draw.line(self.screen, (r, g, b), (0, y), (width, y))
    
    def _draw_floating_particles(self, animation_time):
        """Draw floating particle effects"""
        particle_colors = [
            (144, 238, 144),  # Light green
            (34, 139, 34),    # Forest green
            (255, 215, 0),    # Gold
            (255, 182, 193)   # Light pink
        ]
        
        for i in range(15):
            particle_x = (SCREEN_WIDTH // 2) + 200 * math.cos(animation_time * 0.3 + i * 0.5)
            particle_y = (SCREEN_HEIGHT // 2) + 100 * math.sin(animation_time * 0.4 + i * 0.7)
            particle_size = 3 + 2 * math.sin(animation_time * 2 + i)
            
            color = particle_colors[i % len(particle_colors)]
            pygame.draw.circle(
                self.screen, color, 
                (int(particle_x), int(particle_y)), 
                int(particle_size)
            )
    
    def _draw_title(self):
        """Draw game title with shadow effect"""
        title_text = "🌱 Virtual Plant Buddy"
        
        # Shadow
        title_shadow = self.fonts['title'].render(title_text, True, (50, 50, 50))
        shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH//2 + 3, SCREEN_HEIGHT//2 - 100 + 3))
        self.screen.blit(title_shadow, shadow_rect)
        
        # Main title
        title_surface = self.fonts['title'].render(title_text, True, (34, 139, 34))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(title_surface, title_rect)
    
    def _draw_subtitle(self, animation_time):
        """Draw animated subtitle"""
        subtitle_scale = 1 + 0.1 * math.sin(animation_time * 2)
        subtitle_text = "Watch your plant grow with love and care"
        subtitle_surface = self.fonts['subtitle'].render(subtitle_text, True, (100, 100, 100))
        
        # Scale for breathing effect
        scaled_width = int(subtitle_surface.get_width() * subtitle_scale)
        scaled_height = int(subtitle_surface.get_height() * subtitle_scale)
        scaled_subtitle = pygame.transform.scale(subtitle_surface, (scaled_width, scaled_height))
        
        subtitle_rect = scaled_subtitle.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(scaled_subtitle, subtitle_rect)
    
    def _draw_play_button(self):
        """Draw interactive play button"""
        button_width, button_height = 200, 60
        button_x = SCREEN_WIDTH//2 - button_width//2
        button_y = SCREEN_HEIGHT//2 + 20
        
        # Check hover state
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        is_hovering = button_rect.collidepoint(mouse_pos)
        
        # Button appearance based on hover
        if is_hovering:
            button_color = COLORS['button_hover']
            text_color = COLORS['text_light']
            button_scale = 1.05
        else:
            button_color = COLORS['button_normal']
            text_color = COLORS['text_light']
            button_scale = 1.0
        
        # Scale button
        scaled_width = int(button_width * button_scale)
        scaled_height = int(button_height * button_scale)
        scaled_x = SCREEN_WIDTH//2 - scaled_width//2
        scaled_y = button_y + (button_height - scaled_height)//2
        
        # Button shadow
        shadow_rect = pygame.Rect(scaled_x + 3, scaled_y + 3, scaled_width, scaled_height)
        pygame.draw.rect(self.screen, (20, 20, 20), shadow_rect, border_radius=10)
        
        # Main button
        main_button_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        pygame.draw.rect(self.screen, button_color, main_button_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLORS['text_light'], main_button_rect, 3, border_radius=10)
        
        # Button text
        button_text = self.fonts['button'].render("🌱 Start Growing!", True, text_color)
        button_text_rect = button_text.get_rect(center=main_button_rect.center)
        self.screen.blit(button_text, button_text_rect)
        
        return button_rect
    
    def _draw_instructions(self):
        """Draw menu instructions"""
        instruction_text = "Click the button or press SPACE to begin your plant journey"
        instruction_surface = self.fonts['instruction'].render(instruction_text, True, (80, 80, 80))
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        self.screen.blit(instruction_surface, instruction_rect)
    
    def handle_click(self, mouse_pos):
        """Handle menu button clicks"""
        if self.button_rect and self.button_rect.collidepoint(mouse_pos):
            return True
        return False