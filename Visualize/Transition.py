import numpy as np
import pygame
from Visualize.morph_image import morph_image

class Transition:
    def __init__(self, screen, resolution):
        self.screen = screen
        self.resolution = resolution

    def descending_circle(self, pos): # pos: x, y
        def calc_distance(pos1, pos2):
            return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5

        def create_circular_mask(h, w, center=None, radius=None):
            if center is None:  # use the middle of the image
                center = (int(w / 2), int(h / 2))
            if radius is None:  # use the smallest distance between the center and image walls
                radius = min(center[0], center[1], w - center[0], h - center[1])

            Y, X = np.ogrid[:h, :w]
            dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

            mask = dist_from_center <= radius
            return mask

        start_radius = max(calc_distance(pos, (0,self.resolution[0])),
                           calc_distance(pos, (0, 0)),
                           calc_distance(pos, (self.resolution[1], 0)),
                           calc_distance(pos, (self.resolution[1], self.resolution[0])))

        screen = self.screen.copy()
        mask = pygame.Surface((self.resolution[0], self.resolution[1]))
        mask.fill((225, 225, 225))
        rate = 48
        radius = start_radius

        for _ in range(rate):
            start_radius -= 1*1*radius / rate
            filter = create_circular_mask(h=self.resolution[0], w=self.resolution[1], center=pos, radius=start_radius)
            # for x in range(self.resolution[0]//8):
            #     for y in range(self.resolution[1]//8):
            #         # Set color based on boolean value
            #         color = (255, 255, 255) if filter[x][y] else (0, 0, 0)
            #         # Set the color of the pixel
            #         pygame.draw.rect(mask, color, (x * 8, y * 8, 8, 8))
            filter = filter.reshape((self.resolution[0], self.resolution[1], 1)).repeat(3, axis=2)
            print(filter.shape)

            frame = np.where(filter, pygame.surfarray.array3d(screen), (0, 0, 0))
            self.screen.blit(pygame.surfarray.make_surface(frame), (0, 0))
            pygame.display.flip()
            pygame.time.delay(5)

    def ascending_circle(self, pos):  # pos: x, y
        def calc_distance(pos1, pos2):
            return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

        def create_circular_mask(h, w, center=None, radius=None):
            if center is None:  # use the middle of the image
                center = (int(w / 2), int(h / 2))
            if radius is None:  # use the smallest distance between the center and image walls
                radius = min(center[0], center[1], w - center[0], h - center[1])

            Y, X = np.ogrid[:h, :w]
            dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

            mask = dist_from_center <= radius
            return mask

        end_radius = max(calc_distance(pos, (0, self.resolution[0])),
                         calc_distance(pos, (0, 0)),
                         calc_distance(pos, (self.resolution[1], 0)),
                         calc_distance(pos, (self.resolution[1], self.resolution[0])))

        screen = self.screen.copy()
        mask = pygame.Surface((self.resolution[0], self.resolution[1]))
        mask.fill((225, 225, 225))
        rate = 48
        radius = 0

        for _ in range(rate):
            radius += 1 * 1 * end_radius / rate
            filter = create_circular_mask(h=self.resolution[0], w=self.resolution[1], center=pos,
                                          radius=radius)
            # for x in range(self.resolution[0]//8):
            #     for y in range(self.resolution[1]//8):
            #         # Set color based on boolean value
            #         color = (255, 255, 255) if filter[x][y] else (0, 0, 0)
            #         # Set the color of the pixel
            #         pygame.draw.rect(mask, color, (x * 8, y * 8, 8, 8))
            filter = filter.reshape((self.resolution[0], self.resolution[1], 1)).repeat(3, axis=2)
            print(filter.shape)

            frame = np.where(filter, pygame.surfarray.array3d(screen), (0, 0, 0))
            self.screen.blit(pygame.surfarray.make_surface(frame), (0, 0))
            pygame.display.flip()
            pygame.time.delay(2)











