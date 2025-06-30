import turtle
import math
import random
from abc import ABC
import ggwave
import simpleaudio as sa
import threading
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
    minsize = 6.0
    def __init__(self,X,Y,heading,sides,length,voice,line_file,screen,colorlist): #pass screen from Euclydia
        super().__init__()
        self.X = X
        self.Y = Y
        self.set_heading(heading)
        self.sides = sides
        self.length = length
        self.voice = voice
        self.outline = self.calcpoints()
        self.screen = screen
        self.bounds = self.screen.window_width(), self.screen.window_height()
        self.lines = line_file
        self.id_num = Shape.id_num
        Shape.registry.update({self.id_num:self})
        self.turtle_setup(colorlist)
        self.start_life()
        Shape.id_num += 1

    def turtle_setup(self, colorlist):
        
        chosen_color = self.set_color(self.color,colorlist)
        self.color(chosen_color)
        self.screen.register_shape(str(self.id_num), tuple(self.outline))
        self.shape(str(self.id_num))
        scale = max(math.sqrt(each.get_area()) / 10, minsize)
        self.shapesize(scale)
        self.penup


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
    
    def set_color(self, color, colorlist):
        valid_names = [cls.__name__.lower() for cls in colorlist]
        if color.lower() not in valid_names:
            raise ValueError(f"Invalid color '{color}'")
        self.color_name = color.lower()
        return self.color_name


    
    def sayname(self):
         return self.id_num
    
    def set_heading(self,heading):
         self.heading = int(heading)

    def get_heading(self):
         return self.heading()
             
    def calcpoints(self):
         angle = math.radians(360/self.sides)
         outline = []
         i = 0
         while i <= self.sides:
             point = (math.cos(angle*i),math.sin(angle*i))
             outline.append(point)
             i+=1
         return outline

    def move(self):
        if random.random() < 0.3:
            self.left(random.uniform(-30, 30))  # Random heading jitter
        if random.random() < 0.6:
            self.forward(random.uniform(5, 15))
        self.collisions()

        x, y = self.pos()
        width, height = self.bounds
        if abs(x) > width / 2 or abs(y) > height / 2:
            self.setheading(self.heading() + 180)

    def start_life(self):
        def tick():
            self.move()
            self.screen.ontimer(tick, 100 + int(random.random() * 200))
            if random.randint(0,100) == 5:
                self.say()
        tick()

    def collisions(self,min_dist=20):
        x1, y1 = self.pos()
        for key, other in Shape.registry.items():
            if other is self:
                continue
        x2, y2 = other.pos()
        distance = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
        if distance < min_dist:
                self.left(180)
                self.forward(10)

    def read(self):
        f = open(self.lines)
        script = []
        for each in f:
            script.append(each)
        return script

    def say(self):
        phrase = random.choice(self.read())
        voice = {
            "FC":1,
            "FA":2,
            "MC":7,
            "MA":8,
            "SC":0,
            "EU":6

        }
        def play_audio(voice,phrase):
            waveform = ggwave.encode(phrase, voice, volume=20)
            sa.WaveObject(waveform, 1, 2, 48000).play()

        threading.Thread(target=play_audio(voice[self.voice],phrase), daemon=True).start()
 

    def drive(self):
        pass

