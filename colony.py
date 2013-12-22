from ant import Ant


class Colony:
    
    def __init__(self, numberOfAnts):
        
        '''
        Creates an ant colony of 'numberOfAnts' ants
        with 0 from 0 to numberOfAnts - 1
        '''
              
        self.ants = [Ant(i) for i in range(0,numberOfAnts)]
        
            
    def __str__(self):
        
        return str(self.ants[0])