import pygame

class Minimap:
    def __init__(self, screen, maze, player, resolution):
        '''
        Parameters:
        - maze: Get the maze being played
        - player: Get the current instance of player 
        '''
        self.cell_size = 5
        self.row, self.col = 20, 20

        self.screen = screen
        self.maze = maze
        self.player = player
        self.miniscreen = pygame.Surface((self.col * self.cell_size, self.row * self.cell_size))

        self.resolution = resolution
        
        self.display_pos = (0,0)

        #For pressing M
        self.zoom_percentage = 1
        self.count_m = False

    def resize_surface(self, new_size, new_display_pos, new_zoom_percentage):
        self.miniscreen = pygame.Surface((new_size[1], new_size[0]))
        self.display_pos = new_display_pos
        self.zoom_percentage = new_zoom_percentage

    def update(self):
        def draw(size):
            '''
            Input:
            - size: Get the size of the displayed minimap
            '''

            current_player_pos = self.player.pos

            tmp_row = len(self.maze)
            tmp_col = len(self.maze[0])

            x_start = current_player_pos[0] - (size[0] * self.zoom_percentage) // 2
            x_end = current_player_pos[0] + (size[0] * self.zoom_percentage) // 2
            y_start = current_player_pos[1] - (size[1] * self.zoom_percentage) // 2
            y_end = current_player_pos[1] + (size[1] * self.zoom_percentage) // 2

            for i in range(x_start, x_end):
                for j in range(y_start, y_end):
                    ceil_rect = pygame.Rect((j - y_start) * self.cell_size, (i - x_start) * self.cell_size, self.cell_size, self.cell_size)

                    if i >= tmp_col or j >= tmp_row or i < 0 or j < 0:
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

            self.screen.blit(self.screen, (0,0))
            self.screen.blit(self.miniscreen, (self.display_pos[1], self.display_pos[0]))

            pygame.display.update()

        draw((self.row, self.col))

    def zoom(self):
        if not self.count_m:
            new_size = (30 * self.cell_size, 30 * self.cell_size)

            new_display_pos = (self.resolution[0] // 2 - new_size[0] // 2, self.resolution[1] // 2 - new_size[0] // 2)
            new_zoom_percentage = 2
            self.resize_surface(new_size, new_display_pos, new_zoom_percentage)

            pygame.display.update()

            self.count_m = True
        else:
            new_size = (20 * self.cell_size, 20 * self.cell_size)

            new_display_pos = (0,0)
            new_zoom_percentage = 1
            self.resize_surface(new_size, new_display_pos, new_zoom_percentage)

            self.zoom_percentage = 1

            pygame.display.update()

            self.count_m = False