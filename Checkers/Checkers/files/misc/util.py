from .settings import *
import pygame

def calculatePos(row, col):
    return (sqSize*col + sqSize//2, sqSize*row + sqSize//2)

def calculateCoord(x, y):
    return y//sqSize, x//sqSize

def drawSquares(screen):
    for row in range(sqInWidth):
        for col in range(row % 2, sqInWidth, 2):
            pygame.draw.rect(screen, BOARD_COLOR, (row*sqSize, col*sqSize, sqSize, sqSize))

def invertTurn(turn):
    if turn == 'black':
        return 'white'
    else:
        return 'black' 

def getPiecesWidthValidMoves(board, pieceColor):
    pieces = []

    for rowIndex,row in enumerate(board):
        for colIndex,col in enumerate(row):
            square = board[rowIndex][colIndex]
            
            if square != 0:
                if square.color == pieceColor and len(getValidMoves(board, (rowIndex, colIndex))) > 0:
                    pieces.append([rowIndex, colIndex])

    return pieces

def isValidMove(board, pieceCoord, moveCoord):
    # Iegūstiet gabala pašreizējo rindu un kolonnu
    row, col = pieceCoord
    piece = board[row][col]

    # Iegūstiet galamērķa rindu un kolonnu
    destRow, destCol = moveCoord

    # Pārbaudiet, vai laukumu aizņem paša spēlētāja figūra
    if board[destRow][destCol] != 0 and board[destRow][destCol] != piece.color:
        return False
    
    # Pārbaudiet, vai gājiens ir derīgs lēciens pāri pretinieka figūrai
    if piece.color == 'black':
        opponent = 'white'
    else:
        opponent = 'black'

    # Pārbaudiet, vai gājiens ir diagonāls gājiens, kas ietver lēcienu pāri pretinieka figūrai
    rowDiff = abs(row - destRow)
    colDiff = abs(col - destCol)
    if rowDiff == 2 and colDiff == 2:
        jumpRow = (row + destRow) // 2
        jumpCol = (col + destCol) // 2
        jumpPos = board[jumpRow][jumpCol]
        if jumpPos != 0 and ((destRow - row) * piece.direction > 0 or piece.king):
            if jumpPos.color == opponent and board[destRow][destCol] == 0:
                return True
    # Pārbaudiet, vai kustība ir vienkārša pa diagonāli
    if rowDiff == 1 and colDiff == 1:
        if (destRow - row) * piece.direction > 0 or piece.king:
            return True
    # Ja neviens no iepriekš minētajiem nosacījumiem nav izpildīts, pārvietošana nav derīga
    return False

def getValidMoves(board, pieceCord):
    row, col = pieceCord
    validMoves = []

    for indexRow,rowBoard in enumerate(board):
        for indexCol,colBoard in enumerate(rowBoard):
            if isValidMove(board, (row, col), (indexRow, indexCol)):
                validMoves.append([indexRow, indexCol])
    
    return validMoves

def checkWin(board):
    winner = None
    if len(getPiecesWidthValidMoves(board, 'black')) == 0:
        winner = 'white'
    
    elif len(getPiecesWidthValidMoves(board, 'white')) == 0:
        winner = 'black'
    
    return winner

def checkMoveMakesKing(row, pieceColor):
    """Pārbaudiet, vai gājiens padara figūru par karali"""

    if pieceColor == 'black':
        if row == sqInHeight-1:
            return True
        
    elif pieceColor == 'white':
        if row == 0:
            return True
        
    return False

def makeMove(board, turn, piece, move):
    pieceRow, pieceCol = piece
    moveRow, moveCol = move
    
    board[pieceRow][pieceCol].move(moveRow, moveCol)

    board[moveRow][moveCol] = board[pieceRow][pieceCol]
    board[pieceRow][pieceCol] = 0

    if checkMoveMakesKing(moveRow, turn):
        board[moveRow][moveCol].makeKing()

    rowDiff, colDiff = abs(pieceRow - moveRow), abs(pieceCol - moveCol)

    if rowDiff == 2 and colDiff == 2:

        jumpRow, jumpCol = (pieceRow + moveRow) // 2, (pieceCol + moveCol) // 2
        jumpPos = board[jumpRow][jumpCol]
        if jumpPos.color == invertTurn(turn):
            board[jumpRow][jumpCol] = 0

    return board

