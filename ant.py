

class Ant(object):
    
    def __init__(self, ant_id):
        
        ''' Ant class
        This class is to be run as a multiprocessing Task
        Id: numerical identifier. starts from 0
        startNode: numerical identifier of the start node
        currentNode: numerical identifier of the current node
        '''
        
        self.id = ant_id
        self.startNode = None # This is assigned on the start function
        self.currentNode = None
        
        self.probability_table = dict() # Probability table for each node that this ant has visited


        self.graph =
    
    def __str__(self):
        
        return "[ Ant no:"+ str(self.id) + ", Start node:"+ str(self.startNode)+", Current node: "+ str(self.currentNode) +" ]"

        
    def __call__(self):
    
        ''' __call__ (lookForFood)
            Method to be called by Consumer in a multiprocessing Queue
            Parameters:
            none
            
            The ant looks for a solution of the ACOProblem and when it does find one, 
            return to it's house, giving a positive feedback (depositing pheromone)
            on the path
        '''
        
        
        