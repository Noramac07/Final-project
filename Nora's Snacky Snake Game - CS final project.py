#importing needed libraries
import tkinter
import random
import os

#game varibles values and functions
ROWS = 20
COLLUMS = 20
TILE_SIZE = 20 
WIDTH = 400 #overall width of game peramiters rows x collums
HEIGHT = 400 #overall height of game peramiters rows x collums

#game peramiters 
game = tkinter.Tk()
game.title("Nora's Snacky Snake Game")
game.resizable(False,False)

#game background and borders
BACKGROUND = tkinter.Canvas(game, bg = "LightBlue", width = WIDTH, height = HEIGHT, borderwidth = 2, highlightthickness = 2)
BACKGROUND.pack() #putting this within the window/ game peramiters
game.update() #add multiple items at once

#restart and back to menu messages
restart = tkinter.Button(game, text = "Try again?", font = "Arial 10", command = lambda: start_over()) 
restart.place_forget() #used to hide the message
Go_Back = tkinter.Button(game, text = "Level Selection", font = "Arial 10", command = lambda: go_back())
Go_Back.place_forget()

class TILE: #makes TILE as an x and y point
    def __init__(self,x,y):
        self.x = x
        self.y = y

#Snake, Food, and velocity peramiters
Snake = TILE(200,300) #snake's head start position
Food = TILE(200,100) #food's starting position
Snake_Body = [] #making multiple snake tiles as a list
Gameover = False #at start game isnt over
Pause = False
Score = 0 #starting score
Highscore = [] 
Speed = 100
VelX = 0 #starting velocity of both varibles before any keys are pressed
VelY = 0 
loop = None
Menu = None

Hsfile = "highscores.txt" #define highscore file varible

def load_hs(): #load highscore function
    global Highscore
    if os.path.exists(Hsfile): #putting Hsfile in os file type
        with open(Hsfile, "r") as f: #reads file
            for line in f:
                line = line.strip()
                if line.isdigit(): #checks its a digit
                    Highscore.append(int(line))
        Highscore.sort(reverse=True) #sorts from first to last 

def save_hs(): #saving the highscore function
    with open(Hsfile, "w") as f: #writes file
        for score in Highscore:
            f.write(str(score) + "\n") #new line 
load_hs() #calling load highscore

def draw(): #draw function
    global Snake, Food, Snake_Body, Gameover, Score, loop, Pause  #defining caribles as global

    BACKGROUND.delete("all")  # clear everything first
    if Pause:  # handle pause first
        BACKGROUND.create_text(200, 200, font = "Arial 30", text = "Paused, Continue?", fill = "black")
        BACKGROUND.create_text(40, 20, font = "Arial 10", text = f"Score: {Score}", fill = "Black")
        return  # stop here, don’t move or redraw snake

    # Game over screen
    if Gameover:
        BACKGROUND.create_text(200, 200, font = "Arial 30", text = f"Game Over!: {Score}", fill = "Black")
        restart.place(relx = 0.5, rely = 0.6, anchor = "center")
        Go_Back.place(relx = 0.5, rely = 0.7, anchor = "center")
        # Add highscore logic
        if Score not in Highscore: #when it adds highscore (only if not already in highscore)
            Highscore.append(Score)
            Highscore.sort(reverse=True) #highest to lowest)
            if len(Highscore) > 5: #checks how many items in highscore
                Highscore.pop() #removes last/ lowest item
            save_hs()
        BACKGROUND.create_text(200, 60, font = "Arial 15", text = f"New High Score!", fill = "Black")
        for i, hs in enumerate(Highscore): #making i in order from 0-1-2.. and hs as lowest to highest
            BACKGROUND.create_text(200, 85 + i*20, font = "Arial 10", text = f"{i+1}. {hs}", fill = "Black") #appears 20 pixels lower than previous
        return
    
    move() #actions within move function

    BACKGROUND.create_rectangle(Food.x, Food.y, Food.x + 20, Food.y + 20, fill = "#FF3366") #defining color and placement of food (food drawn first to have snake go above)
    BACKGROUND.create_rectangle(Snake.x, Snake.y, Snake.x + 20, Snake.y + 20, fill = "#3300FF") #defining color and placement of snake head
    for Tile in Snake_Body:
        BACKGROUND.create_rectangle(Tile.x, Tile.y, Tile.x + 20, Tile.y + 20, fill = "#3300FF") #defining tiles adding as snake eats and color

    BACKGROUND.create_text(40, 20, font = "Arial 10", text = f"Score: {Score}", fill = "Black")

    loop = game.after(Speed, draw) #stores it with.after so it can be paused later

def paused():
    global Pause, loop
    Pause = not Pause #pause starts as fase, so this makes it true here
    if not Pause: #if true
        draw()  
game.bind("<space>", lambda e: paused()) #binds space bar and pause button

