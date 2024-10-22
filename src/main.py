import pygame, argparse
from board import Board

# Handle flags
parser = argparse.ArgumentParser(description="Mine Sweeper Game Settings")
parser.add_argument('-b', '--bombs', type=int, help="Bomb Count for the game")
parser.add_argument('-s', '--size', type=int, help="Game size in x by x")

pygame.init()
screen = pygame.display.set_mode((900, 900))

pygame.display.set_icon(pygame.image.load(r"src\media\logo.png"))
pygame.display.set_caption("Mine Sweeper: BTTR Edition")

mouse = pygame.mouse

clock = pygame.time.Clock()
clock.tick(30)

running = True

args = parser.parse_args()

if not any(vars(args).values()):
    game_size = 15 # Will be set to x by x
    bomb_count = 40 # clamped to max number og spcaes which is x * x from before
else:
      if args.bombs:
        bomb_count = args.bombs
      if args.size:
        game_size = args.size



number_photos = []
number_photos.append(pygame.image.load(r"src\media\1.png"))
number_photos.append(pygame.image.load(r"src\media\2.png"))
number_photos.append(pygame.image.load(r"src\media\3.png"))
number_photos.append(pygame.image.load(r"src\media\4.png"))
number_photos.append(pygame.image.load(r"src\media\5.png"))
number_photos.append(pygame.image.load(r"src\media\6.png"))
number_photos.append(pygame.image.load(r"src\media\7.png"))
number_photos.append(pygame.image.load(r"src\media\8.png"))


if bomb_count >= game_size**2:
    bomb_count = game_size**2 - 1

spaces = Board(screen, mouse, game_size, bomb_count, number_photos)

while running:
    if spaces.restart_game:
        spaces = Board(screen, mouse, game_size, bomb_count, number_photos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))

    spaces.draw()
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()