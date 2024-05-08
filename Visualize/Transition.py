import cv2
import numpy as np
import pygame

# Support functions
def calc_distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

def create_circular_mask(h, w, center=None, radius=None):
    if center is None:  # use the middle of the image
        center = (int(w / 2), int(h / 2))
    if radius is None:  # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w - center[0], h - center[1])

    Y, X = np.ogrid[:h:8, :w:8]
    dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

    mask = dist_from_center <= radius
    return mask

class Transition:
    def __init__(self, screen, resolution):
        self.screen = screen
        self.resolution = resolution

    def circle(self, pos, zoom_in=True): # pos: x, y
        RADIUS = max(calc_distance(pos, (0, 0)),
                     calc_distance(pos, (0, self.resolution[0])),
                     calc_distance(pos, (self.resolution[1], 0)),
                     calc_distance(pos, (self.resolution[1], self.resolution[0])))


        tmp = pygame.surfarray.array3d(self.screen.copy())
        rate = 48
        radius = RADIUS if zoom_in else 0

        for _ in range(rate):
            radius += -1 * 1 * RADIUS / rate if zoom_in else 1 * 1 * RADIUS / rate

            # Create mask
            filter = create_circular_mask(h=self.resolution[0], w=self.resolution[1], center=pos, radius=radius)
            filter = filter.repeat(8, 0)
            filter = filter.repeat(8, 1)
            filter = filter.reshape((self.resolution[0], self.resolution[1], 1)).repeat(3, axis=2)

            self.screen.blit(pygame.surfarray.make_surface(tmp * filter), (0, 0))
            pygame.display.flip()

    def zelda(self):
        rate = 30
        im1 = cv2.hconcat("Visualize/Resources/livingRoom_BG.png", "Visualize/Resources/kitchen_BG.png")
        for _ in range(rate):
            self.screen.blit(img, (0, 0), (_*self.resolution[0]/rate, 0, 1200, 800)) #PROTOTYPE
            pygame.display.flip()
            pygame.time.delay(30)
        pass
    def transition(self, pos, transition_type): # pos = (x, y) not (y, x)
        """
        Transition effect:
            - circle_in: Zooming in effect
            - circle_out: Zooming out effect
        """
        pos = (pos[1], pos[0])
        if transition_type == 'circle_in':
            self.circle(pos, zoom_in=True)
        elif transition_type == 'circle_out':
            self.circle(pos, zoom_in=False)
        elif transition_type == 'zelda':
            self.zelda()


        pygame.event.clear()


