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
from Visualize.Mouse_Events import Mouse_Events
from Visualize.Transition import Transition

FILENAME = "miniTown_BG.png"

# [PROTOTYPE]
PARAMS = {
    "resources": "Visualize/Resources/",
    "resolution": (1200, 800),  # ratio 3:2
    "cell": (40, 40)  # 12 cells column, 8 cells row
}
# [PROTOTYPE]
WHITE = (200, 200, 200)


def drawGrid(screen):
    """
    FOR FUCKING DEBUG THE GRID MAP
    :param screen:
    :return:
    """
    blockSize = PARAMS["cell"][0]  # Set the size of the grid block
    for x in range(0, PARAMS["resolution"][0], blockSize):
        for y in range(0, PARAMS["resolution"][1], blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, WHITE, rect, 1)


# [PROTOTYPE]

class LoginScreen:
    """
    This is a class to manage Login Screen Instance, (Pokémon theme)
    """

    def __init__(self, screen, res_cel, path_resources):
        """
        :param screen:
        :param res_cel:
        :param path_resources:
        """
        self.resolution, self.cell = res_cel
        self.frame = morph_image(path_resources + FILENAME, self.resolution)
        self.pth_re = path_resources
        self.screen = screen
        self.door_pos = {
            (4, 9): "Login",
            (13, 4): "Exit",
            (22, 10): "Register"
        }

        # Tạo textbox nhập username/password
        self.text_box = FormManager(self.screen, {
            "username": {"position": (483, 426, 568, 24), "color": Color.WHITE.value, "maximum_length": 16,
                         "focusable": True, "init_text": ""},  # (x, y, width, height)
            "password": {"position": (483, 474, 568, 24), "color": Color.WHITE.value, "maximum_length": 32,
                         "focusable": True, "init_text": ""}})  # (x, y, width, height)

        # Transition effect
        self.transition = Transition(self.screen, self.resolution)

    def play(self, player):
        """
        Play the scene
        :param player:
        :return:
        """
        # Background and stuff go here
        self.screen.blit(self.frame, (0, 0))
        # pygame.display.flip()
        # drawGrid(screen=self.screen)

        self.player = player
        # print(self.player.grid_map.get_map(self.player.current_scene).get_grid()[12, 12])
        self.panel_fl = False  # CÁI NI Bị DOWN
        self.screenCopy = self.screen.copy()
        self.player.update(self.screenCopy)
        # Add login panel background
        self.blur = blur_screen(screen=self.screen.copy())

        panel_shape = self.resolution[0] * 0.95, self.resolution[1] * 0.5
        login_panel = morph_image(self.pth_re + "login_box.png", panel_shape)
        register_panel = morph_image(self.pth_re + "register_box.png", panel_shape)

        self.login_panel = add_element(self.blur, login_panel, (
        (self.resolution[0] - panel_shape[0]) / 2, (self.resolution[1] - panel_shape[1]) / 2))
        self.register_panel = add_element(self.blur, register_panel, ((self.resolution[0] - panel_shape[0]) / 2, (
                    self.resolution[1] - panel_shape[1] + 11) / 2))  # HANDLE KIEU SUC VAT
        # self.create_font()  # Create font for text input

        # Start transition effect
        self.transition.transition(pos=(self.player.visual_pos[0] + PARAMS["cell"][0] / 2,
                                        self.player.visual_pos[1] + PARAMS["cell"][1] / 2),
                                   transition_type='circle_out')  # draw transition effect

        # pygame.display.flip()

        self.mouse_handler = Mouse_Events(self.screen, self.player, self.frame, PARAMS)
        self.chosen_door = None

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
                    next_scene, next_grid_pos = self.toggle_panel(event, self.chosen_door)
                    if next_scene:
                        return next_scene, next_grid_pos
                    continue

                if not self.chosen_door:

                    self.mouse_handler.set_pos(mouse_pos)

                    self.screenCopy = self.mouse_handler.get_hover_frame()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.chosen_door = self.mouse_handler.click()
                        continue

                    if event.type == pygame.KEYDOWN:
                        pressed = event.key
                        player_response = self.player.handle_event(pressed)

                        if player_response == "Move":
                            pass
                        if player_response == "Interact":
                            pass  # Handle Interact Here
                        if player_response == "Door":
                            self.panel_fl = True
                            self.chosen_door = self.door_pos[self.player.get_current_door()]
                        # if self.player.handle_event(pressed):  # Handle interact from player
                        #     pass
                        # if self.player.get_grid_pos() in self.door_pos:
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
                self.transition.transition(pos=(self.player.visual_pos[0] + PARAMS["cell"][0] / 2,
                                                self.player.visual_pos[1] + PARAMS["cell"][1] / 2),
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
        self.screen.blit(self.login_panel, (0, 0))
        self.text_box.draw()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:

                return "Login", self.player.get_grid_pos()  # [PROTOTYPE]

            if event.key == pygame.K_RETURN:
                # Get the {"username", "password"} the player input

                tmp_dic = self.text_box.get_all_text()

                with open('user_profile.json', 'r') as file:
                    data = json.load(file)

                for diction in data:
                    if diction["username"] == tmp_dic["username"]:
                        if diction["password"] == tmp_dic["password"]:
                            print("Login successfully")
                            self.player.deactivate(active=True)

                            # Transition effect
                            self.screen.blit(self.screenCopy, (0, 0))
                            self.transition.transition(pos=(self.player.visual_pos[0] + PARAMS["cell"][0] / 2,
                                                            self.player.visual_pos[1] + PARAMS["cell"][1] / 2),
                                                       transition_type='circle_in')

                            return "Menu", self.player.params["initial_pos"]["Menu"]  # [PROTOTYPE]
                        else:
                            print("Password is incorrect, please try again")
                        break
                else:
                    print("The player hasn't registered yet")

        pygame.display.update()

        return None, None

    def register(self, event):
        """
        Register panel
        :return: username and password
        """

        self.screen.blit(self.register_panel, (0, 0))
        self.text_box.draw()
        if event.type == pygame.KEYDOWN:
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
                            return None, None

                        for dic in data:
                            if dic["username"] == cur_input["username"]:
                                print("Ten nguoi choi da duoc dang ki, vui long dang ki ten khac")
                                return None, None

                        data.append(cur_input)
                    except json.JSONDecodeError:
                        data = [self.text_box.get_all_text()]
                    # Rewind to top of the file
                    file.seek(0)

                    json.dump(data, file, indent=4)

                    print("Dang ki thanh cong")

                file.close()
        pygame.display.update()

        return None, None
