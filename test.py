from colony import *
from puzzle import Puzzle


inicio = ([2,1,3,4,5,6,7,8,9,10,11,12,13,15,14,0],15)
fin = ([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0],15)

ratio_de_evaporacion = 0.89

p1 = Puzzle(inicio, fin, 0.5, 0.5, 8, ratio_de_evaporacion)


p1.start()

print(p1.colony)

p1.drawGraph()
