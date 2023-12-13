from tkinter import *
import random

GAME_WIDTH = 500
GAME_HEIGHT = 500
SPEED = 200
SPACE_SIZE = 25
BODY_PARTS_START = 10
SNAKE_COLOR = "green"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"


class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS_START
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS_START):
            self.coordinates.append([0,0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:

    def __init__(self):
        x = random.randint(0, int((GAME_WIDTH/SPACE_SIZE)-1))*SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT/SPACE_SIZE)-1))*SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "u":
        y -= SPACE_SIZE
    elif direction == "d":
        y += SPACE_SIZE
    elif direction == "l":
        x -= SPACE_SIZE
    elif direction == "r":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x,y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=("Score:{}".format(score)))
        canvas.delete("food")
        food = Food()
    else:
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
        del snake.coordinates[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    if new_direction=="l" and direction!="r":
        direction=new_direction

    if new_direction=="r" and direction!="l":
        direction=new_direction

    if new_direction=="u" and direction!="d":
        direction=new_direction

    if new_direction=="d" and direction!="u":
        direction=new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        print("Collided")
        return True

    if y < 0 or y >= GAME_HEIGHT:
        print("Collided")
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("Body Part Collision")
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2,
                       canvas.winfo_height()/2,
                       font=('consolas', 70), text="Game Over", fill="red")

window = Tk()
window.title("slug game")
window.resizable(False, False)

#
score = 0
direction = "d"

label = Label(window, text="Score={}".format(score), font=('Times New Roman', 40))
label.pack()
#
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack();

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int(screen_width/2 - window_width/2)
y = int(screen_height/2 - window_height/2)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.bind('<Left>', lambda event: change_direction('l'))
window.bind('<Right>', lambda event: change_direction('r'))
window.bind('<Up>', lambda event: change_direction('u'))
window.bind('<Down>', lambda event: change_direction('d'))

snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()