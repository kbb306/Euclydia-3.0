import turtle
import math
import random
from abc import ABC
class Color(ABC):
    def __init__(self,colorlist):
          self.color = type(self)
          colorlist.append(self.color)
    def report_color(self):
         return self.color
          
    
     

class Red(Color):
     def __init__(self,colorlist):
          super().__init__(colorlist)
     
class Green(Color):
     def __init__(self,colorlist):
        super().__init__(colorlist)
         

class Blue(Color):
     def __init__(self,colorlist):
          super().__init__(colorlist)
     
          
class Yellow(Color):
     def __init__(self,colorlist):
          super().__init__(colorlist)
         
     
class Purple(Color):
     def __init__(self,colorlist):
          super().__init__(colorlist)

class Black(Color):
     def __init__(self, colorlist):
          super().__init__(colorlist)

class Brown(Color):
    def __init__(self, colorlist):
        super().__init__(colorlist)

class Orange(Color):
    def __init__(self, colorlist):
        super().__init__(colorlist)

class Pink(Color):
    def __init__(self, colorlist):
        super().__init__(colorlist)

class Gray(Color):
    def __init__(self, colorlist):
        super().__init__(colorlist)

class Lime(Color):
    def __init__(self, colorlist):
        super().__init__(colorlist)

class SkyBlue(Color):
    def __init__(self, colorlist):
        super().__init__(colorlist)

class Shape(turtle.Turtle):
    id_num = 0
    registry = {}  # shared across all Shape instances
    def __init__(self,X,Y,heading,sides,length,gender,line_file,screen): #pass screen from Euclydia
        self.X = X
        self.Y = Y
        self.heading = heading
        self.sides = sides
        self.length = length
        self.gender = gender
        self.outline = self.calcpoints()
        self.bounds = self.screen.window_width, self.screen.window_height
        self.screen = screen
        self.id_num = Shape.id_num
        Shape.registry.update({self.id_num:self})
        self.turtle_setup(self)
        self.start_life()
        Shape.id_num += 1
    def turtle_setup(self):

        self.color(str(self.set_color()))
        self.heading(self.heading)
        self.screen.register_shape(self.id_num,self.outline) 
        self.shape(self.id_num)

    def delete(self):
        """Remove the shape from the screen and from the registry."""
        # Hide and clear the turtle
        self.hideturtle()
        self.clear()

        # Remove from the registry if stored there
        if hasattr(self.__class__, "registry"):
            to_delete = None
            for key, value in self.__class__.registry.items():
                if value is self:
                    to_delete = key
                    break
            if to_delete:
                del self.__class__.registry[to_delete]

        # Optionally, remove from screen updates
        self._destroy()  # Private call to ensure the turtle object is invalidated


    def voice_setup(self):
        pass

    def get_center(self):
       self.center = (self.centerX, self.centerY)
       return self.center
    
    def get_X(self):
         return self.centerX
    
    def get_Y(self):
         return self.centerY
    
    def set_X(self, X):
         self.centerX = float(X)
         self.xcor(self.centerX)

    def set_Y(self, Y):
         self.centerY = float(Y)


    def get_area(self):
         apothem = self.length/(2 * math.tan(math.radians(180/self.sides)))
         area = (self.sides*self.length*apothem)/2
         return area
    
    def set_color(self, colorlist, color="Black"):
        # Create a list of valid color names
        colorlist_str = [cls.__name__ for cls in colorlist]
        # Loop until a valid color is chosen
        while color not in colorlist_str:
            print(f"Invalid color. Available options: {', '.join(colorlist_str)}")
            color = input("Select a color: ")
        # Find the corresponding class and create a new instance
        colorclass = [cls for cls in colorlist if cls.__name__ == color][0]
        self.color = colorclass
        #print(f"Color set to {color}.")
        return self.color.__name__
    
    def sayname(self):
         return self.id_num
    
    def set_heading(self,heading):
         self.heading = int(heading)

    def get_heading(self):
         return self.heading
             
    def calcpoints(self):
         angle = math.radians(360/self.sides)
         outline = []
         i = 0
         while i <= self.sides:
             point = (math.cos(angle*i),math.sin(angle*i))
             outline.append(point)
             i+=1
         return outline

    def pathfinding(self):
        if random.random() < 0.3:
            self.left(random.uniform(-30, 30))  # Random heading jitter
        if random.random() < 0.6:
            self.forward(random.uniform(5, 15))
        self.check_collisions()

        x, y = self.pos()
        width, height = self.bounds
        if abs(x) > width / 2 or abs(y) > height / 2:
            self.setheading(self.t.heading() + 180)

    def start_life(self):
        def tick():
            self.move()
            self.screen.ontimer(tick, 100 + int(random.random() * 200))
        tick()

    def collisions(self,min_dist=20):
        x1, y1 = self.t.pos()
        for other in Shape.registry.items():
            if other is self:
                continue
        x2, y2 = other.t.pos()
        distance = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
        if distance < min_dist:
                self.left(180)
                self.forward(10)



