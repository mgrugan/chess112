from cmu_graphics import *
import subprocess
import copy

class ChessPiece:
    def __init__(self, pieceType, row, col, isWhite):
        self.type = pieceType
        self.row = row
        self.col = col
        self.isWhite = isWhite
        self.hasMoved = False
    
    def linearMoves (self, board, directionChanges):
        moves = []
        for rowChange, colChange in directionChanges:
            currRow = self.row
            currCol = self.col
            while True:
                currRow += rowChange
                currCol += colChange
                if not (0 <= currRow < 8 and 0 <= currCol < 8):
                    break
                target = board[currRow][currCol]
                if target == None:
                    moves.append((currRow, currCol))
                elif self.isWhite != target.isWhite:
                    moves.append((currRow, currCol))
                    break
                else:
                    break
        return moves
    def singleStep(self, board, directionalChange):
        moves = []
        for rowChange, colChange in directionalChange:
            row = rowChange + self.row
            col = colChange + self.col
            if 0 <= row < 8 and 0<= col <8:
                target = board[row][col]
                if target == None or (self.isWhite != target.isWhite):
                    moves.append((row, col))
        return moves

    def getLegalMoves(self, board):
        moves = []
        if self.type == "P":
            direction = -1 if self.isWhite else 1
            if 0 <= self.row + direction < 8 and board[self.row + direction][self.col] == None:
                moves.append((self.row + direction, self.col))
            if (self.isWhite and self.row == 6) or (not self.isWhite and self.row == 1):
                if board[self.row + direction][self.col] == None and board[self.row + 2 * direction][self.col] == None:
                    moves.append((self.row + 2*direction, self.col))
            for diagonals in [-1, 1]:
                if 0 <= self.col + diagonals < 8 and 0 <= self.row + direction < 8:
                    target = board[self.row + direction][self.col + diagonals] 
                    if target and target.isWhite != self.isWhite:
                        moves.append((self.row + direction, self.col + diagonals))

        elif self.type == "R":
            moves.extend(self.linearMoves(board,[(0,1), (1, 0), (0, -1),(-1,0)]))
        elif self.type == "B":
            moves.extend(self.linearMoves(board,[(1,1), (1, -1), (-1, -1),(-1,1)]))
        elif self.type == 'Q':
            moves.extend(self.linearMoves(board,[(0,1), (1, 0), (0, -1),(-1,0),
                                    (1,1), (1, -1), (-1, -1),(-1,1)]))

        elif self.type == "N":
            moves.extend(self.singleStep(board, [(2, -1), (2, 1), (-2, 1), (-2, -1),
                                                 (1, 2), (1, -2), (-1, 2), (-1, -2)]))
        if self.type == "K": 
            moves.extend(self.singleStep(board, [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), 
                                                 (-1, 1), (1, -1), (-1, -1)]))
            
            if not self.hasMoved:
                row = self.row
                if board[row][5] == None and board[row][6] == None:
                    rook = board[row][7]
                    if rook and rook.type == "R" and not rook.hasMoved:
                        if not isKingInCheck(board, self.isWhite) and \
                        not makesKingCheck(board, self, row, 5) and not makesKingCheck(board, self, row, 6):
                                moves.append((row, 6))

                if board[row][1] is None and board[row][2] is None and board[row][3] is None:
                    rook = board[row][0]
                    if rook and rook.type == "R" and not rook.hasMoved:
                        if not isKingInCheck(board, self.isWhite) and\
                            not makesKingCheck(board, self, row, 3) and not makesKingCheck(board, self, row, 2):
                            moves.append((row, 2))


        return moves
        
    def attackingMoves(self, board):
        moves = []
        if self.type == "P":
            moves = []
            direction = -1 if self.isWhite else 1
            for diagonals in [-1, 1]:
                row = self.row + direction 
                col = self.col + diagonals
                if 0 <= row < 8 and 0 <= col < 8:
                    moves.append((row, col))
            return moves
        elif self.type == "R":
            moves.extend(self.linearMoves(board,[(0,1), (1, 0), (0, -1),(-1,0)]))
        elif self.type == "B":
            moves.extend(self.linearMoves(board,[(1,1), (1, -1), (-1, -1),(-1,1)]))
        elif self.type == 'Q':
            moves.extend(self.linearMoves(board,[(0,1), (1, 0), (0, -1),(-1,0),
                                    (1,1), (1, -1), (-1, -1),(-1,1)]))

        elif self.type == "N":
            moves.extend(self.singleStep(board, [(2, -1), (2, 1), (-2, 1), (-2, -1),
                                                 (1, 2), (1, -2), (-1, 2), (-1, -2)]))
        elif self.type == "K": 
            moves.extend(self.singleStep(board, [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), 
                                                 (-1, 1), (1, -1), (-1, -1)]))
        return moves
