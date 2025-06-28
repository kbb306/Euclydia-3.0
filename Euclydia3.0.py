import turtle
from Shapesource4 import *
screen = turtle.Screen()
Euclydia = {}
def create():
    print("Wlecome to the shape nursery!")
    print("------------------------------------------------------------")
    print("""   First, where would you like your shape to be placed?""")
    X = int(input("     Enter an X coordinate: "))
    Y = int(input("     Enter a Y coordinate: "))
    heading = int(input("       Which angle should your shape be turned at? (0-360)"))
    print("""   Now, we need its looks.""")
    sides = int(input("""       How many sides?: """))
    length = int(input("""      What length (irregular polygons are unsupported)?: """))
    gender = 0
    while gender not in [1,2]:
        gender = int(input("""      Shapes don't have gender like us, but we do need pronouns.
                                1. She/Her
                                2. He/Him
                       
                                Selection: """))
        
    line_file = input("""   Any special phrases you'd like to define (in a text file in 'Resources')?""")
    if line_file == "":
        line_file = "Resources/phrases.csv"
    else:
        line_file = "".join(["Resources","/", line_file])

    name = input("""    Time to name your shape: """)
    newshape = Shape(X,Y,heading,sides,length)
    print("Rockabye",name+",","please don't you cry....")
    Euclydia.update({name:newshape})
    print("""Your shape is finished!""")

