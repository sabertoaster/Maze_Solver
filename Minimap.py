import pygame

class Minimap:
    def __init__(self, screen, size, maze, player, resolution, display_pos):
        '''
        Parameters:
        - maze: Get the maze being played
        - player: Get the current instance of player 
        '''
        self.cell_size = 15
        self.row, self.col = size

        self.screen = screen
        self.maze = maze
        self.player = player
        self.miniscreen = pygame.Surface((self.col * self.cell_size, self.row * self.cell_size))

        self.resolution = resolution
        
        self.display_pos = display_pos

        #For pressing M
        self.zoom_percentage = 1
        self.width = self.row * self.cell_size
        self.length = self.col * self.cell_size

    def resize_surface(self, new_size, new_display_pos, new_zoom_percentage):
        self.length = new_size[0]
        self.miniscreen = pygame.Surface((new_size[1], new_size[0]))
        self.display_pos = new_display_pos
        self.zoom_percentage = new_zoom_percentage

    def update(self):
        #Draw the maze on minimap everytime the player move
        def draw(size):
            '''
            Input:
            - size: Get the size of the displayed minimap
            '''

            current_player_pos = self.player.grid_pos

            tmp_row = len(self.maze)
            tmp_col = len(self.maze[0])

            x_start = current_player_pos[0] - int((size[0] // 2) * self.zoom_percentage)
            x_end = current_player_pos[0] + int((size[0] // 2) * self.zoom_percentage)
            y_start = current_player_pos[1] - int((size[1] // 2) * self.zoom_percentage)
            y_end = current_player_pos[1] + int((size[1] // 2) * self.zoom_percentage)

            for i in range(x_start, x_end):
                for j in range(y_start, y_end):
                    ceil_rect = pygame.Rect((j - y_start) * self.cell_size, (i - x_start) * self.cell_size, self.cell_size, self.cell_size)

                    if i >= tmp_row or j >= tmp_col or i < 0 or j < 0:
                        pygame.draw.rect(self.miniscreen, (255, 51, 255), ceil_rect)
                    elif current_player_pos == [i,j]:
                        pygame.draw.rect(self.miniscreen, (0, 255, 255), ceil_rect)
                    elif self.maze[i][j] == ' ':
                        pygame.draw.rect(self.miniscreen, (255,255,255), ceil_rect)
                    elif self.maze[i][j] == '#':
                        pygame.draw.rect(self.miniscreen, (0,0,0), ceil_rect)
                    elif self.maze[i][j] == 'E':
                        pygame.draw.rect(self.miniscreen, (255,255,0), ceil_rect)
                    elif self.maze[i][j] == 'S':
                        pygame.draw.rect(self.miniscreen, (255,0,0), ceil_rect)

            self.screen.blit(self.miniscreen, self.display_pos[::-1])

            pygame.display.update()

        draw((self.row, self.col))