def onAppStart(app):

    app.rows = 8
    app.cols = 8
    app.boardLeft = 375
    app.boardTop = 50
    app.boardWidth = 700
    app.boardHeight = 700
    app.cellBorderWidth = 1
    app.board = createInitialBoard()
    app.selectedPiece = None
    app.turn = True 
    app.makePromotion = False

    app.moveHistory = []

    app.rectLeft = 20
    app.rectTop = 20
    app.menuButtonWidth = 100
    app.menuButtonHeight = 50
    app.dashesOn = False

    app.rectLeft1 = 1100
    app.rectTop1 = 400
    app.UDWidth = 200
    app.UDHieght = 75

    
    app.gameOver = False
    app.GOWidth = 450
    app.GOHeight = 200
    app.GOLeft = (app.width//2) - (app.GOWidth//2)
    app.GOTop = (app.height//2) - (app.GOHeight//2)

    app.whitePawn = "/Users/mariogrugan/Documents/15-112/whitePieces/whitePawn.png" # https://greenchess.net/info.php?item=downloads downloaded all of pieces from here
    app.whiteKing = "/Users/mariogrugan/Documents/15-112/whitePieces/white-king.png" 
    app.whiteQueen = "/Users/mariogrugan/Documents/15-112/whitePieces/white-queen.png"
    app.whiteKnight = "/Users/mariogrugan/Documents/15-112/whitePieces/white-knight.png"
    app.whiteBishop = "/Users/mariogrugan/Documents/15-112/whitePieces/white-bishop.png"
    app.whiteRook = "/Users/mariogrugan/Documents/15-112/whitePieces/white-rook.png"

    
    app.blackPawn = "/Users/mariogrugan/Documents/15-112/blackPieces/blackPawn.png"
    app.blackKing = "/Users/mariogrugan/Documents/15-112/blackPieces/black-king.png"
    app.blackQueen = "/Users/mariogrugan/Documents/15-112/blackPieces/black-queen.png"
    app.blackKnight = "/Users/mariogrugan/Documents/15-112/blackPieces/black-knight.png"
    app.blackBishop = "/Users/mariogrugan/Documents/15-112/blackPieces/black-bishop.png"
    app.blackRook = "/Users/mariogrugan/Documents/15-112/blackPieces/black-rook.png"


def createInitialBoard():
    board = [
        [ChessPiece("R", 0, 0, False),
        ChessPiece("N", 0, 1, False),
        ChessPiece("B", 0, 2, False),
        ChessPiece("Q", 0, 3, False),
        ChessPiece("K", 0, 4, False),
        ChessPiece("B", 0, 5, False),
        ChessPiece("N", 0, 6, False),
        ChessPiece("R", 0, 7, False)],
            [ChessPiece('P', 1, col, False) for col in range(8)],
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
        [ChessPiece('P', 6, col, True) for col in range(8)],
        [ChessPiece("R", 7, 0, True),
            ChessPiece("N", 7, 1, True),
            ChessPiece("B", 7, 2, True),
            ChessPiece("Q", 7, 3, True),
            ChessPiece("K", 7, 4, True),
            ChessPiece("B", 7, 5, True),
            ChessPiece("N", 7, 6, True),
            ChessPiece("R", 7, 7, True)]
            ]
    return board

def redrawAll(app):
    drawBackground(app)
    drawBoard(app)
    drawBoardBorder(app)
    drawMainMenu(app)
    drawCoordinates(app)
    drawUndoButton(app)
    if app.makePromotion:
        drawPromoOptions(app)
    if app.gameOver:

        if app.turn == True:
            winner = 'WHITE'
            
        else:
            winner = 'BLACK'
            
        drawRect(app.GOLeft, app.GOTop, app.GOWidth, app.GOHeight,
                 fill = 'purple', border = "white", borderWidth = 5)
        drawLabel(f'CHECKMATE! {winner} WON!', app.GOLeft + app.GOWidth//2, app.GOTop +  app.GOHeight//2, fill = 'white', size=30)
        drawLabel("Press 'R' To Restart", app.GOLeft + app.GOWidth//2 , app.GOTop +  app.GOHeight//2 + 50, 
                  size = 20, fill = 'white' )
    if app.selectedPiece:
        selectedPiece = app.selectedPiece
        cellLeft, cellTop = getCellLeftTop(app, selectedPiece.row, selectedPiece.col)
        cellWidth, cellHeight = getCellSize(app)
        drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill = None, border = "yellow", borderWidth = 3)
    

def drawPromoOptions(app):
    piece = app.board[app.promotionRow][app.promotionCol] 
    isWhite = piece.isWhite
    promotionOptions = ['Q', 'R', 'B', "N"]
    images = { 'Q': app.whiteQueen if isWhite else app.blackQueen,
              'R': app.whiteRook if isWhite else app.blackRook,
              'B': app.whiteBishop if isWhite else app.blackBishop,
              'N': app.whiteKnight if isWhite else app.blackKnight
}

    optionWidth = 100
    optionHeight = 100
    startX = app.width//2 - 200
    startY = app.height // 2 - 50

    counter = 0
    for option in promotionOptions:
        left = startX + counter  * optionWidth
        top = startY 
        drawRect(left, top, optionWidth, optionHeight, fill = "purple", border = "white")
        drawImage(images[option], left + 10, top + 10, width = optionWidth -20, height=optionHeight -20)
        counter += 1

def drawUndoButton(app):
    drawRect(app.rectLeft1, app.rectTop1, app.UDWidth, app.UDHieght, 
             fill = 'purple',border = "white")
    drawLabel("Undo Move",app.rectLeft1 +  app.UDWidth//2, app.rectTop1 + app.UDHieght//2, 
              size = 18, fill = 'white')


def drawMainMenu(app):
    drawRect(app.rectLeft, app.rectTop, app.menuButtonWidth, app.menuButtonHeight, 
             fill = 'purple',border = "white", dashes = app.dashesOn)
    drawLabel("Main Menu",app.rectLeft +  app.menuButtonWidth//2, app.rectTop + app.menuButtonHeight//2, 
              size = 18, fill = 'white')

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            color = 'white' if (row + col) % 2 == 0 else rgb(97, 38, 163)
            drawCell(app, row, col, color)
            drawPiece(app, row, col)

def drawPiece(app, row, col):
    if row < len(app.board) and col < len(app.board[row]):
        piece = app.board[row][col]
        if piece:
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellWidth, cellHeight = getCellSize(app)
            pieceImages = {
                ('P', True) :app.whitePawn, 
                ('P', False) : app.blackPawn,
                ('B', True): app.whiteBishop,
                ('B', False): app.blackBishop, 
                ('N', True): app.whiteKnight,
                ('N', False): app.blackKnight,
                ('K', True): app.whiteKing,
                ('K', False): app.blackKing,
                ('Q', True): app.whiteQueen,
                ('Q', False): app.blackQueen,
                ('R', True): app.whiteRook,
                ('R', False): app.blackRook}
            pieceImage = pieceImages.get((piece.type,piece.isWhite))
            if pieceImage:
                drawImage(pieceImage, cellLeft, cellTop, width = cellWidth, height = cellHeight)

def drawCoordinates(app):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
    i, j = getCellSize(app)
    coordX = 418
    for letter in letters:
        drawLabel(letter, coordX, 775, fill = "white", size = 22)
        coordX += i
    numbers = ["8", "7", "6", "5", "4", "3", "2", "1"]
    coordY = 98
    for number in numbers:
        drawLabel(number, 345, coordY, fill = "white", size = 22)
        coordY += i

def drawBoardBorder(app):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)
def drawBackground(app):
    drawRect(0, 0, 1920, 1080, fill= rgb(97, 38, 163), opacity = 70)


def onMouseMove(app, mouseX, mouseY):
    
    right = app.rectLeft + app.menuButtonWidth
    top = app.rectTop + app.menuButtonHeight
    if (app.rectLeft <= mouseX <= right) and (app.rectTop <= mouseY <= top):
        app.dashesOn = True
    else:
        app.dashesOn = False
def onMousePress(app, mouseX, mouseY):
    if app.makePromotion:
        makePromotion(app, mouseX, mouseY)

    UDright = app.rectLeft1 + app.UDWidth
    UDtop = app.rectTop1 + app.UDHieght
    if (app.rectLeft1 <= mouseX <= UDright) and (app.rectTop1 <= mouseY <= UDtop):
        undoMove(app)

    rightRect = app.rectLeft + app.menuButtonWidth
    topRect = app.rectTop + app.menuButtonHeight
    if (app.rectLeft <= mouseX <= rightRect) and (app.rectTop <= mouseY <= topRect):
        subprocess.Popen(['python3', '/Users/mariogrugan/Documents/15-112/Main_Menu.py'], start_new_session=True) #https://www.youtube.com/watch?v=LTcmdZhrc00 learned about subprocess and for specific argument I found https://www.datacamp.com/tutorial/python-subprocess here
        exit()

    rightBoard = app.boardLeft + app.boardWidth
    topBoard = app.boardTop + app.boardHeight
    if (app.boardLeft <= mouseX <= rightBoard) and (app.boardTop <= mouseY <= topBoard):
        row, col = getSelectedCell(app, mouseX, mouseY)
    
        if app.selectedPiece:
            movePieces(app, row, col)
        elif not app.selectedPiece:
            selectPiece(app, row, col)
   
def undoMove(app):
    if app.moveHistory:
        app.board = app.moveHistory.pop()
        app.turn = not app.turn
        app.selectedPiece = None
        app.makePromotion = False
def makePromotion(app, mouseX, mouseY):
    promotionOptions = ['Q', 'R', 'B', "N"]
    optionWidth = 100
    optionHeight = 100
    startX = app.width//2 - 200
    startY = app.height // 2 - 50

    counter = 0
    for option in promotionOptions:
        left = startX + counter  * optionWidth
        top = startY 
        if left <= mouseX <= left + optionWidth and top <= mouseY <= top + optionHeight:
            pieceType = option
            row = app.promotionRow
            col = app.promotionCol
            isWhite = app.board[row][col].isWhite 
            app.board[row][col] = ChessPiece(pieceType, row, col, isWhite)
            app.makePromotion = False
            

            if checkmate(app.board, not app.turn):
                app.gameOver = True 

            app.turn = not app.turn
            app.selectedPiece = None
            return
        counter += 1


def getSelectedCell(app, x, y):
    
    cellWidth, cellHieght = getCellSize(app)
    row = int((y - app.boardTop)/cellHieght)
    col = int((x - app.boardLeft)/cellWidth)
    if 0 <= row < app.rows and 0 <= col < app.cols:
        return (row, col)
    else:
        return 
    
def selectPiece(app, row, col):
    selectedPiece = app.board[row][col]
    if selectedPiece is not None:
        if (app.turn and selectedPiece.isWhite) or (not app.turn and not selectedPiece.isWhite):
            app.selectedPiece = selectedPiece

def movePieces(app, row, col):

    piece = app.selectedPiece
    legalMoves = piece.getLegalMoves(app.board)

    if (row, col) in legalMoves:
        if (app.turn and piece.isWhite) or (not app.turn and not piece.isWhite):
            if not makesKingCheck(app.board, piece, row, col):
                app.moveHistory.append(copy.deepcopy(app.board))
                if piece.type == "K" and abs(piece.col - col) == 2:
                    if col == 6:
                        rook = app.board[row][7]
                        app.board[piece.row][5] = rook
                        app.board [piece.row][7] = None
                        rook.col = 5
                    elif col == 2:
                        rook = app.board[row][0]
                        app.board[piece.row][3] = rook
                        app.board[piece.row][0] = None
                        rook.col = 3
            
                app.board[piece.row][piece.col] = None
                piece.row, piece.col = (row, col)
                app.board[row][col] = piece 
                piece.hasMoved = True

                if piece.type == "P" and (row == 0 or row == 7):
                    
                    app.promotionRow = row
                    app.promotionCol = col
                    app.makePromotion = True
                    app.selectedPiece = None
                    return 

                if checkmate(app.board, not app.turn):
                    app.gameOver = True
                else:
                    app.turn = not app.turn
    app.selectedPiece = None
def makesKingCheck(board, piece, targetRow, targetCol):

    #ChatGPT helped me debug this because originally
    #my code hit max recursion depth when 
    #implimenting castling and I didn't know why. Only took out boolean logic
    #and replaced with this 'kingInCheck = isKingInCheck(board, piece.isWhite.'


    ogRow = piece.row
    ogCol = piece.col
    targetPiece = board[targetRow][targetCol]

    board[ogRow][ogCol] = None
    board[targetRow][targetCol] = piece
    piece.row, piece.col = targetRow, targetCol

    kingInCheck = isKingInCheck(board, piece.isWhite)

                
    board[targetRow][targetCol] = targetPiece
    board[ogRow][ogCol] = piece
    piece.row = ogRow
    piece.col = ogCol

    return kingInCheck


def isKingInCheck(board, pieceColor):
    king = None

    for row in board:
        for piece in row:
            if piece and piece.type == "K" and piece.isWhite == pieceColor:
                king = piece
                break
        if king:
            break
    
    for row in board:
        for attackingPiece in row:
            if attackingPiece and attackingPiece.isWhite != pieceColor:
                if (king.row, king.col) in attackingPiece.attackingMoves(board):
                    return True
            
    return False

def checkmate(board, isWhiteTurn):
    if not isKingInCheck(board, isWhiteTurn):
        return False
    
    for row in board:
        for piece in row:
            if piece and piece.isWhite == isWhiteTurn:
                for moves in piece.getLegalMoves(board):
                    targetRow, targetCol = moves
                    if not makesKingCheck(board, piece,targetRow, targetCol):
                        return False
    return True


def onKeyPress(app, key):
    if app.gameOver and key == 'R':
        app.board = createInitialBoard()
        app.moveHistory = []
        app.gameOver = False
        app.selectedPiece = None
        app.makePromotion = False
        app.turn = True



def main():
    runApp(width = 1500, height = 800)

main()