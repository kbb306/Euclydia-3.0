import turtle
from Shapesource4 import * #Psst. Change to Shapesource0 for a surprise!
import csv
screen = turtle.Screen()
init_speech_window()
wn = screen
minsize = 6.0
wn.title("Euclydia")
def get_all_subclasses(cls):
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(get_all_subclasses(subclass))
    return subclasses

def create(Euclydia,screen,colorlist):
    print("Welcome to the shape nursery!")
    print("------------------------------------------------------------")
    print("""   First, where would you like your shape to be placed?""")
    X = int(input("     Enter an X coordinate: "))
    Y = int(input("     Enter a Y coordinate: "))
    heading = int(input("   Which angle should your shape be turned at (0-360)?: "))
    print("""   Now, we need its looks.""")
    sides = int(input("""       How many sides?: """))
    length = int(input("""      What length (irregular polygons are unsupported)?: """))
    gender = 0
    while gender not in ["M","F"]:
        gender = str(input("""  Shapes don't have gender like us, but we do need pronouns.
                                    F. She/Her
                                    M. He/Him
                       
    
                                Selection: """))
    age = 0
    while age not in ["A","C"]:
        age = str(input("""     Is your shape a(n)?
                                    A. Adult
                                    C. Child
                                Input: """))
    voice = "".join([gender.upper(),age.upper()])
        
    color = input("Select a Color (see Shapesource4.py for a list): ")


        
    line_file = input("""   Any special phrases you'd like to define (in a text file in 'Resources')?
                      Input File Name (Blank for default): """)
    if line_file == "":
        line_file = "Resources/phrases.txt"
    else:
        line_file = "".join(["Resources","/", line_file])

    name = input("""    Time to name your shape: """)
    newshape = Shape(name,sides,length,X,Y,color,heading,voice,line_file,screen,colorlist,minsize)
    print("Rockabye",name+",","please don't you cry....")
    Euclydia.update({name:newshape})
    print("""Your shape is finished!""")
    return Euclydia

def load(Euclydia,screen,colorlist):
    with open("Resources/"+input("Enter a filename: ")) as f:
        loader = csv.reader(f)
        poplist = list(loader)
        for each in poplist:
            if not each[8].startswith("Resources/"):
                each[8] = "Resources/" + each[8]

            newshape = Shape(each[0],float(each[1]),float(each[2]),float(each[3]),float(each[4]),each[5],float(each[6]),each[7],each[8],screen,colorlist)
            Euclydia.update({each[0]:newshape})

def save(Euclydia):
    rows = []
    for each in Euclydia.values():
        color_name = each.color.__name__ if hasattr(each.color, "__name__") else "Unknown"
        new = [each.name, each.sides, each.length, each.centerX, each.centerY, color_name, each.heading, each.gender, each.line_file]
        rows.append(new)
    
    # Temporarily stop the turtle window to avoid conflicts
    wn.tracer(0)  # Disable screen updates
    wn.update()   # Ensure the screen reflects the current state
    
    with open(input("Enter a filename: "), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    print("Export complete!")
    
    # Resume turtle graphics
    wn.tracer(1)
    return

def delete(Euclydia):
    print("""Current Popoulation:""")
    for each in list(Euclydia.keys()):
        print(each)
    key = "Why did you do it?"
    while key not in list(Euclydia.keys()):
        key = input("Select a shape: ")
    Euclydia[key].delete()
    del Euclydia[key]
    print("Why did you do it?")
    return Euclydia

def locate(Euclydia):
    print("""Current Population:""")
    for each in list(Euclydia.keys()):
        print(each)
    key = "Why did you do it?"
    while key not in list(Euclydia.keys()):
        key = input("Select a shape: ")
    print(key, "is located at", Euclydia[key].pos())



def main():
    Euclydia = {}
    colorlist = get_all_subclasses(Color)
    while True:
        print("""Welcome to Euclydia!
              ------------------------
              1. Create a shape
              2. Delete a shape
              3. Locate a shape
              4. Import a population
              5. Export a population
              6. Drive a shape
              7. Quit
              """)
        selection = int(input("Select an option: "))

        if selection == 1:
            create(Euclydia,screen,colorlist)
        elif selection == 2:
            delete(Euclydia)
        elif selection == 3:
            locate(Euclydia)
        elif selection == 4:
            load(Euclydia,screen,colorlist)
        elif selection == 5:
            save(Euclydia)
        elif selection == 6:
            drive(Euclydia)
        elif selection == 7:
            print("Goodbye!")
            wn.bye()
            break
        else:
            print("Invalid option.")

def drive(Euclydia):
    print("""Current Population:""")
    for each in list(Euclydia.keys()):
        print(each)
    key = "Why did you do it?"
    while key not in list(Euclydia.keys()):
        key = input("Select a shape: ")
    Euclydia[key].drive()
main()
wn.mainloop()