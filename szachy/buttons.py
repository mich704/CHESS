from graphics import *

class Button():
    disabled_color = color_rgb(116, 100, 116)

    def __init__(self, win, c1, c2, size, m, start_x, start_y,):
        self.win = win

        self.c1 = c1
        self.c2 = c2
        self.is_active=False

        self.size = size
        self.m = m
        self.start_x = start_x
        self.start_y = start_y
    
    def buttons_type(self,type):
        txt=Text(Point(self.start_x+self.m/2+40,self.start_y-15),type)
        txt.setFace("courier")
        txt.setTextColor("black")
        txt.draw(self.win)


    def deactivate(self):
        self.is_active=False
        self.button_t.setFill(Button.disabled_color)

    def activate(self):
        self.is_active=True
        self.button_t.setFill(self.c1)


    def draw_button(self):
        self.button.draw(self.win)
        self.button_t.draw(self.win)

    def button_parameters(self):
        self.button.setOutline(self.c1)
        self.button.setWidth(3)
        self.button.setFill(self.c2)
        self.button_t.setFill(Button.disabled_color)
        self.button_t.setOutline(self.c2)

    def clicked(self, click_x, click_y):
        if (
            int(click_x) in range(int(self.start_x), int(self.end_x)) and
            int(click_y) in range(int(self.start_y), int(self.end_y)) 
        ):
            return True
        return False
        




class prevButton(Button):
    def __init__(self, win, c1, c2, size, m, start_x, start_y):
        super().__init__(win, c1, c2, size, m, start_x, start_y)
        
        self.prev_p1 = Point(self.start_x, self.start_y)
        self.prev_p2 = Point(self.start_x + self.size*2, self.start_y + self.size*2)

        self.end_x=self.start_x + self.size*2
        self.end_y= self.start_y + self.size*2
        
        self.button = Rectangle(self.prev_p1, self.prev_p2)

        self.button_t = Polygon(
            Point(self.start_x + self.m, self.start_y + self.size ),
            Point(self.start_x + self.size*2 - self.m, self.start_y + self.size*2 - self.m),
            Point(self.start_x + self.size*2 - self.m, self.start_y + self.m))

        self.button_parameters()
        self.buttons_type("REWIND")
        


class nextButton(Button):
    def __init__(self, win, c1, c2, size, m, start_x, start_y):
        super().__init__(win, c1, c2, size, m, start_x, start_y)


        self.next_p1 = Point(self.start_x + self.size*2 , self.start_y)
        self.next_p2 = Point(self.start_x + self.size*4, self.start_y + self.size*2)

        self.end_x = self.start_x + self.size*4
        self.end_y = self.start_y + self.size*2

        
        self.button = Rectangle(self.next_p1, self.next_p2)

        self.button_t = Polygon(
            Point(self.start_x + self.size*3.5 + self.m, self.start_y + self.size ),
            Point(self.start_x + self.size*2.5 - self.m, self.start_y + self.size*2 - self.m),
            Point(self.start_x + self.size*2.5 - self.m, self.start_y + self.m))

        self.button_parameters()

class RestorePosition(Button):
    def __init__(self, win, c1, c2, m, start_x, end_x, start_y, end_y, txt):
        self.win = win
        self.is_active = False

        self.start_x = start_x
        self.end_x = end_x
        self.start_y = start_y
        self.end_y = end_y

        self.button = Rectangle(Point(self.start_x, self.start_y), Point(self.end_x, self.end_y))

        self.button.setOutline(c2)
        self.button.setWidth(m)
        self.button.setFill(c1)

        self.txt = Text(Point((self.start_x + self.end_x) / 2, (self.start_y + self.end_y) / 2), txt)
        self.txt.setSize(8)
        self.txt.setStyle("bold")
        self.txt.setFace("courier")


        

    def draw_button(self):
        if not self.is_active:
            self.button.draw(self.win)
            self.txt.draw(self.win)
            self.is_active = True

    def undraw_button(self):
        if self.is_active:
            self.button.undraw()
            self.txt.undraw()
            self.is_active = False