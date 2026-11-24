import pygame
from config import largura, altura
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((largura, altura), pygame.SCALED)
    pygame.display.set_caption("Battle Space - Edição Turbinada")
    game = Game(screen)
    game.executar()

if __name__ == "__main__":
    main()
