import pygame
from elements import Player, Gun, HorizontalTube, VerticalTube, config


def generate_tubes():
    ...


if __name__ == "__main__":

    player1, player2 = Player(), Player()

    generate_tubes()

    pygame.init()

    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    screen.fill(config.BACKGROUND_COLOR)
    pygame.display.set_caption(config.GAME_NAME)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        pygame.display.flip()
