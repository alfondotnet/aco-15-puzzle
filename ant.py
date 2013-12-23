

class Ant:
    
    def __init__(self, ant_id):
        
        ''' Ant class
        Id: numerical identifier. starts from 0
        startNode: numerical identifier of the start node
        currentNode: numerical identifier of the current node
        '''
        
        self.id = ant_id
        self.startNode = None # This is assigned on the start function
        self.currentNode = None
        
        self.tabooList = []

    
    def __str__(self):
        
        return "[ Ant no:"+ str(self.id) + ", Start node:"+ str(self.startNode)+", Current node: "+ str(self.currentNode) +" ]"

        
        
        
        
        