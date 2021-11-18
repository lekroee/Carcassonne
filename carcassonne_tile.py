""" carcassonne_tile.py
Logan Kroeger
Creates a class for the Carcassone tile object
CS 120"""

class carcassonne_tile:
    """Represents a tile from the game Carcassonne

    The constructor takes info about the four sides of a tile and whether
    or not two or more cities on a tile connect"""

    def __init__(self, north, east, south, west, city_connects):
        self._edge_info = [north, east, south, west]
        self._city_connects = city_connects

    def get_edge(self, side):
        """Returns the string representing the desired side of a tile
        Args: side is an int 0-3 representing a side of the tile"""
        return self._edge_info[side]


    def edge_has_road(self, side):
        """Returns T/F whether or not a side of a tile has a road
        Args: side is an int 0-3 representing a side of the tile"""
        return self._edge_info[side][-1] == "d"

    def edge_has_city(self, side):
        """Returns T/F whether or not a side of a tile has a city
        Args: side is an int 0-3 representing a side of the tile"""
        return self._edge_info[side][-1] == "y"

    def has_crossroads(self):
        """Returns T/F whether or not a tile has a crossroads"""
        count = 0
        for i in range(len(self._edge_info)):
            if self._edge_info[i][-1] == "d":
                count += 1
        if count >= 3:
            return True
        return False

    def road_get_connection(self, from_side):
        """Returns the side of a tile(int 0-3) that a road connects to on a tile
        Args: from_side is an int 0-3 representing a side of the tile"""
        if self.has_crossroads():
            return -1
        for i in range(len(self._edge_info)):
            if i == from_side:
                continue
            if self._edge_info[i][-1] == "d":
                return i

    def city_connects(self, sideA, sideB):
        """Returns T/F whether or not the two sides(ints 0-3) of a tile have
        cities that connect"""
        if sideA == sideB:
            return True
        if self._city_connects:
            if self._edge_info[sideA][-1] == 'y' and\
               self._edge_info[sideB][-1] == 'y':
                return True
        return False

    def rotate(self):
        """Returns a new tile object with the values 'rotated 90 degrees'"""
        return carcassonne_tile(self._edge_info[3], self._edge_info[0],
                                self._edge_info[1], self._edge_info[2],
                                self._city_connects)


tile01 = carcassonne_tile("city", "grass+road", "grass", "grass+road", False)
tile02 = carcassonne_tile("city", "city", "grass", "city", True)
tile03 = carcassonne_tile("grass+road", "grass+road", "grass+road",
                          "grass+road", False)
tile04 = carcassonne_tile("city", "grass+road", "grass+road", "grass", False)
tile05 = carcassonne_tile("city", "city", "city", "city", True)
tile06 = carcassonne_tile("grass+road", "grass", "grass+road", "grass", False)
tile07 = carcassonne_tile("grass", "city", "grass", "city", False)
tile08 = carcassonne_tile("grass", "city", "grass", "city", True)
tile09 = carcassonne_tile("city", "city", "grass", "grass", True)
tile10 = carcassonne_tile("grass", "grass+road", "grass+road",
                          "grass+road", False)
tile11 = carcassonne_tile("city", "grass+road", "grass+road", "city", True)
tile12 = carcassonne_tile("city", "grass", "grass+road", "grass+road", False)
tile13 = carcassonne_tile("city", "grass+road", "grass+road",
                          "grass+road", False)
tile14 = carcassonne_tile("city", "city", "grass", "grass", False)
tile15 = carcassonne_tile("grass+road", "grass+road", "grass", "grass", False)
tile16 = carcassonne_tile("city", "grass", "grass", "grass", False)