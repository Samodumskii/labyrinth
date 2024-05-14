from game_utils import *
from labyrinth import *

pygame.init()
game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((WIDTH + 500, HEIGHT))
clock = pygame.time.Clock()
bg = pygame.image.load(BACKGROUND).convert()
pygame.time.set_timer(pygame.USEREVENT, 1000)
game = create_game()

# fonts
font_menu = pygame.font.SysFont('Impact', 30)
font = pygame.font.SysFont('Impact', 50)
text_font = pygame.font.SysFont('Impact', 50)

while True:
    surface.blit(bg, (WIDTH, 0))
    surface.blit(game_surface, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.USEREVENT:
            game.time -= 1
        if event.type == pygame.KEYDOWN:
            # save and restore game
            if event.key == pygame.K_s:
                save_game(game)
            if event.key == pygame.K_c:
                restore_game(game)
                # controls and movement
    pressed_key = pygame.key.get_pressed()
    for button, button_value in BUTTONS.items():
        if pressed_key[button_value] and not game.character.is_colliding(*game.character.directions[button],
                                                                         game.walls_collide_list):
            game.character.direction = game.character.directions[button]
            break
    if not game.character.is_colliding(*game.character.direction, game.walls_collide_list):
        game.character.move()

    # gameplay
    if collide_door(game) or is_game_over(game):
        game = create_game()
    game.character.take_key(game.key_list)
    collide_puddle(game)

    # draw labyrinth, subjects, character
    [cell.draw(game_surface) for row in game.labyrinth for cell in row]
    [key.draw(game_surface) for key in game.key_list]
    [door.draw(game_surface) for door in game.door_list]
    [puddle.draw(game_surface) for puddle in game.puddle_list]
    game.character.draw(game_surface)

    # draw stats and menu
    surface.blit(text_font.render('Time:', True, pygame.Color('cyan')), (WIDTH + 70, 30))
    surface.blit(font.render(f'{game.time}', True, pygame.Color('cyan')), (WIDTH + 70, 100))
    surface.blit(text_font.render('Keys:', True, pygame.Color('Orange')), (WIDTH + 70, 170))
    surface.blit(font.render(f'{", ".join(game.character.keys)}', True, pygame.Color('Orange')), (WIDTH + 70, 240))
    surface.blit(font_menu.render(f'Press [S] save game', True, pygame.Color('yellow')), (WIDTH + 70, 600))
    surface.blit(font_menu.render(f'Press [C] restore game', True, pygame.Color('yellow')), (WIDTH + 70, 650))

    pygame.display.flip()
    clock.tick(FPS)
