from acoproblem import ACOProblem

class Puzzle(ACOProblem):

    '''
    This class overrides the generic class ACOProblem.
    To avoid having to look for the "hole" or "empty cell" in each state.
    I am passing the index of hole each time along with the state.
    So, our state is a pair ([state],hole)
    '''
    
    def __init__(self, initialPieces, solution, alpha, beta):
        super(Puzzle, self).__init__(initialPieces, solution, alpha, beta)
        
      
    ''' 
    Here we determine each state successors
    For example:
    
    1   2   3   4
    5   6   7   8
    9  10  11  12
    13 14  15  0
    
    Will have
    
    1   2   3   4            1   2   3   4 
    5   6   7   8   and      5   6   7   8
    9  10  11  12            9  10  11   0
    13 14  0   15           13  14  15  12
    
    as successors.
    
    '''   
    def successors(self, state):

        pieces,hole = state
        successors = list()
        
        # Now we generate possible successors
        
        # If the hole is on the top edge of the square
        # We are sure that the hole can go down (index + 4)
        if hole < 4 == 0:
            successor = pieces[:] 
            successor[hole],successor[hole+4] = successor[hole+4],0    
            successors.append(successor)
        
        # If the hole is in the right edge of the square
        # We are sure the hole can go left (index - 1)
        if hole % 4 == 3:
            successor = pieces[:]
            successor[hole],successor[hole-1] = successor[hole-1],0
            successors.append(successor)
            
        # If the hole is on the bottom edge of the square
        # We are sure the hole can go up (index - 4)
        if hole > 11:
            successor = pieces[:]
            successor[hole],successor[hole-4] = successor[hole-4],0
            successors.append(successor)
                        
        # If the hole is on the left edge of the square
        # We are sure the hole can go right (index + 1)
        if hole % 4 == 0:
            successor = pieces[:]
            successor[hole],successor[hole+1] = successor[hole+1],0
            successors.append(successor)

            
        return successors
        