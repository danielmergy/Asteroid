from ship import Ship
from torpedo import Torpedo
from math import sqrt

MIN_SCREEN=-500
MAX_SCREEN=500
DELTA= MAX_SCREEN-MIN_SCREEN
SCALE_RADIUS=10
NRML_RAD=5

SHIP_RAD=1
TORPEDO_RAD=4

class Asteroid:

    """
    A moving object in a 2D plan
    """


    def __init__(self,location_x,location_y,speed_x,speed_y,size):
        """""
        A constructor for an asteroid object
        :param location_x: A int representing the position on the x axis -500 to 500
        :param location_y: A int representing the position on the y axis -500 to 500
        :param speed_x: A int representing the speed on the x axis
        :param speed_y: A int representing the speed on the y axis
        :param size: A int in range 1 to 3
        """
        self.location_x =location_x
        self.location_y = location_y
        self.speed_x = speed_x
        self.speed_y =speed_y
        self.size= size

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


    def has_intersection(self,obj):
        """
        A function for detecting interractions of onbjects in game
        :param obj: the object we suspect to enter in collision with our asteroid
        :returns: True if there if there is a collision else False
        """


        object_radius=0
        asteroid_radius=(SCALE_RADIUS*self.size)-NRML_RAD

        if type(obj)==Ship:
            object_radius=SHIP_RAD

        if type(obj)==Torpedo:
            object_radius=TORPEDO_RAD

        dx=obj.location_x
        dy=obj.location_y

        distance=sqrt((dx-self.location_x)**2+(dy-self.location_y)**2)

        if distance<=object_radius+asteroid_radius:
                return True

        return False
