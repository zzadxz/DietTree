"""The file houses our implementation of the vertex and weighted vertex classes. These are essential to our
implementation of our graph classes."""
from __future__ import annotations
from typing import Any, Union


class Vertex:
    """
    Represents a vertex in a graph used in the context of modeling a network where vertices
    can represent entities such as food items, drinks, desserts, or categories. This
    class allows to make relationships (edges) to other vertices to indicate
    connections between these entities based on predefined criteria (e.g., nutritional similarities, etc).

    Attributes:
        - item (Any): The data stored in this vertex (food item name, macros, etc).
        - kind (str): A string indicating the type of entity this vertex represents. Expected values
                      include 'food', 'dessert', 'drink', or 'category'.
        - neighbours (set[Vertex]): A set of other Vertex instances that are directly connected to
                      this vertex within the graph.

    Preconditions:
        - item is unique within the graph.
        - kind in {'food', 'dessert', 'drink', 'category'}.
        - self not in self.neighbours.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
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


class WeightedVertex(Vertex):
    """
    Extends the Vertex class to include weighted edges, which represent the strength or degree
    of relationship between this vertex and its neighbours. In the context of a food application,
    these weights can represent nutritional similarity or other criteria that determine how closely
    related two food items or categories are.

    Attributes:
        - item (Any): The food item or category this vertex represents.
        - kind (str): The type of entity this vertex represents, such as 'food', 'dessert', 'drink',
                      or 'category'.
        - neighbours (dict[WeightedVertex, Union[int, float]]): A dictionary where keys are
                      instances of WeightedVertex representing the connected vertices, and values
                      are the weights (int or float) indicating the strength of the relationship.

    Preconditions:
        - item is unique within the graph.
        - kind in {'food', 'dessert', 'drink', 'category'}.
        - self not in self.neighbours.keys().
        - All weights are positive numbers.

    Representation Invariants:
        - self not in self.neighbours
        - all(weight > 0 for weight in self.neighbours.values())
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Any
    kind: str
    range: range
    neighbours: dict[WeightedVertex, Union[int, float]]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - self.kind in {'calories', 'protein', 'carbs', 'fat', 'sugars'}
        """
        super().__init__(item, kind)
        self.neighbours = {}

    def vertex_similarity_score(self, other: WeightedVertex, weightings: dict[str, float]) -> float:
        """
        Calculates and returns the similarity score between this vertex and another weighted vertex,
        based on their connected neighbours and the specified weighting criteria. This score can be
        used to determine the closeness or compatibility between two food items or categories by taking
        into account various nutritional or categorical aspects as defined by the weightings.

        Parameters:
            - other: Another instance of WeightedVertex to compare against this vertex.
            - weightings: A dictionary where keys are the kinds of vertices (e.g., 'protein', 'carbs')
                          and values are floats representing the importance or weight of that kind
                          in calculating the similarity score.

        Preconditions:
            - self.kind in {'food', 'dessert', 'drink'} and other.kind in the same set.
            - All values in weightings are positive numbers.
            - self and other have at least one common neighbour kind specified in weightings.

        Postconditions:
            - The returned score is >= 0.
            - The score reflects the weighted relationship based on common neighbours and the specified
              weightings. A higher score indicates greater similarity.

        Representation Invariants:
            - weightings.keys().issubset({'protein', 'carbs', 'fat', 'calories', 'sugars'})
            - all(weight > 0 for weight in weightings.values())
        """

        if weightings is None:
            weightings = {}
        similarity = 0
        shared_neighbours = set(self.neighbours.keys()).intersection(set(other.neighbours.keys()))

        for v in shared_neighbours:
            similarity += 1 * weightings[v.kind]
        return similarity


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()
    import doctest
    doctest.testmod(verbose=True)
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136', 'W0221'],
        'extra-imports': ['csv', 'networkx', 'pandas'],
        'max-nested-blocks': 4,
    })
