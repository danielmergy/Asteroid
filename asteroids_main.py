from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
from random import randint
from math import *
import sys

MIN_SCREEN = -500
MAX_SCREEN = 500

TWENTY_PTS = 20
FIFTY_PTS = 50
HUNDRED_PTS = 100

SPEED_MIN = 1
SPEED_MAX = 4

LIMIT_TORP = 10
LIMIT_SPECIAL = 25
LIFETIME_TORP = 200
LIFETIME_SPECIAL_TORP = 150
DEFAULT_ASTEROIDS_NUM = 5
SPECIAL_COUNTER_INIT = 5
SHIFT_SPECIAL = 30
MAX_SIZE = 3
DIVIDED_SIZE = 2
MIN_SIZE = 1

LIFE_1 = 1
LIFE_2 = 2
LIFE_3 = 3


TIME_LOOP = 1
COUNTER_STEP = 1
SPECIAL_COUNTER_STEP = 1
FIRST_ARG = 1
SQUARE = 2
SCALE_SPD = 2
SPECIAL_SCALE_SPEED = 4
SCREEN_RATE = 5
FIRST_SPECIAL_TORP=90
SHFT_BTWN_SPECIALS=45


HIT_MSG = 'You have been hit by an asteroid  !!!'
HINT = 'You lose a life,try to avoid asteroids to win'
VICTORY = 'Congratulation, you won !!!'
PLAY_AGAIN = 'If you want to play again restart the program'
LOSE = 'You lose...'
QUIT = 'You chose to exit'
BYE = '    bye ! :)    '




