
'''
aconode.py

@Author: Alfonso Perez-Embid (Twitter: @fonsurfing)

'''


class ACONode():
    
    ''' Class for a ACO Node '''
    
    def __init__(self, state, solution=False, start=False):
        
        self.state = state
        self.solution = solution
        self.start = start
        
    def __eq__(self,other):
        
        return (isinstance(other, ACONode) and self.state == other.state)
    
    def __ne__(self,other):
        
        return not(self.__eq__(other))
    