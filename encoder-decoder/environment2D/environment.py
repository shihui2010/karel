from typing import List
from dataclasses import dataclass
import numpy as np


@dataclass
class Item:
    shape: str
    color: str
    movable: bool


class Grid2D:
    def __init__(self, n, arm_loc=None):
        """
        :param n:
        """
        self._grid = [[None] * n for _ in range(n)]
        self._n = n
        if arm_loc is not None:
            self.__check_loc(arm_loc)
        self._arm_x, self._arm_y = (0, 0) if arm_loc is None else arm_loc
        self._arm_holds = None

    def set_item(self, color: str, shape: str, loc: List[int]):
        self.__check_loc(loc)
        self._grid[loc[0]][loc[1]] = Item(shape=shape,
                                          color=color,
                                          movable=True)

    def __check_loc(self, loc):
        if (len(loc) != 2 or not (
                (0 <= loc[0] < self._n) and (0 <= loc[1] < self._n))):
            raise ValueError(f"Invalid arm location {loc}")

    def markersPresent(self):
        return self._grid[self._arm_x][self._arm_y] is not None


    def movableMarkersPresent(self):
        if self.markersPresent():
            if self._grid[self._arm_x][self._arm_y].movable:
                return True
        return False

    def existMovableMarkers(self):
        for i in range(self._n):
            for j in range(self._n):
                if (self._grid[i][j] is not None) and self._grid[i][j].movable:
                    return True
        return False

    def getMarkerShape(self):
        if self._grid[self._arm_x][self._arm_y] is None:
            return None
        return self._grid[self._arm_x][self._arm_y].shape

    def getMarkerColor(self):
        if self._grid[self._arm_x][self._arm_y] is None:
            return None
        return self._grid[self._arm_x][self._arm_y].color

    def pickMarker(self):
        if self.markersPresent() and self._arm_holds is None:
            if self._grid[self._arm_x][self._arm_y].movable:
                self._arm_holds = self._grid[self._arm_x][self._arm_y]
                self._grid[self._arm_x][self._arm_y] = None
            else:
                raise Exception("Unpickable marker")

    def putMarker(self):
        if not self.markersPresent() and self._arm_holds is not None:
            self._arm_holds.movable = False
            self._grid[self._arm_x][self._arm_y] = self._arm_holds
            self._arm_holds = None
        elif self.markersPresent():
            raise Exception("Object exists")

    def fixMarker(self):
        if self.markersPresent():
            self._grid[self._arm_x][self._arm_y].movable = False

    def move(self, x, y):
        self.__check_loc((x, y))
        self._arm_x = x
        self._arm_y = y

    def moveToMovableMarker(self):
        end_i, end_j = 0, 0
        for i in range(self._n):
            for j in range(self._n):
                if (self._grid[i][j] is not None) and self._grid[i][j].movable:
                    self.move(i, j)
                    return
                else:
                    end_i, end_j = i, j
        self.move(end_i, end_j)

    def moveDown(self):
        self._arm_y = min(self._n - 1, self._arm_y + 1)

    def moveUp(self):
        self._arm_y = max(0, self._arm_y - 1)

    def moveRight(self):
        self._arm_x = min(self._n - 1, self._arm_x + 1)

    def moveLeft(self):
        self._arm_x = max(0, self._arm_x - 1)

    def moveTop(self):
        self._arm_y = 0

    def moveBottom(self):
        self._arm_y = self._n - 1

    def moveLeftmost(self):
        self._arm_x = 0

    def moveRightmost(self):
        self._arm_x = self._n - 1

    def upperBoundary(self):
        return self._arm_y == self._n - 1

    def lowerBoundary(self):
        return self._arm_y == 0

    def leftBoundary(self):
        return self._arm_x == 0

    def rightBoundary(self):
        return self._arm_x == self._n - 1

    @property
    def n(self):
        return self._n

    @property
    def state(self):
        str = ""
        for cid in range(self._n):
            for rid in range(self._n):
                if self._grid[rid][cid] is not None:
                    if self._grid[rid][cid].shape == "round":
                        str += "o"
                    elif self._grid[rid][cid].shape == "square":
                        str += "x"
                    else:
                        str += "+"
                else:
                    str += "."
            str += "\n"
        return str

    def __repr__(self):
        repr = self.state
        return repr

    @property
    def arm_loc(self):
        return self._arm_x, self._arm_y

    def to_tensor(self, colors: List[str], shapes: List[str]):
        """
        each grid is represented as n x n x (3+k+m) tensor, where k is number of
        colors of the markers and the m is the number of shapes
        each cell is -d vector and
        each element of the vector is binary indicating:
        0: if arm on the cell
        1: if marker present
        2: if marker present and movable
        {j+2}: if marker present and the color is j-th color, j=1, ..., k
        {k+3+i: k+3+m}: if marker present and the shape is i-th shape, i=1,...,m
        :return: np.array of shape [n, n, 3+k+m]
        """
        k = len(colors)
        m = len(shapes)
        res = np.zeros([self._n, self._n, 3 + m + k], dtype=np.int8)
        for cid in range(self._n):
            for rid in range(self._n):
                if rid == self._arm_x and cid == self._arm_y:
                    res[rid][cid][0] = 1
                if self._grid[rid][cid] is not None:
                    item = self._grid[rid][cid]
                    res[rid][cid][1] = 1
                    if item.movable:
                        res[rid][cid][2] = 1
                    color_id = colors.index(item.color)
                    res[rid][cid][color_id + 3] = 1
                    shape_id = shapes.index(item.shape)
                    res[rid][cid][k + 3 + shape_id] = 1
        return res


if __name__ == "__main__":
    env = Grid2D(n=4)
    env.set_item("yellow", "round", [2, 3])
    print(env)
    print("=========")
    env.move(2, 3)
    env.pickMarker()
    env.move(1, 1)
    env.putMarker()
    env.move(2, 1)
    print(env)
    res = env.to_tensor(["yellow", "red"], ["round", "square"])
    print(res)
