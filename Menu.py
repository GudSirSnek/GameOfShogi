import pygame as p
import webbrowser
height = 1057 #defines the board resolution
width = 1920
x_offset = 459
y_offset = 243
scale = 2
MAX_FPS = 15
HEIGHT = height//scale
WIDTH = width//scale
colors = [p.color.Color("white"), p.color.Color("gray"), p.color.Color("black"), p.color.Color("green"), p.color.Color("red"), p.color.Color("blue")]



p.font.init()

myfont = p.font.SysFont('Comic Sans MS', 100//scale)

def Main(screen, clock):
    #top center has title
    # under "play"- goes to game setup
    # under that, third party resources
    screen.fill(p.color.Color("white"))
    Title = myfont.render("SHOGI", True, (0, 0, 0))
    Play = myfont.render("PLAY", True, (0, 0, 0))
    Help = myfont.render("HELP", True, (0, 0, 0))


    p.draw.rect(screen, colors[2], p.rect.Rect(780//scale, 50//scale, 380//scale, 100//scale), 2)
    p.draw.rect(screen, colors[2], p.rect.Rect(840//scale, 450//scale, 260//scale, 100//scale), 2)
    p.draw.rect(screen, colors[2], p.rect.Rect(840//scale, 850//scale, 260//scale, 100//scale), 2)
    screen.blit(Title, (790//scale, 30//scale))
    screen.blit(Play, (850//scale, 430//scale))
    screen.blit(Help, (850//scale, 830//scale))

    clock.tick(15)
    p.display.flip()


def Options(screen, Color1, Color2, size, type, MH, Timer, clock):
    screen.fill(p.color.Color("white"))
    Title = myfont.render("SHOGI", True, (0, 0, 0))
    Bcolor1 = myfont.render("BOARD COLOUR 1", True, (0, 0, 0))
    Bcolor2 = myfont.render("BOARD COLOUR 2", True, (0, 0, 0))
    Bsize = myfont.render("BOARD SIZE", True, (0, 0, 0))
    Ptype = myfont.render("PIECE TYPE", True, (0, 0, 0))
    mh =  myfont.render("MOVE HIGHLIGHTING", True, (0, 0, 0))
    back = myfont.render("BACK", True, (0, 0, 0))
    Time = myfont.render("TIME", True, (0, 0, 0))
    Play = myfont.render("PLAY", True, (0, 0, 0))

    p.draw.rect(screen, colors[2], p.rect.Rect(1500//scale, 10//scale, 200//scale, 200//scale), 4)
    p.draw.rect(screen, colors[2], p.rect.Rect(1500//scale, 210//scale, 200//scale, 200//scale), 4)
    p.draw.rect(screen, colors[2], p.rect.Rect(1700//scale, 10//scale, 200//scale, 200//scale), 4)
    p.draw.rect(screen, colors[2], p.rect.Rect(1700//scale, 210//scale, 200//scale, 200//scale), 4)
    p.draw.rect(screen, Color1, p.rect.Rect(1500//scale, 10//scale, 200//scale, 200//scale))
    p.draw.rect(screen, Color2, p.rect.Rect(1500//scale, 210//scale, 200//scale, 200//scale))
    p.draw.rect(screen, Color2, p.rect.Rect(1700//scale, 10//scale, 200//scale, 200//scale))
    p.draw.rect(screen, Color1, p.rect.Rect(1700//scale, 210//scale, 200//scale, 200//scale))

    screen.blit(Title, (790//scale, 30//scale))
    p.draw.rect(screen, colors[2], p.rect.Rect(780//scale, 50//scale, 380//scale, 100//scale), 2)

    screen.blit(Bcolor1, (60//scale, 200//scale))
    p.draw.rect(screen, colors[2], p.rect.Rect(50//scale, 230//scale, 1150//scale, 100//scale), 2)

    screen.blit(Bcolor2, (60//scale, 300//scale))
    p.draw.rect(screen, colors[2], p.rect.Rect(50//scale, 330//scale, 1150//scale, 100//scale), 2)

    screen.blit(Bsize, (60//scale, 400//scale))
    p.draw.rect(screen, colors[2], p.rect.Rect(50//scale, 430//scale, 1150//scale, 100//scale), 2)

    screen.blit(Ptype, (60//scale, 500//scale))
    p.draw.rect(screen, colors[2], p.rect.Rect(50//scale, 530//scale, 1150//scale, 100//scale), 2)

    screen.blit(mh, (60//scale, 600//scale))
    p.draw.rect(screen, colors[2], p.rect.Rect(50//scale, 630//scale, 1150//scale, 100//scale), 2)

    screen.blit(Time, (60//scale, 700//scale))
    p.draw.rect(screen, colors[2], p.rect.Rect(50//scale, 730//scale, 1150//scale, 100//scale), 2)


    p.draw.rect(screen, colors[2], p.rect.Rect(1200//scale, 230//scale, 100//scale, 100//scale), 4)
    p.draw.rect(screen, colors[2], p.rect.Rect(1200//scale, 330//scale, 100//scale, 100//scale), 4)
    p.draw.rect(screen, Color1, p.rect.Rect(1200//scale, 230//scale, 100//scale, 100//scale))
    p.draw.rect(screen, Color2, p.rect.Rect(1200//scale, 330//scale, 100//scale, 100//scale))




    SIZE = myfont.render(size, True, (0, 0, 0))
    screen.blit(SIZE, (1200//scale, 400//scale))
    p.draw.rect(screen, colors[2], p.rect.Rect(1200//scale, 430//scale, 250//scale, 100//scale), 2)


    if type == 1:
        Piece = myfont.render("ENG", True, (0, 0, 0))
    else:
        Piece = myfont.render("JAP", True, (0, 0, 0))



    screen.blit(Piece, (1200//scale, 500//scale))
    p.draw.rect(screen, colors[2], p.rect.Rect(1200//scale, 530//scale, 250//scale, 100//scale), 2)


    Mh = myfont.render(str(MH), True, (0, 0, 0))
    screen.blit(Mh, (1200//scale, 600//scale))
    p.draw.rect(screen, colors[2], p.rect.Rect(1200//scale, 630//scale, 250//scale, 100//scale), 2)

    Timer = myfont.render(str(Timer), True, (0, 0, 0))
    screen.blit(Timer, (1200//scale, 700//scale))
    p.draw.rect(screen, colors[2], p.rect.Rect(1200//scale, 730//scale, 250//scale, 100//scale), 2)


    screen.blit(back, (50//scale, 20//scale))
    p.draw.rect(screen, colors[2], p.rect.Rect(50//scale, 50//scale, 270//scale, 100//scale), 2)

    screen.blit(Play, (1460//scale, 820//scale))
    p.draw.rect(screen, colors[2], p.rect.Rect(1450//scale, 850//scale, 270//scale, 100//scale), 2)



    clock.tick(15)
    p.display.flip()

def load_Images():
    pieces = ["BL", "BN", "BS", "BG", "BK", "BB", "BR", "BP", "WL", "WN", "WS", "WG", "WK", "WB","WR", "WP"]

    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png") , (SQ_size, SQ_size))

    if type == 0:
        type = "Traditional"
    else:
        type = "Translated"


def main():
    running = True
    clock = p.time.Clock()
    p.display.init()
    p.display.set_caption('test caption')
    screen = p.display.set_mode((WIDTH, HEIGHT))




    Color1 = colors[0]
    Color2 = colors[2]
    sizeL = ["5x4", "5x5","9x9"]
    size = "9x9"
    type = 0
    MH = True
    Timer = 60
    timeL = [False, 60, 120, 180, 240, 300, 360]
    RET= True
    while running:
        Main(screen, clock)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                RET = False
            if e.type == p.KEYDOWN:
                if e.key == p.K_ESCAPE:
                    running = False
                    RET = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                if location[0] >= 840//scale and location[0] <= 1100//scale:

                    if location[1] >= 450//scale and location[1] <= 550//scale:

                        running1 = True
                        while running1:

                            Options(screen, Color1, Color2, size, type, MH, Timer, clock)
                            for e in p.event.get():
                                if e.type == p.QUIT:
                                    running = False
                                    running1 = False
                                    RET = False
                                elif e.type == p.MOUSEBUTTONDOWN:
                                    location = p.mouse.get_pos()
                                    if location[0] >= 50//scale and location[0] <= 1200//scale:
                                        if location[1] >= 230//scale and location[1] <= 330//scale:
                                            T = 0
                                            for i in range(len(colors)):
                                                if colors[i] == Color1:
                                                    T = i
                                            h = (T+1)%6
                                            Color1 = colors[h]
                                        elif location[1] >= 330//scale and location[1] <= 430//scale:
                                            T = 0
                                            for i in range(len(colors)):
                                                if colors[i] == Color2:
                                                    T = i
                                            h = (T+1)%6
                                            Color2 = colors[h]
                                        elif location[1] >= 430//scale and location[1] <= 530//scale:


                                            T = 0
                                            for i in range(len(sizeL)):
                                                if sizeL[i] == size:
                                                    T = i
                                            h = (T+1)%3
                                            size = sizeL[h]

                                        elif location[1] >= 530//scale and location[1] <= 630//scale:


                                            type = (type + 1)%2


                                        elif location[1] >= 630//scale and location[1] <= 730//scale:

                                            MH = not MH

                                        elif location[1] >= 730//scale and location[1] <= 830//scale:

                                            T = 0
                                            for i in range(len(timeL)):
                                                if timeL[i] == Timer:
                                                    T = i
                                            h = (T+1)%7
                                            Timer = timeL[h]


                                    if location[0] >= 50//scale and location[0] <= 320//scale:

                                        if location[1] >= 50//scale and location[1] <= 150//scale:
                                            running1 = False

                                elif location[0] >= 1450//scale and location[0] <= 1720//scale:
                                    if location[1] >= 850//scale and location[1] <= 1120//scale:
                                        running1 = False
                                        running = False




                    elif location[1] >= 850//scale and location[1] <= 950//scale:

                        webbrowser.open('https://www.shogi.cz/en/rules', new=2, autoraise=True)
    if RET:
        return [Color1, Color2, size, type, MH, Timer]
    else:
        return RET

if __name__ == "__main__":
    main()
