import matplotlib.pyplot as plt

import networkx as nx
from queue import PriorityQueue
import time

start_time = time.time()

G = nx.DiGraph()

file = open("data.csv",'r')
lines = file.readlines()

edges = []

for row in range(0,len(lines[0:]),2):
    header = lines[row]
    header = header[:len(header)-1].split(',')
    header[2] = int(header[2])
    edges.append(tuple(header))
    
#edges = [('A', 'B', 4), ('A', 'D', 1), ('B', 'D', 4), ('B', 'C', 4), 
 #        ('B', 'J', 10), ('D', 'H', 5), ('D', 'J', 6), ('H', 'J', 2),
  #       ('J','I',3),('C','E',2),('C','F',1),('E','G',2),('F','G',3),
   #      ('G','I',3),('G','J',4),('F','I',5)]

G.add_weighted_edges_from(edges[:1000])

plt.figure(1)

nx.draw_networkx(G, with_labels = True)
plt.savefig("OriginalGraphKruskal.png")

print("!---Original Graph---!")
print("Total number of nodes: ", int(G.number_of_nodes()))
print("Total number of edges: ", int(G.number_of_edges()))

class Kruskal:
    def __init__(self, n):
        self.forest = []
        self.edgesQueue = PriorityQueue()
        self.edgeadded = 1
        self.numberOfNodes = n
        self.MSTEdges = []
    
    def initializeForest(self, Vertices):
        for v in Vertices:
            self.forest.append((v,))
    
    def addEdgesInPriorityQueue(self, listOfEdges):
        for edge in listOfEdges:
            self.edgesQueue.put((edge[2],edge[:2]))
        
    def kruskalAlgo(self):
        while self.edgeadded < self.numberOfNodes and not self.edgesQueue.empty():
            cheapestEdge = self.edgesQueue.get()
            
            edge = cheapestEdge[1]
          
            reject = False
            for tree in self.forest:
                if edge[0] in tree and edge[1] in tree:         # Forms a cycle reject this edge
                    reject = True
            
            if not reject:
                tree1 = None
                tree2 = None
                for tree in self.forest:
                    if edge[0] in tree:
                        tree1 = tree
                    elif edge[1] in tree:
                        tree2 = tree
                self.forest.remove(tree1)
                self.forest.remove(tree2)
                newTree = tree1 + tree2              
                self.forest.append(newTree)
                edge = edge + (cheapestEdge[0],)
                self.MSTEdges.append(edge)
                self.edgeadded += 1
        
    def showMST(self):
        MST = nx.DiGraph()
        
        MST.add_weighted_edges_from(self.MSTEdges)
        plt.figure(2)
        nx.draw_spring(MST, with_labels = True)
        plt.savefig("MSTKruskal.png")
        
        print("!---Minimum Spanning Tree---!")
        print("Total number of nodes: ", int(MST.number_of_nodes()))
        print("Total number of edges: ", int(MST.number_of_edges()))
            
MSTKrus = Kruskal(G.number_of_nodes())
MSTKrus.initializeForest(G.nodes())
MSTKrus.addEdgesInPriorityQueue(edges[:1000])
MSTKrus.kruskalAlgo()
MSTKrus.showMST()
print("\n\nTotal time taken for all processes: ")
print("--- %s seconds ---" % (time.time() - start_time))
file = open("time.csv",'a')
file.write(str(time.time() - start_time))
file.write('\n')
file.close()