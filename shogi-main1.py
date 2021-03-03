#main class handles user input and current gameState class
import pygame as p
import shogiEngine1
import os
import copy
import Piece
import Menu


height = 1057 #defines the board resolution
width = 1920
sq_size = 66
x_offset = 459
y_offset = 243
scale = 1

p.font.init()

myfont = p.font.SysFont('Comic Sans MS', 28//scale)
myfont1 = p.font.SysFont('Comic Sans MS', 10//scale)
HEIGHT = height//scale
WIDTH = width//scale
SQ_size = sq_size//scale #defines the size of each square
xoffset = x_offset//scale
yoffset = y_offset//scale
MAX_FPS = 15
IMAGES = {}
IMAGES_TAKEN = {}
background = p.transform.scale(p.image.load("images/wood-square.png") , (706//scale, 706//scale))
colors = [p.color.Color("white"), p.color.Color("gray"), p.color.Color("black"), p.color.Color("green"), p.color.Color("purple")]

def load_Images(SQ_size, type):
    pieces = ["BL", "BN", "BS", "BG", "BK", "BB", "BR", "BP", "WL", "WN", "WS", "WG", "WK", "WB","WR", "WP"]

    if type == 1:
        for piece in pieces:
            IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png") , (SQ_size, SQ_size))
            IMAGES_TAKEN[piece] = p.transform.scale(p.image.load("images/" + piece + ".png") , (66//scale, 66//scale))
    else:
        for piece in pieces:
            IMAGES[piece] = p.transform.scale(p.image.load("images/JAP/" + piece + ".png") , (SQ_size, SQ_size))
            IMAGES_TAKEN[piece] = p.transform.scale(p.image.load("images/JAP/" + piece + ".png") , (66//scale, 66//scale))


def drawGameState(screen, gs, playerClicks, Wmoves, Bmoves, GO, MH, color, SQ_size): #graphics for current gamestate
    screen.fill(colors[0]) #reset screen to white
    drawBoard(screen, gs, playerClicks, Wmoves, Bmoves, MH, color, SQ_size) #draw squares on drawBoard
    drawPieces(screen, gs, SQ_size) #draw pieces on top of squares
    drawMoveHistory(screen, gs.moveLog) #draw move history
    drawTaken(screen, gs.Wcapture, gs.Bcapture) #draw taken pieces
    drawTimer(screen, gs) #draw player times

    if GO[2]: #Checks for game over
        drawWin(screen, GO)
    if gs.Wtimer <= 0:
        drawWin(screen, [False, True, True])
    elif gs.Btimer <= 0:
        drawWin(screen, [True, False, True])



def drawBoard(screen, gs, playerClicks, Wmoves, Bmoves, MH, color, SQ_size): #draw squares, later on: implement custom colors

    screen.blit(background, p.rect.Rect(403//scale, 187//scale, 706//scale, 706//scale))#draws backdrop of board

    k = [-1, -1]
    for r in range(gs.dimensionsx): #this inbedded loop loops over all squares in the board and generates them on the screen
        for c in range(gs.dimensionsy):
            colo = color[((r+c)%2)] #this line dictates the color of the square currently iterating
            p.draw.rect(screen, colo, p.rect.Rect(c*SQ_size+xoffset, r*SQ_size+yoffset, SQ_size, SQ_size))

    if len(playerClicks) == 1 and MH: #this portion is used when a piece has been selected to move but hasnt been moved yoffset
                                #this portion is to highlight all possible moves of that piece
        moveset = []
        if gs.whiteToMove: #checks whos turn it is
            for i in Wmoves: #iterates over the White possible moves to find the selected piece's moveset
                if i[2][0] == playerClicks[0][0] and i[2][1] == playerClicks[0][1]:
                    k = [i[2][0], i[2][1]]
                    moveset = i[3]
                    break
        else: #same as lines 65-70 but for the Black player
            for i in Bmoves:
                if i[2][0] == playerClicks[0][0] and i[2][1] == playerClicks[0][1]:
                    k = [i[2][0], i[2][1]]
                    moveset = i[3]
                    break

        for i in moveset: #iterates over the selected piece's possible moves and highlight the squares in green
            p.draw.rect(screen, colors[4], p.rect.Rect(i[1]*SQ_size+xoffset, i[0]*SQ_size+yoffset, SQ_size, SQ_size))

def drawPieces(screen, gs, SQ_size): #draw pieces on board using current gameState
    for r in range(gs.dimensionsx):
        for c in range(gs.dimensionsy): #nested loop used to iterate over all squares in the board
            piece = gs.board[r][c]
            if piece != "--": #not empty square
                if piece.Color != "Null": #not an empty square
                    screen.blit(IMAGES[piece.Color[0] + piece.Name[0]], p.rect.Rect(piece.Position[1]*SQ_size+xoffset, piece.Position[0]*SQ_size+yoffset, SQ_size, SQ_size))

def drawPromotion(screen):
    p.draw.rect(screen, colors[1], p.rect.Rect(1000//scale, 1000//scale, 156//scale, 48//scale))
    yes = myfont.render("yes", True, (255, 255, 255))
    screen.blit(yes, (1000//scale, 1000//scale))

    p.draw.rect(screen, colors[1], p.rect.Rect(1000//scale + 156//scale, 1000//scale, 156//scale, 48//scale))
    no = myfont.render("no", True, (255, 255, 255))
    screen.blit(no, (1000//scale + 156//scale, 1000//scale))

def drawMoveHistory(screen, moveLog):

    p.draw.rect(screen, colors[2], p.rect.Rect(1506//scale, 82//scale, 156//scale, 48//scale)) #draws box which move history will appear in
    undo = myfont.render("UNDO", True, (255, 255, 255)) #draws undo and redo tabs

    screen.blit(undo, (1506//scale, 82//scale))

    xsize = (390//3 - 2)//scale
    ysize = (862//25 -1)//scale

    for i in range(0, 25): #generates individual cells which each move will appear in
        p.draw.rect(screen, colors[2], p.rect.Rect(1507//scale + 1, (148//scale)+(i*(ysize + 1)), xsize, ysize), 1)

    if len(moveLog) >= 25: #sees if the length of the movelog is above limits
        r = 25
        M = moveLog[-25:] #here, M only contains the 25 most recent moves
    else:
        r = len(moveLog)
        M = moveLog.copy()
        M.reverse()
    for i in range(r): #iterates over M and prints each move

        m = M[i]
        text1 = myfont.render(m.getShogiNotation(), True, (0, 0, 0))
        text2 = myfont.render("---->", True, (0, 0, 0))

        screen.blit(text1,(1517//scale + 1,(140//scale)+(i*(ysize + 1))))


def drawTaken(screen, Wcapture, Bcapture):
    p.draw.rect(screen, colors[2], p.rect.Rect(403//scale, 46//scale,  462//scale, 66//scale), 2)#draws rectangle that will hold White piece graphics
    p.draw.rect(screen, colors[2], p.rect.Rect(403//scale, 112//scale,  462//scale, 66//scale), 2) #drawes rectangle that will hold number of each piece captured
    p.draw.rect(screen, colors[2], p.rect.Rect(403//scale, 900//scale,  462//scale, 66//scale), 2) #same as 134 but for white player
    p.draw.rect(screen, colors[2], p.rect.Rect(403//scale, 966//scale,  462//scale, 66//scale), 2) #same as 135 but for white player


    pieces = ["BL", "BN", "BS", "BG", "BB", "BR", "BP", "WL", "WN", "WS", "WG", "WB","WR", "WP"]
    for i in range(7):

        screen.blit(IMAGES_TAKEN[pieces[i]], p.rect.Rect((403+66*i)//scale, 112//scale,  66//scale, 66//scale))
        screen.blit(IMAGES_TAKEN[pieces[i+7]], p.rect.Rect((403+66*i)//scale, 900//scale,  66//scale, 66//scale))

    Wcount = [0, 0, 0, 0, 0, 0, 0]
    Bcount = [0, 0, 0, 0, 0, 0, 0]

    for i in Wcapture:
        if i.Name == "Lance":
            Wcount[0] = Wcount[0] + 1
        elif i.Name == "Night":
            Wcount[1] = Wcount[1] + 1
        elif i.Name == "Silver General":
            Wcount[2] = Wcount[2] + 1
        elif i.Name == "Gold General":
            Wcount[3] = Wcount[3] + 1
        elif i.Name == "Bishop":
            Wcount[4] = Wcount[4] + 1
        elif i.Name == "Rook":
            Wcount[5] = Wcount[5] + 1
        elif i.Name == "Pawn":
            Wcount[6] = Wcount[6] + 1


    for i in Bcapture:
        if i.Name == "Lance":
            Bcount[0] = Bcount[0] + 1
        elif i.Name == "Night":
            Bcount[1] = Bcount[1] + 1
        elif i.Name == "Silver General":
            Bcount[2] = Bcount[2] + 1
        elif i.Name == "Gold General":
            Bcount[3] = Bcount[3] + 1
        elif i.Name == "Bishop":
            Bcount[4] = Bcount[4] + 1
        elif i.Name == "Rook":
            Bcount[5] = Bcount[5] + 1
        elif i.Name == "Pawn":
            Bcount[6] = Bcount[6] + 1

    for i in range(len(Wcount)):
        text1 = myfont.render(str(Wcount[i]), True, (0, 0, 0))
        screen.blit(text1,((403+66*i)//scale,966//scale))

    for i in range(len(Bcount)):
        text1 = myfont.render(str(Bcount[i]), True, (0, 0, 0))
        screen.blit(text1,((403+66*i)//scale,46//scale))

def drawMove(screen, moveset, SQ_size):
    for i in moveset:
        p.draw.rect(screen, colors[3], p.rect.Rect(i[1]*SQ_size+xoffset, i[0]*SQ_size+yoffset, SQ_size, SQ_size))


def drawWin(screen, GO):

    if not GO[0] and GO[1]:
        GameOVerText = myfont.render("Game Over, Black Wins", True, (0, 0, 0))
        p.draw.rect(screen, colors[2], p.rect.Rect(10//scale, 10//scale,  350//scale, 66//scale), 2)
        screen.blit(GameOVerText, (20//scale, 10//scale))


    elif GO[0] and not GO[1]:
        GameOVerText = myfont.render("Game Over, White Wins", True, (0, 0, 0))
        p.draw.rect(screen, colors[2], p.rect.Rect(10//scale, 10//scale,  350//scale, 66//scale), 2)
        screen.blit(GameOVerText, (20//scale, 10//scale))
    ret = myfont.render("press backspace to return to menu or press esc to quit", True, (0, 0, 0))
    screen.blit(ret, (500//scale, 10//scale))



def drawTimer(screen, gs):
    p.draw.rect(screen, colors[2], p.rect.Rect(938//scale, 900//scale,  170//scale, 66//scale), 2)
    p.draw.rect(screen, colors[2], p.rect.Rect(938//scale, 966//scale,  170//scale, 66//scale), 2)

    p.draw.rect(screen, colors[2], p.rect.Rect(938//scale, 46//scale,  170//scale, 66//scale), 2)
    p.draw.rect(screen, colors[2], p.rect.Rect(938//scale, 112//scale,  170//scale, 66//scale), 2)

    Wtext = myfont.render("White Time", True, (0, 0, 0))
    Btext = myfont.render("Black Time", True, (0, 0, 0))

    screen.blit(Wtext, (938//scale, 906//scale))
    screen.blit(Btext, (938//scale, 60//scale))
    Wtime = myfont.render(str(round(gs.Wtimer, 3)), True, (0, 0, 0))
    screen.blit(Wtime, (938//scale, 974//scale))
    Btime = myfont.render(str(round(gs.Btimer, 3)), True, (0, 0, 0))
    screen.blit(Btime, (938//scale, 120//scale))


def setup():

    dimension = int(input("Enter dimension: "))
    timer = int(input("Enter times: "))
    WTM= bool(input("white first?"))
    return [dimension, timer, WTM]


def gameOver(gs, Bmoves, Wmoves):
    gameover = False
    WCM = True
    BCM = True


    g = copy.deepcopy(gs)
    Bmoves1 = g.getMoves("Black")
    C = g.checkCheck("White", Bmoves1)
    if len(C) > 0:
        Wmoves = gs.getMoves("White")
        Bmoves = gs.getMoves("Black")
        WCM = gs.checkMate(copy.deepcopy(Wmoves), copy.deepcopy(Bmoves), C, "White", "Black")
        if not WCM:
            gameover = True


    g = copy.deepcopy(gs)
    Wmoves1 = g.getMoves("White")
    C = g.checkCheck("Black", Wmoves1)
    if len(C) > 0:
        Wmoves = gs.getMoves("White")
        Bmoves = gs.getMoves("Black")
        BCM = gs.checkMate(copy.deepcopy(Bmoves), copy.deepcopy(Wmoves), C, "Black", "White")
        if not BCM:
            gameover = True
    return [WCM, BCM, gameover]


def main():

    #S = setup()
    S = Menu.main()
    if S == False:
        running = False
    else:
        #os.environ['SDL_VIDEO_CENTERED'] = '1'
        screen = p.display.set_mode((WIDTH, HEIGHT), p.FULLSCREEN)

        clock = p.time.Clock()
        screen.fill(p.color.Color("white"))
        MH = S[4]
        COLOR = [S[1], S[0]]
        SQ_size = (594//int(S[2][0]))//scale

        gs = shogiEngine1.GameState(S[2], True, S[5])
        start_ticks=p.time.get_ticks() #starter tick


        load_Images(SQ_size, S[3])
        running = True

        sqSelected = () #No square selected, keep track of last click of the user (tuple)
        playerClicks = [] #keep track of player clicks (2 tuples: [(6,4)])
        Wchecks = []
        Bchecks = []
        GO = [True, True, False]
        Wmoves = gs.getMoves("White")
        Bmoves = gs.getMoves("Black")
        Dfound= False
        quit = False
        movestack = []

    while running:
        if gs.whiteToMove and not GO[2] and gs.timer != False:
            gs.Wtimer = gs.Wtimer -1/15

        elif not gs.whiteToMove and not GO[2] and gs.timer != False:
            gs.Btimer = gs.Btimer -1/15

        if GO[2] or gs.Wtimer <= 0 or gs.Btimer <= 0:

            running = False


        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                quit = True
            elif  e.type == p.KEYDOWN:
                if e.key == p.K_ESCAPE:
                    running = False
                    quit = True
            elif e.type == p.MOUSEBUTTONDOWN:

                location = p.mouse.get_pos() #x,y location of mouse
                col = (location[0] -xoffset)//SQ_size
                row = (location[1] - yoffset)//SQ_size

                if location[1] >= 900//scale and location[1] <= 966//scale and gs.whiteToMove or location[1] >= 112//scale and location[1] <= 178//scale and not gs.whiteToMove:

                    T= (location[0]-(403//scale))//(66//scale)

                    switch = {
                        0: "Lance",
                        1: "Night",
                        2: "Silver General",
                        3: "Gold General",
                        4: "Bishop",
                        5: "Rook",
                        6: "Pawn"
                    }
                    if gs.whiteToMove:
                        for i in gs.Wcapture:

                            if i.Name == switch.get(T):

                                F = i
                                Dfound = True
                    elif not gs.whiteToMove:
                        for i in gs.Bcapture:

                            if i.Name == switch.get(T):
                                F = i
                                Dfound = True

                if gs.isInBoard(row, col):
                    if sqSelected == (row, col): #check if the user clicks the same square
                        sqSelected = () #deselect
                        playerClicks = [] #clear player clicks

                    elif gs.board[row][col].Name == "Null" and len(sqSelected) == 0 and not Dfound:
                        sqSelected = () #deselect
                        playerClicks = [] #clear player clicks

                    elif gs.board[row][col].Color == "Black" and gs.whiteToMove == True and len(sqSelected)<1 or gs.board[row][col].Color == "White" and gs.whiteToMove == False and len(sqSelected)<1:
                        sqSelected = () #deselect
                        playerClicks = [] #clear player clicks

                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) #append for both 1st and 2nd clicks

                    if len(playerClicks) == 2:

                        move = shogiEngine1.Move(playerClicks[0], playerClicks[1], copy.deepcopy(gs.board), copy.deepcopy(gs.whiteToMove), Wmoves, Bmoves, copy.deepcopy(gs.Wcapture), copy.deepcopy(gs.Bcapture), copy.deepcopy(gs.Wtimer), copy.deepcopy(gs.Btimer))
                        sqSelected = () #deselect
                        playerClicks = [] #clear player clicks

                        if gs.whiteToMove:
                            Valid = gs.validateMove(Wmoves, move)
                            if Valid == True:
                                g = copy.deepcopy(gs)
                                g.makeMove(copy.deepcopy(move))
                                Bmoves1 = g.getMoves("Black")
                                C = g.checkCheck("White", Bmoves1)
                        else:
                            Valid = gs.validateMove(Bmoves, move)
                            if Valid == True:
                                g = copy.deepcopy(gs)
                                g.makeMove(copy.deepcopy(move))
                                Wmoves1 = g.getMoves("White")
                                C = g.checkCheck("Black", Wmoves1)


                        if Valid == True and len(C) == 0:
                            movestack = []
                            move.pieceMoved.Promotable = move.checkPromote(move.pieceMoved)
                            gs.makeMove(move)
                            gs.moveLog.append(move) #log move
                            gs.whiteToMove = not gs.whiteToMove
                            Wmoves = gs.getMoves("White")
                            Bmoves = gs.getMoves("Black")
                            Wchecks = gs.checkCheck("White", Bmoves)
                            Bchecks = gs.checkCheck("Black", Wmoves)
                            move.pieceMoved.Promotable = move.checkPromote(move.pieceMoved)

                            if move.pieceMoved.Promotable == True and move.pieceMoved.Promotion != True:
                                drawPromotion(screen)
                                p.display.update()
                                #print promote button
                                Zrunning = True
                                while Zrunning:
                                    for e in p.event.get():
                                        if e.type == p.QUIT:
                                            running = False
                                            Zrunning = False

                                        if e.type == p.MOUSEBUTTONDOWN:
                                            location = p.mouse.get_pos() #x,y location of mouse
                                            if location[0] >= 1000//scale and location[0] <= (1000+156)//scale and location[1] >= 1000//scale and location[1] <= (1000 + 156)//scale:
                                                move.pieceMoved.Promotion = True
                                                Zrunning = False
                                            elif location[0] >= (1000+156)//scale and location[0] <= (1000+ 2*156)//scale and location[1] >= 1000//scale and location[1] <= (1000 + 156)//scale:
                                                Zrunning = False
                                                pass

                        else:
                            sqSelected = () #deselect
                            playerClicks = [] #clear player clicks

                        GO = gameOver(gs, Bmoves, Wmoves)

                    elif len(playerClicks) == 1 and Dfound == True:
                        if F.Name == "Pawn" or F.Name == "Night" or F.Name == "Lance":
                            if row == 0 and gs.whiteToMove or row == 8 and not gs.whiteToMove:

                                sqSelected = () #deselect
                                playerClicks = [] #clear player clicks
                                Dfound = False
                        if F.Name == "Pawn" and not F.Promotion:
                            for i in range(gs.dimensionsx):
                                if gs.board[i][col].Name == F.Name and gs.board[i][col].Color == F.Color:

                                    sqSelected = () #deselect
                                    playerClicks = [] #clear player clicks
                                    Dfound = False
                                    break

                        if gs.board[row][col].Name == "Null":

                            movestack = []

                            if gs.whiteToMove:
                                F.Color = "White"
                                F.Direction = 1
                                F.Position = (row, col)
                                F.Promotable = False
                                F.Promotion = False
                                gs.board[row][col] = F
                                #gs.board[row][col] = FPiece.Pawn("White", F.Name, (row, col), 1)
                                c = 0
                                for i in gs.Wcapture:
                                    if i.Name == F.Name:
                                        gs.Wcapture.pop(c)
                                        break
                                    c = c + 1



                            elif not gs.whiteToMove:
                                F.Color = "Black"
                                F.Direction = -1
                                F.Position = (row, col)
                                F.Promotable = False
                                F.Promotion = False
                                gs.board[row][col] = F
                                c = 0
                                for i in gs.Bcapture:
                                    if i.Name == F.Name:
                                        gs.Bcapture.pop(c)
                                        break
                                    c = c + 1
                            Dfound = False

                            gs.whiteToMove = not gs.whiteToMove
                        #add code to check if move causes checkmate
                        sqSelected = () #deselect
                        playerClicks = [] #clear player clicks

                        GO = gameOver(gs, Bmoves, Wmoves)

                if location[0] >= 1506//scale and location[0] <=1662//scale and location[1] >= 82//scale and location[1] <= 130:

                    if len(gs.moveLog) != 0:
                        t = gs.moveLog.pop()
                        gs.board = t.boardHis
                        gs.whiteToMove = t.whiteMove
                        gs.Wcapture = t.boardCapW
                        gs.Bcapture = t.boardCapB
                        gs.Wtimer = t.timeW
                        gs.Btimer = t.timeB
                        Wmoves = gs.getMoves("White")
                        Bmoves = gs.getMoves("Black")
                        sqSelected = () #deselect
                        playerClicks = [] #clear player clicks
                        GO = gameOver(gs, Bmoves, Wmoves)


        drawGameState(screen, gs, playerClicks, Wmoves, Bmoves, GO, MH, COLOR, SQ_size)
        clock.tick(MAX_FPS)
        p.display.flip()

    if not quit:
        Erunning = True
        while Erunning:
            drawGameState(screen, gs, playerClicks, Wmoves, Bmoves, GO, MH, COLOR, SQ_size)
            clock.tick(MAX_FPS)
            p.display.flip()
            for e in p.event.get():
                if e.type == p.QUIT:
                    Erunning = False
                    p.display.quit()
                    return False
                if e.type == p.KEYDOWN:
                    if e.key == p.K_BACKSPACE:
                        Erunning = False
                        p.display.quit()
                        return True
                    elif e.key == p.K_ESCAPE:
                        Erunning = False
                        p.display.quit()
                        return False


if __name__ == "__main__":
    running = True
    while running:
        running = main()
