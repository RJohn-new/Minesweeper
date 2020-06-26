import pygame
import random


# Building list of 100 squares for the grid
def make_board(surface, size):
    squares = list()
    width = (surface.get_width() / size) - 1
    height = (surface.get_height() / size) - 1

    for i in range(size):
        for j in range(size):
            rectangle = pygame.Rect((width * i) + i, (height * j) + j, width, height)
            pygame.draw.rect(surface, (170, 170, 170), rectangle)
            squares.append(rectangle)
    pygame.display.update()
    return squares


# Pick squares to contain bombs from the list of squares
def pick_bombs(squares, size):
    bombs = [False for x in squares]
    for i in range(size + size // 2):
        place = random.randint(0, 99)
        while bombs[place]:
            place = random.randint(0, 99)
        bombs[place] = True
    return bombs


# End of game reveal of the locations of all bombs
def reveal(surface, squares, bombs):
    font = pygame.font.Font('freesansbold.ttf', 32)
    bomb = font.render("B", True, (0, 0, 0), (170, 170, 170))
    bomb_rec = bomb.get_rect()
    for x in range(len(bombs)):
        if bombs[x]:
            bomb_rec.center = (squares[x].left + (squares[x].width // 2), squares[x].top + (squares[x].height // 2))
            surface.blit(bomb, bomb_rec)
    pygame.display.update()


# Computation of the number of neighboring bombs to display when square is clicked
# Also clears areas if there are no nearby bombs
def nearby(surface, squares, bombs, index, known, found):
    total = 0

    # if selected square is not on an edge of the board (boundary logic)
    not_left = index not in range(0, 10)
    not_right = index not in range(90, 100)
    not_top = index % 10 != 0
    not_bottom = index % 10 != 9

    # if statements to test all 8 bordering squares for bombs and increment number of neighboring bombs
    if not_bottom and bombs[index+1]:
        total += 1
    if not_top and bombs[index-1]:
        total += 1
    if not_right and not_top and bombs[index+9]:
        total += 1
    if not_right and bombs[index+10]:
        total += 1
    if not_right and not_bottom and bombs[index+11]:
        total += 1
    if not_left and not_bottom and bombs[index-9]:
        total += 1
    if not_left and bombs[index-10]:
        total += 1
    if not_left and not_top and bombs[index-11]:
        total += 1
    font = pygame.font.Font('freesansbold.ttf', 32)
    known.append(index)
    # Display number of neighboring bombs
    if total != 0:
        num = font.render(str(total), True, (0, 0, 0), (170, 170, 170))
        num_rec = num.get_rect()
        num_rec.center = (squares[index].left + (squares[index].width // 2),
                          squares[index].top + (squares[index].height // 2))
        surface.blit(num, num_rec)
    # Or grey-out empty area and explore to find the size of the full area
    else:
        new_rec = pygame.Rect(squares[index].left, squares[index].top, squares[index].width, squares[index].height)
        pygame.draw.rect(surface, (50, 50, 50), new_rec)
        if not_bottom and index+1 not in known:
            nearby(surface, squares, bombs, index+1, known, found)
        if not_top and index-1 not in known:
            nearby(surface, squares, bombs, index-1, known, found)

        if not_right and not_top and index+9 not in known:
            nearby(surface, squares, bombs, index+9, known, found)
        if not_right and not_bottom and index+11 not in known:
            nearby(surface, squares, bombs, index+11, known, found)
        if not_left and not_bottom and index-9 not in known:
            nearby(surface, squares, bombs, index-9, known, found)
        if not_left and not_top and index-11 not in known:
            nearby(surface, squares, bombs, index-11, known, found)

        if not_right and index+10 not in known:
            nearby(surface, squares, bombs, index+10, known, found)
        if not_left and index-10 not in known:
            nearby(surface, squares, bombs, index-10, known, found)
    found[0] += 1


def main():
    # Creating 500 x 500 window for game with a 10x10 grid for minesweeper
    width = 500
    height = 500
    size = 10
    pygame.init()

    # Setting up window with title and premaking game over and victory tests for end of game
    pygame.display.set_caption("Minesweeper")
    win = pygame.display.set_mode((width, height))
    game_over = False

    rect_list = make_board(win, size)
    bomb_list = pick_bombs(rect_list, size)

    font = pygame.font.Font('freesansbold.ttf', 32)

    lose_text = font.render('Game Over', True, (0, 0, 0), (255, 255, 255))
    text_rec = lose_text.get_rect()
    text_rec.center = (width // 2, height // 2)

    win_text = font.render('WIN!', True, (0, 0, 0), (255, 255, 255))
    win_rec = win_text.get_rect()
    win_rec.center = (width // 2, height // 2)

    known = list()
    found = [0]

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if pygame.mouse.get_pressed()[0]:
                for x in range(len(rect_list)):
                    if rect_list[x].collidepoint(pygame.mouse.get_pos()) and x not in known:
                        if bomb_list[x]:
                            reveal(win, rect_list, bomb_list)
                            win.blit(lose_text, text_rec)
                        else:
                            nearby(win, rect_list, bomb_list, x, known, found)
                if found[0] >= size**2 - (size+size//2):
                    reveal(win, rect_list, bomb_list)
                    win.blit(win_text, win_rec)
                    if pygame.mouse.get_pressed()[0] and win_rec.collidepoint(pygame.mouse.get_pos()):
                        main()
            if pygame.mouse.get_pressed()[2]:
                for x in range(len(rect_list)):
                    if rect_list[x].collidepoint(pygame.mouse.get_pos()) and x not in known:
                        suspect = font.render('X', True, (0, 0, 0), (170, 170, 170))
                        suspect_rec = suspect.get_rect()
                        suspect_rec.center = (rect_list[x].left + rect_list[x].width // 2,
                                              rect_list[x].top + rect_list[x].height // 2)
                        win.blit(suspect, suspect_rec)
            pygame.display.update()


if __name__ == "__main__":
    main()
