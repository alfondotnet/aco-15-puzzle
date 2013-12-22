

class Ant:
    
    def __init__(self, id):
        
        ''' Ant class
        Id: numerical identifier. starts from 0
        startNode: numerical identifier of the start node
        currentNode: numerical identifier of the current node
        '''
        
        self.id = id
        self.startNode = None # This is assigned on the start function
        self.currentNode = None
        
        self.tabooList = []

    
    def __str__(self):
        return str("["+id+"]")

        
        
        
        
        