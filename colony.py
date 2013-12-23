from ant import Ant


class Colony:
    
    def __init__(self, numberOfAnts):
        
        '''
        Creates an ant colony of 'numberOfAnts' ants
        with 0 from 0 to numberOfAnts - 1
        '''
              
        self.ants = [Ant(i) for i in range(0,numberOfAnts)]
        
            
    def __str__(self):
        
        colony_str = "Our colony has "+ str(len(self.ants)) + " ants.\n"
        
        for ant in self.ants:
            
            colony_str += str(ant) + "\n"
            
        return colony_str
            