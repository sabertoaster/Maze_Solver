import cv2
import pygame

def morph_image(target: str, resolution) -> pygame.Surface:
    # result = cv2.imread(target, cv2.IMREAD_UNCHANGED) # [PROTOTYPE]
    # print(result.shape)
    # result = cv2.resize(result, resolution)
    image = pygame.image.load(target).convert_alpha()
    image = pygame.transform.scale(image, resolution)
    return image
    # return pygame.image.frombuffer(image.tobytes(), image.shape[1::-1], "RGB")
