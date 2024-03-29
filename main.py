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
    def __init__(self, x, y, name_object, sprite, creature=None, ai=None):
        self.x = x  # Map Address
        self.y = y  # Map Address
        self.sprite = sprite

        self.creature = creature
        self.ai = ai
        # Tie in the game components to the Actor class
        if creature:
            #self.creature = creature
            creature.owner = self

        if ai:
            #self.ai = ai
            ai.owner = self


    def draw(self):
        SURFACE_MAIN.blit(self.sprite, (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

    def move(self, dx, dy):

        # Checks if the movement direction is a Tile or not
        tile_is_Wall = (GAME_MAP[self.x + dx][self.y + dy].block_path == True)  # True if it is a wall

        target = None

        # Checks if the objects are not self and not going to bump into the enemy square
        for object in GAME_OBJECTS:
            if object is not self and object.x == self.x + dx and object.y == self.y and object.creature:
                target = object
                break

        if target:
            print(self.creature.name + " attacks " + target.creature.name)
            target.creature.take_damage(5)

        if not tile_is_Wall and target is None:
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
    def __init__(self, name_instance, hp=10, death_function=None):
        self.name = name_instance
        self.maxhp = hp
        self.hp = hp
        self.death_function = death_function

    def take_damage(self, damage):
        self.hp -= damage
        print(self.name + "'s health is " + str(self.hp) + "/" + str(self.maxhp) + " for 5 damage!")

        if self.hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)

#      ___       __
#     /   \     |  |
#    /  ^  \    |  |
#   /  /_\  \   |  |
#  /  _____  \  |  |
# /__/     \__\ |__|

class ai_Test:
    """
    Once per turn, execute.
    """
    def take_turn(self):
        self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))


def death_monster(monster):
    """
    On death, most monsters stop moving.
    :param monster:
    :return:
    """

    print(monster.creature.name + " is dead!")
    monster.creature = None
    monster.ai = None


# TODO: class com_Item:


# TODO: class com_Containers:


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

    for x in range(constants.MAP_WIDTH):
        # Creates the top horizontal line
        new_map[x][0].block_path = True
        # Creates the bottom horizontal line
        new_map[x][constants.MAP_HEIGHT - 1].block_path = True

    for y in range(constants.MAP_HEIGHT):
        # Creates the vertical left line
        new_map[0][y].block_path = True
        # Creates the vertical right line
        new_map[constants.MAP_WIDTH - 1][y].block_path = True

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

    # draw all objects
    for obj in GAME_OBJECTS:
        obj.draw()

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

    # player action definition
    player_action = "no-action"

    while not game_quit:

        # handle player input
        player_action = game_handle_keys()

        if player_action == "QUIT":
            game_quit = True

        elif player_action != "no-action":
            for obj in GAME_OBJECTS:
                # Only execute the enemy movement if the obj_Actor has ai.
                if obj.ai:
                    obj.ai.take_turn()

        # draw the game
        draw_game()

    # quit the game
    pygame.quit()
    exit()


def game_initialization():
    """
    This function initializes the main windows and Pygame
    :return: None
    """

    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS

    # initialize Pygame
    pygame.init()

    # Initializes the window surface
    SURFACE_MAIN = pygame.display.set_mode((constants.MAP_WIDTH * constants.CELL_WIDTH,
                                            constants.MAP_HEIGHT * constants.CELL_HEIGHT))
    pygame.display.set_caption("The Crazy Adventures of Culebrita")

    # Initializes the map of the game
    GAME_MAP = map_create()

    # Initialize the player
    creature_com1 = com_Creature("greg")
    PLAYER = obj_Actor(1, 1, "python", constants.S_PLAYER, creature=creature_com1)

    creature_com2 = com_Creature("jackie", death_function=death_monster)
    ai_com = ai_Test()
    ENEMY = obj_Actor(15, 15, "crab", constants.S_ENEMY, creature=creature_com2, ai=ai_com)

    GAME_OBJECTS = [PLAYER, ENEMY]


def game_handle_keys():
    """
    Game key handler functions
    :return: char
        "QUIT" if the player presses the x in the top corner
    """

    # get player input
    events_list = pygame.event.get()

    # process input
    for event in events_list:
        if event.type == pygame.QUIT:
            return "QUIT"

        # Player movement changes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                PLAYER.move(0, -1)
                return "player-moved"

            elif event.key == pygame.K_DOWN:
                PLAYER.move(0, 1)
                return "player-moved"

            elif event.key == pygame.K_RIGHT:
                PLAYER.move(1, 0)
                return "player-moved"

            elif event.key == pygame.K_LEFT:
                PLAYER.move(-1, 0)
                return "player-moved"

    return "no-action"


# .______       __    __  .__   __.
# |   _  \     |  |  |  | |  \ |  |
# |  |_)  |    |  |  |  | |   \|  |
# |      /     |  |  |  | |  . `  |
# |  |\  \----.|  `--'  | |  |\   |
# | _| `._____| \______/  |__| \__|
if __name__ == '__main__':
    game_initialization()
    game_main_loop()
