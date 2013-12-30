from colony import *
from puzzle import Puzzle
import sys
import networkx as nx
import random

# idea wapa, q cada hormiga vaya pintando su camino en un fichero para ir 
# mostrando el de todas 

inicio = ([2,1,3,4,5,6,7,8,9,10,11,12,13,15,14,0],15)
fin = ([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0],15)

i=0
nants = 20
base_attractiveness = 1

ratio_de_evaporacion = 0.89
cota = 0.8

p1 = Puzzle(inicio, fin, 1, 1, nants, ratio_de_evaporacion, cota, base_attractiveness)

p1.run()


''' 
sols = p1.generateAntSolutions()
if sols != [False for _ in range(len(p1.colony.ants))]:
    print ("Sol encontrada.")
    
    for g in sols:
        if g != False:
            print("\t de tamano: "+ str(len(nx.shortest_path(g,p1.generateNodeHash(inicio),p1.generateNodeHash(fin)))))
    
    break
'''