from typing import List
from dataclasses import dataclass


@dataclass
class Item:
    shape: str
    color: str
    fixed: bool


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

    def set_items(self, color: str, shape: str, loc: List[int]):
        self.__check_loc(loc)
        self._grid[loc[0]][loc[1]] = Item(shape=shape, color=color, fixed=False)

    def __check_loc(self, loc):
        if (len(loc) != 2 or not (
                (0 <= loc[0] < self._n) and (0 <= loc[1] < self._n))):
            raise ValueError(f"Invalid arm location {loc}")

    def markersPresent(self):
        return self._grid[self._arm_x][self._arm_y] is not None

    def

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
            self._arm_holds = self._grid[self._arm_x][self._arm_y]
            self._grid[self._arm_x][self._arm_y] = None

    def putMarker(self):
        if not self.markersPresent() and self._arm_holds is not None:
            self._grid[self._arm_x][self._arm_y] = self._arm_holds
            self._arm_holds = None

    def fixMarker(self):
        if self.markersPresent():
            self._grid[self._arm_x][self._arm_y].fixed = True

    def move(self, x, y):
        self.__check_loc((x, y))
        self._arm_x = x
        self._arm_y = y

    def moveUp(self):
        if 0 <= (self._arm_y - 1) < self._n:
            self._arm_y -= 1

    def moveDown(self):
        if 0 <= (self._arm_y + 1) < self._n:
            self._arm_y += 1

    def moveRight(self):
        if 0 <= (self._arm_x + 1) < self._n:
            self._arm_x += 1

    def moveLeft(self):
        if 0 <= (self._arm_x - 1) < self._n:
            self._arm_x -= 1

    def moveToUnfixedMarker(self):
        for i in range(self._n):
            for j in range(self._n):
                if (self._grid[i][j] is not None) and (not self._grid[i][j].fixed):
                    self.move(i, j)
                    break

    @property
    def n(self):
        return self._n

    def __repr__(self):
        str = ""
        for rid in range(self._n):
            for cid in range(self._n):
                if self._arm_x == rid and self._arm_y == cid:
                    str += "a"
                elif self._grid[rid][cid] is not None:
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

if __name__ == "__main__":
    env = Grid2D(n=10)
    env.set_items("yellow", "round", [2, 3])
    print(env)
    print("=========")
    env.move(2, 3)
    env.pickMarker()
    env.move(7, 6)
    env.putMarker()
    env.move(2, 4)
    print(env)
