import pygame
import os
from elements import Player, Gun, HorizontalTube, VerticalTube, config

def generate_tubes():
    ...

def load_player_images():
    player_images = {}
    for character in ["player1", "player2"]:
        character_path = os.path.join(os.path.dirname(__file__), "assets", "Characters", character)
        idle_image = pygame.image.load(os.path.join(character_path, f"{character}_idle.png"))
        jump_image = pygame.image.load(os.path.join(character_path, f"{character}_jump.png"))
        run_image = pygame.image.load(os.path.join(character_path, f"{character}_run.png"))

        idle_frames = [idle_image.subsurface((i * (idle_image.get_width() // 4), 0, idle_image.get_width() // 4, idle_image.get_height())) for i in range(4)]
        jump_frames = [jump_image.subsurface((i * (jump_image.get_width() // 8), 0, jump_image.get_width() // 8, jump_image.get_height())) for i in range(8)]
        run_frames = [run_image.subsurface((i * (run_image.get_width() // 4), 0, run_image.get_width() // 4, run_image.get_height())) for i in range(4)]

        player_images[character] = {"idle": idle_frames, "jump": jump_frames, "run": run_frames}
    return player_images

if __name__ == "__main__":
    player_images = load_player_images()
    player1, player2 = Player(), Player()

    generate_tubes()

    pygame.init()

    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption(config.GAME_NAME)

    clock = pygame.time.Clock()

    running = True
    moving_left = False
    moving_right = False
    is_running = False
    frame_counter = 0
    frame_delay = 10

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                moving_left = keys[pygame.K_LEFT]
                moving_right = keys[pygame.K_RIGHT]
                is_running = moving_left or moving_right
                if event.key == pygame.K_UP and event.type == pygame.KEYDOWN:
                    player1.jump()

        if moving_left:
            player1.move("x", "left", 5)
        if moving_right:
            player1.move("x", "right", 5)

        player1.update_position()
        screen.fill(config.BACKGROUND_COLOR)

        if not player1.on_ground:
            current_frames = player_images["player1"]["jump"]
        elif is_running:
            current_frames = player_images["player1"]["run"]
        else:
            current_frames = player_images["player1"]["idle"]

        if moving_left:
            current_frame = pygame.transform.flip(current_frames[frame_counter // frame_delay], True, False)
        else:
            current_frame = current_frames[frame_counter // frame_delay]

        screen.blit(current_frame, player1.position)

        frame_counter += 1
        if frame_counter >= frame_delay * len(player_images["player1"]["idle"]):
            frame_counter = 0

        pygame.display.update()
        pygame.display.flip()
pygame.quit()
