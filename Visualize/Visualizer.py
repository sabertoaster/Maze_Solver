from typing import Tuple, List
import pygame
import cv2
from Visualize.LoginScreen import LoginScreen as login


class Visualizer:
    def __init__(self, path_resources: str, resolution: Tuple[int, int]):
        self.pth_re = path_resources  # Assign resources path

        self.logo = pygame.image.load(path_resources + "logo.png")  # Load logo image
        self.resolution = resolution
        self.screen = pygame.display.set_mode(
            resolution)  # Create a surface on screen that has the size of `resolution`

        self.scenes_collection = {
            "Login": login(self.screen, resolution, self.pth_re),
            "Register": None,
            "Menu": None,
            "Play": None,
            "Pause": None,
            "Leaderboard": None,
            "Settings": None,
            "GameOver": None,
        }

    def start_visualize(self):
        pygame.init()
        pygame.display.set_icon(self.logo)
        pygame.display.set_caption("Tâm và Gia Huy")

    def draw_scene(self, scene_name: str):
        scene = self.scenes_collection[scene_name]
        scene.play()

    def apply_transition(self):
        pass

    # def matching_entity(self, entity: str) -> pygame.Surface:
    #     match entity:
    #         case "Login":
    #             return login(self.pth_re)
    #         case "Register":
    #             pass
    #         case "Menu":
    #             pass
    #         case "Play":
    #             pass
    #         case "Pause":
    #             pass
    #         case "Leaderboard":
    #             pass
    #         case "Settings":
    #             pass
    #         case "GameOver":
    #             pass
