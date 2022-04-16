import matplotlib.pyplot as plt

import networkx as nx
from queue import PriorityQueue
import time

start_time = time.time()

G = nx.Graph()

file = open("data.csv",'r')
lines = file.readlines()

edges = []

for row in range(0,len(lines[0:]),2):
    header = lines[row]
    header = header[:len(header)-1].split(',')
    header[2] = int(header[2])
    edges.append(tuple(header))
    
#edges = [('a', 'b', 9), ('a', 'd', 2), ('a', 'c', 5), ('d', 'c', 4), 
#         ('d', 'b', 6), ('d', 'e', 4), ('e', 'c', 5), ('e', 'b', 5)]

G.add_weighted_edges_from(edges[:1000])

plt.figure(1)

nx.draw_networkx(G, with_labels = True)
plt.savefig("OriginalGraphPrim.png")

print("!---Original Graph---!")
print("Total number of edges: ", int(G.number_of_edges()))

class Prims:
    def __init__(self):
        self.tree = []
        self.table = {}
        self.queTable = {}
        self.que = PriorityQueue()
    
    def pickRoot(self, node):
        self.rootNode = node
    
    def initializePriorityQueue(self, listOfNodes):
        self.que.put((0,self.rootNode))
        for node in listOfNodes:
            if node != self.rootNode:
                self.que.put((10000,node))
                self.queTable[node] = 10000 
    
    def initializeTable(self, listOfNodes):
        for node in listOfNodes:
            self.table[node] = '-'
        
    def primsAlgo(self, listOfEdges, NoOfNodes):
        while not self.que.empty():
            nextVertex = self.que.get()
            self.tree.append(nextVertex[1])
            for edge in listOfEdges:
                if nextVertex[1] in edge:
                    edge = list(edge)
                    edge.remove(nextVertex[1])
                    edge = tuple(edge)
                    if edge[0] not in self.tree:
                        if edge[1] < self.queTable[edge[0]]:
                            self.queTable[edge[0]] = edge[1]
                            self.table[edge[0]] = nextVertex[1]
                            self.que.put((edge[1],edge[0]))
            if(len(self.tree) == NoOfNodes):
                while not self.que.empty():
                    nextVertex = self.que.get()
                            
    def ShowMST(self):
        MST = nx.Graph()
        
        edges = []
        
        for vertex in self.table.keys():
            if self.table[vertex] != '-':
                edges.append((vertex,self.table[vertex],self.queTable[vertex]))
        
        MST.add_weighted_edges_from(edges)
        plt.figure(2)
        nx.draw_spring(MST, with_labels = True)
        plt.savefig("MSTPrim.png")
        
        
        print("!---Minimum Spanning Tree---!")
        print("Total number of edges: ", int(MST.number_of_edges()))

        
MSTPrims = Prims()
MSTPrims.pickRoot('5')
MSTPrims.initializePriorityQueue(list(G.nodes()))
MSTPrims.initializeTable(list(G.nodes()))
MSTPrims.primsAlgo(edges[:1000], int(G.number_of_nodes()))  
MSTPrims.ShowMST()      
plt.show()
print("\n\nTotal time taken for all processes: ")
print("--- %s seconds ---" % (time.time() - start_time))
file = open("time.csv",'a')
file.write(str(time.time() - start_time))
file.write('\n')
file.close()