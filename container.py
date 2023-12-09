import turtle

class Container:
    def __init__(self):
        self.elements = []
        self.border_turtle = turtle.Turtle()
        self.border_turtle.hideturtle()
        self.border_turtle.speed(0)  # Fastest drawing speed
        self.border_turtle.penup()

    def add_element(self, element):
        self.elements.append(element)

    def set_position(self, x, y):
        for element in self.elements:
            if hasattr(element, 'position') and callable(getattr(element, 'position')):
                current_x, current_y = element.position()
                element.setposition(current_x + x, current_y + y)

    def draw_border(self, x, y, width, height):
        self.border_turtle.penup()
        self.border_turtle.goto(x - width / 2, y - height / 2)
        self.border_turtle.pendown()
        for _ in range(2):
            self.border_turtle.forward(width)
            self.border_turtle.left(90)
            self.border_turtle.forward(height)
            self.border_turtle.left(90)
        self.border_turtle.penup()

    def update_elements(self):
        for element in self.elements:
            if hasattr(element, 'draw') and callable(getattr(element, 'draw')):
                element.draw()
