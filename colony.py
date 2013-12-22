from ant import Ant


class Colony:
    
    def __init__(self, numberOfAnts):
        
        '''
        Creates an ant colony of 'numberOfAnts' ants
        '''
        
        self.ants = [Ant(i) for i in range(1,numberOfAnts)]
        
        
    def __str__(self):
        return str(self.ants[0])