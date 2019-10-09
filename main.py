import tcod as libtcod
import pygame

# Game Files
import constants


# DEFINITIONS

#      _______.___________..______       __    __    ______ .___________.
#     /       |           ||   _  \     |  |  |  |  /      ||           |
#    |   (----`---|  |----`|  |_)  |    |  |  |  | |  ,----'`---|  |----`
#     \   \       |  |     |      /     |  |  |  | |  |         |  |
# .----)   |      |  |     |  |\  \----.|  `--'  | |  `----.    |  |
# |_______/       |__|     | _| `._____| \______/   \______|    |__|

class struc_Tile:
    """
    determines if the there's a tile or not in the map
    """
    def __init__(self, block_path):
        self.block_path = block_path


#   ______   .______          __   _______   ______ .___________.    _______.
#  /  __  \  |   _  \        |  | |   ____| /      ||           |   /       |
# |  |  |  | |  |_)  |       |  | |  |__   |  ,----'`---|  |----`  |   (----`
# |  |  |  | |   _  <  .--.  |  | |   __|  |  |         |  |        \   \
# |  `--'  | |  |_)  | |  `--'  | |  |____ |  `----.    |  |    .----)   |
#  \______/  |______/   \______/  |_______| \______|    |__|    |_______/

class obj_Actor:
    def __init__(self, x, y, name_object, sprite, creature=None):
        self.x = x  # Map Address
        self.y = y  # Map Address
        self.sprite = sprite

        if creature:
            self.creature = creature
            creature.owner = self


    def draw(self):
        SURFACE_MAIN.blit(self.sprite, (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

    def move(self, dx, dy):
        # Only move when the block ahead is False
        if GAME_MAP[self.x + dx][self.y + dy].block_path == False:
            self.x += dx
            self.y += dy


#   ______   ______   .___  ___. .______     ______   .__   __.  _______ .__   __. .___________.    _______.
#  /      | /  __  \  |   \/   | |   _  \   /  __  \  |  \ |  | |   ____||  \ |  | |           |   /       |
# |  ,----'|  |  |  | |  \  /  | |  |_)  | |  |  |  | |   \|  | |  |__   |   \|  | `---|  |----`  |   (----`
# |  |     |  |  |  | |  |\/|  | |   ___/  |  |  |  | |  . `  | |   __|  |  . `  |     |  |        \   \
# |  `----.|  `--'  | |  |  |  | |  |      |  `--'  | |  |\   | |  |____ |  |\   |     |  |    .----)   |
#  \______| \______/  |__|  |__| | _|       \______/  |__| \__| |_______||__| \__|     |__|    |_______/

class com_Creature:
    """
    Creatures have health, can damage other objects by attacking them. Can also die.
    """
    def __init__(self, name_instance, hp=10):
        self.name = name_instance
        self.hp = hp


# class com_Items:
#     pass


# class com_Containers:
#     pass


# .___  ___.      ___      .______
# |   \/   |     /   \     |   _  \
# |  \  /  |    /  ^  \    |  |_)  |
# |  |\/|  |   /  /_\  \   |   ___/
# |  |  |  |  /  _____  \  |  |
# |__|  |__| /__/     \__\ | _|

def map_create():
    new_map = [[struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_HEIGHT)]

    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    return new_map


#  _______  .______          ___   ____    __    ____  __  .__   __.   _______
# |       \ |   _  \        /   \  \   \  /  \  /   / |  | |  \ |  |  /  _____|
# |  .--.  ||  |_)  |      /  ^  \  \   \/    \/   /  |  | |   \|  | |  |  __
# |  |  |  ||      /      /  /_\  \  \            /   |  | |  . `  | |  | |_ |
# |  '--'  ||  |\  \----./  _____  \  \    /\    /    |  | |  |\   | |  |__| |
# |_______/ | _| `._____/__/     \__\  \__/  \__/     |__| |__| \__|  \______|

def draw_game():

    global SURFACE_MAIN

    # clear the surface
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    # draw the map
    draw_map(GAME_MAP)

    # TODO: draw the character
    ENEMY.draw()
    PLAYER.draw()

    # update the display
    pygame.display.flip()


def draw_map(map_to_draw):
    """
    Draws the map on screen
    :param map_to_draw: MAP
    :return: None
    """

    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map_to_draw[x][y].block_path == True:
                # draw wall
                SURFACE_MAIN.blit(constants.S_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
            else:
                # draw floor
                SURFACE_MAIN.blit(constants.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


#   _______      ___      .___  ___.  _______
#  /  _____|    /   \     |   \/   | |   ____|
# |  |  __     /  ^  \    |  \  /  | |  |__
# |  | |_ |   /  /_\  \   |  |\/|  | |   __|
# |  |__| |  /  _____  \  |  |  |  | |  |____
#  \______| /__/     \__\ |__|  |__| |_______|

def game_main_loop():
    """
    In this function, we loop the main game
    :return: None
    """

    game_quit = False
    while not game_quit:

        # get player input
        events_list = pygame.event.get()

        # process input
        for event in events_list:
            if event.type == pygame.QUIT:
                game_quit = True

            # Player movement changes
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    PLAYER.move(0, -1)

                elif event.key == pygame.K_DOWN:
                    PLAYER.move(0, 1)

                elif event.key == pygame.K_RIGHT:
                    PLAYER.move(1, 0)

                elif event.key == pygame.K_LEFT:
                    PLAYER.move(-1, 0)

        # draw the game
        draw_game()

    # quit the game
    pygame.quit()
    exit()


def game_initializate():
    """
    This function initializes the main windows and Pygame
    :return: None
    """

    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY

    # initialize Pygame
    pygame.init()

    # Initializes the window surface
    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))
    pygame.display.set_caption("The Crazy Adventures of Culebrita")

    # Initializes the map of the game
    GAME_MAP = map_create()

    # Initialize the player
    creature_com1 = com_Creature("greg")
    PLAYER = obj_Actor(0, 0, "python", constants.S_PLAYER, creature=creature_com1)

    creature_com2 = com_Creature("jackie")
    ENEMY = obj_Actor(15, 15, "crab", constants.S_ENEMY, creature=creature_com2)


# .______       __    __  .__   __.
# |   _  \     |  |  |  | |  \ |  |
# |  |_)  |    |  |  |  | |   \|  |
# |      /     |  |  |  | |  . `  |
# |  |\  \----.|  `--'  | |  |\   |
# | _| `._____| \______/  |__| \__|
if __name__ == '__main__':
    game_initializate()
    game_main_loop()
