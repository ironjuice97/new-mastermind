import turtle
from Point import Point

MARBLE_RADIUS = 15

class Marble:
    def __init__(self, position, color, size=MARBLE_RADIUS):
        self.pen = turtle.Turtle()
        self.color = color
        self.position = position  # position is an instance of Point
        self.visible = False
        self.is_empty = True
        self.pen.hideturtle()
        self.size = size
        self.pen.speed(0)  # set to fastest drawing

    def set_color(self, color):
        self.color = color
        self.is_empty = False

    def draw(self):
        self.pen.up()
        self.pen.goto(self.position.x, self.position.y)  # Corrected access to x and y
        self.visible = True
        self.is_empty = False
        self.pen.down()
        self.pen.fillcolor(self.color)
        self.pen.begin_fill()
        self.pen.circle(self.size)
        self.pen.end_fill()

    def draw_empty(self):
        self.erase()
        self.pen.up()
        self.pen.goto(self.position.x, self.position.y)  # Corrected access to x and y
        self.visible = True
        self.is_empty = True
        self.pen.down()
        self.pen.circle(self.size)
        
    def erase(self):
        self.visible = False
        self.pen.clear()

    def get_color(self):
        return self.color

    def clicked_in_region(self, x, y):
        if abs(x - self.position.x) <= self.size * 2 and \
           abs(y - self.position.y) <= self.size * 2:  # Corrected access to x and y
            return True
        return False
    
    def move(self, dx, dy):
        """Move the marble by dx and dy."""
        self.position.x += dx
        self.position.y += dy
        if self.visible:
            if self.is_empty:
                self.draw_empty()
            else:
                self.draw()