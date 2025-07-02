import turtle
import math
import random
from abc import ABC
import ggwave
import pyaudio
import threading
import os
import numpy as np
import tkinter as tk
try:
    from smaz import compress, decompress
except:
    import brotli
finally: 
    import lz4

speech_window = None
def init_speech_window():
    global speech_window, speech_text
    speech_window = tk.Toplevel()
    speech_window.title("Shape Speech Translator")
    speech_text = tk.Text(speech_window, height=20, width=60)
    speech_text.pack()


class Speech:
    def __init__(self,phrase,voice):
        self.phrase = phrase
        self.voice = voice
    def playback(self):
        p = pyaudio.PyAudio()
        self.waveform = ggwave.encode(self.phrase, self.voice, volume = 20)
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, output=True, frames_per_buffer=4096)
        stream.write(self.waveform, len(self.waveform)//4)
        stream.stop_stream()
        stream.close()

        p.terminate()


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
    def __init__(self,name,sides,length,X,Y,color,heading,voice,line_file,screen,colorlist,minsize=minsize): #pass screen from Euclydia
        super().__init__()
        self.X = X
        self.Y = Y
        self.name = name
        self.sides = sides
        self.length = length
        self.angle = heading
        self.voice = voice
        self.outline = self.calcpoints()
        self.screen = screen
        self.bounds = self.screen.window_width(), self.screen.window_height()
        self.lines = line_file
        self.id_num = Shape.id_num
        Shape.registry.update({self.id_num:self})
        self.turtle_setup(minsize,color,colorlist)
        self.start_life()
        Shape.id_num += 1

    def turtle_setup(self,minsize,color,colorlist):
        self.screen.register_shape(str(self.id_num), tuple(self.outline))
        self.shape(str(self.id_num))
        self.setheading(self.angle)
        self.color(self.set_color(color,colorlist))
        scale = max(math.sqrt(self.get_area()) / 10, minsize)
        self.shapesize(scale)
        self.penup()


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
        x, y = self.pos()
        width, height = self.bounds
        # Slight random turn every so often (5% chance)
        if random.random() < 0.05:
            self.setheading(self.heading() + random.uniform(-10, 10))

        # Constant slow forward motion
        self.forward(3)

        # Handle collision with other shapes
        self.collisions()

        # ✅ Wrap horizontally (Pac-Man logic)
        if x < -width / 2:
            self.hideturtle()
            self.setx(width / 2)
            self.showturtle()
        elif x > width / 2:
            self.hideturtle()
            self.setx(-width / 2)
            self.showturtle()

            # Recalculate y after forward + collision
        _, y = self.pos()
        if y > height / 2:
            self.sety(height / 2)
            self.setheading((self.heading() + 180) % 360)
        elif y < -height / 2:
            self.sety(-height / 2)
            self.setheading((self.heading() + 180) % 360)

    def start_life(self):
        def tick():
            try:
                self.move()
                self.screen.ontimer(tick, 500 + int(random.random() * 500))
                if random.randint(0, 500) == 5:
                    self.say()
            except turtle.Terminator:
                print(f"[Turtle Error] Shape {self.name} was terminated.")
        tick()

    def collisions(self, min_dist=20):
        x1, y1 = self.pos()
        for key, other in Shape.registry.items():
            if other is self:
                continue
            x2, y2 = other.pos()
            distance = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
            if distance < min_dist:
                # Bounce away from other shape
                angle = self.towards(x2, y2)
                self.setheading((angle + 180) % 360)
                self.forward(5)



    def read(self):
        try:
            with open(self.lines, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
                if not lines:
                    raise ValueError("Phrase file is empty.")
                return lines
        except Exception as e:
            #print(f"[ERROR] Could not find phrase file: {self.lines}")
            return ["WHY DID YOU DO IT?"]



    def say(self):
        try:
            phrase = random.choice(self.read())
        except Exception as e:
            print(f"[Phrase Error] {e}")
            phrase = "WHY DID YOU DO IT?"

        voice_map = {
            "FC": 2,
            "FA": 1,
            "MC": 8,
            "MA": 7,
            "SC": 0,
            "EU": 6,
        }

        voice_id = voice_map.get(self.voice, 8)  # Default to 'MA' if unknown
        speech = Speech(phrase,voice_id)
        if speech_window and speech_window.winfo_exists():
            speech_text.insert(tk.END, f"{self.name} says: {phrase}\n")
            speech_text.see(tk.END)

        threading.Thread(target=speech.playback, daemon=True).start()

        