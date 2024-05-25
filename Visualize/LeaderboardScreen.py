import pygame
import pygame.locals as pl
from pygame_textinput import TextInputVisualizer, TextInputManager
import numpy as np
import cv2
import os
import json
from Visualize.ImageProcess import blur_screen
from Visualize.ImageProcess import morph_image
from Visualize.ImageProcess import add_element
from Visualize.MouseEvents import MouseEvents
from Visualize.Transition import Transition
from Visualize.HangingSign import HangingSign

from CONSTANTS import RESOLUTION, SCENES, RESOURCE_PATH, COLORS, CircularLinkedList, FONTS
RESOURCE_PATH += 'img/'


SCENE_NAME = "Leaderboard"


def drawGrid(screen):
    """
    FOR FUCKING DEBUG THE GRID MAP
    :param screen:
    :return:
    """
    blockSize = SCENES[SCENE_NAME]["cell"][0]  # Set the size of the grid block
    for x in range(0, RESOLUTION[0], blockSize):
        for y in range(0, RESOLUTION[1], blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, COLORS.WHITE.value, rect, 1)


# [PROTOTYPE]
list_level = CircularLinkedList(["Easy", "Medium", "Hard"])
panel_buttons = ((8, 5), (8, 9))  # left right


class LeaderboardScreen:
    """
    This is a class to manage Login Screen Instance, (Pokémon theme)
    """

    def __init__(self, screen, sounds_handler):
        """
        :param screen:
        :param res_cel:
        :param path_resources:
        """
        self.panel_fl = False
        self.frame = morph_image(RESOURCE_PATH + SCENES[SCENE_NAME]["BG"], RESOLUTION)
        self.screen = screen
        
        self.sounds_handler = sounds_handler
        
        self.instructions_frame = morph_image(RESOURCE_PATH + SCENES[SCENE_NAME]['BG_instructions'], RESOLUTION)


        # Transition effect
        self.transition = Transition(self.screen, RESOLUTION, self.sounds_handler)

        self.sign = HangingSign(SCENE_NAME.upper(), 50)

        leaderboard_panel_easy, leaderboard_panel_medium, leaderboard_panel_hard = self.visualize_leaderboard(self.get_data_for_leaderboard())

        blur = blur_screen(screen=self.frame)
        self.current_level_leaderboard_panel = list_level.pop()
        self.leaderboard_panel = {
            "Easy": add_element(blur,
                                leaderboard_panel_easy,
                                ((RESOLUTION[0] - leaderboard_panel_easy.get_width()) / 2,
                                 (RESOLUTION[1] - leaderboard_panel_easy.get_height()) / 2)),
            "Medium": add_element(blur,
                                  leaderboard_panel_medium,
                                  ((RESOLUTION[0] - leaderboard_panel_medium.get_width()) / 2,
                                   (RESOLUTION[1] - leaderboard_panel_medium.get_height()) / 2)),
            "Hard": add_element(blur,
                                leaderboard_panel_hard,
                                ((RESOLUTION[0] - leaderboard_panel_hard.get_width()) / 2,
                                 (RESOLUTION[1] - leaderboard_panel_hard.get_height()) / 2)),
        }

    def play(self, player):
        """
        Play the scene
        :param player:
        :return:
        """

        # Background and stuff go here
        self.screen.blit(self.frame, (0, 0))
        pygame.display.flip()

        # Draw Player
        self.player = player
        self.player.re_init(name=self.player.name, scene=SCENE_NAME, dir=self.player.current_direction)
        self.screenCopy = self.screen.copy()
        self.player.update(self.screenCopy)
        
        self.show_instructions = [False]

        self.mouse_handler = MouseEvents(self.screen, self.player, self.frame, self.show_instructions)

        self.chosen_door = None
        self.chosen_obj = None
        self.hovered_obj = None

        running = True
        while running:
            events = pygame.event.get()
            for event in events:

                mouse_pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    # self.transition.transition(pos=(self.player.visual_pos[0] + SCENES[SCENE_NAME]["cell"][0] / 2,
                    #             self.player.visual_pos[1] + SCENES[SCENE_NAME]["cell"][1] / 2),
                    #         transition_type='circle_in')
                    return None, None

                if self.chosen_door:
                    next_scene, next_grid_pos = self.toggle_panel(self.chosen_door)
                    if next_scene:
                        return next_scene, next_grid_pos

                if self.chosen_obj:
                    self.handle_object(self.chosen_obj)
                    self.chosen_obj = None
                    continue

                self.mouse_handler.set_pos(mouse_pos)

                self.screenCopy, self.hovered_obj = self.mouse_handler.get_hover_frame(self.screenCopy,
                                                                                       self.hovered_obj,
                                                                                       self.player.touched_obj)

                if event.type == pygame.MOUSEBUTTONUP:
                    self.chosen_door, self.chosen_obj = self.mouse_handler.click()
                    events.append(pygame.event.Event(pygame.USEREVENT, {}))
                    continue

                if event.type == pygame.KEYDOWN:
                    pressed = event.key
                    
                    if pressed == pygame.K_m:
                        self.sounds_handler.switch()
                        continue
                    
                    if pressed == pl.K_SPACE:
                        if not self.show_instructions[0]:
                            self.screen.blit(self.instructions_frame, (0, 0))
                            self.screenCopy = self.screen.copy()
                            self.player.update(self.screen.copy())
                            pygame.display.flip()
                            
                            self.show_instructions[0] = True
                            continue
                        else:
                            self.screen.blit(self.frame, (0, 0))
                            self.screenCopy = self.screen.copy()
                            self.player.update(self.screen.copy())
                            pygame.display.flip()
                            
                            self.show_instructions[0] = False
                            continue
                    
                    player_response = self.player.handle_event(pressed)

                    if player_response == "Move":
                        pass
                    if player_response == "Interact":
                        self.chosen_obj = self.player.interacted_obj
                        if self.chosen_obj:
                            events.append(pygame.event.Event(pygame.USEREVENT, {}))
                            continue
                    if player_response == "Door":
                        self.chosen_door = SCENES[SCENE_NAME]['DOORS'][self.player.get_current_door()]

                    self.player.update(self.screenCopy)

    def handle_object(self, obj):
        """
        Handle the objects
        :param obj:
        :return:
        """
        if obj == "Trophy":
            self.trophy()

    def toggle_panel(self, name):
        """
        :param name: to know whether if the player step into which door
        :return:
        """

        if name:
            self.player.deactivate(active=False)
            if name == "Menu":
                self.player.deactivate(active=True)
                self.player.update(self.screen)
                self.transition.transition(transition_type='zelda_lr', next_scene=name)

                # Player re-init

                self.player.re_init(name=self.player.name, scene="Menu", dir='right')

                return name, (1, self.player.get_grid_pos()[1])

        return None, None

    def trophy(self):
        """
        Leaderboard
        :return:
        """
        self.screen.blit(self.leaderboard_panel[self.current_level_leaderboard_panel], (0, 0))
        pygame.display.update()

        running = True
        while running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()

                mouse_pos = pygame.mouse.get_pos()
                mouse_grid_pos = (mouse_pos[1] // SCENES[SCENE_NAME]['cell'][0]), (
                            mouse_pos[0] // SCENES[SCENE_NAME]['cell'][1])

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.screen.blit(self.frame, (0, 0))
                        self.player.update(self.screenCopy)
                        running = False
                        break
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.current_level_leaderboard_panel = list_level.pop()
                        self.screen.blit(self.leaderboard_panel[self.current_level_leaderboard_panel], (0, 0))
                        pygame.display.update()
                        continue
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.current_level_leaderboard_panel = list_level.back()
                        self.screen.blit(self.leaderboard_panel[self.current_level_leaderboard_panel], (0, 0))
                        pygame.display.update()
                        continue
                if event.type == pygame.MOUSEBUTTONUP:
                    if mouse_grid_pos == panel_buttons[0]:
                        self.current_level_leaderboard_panel = list_level.back()
                        self.screen.blit(self.leaderboard_panel[self.current_level_leaderboard_panel], (0, 0))
                        pygame.display.update()
                        continue
                    elif mouse_grid_pos == panel_buttons[1]:
                        self.current_level_leaderboard_panel = list_level.pop()
                        self.screen.blit(self.leaderboard_panel[self.current_level_leaderboard_panel], (0, 0))
                        pygame.display.update()
                        continue

    def get_data_for_leaderboard(self):
        """
        Get the data for the leaderboard
        :return:
        """
        leaderboard_data = {
            "Easy": {

            },
            "Medium": {

            },
            "Hard": {

            },
        }
        try:
            path = "./WinRecord/"
            for file in os.listdir(path):
                with open(path + file, "r") as fi:
                    if file.endswith(".json"):
                        data = json.load(fi)
                        for profile in data:
                            if profile["level"] == "Easy":
                                if len(leaderboard_data["Easy"]) < 5:
                                    if profile["score"] != 0:
                                        if profile["player.name"] not in leaderboard_data["Easy"]:
                                            leaderboard_data["Easy"][profile["player.name"]] = profile["score"]
                                        else:
                                            if profile["score"] < leaderboard_data["Easy"][profile["player.name"]]:
                                                leaderboard_data["Easy"][profile["player.name"]] = profile["score"]

                            if profile["level"] == "Medium":
                                if len(leaderboard_data["Medium"]) < 5:
                                    if profile["score"] != 0:
                                        if profile["player.name"] not in leaderboard_data["Medium"]:
                                            leaderboard_data["Medium"][profile["player.name"]] = profile["score"]
                                        else:
                                            if profile["score"] < leaderboard_data["Medium"][profile["player.name"]]:
                                                leaderboard_data["Medium"][profile["player.name"]] = profile["score"]

                            if profile["level"] == "Hard":
                                if len(leaderboard_data["Hard"]) < 5:
                                    if profile["score"] != 0:
                                        if profile["player.name"] not in leaderboard_data["Hard"]:
                                            leaderboard_data["Hard"][profile["player.name"]] = profile["score"]
                                        else:
                                            if profile["score"] < leaderboard_data["Hard"][profile["player.name"]]:
                                                leaderboard_data["Hard"][profile["player.name"]] = profile["score"]

            leaderboard_data["Easy"] = dict(sorted(leaderboard_data["Easy"].items(), key=lambda x: x[1]))
            leaderboard_data["Medium"] = dict(sorted(leaderboard_data["Medium"].items(), key=lambda x: x[1]))
            leaderboard_data["Hard"] = dict(sorted(leaderboard_data["Hard"].items(), key=lambda x: x[1]))

            return leaderboard_data
        except:
            return leaderboard_data

    def visualize_leaderboard(self, leaderboard_data):
        """
        Visualize the leaderboard
        :return:
        """
        leaderboard_panel_easy = pygame.image.load(RESOURCE_PATH + "leaderboard_easy.png").convert_alpha()
        leaderboard_panel_medium = pygame.image.load(RESOURCE_PATH + "leaderboard_medium.png").convert_alpha()
        leaderboard_panel_hard = pygame.image.load(RESOURCE_PATH + "leaderboard_hard.png").convert_alpha()

        name_font = pygame.font.Font(FONTS["default_bold"], 30)
        score_font = pygame.font.Font(FONTS["default"], 40)
        pos = 0
        for key, value in leaderboard_data["Easy"].items():
            name = name_font.render(str(pos + 1) + ". " + str(key), True, COLORS.LIGHT_YELLOW.value)
            score = score_font.render(str(value), True, COLORS.BLACK.value)

            leaderboard_panel_easy.blit(name, (240, 280 + pos * 60 - 10))
            leaderboard_panel_easy.blit(score, (440, 280 + pos * 60 - 20))
            pos += 1

        pos = 0
        for key, value in leaderboard_data["Medium"].items():
            name = name_font.render(str(pos + 1) + ". " + str(key), True, COLORS.LIGHT_YELLOW.value)
            score = score_font.render(str(value), True, COLORS.BLACK.value)

            leaderboard_panel_medium.blit(name, (240, 280 + pos * 60 - 10))
            leaderboard_panel_medium.blit(score, (460, 280 + pos * 60 - 20))
            pos += 1

        pos = 0
        for key, value in leaderboard_data["Hard"].items():
            name = name_font.render(str(pos + 1) + ". " + str(key), True, COLORS.LIGHT_YELLOW.value)
            score = score_font.render(str(value), True, COLORS.BLACK.value)

            leaderboard_panel_hard.blit(name, (240, 280 + pos * 60 - 10))
            leaderboard_panel_hard.blit(score, (460, 280 + pos * 60 - 20))
            pos += 1

        return leaderboard_panel_easy, leaderboard_panel_medium, leaderboard_panel_hard