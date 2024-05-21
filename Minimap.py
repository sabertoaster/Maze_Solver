import pygame
import numpy as np
from CONSTANTS import RESOLUTION

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

        #The position where the maze begin to be cut
        self.cut_start_pos = (int(self.player.visual_pos[0]) - self.cell_size * self.col // 2, int(self.player.visual_pos[1]) - self.cell_size * self.row // 2)
        self.cut_area = (self.cell_size * self.col, self.cell_size * self.row)

        self.trace_path = None
        self.solution_flag = False
        
        # self.miniscreen = pygame.Surface((self.col * self.cell_size, resolution[1]))

        #For pressing M
        self.zoom_percentage = 1
        self.width = self.row * self.cell_size
        self.length = self.col * self.cell_size

    #Attach Player to minimap
    def attach_player(self):
        self.player.grid_step = 1

        self.player.ratio = (80,80)
        
        self.player.visual_step = self.cell_size * self.player.grid_step

        self.player.visual_pos = ((self.player.grid_pos[0] + self.col // 2) * self.cell_size
                                  ,(self.player.grid_pos[1] + self.row // 2) * self.cell_size)
        
        self.player.name_box.set_position((self.player.visual_pos[0] - (self.player.name_length // 2) + self.cell_size // 2,
                                            self.player.visual_pos[1] - 1.5 * self.cell_size))
        # self.visual_step = self.player.grid_step * self.cell_size
        
    # def resize_surface(self, new_size, new_display_pos, new_zoom_percentage):
    #     self.length = new_size[0]
    #     self.miniscreen = pygame.Surface((new_size[1], new_size[0]))
    #     self.display_pos = new_display_pos
    #     self.zoom_percentage = new_zoom_percentage

    def update(self, screenCopy):
        #Draw the maze on minimap everytime the player move
        
        # self.screen.blit(screenCopy.copy(), (0,0))
        self.draw(screenCopy)
    

    def draw(self, screenCopy):
        '''
        Input:
        - size: Get the size of the displayed minimap
        '''
        # x_start = current_player_pos[0] - int((size[0] // 2) * self.zoom_percentage)
        # x_end = current_player_pos[0] + int((size[0] // 2) * self.zoom_percentage)
        # y_start = current_player_pos[1] - int((size[1] // 2) * self.zoom_percentage)
        # y_end = current_player_pos[1] + int((size[1] // 2) * self.zoom_percentage)

        # ceil_rect = pygame.Rect((j - y_start) * self.cell_size, (i - x_start) * self.cell_size, self.cell_size, self.cell_size)

        if self.player.active:
            if self.player.visualize_direction[0] != self.player.visualize_direction[1]:
                # self.cut_surface = self.cut_maze(screenCopy)

                # self.screen.blit(self.cut_surface, self.display_pos) 
                
                # pygame.display.update() 
                rate = 24
                for i in range(0, rate, 4):
                    self.new_background = self.cut_maze(screenCopy, rate // 4 + 1 - (rate % 4 == 0))

                    self.screen.blit(self.new_background, self.display_pos, (self.cut_start_pos, self.cut_area)) 

                    self.cut_start_pos = (int(self.player.visual_pos[0]) - self.cell_size * self.col // 2, int(self.player.visual_pos[1]) - self.cell_size * self.row // 2)
                    
                    pygame.display.flip()

                self.player.visualize_direction = (self.player.visualize_direction[1], self.player.visualize_direction[1])
                return

            self.new_background = self.cut_maze(screenCopy)

            self.screen.blit(self.new_background, self.display_pos, (self.cut_start_pos, self.cut_area)) 
            
            pygame.display.update() 
            
    def draw_solution(self, screen):
        if self.trace_path:
            for pos in self.trace_path:
                ceil_rect = pygame.Rect((self.col // 2 + pos[1]) * self.cell_size, (self.row // 2 + pos[0]) * self.cell_size, self.cell_size, self.cell_size)

                pygame.draw.rect(screen, (127, 0, 255), ceil_rect)
            

    def cut_maze(self, screen, ratio = 1):
        copy_screen = screen.copy()

        if self.solution_flag:
            self.draw_solution(copy_screen)

        self.player.draw_on_minimap(copy_screen, self.cell_size, ratio)
        #Convert surface to numpy array
        return copy_screen
        # maze_surface = pygame.surfarray.array3d(copy_screen)

        #Get a local area of the maze surrounding players
        # maze_surface = maze_surface[self.maze_cell_size * (self.player.grid_pos[0]) : self.maze_cell_size * (self.player.grid_pos[0] + self.row)
        #                             ,self.maze_cell_size * (self.player.grid_pos[1]) : self.maze_cell_size * (self.player.grid_pos[1] + self.col)]
        
        # maze_surface = maze_surface[int(self.player.visual_pos[0]) - self.cell_size * self.col // 2 : int(self.player.visual_pos[0]) + self.cell_size * self.col // 2
        #                             ,int(self.player.visual_pos[1]) - self.cell_size * self.row // 2 : int(self.player.visual_pos[1]) + self.cell_size * self.row // 2]

        # return pygame.surfarray.make_surface(maze_surface)