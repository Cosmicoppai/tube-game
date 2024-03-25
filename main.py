import pygame
from elements import Player, Gun, HorizontalTube, VerticalTube, config
from pygame.surface import Surface
from time import sleep


def generate_tubes():
    ...


def load_player_images() -> tuple[list[Player], dict[str, dict[str, list[Surface]]]]:
    players = []
    player_images = {}
    for character in ["player1", "player2"]:
        character_path = config.ASSETS_PATH.joinpath("Characters", character)
        idle_image = pygame.image.load(character_path.joinpath(f"{character}_idle.png"))
        jump_image = pygame.image.load(character_path.joinpath(f"{character}_jump.png"))
        run_image = pygame.image.load(character_path.joinpath(f"{character}_run.png"))

        idle_frames = [idle_image.subsurface((i * (idle_image.get_width() // 4), 0, idle_image.get_width() // 4, idle_image.get_height())) for i in range(4)]
        jump_frames = [jump_image.subsurface((i * (jump_image.get_width() // 8), 0, jump_image.get_width() // 8, jump_image.get_height())) for i in range(8)]
        run_frames = [run_image.subsurface((i * (run_image.get_width() // 4), 0, run_image.get_width() // 4, run_image.get_height())) for i in range(4)]

        player_images[character] = {"idle": idle_frames, "jump": jump_frames, "run": run_frames}
        players.append(Player(character))

    return players, player_images


def load_death_animations() -> list[Surface]:
    death_image = pygame.image.load(config.ASSETS_PATH.joinpath("Effects", "death.png"))
    death_frame = 8
    return [death_image.subsurface((i * (death_image.get_width() // death_frame), 0, death_image.get_width() // death_frame, death_image.get_height())) for i in range(death_frame)]


def play_death_animation(dead_player: Player, screen, death_frames):
    extra_space = 10
    for _ in range(2):
        for frame in death_frames:
            clear_rect = pygame.Rect(dead_player.position, (dead_player.size + extra_space, dead_player.size + extra_space))
            screen.fill(config.BACKGROUND_COLOR, clear_rect)
            screen.blit(frame, dead_player.position)
            pygame.display.update(clear_rect)
            sleep(0.1)


def update_and_render_player(player: Player, player_images, keys, screen, frame_counter, frame_delay):
    if player.id == "player1":
        moving_left = keys[pygame.K_LEFT]
        moving_right = keys[pygame.K_RIGHT]
        jump_move = keys[pygame.K_UP]
    else:
        moving_left = keys[pygame.K_a]
        moving_right = keys[pygame.K_d]
        jump_move = keys[pygame.K_w]

    is_running = moving_left or moving_right

    if moving_left:
        player.move("x", "left", 5)
    if moving_right:
        player.move("x", "right", 5)

    if jump_move:
        player.jump()

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


def check_collisions(player1: Player, player2: Player, bullets: pygame.sprite.Group):
    player_1_rect = pygame.Rect(player1.position, (player1.size, player1.size))
    player_2_rect = pygame.Rect(player2.position, (player2.size, player2.size))

    for bullet in bullets:
        if bullet.has_hit:
            continue

        if player_1_rect.colliderect(bullet.rect) and bullet.owner.id != player1.id:
            player1.health -= bullet.owner.weapon.damage
            bullet.has_hit = True

        if player_2_rect.colliderect(bullet.rect) and bullet.owner.id != player2.id:
            player2.health -= bullet.owner.weapon.damage
            bullet.has_hit = True


if __name__ == "__main__":
    pygame.init()

    background_image = pygame.image.load(config.ASSETS_PATH.joinpath("Platform", "bg1.png"))

    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption(config.GAME_NAME)

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    players, player_images = load_player_images()
    player1 = players[0]
    player2 = players[1]

    generate_tubes()

    death_frames = load_death_animations()

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

        screen.blit(background_image, (config.BG_IMAGE_SHIFT, 0))

        update_and_render_player(player1, player_images, keys, screen, frame_counter, frame_delay)
        update_and_render_player(player2, player_images, keys, screen, frame_counter, frame_delay)

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if bullets:
            check_collisions(player1, player2, bullets)

        if player1.health <= 0 or player2.health <= 0:
            _player = player1 if player1.health <= 0 else player2
            play_death_animation(_player, screen, death_frames)
            running = False

        frame_counter += 1
        if frame_counter >= frame_delay * len(player_images[player1.id]["idle"]):
            frame_counter = 0

        pygame.display.update()

    pygame.quit()
