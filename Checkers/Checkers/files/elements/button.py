import pygame

class Button:
    def __init__(self, screen, pos, text, font, bgColor, textColor, align='topleft', padding=20, width=0, borderRadius=5) -> None:
        self.screen = screen
        self.x, self.y = pos
        self.string = text
        self.font = font
        self.bgColor, self.textColor = bgColor, textColor
        self.padding = padding
        self.width = width
        self.borderRadius = borderRadius

        self.textSurface = self.font.render(self.string, True, self.textColor)
        self.textRect = self.textSurface.get_rect()


        self.sizeX, self.sizeY = self.textRect.width+self.padding*2, self.textRect.height+self.padding*2

        self.alignInit(align)

        self.rect = pygame.rect.Rect(self.x, self.y, self.sizeX, self.sizeY)
    
    def alignInit(self, align):
        if align == 'center':
            self.x -= self.sizeX//2
            self.y -= self.sizeY//2
        
        elif align == 'left':
            self.y -= self.sizeY//2
        
        elif align == 'right':
            self.x -= self.sizeX
            self.y -= self.sizeY//2
        
        elif align == 'top':
            self.x -= self.sizeX//2
        
        elif align == 'bottom':
            self.x -= self.sizeX//2
            self.y -= self.sizeY
        
        elif align == 'topright':
            self.x -= self.sizeX
        
        elif align == 'bottomright':
            self.x -= self.sizeX
            self.y -= self.sizeY
        
        elif align == 'bottomleft':
            self.y -= self.sizeY
        
        else:
            print("[ ERR ]:", align, "alignment doesn't exist")

    def isPressed(self, click):
        mx, my = pygame.mouse.get_pos()
        return click and self.rect.collidepoint(mx, my)

    def drawText(self):
        x, y = self.rect.centerx-self.textRect.width//2, self.rect.centery-self.textRect.height//2
        self.screen.blit(self.textSurface, (x, y))

    def draw(self):
        pygame.draw.rect(self.screen, self.bgColor, self.rect, self.width, self.borderRadius)
        self.drawText()
        
    def update(self):
        self.draw()