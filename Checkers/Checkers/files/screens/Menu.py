import pygame, sys
from ..misc.settings import *
from ..misc.util import *
from ..elements.button import Button

class Menu:
    def __init__(self, screen, clock) -> None:
        self.screen = screen
        self.clock = clock

        self.menu = pygame.image.load('files/assets/menu.png')
        self.font = pygame.font.Font('files/fonts/Cinzel-Bold.ttf', 20)

        # Pogas, lai izvēlētos, kurš spers pirmo gājienu
        self.humanButton = Button(self.screen, (WIDTH//2, HEIGHT//2), "Human", self.font, 'white', 'black', align='center', borderRadius=20)
        self.computerButton = Button(self.screen, (WIDTH//2, HEIGHT//2+self.humanButton.sizeY+15), "Computer", self.font, 'white', 'black', align='center', borderRadius=20)

        self.computerButtonPressed = False
        self.humanButtonPressed = False
        self.click = False
    
    def events(self):
        self.click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True

    def draw(self):
        self.screen.fill(MENU_COLOR)
        self.screen.blit(self.menu, (0, 0))

    def update(self):
        self.events()

        self.draw()
        self.computerButton.update()
        self.humanButton.update()

        pygame.display.flip()
        self.clock.tick(FPS)

    def run(self):
        # Atiestatīt vērtības nākamajai spēles iterācijai
        self.__init__(self.screen, self.clock)

        while True:
            
            # Iegūstiet pogas statusu
            self.computerButtonPressed = self.computerButton.isPressed(self.click)
            self.humanButtonPressed = self.humanButton.isPressed(self.click)

            # Ja kāds no tiem tiek nospiests, tam vajadzētu
            if self.computerButtonPressed:
                return 'computer'
            elif self.humanButtonPressed:
                return 'human'
            
            else:
                self.update()
