import pygame
import random
import copy
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN_BLUE = (0, 153, 153)
LIGHT_GRAY = (192, 192, 192)
RED = (255, 0, 0)

block_size = 30
left_margin = 2 * block_size
upper_margin = block_size

size = (left_margin + 30 * block_size, upper_margin + 15 * block_size)
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
dotted_set = set()
hit_blocks = set()
pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Morskoy Boy")

font_size = int(block_size / 1.5)

font = pygame.font.SysFont('notosans', font_size)


class AutoShips:
    """ class for creating ships automatically

    :param offset: where the grid starts
    :type offset: int
    :param available_blocks: coordinates of all blocks that are avaiable for creating ships
    :type available_blocks: set[tuple[int, int]]
    :param ships_set: set of ships
    :type ships_set: set
    :param ships: list of ships
    :type ships: list
    :param number_of_blocks: length of a needed ship
    :type number_of_blocks: int
    :param coor:  x or y coordinate to increment/decrement
    :type coor: int
    :param str_rev: 1 or -1
    :type str_rev: int
    :param x_or_y: 0 or 1
    :type x_or_y: int
    :param ship_coordinates: coordinates of unfinished ship
    :type ship_coordinates: list[tuple[Any, Any]]
    :param new_ship: list of tuples with a newly created ship's coordinates
    :type new_ship: list
    """
    def __init__(self, offset):
        self.offset = offset
        self.available_blocks = set((x, y) for x in range(1 + self.offset, 11 + self.offset) for y in range(1, 11))
        self.ships_set = set()
        self.ships = self.populate_grid()

    def create_start_block(self, available_blocks):
        x_or_y = random.randint(0, 1)
        str_rev = random.choice((-1, 1))
        x, y = random.choice(tuple(available_blocks))
        return x, y, x_or_y, str_rev

    def create_ship(self, number_of_blocks, available_blocks):
        ship_coordinates = []
        x, y, x_or_y, str_rev = self.create_start_block(available_blocks)
        for _ in range(number_of_blocks):
            ship_coordinates.append((x, y))
            if not x_or_y:
                str_rev, x = self.get_new_block_to_ship(
                    x, str_rev, x_or_y, ship_coordinates)
            else:
                str_rev, y = self.get_new_block_to_ship(
                    y, str_rev, x_or_y, ship_coordinates)
        if self.is_ship_valid(ship_coordinates):
            return ship_coordinates
        return self.create_ship(number_of_blocks, available_blocks)

    def get_new_block_to_ship(self, coor, str_rev, x_or_y, ship_coordinates):
        if (coor <= 1 - self.offset * (x_or_y - 1) and str_rev == -1) or (
                coor >= 10 - self.offset * (x_or_y - 1) and str_rev == 1):
            str_rev *= -1
            return str_rev, ship_coordinates[0][x_or_y] + str_rev
        else:
            return str_rev, ship_coordinates[-1][x_or_y] + str_rev

    def is_ship_valid(self, new_ship):
        ship = set(new_ship)
        return ship.issubset(self.available_blocks)

    def add_new_ship_to_set(self, new_ship):
        self.ships_set.update(new_ship)

    def update_available_blocks_for_creating_ships(self, new_ship):
        for elem in new_ship:
            for k in range(-1, 2):
                for m in range(-1, 2):
                    if 0 + self.offset < (elem[0] + k) < 11 + self.offset and 0 < (elem[1] + m) < 11:
                        self.available_blocks.discard((elem[0] + k, elem[1] + m))

    def populate_grid(self):
        ships_coordinates_list = []
        for number_of_blocks in range(4, 0, -1):
            for _ in range(5 - number_of_blocks):
                new_ship = self.create_ship(
                    number_of_blocks, self.available_blocks)
                ships_coordinates_list.append(new_ship)
                self.add_new_ship_to_set(new_ship)
                self.update_available_blocks_for_creating_ships(new_ship)
        return ships_coordinates_list


