# 🛠️ Development Guide

## Project Architecture

### File Organization

```
game/
├── __init__.py         # Package exports
├── settings.py         # All configuration in one place
├── utils.py           # Shared utility functions
├── plant.py           # Plant logic (Model)
├── ui.py             # Rendering logic (View)
├── menu.py           # Menu system (View)
└── game_manager.py   # Main controller (Controller)
```

This follows a **Model-View-Controller (MVC)** pattern:
- **Model**: `plant.py` - Game data and logic
- **View**: `ui.py`, `menu.py` - Visual presentation
- **Controller**: `game_manager.py` - User input and coordination

### Key Design Principles

1. **Single Responsibility**: Each module has one clear purpose
2. **Dependency Injection**: Objects receive their dependencies
3. **Configuration Centralization**: All settings in `settings.py`
4. **Error Handling**: Graceful fallbacks for missing assets
5. **State Management**: Clean separation of game states

## Adding New Features

### 1. Adding a New Plant Stage

**Step 1**: Update `settings.py`
```python
GROWTH_STAGES = [
    # ... existing stages ...
    {
        "name": "fruit", 
        "image": "fruit.png", 
        "start_age": 30, 
        "full_size_age": 40, 
        "base_scale": 1.2
    }
]
```

**Step 2**: Add image to `assets/images/fruit.png`

**Step 3**: The system automatically handles the rest!

### 2. Adding New UI Elements

**In `ui.py`**:
```python
def draw_new_feature(self, data):
    """Draw your new UI element"""
    # Implementation here
    pass
```

**In `game_manager.py`**:
```python
def render_game(self):
    # ... existing rendering ...
    self.ui.draw_new_feature(some_data)
```

### 3. Adding New Game Mechanics

**In `plant.py`**:
```python
def new_plant_behavior(self):
    """Add new plant behavior"""
    # Implementation here
    pass
```

**In `game_manager.py`**:
```python
def update(self, dt):
    # ... existing updates ...
    if some_condition:
        self.plant.new_plant_behavior()
```

## Code Style Guidelines

### Naming Conventions
- **Classes**: `PascalCase` (e.g., `GameManager`)
- **Functions/Variables**: `snake_case` (e.g., `draw_plant`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `SCREEN_WIDTH`)
- **Private methods**: `_leading_underscore` (e.g., `_draw_button`)

### Documentation
- All public functions need docstrings
- Use type hints where helpful
- Comment complex algorithms
- Keep comments up-to-date

### Error Handling
```python
try:
    # Risky operation
    result = load_image(path)
except pygame.error:
    # Graceful fallback
    result = create_placeholder()
```

## Testing Your Changes

### Quick Test
```bash
python main.py
```

### Module Test
```bash
python -c "from game.plant import Plant; print('Plant module OK')"
python -c "from game.ui import UI; print('UI module OK')"
```

### Image Optimization Test
```bash
python optimize_images.py
```

## Performance Considerations

### Rendering Optimization
- Cache scaled images when possible
- Use `convert_alpha()` for images with transparency
- Minimize `pygame.transform.scale()` calls per frame

### Memory Management
- Don't create new surfaces every frame
- Reuse objects where possible
- Use appropriate data structures

### Frame Rate
- Target 60 FPS consistently
- Profile with `clock.get_fps()` if needed
- Optimize expensive operations (gradients, scaling)

## Debugging Tips

### Common Issues

1. **Import Errors**: Check `__init__.py` files exist
2. **Missing Images**: Check `assets/images/` folder
3. **Save File Issues**: Delete `data/savegame.json` to reset
4. **Performance**: Check for infinite loops or heavy operations

### Debug Mode
Add to `settings.py`:
```python
DEBUG = True
SHOW_FPS = True
```

### Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

## Contributing Workflow

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes following the style guide
4. **Test** thoroughly
5. **Commit** with clear messages: `git commit -m "Add amazing feature"`
6. **Push** to your fork: `git push origin feature/amazing-feature`
7. **Create** a Pull Request

## Future Architecture Ideas

### Plugin System
```python
# plugins/weather.py
class WeatherPlugin:
    def update(self, plant, weather_data):
        # Modify plant based on weather
        pass
```

### Event System
```python
# events.py
class EventManager:
    def emit(self, event_name, data):
        # Notify all listeners
        pass
```

### Save System Enhancement
```python
# save_manager.py
class SaveManager:
    def save_multiple_plants(self, plants):
        # Support multiple save slots
        pass
```

---

Happy coding! 🌱✨