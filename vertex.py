from __future__ import annotations
from typing import Any, Union


# TODO EVERYTHING
class Vertex:
    """A vertex in a book review graph, used to represent a user or a book.

    Each vertex item is either a user id or book title. Both are represented as strings,
    even though we've kept the type annotation as Any to be consistent with lecture.

    Instance Attributes:
        - item: The data stored in this vertex, representing a user or book.
        - kind: The type of this vertex: 'user' or 'book'.
        - neighbours: The vertices that are adjacent to this vertex.
        - TODO

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'user', 'book'}
        - TODO
    """
    item: Any
    kind: str
    neighbours: set[Vertex]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'book'}
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
        - kind: The type of this vertex: 'user' or 'book'.
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'user', 'book'}
    """
    item: Any
    kind: str
    neighbours: dict[WeightedVertex, Union[int, float]]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'book'}
        """
        super().__init__(item, kind)
        self.neighbours = {}

    ############################################################################
    # Part 2, Q2a
    ############################################################################
    def similarity_score_unweighted(self, other: WeightedVertex) -> float:
        """Return the unweighted similarity score between this vertex and other.

        The unweighted similarity score is calculated in the same way as the
        similarity score for Vertex (from Exercise 3). That is, just look at edges,
        and ignore the weights.
        """

        if self.degree() == 0 or other.degree() == 0:
            return 0.0
        else:
            self_neighbours = set(self.neighbours.keys())
            other_neighbours = set(other.neighbours.keys())

            intersection = self_neighbours.intersection(other_neighbours)
            union = self_neighbours.union(other_neighbours)
            return len(intersection) / len(union)

    def similarity_score_strict(self, other: WeightedVertex) -> float:
        """Return the strict weighted similarity score between this vertex and other.

        See Exercise handout for details.
        """

        if self.degree() == 0 or other.degree() == 0:
            return 0.0
        else:
            common_neighbours_same_weight = {
                u for u in self.neighbours if u in other.neighbours and self.neighbours[u] == other.neighbours[u]
            }
            all_unique_neighbours = set(self.neighbours.keys()).union(set(other.neighbours.keys()))

            return len(common_neighbours_same_weight) / len(all_unique_neighbours)
