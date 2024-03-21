def generate_tubes():
    ...


if __name__ == "__main__":
    import pygame
    from elements import Player, Tube, Weapon

    player1, player2 = Player(), Player()

    generate_tubes()

    pygame.init()

    width, height = 800, 600

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tubi Fire")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        pygame.display.flip()
