#this class is responsible for storing all the information of the current state of a shogi game
#also used to determine valid moves and move log
import Piece
import copy

class GameState():
    def __init__(self, dimensions, whiteToMove, timer):

        #starting chess board setup, first letter indicates the colour, second letter indicates the shogi piece
        if dimensions == "9x9":
            self.board = [
            ["BL", "BN", "BS", "BG", "BK", "BG", "BS", "BN", "BL",],
            ["--", "BR", "--", "--", "--", "--", "--", "BB", "--",],
            ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP",],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--",],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--",],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--",],
            ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP",],
            ["--", "WB", "--", "--", "--", "--", "--", "WR", "--",],
            ["WL", "WN", "WS", "WG", "WK", "WG", "WS", "WN", "WL"]]

            self.dimensionsx = 9
            self.dimensionsy = 9
        elif dimensions == "5x4":
            self.board = [
            ["BK", "BB", "BG", "BS"],
            ["BP", "--", "--", "--"],
            ["--", "--", "--", "--"],
            ["--", "--", "--", "WP"],
            ["WS", "WG", "WB", "WK"]]
            self.dimensionsx = 5
            self.dimensionsy = 4

        elif dimensions == "5x5":
            self.board = [
            ["BR", "BB", "BS", "BG", "BK"],
            ["--", "--", "--", "--", "BP"],
            ["--", "--", "--", "--", "--"],
            ["WP", "--", "--", "--", "--"],
            ["WK", "WG", "WS", "WB", "WR"]]

            self.dimensionsx = 5
            self.dimensionsy = 5

        self.whiteToMove = whiteToMove
        self.moveLog = []
        self.Wcapture = []
        self.Bcapture = []

        if timer != False:
            self.Wtimer = timer
            self.Btimer = timer
            self.timer = True
        else:
            self.Wtimer = 100
            self.Btimer = 100
            self.timer = False

        self.Setup1()


    def Setup1(self):
        for i in range(self.dimensionsx):
            for j in range(self.dimensionsy):
                N = self.board[i][j][1]
                if self.board[i][j][0] == "W":
                    C = "White"
                    D = 1
                else:
                    C = "Black"
                    D = -1
                if N == "P":
                    self.board[i][j] = Piece.Pawn(C, "Pawn", (i, j), D)

                elif N == "R":
                    self.board[i][j] = Piece.Rook(C, "Rook", (i, j), D)
                elif N == "B":
                    self.board[i][j] = Piece.Bishop(C, "Bishop", (i, j), D)
                elif N == "L":
                    self.board[i][j] = Piece.Lance(C, "Lance", (i, j), D)

                elif N == "N":
                    self.board[i][j] = Piece.Knight(C, "Night", (i, j), D)

                elif N == "S":
                    self.board[i][j] = Piece.Silver_General(C, "Silver General", (i, j), D)

                elif N == "G":
                    self.board[i][j] = Piece.Gold_General(C, "Gold General", (i, j), D)

                elif N == "K":
                    self.board[i][j] = Piece.King(C, "King", (i, j), D)

                else:
                    self.board[i][j] = Piece.Piece("Null", "Null", (i, j))



    def makeMove(self, move):

        """
        R1, R2, C1, C2: starting row, ending row, starting column, ending column
        """
        R1 = move.startRow
        C1 = move.startCol
        R2 = move.endRow
        C2 = move.endCol

        temp = self.board[R1][C1].Position #temporary stores position of moving piece


        self.board[R2][C2] = Piece.Piece("Null", "Null", (R1, C1))#clears squares
        self.board[R1][C1] = Piece.Piece("Null", "Null", (R1, C1))

        move.pieceMoved.Position = (R2, C2)
        self.board[R2][C2] = move.pieceMoved
        if self.board[R2][C2].Promotable != True: #checks if piece can be promoted
            self.board[R2][C2].Promotable = move.checkPromote(self.board[R2][C2])
        if move.pieceMoved.Promotion == True:
            move.pieceMoved.moves = move.pieceMoved.Pmoves

        if move.pieceCaptured.Name != "Null": #appends captured piece of capture list
            if move.pieceCaptured.Color == "White":
                self.Bcapture.append(move.pieceCaptured)
            elif move.pieceCaptured.Color =="Black":
                self.Wcapture.append(move.pieceCaptured)


    def isInBoard(self,x,y):
        "checks if a position is on the board"
        if x >= 0 and x < self.dimensionsx and y >= 0 and y < self.dimensionsy:
            return True
        return False


    def checkCheck(self, Color, moves):

        checkPiece = []
        for i in range(self.dimensionsx):
            for j in range(self.dimensionsy):
                if self.board[i][j].Name == "King":
                    if self.board[i][j].Color == Color:
                        C = self.board[i][j]
                else:
                    pass

        for i in moves:
            for j in i[3]:
                if j[0] == C.Position[0] and j[1] == C.Position[1]:
                    O = i[:3]
                    O.append(j)
                    checkPiece.append(O)
        return checkPiece

    def getMovePiece(self, Piece):
        moves = []

        T = Piece
        if T.Name != "Null":
            S = []
            S.append(T.Name)
            S.append(T.Color)
            S.append(T.Position)
            Sset = T.moves
            Pos = T.Position
            C = []

            for l in Sset[1]:
                Dx = 1
                Dy = 1
                Dx = Dx * l[0] * T.Direction
                Dy = Dy * l[1] * T.Direction
                Ty = 0
                Tx = 0

                for L in range(self.dimensionsx):
                    Tx = Tx + Dx
                    Ty = Ty + Dy

                    k = [Pos[0] + Tx, Pos[1] + Ty]
                    if self.isInBoard(k[0], k[1]):
                        if self.board[k[0]][k[1]].Color =="Null":
                            C.append(k)

                        elif self.board[k[0]][k[1]].Color != T.Color:
                            C.append(k)
                            break
                        elif self.board[k[0]][k[1]].Color == T.Color:
                            break



            for G in Sset[0]:
                k = [Pos[0] + G[0]*T.Direction, Pos[1] + G[1]*T.Direction]
                if self.isInBoard(k[0], k[1]):
                    if self.board[k[0]][k[1]].Color != Color:
                        C.append(k)

            S.append(C)
            moves.append(S)
        return moves

    def checkMate(self, moves1, moves2, Clist, Color1, Color2):
        fix = False
        for i in moves1:
            for j in i[3]:
                move = Move(i[2], j, self.board, self.whiteToMove, moves2, moves1, [], [], 0, 0)
                g = copy.deepcopy(self)
                g.makeMove(copy.deepcopy(move))
                Bmoves1 = g.getMoves(Color1)
                Wmoves1 = g.getMoves(Color2)
                C = g.checkCheck(Color1, Wmoves1)

                if len(C) > 0:
                    pass

                elif (len(C)) == 0:
                    fix = True
                    break
            if fix:
                return True

        if not fix:
            return False


    def getMoves(self, Color):
        moves = []

        for i in range(self.dimensionsx):
            for j in range(self.dimensionsy):
                T = self.board[i][j]
                if T.Name != "Null" and T.Color == Color:
                    S = []
                    S.append(T.Name)
                    S.append(T.Color)
                    S.append(T.Position)
                    Sset = T.moves
                    Pos = T.Position
                    C = []

                    for l in Sset[1]:
                        Dx = 1
                        Dy = 1
                        Dx = Dx * l[0] * T.Direction
                        Dy = Dy * l[1] * T.Direction
                        Ty = 0
                        Tx = 0

                        for L in range(self.dimensionsx):
                            Tx = Tx + Dx
                            Ty = Ty + Dy

                            k = [Pos[0] + Tx, Pos[1] + Ty]
                            if self.isInBoard(k[0], k[1]):
                                if self.board[k[0]][k[1]].Color =="Null":
                                    C.append(k)

                                elif self.board[k[0]][k[1]].Color != T.Color:
                                    C.append(k)
                                    break
                                elif self.board[k[0]][k[1]].Color == T.Color:
                                    break

                    for G in Sset[0]:
                        k = [Pos[0] + G[0]*T.Direction, Pos[1] + G[1]*T.Direction]
                        if self.isInBoard(k[0], k[1]):
                            if self.board[k[0]][k[1]].Color != Color:
                                C.append(k)

                    S.append(C)
                    moves.append(S)
        return moves

    def validateMove(self, moves, move):
        R1 = move.startRow
        C1 = move.startCol
        R2 = move.endRow
        C2 = move.endCol
        validmove = False

        for i in moves:
            if move.pieceMoved.Name == i[0] and move.pieceMoved.Color == i[1] and move.pieceMoved.Position == i[2]:
                moveset = i
                for j in moveset[3]:
                    if R2 == j[0] and C2 == j[1]:
                        validmove = True
                        return True
        return False


