import json
import pygame
from Visualize.ImageProcess import blur_screen
from Visualize.ImageProcess import morph_image
from Visualize.ImageProcess import add_element
from Visualize.MouseEvents import MouseEvents
from Visualize.Transition import Transition
from Visualize.HangingSign import HangingSign

from CONSTANTS import RESOLUTION, SCENES, RESOURCE_PATH, COLORS, FONTS

SCENE_NAME = "Play"

#[PROTOYPE]
cards_click_range = {
    0: [(x,y) for x in range(3,6) for y in range(1,6)],
    1: [(x,y) for x in range(3,6) for y in range(8,13)],
    2: [(x,y) for x in range(7,10) for y in range(5,10)],
}
cards_top_left = [(100, 260), (640, 260), (380, 520)]


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


class PlayScreen:
    """
    This is a class to manage Login Screen Instance, (Pokémon theme)
    """

    def __init__(self, screen, sounds_hanlder):
        """
        :param screen:
        :param res_cel:
        :param path_resources:
        """
        self.panel_fl = False
        self.frame = morph_image(RESOURCE_PATH + SCENES[SCENE_NAME]["BG"], RESOLUTION)
        self.screen = screen
        
        self.sounds_handler = sounds_hanlder

        # Transition effect
        self.transition = Transition(self.screen, RESOLUTION, sounds_handler=self.sounds_handler)

        self.sign = HangingSign(SCENE_NAME.upper(), 50)

    def play(self, player):
        """
        Play the scene
        :param player:
        :return:
        """

        # Background and stuff go here
        self.screen.blit(self.frame, (0, 0))
        pygame.display.flip()

        self.player = player
        self.player.re_init(name=self.player.name, scene=SCENE_NAME, dir=self.player.current_direction)
        self.screenCopy = self.screen.copy()
        self.player.update(self.screenCopy)
        # Add login panel background

        # Load panel momentos
        load_panel = pygame.image.load(RESOURCE_PATH + "load_panel.png").convert_alpha()
        self.load_card = pygame.image.load(RESOURCE_PATH + "load_card.png").convert_alpha()
        self.load_cards = self.get_data_and_fill_in_load_panel(self.load_card, cards_top_left)
        self.card_hover_frame = pygame.image.load(RESOURCE_PATH + "load_card_hover.png").convert_alpha()
        
        self.saved_games = {
            0 : {},
            1 : {},
            2 : {},   
        }
        self.load__saved_games()
        
        # Load panel momentos

        blur = blur_screen(screen=self.screenCopy)
        self.load_panel = add_element(blur, load_panel,
                                      ((RESOLUTION[0] - load_panel.get_width()) / 2,
                                       (RESOLUTION[1] - load_panel.get_height()) / 2))

        self.mouse_handler = MouseEvents(self.screen, self.player, self.frame)

        self.chosen_obj = None
        self.chosen_door = None
        self.hovered_obj = None
        
        running = True
        while running:
            events = pygame.event.get()
            for event in events:

                mouse_pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    return None, None

                if self.chosen_door:
                    next_scene, next_grid_pos = self.toggle_panel(self.chosen_door)
                    self.chosen_door = None
                    if next_scene:
                        return next_scene, next_grid_pos

                if self.chosen_obj:
                    self.handle_object(self.chosen_obj)
                    self.chosen_obj = None  
                    continue

                self.mouse_handler.set_pos(mouse_pos)

                self.screenCopy, self.hovered_obj = self.mouse_handler.get_hover_frame(self.screenCopy,
                                                                                       self.hovered_obj)

                if event.type == pygame.MOUSEBUTTONUP:
                    self.chosen_door, self.chosen_obj = self.mouse_handler.click()
                    events.append(pygame.event.Event(pygame.USEREVENT, {}))
                    continue

                if event.type == pygame.KEYDOWN:
                    pressed = event.key
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
        Handle the object
        :param event:
        :return:
        """
        pass
        

    def toggle_panel(self, name):
        """
        :param name: to know whether if the player step into which door
        :return:
        """
        if name:

            if name == "Menu":
                self.player.update(self.screen)
                self.transition.transition(transition_type='zelda_rl', next_scene=name)

                # Player re-init
                self.player.deactivate(active=True)
                self.player.re_init(name=self.player.name, scene="Menu", dir='left')

                return name, (13, self.player.get_grid_pos()[1])

            if name == "Easy":
                self.set_current_mode("Easy")
                return "Gameplay", (0, 0)

            if name == "Medium":
                self.set_current_mode("Medium")
                return "Gameplay", (0, 0)

            if name == "Hard":
                self.set_current_mode("Hard")
                return "Gameplay", (0, 0)
            
            if name == "Load":
                x, y = self.load()
                return x, y
        return None, None

    def set_current_mode(self, level):
        """
        Set the current mode of the game into the ```current_profile.json```
        """
        current_profile = {
            "player.name": self.player.name,
            "level": level,
            "mode": "Manual",
            "score": 0,
            "time": 0,
            "player.grid_pos": [-1, -1],
            "player.visual_pos": [-1, -1],
            "maze_toString": []
        }
        with open("current_profile.json", "w") as fi:
            json.dump(current_profile, fi, indent=4)

    def load(self):
        
        self.screen.blit(self.load_panel, (0, 0))
        self.visualize_savefile_panel()
        pygame.display.update()
                
        hovered = None

        running = True
        while running:
            events = pygame.event.get()

            for event in events:

                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                mouse_pos = pygame.mouse.get_pos()
                mouse_grid_pos = (mouse_pos[1] // SCENES[SCENE_NAME]['cell'][0]), (mouse_pos[0] // SCENES[SCENE_NAME]['cell'][1])

                key = None
                for i, val in cards_click_range.items():
                    if mouse_grid_pos in val:
                        key = i
                        break

                if key is not None and self.saved_games[key] and key != hovered:
                    # self.screen.blit(self.load_panel, (0, 0))
                    self.visualize_savefile_panel()
                    self.screen.blit(self.card_hover_frame, cards_top_left[key])
                    pygame.display.flip()
                if key is None and hovered is not None:
                    # self.screen.blit(self.load_panel, (0, 0))
                    self.visualize_savefile_panel()
                    pygame.display.flip()
                hovered = key

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.screen.blit(self.frame, (0, 0))
                        self.player.update(self.screenCopy)
                        running = False
                        return None, None

                if event.type == pygame.MOUSEBUTTONUP:
                    if key is not None:
                        if self.saved_games[key]:
                            with open("current_profile.json", "w") as fi:
                                json.dump(self.saved_games[key], fi, indent=4)
                            running = False
                            return "Gameplay", (0, 0)
                    else:
                        continue


    def visualize_savefile_panel(self):
        """
        Visualize the save file panel
        :return:
        """
        for i, card in enumerate(self.load_cards):
            print(i)
            self.screen.blit(card, cards_top_left[i])
        pygame.display.flip()

    def get_data_and_fill_in_load_panel(self, template, position_lst):
        """
        Get the data from the save file and fill in the load panel
        :param template:
        """
        try:
            cards = []
            with open("./SaveFile/" + self.player.name + ".json", "r+") as fi:
                data = json.load(fi)
                print(data)
                for i in range(0, min(len(data), len(position_lst))):
                    card = template.copy()
                    cards.append(self.fill_in_data(card, data[i]))
            return cards
        except:
            return []
        
    def load__saved_games(self):
        try:
            with open("./SaveFile/" + self.player.name + ".json", "r+") as fi:
                data = json.load(fi)
                for i in range(0, min(len(data), len(cards_top_left))):
                    self.saved_games[i] = data[i]
        except:
            pass

    def fill_in_data(self, card, data):
        """
        Fill in the data into the card
        :param card:
        :param data:
        :return:
        """
        font = pygame.font.Font(FONTS["default_bold"], 20)
        text = font.render("Save No." + str(data["id"] + 1), True, (10, 10, 10))
        card.blit(text, (175, 25))
        
        font = pygame.font.Font(FONTS["default_bold"], 25)
        text = font.render(data["level"], 1, (10, 10, 10))
        card.blit(text, (75, 50))
        text = font.render(str(data["step"]), 1, (10, 10, 10))
        card.blit(text, (115, 120))
        text = font.render(str(data["time"]), 1, (10, 10, 10))
        card.blit(text, (115, 170))

        snapshot = morph_image("./SaveFile/" + self.player.name + str(data["id"]) + ".png", (165, 165))
        card.blit(snapshot, (210, 55))
        return card