def move(): #move function
    global Snake, Food, Snake_Body, Gameover, Score

    #Gameover - How to loose (wall and body)
    if (Gameover):
        return
    
    #Change length of snake body
    for i in range(len(Snake_Body)-1,-1,-1): #starts at last segment, moves toward first segment
        Tile = Snake_Body[i]
        if (i == 0): #first segment follows snake head
            Tile.x = Snake.x
            Tile.y = Snake.y
        else: 
            PreviousTile = Snake_Body[i-1] #each segment cpoys the above one
            Tile.x = PreviousTile.x
            Tile.y = PreviousTile.y

    #move in direction of of VelX and VelY
    Snake.x += VelX * 20 
    Snake.y += VelY * 20 

    if (Snake.x < 0 or Snake.x >= WIDTH or Snake.y < 0 or Snake.y >= HEIGHT): #How to lose by hitting the wall
        Gameover = True
        return
    for Tile in Snake_Body: #How to lose by hitting the body of the snake
        if (Snake.x == Tile.x and Snake.y == Tile.y):
            Gameover = True
            return
        
    #Snake into Food collison
    if (Snake.x == Food.x and Snake.y == Food.y): #Once food is eaten, adds to snake body 
        Snake_Body.append(TILE(Food.x,Food.y))
        Food.x = random.randint(0,COLLUMS-1) * 20 #Once food is eaten, it moves to a random place 
        Food.y = random.randint(0,ROWS-1) * 20
        Score += 1 #adds one to the score each time food collison occures
        
#Restart - how to try again   
def start_over():
    global loop, Snake, Food, Snake_Body, VelX, VelY, Gameover, Score

    if loop is not None:
        game.after_cancel(loop) #stop previous loop for running

    Snake.x = 200 #redefining peramiters for these functions
    Snake.y = 300
    Food.x = 200
    Food.y = 100
    Snake_Body = []
    VelX = 0
    VelY = 0
    Gameover = False
    Score = 0
        
    restart.place_forget() #used to hide the message
    Go_Back.place_forget()

    draw()

#return to menu function
def go_back():
    global loop, Snake, Snake_Body, VelX, VelY, Gameover, Score, Menu

    if loop is not None:
        game.after_cancel(loop) #redefing peramiters for these functions

    Snake.x = 200 #redefining peramiters for these functions
    Snake.y = 300
    Food.x = 200
    Food.y = 100
    Snake_Body = []
    VelX = 0
    VelY = 0
    Gameover = False
    Score = 0
        
    restart.place_forget() #used to hide the message
    Go_Back.place_forget()

    Menu = tkinter.Frame(game, bg = "Black") #putting menu frame inside game window
    Menu.place(relx = 0.5, rely = 0.5, anchor = "center") #placing message

    message = tkinter.Label(Menu, text = "Select Difficulty", fg = "white", bg = "black", font = "Arial 25") #level selection message displayed inside menu frame
    message.pack(pady = 10) #spacing

    B1 = tkinter.Button(Menu, text = "Easy", width = 25, font = "Arial 20", command = lambda: level(150)) #easy level option button
    B1.pack(pady = 5)
    B2 = tkinter.Button(Menu, text = "Medium", width = 25, font = "Arial 20", command = lambda: level(100)) #medium level button
    B2.pack(pady = 5)
    B3 = tkinter.Button(Menu, text = "Difficult", width = 25, font = "Arial 20", command = lambda: level(50)) #hard level button
    B3.pack(pady = 5)

#Different speed levels being selected
def level(level_speed):
    global Menu, Speed
    Speed = level_speed
    Menu.destroy() #closes the difficulty frame 
    draw() #calls draw function (snake and food)

Menu = tkinter.Frame(game, bg = "Black") #putting menu frame inside game window
Menu.place(relx = 0.5, rely = 0.5, anchor = "center") #placing message

message = tkinter.Label(Menu, text = "Select Difficulty", fg = "white", bg = "black", font = "Arial 30") #displays message inside the menu frame 
message.pack(pady = 10) #space between

B1 = tkinter.Button(Menu, text = "Easy", width = 25, font = "Arial 25", command = lambda: level(150)) 
B1.pack(pady = 5) #space between
B2 = tkinter.Button(Menu, text = "Medium", width = 25, font = "Arial 25", command = lambda: level(100))
B2.pack(pady = 5) 
B3 = tkinter.Button(Menu, text = "Difficult", width = 25, font = "Arial 25", command = lambda: level(50))
B3.pack(pady = 5)

#Movemnt using arrow keys
def change_direction(e): #e means event
    global VelX, VelY, loop
    
    if (e.keysym == "Up" and VelY != 1): #defining the direction of movement for each arrow key (using x and y)
        VelX = 0
        VelY = -1
    elif (e.keysym == "Down" and VelY != -1):
        VelX = 0
        VelY = 1
    elif (e.keysym == "Right" and VelX != -1):
        VelX = 1
        VelY = 0
    elif (e.keysym == "Left" and VelX != 1):
        VelX = -1
        VelY = 0
    if loop is not None:
        game.after_cancel(loop)
    loop = game.after(Speed, draw)

game.bind("<KeyRelease>", change_direction) #once a key is pressed, it releases and movement starts
game.mainloop() #keeps window open until closed by user