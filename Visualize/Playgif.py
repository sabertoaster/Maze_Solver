import pygame

IMG_PATH = "Visualize/Resources/animation"
FPS = 60
FRAMES = ["welcome_1.png",
          "welcome_2.png",
          "welcome_3.png",
          "welcome_4.png"]


def play_gif(screen):
    """
    Play gif
    :param screen:
    :return:
    """
    clock = pygame.time.Clock()
    frames = [pygame.image.load(IMG_PATH + "/" + frame) for frame in FRAMES]
    frame = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                return
        screen.fill((255, 255, 255))
        screen.blit(frames[frame], (0, 0))
        frame += 1
        frame %= len(frames)
        pygame.display.flip()
        clock.tick(FPS)
