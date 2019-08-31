import constants
import pygame
import time
import random
import os
import img2pdf 
from threading import Thread
from PIL import Image
from collections import defaultdict

  
options = """

+--------------------------+
| opções:                  |
+---+----------------------+
| 1 |    exportar          |
| 2 |    jogar             |
| 3 |    resolver          |
| 0 |    sair              |
+---+----------------------+

Digite o numero da opção desejada:

"""

print("""
 _        _    ____ ___ ____  ___ _   _ _____ ___          _   ___  
| |      / \  | __ )_ _|  _ \|_ _| \ | |_   _/ _ \  __   _/ | / _ \ 
| |     / _ \ |  _ \| || |_) || ||  \| | | || | | | \ \ / / || | | |
| |___ / ___ \| |_) | ||  _ < | || |\  | | || |_| |  \ V /| || |_| |
|_____/_/   \_\____/___|_| \_\___|_| \_| |_| \___/    \_/ |_(_)___/ 

""")

while True:
    GRID_WIDTH = int(input('Digite a largura do labirinto (1-50): '))
    GRID_HEIGHT = int(input('Digite a altura do labirinto (1-30): '))
    print('\n')

    if GRID_WIDTH >= 1 and GRID_WIDTH <= 50 and GRID_HEIGHT >= 1 and GRID_HEIGHT <= 30:
        break

os.system('cls' if os.name == 'nt' else 'clear')

print('COMANDOS:')
print('> ↑ (seta para cima): aumenta a velocidade da animação')
print('> ↓ (seta para baixo): diminui a velocidade da animação')


pygame.init()
pygame.display.set_caption("Labirinto v1.0")
screen = pygame.display.set_mode(((GRID_WIDTH+1)*20, (GRID_HEIGHT+1)*20))
clock = pygame.time.Clock()


grid = []
visited = []
stack = []
solution = {}
paths = defaultdict(list)


def generate_grid(x, y):
    for i in range(1, GRID_HEIGHT):
        y = y + constants.CELL_WIDTH
        x = 20
        for j in range(1, GRID_WIDTH):
            grid.append((x, y))
            x = x + constants.CELL_WIDTH

def start_point(x, y):
    pygame.draw.rect(screen, constants.GREEN, (x+2, y+2, 16, 16), 0)
    pygame.display.update()
    

def end_point(x, y):
    pygame.draw.rect(screen, constants.RED, (x+2, y+2, 16, 16), 0)
    pygame.display.update()

def solution_line(x, y, x1, y1):
    pygame.draw.line(screen, constants.RED, (x+10.5, y+10.5), (x1+10.5, y1+10.5), 3)
    pygame.display.update()

def expand_down(x, y):
    pygame.draw.rect(screen, constants.WHITE, (x + 1, y + 1, 19, 39), 0)
    pygame.display.update()


def expand_up(x, y):
    pygame.draw.rect(screen, constants.WHITE, (x + 1, y - constants.CELL_WIDTH + 1, 19, 39), 0)
    pygame.display.update()


def expand_left(x, y):
    pygame.draw.rect(screen, constants.WHITE, (x - constants.CELL_WIDTH + 1, y + 1, 39, 19), 0)
    pygame.display.update()


def expand_right(x, y):
    pygame.draw.rect(screen, constants.WHITE, (x + 1, y + 1, 39, 19), 0)
    pygame.display.update()


def backtracking_cell(x, y):
    pygame.draw.rect(screen, constants.WHITE, (x + 1, y + 1, 18, 18), 0)
    pygame.display.update()


def single_cell(x, y):
    pygame.draw.rect(screen, constants.BLUE, (x + 1, y + 1, 18, 18), 0)
    pygame.display.update()

def single_cell2(x, y):
    pygame.draw.rect(screen, constants.WHITE, (x + 1, y + 1, 18, 18), 0)
    pygame.display.update()


def solution_cell(x, y):
    pygame.draw.rect(screen, constants.BLUE, (x+8, y+8, 5, 5), 0)
    pygame.display.update()


