import pygame
import sys
import json
import os
import math

# ---------------- SETTINGS ----------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Growth stage thresholds (in seconds) with smooth transition zones
GROWTH_STAGES = [
    {"name": "seed", "image": "seed.png.webp", "start_age": 0, "full_size_age": 5, "base_scale": 0.3},
    {"name": "sprout", "image": "sprout.png.webp", "start_age": 8, "full_size_age": 15, "base_scale": 0.6},
    {"name": "flower", "image": "flower.png.webp", "start_age": 18, "full_size_age": 25, "base_scale": 1.0}
]

SAVE_FILE = "data/savegame.json"

# Animation settings
GROWTH_ANIMATION_SPEED = 2.0
WATER_EFFECT_DURATION = 1.0
BREATHING_SPEED = 1.5

# Game states
MENU = "menu"
PLAYING = "playing"
game_state = MENU

# ---------------- INITIAL SETUP ----------------
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("🌱 Virtual Plant Buddy - Enhanced Growth")
clock = pygame.time.Clock()

# Load assets
ASSET_PATH = "assets/images"
plant_images = {}
for stage in GROWTH_STAGES:
    try:
        img = pygame.image.load(os.path.join(ASSET_PATH, stage["image"])).convert_alpha()
        plant_images[stage["name"]] = img
    except pygame.error:
        # Create placeholder colored rectangles if images don't exist
        placeholder = pygame.Surface((100, 100), pygame.SRCALPHA)
        if stage["name"] == "seed":
            pygame.draw.circle(placeholder, (139, 69, 19), (50, 50), 20)
        elif stage["name"] == "sprout":
            pygame.draw.rect(placeholder, (34, 139, 34), (40, 20, 20, 60))
            pygame.draw.circle(placeholder, (0, 100, 0), (50, 20), 15)
        else:  # flower
            pygame.draw.rect(placeholder, (34, 139, 34), (45, 30, 10, 50))
            for i in range(6):
                angle = i * 60
                x = 50 + 20 * math.cos(math.radians(angle))
                y = 30 + 20 * math.sin(math.radians(angle))
                pygame.draw.circle(placeholder, (255, 20, 147), (int(x), int(y)), 8)
        plant_images[stage["name"]] = placeholder

# Fonts
font_large = pygame.font.SysFont("Arial", 28, bold=True)
font_medium = pygame.font.SysFont("Arial", 20)
font_small = pygame.font.SysFont("Arial", 16)
font_title = pygame.font.SysFont("Arial", 48, bold=True)
font_subtitle = pygame.font.SysFont("Arial", 24)

