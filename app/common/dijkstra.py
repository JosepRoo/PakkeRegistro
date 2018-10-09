import queue
from collections import namedtuple

Edge = namedtuple('Edge', ['vertex', 'weight', 'description'])


class GraphUndirectedWeighted:
    def __init__(self, vertex_count):
        self.vertex_count = vertex_count
        self.adjacency_list = [[] for _ in range(vertex_count)]

    def add_edge(self, source, dest, weight, description):
        assert source < self.vertex_count
        assert dest < self.vertex_count
        self.adjacency_list[source].append(Edge(dest, weight, description))

    def get_edge(self, vertex):
        for e in self.adjacency_list[vertex]:
            yield e

    def get_vertex(self):
        for v in range(self.vertex_count):
            yield v

    def dijkstra(self, source, dest):
        q = queue.PriorityQueue()
        parents = []
        distances = []
        start_weight = float("inf")
        descs = []
        for i in self.get_vertex():
            weight = start_weight
            if source == i:
                weight = 0
            distances.append(weight)
            parents.append(None)
            descs.append(None)

        q.put(([0, source]))

        while not q.empty():
            v_tuple = q.get()
            v = v_tuple[1]

            for e in self.get_edge(v):
                candidate_distance = distances[v] + e.weight
                if distances[e.vertex] > candidate_distance:
                    distances[e.vertex] = candidate_distance
                    parents[e.vertex] = v
                    descs[e.vertex] = e.description
                    q.put(([distances[e.vertex], e.vertex]))

        # shortest_path = []
        result_path = []
        end = dest
        while end is not None:
            # shortest_path.append(end)
            result_path.append(descs[end]) if descs[end] is not None else None
            end = parents[end]

        # shortest_path.reverse()

        return distances[dest], result_path
