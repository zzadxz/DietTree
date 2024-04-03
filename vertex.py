"""The file houses our implementation of the vertex and weighted vertex classes. These are essential to our
implementation of our graph classes."""
from __future__ import annotations
from typing import Any, Union


# TODO EVERYTHING
class Vertex:
    """A vertex in a book review graph, used to represent a user or a book.

    Each vertex item is either a user id or book title. Both are represented as strings,
    even though we've kept the type annotation as Any to be consistent with lecture.

    Instance Attributes:
        - item: The data stored in this vertex, representing a user or book.
        - kind: The type of this vertex: 'food', 'dessert', 'drink', or 'category'
        - neighbours: The vertices that are adjacent to this vertex.
        - TODO

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'food', 'dessert', 'drink', 'category'}
        - TODO
    """
    item: Any
    kind: str
    neighbours: set[Vertex]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'food', 'dessert', 'drink', 'category'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = set()

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)


class WeightedVertex(Vertex):
    """A vertex in a weighted book review graph, used to represent a user or a book.

    Same documentation as Vertex from Exercise 3, except now neighbours is a dictionary mapping
    a neighbour vertex to the weight of the edge to from self to that neighbour.
    Note that for this exercise, the weights will be integers between 1 and 5.

    Instance Attributes:
        - item: The data stored in this vertex, representing a user or book.
        - kind: The type of this vertex: 'food', 'dessert', 'drink', or 'category'
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'food', 'dessert', 'drink', 'category'}
    """
    item: Any
    kind: str
    range: range
    neighbours: dict[WeightedVertex, Union[int, float]]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - self.kind in {'calories', 'proten'} # TODO (add the rest)
        """
        super().__init__(item, kind)
        self.neighbours = {}

    def vertex_similarity_score(self, other: WeightedVertex, weightings: dict[str, float]) -> float:
        """
        Returns the similarity score between two food vertices.

        Representation Invariants:
            - self.kind in {'food', 'dessert', 'drink'}
            - other.kind in {'food', 'dessert', 'drink'}
        """

        if weightings is None:
            weightings = {}
        similarity = 0
        shared_neighbours = set(self.neighbours.keys()).intersection(set(other.neighbours.keys()))

        for v in shared_neighbours:
            similarity += 1 * weightings[v.kind]
        return similarity

    #
    # def get_similarity_score(self, other: WeightedVertex) -> float:
    #     """Return the similarity score between this vertex and other.
    #     """
    #     similarity = 0.0
    #     shared_neighbours = set(self.neighbours.keys()).intersection(set(other.neighbours.keys()))
    #     for v in shared_neighbours:
    #         if v.kind == 'calories':
    #             similarity += 10  # TODO (switch to variables from the slider)
    #         elif v.kind == 'protein':
    #             similarity += 5
    #         elif v.kind == 'sugar':
    #             similarity += 4
    #         elif v.kind == 'fat':
    #             similarity += 3
    #         elif v.kind in {'carb', 'fiber'}:
    #             similarity += 2
    #         else:
    #             similarity += 1
    #     return similarity


if __name__ == '__main__':
    # You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # # increases the running time of the functions/methods.
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136', 'W0221'],
        'extra-imports': ['csv', 'networkx', 'pandas'],
        'max-nested-blocks': 4,
    })
