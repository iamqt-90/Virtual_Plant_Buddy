#!/usr/bin/env python3
"""
Virtual Plant Buddy - Main Entry Point
A beautiful plant growth simulation game with smooth animations
"""

from game import GameManager


def main():
    """Main entry point for the game"""
    try:
        game = GameManager()
        game.run()
    except KeyboardInterrupt:
        print("\n🌱 Thanks for playing Virtual Plant Buddy!")
    except Exception as e:
        print(f"❌ Game error: {e}")
        print("Please check that all dependencies are installed:")
        print("  pip install -r requirements.txt")


if __name__ == "__main__":
    main()
