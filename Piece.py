class Piece():

    def __init__(self, color, name, pos):
        self.Name = name
        self.Color = color
        self.Position = pos
        self.Promotion = False
        self.Promotable = False

class Pawn(Piece):

    def __init__(self,color,name,pos, Direction):
        super().__init__(color, name, pos)
        self.Direction = Direction
        self.moves = [[(-1, 0)], []]
        self.Pmoves = [(-1, -1), (-1, 0), (-1, 1), (1, 0), (0, -1), (0, 1), []]


class Bishop(Piece):
    def __init__(self,color,name,pos, Direction):
        super().__init__(color, name, pos)
        self.Direction = Direction
        self.moves = [[], [(1, 1), (1, -1), (-1, 1), (-1, -1)]]
        self.Pmoves = [[(-1, 0), (0, -1), (0, 1), (1, 0)], [(1, 1), (1, -1), (-1, 1), (-1, -1)]]

class Rook(Piece):
    def __init__(self,color,name,pos, Direction):
        super().__init__(color, name, pos)
        self.Direction = Direction
        self.moves = [[], [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        self.Pmoves = [[(-1, -1), (-1, 1), (1, -1), (1, 1)], [(-1, 0), (1, 0), (0, -1), (0, 1)]]

class Lance(Piece):
    def __init__(self,color,name,pos, Direction):
        super().__init__(color, name, pos)
        self.Direction = Direction
        self.moves = [[], [(-1, 0)]]
        self.Pmoves = [[(-1, -1), (-1, 0), (-1, 1), (1, 0), (0, -1), (0, 1)], []]

class Knight(Piece):
    def __init__(self,color,name,pos, Direction):
        super().__init__(color, name, pos)
        self.Direction = Direction
        self.moves = [[(-2, -1), (-2, 1)], []]
        self.Pmoves = [[(-1, -1), (-1, 0), (-1, 1), (1, 0), (0, -1), (0, 1)], []]

class Silver_General(Piece):
    def __init__(self,color,name,pos, Direction):
        super().__init__(color, name, pos)
        self.Direction = Direction
        self.moves = [[(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 1)], []]
        self.Pmoves = [[(-1, -1), (-1, 0), (-1, 1), (1, 0), (0, -1), (0, 1)], []]


class Gold_General(Piece):
    def __init__(self,color,name,pos, Direction):
        super().__init__(color, name, pos)
        self.Direction = Direction
        self.Promotion = True
        self.moves = [[(-1, -1), (-1, 0), (-1, 1), (1, 0), (0, -1), (0, 1)], []]
        self.Pmoves = [[(-1, -1), (-1, 0), (-1, 1), (1, 0), (0, -1), (0, 1)], []]

class King(Piece):
    def __init__(self,color,name,pos, Direction):
        super().__init__(color, name, pos)
        self.Direction = Direction
        self.Promotion = True
        self.moves = [[(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)], []]
        self.Pmoves = [[(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)], []]
