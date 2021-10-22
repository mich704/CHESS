from graphics import *
class Move(object):
    standard_color = 'grey'
    takes_color = color_rgb(225, 78, 102)

    """
        Avalible types are:
            None (standard move)
            'takes'
            'castle'
            'en_passant'
    """

    def __init__(self, y, x, win, type = None, castle_way = None):
        self.y = y
        self.x = x
        self.win = win
        self.type = type
        self.castle_way = castle_way

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        if type == None or type == 'castle':
            self.img = Circle(Point(self.x * 100 + 50,self.y * 100 + 50), 15)
            self.img.setFill(Move.standard_color)
            self.img.setOutline(Move.standard_color)


        elif type == 'takes' or type == 'en_passant':
            self.img = Circle(Point(self.x * 100 + 50,self.y * 100 + 50), 12)
            self.img.setFill(Move.takes_color)
            self.img.setOutline(Move.takes_color)

        else:
            raise ValueError("Unknow move type")

        self._type = type


        

    def draw_move(self):
        self.img.draw(self.win)

    def undraw_move(self):
        if self.img != None:
            self.img.undraw()
        else:
            raise ValueError("There is no image to undraw")

    def __str__(self):
        return str(self.y) + " " + str(self.x)