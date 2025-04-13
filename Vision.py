import tkinter as tk
import random

#Create the root window
root= tk.Tk()
root.title("Simulator")

#Create the canvas within the window
canvas_width = 500
canvas_height = 500
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

#Add a rectangle to the canvas
#The first two coordinates are where the top left corner starts
#The last two coordinates are where the bottom right corner starts
#canvas.create_rectangle( (10,10,20,20),fill='red')


class Agent:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = 100
        self.y = 100
        self.size = random.randint(5,100)
        self.rect = canvas.create_rectangle( (self.x,self.y,self.x+self.size,self.y+self.size))
        self.target_food = None

    def move(self):
        #Defines how the agent moves
        dx = random.randint(-5,5)
        dy = random.randint(-5,5)
        self.canvas.move(self.rect, dx, dy) 

        self.x += dx
        self.y += dy

    def check_vision(self):
        #Represent vision with a circle
        vision_circle = create_circle(self.x, self.y, 300, canvas)

        #Check if any food is within the vision radius
        visible_food = []
        for food in food_list:
            dist = euclidean_distance(self.x - food.x,self.y-food.y)
            if dist <= 300:
                visible_food.append([food,dist])

        if visible_food:
            x1, y1, x2, y2 = self.canvas.bbox(self.rect)
            a1,b1,a2,b2 = food.get_bounding_box()
            agent_cx = (x1 + x2) / 2
            agent_cy = (y1 + y2) / 2

            food_cx = (a1 + a2) / 2
            food_cy = (b1 + b2) / 2

            dx = food_cx - agent_cx
            dy = food_cy - agent_cy

            length = (dx**2 + dy**2) ** 0.5

            if length != 0:
                dx /= length
                dy /= length
            speed=6
            self.canvas.move(self.rect, dx * speed, dy * speed)
        else:
            self.move()

    def at_food(self):
        #If the agent is at the food, the food is destroyed
        for food in food_list[:]:
        #These get the bounding box positions of the agents on the screen
            x1, y1, x2, y2 = self.canvas.bbox(self.rect)
            a1,b1,a2,b2 = food.get_bounding_box()
            #We then check if the bouding boxes overlap at all
            #This will return true or false
            if (
                x1 < a2 and x2 > a1 and
                y1 < b2 and y2 > b1
            ) == True:
                print("Food consumed")
                food.destroy()
                food_list.remove(food)
    
    def get_pos(self):
        #Gets the agents current position
        return self.x, self.y

class Food:
    def __init__(self,canvas):
        self.canvas = canvas
        self.x = random.randint(0,500)
        self.y = random.randint(0,500)
        self.size = 20
        self.food_rect = canvas.create_rectangle( (self.x,self.y,self.x+self.size,self.y+self.size),fill='green')

    def destroy(self):
        self.canvas.delete(self.food_rect)

    def get_bounding_box(self):
        return self.canvas.bbox(self.food_rect)

def create_circle(x, y, r, canvas): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1)

def euclidean_distance(x,y):
    return (x**2 + y**2)**0.5

#Create the agents
agent = Agent(canvas)
food_list = [Food(canvas)]

def update():
    #agent.move()
    agent.check_vision()
    agent.at_food()
    #print(agent.get_pos())
    root.after(50, update)

update()  # start the loop

root.mainloop()
