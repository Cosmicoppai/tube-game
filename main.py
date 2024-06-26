import pygame
from elements import Player, Gun, HorizontalTube, VerticalTube, config
from elements.config import FLOOR_HEIGHT
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


def update_and_render_player(player: Player, player_images, keys, screen, frame_counter, frame_delay, bullets, keys_prev):
    if player.id == "player1":
        moving_left = keys[pygame.K_LEFT]
        moving_right = keys[pygame.K_RIGHT]
        jump_move = keys[pygame.K_UP]
        shoot = keys[pygame.K_DOWN] and not keys_prev.get(pygame.K_DOWN, False)
    else:
        moving_left = keys[pygame.K_a]
        moving_right = keys[pygame.K_d]
        jump_move = keys[pygame.K_w]
        shoot = keys[pygame.K_s] and not keys_prev.get(pygame.K_s, False)

    is_running = moving_left or moving_right

    if moving_left:
        player.move("x", "left", 5)
    if moving_right:
        player.move("x", "right", 5)

    if jump_move:
        player.jump()

    
    player.weapon.has_hit = False

    
    if shoot:
        new_bullet = player.attack()
        bullets.add(new_bullet)
        all_sprites.add(new_bullet)

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

    # Set spawn points 
    player1.position = (100, FLOOR_HEIGHT)
    player2.position = (1000, FLOOR_HEIGHT) 

    generate_tubes()

    death_frames = load_death_animations()

    clock = pygame.time.Clock()

    running = True
    frame_counter = 0
    frame_delay = 10

    keys_prev = {}

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update all sprites
        all_sprites.update()

        keys = {pygame.K_DOWN: False, pygame.K_s: False, pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_w: False, pygame.K_a: False, pygame.K_d: False}
        keys_pressed = pygame.key.get_pressed()
        for key in keys:
            if keys_pressed[key]:
                keys[key] = True

        screen.blit(background_image, (config.BG_IMAGE_SHIFT, 0))

        update_and_render_player(player1, player_images, keys, screen, frame_counter, frame_delay, bullets, keys_prev)
        update_and_render_player(player2, player_images, keys, screen, frame_counter, frame_delay, bullets, keys_prev)

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

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

        keys_prev = keys.copy()

    pygame.quit()
