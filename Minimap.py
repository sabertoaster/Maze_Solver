import pygame
import numpy as np
from Visualize.ImageProcess import morph_image
from CONSTANTS import RESOLUTION, RESOURCE_PATH
RESOURCE_PATH += 'img/'



class Minimap:
    def __init__(self, screen, maze, grid_size, maze_surface, maze_cell_size, display_pos, player):
        '''
        Parameters:
        - maze: Get the maze being played
        - player: Get the current instance of player 
        '''
        self.cell_size = RESOLUTION[1] // min(grid_size)
        self.row, self.col = grid_size
        # self.visual_size = (self.col * maze_cell_size, self.row * maze_cell_size)

        self.screen = screen
        self.resolution = RESOLUTION

        self.player = player
        self.attach_player()

        self.maze = maze
        self.maze_cell_size = maze_cell_size
        self.maze_surface = maze_surface
        self.display_pos = display_pos[::-1]

        # The position where the maze begin to be cut
        self.cut_start_pos = (int(self.player.visual_pos[0]) - self.cell_size * self.col // 2,
                              int(self.player.visual_pos[1]) - self.cell_size * self.row // 2)
        self.cut_area = (self.cell_size * self.col, self.cell_size * self.row)

        # snapshot
        self.snapshot = pygame.Surface(self.cut_area)

        self.trace_path = None
        self.visited = None
        self.visited_index = 0
        self.solution_flag = False

        # self.miniscreen = pygame.Surface((self.col * self.cell_size, resolution[1]))

        # For pressing M
        self.zoom_percentage = 1
        self.width = self.row * self.cell_size
        self.length = self.col * self.cell_size

        self.hint_flag = False # Phan biet auto flag va show hint flag -> draw solution?
        self.finish_finding_path = False
        
    # Attach Player to minimap
    def attach_player(self):
        self.player.grid_step = 1

        self.player.ratio = (80, 80)

        self.player.visual_step = self.cell_size * self.player.grid_step

        self.player.visual_pos = ((self.player.grid_pos[0] + self.col // 2 + 1 / 2) * self.cell_size
                                  , (self.player.grid_pos[1] + self.row // 2 + 1 / 2) * self.cell_size)

        self.player.name_box.set_position(
            (self.player.visual_pos[0] - (self.player.name_length // 2) + self.cell_size // 2,
             self.player.visual_pos[1] - 1.5 * self.cell_size))

    def update(self, screenCopy):
        # Draw the maze on minimap everytime the player move

        self.draw(screenCopy)

    def init_at_start(self, screenCopy):
        self.draw_without_player(screenCopy)

    def draw(self, screenCopy):
        '''
        Input:
        - size: Get the size of the displayed minimap
        '''


        if self.player.active:
            if self.player.visualize_direction[0] != self.player.visualize_direction[1]:
                rate = 12
                for i in range(rate):
                    self.new_background = self.draw_on_background(screenCopy, rate)

                    self.screen.blit(self.new_background, self.display_pos, (self.cut_start_pos, self.cut_area))

                    self.cut_start_pos = (self.player.visual_pos[0] - self.cell_size * self.col // 2,
                                          self.player.visual_pos[1] - self.cell_size * self.row // 2)

                    pygame.display.flip()
                self.player.visualize_direction = (self.player.visualize_direction[1], self.player.visualize_direction[1])
                
        self.new_background = self.draw_on_background(screenCopy)
        self.screen.blit(self.new_background, (0, 0), (self.cut_start_pos, self.cut_area))

        pygame.display.update()
    def get_snapshot(self):
        self.snapshot.blit(self.new_background, (0, 0), (self.cut_start_pos, self.cut_area))
        return self.snapshot

    def draw_without_player(self, screenCopy):
        '''
        Input:
        - size: Get the size of the displayed minimap
        '''

        if self.player.active:
            if self.player.visualize_direction[0] != self.player.visualize_direction[1]:
                rate = 60
                for i in range(0, rate, 4):
                    self.new_background = self.screen_without_player(screenCopy)

                    self.screen.blit(self.new_background, self.display_pos, (self.cut_start_pos, self.cut_area))

                    self.cut_start_pos = (self.player.visual_pos[0] - self.cell_size * self.col / 2,
                                          self.player.visual_pos[1] - self.cell_size * self.row / 2)

            self.new_background = self.screen_without_player(screenCopy)
            self.screen.blit(self.new_background, self.display_pos, (self.cut_start_pos, self.cut_area))

    def draw_solution(self, screen):
        def get_directions(pos1, pos2):

            dx = pos1[0] - pos2[0]
            dy = pos1[1] - pos2[1]

            if dx > 0:
                return "RIGHT"
            elif dx < 0:
                return "LEFT"
            elif dy > 0:
                return "DOWN"
            elif dy < 0:
                return "UP"
            return "UP"

        footprint = morph_image(RESOURCE_PATH + "footprint.png", (self.cell_size, self.cell_size))

        footprints = {
            "UP": pygame.transform.rotate(footprint, 270),
            "DOWN": pygame.transform.rotate(footprint, 90),
            "LEFT": pygame.transform.rotate(footprint, 180),
            "RIGHT": pygame.transform.rotate(footprint, 0)
        }

        if self.trace_path:
            for i in range(len(self.trace_path) - 1):
                direction = get_directions(self.trace_path[i], self.trace_path[i + 1])
                screen.blit(footprints[direction], (
                            self.display_pos[0] + self.cell_size * (self.col + 1) / 2 + self.cell_size * self.trace_path[i][1],
                            self.display_pos[1] + self.cell_size * (self.row + 1) / 2 + self.cell_size * self.trace_path[i][0]))
    def draw_on_background(self, screen, ratio=1):
        copy_screen = screen.copy()

        if self.solution_flag:
            if self.hint_flag:
                self.draw_solution(copy_screen)
            elif not self.visited or self.finish_finding_path:
                self.draw_solution(copy_screen)

        self.player.draw_on_minimap(copy_screen, self.cell_size, ratio)
        # Convert surface to numpy array
        return copy_screen
    def screen_without_player(self, screen):
        copy_screen = screen.copy()

        if self.solution_flag:
            self.draw_solution(copy_screen)

        return copy_screen
