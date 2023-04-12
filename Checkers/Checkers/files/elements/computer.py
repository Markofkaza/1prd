from ..misc.util import *
import pygame, sys
from copy import deepcopy

class Computer:
    def __init__(self, computerColor) -> None:
        self.computerColor = computerColor
        
        # Iegūstiet spēlētāja krāsu
        self.humanColor = invertTurn(self.computerColor)

        # Analizējamo pagriezienu skaits nākotnē
        self.depth = 3 # A balanced number would be 3
    
    def events(self):
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
    def isInCenter(self, pieceCord):
        row, col = pieceCord

        if row > sqInHeight//3 and row < int(sqInHeight*0.66):
            if col > sqInWidth//3 and col < int(sqInWidth*0.66):
                return True
            
        return False

    def eval(self, board):
        """
        Šī funkcija nosaka minimax algoritma efektivitāti, jo tā uzskata kustību par labu.
        Tas ņem vērā: gabalu skaitu, karaļu skaitu, kontrolē esošo gabalu skaitu un gabalu izvietojumu
        Izvietojums tiek novērtēts pēc gabalu skaita dēļa centrā
        """
        humanPieces = computerPieces = humanKings = computerKings = 0 # N pieces
        humanSquareControl = computerSquareControl = 0 # Control
        humanPiecesInCenter = computerPiecesInCenter = 0 # N Pieces in center

        for rowIndex,row in enumerate(board):
            for colIndex,col in enumerate(row):

                piece = board[rowIndex][colIndex]
                pieceCord = (rowIndex, colIndex)

                if piece != 0:
                    if piece.color == self.humanColor:
                        humanPieces += 1

                        humanSquareControl += len(getValidMoves(board, pieceCord))

                        if piece.king:
                            humanKings += 1

                        if self.isInCenter(pieceCord):
                            humanPiecesInCenter += 1

                    elif piece.color == self.computerColor:
                        computerPieces += 1

                        computerSquareControl += len(getValidMoves(board, pieceCord))

                        if piece.king:
                            computerKings += 1

                        if self.isInCenter(pieceCord):
                            computerPiecesInCenter += 1

        piecesScore = computerPieces-humanPieces
        kingsScore = computerKings-humanKings
        controlScore = computerSquareControl - humanSquareControl
        piecesInCenterScore = computerPiecesInCenter - humanPiecesInCenter

        # Aprēķina dēļa rezultātu
        # Katram faktoram ir savs reizinātājs
        return 1*piecesScore + 2*kingsScore + 1*controlScore + 2*piecesInCenterScore
    
    def writeGameTreeToFile(self, gameTree):
        """
        Ieraksta spēļu koku failā "files/gameTree.txt".
        Katra faila rinda apzīmē pārvietošanos spēles kokā šādā formātā:
        Gabals: (piece0, piece1) -> Move: (move0, move1)
        """

        # Atveriet failu rakstīšanai
        with open("gameTree.txt", "w") as file:
            for move_dict in gameTree:
                for pieceCoords, moveCoords in move_dict.items():
                    
                    # Konvertējiet gabalu un pārvietojiet vērtības uz formatētām virknēm
                    pieceStr = f"Piece: ({pieceCoords[0]}, {pieceCoords[1]})"
                    moveStr = f"Move: ({moveCoords[0]}, {moveCoords[1]})"
                    
                    # Ierakstiet failā formatēto virkni
                    line = f"{pieceStr} -> {moveStr}\n"
                    file.write(line)

    def minimax(self, board, depth, maximizing_player, gameTree, alpha, beta):
        """
        Šis ir minimax algoritma Python implementācija ar alfa-beta atzarošanu spēļu lēmumu pieņemšanai.
        Tas rekursīvi novērtē visas iespējamās kustības, atkārtojot spēlētāja figūras un derīgus gājienus,
        izvēloties gājienu ar augstāko vai zemāko vērtību atkarībā no tā, vai tas ir attiecīgi maksimizējoša vai minimizējoša spēlētājs.
        Algoritms izmanto alfa-beta atzarošanu, lai uzlabotu efektivitāti, likvidējot zarus, kas, visticamāk, nenovedīs pie labāka rezultāta.
        """
        
        self.events() # Check for window close

        # Exit condition
        if depth == 0 or checkWin(board):
            return self.eval(board), gameTree

        if maximizing_player:
            bestValue = float("-inf")
            for piece in getPiecesWidthValidMoves(board, self.computerColor):
                for move in getValidMoves(board, piece):
                    newBoard = deepcopy(board)
                    newBoard = makeMove(newBoard, self.computerColor, piece, move)
                    
                    gameTree.append({tuple(piece):tuple(move)})
                    value, gameTree = self.minimax(newBoard, depth - 1, False, gameTree, alpha, beta)
                    bestValue = max(bestValue, value)

                    alpha = max(alpha, bestValue)
                    if beta <= alpha:
                        break
                if beta <= alpha:
                    break
            return bestValue, gameTree
        
        else:
            bestValue = float("inf")
            for piece in getPiecesWidthValidMoves(board, self.humanColor):
                for move in getValidMoves(board, piece):
                    newBoard = deepcopy(board)
                    newBoard = makeMove(newBoard, self.humanColor, piece, move)

                    gameTree.append({tuple(piece):tuple(move)})
                    value, gameTree = self.minimax(newBoard, depth - 1, True, gameTree, alpha, beta)
                    bestValue = min(bestValue, value)

                    beta = min(beta, bestValue)
                    if beta <= alpha:
                        break
                if beta <= alpha:
                    break
            return bestValue, gameTree
    
    def getMove(self, board):
        # Inicialize vertibas
        bestPiece, bestMove = None, None
        bestScore = float("-inf")
        
        # Itere cauri visiem datora kauliniem ar derigiem gajieniem
        for piece in getPiecesWidthValidMoves(board, self.computerColor):
            for move in getValidMoves(board, piece):

                # Izveidojiet jaunu dēļa stāvokli, kopējot pašreizējo paneli
                newBoard = deepcopy(board)

                # Veikt kustību šajā kopētajā laukumā
                newBoard = makeMove(newBoard, self.computerColor, piece, move)

                # Aprēķināt kustības rezultātu, izmantojot minimālo algoritmu
                score, gameTree = self.minimax(newBoard, self.depth, False, [{tuple(piece):tuple(move)}], float("-inf"), float("inf"))

                # Ja šī gājiena rezultāts ir labāks par līdz šim labāko rezultātu, atjauniniet labāko gabalu, labāko gājienu un labāko rezultātu
                if score > bestScore:
                    bestScore = score
                    bestTree = gameTree
                    bestPiece, bestMove = piece, move

        self.writeGameTreeToFile(bestTree)

        # Atgriezt labāko gabalu un labāko kustību
        return bestPiece, bestMove



