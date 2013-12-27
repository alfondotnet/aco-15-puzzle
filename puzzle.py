from acoproblem import ACOProblem
import random

'''
puzzle.py

@Author: Alfonso Perez-Embid (Twitter: @fonsurfing)

'''

class Puzzle(ACOProblem):

    '''
    This class overrides the generic class ACOProblem.im
    To avoid having to look for the "hole" or "empty cell" in each state.
    I am passing the index of hole each time along with the state.
    So, our state is a pair ([state],hole)
    '''
    
    def __init__(self, initialPieces, solution, alpha, beta, number_of_ants, p, q0):
        
        super(Puzzle, self).__init__([initialPieces], [solution], alpha, beta, number_of_ants, p, q0)
        
        # Now we pass the self to every ant so they know how to expand the graph.
        
        for ant in self.colony.ants:
            
            ant.aco_specific_problem = self

    def endCondition(self):
        '''
        Here we have to determine when we have to end.
        '''
        # TODO
        return self.globalSolution < 30
    
    def generateNodeHash(self, state):
        
        ''' generateNodeHash
            Parameters:
            state
            
            Based on the state, we generate an unique integer hash, so we can identify uniquely
            each node of the graph
        '''
        idx = 0
        state_tiles = state[0]

        for i in range(16):
            
            val = state_tiles[i]
            idx |= val << (i * 4)


        return idx       
          

    def generateStateFromHash(self, hash):
        
        ''' This receives a hash and generates the state '''
        
        hex = "{0:016x}".format(hash)[::-1] # we convert the number to hex and reverse it
        list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        
        for i,h in enumerate(hex):    
            digits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
            list[i] = digits.index(h)

        return (list,list.index(0))


    def calculate_cost(self, state):
        
        ''' calculate_cost:
            Parameters: 
            state = Current state to calculate cost (Remember is a pair State and hole index!)

            Calculate the cost of 'state', by applying the heuristic function from it to the
            solution state
        '''
        
        solution = self.solutionStates[0]
        cost = 0
        
        def distance_between_array_indexes(index_from,index_to):
            
            ''' given two indexes of the 15-puzzle array, return 
                their manhattan distance
                
                1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0
                
                1  2  3  4
                5  6  7  8
                9 10 11 12
                1314 15 0
                
            '''
            
            def index_to_ij(index):     
                return (index%4,index/4)
                
            ij1 = index_to_ij(index_from)
            ij2 = index_to_ij(index_to)
            
            return abs(ij2[0] - ij1[0]) + abs(ij2[1] - ij1[1])
    
        for i in range(16):

            cost += distance_between_array_indexes(solution[0][i], state[0][i])
        
        return cost + self.number_of_linear_conflicts(state)*2
        
        
    def number_of_linear_conflicts(self, state):
        '''
        Calculates the number of linear conflicts of a state
        '''
        state_tiles = state[0]
        
        def number_lc(state,line,row):
            ''' given a line (0-3) return the number of linear conflicts in it
                row = True means a row otherwise a column
            '''
            index_from = line * 4 if row else line%4
            index_to = index_from + 4 if row else index_from+13
            pass_range = 1 if row else 4
            
            linear_conflicts = 0
            
            for tile in range(index_from,index_to,pass_range):
                for other_tile in range(index_from,index_to,pass_range):
                    if tile != other_tile:
                        goal_tile = self.solutionStates[0][0].index(state[tile])
                        goal_other_tile = self.solutionStates[0][0].index(state[other_tile])
                        if index_from <= goal_tile <= index_to and \
                        index_from <= goal_other_tile <= index_to:
                            # now check if tile is to the left of other_tile and its goal is to the right of
                            # other_tile     
                            if tile < other_tile and goal_tile > goal_other_tile:
                                linear_conflicts += 1
                                
            return linear_conflicts
                
        linear_conflicts = 0
        
        for line in range(0,4):
            linear_conflicts += number_lc(state_tiles, line, True)
            linear_conflicts += number_lc(state_tiles, line, False)
        
        return linear_conflicts         

    
    def successors(self, state):
      
        ''' 
        Here we determine each state successors
    
        ''' 
        
        pieces,hole = state
        successors = list()
        
        potential_movements = dict({'up':True,'right':True,'down':True,'left':True})
        
        
        # Now we eliminate the potential movements
        
        if hole < 4:
            potential_movements['up'] = False
            
        if hole % 4 == 3:
            potential_movements['right'] = False
            
        if hole > 11: 
            potential_movements['down'] = False    
         
        if hole % 4 == 0: 
            potential_movements['left'] = False 
            
            
        if potential_movements['down']:
            successor = pieces[:] 
            successor[hole],successor[hole+4] = successor[hole+4],0    
            successors.append((successor,hole+4))
        

        if potential_movements['left']:
            successor = pieces[:]
            successor[hole],successor[hole-1] = successor[hole-1],0
            successors.append((successor,hole-1))
            

        if potential_movements['up']:
            successor = pieces[:]
            successor[hole],successor[hole-4] = successor[hole-4],0
            successors.append((successor,hole-4))
                        

        if potential_movements['right']:
            successor = pieces[:]
            successor[hole],successor[hole+1] = successor[hole+1],0
            successors.append((successor,hole+1))

            
        return successors
        