# ---------------- MENU FUNCTIONS ----------------
def draw_menu():
    """Draw the main menu screen"""
    # Animated background gradient
    for y in range(SCREEN_HEIGHT):
        color_ratio = y / SCREEN_HEIGHT
        wave = math.sin(animation_time * 0.5 + y * 0.01) * 20
        r = int(100 + (180 - 100) * color_ratio + wave)
        g = int(150 + (255 - 150) * color_ratio + wave)
        b = int(200 + (180 - 200) * color_ratio + wave)
        r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    # Floating particles effect
    for i in range(15):
        particle_x = (SCREEN_WIDTH // 2) + 200 * math.cos(animation_time * 0.3 + i * 0.5)
        particle_y = (SCREEN_HEIGHT // 2) + 100 * math.sin(animation_time * 0.4 + i * 0.7)
        particle_size = 3 + 2 * math.sin(animation_time * 2 + i)
        
        # Particle colors (plant-themed)
        colors = [(144, 238, 144), (34, 139, 34), (255, 215, 0), (255, 182, 193)]
        color = colors[i % len(colors)]
        
        pygame.draw.circle(screen, color, (int(particle_x), int(particle_y)), int(particle_size))
    
    # Title with shadow effect
    title_text = "🌱 Virtual Plant Buddy"
    
    # Shadow
    title_shadow = font_title.render(title_text, True, (50, 50, 50))
    title_shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH//2 + 3, SCREEN_HEIGHT//2 - 100 + 3))
    screen.blit(title_shadow, title_shadow_rect)
    
    # Main title
    title_surface = font_title.render(title_text, True, (34, 139, 34))
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
    screen.blit(title_surface, title_rect)
    
    # Subtitle with breathing effect
    subtitle_scale = 1 + 0.1 * math.sin(animation_time * 2)
    subtitle_text = "Watch your plant grow with love and care"
    subtitle_surface = font_subtitle.render(subtitle_text, True, (100, 100, 100))
    
    # Scale subtitle for breathing effect
    scaled_subtitle = pygame.transform.scale(subtitle_surface, 
                                           (int(subtitle_surface.get_width() * subtitle_scale),
                                            int(subtitle_surface.get_height() * subtitle_scale)))
    subtitle_rect = scaled_subtitle.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
    screen.blit(scaled_subtitle, subtitle_rect)
    
    # Play button with hover effect
    button_width, button_height = 200, 60
    button_x = SCREEN_WIDTH//2 - button_width//2
    button_y = SCREEN_HEIGHT//2 + 20
    
    # Get mouse position for hover effect
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    is_hovering = button_rect.collidepoint(mouse_pos)
    
    # Button colors
    if is_hovering:
        button_color = (50, 180, 50)
        text_color = (255, 255, 255)
        button_scale = 1.05
    else:
        button_color = (34, 139, 34)
        text_color = (255, 255, 255)
        button_scale = 1.0
    
    # Draw button with scale effect
    scaled_width = int(button_width * button_scale)
    scaled_height = int(button_height * button_scale)
    scaled_x = SCREEN_WIDTH//2 - scaled_width//2
    scaled_y = button_y + (button_height - scaled_height)//2
    
    # Button shadow
    shadow_rect = pygame.Rect(scaled_x + 3, scaled_y + 3, scaled_width, scaled_height)
    pygame.draw.rect(screen, (20, 20, 20), shadow_rect, border_radius=10)
    
    # Main button
    main_button_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
    pygame.draw.rect(screen, button_color, main_button_rect, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), main_button_rect, 3, border_radius=10)
    
    # Button text
    button_text = font_large.render("🌱 Start Growing!", True, text_color)
    button_text_rect = button_text.get_rect(center=main_button_rect.center)
    screen.blit(button_text, button_text_rect)
    
    # Instructions at bottom
    instruction_text = "Click the button or press SPACE to begin your plant journey"
    instruction_surface = font_small.render(instruction_text, True, (80, 80, 80))
    instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
    screen.blit(instruction_surface, instruction_rect)
    
    return button_rect

def handle_menu_click(mouse_pos, button_rect):
    """Handle menu button clicks"""
    global game_state
    if button_rect.collidepoint(mouse_pos):
        game_state = PLAYING
        return True
    return False

# ---------------- GAME STATE ----------------
if not os.path.exists("data"):
    os.makedirs("data")

def load_game():
    # Default state with all required keys
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
            
            # Merge loaded state with defaults to ensure all keys exist
            for key, default_value in default_state.items():
                if key not in loaded_state:
                    loaded_state[key] = default_value
            
            return loaded_state
        except (json.JSONDecodeError, FileNotFoundError):
            # If save file is corrupted, return default state
            return default_state
    
    return default_state

def save_game(state):
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f)

state = load_game()

# Animation state
animation_time = 0
water_effect_time = 0
growth_animation_progress = 0

# ---------------- FUNCTIONS ----------------
def get_current_stage_info(age):
    """Get current growth stage and transition progress"""
    current_stage = GROWTH_STAGES[0]
    next_stage = None
    transition_progress = 0.0
    
    for i, stage in enumerate(GROWTH_STAGES):
        if age >= stage["start_age"]:
            current_stage = stage
            if i + 1 < len(GROWTH_STAGES):
                next_stage = GROWTH_STAGES[i + 1]
                # Calculate transition progress
                if age >= next_stage["start_age"] - 3:  # Start transition 3 seconds early
                    transition_start = next_stage["start_age"] - 3
                    transition_progress = min(1.0, (age - transition_start) / 3.0)
    
    return current_stage, next_stage, transition_progress

