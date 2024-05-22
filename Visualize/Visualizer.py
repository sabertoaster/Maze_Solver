from copy import deepcopy
from typing import Tuple, List
import pygame
import cv2
from Visualize.LoginScreen import LoginScreen as login
from Visualize.MenuScreen import MenuScreen as menu
from Visualize.PlayScreen import PlayScreen as play
from Visualize.LeaderboardScreen import LeaderboardScreen as leaderboard
from Gameplay import Gameplay
from Sounds import SoundsHandler
from CONSTANTS import RESOLUTION, RESOURCE_PATH, CURRENT_PLAY_MODE


class Visualizer:
    def __init__(self, screen, player, sounds_handler):
        """
        A Structure to visualize the game
        :param screen:
        :param player:
        A Visualizer consists of following variables:
        - Resources path
        - Resolution
        - Screen (to draw on, the fuck you think?)
        - Player (to move, duh)
        - Scene Sets (for indexing)
        """
        self.screen = screen
        self.player = player
        self.logo = pygame.image.load(RESOURCE_PATH + "logo.png")  # Load logo image

        self.panel_collection = {  # Pop-up panel, with buttons to choose, information presentation, sths like that
            "Pause": None,
            "GameOver": None,
            "Generic": None
        }
        
        self.sounds_handler = sounds_handler
        
        self.reset_scene_collection()
        
    def reset_scene_collection(self):
        self.scenes_collection = {
            "Login": login(self.screen, self.sounds_handler),
            "Register": None,  # Chung với Login
            "Menu": menu(self.screen, self.sounds_handler),
            "Play": play(self.screen),  # Chọn mode
            "Leaderboard": leaderboard(self.screen),
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
        if scene_name == "Gameplay":
            gameplay_scene = Gameplay(self.screen, (0, 0), (0, 0))
            next_scene, next_grid_pos = gameplay_scene.play(player=self.player)
            del gameplay_scene
            return next_scene, next_grid_pos

        self.reset_scene_collection()
        scene = self.scenes_collection[scene_name]
        next_scene, next_grid_pos = scene.play(player=self.player)  # Chac chan co next scene, next grid_pos
        del scene
        return next_scene, next_grid_pos

    def start_gameplay(self):
        """
        Start the game
        :return:
        """
        gameplay_scene = Gameplay(self.screen, (0, 0), (0, 0))
        next_scene, next_grid_pos = gameplay_scene.play(player=self.player)
        del gameplay_scene
        return next_scene, next_grid_pos


    def apply_transition(self):

        pass

    # def matching_entity(self, entity: str) -> pygame.Surface:
    #     match entity:
    #         case "Login":
    #             return login(RESOURCE_PATH)
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
