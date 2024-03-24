import pygame
import os
from elements import Player, Gun, HorizontalTube, VerticalTube, config
from pygame.surface import Surface


def generate_tubes():
    ...


def load_player_images() -> tuple[list[Player], dict[str, dict[str, list[Surface]]]]:
    players = []
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
        players.append(Player(character))

    return players, player_images


def update_and_render_player(player: Player, player_images, keys, screen, frame_counter, frame_delay):
    if player.id == "player1":
        moving_left = keys[pygame.K_LEFT]
        moving_right = keys[pygame.K_RIGHT]
        jump_key = pygame.K_UP
    else:
        moving_left = keys[pygame.K_a]
        moving_right = keys[pygame.K_d]
        jump_key = pygame.K_w

    is_running = moving_left or moving_right

    if moving_left:
        player.move("x", "left", 5)
    if moving_right:
        player.move("x", "right", 5)

    player.update_position()

    if not player.on_ground:
        current_frames = player_images[player.id]["jump"]
    elif is_running:
        current_frames = player_images[player.id]["run"]
    else:
        current_frames = player_images[player.id]["idle"]

    if moving_left:
        current_frame = pygame.transform.flip(current_frames[frame_counter // frame_delay], True, False)
    else:
        current_frame = current_frames[frame_counter // frame_delay]

    screen.blit(current_frame, player.position)


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption(config.GAME_NAME)

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    players, player_images = load_player_images()
    player1 = players[0]
    player2 = players[1]

    generate_tubes()

    clock = pygame.time.Clock()

    running = True
    frame_counter = 0
    frame_delay = 10

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player1.jump()
                if event.key == pygame.K_w:
                    player2.jump()
                if event.key == pygame.K_RETURN:
                    new_bullet = player1.attack()
                    bullets.add(new_bullet)
                    all_sprites.add(new_bullet)

                if event.key == pygame.K_f:
                    new_bullet = player2.attack()
                    bullets.add(new_bullet)
                    all_sprites.add(new_bullet)

        # Update all sprites
        all_sprites.update()

        keys = pygame.key.get_pressed()

        screen.fill(config.BACKGROUND_COLOR)

        update_and_render_player(player1, player_images, keys, screen, frame_counter, frame_delay)
        update_and_render_player(player2, player_images, keys, screen, frame_counter, frame_delay)

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        frame_counter += 1
        if frame_counter >= frame_delay * len(player_images[player1.id]["idle"]):
            frame_counter = 0

        pygame.display.update()

    pygame.quit()

