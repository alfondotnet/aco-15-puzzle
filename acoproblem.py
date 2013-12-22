from networkx import *

class ACOProblem(object):
      
    '''Generic class for a generic ACOProblem'''
    
    def __init__(self, initialState, solution, alpha, beta) :      
        '''
        To implement:
        Initialize a new ACOProblem 
        '''
        # First, we create a new colony
        
        
    def objectiveFunction(self):
        raise NotImplementedError()
        '''
        To implement:
        Returns the objective function image associated with a particular
        ACOProblem
        '''
    
    
    def successors(self, state):
        raise NotImplementedError()
        '''
        To override:
        Given a current state, it must return the successors of that state
        '''
    
    def solve(self):
        
        '''
        Solves the Optimization problem
        '''
        
        
        