MIN_SCREEN=-500
MAX_SCREEN=500
DELTA= MAX_SCREEN-MIN_SCREEN

class Torpedo:

    """
    A moving object in a 2D plan
    """


    def __init__(self,location_x,location_y,speed_x,speed_y,heading):
        """""
        A constructor for a torpedo object
        :param location_x: A int representing the position on the x axis -500 to 500
        :param location_y: A int representing the position on the y axis -500 to 500
        :param speed_x: A int representing the speed on the x axis
        :param speed_y: A int representing the speed on the y axis
        :param orientation: A float in range 0 to 360
        """

        self.location_x =location_x
        self.location_y = location_y
        self.speed_x = speed_x
        self.speed_y =speed_y
        self.heading= heading
        self.life=0

    def move_x(self):
        """
        A function for moving the object on the X axis
        """
        self.location_x= ((self.speed_x + self.location_x - MIN_SCREEN) % DELTA) + MIN_SCREEN


    def move_y(self):
        """
        A function for moving the object on the Y axis
        """
        self.location_y= ((self.speed_y + self.location_y - MIN_SCREEN) % DELTA) + MIN_SCREEN

