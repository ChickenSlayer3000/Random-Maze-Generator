from tkinter import Tk, Canvas
from random import randint

'''DATA'''
cell_size = 9 #pixels
maze_size = 60 # rows and columns

'''LISTS'''
visited_cells = []
walls = []
revisited_cells = []
paths = []

'''COLORS'''
end_color = 'red'
start_color = 'Green'
path_color = 'violet'

'''CREATES THE BASIC ARRAY TO DRAW THE MAZE ON'''
maze_map = [['w' for _ in range(maze_size)]for _ in range(maze_size)]


def create(canvas):
    '''CREATES THE BASIS FOR AND INITIATES DRAW'''
    for row in range(maze_size):
        for col in range(maze_size):
            if maze_map[row][col] == 'P':
                color = 'White'
            elif maze_map[row][col] == 'w':
                color = 'black'
            draw(canvas, row, col, color)
 
def draw(canvas, row, col, color):
    '''DRAWS RECTANGLES FOR EACH CELL IN MAZE_MAP'''
    x1 = col*cell_size
    y1 = row*cell_size
    x2 = x1+cell_size
    y2 = y1+cell_size
    canvas.create_rectangle(x1, y1, x2, y2, fill=color)

def check_neighbours(ccr, ccc, find_end):
    '''CHECKS NEIGHBOURS'''
    neighbours = [[ccr, ccc-1, ccr-1, ccc-2, ccr, ccc-2, ccr+1, ccc-2, ccr-1, ccc-1, ccr+1, ccc-1], #left
                [ccr, ccc+1, ccr-1, ccc+2, ccr, ccc+2, ccr+1, ccc+2, ccr-1, ccc+1, ccr+1, ccc+1], #right
                [ccr-1, ccc, ccr-2, ccc-1, ccr-2, ccc, ccr-2, ccc+1, ccr-1, ccc-1, ccr-1, ccc+1], #top
                [ccr+1, ccc, ccr+2, ccc-1, ccr+2, ccc, ccr+2, ccc+1, ccr+1, ccc-1, ccr+1, ccc+1]] #bottom
    visitable_neighbours = []
    if not find_end:           
        for i in neighbours:                                                                        #find neighbours to visit
            if i[0] > 0 and i[0] < (maze_size-1) and i[1] > 0 and i[1] < (maze_size-1):
                if maze_map[i[2]][i[3]] == 'P' or maze_map[i[4]][i[5]] == 'P' or maze_map[i[6]][i[7]] == 'P' or maze_map[i[8]][i[9]] == 'P' or maze_map[i[10]][i[11]] == 'P':
                    walls.append(i[0:2])                                                                                               
                else:
                    visitable_neighbours.append(i[0:2])
        return visitable_neighbours
    elif find_end:
        for _ in neighbours:
            if maze_map[_[0]][_[1]] == 'P':
                visitable_neighbours.append(_[0:2])
        return visitable_neighbours

def path_finder(bcr, bcc, ecr, ecc):
    '''FINDS PATH TO END'''
    possible_path = check_neighbours(bcr, bcc, True)
    paths.append([bcr, bcc])
    if bcr == ecr and bcc == ecc:
        return True
    else:
        for i in possible_path:
            if i not in paths:
                found = path_finder(i[0], i[1], ecr, ecc)               
                if found:
                    return paths
                    break
                else:
                    bcr, bcc = paths.pop()

def main():
    '''Main'''
    e = None
    ccr = randint(1, maze_size-1)
    ccc = randint(1, maze_size-1)
    maze_map[ccr][ccc] = 'P'
    finished = False
    
    while not finished:
        visitable_neighbours = check_neighbours(ccr, ccc, False)
        if len(visitable_neighbours) != 0:
            d = randint(1, len(visitable_neighbours))-1
            ncr, ncc = visitable_neighbours[d]
            maze_map[ncr][ncc] = 'P'
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
    canvas_side = maze_size*cell_size
    canvas = Canvas(window, width = canvas_side, height = canvas_side, bg = 'grey')
    canvas.pack()
    create(canvas)
    final_path = path_finder(ccr, ccc, ecr, ecc)
    for i in final_path:
        draw(canvas, i[0], i[1], path_color)
    draw(canvas, ccr, ccc, start_color)
    draw(canvas, ecr, ecc, end_color)
    window.mainloop()

if __name__ == "__main__":
    main()
