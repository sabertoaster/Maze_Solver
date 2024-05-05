from copy import deepcopy
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
        self.reset_scene_collection()
        self.logo = pygame.image.load(self.pth_re + "logo.png")  # Load logo image


        self.panel_collection = { # Pop-up panel, with buttons to choose, information presentation, sths like that
            "Pause": None,
            "GameOver": None,
            "Generic": None
        }
    def reset_scene_collection(self):
        self.scenes_collection = {
            "Login": login(self.screen, (self.resolution, self.cell["Login"]), self.pth_re),
            "Register": None,  # Chung với Login
            "Menu": menu(self.screen, (self.resolution, self.cell["Menu"]), self.pth_re),
            "Play": None,  # Chọn mode
            "Leaderboard": None,
            "Settings": None,
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

        scene = self.scenes_collection.copy()[scene_name]

        if scene:
            try:
                next_scene, next_grid_pos = scene.play(player = self.player) # Chac chan co next scene, next grid_pos
            except TypeError:
                return None, None
            else:
                return next_scene, next_grid_pos
        
        return None, None

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