class Move():

    #map keys to values
    #key : values
    rankToRows = {"1": 8, "2": 7, "3" : 6, "4" : 5,
                    "5" : 4, "6" : 3, "7" : 2, "8" : 1, "9" : 0}
    rowsToRanks = {v: k for k, v in rankToRows.items()}
    filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3,
                    "e" : 4, "f" : 5, "g" : 6, "h" : 7, "i" : 8}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, white, Wmoves, Bmoves, Wcap, Bcap, TimeW, TimeB):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.boardHis = copy.deepcopy(board)
        self.boardCapW = Wcap
        self.boardCapB = Bcap
        self.timeW = TimeW
        self.timeB = TimeB
        self.whiteMove = copy.deepcopy(white)
        self.WmovesH = copy.deepcopy(Wmoves)
        self.BmovesH = copy.deepcopy(Bmoves)

    def checkPromote(self, Piece):
        if Piece.Color == "White":
            if self.startRow > 2 and self.endRow<= 2:
                return True
            elif self.startRow <= 2 and self.endRow<= 2:
                return True
            elif self.startRow <= 2 and self.endRow > 2:
                return True
            else:
                return False

        if Piece.Color == "Black":
            if self.startRow < 6 and self.endRow >= 6:
                return True
            elif self.startRow >= 6 and self.endRow>= 6:
                return True
            elif self.startRow >= 6 and self.endRow < 6:
                return True
            else:
                return False

    def getShogiNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
