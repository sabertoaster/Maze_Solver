import cv2
import numpy as np
import pygame
from CONSTANTS import SCENES, RESOURCE_PATH

# Support functions
def calc_distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


def create_circular_mask(h, w, center=None, radius=None, bit_size=16):
    if center is None:  # use the middle of the image
        center = (int(w / 2), int(h / 2))
    if radius is None:  # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w - center[0], h - center[1])

    Y, X = np.ogrid[:h:bit_size, :w:bit_size]
    dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

    mask = dist_from_center <= radius
    return mask


class Transition:
    def __init__(self, screen, resolution):
        self.screen = screen
        self.resolution = resolution

    def circle(self, pos, zoom_in=True):  # pos: x, y
        RADIUS = max(calc_distance(pos, (0, 0)),
                     calc_distance(pos, (0, self.resolution[0])),
                     calc_distance(pos, (self.resolution[1], 0)),
                     calc_distance(pos, (self.resolution[1], self.resolution[0])))

        tmp = pygame.surfarray.array3d(self.screen.copy())
        
        rate = 96
        size = 16
        
        radius = RADIUS if zoom_in else 0

        for _ in range(rate):
            radius += -1 * 1 * RADIUS / rate if zoom_in else 1 * 1 * RADIUS / rate

            # Create mask
            filter = create_circular_mask(h=self.resolution[0], w=self.resolution[1], center=pos, radius=radius,
                                          bit_size=size)
            filter = filter.repeat(size, 0)
            filter = filter.repeat(size, 1)
            filter = filter.reshape((self.resolution[0], self.resolution[1], 1)).repeat(3, axis=2)

            self.screen.blit(pygame.surfarray.make_surface(tmp * filter), (0, 0))
            pygame.display.flip()

    def sign_pop(self, box):
        box = box.to_surface()
        box_shape = box.get_size()
        screen_copy = self.screen.copy()
        rate = 48
        for _ in range(rate):
            self.screen.blit(screen_copy, (0, 0))
            self.screen.blit(box, (0, 0),
                             (0, box_shape[1] - (_ + 1) * box_shape[1] / rate, self.resolution[0], self.resolution[1]))
            pygame.display.update()
            pygame.time.delay(10)

        pygame.time.delay(500)

        for _ in range(rate):
            self.screen.blit(screen_copy, (0, 0))
            self.screen.blit(box, (0, 0), (0, (_ + 1) * box_shape[1] / rate, self.resolution[0], self.resolution[1]))
            pygame.display.update()
            pygame.time.delay(10)

    def zelda(self, next_scene, reversed, direction='h'):
        rate = 96
        if direction == 'h':
            zelda = pygame.Surface((self.resolution[0] * 2, self.resolution[1]), pygame.SRCALPHA)
        elif direction == 'v':
            zelda = pygame.Surface((self.resolution[0], self.resolution[1] * 2), pygame.SRCALPHA)

        next_scene_screen = pygame.image.load(RESOURCE_PATH + SCENES[next_scene]["BG"]).convert_alpha()

        if reversed:
            if direction == 'h':
                zelda.blit(next_scene_screen, (0, 0))
                zelda.blit(self.screen, (self.resolution[0], 0))
            elif direction == 'v':
                zelda.blit(next_scene_screen, (0, 0))
                zelda.blit(self.screen, (0, self.resolution[1]))

        else:
            if direction == 'h':
                zelda.blit(self.screen, (0, 0))
                zelda.blit(next_scene_screen, (self.resolution[0], 0))
            elif direction == 'v':
                zelda.blit(self.screen, (0, 0))
                zelda.blit(next_scene_screen, (0, self.resolution[1]))

        for scroll in range(rate):
            if reversed:
                if direction == 'h':
                    self.screen.blit(zelda, (0, 0), (
                        self.resolution[0] - (scroll + 1) * self.resolution[0] / rate, 0, self.resolution[0],
                        self.resolution[1]))
                elif direction == 'v':
                    self.screen.blit(zelda, (0, 0),
                                     (0, self.resolution[1] - (scroll + 1) * self.resolution[1] / rate,
                                      self.resolution[0], self.resolution[1]))


            else:
                if direction == 'h':
                    self.screen.blit(zelda, (0, 0),
                                     ((scroll + 1) * self.resolution[0] / rate, 0, self.resolution[0],
                                      self.resolution[1]))
                elif direction == 'v':
                    self.screen.blit(zelda, (0, 0), (
                        0, (scroll + 1) * self.resolution[1] / rate, self.resolution[0], self.resolution[1]))

            pygame.display.flip()
            pygame.time.delay(10)

    def transition(self, transition_type, pos=(0, 0), box=None, next_scene=None):  # pos = (x, y) not (y, x)
        """
        Transition effect:
            - circle_in: Zooming in effect
            - circle_out: Zooming out effect
            - zelda_lr: Transition effect from left to right
            - zelda_rl: Transition effect from right to left
            - zelda_ud: Transition effect from up to down
            - zelda_du: Transition effect from down to up
        """
        pos = (pos[1], pos[0])

        if transition_type == 'circle_in':
            self.circle(pos, zoom_in=True)

        elif transition_type == 'circle_out':
            self.circle(pos, zoom_in=False)

        elif transition_type == 'zelda_lr':
            self.zelda(next_scene, reversed=False)

        elif transition_type == 'zelda_rl':
            self.zelda(next_scene, reversed=True)

        elif transition_type == 'zelda_ud':
            self.zelda(next_scene, reversed=False, direction='v')

        elif transition_type == 'zelda_du':
            self.zelda(next_scene, reversed=True, direction='v')

        elif transition_type == "sign_pop":
            self.sign_pop(box)

        pygame.event.clear()
