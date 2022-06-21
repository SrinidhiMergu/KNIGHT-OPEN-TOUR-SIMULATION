import pygame, sys
from pygame import mixer 

#Function to create a button
def create_button(pos_x, pos_y, width, height, hovercolor, defaultcolor):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)
    if (pos_x + width) > mouse[0] > pos_x and (pos_y + height) > mouse[1] > pos_y:
        pygame.draw.rect(screen, hovercolor, (pos_x, pos_y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, defaultcolor, (pos_x, pos_y, width, height))

# Start menu true until we click the start button
def start_menu():
    start_text = FONT.render("KNIGHT'S  TOUR", True, BLACK_TILE_COLOR)
    start_button_text =  SMALL_FONT.render("Start the tour", True, BLACKISH)

    while True:
        screen.fill(WHITE_TILE_COLOR)
        #The title centered text
        screen.blit(start_text, ((screen_size - start_text.get_width()) / 2, 300))

        #start button (left, top, width, height)
        start_button =  create_button(screen_size - 150, 50, 125, 75, LIGHT_GREY, SLATE_GREY)

        if start_button:
            chess_board_screen()

        # Start button text
        screen.blit(start_button_text, (screen_size - 145, 75))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()

        pygame.display.update()
        clock.tick(15)

# Chess board background and the path covered
def chess_board_screen():
    mixer.music.load('fluffing_duck.mp3')
    mixer.music.play()
    mixer.music.set_volume(0.02)

    screen.fill(BLACK_TILE_COLOR)

    for i in range(size):
        for j in range(size):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, WHITE_TILE_COLOR, (tile_size * i, tile_size * j, tile_size, tile_size), 0)

    knight_x = y
    knight_y = x
    pygame.draw.circle(screen, KNIGHT_TILE_COLOR,
            (tile_size * knight_x + tile_size // 2, tile_size * knight_y + tile_size // 2), tile_size // 4, 0)
    pygame.display.update()
    msElapsed = clock.tick(fps)

    mov_num = 0
    while True:
        if mov_num != (len(moves) - 1):
                knight_x = moves[mov_num][1]
                knight_y = moves[mov_num][0]
                pygame.draw.circle(screen, VISITED_TILE_COLOR,
                               (tile_size * knight_x + tile_size // 2, tile_size * knight_y + tile_size // 2), tile_size // 4, 0)
                mov_num += 1
                move(mov_num)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        msElapsed = clock.tick(fps)

# A class to find the best possible path to cover all the squares
class Solve_knight_tour:

    def __init__(self, board_size):
        self.size = board_size
        self.chess_board = [[-1 for i in range(self.size)] for j in range(self.size)]

    def is_valid(self, row, col):
        if self.chess_board[row][col] == -1:
            return 1
        return 0

    def get_possible_moves(self, x, y):
        k_moves = [[2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2], [1, -2], [2, -1]]
        possible_moves = []
        for i in range(8):
            if (0 <= x+k_moves[i][0] < self.size) and (0 <= y+k_moves[i][1] < self.size) and \
                    self.is_valid(x+k_moves[i][0], y+k_moves[i][1]):

                possible_moves.append([x+k_moves[i][0], y+k_moves[i][1]])
        return possible_moves

    def solve(self, x, y):
        knight_moves = [[x, y]]
        counter = 2
        self.chess_board[x][y] = 1
        for i in range(self.size*self.size):
            pos = self.get_possible_moves(x, y)
            if pos == []:
                break
            Min = pos[0]
            for p in pos:
                if len(self.get_possible_moves(p[0], p[1])) <= len(self.get_possible_moves(Min[0], Min[1])):
                    Min = p
            x = Min[0]
            y = Min[1]
            knight_moves.append([x, y])
            self.chess_board[x][y] = counter
            counter += 1
        return knight_moves

size = int(input("Enter chess board size: "))
x, y = map(int, input("Enter initial coordinates: ").split())
board = Solve_knight_tour(size)
moves = board.solve(x, y)


def move(mov_num):
    knight_x = moves[mov_num][1]
    knight_y = moves[mov_num][0]
    pygame.draw.circle(screen, KNIGHT_TILE_COLOR,
                    (tile_size * knight_x + tile_size // 2, tile_size * knight_y + tile_size // 2), tile_size // 4, 0)


fps=1.5
screen_size = 700
tile_size = screen_size // size

pygame.init()
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Knight's Tour")

clock = pygame.time.Clock()


WHITE_TILE_COLOR = (254, 205, 157)
BLACK_TILE_COLOR = (208, 138, 70)
VISITED_TILE_COLOR = (255, 255, 255)
KNIGHT_TILE_COLOR = (120, 120, 120)

FONT = pygame.font.SysFont("comicsansms", 65)
SMALL_FONT = pygame.font.SysFont("comicsansms", 14)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 100, 10)
SLATE_GREY = (112, 128, 144)
LIGHT_GREY = (165, 175, 185)
BLACKISH = (10, 10, 10)

def main():
    # game loop
    while True:
        start_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        msElapsed = clock.tick(fps)

if __name__ == "__main__":
    main()
