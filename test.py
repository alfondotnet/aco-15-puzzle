from colony import *
from puzzle import Puzzle
import sys
import networkx as nx

# idea wapa, q cada hormiga vaya pintando su camino en un fichero para ir 
# mostrando el de todas 

inicio = ([5,1,3,4,2,6,7,8,0,9,10,11,13,14,15,12],8)
#inicio = ([2,1,3,4,5,6,7,8,9,10,11,12,13,15,14,0],15)
#inicio = ([4,2,13,15,12,1,6,0,3,8,9,11,7,10,14,5],7)
fin = ([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0],15)

i=0

while True:
    
    ratio_de_evaporacion = 0.89
    
    p1 = Puzzle(inicio, fin, 1, 1, 8, ratio_de_evaporacion, 0.3)
    p1.start()
    
    sols = p1.generateAntSolutions()
    print (sols)
    if sols != [False for _ in range(len(p1.colony.ants))]:
        print ("Sol encontrada.")
        
        for g in sols:
            if g != False:
                print("\t de tamano: "+ str(len(nx.shortest_path(g,p1.generateNodeHash(inicio),p1.generateNodeHash(fin)))))
        
        break
    '''
    hormiga = p1.colony.ants[0]

    print(hormiga)
    solucion = hormiga.__call__()
    
    if 1147797409030816545 in hormiga.graph.nodes(data=False):
        print("Solucion esta en el grafo")
    if solucion == True:
        print("solucion encontrada!")
        break
        
    i += 1
    '''

#print(p1.colony)
#p1.drawGraph()
