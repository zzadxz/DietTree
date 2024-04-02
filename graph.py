""" This file houses the Graph and WeightedGraph classes and the load_weighted_graph method. This marks the
technical backbone of our code and where much of the data analysis comes from.
"""
from __future__ import annotations
from typing import Any, Union, Optional
import pandas as pd
from vertex import Vertex
from vertex import WeightedVertex


class Graph:
    """
    A graph used to represent a book review network.
    """
    # Private Instance Attributes:
    #     - vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to vertex object.
    vertices: dict[Any, Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self.vertices = {}

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'food', 'dessert', 'drink', 'category'}
        """
        if item not in self.vertices:
            self.vertices[item] = Vertex(item, kind)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            v2 = self.vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self.vertices:
            v = self.vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'food', 'dessert', 'drink', 'category'}
        """
        if kind != '':
            return {v.item for v in self.vertices.values() if v.kind == kind}
        else:
            return set(self.vertices.keys())


class WeightedGraph(Graph):
    """A weighted graph used to represent a book review network that keeps track of review scores.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _WeightedVertex object.
    _vertices: dict[Any, WeightedVertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

        # This call isn't necessary, except to satisfy PythonTA.
        Graph.__init__(self)

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'food', 'dessert', 'drink', 'category'}
        """
        if item not in self._vertices:
            self._vertices[item] = WeightedVertex(item, kind)

    def add_edge(self, item1: Any, item2: Any, weight: Union[int, float] = 1) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def get_weight(self, item1: Any, item2: Any) -> Union[int, float]:
        """Return the weight of the edge between the given items.

        Return 0 if item1 and item2 are not adjacent.

        Preconditions:
            - item1 and item2 are vertices in this graph
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]
        return v1.neighbours.get(v2, 0)

    def average_weight(self, item: Any) -> float:
        """Return the average weight of the edges adjacent to the vertex corresponding to item.

        Raise ValueError if item does not corresponding to a vertex in the graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return sum(v.neighbours.values()) / len(v.neighbours)
        else:
            raise ValueError

    def get_similarity_score(self, item1: Any, item2: Any,
                             score_type: str = 'unweighted') -> float:
        """Return the similarity score between the two given items in this graph.

        score_type is one of 'unweighted' or 'strict', corresponding to the
        different ways of calculating weighted graph vertex similarity, as described
        on the assignment handout.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - score_type in {'unweighted', 'strict'}
        """

        if item1 not in self._vertices or item2 not in self._vertices:
            raise ValueError

        vertex1 = self._vertices[item1]
        vertex2 = self._vertices[item2]

        if score_type == 'unweighted':
            return vertex1.similarity_score_unweighted(vertex2)
        elif score_type == 'strict':
            return vertex1.similarity_score_strict(vertex2)
        else:
            raise ValueError

    def recommend_books(self, food: str, limit: int,
                        score_type: str = 'unweighted') -> list[str]:  # TODO (do we even need this?)
        """Return a list of up to <limit> recommended books based on similarity to the given book.

        score_type is one of 'unweighted' or 'strict', corresponding to the
        different ways of calculating weighted graph vertex similarity, as described
        on the assignment handout. The corresponding similarity score formula is used
        in this method (whenever the phrase "similarity score" appears below).

        The return value is a list of the titles of recommended books, sorted in
        *descending order* of similarity score. Ties are broken in descending order
        of book title. That is, if v1 and v2 have the same similarity score, then
        v1 comes before v2 if and only if v1.item > v2.item.

        The returned list should NOT contain:
            - the input book itself
            - any food items with a similarity score of 0 to the input book
            - any duplicates
            - any vertices that represents a user (instead of a book)

        Up to <limit> books are returned, starting with the book with the highest similarity score,
        then the second-highest similarity score, etc. Fewer than <limit> books are returned if
        and only if there aren't enough books that meet the above criteria.

        Preconditions:
            - food in self._vertices
            - self._vertices[food].kind in {'food', 'dessert', 'drink'}
            - limit >= 1
            - score_type in {'unweighted', 'strict'}
        """

        if food not in self._vertices or self._vertices[food].kind != 'book':
            raise ValueError

        book_vertex = self._vertices[food]
        scores = []

        for other in self._vertices.values():
            if other.kind in {'food', 'dessert', 'drink'} and other.item != food:
                if score_type == 'unweighted':
                    score = book_vertex.similarity_score_unweighted(other)
                elif score_type == 'strict':
                    score = book_vertex.similarity_score_strict(other)
                else:
                    raise ValueError

                if score > 0:
                    scores.append((score, other.item))

        scores.sort(key=lambda x: x[1])
        scores.sort(key=lambda x: x[0], reverse=True)

        recommendations = [title for _, title in scores][:limit]
        return recommendations


def convert_to_increment(value: str, increment: int) -> Optional[float]:
    """Helper function to convert nutritional values into specified increments."""
    try:
        value = float(value.replace(' g', '').replace('mg', ''))
        return round(value / increment) * increment
    except (ValueError, TypeError):
        return None


def preprocess_dataframe(df: pd.DataFrame, categories: dict[str, int]) -> pd.DataFrame:
    """Preprocess the dataframe to adjust nutritional values based on increments."""
    for category, increment in categories.items():
        df[category] = df[category].apply(lambda x: convert_to_increment(x, increment))
    return df.dropna(subset=categories.keys(), how='all')


def add_nutritional_edges(row: pd.Series, graph: WeightedGraph, categories: dict[str, int],
                          weights: dict[str, int]) -> None:
    """Adds all the required edges between vertices initialized from each row in our csv"""
    item_name = row['Item']
    item_category = row['Category'].lower()
    item_data = row.to_dict()  # Convert the row to a dictionary for vertex data

    # Pass item_data when adding a vertex
    if item_name not in graph.get_all_vertices():
        graph.add_vertex(item_data, item_category)

    for category in categories.keys():
        value = row[category]
        if pd.notna(value):
            category_vertex = f"{category}_{value}"
            if category_vertex not in graph.get_all_vertices():
                graph.add_vertex(category_vertex, category)
            weight = weights.get(category, 1)  # Use default weight of 1 if not specified
            graph.add_edge(item_name, category_vertex, weight)


def load_weighted_review_graph(food_file: str, categories: dict[str, int], weights: dict[str, int]) -> WeightedGraph:
    """Return a book review WEIGHTED graph corresponding to the given datasets.

    This should be very similar to the corresponding function from Exercise 3, except now
    the book review scores are used as edge weights.

    Preconditions:
        - reviews_file is the path to a CSV file corresponding to the food datase
    """
    graph = WeightedGraph()
    df = pd.read_csv(food_file)

    valid_categories = ['dessert', 'food', 'drink']
    df = df[df['Category'].str.lower().isin(valid_categories)]

    df_filtered = preprocess_dataframe(df, categories)
    for _, row in df_filtered.iterrows():
        add_nutritional_edges(row, graph, categories, weights)

    return graph


if __name__ == '__main__':
    # You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # # increases the running time of the functions/methods.
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
