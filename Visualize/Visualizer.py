from typing import Tuple, List
import pygame
import cv2
from Visualize.LoginScreen import LoginScreen as login
from Visualize.MenuScreen import MenuScreen as menu

class Visualizer:
    def __init__(self, params, screen, player):
        """
        A Structure to visualize the game
        :param params:
        :param screen:
        :param player:
        A Visualizer consists of following variables:
        - Resources path
        - Resolution
        - Screen (to draw on, the fuck you think?)
        - Player (to move, duh)
        - Scene Sets (for indexing)
        """
        self.params = params.copy() # Assign dict to do convention sussy thing
        self.pth_re = params["resources"]  # Assign resources path to look for images, audio, font, stuffs, etc
        self.resolution = params["resolution"]
        self.cell = params["cell"]
        self.screen = screen
        self.player = player

        self.logo = pygame.image.load(self.pth_re + "logo.png")  # Load logo image
        self.scenes_collection = {
            "Login": login(self.screen, (self.resolution, self.cell), self.pth_re),
            "Register": None,   # Chung với Login
            "Menu": menu(self.screen, (self.resolution, self.cell), self.pth_re),
            "Play": None,   # Chọn mode
            "Leaderboard": None,
            "Settings": None,
        }

        self.panel_collection = { # Pop-up panel, with buttons to choose, information presentation, sths like that
            "Pause": None,
            "GameOver": None,
            "Generic": None
        }

    def start_visualize(self):
        """
        This is quite useless to be honest (for now)
        :return:
        """
        pygame.display.set_icon(self.logo)
        pygame.display.set_caption("Tâm và Gia Huy")

    def draw_scene(self, scene_name: str):
        """
        Activate the given scene name from self.scenes_collection
        Return the next scene the player chose (in-game)
        :param scene_name:
        :return:
        """
        scene = self.scenes_collection[scene_name]
        next_scene = scene.play(player=self.player)
        return next_scene

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