def calculate_plant_scale(age, base_scale, stage_info):
    """Calculate smooth scaling based on age and growth stage"""
    current_stage, next_stage, transition_progress = stage_info
    
    # Base growth within stage
    stage_progress = min(1.0, (age - current_stage["start_age"]) / 
                        (current_stage["full_size_age"] - current_stage["start_age"]))
    
    # Smooth growth curve (ease-out)
    stage_progress = 1 - (1 - stage_progress) ** 2
    
    # Calculate scale
    min_scale = base_scale * 0.3
    max_scale = base_scale * current_stage["base_scale"]
    current_scale = min_scale + (max_scale - min_scale) * stage_progress
    
    # Add breathing effect for living feel
    breathing = 1 + 0.05 * math.sin(animation_time * BREATHING_SPEED)
    
    # Add water effect
    water_boost = 1.0
    if water_effect_time > 0:
        water_boost = 1 + 0.2 * (water_effect_time / WATER_EFFECT_DURATION)
    
    return current_scale * breathing * water_boost

def draw_plant():
    """Draw plant with smooth transitions and effects"""
    age = state["age"]
    stage_info = get_current_stage_info(age)
    current_stage, next_stage, transition_progress = stage_info
    
    # Calculate position with slight sway
    sway = 5 * math.sin(animation_time * 0.8)
    plant_x = SCREEN_WIDTH // 2 + sway
    plant_y = SCREEN_HEIGHT // 2 + 50
    
    # Draw current stage
    current_img = plant_images[current_stage["name"]]
    current_scale = calculate_plant_scale(age, 1.0, stage_info)
    
    # Scale image
    scaled_size = (int(current_img.get_width() * current_scale),
                   int(current_img.get_height() * current_scale))
    scaled_img = pygame.transform.scale(current_img, scaled_size)
    
    # Apply transparency for transition
    if transition_progress > 0 and next_stage:
        alpha = int(255 * (1 - transition_progress * 0.7))
        scaled_img.set_alpha(alpha)
    
    # Draw current stage
    rect = scaled_img.get_rect(center=(plant_x, plant_y))
    screen.blit(scaled_img, rect)
    
    # Draw next stage during transition
    if transition_progress > 0.3 and next_stage:
        next_img = plant_images[next_stage["name"]]
        next_scale = calculate_plant_scale(age, transition_progress, stage_info)
        
        next_scaled_size = (int(next_img.get_width() * next_scale),
                           int(next_img.get_height() * next_scale))
        next_scaled_img = pygame.transform.scale(next_img, next_scaled_size)
        
        # Fade in next stage
        alpha = int(255 * (transition_progress - 0.3) / 0.7)
        next_scaled_img.set_alpha(alpha)
        
        next_rect = next_scaled_img.get_rect(center=(plant_x, plant_y))
        screen.blit(next_scaled_img, next_rect)
    
    # Draw growth sparkles during rapid growth
    if state["water"] > 70 and transition_progress > 0:
        draw_growth_effects(plant_x, plant_y)

def draw_growth_effects(x, y):
    """Draw sparkle effects during growth"""
    for i in range(5):
        sparkle_x = x + 40 * math.cos(animation_time * 3 + i)
        sparkle_y = y + 40 * math.sin(animation_time * 3 + i)
        
        # Sparkle color changes
        color_intensity = int(128 + 127 * math.sin(animation_time * 5 + i))
        color = (255, color_intensity, 100)
        
        pygame.draw.circle(screen, color, (int(sparkle_x), int(sparkle_y)), 3)

def draw_enhanced_stats():
    """Draw enhanced UI with progress bars and better visuals"""
    # Background panel
    panel_rect = pygame.Rect(20, 20, 300, 120)
    pygame.draw.rect(screen, (255, 255, 255, 200), panel_rect)
    pygame.draw.rect(screen, (100, 100, 100), panel_rect, 2)
    
    y_offset = 35
    
    # Water bar
    water_text = font_medium.render("💧 Water", True, (0, 100, 200))
    screen.blit(water_text, (30, y_offset))
    
    water_bar_rect = pygame.Rect(120, y_offset + 5, 150, 15)
    pygame.draw.rect(screen, (200, 200, 200), water_bar_rect)
    water_fill = pygame.Rect(120, y_offset + 5, int(150 * state["water"] / 100), 15)
    
    # Water bar color based on level
    if state["water"] > 60:
        water_color = (0, 150, 255)
    elif state["water"] > 30:
        water_color = (255, 200, 0)
    else:
        water_color = (255, 100, 100)
    
    pygame.draw.rect(screen, water_color, water_fill)
    pygame.draw.rect(screen, (100, 100, 100), water_bar_rect, 1)
    
    y_offset += 30
    
    # Age and stage info
    current_stage, _, _ = get_current_stage_info(state["age"])
    age_text = font_medium.render(f"🌱 Age: {state['age']}s ({current_stage['name'].title()})", True, (0, 150, 0))
    screen.blit(age_text, (30, y_offset))
    
    y_offset += 25
    
    # Happiness indicator
    happiness_text = font_medium.render(f"😊 Happiness: {state['happiness']}/100", True, (255, 100, 150))
    screen.blit(happiness_text, (30, y_offset))