class GameRunner:
    """
    The launcher of the game with the interface
    """

    def __init__(self, asteroids_amount):
        """""
       A constructor for a GameRunner object
       :param asteroids_amount: the number of asteroids objects to add
       """
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__asteroid_amounts = asteroids_amount

        self.asteroids = {}


        self.score = 0
        self.counter_torpedo = 0
        self.special_counter = 0
        self.time = 0
        self.torpedos_lst = []
        self.lives = [LIFE_1, LIFE_2, LIFE_3]
        self.special_torpedos_lst = []


        # Creation of the ship.
        self.ship = Ship(randint(MIN_SCREEN, MAX_SCREEN),
                         randint(MIN_SCREEN, MAX_SCREEN), 0, 0, 0)
        self.__screen.draw_ship(self.ship.location_x, self.ship.location_y, 0)

        # Creation of the asteroids according to the amount put by the user.
        i = 0
        while i < asteroids_amount:
            my_asteroid = Asteroid(randint(MIN_SCREEN, MAX_SCREEN),
                                   randint(MIN_SCREEN, MAX_SCREEN),
                                   randint(SPEED_MIN, SPEED_MAX),
                                   randint(SPEED_MIN, SPEED_MAX), MAX_SIZE)
            if my_asteroid.has_intersection(self.ship):
                continue

            self.__screen.register_asteroid(my_asteroid, MAX_SIZE)
            self.__screen.draw_asteroid(my_asteroid,
                                        randint(MIN_SCREEN, MAX_SCREEN),
                                        randint(MIN_SCREEN, MAX_SCREEN))
            self.asteroids[id(my_asteroid)] = my_asteroid
            i += 1

        self._do_loop()


    def run(self):
        """
        begins the game and display the screen
        """
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        """
        Sets the timer to go off again
        """
        self._game_loop()
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)




    def print_the_asteroids(self):
        """"
        takes all the asteroids in game and move them in the screen
        """
        for asteroid_key in self.asteroids.keys():
            ast = self.asteroids[asteroid_key]
            ast.move_x()
            ast.move_y()
            self.__screen.draw_asteroid(ast, ast.location_x, ast.location_y)

    def print_the_ship(self):
        """"
        moves the ship throughout the game
        """
        self.ship.move_x()
        self.ship.move_y()
        self.__screen.draw_ship(self.ship.location_x, self.ship.location_y,
                                self.ship.heading)

    def print_the_torpedos(self):
        """
        takes all the torpedos in game and move them in the screen
        """

        for torpedo in self.torpedos_lst:
            torpedo.move_x()
            torpedo.move_y()
            self.__screen.draw_torpedo(torpedo, torpedo.location_x,
                                       torpedo.location_y,torpedo.heading)

        for torpedo in self.special_torpedos_lst:
            torpedo.move_x()
            torpedo.move_y()
            self.__screen.draw_torpedo(torpedo,torpedo.location_x,
                                       torpedo.location_y,torpedo.heading)

    def check_end(self):
        """
        checks if there is asteroids left. If not, it ends the game
        """
        if len(self.asteroids) == 0:
            self.__screen.show_message(VICTORY, PLAY_AGAIN)
            return True

    def initiate_torpedo(self):
        """
        creates a torpedo and register it in the API
        """
        new_speed_x = self.ship.speed_x + SCALE_SPD * cos(
            radians(self.ship.heading))
        new_speed_y = self.ship.speed_x + SCALE_SPD * sin(
            radians(self.ship.heading))

        torpedo = Torpedo(self.ship.location_x, self.ship.location_y,
                          new_speed_x, new_speed_y, self.ship.heading)

        self.torpedos_lst.append(torpedo)
        torpedo.life=LIFETIME_TORP
        self.__screen.register_torpedo(torpedo)
        self.__screen.draw_torpedo(torpedo,torpedo.location_x,
                                   torpedo.location_y, torpedo.heading)
        self.counter_torpedo += COUNTER_STEP

    def is_there_a_collisions(self):
        """
        checks if there is a collision between the ship and a asteroid
        """
        for asteroid_key in self.asteroids.keys():
            ast = self.asteroids[asteroid_key]
            if ast.has_intersection(self.ship):
                self.__screen.unregister_asteroid(ast)
                self.asteroids.pop(asteroid_key)
                return True

    def check_if_losing(self):
        """
        checks if there are lives left. If not, it's game over
        """
        if len(self.lives) == 0:
            self.__screen.show_message(LOSE, PLAY_AGAIN)
            return True


    def display_lose_life_message(self):
        """
        displays the message of losing life and remove a life of the screen
        """
        self.__screen.show_message(HIT_MSG, HINT)
        self.__screen.remove_life()

    def is_there_a_hit(self):
        """
        This function checks the hits of the torpedo on the asteroids
        :return: tuple (asteroid, torpedo, type of torpedo) if there is
        collision. Else return None.
        type of torpedo : 0 for a normal, 1 for a special
        """
        for asteroid_key in self.asteroids.keys():

            for torpedo in self.torpedos_lst:
                ast = self.asteroids[asteroid_key]
                if ast.has_intersection(torpedo):
                    return ast, torpedo, 0

            for special_torpedo in self.special_torpedos_lst:
                ast = self.asteroids[asteroid_key]
                if ast.has_intersection(special_torpedo):
                    return ast, special_torpedo, 1

    def define_new_asteroid_speed(self, asteroid, torpedo):
        """
        This function defines the speed of the new asteroid created
        :param asteroid: An Asteroid object
        :param torpedo: A Torpedo object
        :return: tuple (new_speed_x,new_speed_y)
        """
        new_speed_x = (asteroid.speed_x + torpedo.speed_x) / sqrt(
            asteroid.speed_x ** SQUARE + asteroid.speed_y ** SQUARE)
        new_speed_y = (asteroid.speed_y + torpedo.speed_y) / sqrt(
            asteroid.speed_x ** SQUARE + asteroid.speed_y ** SQUARE)
        return new_speed_x, new_speed_y

    def initiate_new_asteroid(self, asteroid, new_speed_x, new_speed_y):
        """
        This function defines the new asteroid created
        :param asteroid: the Asteroid object who have been hit
        :param new_speed_x: The speed of the new object on the x axis
        :param new_speed_y: The speed of the new object on the y axis
        """
        my_asteroid = Asteroid(asteroid.location_x, asteroid.location_y,
                               new_speed_x, new_speed_y, asteroid.size - 1)
        self.asteroids[id(my_asteroid)] = my_asteroid
        self.__screen.register_asteroid(my_asteroid, asteroid.size - 1)

        self.__screen.draw_asteroid(my_asteroid, asteroid.location_x,
                                    asteroid.location_y)

    def update_score(self, asteroid):
        """
       This function defines the new asteroid created
       :param asteroid: the Asteroid object who have been hit
       """
        if asteroid.size == MAX_SIZE:
            self.score += TWENTY_PTS
        if asteroid.size == DIVIDED_SIZE:
            self.score += FIFTY_PTS
        if asteroid.size == MIN_SIZE:
            self.score += HUNDRED_PTS

        self.__screen.set_score(self.score)

    def asteroid_division(self, asteroid, torpedo, type_of_torpedo):
        """
        This function remove the elements of the collision and create new ones
        :param asteroid: An Asteroid object
        :param torpedo: A Torpedo object
        :param type_of_torpedo: The type of the torpedo (0 or 1)
        """

        self.update_score(asteroid)
        self.__screen.unregister_torpedo(torpedo)
        self.asteroids.pop(id(asteroid))
        self.__screen.unregister_asteroid(asteroid)


        # for a normal torpedo
        if type_of_torpedo == 0:
            self.torpedos_lst.remove(torpedo)
            self.counter_torpedo -= COUNTER_STEP

        # for a special torpedo
        if type_of_torpedo == 1:
            self.special_torpedos_lst.remove(torpedo)
            self.special_counter -= SPECIAL_COUNTER_STEP


        # in the case that the asteroid can divide
        if asteroid.size != MIN_SIZE and type_of_torpedo!=1:
            new_speed_x = self.define_new_asteroid_speed(asteroid, torpedo)[0]
            new_speed_y = self.define_new_asteroid_speed(asteroid, torpedo)[1]
            self.initiate_new_asteroid(asteroid, new_speed_x, new_speed_y)
            self.initiate_new_asteroid(asteroid, -new_speed_x, -new_speed_y)

    def check_input(self):
        """
        checks the commands of the user and changes the requested parameters
        """
        # in the case that the user has pressed the left button,
        # the ship goes the the left
        if self.__screen.is_left_pressed():
            self.ship.change_heading_left()

        # in the case that the user has pressed the right button,
        # the ship goes the the right
        if self.__screen.is_right_pressed():
            self.ship.change_heading_right()

        # in the case that the user has pressed the up button,
        # the ship goes up
        if self.__screen.is_up_pressed():
            self.ship.accelerate_x()
            self.ship.accelerate_y()

        # in the case that the user has pressed the space button,
        # the ship sends torpedo
        if self.__screen.is_space_pressed():
            if self.counter_torpedo < LIMIT_TORP:
                self.initiate_torpedo()

        # in the case that the user has pressed the teleport key,
        # the ship is randomly teleported
        if self.__screen.is_teleport_pressed():
            self.relocate_the_ship()

        # in the case that the user has pressed the fire key,
        # the ship sends special torpedo
        if self.__screen.is_special_pressed():
            if self.special_counter < LIMIT_SPECIAL:
                self.special_shot()

        # in the case that the user has pressed 'Quit',
        # the games ends and the window closes


    def forced_exit(self):
        if self.__screen.should_end():
            self.__screen.show_message(QUIT, BYE)
            return True

    def print_objects_in_game(self):
        """
        The main function for displaying all the objects in game
        """
        self.print_the_ship()
        self.print_the_torpedos()
        self.print_the_asteroids()

    def is_a_normal_torpedo_over(self):
        """
        checks if the lifetime of a torpedo is over
        :return: a Torpedo object and the type of torpedo,0:
        """
        for torpedo in self.torpedos_lst:
            if torpedo.life==0:
                return (torpedo,0)


    def is_a_special_torpedo_over(self):
        """
        checks if the lifetime of a special torpedo is over
        :return: a Torpedo object and the type of torpedo,1 :
        """
        for torpedo in self.special_torpedos_lst:
            if torpedo.life==0:
                return (torpedo,1)



    def delete_the_torpedo(self, torpedo, type_of_torpedo):
        """
         This function deletes a torpedo because its lifetime ends
         """
        self.__screen.unregister_torpedo(torpedo)

        # for a normal torpedo
        if type_of_torpedo == 0:
            self.torpedos_lst.remove(torpedo)
            self.counter_torpedo -= COUNTER_STEP

        # for a special torpedo
        if type_of_torpedo == 1:
            self.special_torpedos_lst.remove(torpedo)
            self.special_counter -= SPECIAL_COUNTER_STEP

    def relocate_the_ship(self):
        """
        This function relocates the ship in a self place and immobilise it
        """
        self.ship.location_x = randint(MIN_SCREEN, MAX_SCREEN)
        self.ship.location_y = randint(MIN_SCREEN, MAX_SCREEN)
        self.ship.speed_x = 0
        self.ship.speed_y = 0
        for asteroid in self.asteroids.values():
            if asteroid.has_intersection(self.ship):
                self.relocate_the_ship()

    def move_the_asteroids(self):
        """
        This function moves the asteroids in game
        """
        for asteroid in self.asteroids.values():
            asteroid.speed_x = randint(SPEED_MIN, SPEED_MAX)
            asteroid.speed_y = randint(SPEED_MIN, SPEED_MAX)
            asteroid.move_x()
            asteroid.move_y()

    def stop_the_game(self):
        """
        This function stops the game when there is a collision
        """
        self.ship.speed_x = 0
        self.ship.speed_y = 0
        for asteroid in self.asteroids.values():
            asteroid.speed_x = 0
            asteroid.speed_y = 0

    def special_shot(self):
        """
       This function initiates the special torpedos
       """
        new_speed_x = self.ship.speed_x + SPECIAL_SCALE_SPEED * cos(
            radians(self.ship.heading))
        new_speed_y = self.ship.speed_y + SPECIAL_SCALE_SPEED * sin(
            radians(self.ship.heading))

        # a counter for changing the angle of each torpedo to create a spere
        i = -2
        while i < 3:
            special_torpedo = Torpedo(self.ship.location_x,
                                      self.ship.location_y+(20*i), new_speed_x,
                                      new_speed_y,
                                      self.ship.heading)
            self.__screen.register_torpedo(special_torpedo)
            self.special_torpedos_lst.append(special_torpedo)
            self.__screen.draw_torpedo(special_torpedo,
                                       special_torpedo.location_x,
                                       special_torpedo.location_y,
                                       special_torpedo.heading)
            special_torpedo.life=LIFETIME_SPECIAL_TORP
            i += 1
        self.special_counter += SPECIAL_COUNTER_INIT

    def remove_life_from__all_torpedos(self):
        for torpedo in self.torpedos_lst:
            torpedo.life-=1
        for torpedo in self.special_torpedos_lst:
            torpedo.life-=1

    def _game_loop(self):
        """
        The main function of the game checking users commands, analysing
        interactions between different objects ,changing their parameters
        update the score,lives,display the objects and close the game in need.
        """



        self.print_objects_in_game()
        self.time += TIME_LOOP
        self.remove_life_from__all_torpedos()
        self.check_input()


        if self.is_there_a_collisions():
            self.stop_the_game()
            self.lives.pop()
            if len(self.lives) > 0:
                self.display_lose_life_message()
            self.relocate_the_ship()
            self.move_the_asteroids()
            self.special_counter = 0
            self.counter_torpedo = 0


        while self.is_there_a_hit() is not None:
            asteroid_hit = self.is_there_a_hit()[0]
            torpedo_that_hit = self.is_there_a_hit()[1]
            type_of_torpedo = self.is_there_a_hit()[2]
            self.asteroid_division(asteroid_hit, torpedo_that_hit,
                                   type_of_torpedo)

        while self.is_a_normal_torpedo_over()is not None:
            torp_to_delete = self.is_a_normal_torpedo_over()[0]
            self.delete_the_torpedo(torp_to_delete, 0)

        while self.is_a_special_torpedo_over()is not None:
            torp_to_delete = self.is_a_special_torpedo_over()[0]
            self.delete_the_torpedo(torp_to_delete, 1)

        if self.check_end() or self.check_if_losing() or self.forced_exit():
             self.__screen.end_game()
             sys.exit()


def main(amount):
    """
    the main function of the game
    :param amount: the number of asteroids that we want to start the game
    """
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > FIRST_ARG:
        main(int(sys.argv[FIRST_ARG]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
