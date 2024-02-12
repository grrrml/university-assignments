import sys
from queue import Queue
from pythonds.graphs import PriorityQueue


class Vertex:
    def __init__(self, num):
        self.id = num
        self.connectedTo = {}
        self.color = "white"  
        self.dist = sys.maxsize  
        self.pred = None  
        self.disc = 0  
        self.fin = 0

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def setColor(self, color):
        self.color = color

    def setDistance(self, d):
        self.dist = d

    def setPred(self, p):
        self.pred = p

    def setDiscovery(self, dtime):
        self.disc = dtime

    def setFinish(self, ftime):
        self.fin = ftime

    def getFinish(self):
        return self.fin

    def getDiscovery(self):
        return self.disc

    def getPred(self):
        return self.pred

    def getDistance(self):
        return self.dist

    def getColor(self):
        return self.color

    def getConnections(self):
        return self.connectedTo.keys()

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

    def __str__(self):
        return (
            str(self.id)
            + ":color "
            + self.color
            + ":disc "
            + str(self.disc)
            + ":fin "
            + str(self.fin)
            + ":dist "
            + str(self.dist)
            + ":pred \n\t["
            + str(self.pred)
            + "]\n"
        )

    def getId(self):
        return self.id


class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0
        self.time = 0

    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, f, t, cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

    def getEdges(self):
        listOfEdges = []
        for i in self.vertList.values():
            for j in i.connectedTo.keys():
                listOfEdges.append((i.id, j.id))
        return listOfEdges

    def dot_repr(self):
        """Creates a dot representation of the graph

        Returns:
            str: dot representation
        """
        dot = "digraph G { \n"

        for vertex in self.vertList:
            for edge in self.vertList[vertex].getConnections():
                dot += str(vertex) + " -> " + str(edge.id) + "\n"
        return dot + "}"

    def bfs(self, start: Vertex):
        """Breadth-first search

        Args:
            start (Vertex): the starting vertex

        Returns:
            list: list of sorted vertices
        """
        graph_list = []
        start.setDistance(0)
        start.setPred(None)
        queue = Queue()
        queue.put(start)
        while not queue.empty():
            currentVert = queue.get()
            currentVert.setColor("gray")
            for nbr in currentVert.getConnections():
                if nbr.getColor() == "white":
                    nbr.setColor("gray")
                    nbr.setDistance(currentVert.getDistance() + 1)
                    nbr.setPred(currentVert)
                    queue.put(nbr)
            currentVert.setColor("black")
            graph_list.append(currentVert.id)
        return graph_list

    def dfs(self):
        """Depth-first search

        Returns:
            list: list of sorted vertices
            dict:
        """
        ts = {}
        order = []
        for v in self:
            v.setColor("white")
            v.setPred(-1)
        for v in self:
            if v.getColor() == "white":
                self._dfs_recursive(v, ts, order)
        for i in self.vertList:
            ts[self.vertList[i].id] = self.vertList[i].fin

        return order, ts

    def _dfs_recursive(self, start, ts, order):
        """Helper recursive function for dfs

        Args:
            start (Vertex): starting vertex
            times (dict): times dict
            order (list): order list
        """
        start.setColor("gray")
        self.time += 1
        start.setDiscovery(self.time)
        for nextv in start.getConnections():
            if nextv.getColor() == "white":
                nextv.setPred(start)
                self._dfs_recursive(nextv, ts, order)
        start.setColor("black")
        order.append(start.id)
        self.time += 1
        start.setFinish(self.time)

    def topological_sort(self):
        """Graph topological sort

        Returns:
            list: sorted vertices
        """
        order, ts = self.dfs()
        sortd = sorted(ts.items(), key=lambda x: x[1], reverse=True)
        return [sortd[i][0] for i in range(len(sortd))]

    def dijkstra(self, start):
        """Calculates the shorted paths to all vertices from starting vertex

        Args:
            start (Vertex): the starting vertex
        """
        pq = PriorityQueue()
        for v in self:
            v.setDistance(sys.maxsize)
        start.setDistance(0)
        pq.buildHeap([(v.getDistance(), v) for v in self])
        while not pq.isEmpty():
            currentVert = pq.delMin()
            for nextVert in currentVert.getConnections():
                newDist = currentVert.getDistance() + currentVert.getWeight(nextVert)
                if newDist < nextVert.getDistance():
                    nextVert.setDistance(newDist)
                    nextVert.setPred(currentVert)
                    pq.decreaseKey(nextVert, newDist)

    def dijkstra_show(self, start):
        """Prints the distances from start to all vertices

        Args:
            start (Vertex): the starting vertex
        """
        self.dijkstra(start)
        print(f"Costs of paths:")
        for v in self:
            print(f"{start.id} -> {v.id}: {v.getDistance()}")


if __name__ == "__main__":
    G = Graph()
    for i in range(6):
        G.addVertex(i)

    G.addEdge(0, 1, 1)
    G.addEdge(0, 5, 1)
    G.addEdge(1, 2, 1)
    G.addEdge(2, 3, 1)
    G.addEdge(3, 4, 1)
    G.addEdge(3, 5, 1)
    G.addEdge(4, 0, 1)
    G.addEdge(5, 4, 1)
    G.addEdge(5, 2, 1)

    print(f"BFS: {G.bfs(G.getVertex(0))}")
    print(f"DFS: {G.dfs()[0]}")
    print(f"Topological sort: {G.topological_sort()}")
    print("Dot representation:\n" + G.dot_repr())
    G.dijkstra_show(G.getVertex(0))
