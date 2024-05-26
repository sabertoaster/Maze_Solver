from GameController import GameController
import pygame
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    game = GameController()
    game.run()

if __name__ == "__main__":
    main()

asset_url = resource_path('Resources')
hero_asset = pygame.image.load(asset_url)