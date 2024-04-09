
'''
A* Pathfinding Visualization Tutorial - Python A* Path Finding Tutorial
By Tech With Tim Container: YouTube Year: 2020 URL: https://www.youtube.com/watch?v=JtiK0DOeI4A


'''
import pygame 
import math
from queue import PriorityQueue

width = 800
win = pygame.display.set_mode((width,width))
pygame.display.set_caption("A* Search")

red = (255,0,0)
green = (0,255,0)
blue = (0,255,0)
yellow = (255,255,0)
white = (255,255,255)
black = (0,0,0)
purple = (128,0,128)
orange = (255,165,0)
turquoise  = (64,224,208)
grey = (128,128,128)
class Spot:
    def __init__(self,row,col,width,total_rows):
        self.row=row
        self.col=col
        self.x=row*width
        self.y=col*width
        self.color=white
        self.neighbors=[]
        self.width = width
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == red
    def is_open(self):
        return self.color == green 
    def is_block(self):
        return self.color == black
    def is_start(self):
        return self.color == orange
    def is_end(self):
        return self.color == turquoise
    def reset(self):
        self.color = white
    

    def make_closed(self):
        self.color = red
    def make_open(self):
        self.color = green 
    def make_block(self):
        self.color = black
    def make_start(self):
        self.color = orange
    def make_end(self):
        self.color = turquoise
    def make_path(self):
        self.color = purple

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
    
    def update_neighbors(self,grid):
        self.neighbors=[]
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col] .is_block(): # down
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col] .is_block(): # up
            self.neighbors.append(grid[self.row-1][self.col])

        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_block(): # right
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid[self.row][self.col-1].is_block(): # left
            self.neighbors.append(grid[self.row][self.col-1])

    def __lt__(self,other):
        return False
    
#    (row,col)
def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)
def re_path(came_front,current,draw):
    while current in came_front:
        current = came_front[current]
        current.make_path()
        
        draw()

def algorithm(draw,grid,start,end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count, start))
    came_front ={}
    g_score = {spot:float('inf') for row in grid for spot in row}
    g_score[start] = 0

    f_score = {spot:float('inf') for row in grid for spot in row}
    f_score[start] = h(start.get_pos(),end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end: 
            re_path(came_front,end, draw)
            end.make_end()
            return True
        
        for neighbor in  current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_front[neighbor] = current 
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(),end.get_pos())
                if neighbor not in open_set_hash:
                    count +=1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()


    return False

def make_grid(rows,width):
    grid = []
    gap = width//rows
    for i in range(rows):
        grid.append([])
        for j in range (rows):
            spot = Spot(i,j,gap,rows)
            grid[i].append(spot)
    return grid

def draw_grid(win,rows, width):
    GAP = width // rows
    for i in range(rows):
        pygame.draw.line(win,grey,(0,i*GAP),(width,i*GAP))
        for j in range(rows):
            pygame.draw.line(win,grey,(j*GAP,0),(j*GAP,width))

def  draw(win, grid, rows, width):
    win.fill(white)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win,rows,width)
    pygame.display.update()

def get_clicked_pos(pos,rows,width):
    gap = width//rows
    y,x = pos

    row = y //gap
    col=x//gap

    return row,col

def main(win,width):

    
    rows =100
    grid = make_grid(rows,width)

    start = None
    end = None

    run = True 
    started = False
    while run:
        draw(win,grid,rows,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]: # left
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,rows,width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_block()

            elif pygame.mouse.get_pressed()[2]: # Right
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,rows,width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end: 
                    end = None
            if event.type  == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(win,grid,rows,width),grid,start, end)
                if event.key == pygame.K_k:
                    start = None
                    end = None
                    grid = make_grid(rows,width)
                    


    pygame.quit()


main(win,width)