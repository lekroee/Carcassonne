""" carcassonne_map.py
Logan Kroeger
Creates a class for a Carcassonne map
CS 120"""
from carcassonne_tile import carcassonne_tile
class CarcassonneMap:
    """A class representing a Carcassonne map with the placed tiles
    and possible locations for a tile to be placed"""

    """The constructor does not take any values but places a tile at 0,0
    to start. The map is represented as a dictionary of coordinates with
    the corresponding tiles"""
    def __init__(self):
        self._map = {(0, 0):
        carcassonne_tile("city", "grass+road", "grass", "grass+road", False)}

    def get_all_coords(self):
        """Returns all the coords of the tiles in the map as a set"""
        retval = set()
        for key in self._map:
            retval.add(key)
        return retval

    def find_map_border(self):
        """Gives all the possible coords where a tile could be placed
        Args: none
        Returns: a set of all the coords as tuples
        Pre-conditions: none"""
        tmp = set()
        retval = set()
        for key in self._map:
            tmp.add((key[0] + 1, key[1]))
            tmp.add((key[0] - 1, key[1]))
            tmp.add((key[0], key[1] + 1))
            tmp.add((key[0], key[1] - 1))
        # To remove locations of tiles in the map
        for val in tmp:
            if val not in self._map:
                retval.add(val)
        return retval

    def get(self, x, y):
        """Returns the tile at the specified coords"""
        coord = (x, y)
        if coord in self._map:
            return self._map[coord]
        return None

    def add(self, x, y, tile, confirm=True, tryOnly=False):
        """Checks to see if a tile can be added to the map
        Args: x, y are ints, tile is a Carcassonne tile obj, confirm is
        a bool indicating whether or not to test if the tile can be added,
        tryOnly is a bool indicating whether or not to actually add a tile
        to the map
        Returns: a bool indicating whether the tile was or can be added
        Pre-conditions: tile must be rotated before trying to add to the
        map. This method cannot check and rotate a tile if it's possible"""
        coord = (x, y)
        # The default. Check to see if tile can be added, add if possible
        if confirm and not tryOnly:
            if self._can_add(coord, tile):
                self._map[coord] = tile
                return True
        # For testing if a tile can be added. Will not actually add tile to map
        if confirm and tryOnly:
            if self._can_add(coord, tile):
                return True
        # Add no matter what
        if not confirm and not tryOnly:
            self._map[coord] = tile
            return True
        # If all fails, then return False indicating that the tile could not be
        # or was not added
        return False

    def _can_add(self, coord, tile):
        """Private method determining if the tile can be added
        Args: coord is a tuple containing the x,y coordinate, tile is the tile obj
        that is being check against the map
        Returns: a bool indicating whether tile can be added
        Pre-conditions: none"""
        # If the place is already taken, tile can't be added
        if coord in self._map:
            return False
        # Check to make sure tile is adjacent to another tile
        if coord not in self.find_map_border():
            return False
        # Check tiles around new location, make sure the edges match
        if not self._check_tiles_around(coord, tile):
            return False
        # If all the cases passed, then tile can be added
        return True

    def _check_tiles_around(self, coord, new_tile):
        """Private method for checking the tiles surrounding the new_tile
        Args: coord is a tuple containing the x,y coordinate, new_tile is the
        tile obj that is being check against the map
        Returns: bool indicating whether tile matches surrounding tiles' edges
        Pre-conditions: must have tiles next to it, check for that before calling"""
        count = 0 # to determine if any tiles were actually checked
        # North new_tile/south map tile check
        if self.get(coord[0], coord[1]+1) is not None:
            if new_tile.get_edge(0) != \
               self._map[coord[0], coord[1]+1].get_edge(2):
                return False
            count += 1
        # East new_tile/west map tile check
        if self.get(coord[0]+1, coord[1]) is not None:
            if new_tile.get_edge(1) != \
               self._map[coord[0]+1, coord[1]].get_edge(3):
                return False
            count += 1
        # South new_tile/north map tile check
        if self.get(coord[0], coord[1]-1) is not None:
            if new_tile.get_edge(2) != \
               self._map[coord[0], coord[1]-1].get_edge(0):
                return False
            count += 1
        # West new_tile/east map tile check
        if self.get(coord[0]-1, coord[1]) is not None:
            if new_tile.get_edge(3) != \
               self._map[coord[0]-1, coord[1]].get_edge(1):
                return False
            count += 1
        # If at least one tile was checked and passed, then new_tile can
        # be placed. Otherwise, no tiles were checked and new_tile cannot
        # be placed.
        if count >= 1:
            return True
        else:
            return False

    def trace_road_one_direction(self, x, y, side):
        coord = (x, y)
        # Set at beginning to avoid repeating recursive call
        if side == 0:
            next_x = x
            next_y = y+1
        elif side == 1:
            next_x = x+1
            next_y = y
        elif side == 2:
            next_x = x
            next_y = y-1
        else:
            next_x = x-1
            next_y = y

        if side == 0:
            opposite = 2
        elif side == 2:
            opposite = 0
        elif side == 1:
            opposite = 3
        else:
            opposite = 1

        if (next_x, next_y) not in self._map:
            return []
        if self._map[(next_x, next_y)].has_crossroads():
            return [(next_x, next_y, opposite, -1)]
        # Return an array of tuples with the x,y coords of each tile crossed and
        # the edges with the roads
        return [(next_x, next_y, opposite, self._get_road_dir(next_x, next_y, opposite))] + \
                self.trace_road_one_direction(next_x, next_y, #Recursive call. Had to be split
                self._get_road_dir(next_x, next_y, opposite))


    def _get_road_dir(self, x, y, from_side):
        """Returns the direction of the next tile that the
        road leads to from given side"""
        for i in range(0, 4):
            if i == from_side:
                continue
            if self._map[(x, y)].edge_has_road(i):
                return i


    def trace_road(self, x,y, side):
        side_con = self._map[(x, y)].road_get_connection(side)
        side_dir = self.trace_road_one_direction(x,y, side)
        other_dir = self.trace_road_one_direction(x,y, side_con)
        retval = []
        if side == 3:
            other_dir = sorted(other_dir, reverse=True)
            side_dir = sorted(side_dir, reverse=True)
        else:
            other_dir = sorted(other_dir)
            side_dir = sorted(side_dir)
        for val in other_dir:
            new_val = (val[0], val[1], val[3], val[2])
            retval.append(new_val)
        retval.append((x,y, side_con, side))
        for val in side_dir:
            retval.append(val)
        return retval

    def trace_city(self, x,y, side):
        finding = True
        known_city = set((x,y, side))

        while finding:
            finding = False
            tmp = set()
            for val in known_city:
                next_tile_coords = self._get_next_tile(val[0],val[1], val[2])
                if next_tile_coords not in self._map:
                    return (False, known_city)
                city_on_tile = self._check_city_connect(val[0], val[1], val[2])
                city_on_next = self._check_city_connect(next_tile_coords[0], next_tile_coords[1],
                                                        self._get_opposite(val[2]))
                if len(city_on_tile) > 0 or len(city_on_next) > 0:
                    known_city = set.union(known_city, city_on_tile)
                    known_city = set.union(known_city, city_on_next)
                    finding = True


    def _check_city_connect(self, x,y, side):
        retval = set()
        for i in range(4):
            if i == side:
                continue
            if self._map[(x,y)].city_connects(side, i):
                retval.add(x,y, i)
        return retval


    def _get_next_tile(self, x,y, side):
        if side == 0:
            next_x = x
            next_y = y+1
        elif side == 1:
            next_x = x+1
            next_y = y
        elif side == 2:
            next_x = x
            next_y = y-1
        else:
            next_x = x-1
            next_y = y
        return (next_x, next_y)

    def _get_opposite(self, of_side):
        if side == 0:
            opposite = 2
        elif side == 2:
            opposite = 0
        elif side == 1:
            opposite = 3
        else:
            opposite = 1

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

game = CarcassonneMap()
game.add(1,0, tile01)
game.add(2,0, tile01)
game.add(3,0, tile01)
game.add(4,0, tile01)
game.add(-1,0, tile01)
game.add(-2,0, tile01)
game.add(-3,0, tile01)
game.add(-4,0, tile01)
game.trace_road(0, 0, 1)