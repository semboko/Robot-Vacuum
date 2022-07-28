import turtle
from time import sleep
from geometry import intersect

class Room:
    def __init__(self, coords):
        self.coords = coords
        self.t = turtle.Turtle()
        self.t.color("red")
        self.t.hideturtle()
        self.t.speed(0)

    def draw_walls(self):
        self.t.penup()
        self.t.setpos(self.coords[0])
        self.t.pendown()
        for x, y in self.coords[1:]:
            self.t.setpos(x, y)
            # self.t.write(str(x) + "," + str(y))
    
    def is_outside(self, x, y, radius):
        xs = [x for x, _ in self.coords]
        ys = [y for _, y in self.coords]

        if x - radius < min(xs) or x + radius > max(xs):
            return True
        
        if y - radius < min(ys) or y + radius > max(ys):
            return True

        return False

class Robot:
    def __init__(self, radius):
        self.t = turtle.Turtle()
        self.t.speed(1)
        self.t.penup()
        self.t.shape("triangle")
        self.radius = radius
        self.step = 10
        self.left_angle = 0
        self.total_path = 0
        self.clean_spots = []
        
        self.drawn_queue = set()
        self.queue_drawer = turtle.Turtle()
        self.queue_drawer.penup()
        self.queue_drawer.hideturtle()
        self.queue_drawer.speed(0)

    def add_room(self, room):
        self.room = room
    
    def step_forward(self):
        self.t.forward(self.step)
        self.total_path += self.step
    
    def rotate(self):
        self.t.left(90)
    
    def step_back(self):
        self.t.back(self.step)
        self.total_path += self.step
    
    def clean_spot(self):
        x, y = self.get_current_pos()
        self.t.dot(5, "blue")
        self.clean_spots.append((x, y))
    
    def spot_is_clean(self):
        x, y = self.get_current_pos()
        if (x, y) in self.clean_spots:
            return True
        return False
    
    def get_current_pos(self):
        x, y = self.t.pos()
        return round(x), round(y)
    
    def forward_is_possible(self):
        possibility = True
        cur_x, cur_y = self.get_forward_sector()
        if self.room.is_outside(cur_x, cur_y, self.radius):
            possibility = False
        return possibility
    
    def get_forward_sector(self):
        self.step_forward()
        x, y = self.get_current_pos()
        self.step_back()
        return x, y

    def move_to(self, x, y):
        self.total_path += self.t.distance(x, y)
        target_left_angle = self.t.towards(x, y)
        angle = (target_left_angle - self.left_angle) % 360
        if angle < 180:
            self.t.left(angle)
        else:
            self.t.right(360 - angle)
        self.left_angle = target_left_angle
        self.t.setpos(x, y)

    def clean(self):
        while True:
            cur_x, cur_y = self.get_current_pos()
            if self.room.is_outside(cur_x, cur_y, self.radius):
                self.step_back()
                self.rotate()
            if self.spot_is_clean():
                print("Spot", cur_x, cur_y)
            self.clean_spot()
            self.step_forward()
    
    def get_ngbh(self):
        cur_x, cur_y = self.get_current_pos()
        return (
            (cur_x + self.step, cur_y),
            (cur_x - self.step, cur_y),
            (cur_x, cur_y + self.step),
            (cur_x, cur_y - self.step),
        )
    
    def move_is_valid(self, new_x, new_y):
        cur_x, cur_y = self.get_current_pos()
        
        for i in range(len(room.coords)-1):
            w1 = room.coords[i]
            w2 = room.coords[i+1]
            if intersect((cur_x, cur_y), (new_x, new_y), w1, w2):
                return False
        return True

    def clean_recursively(self, depth=0):
        print("Current stack:", depth)
        print("Total path:", self.total_path)
        if self.spot_is_clean():
            return
        self.clean_spot()
        for i in range(4):
            if not self.forward_is_possible():
                self.rotate()
                continue
            self.step_forward()
            self.clean_recursively(depth=depth+1)
            self.step_back()
            self.rotate()
    
    def draw_queue(self, x, y):
        if (x, y) not in self.drawn_queue:
            self.queue_drawer.setpos(x, y)
            self.queue_drawer.dot(2, "grey")
    
    def clean_iteratively(self):
        queue = [self.get_current_pos()]
        while queue:
            print("Total path:", self.total_path)
            next_pos = queue.pop()
            # if not self.move_is_valid(*next_pos):
            #     continue
            self.move_to(*next_pos)
            if self.spot_is_clean():
                continue
            self.clean_spot()

            for nbgh_pos in self.get_ngbh():
                if not self.move_is_valid(*nbgh_pos):
                    continue
                if nbgh_pos in queue:
                    continue
                if nbgh_pos in self.clean_spots:
                    continue
                # self.draw_queue(*nbgh_pos)
                queue.append(nbgh_pos)

room = Room((
    (-178, -108),
    (-200, -108),
    (-200, 149),
    (194, 149),
    (194, -159),
    (-72, -159),
    (-72, -108),
    (-85, -108),
    (-85, -99),
    (-72, -99),
    (-72, 0),
    (-7, 0),
    (-7, -5),
    (-63, -5),
    (-63, -150),
    (61, -150),
    (61, -82),
    (33, -82),
    (33, -5),
    (29, -5),
    (29, 0),
    (70, 0),
    (70, -5),
    (38, -5),
    (38, -77),
    (66, -77),
    (66, -150),
    (185, -150),
    (185, -5),
    (106, -5), 
    (106, 0),
    (185, 0),
    (185, 35),
    (182, 35),
    (182, 38),
    (185, 38),
    (185, 141),
    (66, 141),
    (66, 38),
    (152, 38),
    (152, 35),
    (-75, 35),
    (-75, 38),
    (61, 38),
    (61, 141),
    (-66, 141),
    (-66, 116),
    (-72, 116),
    (-72, 141),
    (-192, 141),
    (-192, -99),
    (-178, -99),
    (-178, -108),
    (-85, -108),
))
room.draw_walls()

robot = Robot(radius=10)
robot.add_room(room)
# robot.clean()
# robot.clean_recursively()
robot.clean_iteratively()

turtle.mainloop()