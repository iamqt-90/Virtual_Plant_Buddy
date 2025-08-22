"""
Plant Logic and Growth Mechanics
Handles all plant-related functionality
"""

import math
from .settings import *
from .utils import ease_out_quad, clamp


class Plant:
    def __init__(self, plant_images):
        self.images = plant_images
        self.state = {
            "age": 0,
            "water": 100,
            "growth_progress": 0.0,
            "last_watered": 0,
            "happiness": 50
        }
    
    def load_state(self, state_data):
        """Load plant state from save data"""
        self.state.update(state_data)
    
    def get_state(self):
        """Get current plant state for saving"""
        return self.state.copy()
    
    def get_current_stage_info(self):
        """Get current growth stage and transition progress"""
        age = self.state["age"]
        current_stage = GROWTH_STAGES[0]
        next_stage = None
        transition_progress = 0.0
        
        for i, stage in enumerate(GROWTH_STAGES):
            if age >= stage["start_age"]:
                current_stage = stage
                if i + 1 < len(GROWTH_STAGES):
                    next_stage = GROWTH_STAGES[i + 1]
                    # Start transition 3 seconds early
                    if age >= next_stage["start_age"] - 3:
                        transition_start = next_stage["start_age"] - 3
                        transition_progress = min(1.0, (age - transition_start) / 3.0)
        
        return current_stage, next_stage, transition_progress
    
    def calculate_scale(self, base_scale, animation_time, water_effect_time):
        """Calculate plant scale with animations"""
        current_stage, next_stage, transition_progress = self.get_current_stage_info()
        age = self.state["age"]
        
        # Base growth within stage
        stage_duration = current_stage["full_size_age"] - current_stage["start_age"]
        stage_progress = clamp((age - current_stage["start_age"]) / stage_duration, 0, 1)
        stage_progress = ease_out_quad(stage_progress)
        
        # Calculate scale
        min_scale = base_scale * 0.3
        max_scale = base_scale * current_stage["base_scale"]
        current_scale = min_scale + (max_scale - min_scale) * stage_progress
        
        # Add breathing effect
        breathing = 1 + 0.05 * math.sin(animation_time * BREATHING_SPEED)
        
        # Add water effect
        water_boost = 1.0
        if water_effect_time > 0:
            water_boost = 1 + 0.2 * (water_effect_time / WATER_EFFECT_DURATION)
        
        return current_scale * breathing * water_boost
    
    def water(self):
        """Water the plant"""
        old_water = self.state["water"]
        self.state["water"] = min(self.state["water"] + WATER_GAIN_PER_ACTION, 100)
        self.state["happiness"] = min(self.state["happiness"] + HAPPINESS_GAIN_PER_WATER, 100)
        self.state["last_watered"] = self.state["age"]
        
        return self.state["water"] > old_water  # Return True if water actually increased
    
    def update(self, dt):
        """Update plant state"""
        # Age the plant
        self.state["age"] += 1
        
        # Water consumption
        water_loss = WATER_LOSS_NORMAL
        if self.state["happiness"] < HAPPINESS_THRESHOLD_STRESSED:
            water_loss = WATER_LOSS_STRESSED
        
        self.state["water"] = max(0, self.state["water"] - water_loss)
        
        # Update happiness based on care
        if self.state["age"] - self.state["last_watered"] > NEGLECT_TIME_THRESHOLD:
            self.state["happiness"] = max(0, self.state["happiness"] - 1)
        
        # Boost growth if well cared for
        if (self.state["water"] > 50 and 
            self.state["happiness"] > HAPPINESS_THRESHOLD_HAPPY):
            self.state["growth_progress"] += 0.1
    
    def reset(self):
        """Reset plant to initial state"""
        self.state = {
            "age": 0,
            "water": 100,
            "growth_progress": 0.0,
            "last_watered": 0,
            "happiness": 50
        }
    
    def get_water_color(self):
        """Get water bar color based on water level"""
        if self.state["water"] > 60:
            return COLORS['water_high']
        elif self.state["water"] > 30:
            return COLORS['water_medium']
        else:
            return COLORS['water_low']
    
    def is_growing(self):
        """Check if plant is currently in a growth transition"""
        _, next_stage, transition_progress = self.get_current_stage_info()
        return next_stage is not None and transition_progress > 0
    
    def should_show_sparkles(self):
        """Check if growth sparkles should be shown"""
        return self.state["water"] > 70 and self.is_growing()