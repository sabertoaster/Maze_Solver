import json
import pygame
import pygame.locals as pl
from pygame_textinput import TextInputVisualizer, TextInputManager
import numpy as np
import cv2
from Visualize.ImageProcess import blur_screen
from Visualize.ImageProcess import morph_image
from Visualize.ImageProcess import add_element
from Visualize.TextBox import TextBox, FormManager, Color
from Visualize.MouseEvents import MouseEvents
from Visualize.Transition import Transition
from Visualize.HangingSign import HangingSign

from CONSTANTS import RESOLUTION, SCENES, RESOURCE_PATH, COLORS

SCENE_NAME = "Login"

# def drawGrid(screen):
#     """
#     FOR FUCKING DEBUG THE GRID MAP
#     :param screen:
#     :return:
#     """
#     blockSize = SCENES[SCENE_NAME]["cell[]SCENE_NAME][0]  # Set the size of the grid block
#     for x in range(0, RESOLUTION[0], blockSize):
#         for y in range(0, RESOLUTION[1], blockSize):
#             rect = pygame.Rect(x, y, blockSize, blockSize)
#             pygame.draw.rect(screen, COLORS['WHITE'], rect, 1)

class LoginScreen:
    """
    This is a class to manage Login Screen Instance, (Pokémon theme)
    """

    def __init__(self, screen):
        """
        :param screen:
        :param res_cel:
        :param path_resources:
        """

        self.frame = morph_image(RESOURCE_PATH + SCENES[SCENE_NAME]["BG"], RESOLUTION)
        self.screen = screen
        

        self.text_box = FormManager(self.screen, {
            "username": {"position": (483, 426, 568, 24), "color": Color.WHITE.value, "maximum_length": 16,
                         "focusable": True, "init_text": ""},  # (x, y, width, height)
            "password": {"position": (483, 474, 568, 24), "color": Color.WHITE.value, "maximum_length": 32,
                         "focusable": True, "init_text": ""}})  # (x, y, width, height)

        # Tạo textbox hiển thị notification cho login/ register screen
        self.notify_text_box = FormManager(self.screen, {
            "notification": {"position": (483, 530, 568, 48), "color": Color.RED.value, "maximum_length": 50,
                             "focusable": False, "init_text": "Test"}
        })

        # Transition effect
        self.transition = Transition(self.screen, RESOLUTION)

        self.sign = HangingSign(SCENE_NAME.upper(), 50)

    def play(self, player):
        """
        Play the scene
        :param player:
        :return:
        """
        self.screen.blit(self.frame, (0, 0))
        pygame.display.flip()

        self.player = player
        self.screenCopy = self.screen.copy()
        self.player.update(self.screenCopy)
        # Add login panel background
        self.blur = blur_screen(screen=self.screen.copy())

        self.panel_fl = False  # CÁI NI Bị DOWN

        panel_shape = RESOLUTION[0] * 0.95, RESOLUTION[1] * 0.5
        login_panel = morph_image(RESOURCE_PATH + "login_box.png", panel_shape)
        register_panel = morph_image(RESOURCE_PATH + "register_box.png", panel_shape)

        self.login_panel = add_element(self.blur, login_panel,
                                        ((RESOLUTION[0] - panel_shape[0]) / 2,
                                        (RESOLUTION[1] - panel_shape[1]) / 2))

        self.register_panel = add_element(self.blur, register_panel,
                                          ((RESOLUTION[0] - panel_shape[0]) / 2,
                                           (RESOLUTION[1] - panel_shape[1] + 11) / 2))  # HANDLE KIEU SUC VAT
        # self.create_font()  # Create font for text input

        # Start transition effect 9 60 9 190
        self.transition.transition(pos=(self.player.visual_pos[0] + SCENES[SCENE_NAME]["cell"][0] / 2,
                                        self.player.visual_pos[1] + SCENES[SCENE_NAME]["cell"][1] / 2),
                                   transition_type='circle_out')  # draw transition effect

        self.transition.transition(transition_type='sign_pop', box=self.sign)
        # pygame.display.flip()
        
        # Play BGM


        self.mouse_handler = MouseEvents(self.screen, self.player, self.frame)
        
        self.chosen_door = None
        self.chosen_obj = None
        self.hovered_door = None

        self.notify_text_box.set_text("notification", "Ten nguoi choi da duoc dang ki, vui long dang ki ten khac")

        running = True
        while running:
            events = pygame.event.get()
            self.text_box.update(events)
            for event in events:
                
                mouse_pos = pygame.mouse.get_pos()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.text_box.focus(mouse_pos)
                if event.type == pygame.QUIT:
                    # pygame.quit()
                    return None, None  # Fucking transmit signal to another scene here, this is just a prototype
                if self.chosen_door:
                    if self.panel_fl and event.type == pygame.KEYDOWN:
                        next_scene, next_grid_pos = self.toggle_panel(event, self.chosen_door)
                        if next_scene:
                            return next_scene, next_grid_pos
                    elif not self.panel_fl:
                        self.panel_fl = True
                        if self.chosen_door == "Register":
                            self.screen.blit(self.register_panel, (0, 0))
                        if self.chosen_door == "Login":
                            self.screen.blit(self.login_panel, (0, 0))
                        if self.chosen_door == "Exit":
                            return None, None
                    pygame.display.update()
                    continue

                if not self.chosen_door:

                    self.mouse_handler.set_pos(mouse_pos)

                    self.screenCopy, self.hovered_door = self.mouse_handler.get_hover_frame(self.screenCopy, self.hovered_door)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.chosen_door, self.chosen_obj = self.mouse_handler.click()
                        events.append(pygame.event.Event(pygame.USEREVENT, {}))
                        continue

                    if event.type == pygame.KEYDOWN:
                        pressed = event.key
                        player_response = self.player.handle_event(pressed)

                        if player_response == "Move":
                            pass
                        if player_response == "Interact":
                            pass  # Handle Interact Here
                        if player_response == "Door":
                            # self.panel_fl = True
                            self.chosen_door = SCENES[SCENE_NAME]['DOORS'][self.player.get_current_door()]
                        # if self.player.handle_event(pressed):  # Handle interact from player
                        #     pass
                        # if self.player.get_grid_pos() in DOOR_POS[SCENE_NAME]:
                        #     pass
                    self.player.update(
                        self.screenCopy)  # NEED TO OPTIMIZED, https://stackoverflow.com/questions/61399822/how-to-move-character-in-pygame-without-filling-background

    def toggle_panel(self, event, name):
        """
        :param event:
        :param name: to know whether if the player step into which door
        :return:
        """
        if name:

            self.player.deactivate(active=False)
            if name == "Login":
                next_scene, next_grid_pos = self.login(event)

                if next_scene:
                    self.player.deactivate(active=True)
                    return next_scene, next_grid_pos

            if name == "Exit":
                # Play outro animation here
                self.transition.transition(pos=(self.player.visual_pos[0] + SCENES[SCENE_NAME]["cell"][0] / 2,
                                                self.player.visual_pos[1] + SCENES[SCENE_NAME]["cell"][1] / 2),
                                           transition_type='circle_in')
                self.panel_fl = False
                pygame.quit()
                exit()

            if name == "Register":
                next_scene, next_grid_pos = self.register(event)

                if next_scene:
                    self.player.deactivate(active=True)
                    return next_scene, next_grid_pos

        return None, None

    def login(self, event):
        """
        Login panel
        """
        if event.type == pygame.KEYDOWN:
            self.screen.blit(self.login_panel, (0, 0))
            self.text_box.draw()
            if event.key == pygame.K_ESCAPE:
                return "Login", self.player.get_grid_pos()  # [PROTOTYPE]

            if event.key == pygame.K_RETURN:
                # Get the {"username", "password"} the player input

                tmp_dic = self.text_box.get_all_text()
                try:
                    with open('user_profile.json', 'r') as file:
                        data = json.load(file)
                except json.JSONDecodeError:
                    data = []
                for diction in data:
                    if diction["username"] == tmp_dic["username"]:
                        if diction["password"] == tmp_dic["password"]:
                            print("Login successfully")
                            # Notification
                            self.notify_text_box.set_text("notification", "Login successfully")
                            self.notify_text_box.draw()
                            pygame.display.flip()
                            pygame.time.delay(500)

                            # Transition effect
                            self.screen.blit(self.screenCopy, (0, 0))
                            pygame.display.flip()
                            self.transition.transition(pos=(self.player.visual_pos[0] + SCENES[SCENE_NAME]["cell"][0] / 2,
                                                            self.player.visual_pos[1] + SCENES[SCENE_NAME]["cell"][1] / 2),
                                                       transition_type='circle_in')
                            
                            # Player re-init
                            self.player.deactivate(active=True)
                            self.player.re_init(name=tmp_dic["username"], scene="Menu")

                            return "Menu", SCENES["Menu"]["initial_pos"]  # [PROTOTYPE]
                        else:
                            print("Password is incorrect, please try again")
                            self.notify_text_box.set_text("notification", "Password is incorrect, please try again")
                            self.notify_text_box.draw()
                            break
                else:
                    print("The player hasn't registered yet")
                    self.notify_text_box.set_text("notification", "The player hasn't registered yet")
                    self.notify_text_box.draw()

        pygame.display.update()

        return None, None

    def register(self, event):
        """
        Register panel
        :return: username and password
        """
        if event.type == pygame.KEYDOWN:
            self.screen.blit(self.register_panel, (0, 0))
            self.text_box.draw()
            # self.notify_text_box.set_text("notification", "ME MAY CUC BEO")

            # self.notify_text_box.draw()
            if event.key == pygame.K_ESCAPE:
                return "Login", self.player.get_grid_pos()

            if event.key == pygame.K_RETURN:
                # print(self.text_box.get_all_text())
                with open('user_profile.json', 'r+') as file:
                    try:
                        data = json.load(file)

                        cur_input = self.text_box.get_all_text()

                        if cur_input["password"] == "":
                            print("Vui long nhap mat khau")
                            self.notify_text_box.set_text("notification", "Vui long nhap mat khau")
                            self.notify_text_box.draw()

                            # pygame.display.flip()
                            # pygame.event.clear()
                            # pygame.time.delay(1000)
                            return None, None

                        for dic in data:
                            if dic["username"] == cur_input["username"]:
                                print("Ten nguoi choi da duoc dang ki, vui long dang ki ten khac")
                                self.notify_text_box.set_text("notification",
                                                              "Ten nguoi choi da duoc dang ki, vui long dang ki ten khac")
                                self.notify_text_box.draw()

                                return None, None

                        data.append(cur_input)
                    except json.JSONDecodeError:
                        cur_input = self.text_box.get_all_text()
                        if cur_input["password"] == "":
                            print("Vui long nhap mat khau")
                            self.notify_text_box.set_text("notification", "Vui long nhap mat khau")
                            self.notify_text_box.draw()

                            # pygame.display.flip()
                            # pygame.event.clear()
                            # pygame.time.delay(1000)
                            return None, None
                        data = [cur_input]
                    # Rewind to top of the file
                    file.seek(0)

                    json.dump(data, file, indent=4)

                    print("Dang ki thanh cong")
                    self.notify_text_box.set_text("notification", "Dang ki thanh cong")
                    self.notify_text_box.draw()
                file.close()

        pygame.display.update()

        return None, None
