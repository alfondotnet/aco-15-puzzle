# coding=utf-8
from puzzle import Puzzle
import time

inicio = ([2,1,3,4,5,6,7,8,9,10,11,12,13,15,14,0],15)
fin = ([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0],15)

nants = raw_input("Numero de hormigas: ")
base_attractiveness = raw_input("Atractividad base: ")
initial_tau =  raw_input("Feromona inicial: ")
ratio_de_evaporacion = raw_input("Ratio de evaporacion: ")
cota = raw_input("Cota: ")

alfa = raw_input("Alfa: ")
beta = raw_input("Beta: ")
convergencia_minima = raw_input("Convergencia minima: ")

i = 0

start = time.time()
p1 = Puzzle(inicio, fin, float(alfa), float(beta), int(nants), float(ratio_de_evaporacion), float(cota), float(base_attractiveness), float(initial_tau))

solution = p1.run(int(convergencia_minima))
end = time.time()

if solution == None:
    print("Run again")
else:
    mostrar_solucion = ""
    for s in solution:
        mostrar_solucion += str(s[0])+","
    print("Solution found in "+ str(end-start) + " seconds")
    print("View solution in:")
    print("http://ratslap.com/hormigas/")
    print("Paste this:")
    print(str(mostrar_solucion)[0:-1])