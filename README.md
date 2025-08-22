# 🌱 Virtual Plant Buddy

A beautiful plant growth simulation game with smooth animations and enhanced graphics.

## Features

- **Smooth Growth Transitions**: Watch your plant grow organically through different stages
- **Interactive Care System**: Water your plant and watch it respond with happiness
- **Beautiful Animations**: Breathing effects, swaying motion, and growth sparkles
- **Enhanced UI**: Progress bars, gradient backgrounds, and professional design
- **Menu System**: Welcoming opening screen with animated effects
- **Save System**: Your plant's progress is automatically saved

## How to Play

1. **Start the Game**: Click "🌱 Start Growing!" or press SPACE
2. **Water Your Plant**: Press W or SPACE to give your plant water
3. **Watch It Grow**: Your plant will evolve through three stages:
   - 🌰 **Seed** (0-8 seconds)
   - 🌱 **Sprout** (8-18 seconds) 
   - 🌸 **Flower** (18+ seconds)
4. **Keep It Happy**: Well-watered plants grow faster and stay healthier

## Controls

- **W / SPACE**: Water the plant 💧
- **R**: Reset plant (for testing) 🔄
- **ESC**: Return to menu 🏠
- **Mouse**: Click menu buttons 🖱️

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Virtual-Plant-Buddy.git
   cd Virtual-Plant-Buddy
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   ```bash
   python main.py
   ```

## Requirements

- Python 3.7+
- Pygame 2.5.2+
- Pillow 10.2.0+ (for image handling)

## Project Structure

```
Virtual-Plant-Buddy/
├── main.py              # Entry point (minimal, clean)
├── requirements.txt     # Python dependencies
├── optimize_images.py   # Image optimization script
├── README.md           # This file
├── game/               # Main game package
│   ├── __init__.py     # Package initialization
│   ├── game_manager.py # Main game loop and state management
│   ├── plant.py        # Plant logic and growth mechanics
│   ├── ui.py          # UI components and rendering
│   ├── menu.py        # Menu system and navigation
│   ├── settings.py    # Game settings and constants
│   └── utils.py       # Utility functions and helpers
├── assets/
│   └── images/         # Plant stage images
│       ├── seed.png.webp
│       ├── sprout.png.webp
│       └── flower.png.webp
└── data/
    └── savegame.json   # Auto-generated save file
```

## Architecture

This project uses a clean, modular architecture:

- **`main.py`**: Minimal entry point that just starts the game
- **`game_manager.py`**: Handles the main game loop, events, and state transitions
- **`plant.py`**: Contains all plant-related logic (growth, watering, happiness)
- **`ui.py`**: Manages all visual rendering and UI components
- **`menu.py`**: Handles the main menu system and navigation
- **`settings.py`**: Centralized configuration for easy customization
- **`utils.py`**: Shared utility functions used across modules

### Benefits of This Structure

- **Maintainable**: Each file has a single, clear responsibility
- **Extensible**: Easy to add new features without touching existing code
- **Testable**: Individual components can be tested in isolation
- **Readable**: Code is organized logically and easy to understand
- **Reusable**: Components can be reused in other projects

## Customization

### Adding New Plant Stages

Edit the `GROWTH_STAGES` list in `main.py`:

```python
GROWTH_STAGES = [
    {"name": "seed", "image": "seed.png.webp", "start_age": 0, "full_size_age": 5, "base_scale": 0.3},
    {"name": "sprout", "image": "sprout.png.webp", "start_age": 8, "full_size_age": 15, "base_scale": 0.6},
    {"name": "flower", "image": "flower.png.webp", "start_age": 18, "full_size_age": 25, "base_scale": 1.0},
    # Add your new stage here!
]
```

### Optimizing Images

Run the included image optimizer:

```bash
python optimize_images.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Screenshots

*Add screenshots of your game here!*

## Future Enhancements

- 🎵 Sound effects and background music
- 🌦️ Weather system affecting growth
- 🏆 Achievement system
- 🌿 Multiple plant species
- 🎨 Seasonal themes and decorations
- 📱 Mobile version

---

Made with ❤️ and 🌱 by [Your Name]