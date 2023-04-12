import pygame, sys
from ..misc.settings import *
from ..misc.util import *
from ..elements.piece import Piece
from ..elements.computer import Computer

class Board:
    def __init__(self, screen, clock, firstTurn, winnerFont, subtitleFont) -> None:
        self.screen = screen
        self.clock = clock
        self.firstTurn = firstTurn
        self.winnerFont = winnerFont
        self.subtitleFont = subtitleFont

        # Piešķir katram spēlētājam atbilstošās krāsas
        if firstTurn == 'computer':
            self.computerColor = 'black'
            self.playerColor = 'white'

        else:
            self.computerColor = 'white'
            self.playerColor = 'black'

        # Pirmo gājienu vienmēr veic melnās figūras
        self.turn = self.computerColor if firstTurn == 'computer' else self.playerColor


        # Spēle Loop Exit Bool
        self.gameOver = False


        # Sākotnējās vērtības
        self.selectedPiece = None
        self.winner = None

        # Inicialize laukums
        self.board = self.initBoard()

        # Inicialize datora speletaju
        self.computer = Computer(self.computerColor)

    def initBoard(self):
        """Šī funkcija rūpējas par visu figūru pievienošanu katrā tāfeles kvadrātā"""

        board = []

        # Loop caur katru laukuma rindu
        for row in range(sqInWidth):
            # Pievienojiet laukuma jaunu rindu
            board.append([])

            # Loop caur katru pašreizējās rindas kolonnu
            for col in range(sqInHeight):

                # Pārbaudiet, vai pašreizējā pozīcijā ir jāiekļauj gabals
                if col % 2 == ((row + 1) % 2):

                    # Ja pašreizējā rinda ir mazāka par 3, pievienojiet figūru 1. spēlētājam
                    if row < 3:
                        board[row].append(Piece(row, col, 'black'))

                    # Ja pašreizējā rinda ir lielāka par 4, pievienojiet figūru 2. spēlētājam
                    elif row > 4:
                        board[row].append(Piece(row, col, 'white'))

                    # Ja pašreizējā rinda ir no 3 līdz 4, pievienojiet tāfelei 0 (tukšs)
                    else:
                        board[row].append(0)

                # Ja pašreizējā pozīcijā nedrīkst būt gabals, pievienojiet tāfelei 0 (tukšs)
                else:
                    board[row].append(0)
        return board

    def drawValidMoves(self, selectedPiece):
        validMoves = getValidMoves(self.board, selectedPiece)

        for move in validMoves:
            rowMove, colMove = move

            x, y = calculatePos(rowMove, colMove)
            pygame.draw.circle(self.screen, 'red', (x, y), 5)

    def selectPiece(self, pieceCord):
        row, col = pieceCord
        self.selectedPiece = (row, col)

    def pieceSelectManager(self):
        """Šī funkcija pārvalda gabalu atlasi"""

        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            row, col = calculateCoord(mx, my)
            self.selectedSquare = self.board[row][col]

            if self.selectedSquare != 0:
                if self.selectedSquare.color == self.turn:
                    self.selectPiece((row, col))

    def drawPieces(self):
        """Atjaunina gabalus uz laukuma"""

        for row in range(sqInWidth):
            for col in range(sqInHeight):
                square = self.board[row][col]

                # Ja kvadrāts ir gabals, tas ir jaatjaunina
                if square != 0:
                    square.update(self.screen)

    def drawBorders(self):
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, (0, 0, WIDTH, HEIGHT), width=7)

    def drawBoard(self):
        drawSquares(self.screen)
        self.drawBorders()
        self.drawPieces()

    def moveManger(self):
        """Šī funkcija pārvalda pagriezienus un kustību veikšanu"""

        if self.turn == self.playerColor:
            if pygame.mouse.get_pressed()[0] and self.selectedPiece != None:

                # Iegūstiet preses rindu/kolu
                mx, my = pygame.mouse.get_pos()
                row, col = calculateCoord(mx, my)

                if isValidMove(self.board, (self.selectedPiece), (row, col)):
                    # Veiciet kustību
                    self.board = makeMove(self.board, self.turn, self.selectedPiece, (row, col))

                    # Atiestatīt Val
                    self.selectedPiece = None
                
                    # Turn = datora speletajs
                    self.turn = invertTurn(self.turn)

        else:
            # Atjauniniet displeju, lai parādītu izmaiņas panelī, pirms AI analizē paneli
            pygame.display.flip()

            # Iegūstiet labāko kustību un izpildiet to
            computerMove = self.computer.getMove(self.board)
            makeMove(self.board, self.turn, computerMove[0], computerMove[1])

            # Turn = Cilveka speletajs
            self.turn = invertTurn(self.turn)
        
        self.winner = checkWin(self.board)

    def winnerMessage(self):
        """
        Šī funkcija atveido un parāda uzvarētāja ziņojumu un iespēju lietotājam atgriezties
        izvēlnē, nospiežot taustiņu "M".
        """

        # Nosakiet uzvarētāju
        if self.winner == self.computerColor:
            winner = 'Computer'
        else:
            winner = 'Human'

        # Renderējiet ziņu
        winnerMessage = self.winnerFont.render(f'Winner: {winner}', True, (50, 50, 50))
        winnerRect = winnerMessage.get_rect()

        # Aprēķiniet pozīciju un displeju ekrānā
        x, y = WIDTH//2-winnerRect.width//2, HEIGHT//2-winnerRect.height//2
        self.screen.blit(winnerMessage, (x, y))

        # Atveido instrukcijas tekstu
        instruction = self.subtitleFont.render("Press M to go to the menu!", True, (50, 50, 50))
        instructionRect = instruction.get_rect()

        # Parādās ekrānā pozīcijā
        self.screen.blit(instruction, (WIDTH//2-instructionRect.width//2, y+winnerRect.height//1.5))

        # Spēles cikls beidzas, kad spēlētājs nospiež izejas taustiņu (M)
        key = pygame.key.get_pressed()
        if key[pygame.K_m]:
            self.gameOver = True

    def events(self):
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        self.events()
        self.screen.fill(BACKGROUND_COLOR)

        ######### Game Events #########

        self.pieceSelectManager() # parbauda kaulinu selekciju
        self.drawBoard() # Izmet laukumu uz ekrana

        # Ja izvēlēts gabals
        if self.selectedPiece != None:

            # Parādiet derīgās kustības uz laukuma
            self.drawValidMoves(self.selectedPiece)

        # Pārbaudiet gabalu kustības
        self.moveManger()

        # Parādiet uzvarētāja ziņojumu, ja ir uzvarētājs
        if self.winner != None:
            self.winnerMessage()

        ###############################

        pygame.display.flip() # Update displeju
        self.clock.tick(FPS) # Timing


    def run(self):
        # Atiestatīt vērtības nākamajai spēles iterācijai
        self.__init__(self.screen, self.clock, self.firstTurn, self.winnerFont, self.subtitleFont)
        
        while not self.gameOver:
            self.update()