from .vertex import Vertex


class Rectangle:
    def __init__(self,
                 top_left: Vertex,
                 bottom_right: Vertex,
                 top_right: Vertex = None,
                 bottom_left: Vertex = None) -> None:
        self.top_left: Vertex = top_left
        self._top_right: Vertex = top_right
        self._bottom_left: Vertex = bottom_left
        self.bottom_right: Vertex = bottom_right

    @property
    def top_right(self) -> Vertex:
        if self.top_right is None:
            return Vertex(self.bottom_right.x, self.top_left.y)
        else:
            return self._top_right

    @property
    def bottom_left(self) -> Vertex:
        if self.bottom_left is None:
            return Vertex(self.top_left.x, self.bottom_right.y)
        else:
            return self._bottom_left

    @property
    def cropping_tuple(self) -> tuple:
        return self.top_left.tuple[0], self.top_left.tuple[1], self.bottom_right.tuple[0], self.bottom_right.tuple[1]
