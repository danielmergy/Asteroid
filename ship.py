from math import sin,cos,radians

MIN_SCREEN=-500
MAX_SCREEN=500
DELTA= MAX_SCREEN-MIN_SCREEN
UNIT_OF_ROTATE=7


class Ship:

    """
    A moving object in a 2D plan
    """

    def __init__(self,location_x,location_y,speed_x,speed_y,heading):
        """""
        A constructor for a ship object
        :param location_x: A int representing the position on the x axis -500 to 500
        :param location_y: A int representing the position on the y axis -500 to 500
        :param speed_x: A int representing the speed on the x axis
        :param speed_y: A int representing the speed on the y axis
        :param heading: A float in range 0-360
        """

        self.location_x =location_x
        self.location_y = location_y
        self.speed_x = speed_x
        self.speed_y =speed_y
        self.heading= heading

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

    def accelerate_x(self):
        """
        A function for increasing the speed of the object on the X axis
        """
        self.speed_x+=cos(radians(self.heading))

    def accelerate_y(self):
        """
        A function for increasing the speed of the object on the Y axis
        """
        self.speed_y+=sin(radians(self.heading))

    def change_heading_left(self):
        """
        A function for turning clockwise the heading of the object of 7 degrees
        """
        self.heading+=UNIT_OF_ROTATE

    def change_heading_right(self):
        """
        A function for turning underclockwise the heading of the object of 7 degrees
        """
        self.heading-=UNIT_OF_ROTATE