def water_plant():
    """Enhanced watering with effects"""
    global water_effect_time
    old_water = state["water"]
    state["water"] = min(state["water"] + 25, 100)
    state["happiness"] = min(state["happiness"] + 10, 100)
    state["last_watered"] = state["age"]
    
    # Trigger water effect animation
    if state["water"] > old_water:
        water_effect_time = WATER_EFFECT_DURATION

def update_plant_health():
    """Update plant health based on care"""
    # Decrease happiness if not watered recently
    if state["age"] - state["last_watered"] > 15:
        state["happiness"] = max(0, state["happiness"] - 1)
    
    # Boost growth if well cared for
    if state["water"] > 50 and state["happiness"] > 60:
        state["growth_progress"] += 0.1

# ---------------- MAIN LOOP ----------------
elapsed_time = 0
button_rect = None

while True:
    dt = clock.tick(FPS) / 1000  # Delta time in seconds
    animation_time += dt
    
    # Update water effect timer
    if water_effect_time > 0:
        water_effect_time -= dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if game_state == PLAYING:
                save_game(state)
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == MENU and button_rect:
                handle_menu_click(event.pos, button_rect)
        
        elif event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    game_state = PLAYING
            elif game_state == PLAYING:
                if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    water_plant()
                elif event.key == pygame.K_r:  # Reset plant for testing
                    state["age"] = 0
                    state["water"] = 100
                    state["happiness"] = 50
                elif event.key == pygame.K_ESCAPE:  # Return to menu
                    save_game(state)
                    game_state = MENU

    # Handle different game states
    if game_state == MENU:
        button_rect = draw_menu()
    
    elif game_state == PLAYING:
        # Update game state every second
        elapsed_time += dt
        if elapsed_time >= 1:
            elapsed_time = 0
            state["age"] += 1
            
            # Water decreases based on plant size and happiness
            water_loss = 1
            if state["happiness"] < 30:
                water_loss = 2  # Stressed plants need more water
            
            state["water"] = max(0, state["water"] - water_loss)
            
            # Update plant health
            update_plant_health()

        # Enhanced background with gradient
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(135 + (200 - 135) * color_ratio)
            g = int(206 + (255 - 206) * color_ratio)
            b = int(235 + (200 - 235) * color_ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Draw ground
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)
        pygame.draw.rect(screen, (101, 67, 33), ground_rect)
        
        # Draw plant
        draw_plant()
        
        # Draw enhanced stats
        draw_enhanced_stats()

        # Enhanced instructions
        instruction_bg = pygame.Rect(SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT - 60, 360, 40)
        pygame.draw.rect(screen, (255, 255, 255, 180), instruction_bg)
        pygame.draw.rect(screen, (100, 100, 100), instruction_bg, 2)
        
        instructions1 = font_medium.render("W/SPACE: Water 💧  R: Reset 🔄  ESC: Menu", True, (50, 50, 50))
        screen.blit(instructions1, (SCREEN_WIDTH//2 - 170, SCREEN_HEIGHT - 50))
        
        # Growth stage indicator
        current_stage, next_stage, transition_progress = get_current_stage_info(state["age"])
        if next_stage and transition_progress > 0:
            growth_text = font_small.render(f"Growing into {next_stage['name']}... {int(transition_progress * 100)}%", 
                                          True, (0, 150, 0))
            screen.blit(growth_text, (SCREEN_WIDTH//2 - 100, 150))

    pygame.display.flip()
