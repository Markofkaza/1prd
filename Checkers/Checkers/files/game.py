import pygame
from .misc.settings import *
from .screens.Board import Board
from .screens.Menu import Menu

class Game:
    def __init__(self) -> None:
        pygame.init()

        # Spēles pamati
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.clock = pygame.time.Clock()

        # Fonti
        self.winnerFont = pygame.font.Font("files/fonts/Cinzel-Bold.ttf", 75)
        self.subtitleFont = pygame.font.Font("files/fonts/Cinzel-Bold.ttf", 35)

        # Menu
        self.menu = Menu(self.screen, self.clock)

    def run(self):
        while True:
            # palaist menu
            mode = self.menu.run()

            # palaist laukumu (pati spele)
            board = Board(self.screen, self.clock, mode, self.winnerFont, self.subtitleFont)
            board.run()
