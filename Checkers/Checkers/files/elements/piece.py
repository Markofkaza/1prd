import pygame
from ..misc.settings import *
from ..misc.util import calculatePos

class Piece:
    def __init__(self, row, col, color) -> None:
        self.row, self.col = row, col
        self.color = color

        self.king = False

        self.radius = sqSize*0.7//2

        if self.color == 'black':
            self.direction = 1
        else:
            self.direction = -1

    def __repr__(self) -> str:
        return self.color

    def makeKing(self):
        self.king = True
    
    def move(self, row, col):
        self.row, self.col = row, col

    def draw(self, screen):
        x, y = calculatePos(self.row, self.col)

        if self.king:
            pygame.draw.circle(screen, '#FFD700', (x, y), self.radius+2)

        pygame.draw.circle(screen, self.color, (x, y), self.radius)

    def update(self, screen):
        self.draw(screen)