def make_maze(x, y):
    single_cell(x, y)
    stack.append((x, y))
    visited.append((x, y))
    while len(stack) > 0:
        time.sleep(velocity)
        cell = []

        right = x + constants.CELL_WIDTH
        down = y + constants.CELL_WIDTH
        up = y - constants.CELL_WIDTH
        left = x - constants.CELL_WIDTH

        if (x, down) not in visited and (x, down) in grid:
            cell.append("down")

        if (x, up) not in visited and (x, up) in grid:
            cell.append("up")

        if (right, y) not in visited and (right, y) in grid:
            cell.append("right")

        if (left, y) not in visited and (left, y) in grid:
            cell.append("left")

        if len(cell) > 0:
            cell_chosen = (random.choice(cell))

            if cell_chosen == "right":
                expand_right(x, y)
                solution[(x + constants.CELL_WIDTH, y)] = x, y
                paths[(x, y)].append([x+constants.CELL_WIDTH, y])
                paths[(x+constants.CELL_WIDTH, y)].append([x, y])

                x = x + constants.CELL_WIDTH
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "left":
                expand_left(x, y)
                solution[(x - constants.CELL_WIDTH, y)] = x, y
                paths[(x, y)].append([x - constants.CELL_WIDTH, y])
                paths[(x - constants.CELL_WIDTH, y)].append([x, y])

                x = x - constants.CELL_WIDTH
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "down":
                expand_down(x, y)
                solution[(x, y + constants.CELL_WIDTH)] = x, y
                paths[(x, y)].append([x, y + constants.CELL_WIDTH])
                paths[(x, y + constants.CELL_WIDTH)].append([x, y])

                y = y + constants.CELL_WIDTH
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "up":
                expand_up(x, y)
                solution[(x, y - constants.CELL_WIDTH)] = x, y
                paths[(x, y)].append([x, y - constants.CELL_WIDTH])
                paths[(x, y - constants.CELL_WIDTH)].append([x, y])

                y = y - constants.CELL_WIDTH
                visited.append((x, y))
                stack.append((x, y))
        else:
            x, y = stack.pop()
            single_cell(x, y)
            time.sleep(velocity)
            backtracking_cell(x, y)

def play_maze(x, y):

    single_cell(x,y)

    while True:
        if x == (GRID_WIDTH-1)*20 and y == (GRID_HEIGHT-1)*20:
            solve_maze(x, y)
            start_point(20, 20)
            break
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and [x-constants.CELL_WIDTH, y] in paths[(x, y)]:
                    single_cell2(x,y)
                    x = x - constants.CELL_WIDTH
                    single_cell(x,y)
                if event.key == pygame.K_RIGHT and [x + constants.CELL_WIDTH, y] in paths[(x, y)]:
                    single_cell2(x,y)
                    x = x + constants.CELL_WIDTH
                    single_cell(x,y)
                if event.key == pygame.K_UP and [x, y - constants.CELL_WIDTH] in paths[(x, y)]:
                    single_cell2(x,y)
                    y = y - constants.CELL_WIDTH
                    single_cell(x,y)
                if event.key == pygame.K_DOWN and [x, y + constants.CELL_WIDTH] in paths[(x, y)]:
                    single_cell2(x,y)
                    y = y + constants.CELL_WIDTH
                    single_cell(x,y)


def export_maze():
    file_name = input("digite o nome do arquivo: ")

    os.chdir('..')
    actual_path = os.getcwd() + '/mazes/'
    if not os.path.exists(actual_path):
        os.makedirs(actual_path)
    
    pygame.image.save(screen, actual_path + file_name + ".png")

    img_path = actual_path + file_name + ".png"
    pdf_path = actual_path + file_name + ".pdf"
    image = Image.open(img_path) 
    pdf_bytes = img2pdf.convert(image.filename) 
    file = open(pdf_path, "wb")
    file.write(pdf_bytes)
    image.close()
    file.close() 
    print("Labirinto exportado com sucesso.") 


def solve_maze(x, y):
    solution_cell(x, y)
    x1, y1 = GRID_WIDTH*20, GRID_HEIGHT*20
    while (x1, y1) != (20, 20):
        x1, y1 = solution[x, y]

        solution_cell(x1, y1)        
        solution_line(x, y, x1, y1)

        x, y = x1, y1

        time.sleep(velocity)

velocity = 0.1
running = True


def pygame_monitor():
    global running
    global velocity

    while running:
        clock.tick(constants.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if velocity <= 0.3:
                        velocity += 0.01
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    if velocity >= 0.02:
                        velocity -= 0.01


def main():
    global running
    x, y = 20, 20
    generate_grid(0, 0)
    make_maze(x, y)
    start_point(20, 20)
    end_point((GRID_WIDTH-1)*20, (GRID_HEIGHT-1)*20)
    
    while True:
        option = input(options)
        if option == '1':
            export_maze()
        elif option == '2':
            play_maze(x, y)    
        elif option == '3':
            solve_maze((GRID_WIDTH-1)*20, (GRID_HEIGHT-1)*20)
        elif option == '0':
            running = False
            break

if __name__ == '__main__':
    t1 = Thread(target = pygame_monitor)
    t2 = Thread(target = main)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
