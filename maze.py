from tkinter import *
from random import randint

cell_size = 10 # pixels
ms = 100 # rows and columns
visited_cells = []
walls = []
revisited_cells = []
e = None
start_color = 'Green'
end_color = 'red'

map = [['w' for _ in range(ms)]for _ in range(ms)]


def create():
    for row in range(ms):
        for col in range(ms):
            if map[row][col] == 'P':
                color = 'White'
            elif map[row][col] == 'w':
                color = 'black'
            draw(row, col, color)

def draw(row, col, color):
    x1 = col*cell_size
    y1 = row*cell_size
    x2 = x1+cell_size
    y2 = y1+cell_size
    ffs.create_rectangle(x1, y1, x2, y2, fill=color)


def check_neighbours(ccr, ccc, find_end):
    neighbours = [[ccr, ccc-1, ccr-1, ccc-2, ccr, ccc-2, ccr+1, ccc-2, ccr-1, ccc-1, ccr+1, ccc-1], #left
                [ccr, ccc+1, ccr-1, ccc+2, ccr, ccc+2, ccr+1, ccc+2, ccr-1, ccc+1, ccr+1, ccc+1], #right
                [ccr-1, ccc, ccr-2, ccc-1, ccr-2, ccc, ccr-2, ccc+1, ccr-1, ccc-1, ccr-1, ccc+1], #top
                [ccr+1, ccc, ccr+2, ccc-1, ccr+2, ccc, ccr+2, ccc+1, ccr+1, ccc-1, ccr+1, ccc+1]] #bottom
    visitable_neighbours = []
    blocked_neighbours = []
    if not find_end:           
        for i in neighbours:                                                                        #find neighbours to visit
            if i[0] > 0 and i[0] < (ms-1) and i[1] > 0 and i[1] < (ms-1):
                if map[i[2]][i[3]] == 'P' or map[i[4]][i[5]] == 'P' or map[i[6]][i[7]] == 'P' or map[i[8]][i[9]] == 'P' or map[i[10]][i[11]] == 'P':
                    walls.append(i[0:2])                                                                                               
                else:
                    visitable_neighbours.append(i[0:2])
        return visitable_neighbours
    elif find_end:
        for _ in neighbours:
            if map[_[0]][_[1]] == 'P':
                blocked_neighbours.append(_[0:2])
        return blocked_neighbours

#StartingPoint
scr = randint(1, ms)
scc = randint(1, ms)
ccr, ccc = scr, scc

map[ccr][ccc] = 'P'
finished = False
while not finished:
    visitable_neighbours = check_neighbours(ccr, ccc, False)
    if len(visitable_neighbours) != 0:
        d = randint(1, len(visitable_neighbours))-1
        ncr, ncc = visitable_neighbours[d]
        map[ncr][ncc] = 'P'
        visited_cells.append([ncr, ncc])
        ccr, ccc = ncr, ncc
    if len(visitable_neighbours) == 0:
        try:
            ccr, ccc = visited_cells.pop()
            revisited_cells.append([ccr, ccc])

        except:
            finished = True

while e == None:
    e = randint(1, len(revisited_cells))-1
    ecr = revisited_cells[e][0]
    ecc = revisited_cells[e][1]
    blocked_neighbours = check_neighbours(ecr, ecc, True)
    if len(blocked_neighbours) > 1:
        e = None
    else:
        break

window = Tk()
window.title('Maze')
canvas_side = ms*cell_size
ffs = Canvas(window, width = canvas_side, height = canvas_side, bg = 'grey')
ffs.pack()


create()
draw(scr, scc, start_color)
draw(ecr, ecc, end_color)
window.mainloop()