class Button:
    """Class creates buttons and prints explanatory message for them

    :param x_offset: horizontal offset where to start drawing button
    :type x_offset: int
    :param button_title: Button's name
    :type button_title: str
    :param title_width: width of title
    :type title_width: int
    :param title_height: height pf title
    :type title_height: int
    :param message_to_show: explanatory message to print onscreen
    :type message_to_show: str
    :param color: Button's color. Defaults to None (BLACK)
    :type color: tuple
    :param mouse: pose of mouse
    :type mouse: tuple[int, int]
    :param x_start: where the button starts
    :type x_start: int
    :param y_start: where the button starts
    :type y_start: int
    :param rect_for_draw: rectangle coordinates
    :type rect_for_draw: tuple[int, int, int, int]
    :param rect: rect
    :type rect: Rect
    :param rect_for_draw_button_title: place of button title
    :type rect_for_draw_button_title: tuple[float, float]
    """
    def __init__(self, x_offset, button_title, message_to_show):
        self.title = button_title
        self.title_width, self.title_height = font.size(self.title)
        self.message = message_to_show
        self.button_width = self.title_width + block_size
        self.button_height = self.title_height + block_size
        self.x_start = x_offset
        self.y_start = upper_margin + 10 * block_size + self.button_height
        self.rect_for_draw = self.x_start, self.y_start, self.button_width, self.button_height

        self.rect = pygame.Rect(self.rect_for_draw)

        self.rect_for_draw_button_title = (self.x_start + self.button_width / 2 - self.title_width / 2,
                                           self.y_start + self.button_height / 2 - self.title_height / 2)
        self.color = BLACK

    def draw_button(self, color=None):
        if not color:
            color = self.color
        pygame.draw.rect(screen, color, self.rect_for_draw)
        text_to_blit = font.render(self.title, True, WHITE)
        screen.blit(text_to_blit, self.rect_for_draw_button_title)

    def change_color_on_hover(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.draw_button(GREEN_BLUE)

    def print_message_for_button(self):
        if self.message:
            message_width, message_height = font.size(self.message)
            rect_for_message = (self.x_start / 2 - message_width / 2,
                                self.y_start + self.button_height / 2 - message_height / 2)
            text = font.render(self.message, True, BLACK)
            screen.blit(text, rect_for_message)


auto_button_place = left_margin + 17 * block_size
manual_button_place = left_margin + 20 * block_size
files_button_place = left_margin + 24.5 * block_size
how_to_create_ships_message = "Как вы хотите создать корабли?(АВТО через 1.5мин)"
auto_button = Button(auto_button_place, "АВТО", how_to_create_ships_message)
manual_button = Button(manual_button_place, "ВРУЧНУЮ", how_to_create_ships_message)
files_button = Button(files_button_place, "ФАЙЛЫ", how_to_create_ships_message)
undo_message = "Для отмены последнего корабля нажмити кнопку"
undo_button_place = left_margin + 14 * block_size
undo_button = Button(undo_button_place, "ОТМЕНА", undo_message)
message_rect_for_drawing_ships = (undo_button.rect_for_draw[0] + undo_button.rect_for_draw[2],
                                  upper_margin + 11 * block_size,
                                  size[0] - (undo_button.rect_for_draw[0] + undo_button.rect_for_draw[2]),
                                  4 * block_size)
player1_ships_to_draw = []
player2_ships_to_draw = []


def draw_ships(ships_coordinates_list):
    """Draws rectangles around the blocks that are occupied by a ship

    :param x_start: where the ship starts
    :type x_start: int
    :param y_start: where the ship starts
    :type y_start: int
    :param ships_coordinates_list:  a list of ships s coordinates
    :type ships_coordinates_list: list[list]
    """
    for elem in ships_coordinates_list:
        ship = sorted(elem)
        x_start = ship[0][0]
        y_start = ship[0][1]
        # Hor and 1block ships
        ship_width = block_size * len(ship)
        ship_height = block_size
        # Vert ships
        if len(ship) > 1 and ship[0][0] == ship[1][0]:
            ship_width, ship_height = ship_height, ship_width
        x = block_size * (x_start - 1) + left_margin
        y = block_size * (y_start - 1) + upper_margin
        pygame.draw.rect(
            screen, BLACK, ((x, y), (ship_width, ship_height)), width=block_size // 10)


class Grid:
    """Class to draw the grids and add title, numbers and letters to them

    :param title: Players' name to be displayed on the top of his grid
    :type title: str
    :param offset:  Where the grid starts (in number of blocks)
    :type offset: int
    """
    def __init__(self, title, offset):
        self.title = title
        self.offset = offset
        self.draw_grid()
        self.add_nums_letters_to_grid()
        self.sign_grids()

    def draw_grid(self):
        for i in range(11):
            # Hor grid
            pygame.draw.line(screen, BLACK, (left_margin + self.offset, upper_margin + i * block_size),
                             (left_margin + 10 * block_size + self.offset, upper_margin + i * block_size), 1)
            # Vert grid
            pygame.draw.line(screen, BLACK, (left_margin + i * block_size + self.offset, upper_margin),
                             (left_margin + i * block_size + self.offset, upper_margin + 10 * block_size), 1)

    def add_nums_letters_to_grid(self):
        for i in range(10):
            num_ver = font.render(str(i + 1), True, BLACK)
            letters_hor = font.render(LETTERS[i], True, BLACK)
            num_ver_width = num_ver.get_width()
            num_ver_height = num_ver.get_height()
            letters_hor_width = letters_hor.get_width()

            # Ver num grid1
            screen.blit(num_ver, (left_margin - (block_size // 2 + num_ver_width // 2) + self.offset,
                                  upper_margin + i * block_size + (block_size // 2 - num_ver_height // 2)))
            # Hor LETTERS grid1
            screen.blit(letters_hor, (left_margin + i * block_size + (block_size //
                                                                      2 - letters_hor_width // 2) + self.offset,
                                      upper_margin - block_size))

    def sign_grids(self):
        player = font.render(self.title, True, BLACK)
        sign_width = player.get_width()
        screen.blit(player, (left_margin + 5 * block_size - sign_width // 2 + self.offset,
                             upper_margin - block_size // 2 - font_size + 11 * block_size))


def check_hit_or_miss(fired_block, opponents_ships_list, player2_turn, opponents_ships_list_original_copy,
                      opponents_ships_set):
    """Checks whether the block that was shot at either by computer or by human is a hit or a miss.

    :param fired_block: fired_block
    :type fired_block: tuple[int, int]
    :param opponents_ships_list: opponents_ships_list
    :type opponents_ships_list: list[list]
    :param player2_turn: turn of player2 or  player1
    :type player2_turn: bool
    :param opponents_ships_list_original_copy: opponents_ships_list_original_copy
    :type opponents_ships_list_original_copy: list[list]
    :param opponents_ships_set: opponents_ships_set
    :type opponents_ships_set: set[list]
    :returns: True or False
    :rtype: bool
    """
    for elem in opponents_ships_list:
        diagonal_only = True
        if fired_block in elem:
            ind = opponents_ships_list.index(elem)
            if len(elem) == 1:
                diagonal_only = False
            update_dotted_and_hit_sets(
                fired_block, player2_turn, diagonal_only)
            elem.remove(fired_block)
            opponents_ships_set.discard(fired_block)
            if not elem:
                update_destroyed_ships(
                    ind, player2_turn, opponents_ships_list_original_copy)
            if not player2_turn:
                return False
            else:
                return True
    add_missed_block_to_dotted_set(fired_block)
    if player2_turn:
        return False
    else:
        return True


def add_missed_block_to_dotted_set(fired_block):
    """Adds a fired_block to the set of missed shots

    :param fired_block: fired_block
    :type fired_block: tuple[int, int]
    """
    if not isinstance(fired_block, tuple):
        raise Warning
    dotted_set.add(fired_block)


def update_destroyed_ships(ind, player2_turn, opponents_ships_list_original_copy):
    """Adds blocks before and after a ship to dotted_set to draw dots on them.

    :param ind: index
    :type ind: int
    :param player2_turn: turn of player2 or  player1
    :type player2_turn: bool
    :param opponents_ships_list_original_copy: opponents_ships_list_original_copy
    :type opponents_ships_list_original_copy: list[list]
    """
    if not isinstance(opponents_ships_list_original_copy, list):
        raise Warning
    ship = sorted(opponents_ships_list_original_copy[ind])
    for i in range(-1, 1):
        update_dotted_and_hit_sets(ship[i], player2_turn, False)


def update_dotted_and_hit_sets(fired_block, player2_turn, diagonal_only=True):
    """ Puts dots in center of diagonal or all around a block that was hit

    :param fired_block: fired_block
    :type fired_block: tuple[int, int]
    :param player2_turn: turn of player2 or  player1
    :type player2_turn: bool
    :param diagonal_only: only diagonal or all blocks
    :type diagonal_only: bool
    """
    global dotted_set
    x, y = fired_block
    a, b = 0, 11
    if not player2_turn:
        a += 15
        b += 15
    hit_blocks.add((x, y))
    for i in range(-1, 2):
        for j in range(-1, 2):
            if diagonal_only:
                if i != 0 and j != 0 and a < x + i < b and 0 < y + j < 11:
                    dotted_set.add((x + i, y + j))
            else:
                if a < x + i < b and 0 < y + j < 11:
                    dotted_set.add((x + i, y + j))
    dotted_set -= hit_blocks


def draw_from_dotted_set(dotted_set):
    """Draws dots in the center of all blocks in the dotted_set

    :param dotted_set: dotted_set
    :type dotted_set: set
    """
    for elem in dotted_set:
        pygame.draw.circle(screen, BLACK, (block_size * (
                elem[0] - 0.5) + left_margin, block_size * (elem[1] - 0.5) + upper_margin), block_size // 6)


def draw_hit_blocks(hit_blocks):
    """ Draws 'X' in the blocks that were successfully hit either by computer or by human

    :param hit_blocks: hit blocks
    :type hit_blocks: set
    """
    for block in hit_blocks:
        x1 = block_size * (block[0] - 1) + left_margin
        y1 = block_size * (block[1] - 1) + upper_margin
        pygame.draw.line(screen, BLACK, (x1, y1),
                         (x1 + block_size, y1 + block_size), block_size // 6)
        pygame.draw.line(screen, BLACK, (x1, y1 + block_size),
                         (x1 + block_size, y1), block_size // 6)


def show_message_at_rect_center(text, rect, which_font=font, color=RED):
    """Prints message to screen at a given rect's center.

   :param text: Message to print
   :type text: str
   :param rect: rectangle in (x_start, y_start, width, height) format
   :type rect: tuple
   :param which_font: What font to use to print message. Defaults to font.
   :param color: Color of the message. Defaults to RED.
   :type color: tuple
    """
    text_width, text_height = which_font.size(text)
    text_rect = pygame.Rect(rect)
    x_start = text_rect.centerx - text_width / 2
    y_start = text_rect.centery - text_height / 2
    text_to_blit = which_font.render(text, True, color)
    screen.blit(text_to_blit, (x_start, y_start))


def ship_is_valid(ship_set, blocks_for_manual_drawing):
    """Checks if ship is not touching other ships

   :param ship_set: ship_set
   :type ship_set: set
   :param blocks_for_manual_drawing: blocks_for_manual_drawing
   :type blocks_for_manual_drawing: set
   :return: ship_set.isdisjoint(blocks_for_manual_drawing)
   :rtype:bool
    """
    if len(ship_set) > 4:
        raise Warning
    return ship_set.isdisjoint(blocks_for_manual_drawing)


def check_ships_numbers(ship, num_ship_list):
    """Checks if a ship of particular length (1-4) does not exceed necessary quantity (4-1)

   :param ship: List with new ships' coordinates
   :type ship: list
   :param num_ship_list: List_with numbers of particular ships on respective indexes.
   :type num_ship_list: list
   :return: (5 - len(ship)) > num_ship_list[len(ship) - 1]
   :rtype: bool
    """
    if num_ship_list[-1] > 1 or num_ship_list[-2] > 2 or num_ship_list[-3] > 3 or num_ship_list[-4] > 4:
        raise Warning
    return (5 - len(ship)) > num_ship_list[len(ship) - 1]


def update_used_blocks(ship, used_blocks_set):
    """Adds blocks for drawing

    :param ship: ship
    :type ship: set
    :param used_blocks_set: used_blocks_set
    :type used_blocks_set: set
    :return: used_blocks_set: used_blocks_set
    :rtype: set
    """
    if len(ship) > 5:
        raise Warning
    for block in ship:
        for i in range(-1, 2):
            for j in range(-1, 2):
                used_blocks_set.add((block[0] + i, block[1] + j))
    return used_blocks_set


def restore_used_blocks(deleted_ship, used_blocks_set):
    """Discard blocks for drawing

    :param deleted_ship: deleted ship
    :type deleted_ship: list
    :param used_blocks_set: used_blocks_set
    :type used_blocks_set: set
    :return: used_blocks_set: used_blocks_set
    :rtype: set
    """
    if isinstance(used_blocks_set, list):
        raise Warning
    for block in deleted_ship:
        for i in range(-1, 2):
            for j in range(-1, 2):
                used_blocks_set.discard((block[0] + i, block[1] + j))
    return used_blocks_set


def manual_ships(offset, drawing, ships_not_created, rect_for_grids, num_ships_list, player_ships_set,
                 rect_for_messages_and_buttons, start, ship_size, used_blocks_for_manual_drawing, player_ships_to_draw):
    """Allows both players to create ships manually

    :param offset: Where the grid starts (in number of blocks)
    :type offset: int
    :param drawing: Shows when the drawing of the ship begins
    :type drawing: bool
    :param ships_not_created: shows whether ships have been created or not
    :type ships_not_created: bool
    :param rect_for_grids: rect_for_grids
    :type rect_for_grids: tuple[int, int, int, int]
    :param num_ships_list: list with the number of ship lengths and their number
    :type num_ships_list: list[int]
    :param player_ships_set: Lots of ships
    :type player_ships_set: set
    :param rect_for_messages_and_buttons: rect for messages and buttons
    :type rect_for_messages_and_buttons: tuple[int, int, int, int]
    :param start: the beginning of the construction of ship
    :type start: tuple[int, int]
    :param ship_size: ship size
    :type ship_size: tuple[int, int]
    :param used_blocks_for_manual_drawing: blocks on which ships are drawn
    :type used_blocks_for_manual_drawing: set
    :param player_ships_to_draw: player's work ships to draw
    :type player_ships_to_draw: list
    :return: player_ships_work: player's work ships
    :rtype: list
    """
    while ships_not_created:
        screen.fill(WHITE, rect_for_grids)
        player1_grid = Grid("PLAYER1", 0)
        player2_grid = Grid("PLAYER2", 15 * block_size)
        undo_button.draw_button()
        undo_button.print_message_for_button()
        undo_button.change_color_on_hover()
        mouse = pygame.mouse.get_pos()
        if not player_ships_to_draw:
            undo_button.draw_button(LIGHT_GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ships_not_created = False
                game_over = True
            elif undo_button.rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN:
                if player_ships_to_draw:
                    deleted_ship = player_ships_to_draw.pop()
                    num_ships_list[len(deleted_ship) - 1] -= 1
                    used_blocks_for_manual_drawing = restore_used_blocks(
                        deleted_ship, used_blocks_for_manual_drawing)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                x_start, y_start = event.pos
                start = x_start, y_start
                ship_size = (0, 0)
            elif drawing and event.type == pygame.MOUSEMOTION:
                x_end, y_end = event.pos
                end = x_end, y_end
                ship_size = x_end - x_start, y_end - y_start
            elif drawing and event.type == pygame.MOUSEBUTTONUP:
                x_end, y_end = event.pos
                drawing = False
                ship_size = (0, 0)
                start_block = ((x_start - left_margin) // block_size + 1,
                               (y_start - upper_margin) // block_size + 1)
                end_block = ((x_end - left_margin) // block_size + 1,
                             (y_end - upper_margin) // block_size + 1)
                if start_block > end_block:
                    start_block, end_block = end_block, start_block
                temp_ship = []
                if (0 + offset < start_block[0] < 15 + offset and 0 < start_block[1] < 11 and
                        0 + offset < end_block[0] < 15 + offset and 0 < end_block[1] < 11):
                    screen.fill(WHITE, message_rect_for_drawing_ships)
                    if start_block[0] == end_block[0] and (end_block[1] - start_block[1]) < 4:
                        for block in range(start_block[1], end_block[1] + 1):
                            temp_ship.append((start_block[0], block))
                    elif start_block[1] == end_block[1] and (end_block[0] - start_block[0]) < 4:
                        for block in range(start_block[0], end_block[0] + 1):
                            temp_ship.append((block, start_block[1]))
                    else:
                        show_message_at_rect_center(
                            "КОРАБЛЬ СЛИШКОМ БОЛЬШОЙ!", message_rect_for_drawing_ships)
                else:
                    show_message_at_rect_center(
                        "КОРАБЛЬ ЗА ПРЕДЕЛАМИ СЕТКИ!", message_rect_for_drawing_ships)
                if temp_ship:
                    temp_ship_set = set(temp_ship)
                    if ship_is_valid(temp_ship_set, used_blocks_for_manual_drawing):
                        if check_ships_numbers(temp_ship, num_ships_list):
                            num_ships_list[len(temp_ship) - 1] += 1
                            player_ships_to_draw.append(temp_ship)
                            player_ships_set |= temp_ship_set
                            used_blocks_for_manual_drawing = update_used_blocks(
                                temp_ship, used_blocks_for_manual_drawing)
                        else:
                            show_message_at_rect_center(
                                f"ДОСТАТОЧНО {len(temp_ship)}-ПАЛУБНЫХ КОРАБЛЕЙ", message_rect_for_drawing_ships)
                    else:
                        show_message_at_rect_center(
                            "КОРАБЛИ ПРИКАСАЮТСЯ!", message_rect_for_drawing_ships)
            if len(player_ships_to_draw) == 10:
                ships_not_created = False
                screen.fill(WHITE, rect_for_messages_and_buttons)
        pygame.draw.rect(screen, BLACK, (start, ship_size), 3)
        # draw_ships(player_ships_to_draw)
        pygame.display.update()
    return copy.deepcopy(player_ships_to_draw)


def files_ships_function(file):
    """A function for opening a file and creating ships based on data from the file

    :param file: file
    :type file: str
    :return: [files_ships_list, files_ships_set]
    :rtype: list
    """
    if not isinstance(file, str):
        raise Warning
    with open(file) as f:
        files_ships_list = list()
        files_ships_set = set()
        files_ships = f.readline()
        files_ships = files_ships.replace('[[', '[').replace(']]', ']').replace('],', ']|').split('|')
        for ship in files_ships:
            elements = ship.rstrip().lstrip().replace('[(', '(').replace(')]', ')').replace('),', ')|').split('|')
            files_ships_list.append([eval(element) for element in elements])
            files_ships_set.update([eval(element) for element in elements])
        return [files_ships_list, files_ships_set]


start_time = time.time()


def main():
    """the main function responsible for the operation of the entire program

    :param game_over: game over or not
    :type game_over: bool
    :param player2_turn: the first or second player moves
    :type player2_turn: bool
    :param drawing: draw or not draw some object
    :type drawing: bool
    :param start: The beginning of drawing the ship
    :type start: tuple[int, int]
    :param ship_size: ship size
    :type ship_size: tuple[int, int]
    :param ships_creation_not_decided: choosing a way to create a ships
    :type ships_creation_not_decided: bool
    :param ships_not_created: checks if all ships are built
    :type ships_not_created: bool
    :param rect_for_grids: rect for grids
    :type rect_for_grids: tuple[int, int, int, int]
    :param rect_for_messages_and_buttons:
    :type rect_for_messages_and_buttons:
    :param player1_ships_to_draw: player1 ships to draw
    :type player1_ships_to_draw: list
    :param player1_ships_set: player1 ships set
    :type player1_ships_set: set
    :param player2_ships_to_draw:  player2 ships to draw
    :type player2_ships_to_draw: list
    :param player2_ships_set: player2 ships set
    :type player2_ships_set: set
    :param used_blocks_for_manual_drawing: area for drawing ships manually
    :type used_blocks_for_manual_drawing: set
    :param num_ships_player1_list: stores the number and length of ships for player1
    :type num_ships_player1_list: tuple[int, int, int, int]
    :param num_ships_player2_list: stores the number and length of ships for player2
    :type num_ships_player2_list: tuple[int, int, int, int]
    :param player1_grid: grid for player1
    :type player1_grid: Grid
    :param player2_grid: grid for player2
    :type player2_grid: Grid
    :param player1: player 1
    :type player1: AutoShips
    :param player2: player2
    :type player2: AutoShips
    :param player1_ships_working: the first player's work ships
    :type player1_ships_working:  list
    :param player2_ships_working:the second player's work ships
    :type player2_ships_working: list
    :param auto_button: button for auto
    :type auto_button: Button
    :param files_button: button for files
    :type files_button: Button
    :param manual_button: button for manual
    :type manual_button:Button
    """
    game_over = False
    player2_turn = False
    screen.fill(WHITE)
    drawing = False
    start = (0, 0)
    ship_size = (0, 0)
    ships_creation_not_decided = True
    ships_not_created = True
    rect_for_grids = (0, 0, size[0], upper_margin + 12 * block_size)
    rect_for_messages_and_buttons = (0, upper_margin + 11 * block_size, size[0], 5 * block_size)
    player1_ships_to_draw = []
    player1_ships_set = set()
    player2_ships_to_draw = []
    player2_ships_set = set()
    used_blocks_for_manual_drawing = set()
    num_ships_player1_list = [0, 0, 0, 0]
    num_ships_player2_list = [0, 0, 0, 0]
    player1_grid = Grid("PLAYER1", 0)
    player2_grid = Grid("PLAYER2", 15 * block_size)
    pygame.display.update()

    while ships_creation_not_decided:
        current_time = time.time() - start_time
        if current_time >= 90:
            player1 = AutoShips(0)
            player2 = AutoShips(15)
            player1_ships_to_draw = player1.ships
            player1_ships_set = player1.ships_set
            player1_ships_working = copy.deepcopy(player1.ships)
            player2_ships_to_draw = player2.ships
            player2_ships_set = player2.ships_set
            player2_ships_working = copy.deepcopy(player2.ships)
            ships_creation_not_decided = False
            ships_not_created = False
            break
        auto_button.draw_button()
        manual_button.draw_button()
        files_button.draw_button()
        auto_button.change_color_on_hover()
        manual_button.change_color_on_hover()
        files_button.change_color_on_hover()
        auto_button.print_message_for_button()
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                ships_creation_not_decided = False
                ships_not_created = False
            elif event.type == pygame.MOUSEBUTTONDOWN and auto_button.rect.collidepoint(mouse):
                player1 = AutoShips(0)
                player2 = AutoShips(15)
                player1_ships_to_draw = player1.ships
                player1_ships_set = player1.ships_set
                player1_ships_working = copy.deepcopy(player1.ships)
                player2_ships_to_draw = player2.ships
                player2_ships_set = player2.ships_set
                player2_ships_working = copy.deepcopy(player2.ships)
                ships_creation_not_decided = False
                ships_not_created = False
            elif event.type == pygame.MOUSEBUTTONDOWN and files_button.rect.collidepoint(mouse):
                player1_ships_to_draw = files_ships_function('player1_grid.txt')[0]
                player1_ships_set = files_ships_function('player1_grid.txt')[1]
                player1_ships_working = copy.deepcopy(player1_ships_to_draw)
                player2_ships_to_draw = files_ships_function('player2_grid.txt')[0]
                player2_ships_set = files_ships_function('player2_grid.txt')[1]
                player2_ships_working = copy.deepcopy(player2_ships_to_draw)
                ships_creation_not_decided = False
                ships_not_created = False
            elif event.type == pygame.MOUSEBUTTONDOWN and manual_button.rect.collidepoint(mouse):
                ships_creation_not_decided = False

        pygame.display.update()
        screen.fill(WHITE, rect_for_messages_and_buttons)

    player1_ships_working = manual_ships(0, drawing, ships_not_created, rect_for_grids,
                                         num_ships_player1_list, player1_ships_set,
                                         rect_for_messages_and_buttons, start, ship_size,
                                         used_blocks_for_manual_drawing, player1_ships_to_draw)
    player2_ships_working = manual_ships(15, drawing, ships_not_created, rect_for_grids,
                                         num_ships_player2_list, player2_ships_set,
                                         rect_for_messages_and_buttons, start, ship_size,
                                         used_blocks_for_manual_drawing, player2_ships_to_draw)

    while not game_over:
        # draw_ships(player1_ships_to_draw)
        # draw_ships(player2_ships_to_draw)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif not player2_turn and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (left_margin + 15 * block_size < x < left_margin + 25 * block_size) and (
                        upper_margin < y < upper_margin + 10 * block_size):
                    fired_block = ((x - left_margin) // block_size + 1, (y - upper_margin) // block_size + 1)
                    if fired_block not in dotted_set and fired_block not in hit_blocks:
                        player2_turn = check_hit_or_miss(fired_block, player2_ships_working, False,
                                                         player2_ships_to_draw, player2_ships_set)
            elif player2_turn and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (left_margin < x < left_margin + 10 * block_size) and (
                        upper_margin < y < upper_margin + 10 * block_size):
                    fired_block = ((x - left_margin) // block_size + 1, (y - upper_margin) // block_size + 1)
                    if fired_block not in dotted_set and fired_block not in hit_blocks:
                        player2_turn = check_hit_or_miss(fired_block, player1_ships_working, True,
                                                         player1_ships_to_draw, player1_ships_set)
        if not player2_ships_set and not player1_ships_set:
            pass
        elif not player2_ships_set:
            show_message_at_rect_center(
                "ВЫИГРАЛ PLAYER1!", (0, 0, size[0], size[1]),
                pygame.font.SysFont('notosans', font_size + block_size * 2))
        elif not player1_ships_set:
            show_message_at_rect_center(
                "ВЫИГРАЛ PLAYER2!", (0, 0, size[0], size[1]),
                pygame.font.SysFont('notosans', font_size + block_size * 2))
        pygame.display.update()
        draw_from_dotted_set(dotted_set)
        draw_hit_blocks(hit_blocks)
        pygame.display.update()


main()
pygame.quit()
