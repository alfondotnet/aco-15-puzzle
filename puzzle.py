from acoproblem import ACOProblem

import random

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
            idx |= i << (val * 4)


        return idx       
          

    def generateStateFromHash(self, hash):
        
        ''' This receives a hash and generates the state '''
        # Todo


    def calculate_cost(self, state):
        
        ''' calculate_cost:
            Parameters: 
            state = Current state to calculate cost (Remember is a pair State and hole index!)

            Calculate the cost of 'state', by applying the heuristic function from it to the
            solution state
        '''
        
        # TODO
        
        return random.random()
            
            

    def successors(self, state):
      
        ''' 
        Here we determine each state successors
    
        ''' 
        
        pieces,hole = state
        successors = list()
        
        # Now we generate possible successors
        
        # If the hole is on the top edge of the square
        # We are sure that the hole can go down (index + 4)
        if hole < 4 == 0:
            successor = pieces[:] 
            successor[hole],successor[hole+4] = successor[hole+4],0    
            successors.append((successor,hole+4))
        
        # If the hole is in the right edge of the square
        # We are sure the hole can go left (index - 1)
        if hole % 4 == 3:
            successor = pieces[:]
            successor[hole],successor[hole-1] = successor[hole-1],0
            successors.append((successor,hole-1))
            
        # If the hole is on the bottom edge of the square
        # We are sure the hole can go up (index - 4)
        if hole > 11:
            successor = pieces[:]
            successor[hole],successor[hole-4] = successor[hole-4],0
            successors.append((successor,hole-4))
                        
        # If the hole is on the left edge of the square
        # We are sure the hole can go right (index + 1)
        if hole % 4 == 0:
            successor = pieces[:]
            successor[hole],successor[hole+1] = successor[hole+1],0
            successors.append((successor,hole+1))

            
        return successors
        