import cv2
import pygame


def morph_image(target: str, resolution=(1200,800)) -> pygame.Surface:
    image = pygame.image.load(target).convert_alpha()
    image = pygame.transform.scale(image, resolution)
    return image

def blur_screen(screen) -> pygame.Surface:
    result = cv2.blur(pygame.surfarray.array3d(screen.copy()).swapaxes(0, 1), (10, 10))
    return pygame.image.frombuffer(result.tobytes(), result.shape[1::-1], "RGB")


def za_warudo(screen) -> pygame.Surface:
    result = cv2.blur(pygame.surfarray.array3d(screen.copy()).swapaxes(0, 1), (10, 10))
    return pygame.image.frombuffer(result.tobytes(), result.shape[1::-1], "BGR")


def add_element(screen, element, pos) -> pygame.Surface:
    res = screen.copy()
    res.blit(element, pos)
    return res
