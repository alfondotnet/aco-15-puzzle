import networkx as nx
import matplotlib.pyplot as plt


class ACOProblem(object):
      
    '''Generic class for a generic ACOProblem'''
    
    def __init__(self, initialState, solutionState, alpha, beta) :      
        '''
        To implement:
        Initialize a new ACOProblem 
        '''
        self.graph = nx.Graph()
        self.graph.add_node(1) # Initial
        self.graph.add_node(0) # Solution
        
        self.graph.node[1]['state'] = initialState
        self.graph.node[0]['state'] = solutionState
        
        
        # TODO:
        # This in here?    
        
        first_successors = [s for s in self.successors(initialState)]
        
        for i,successor_state in enumerate(first_successors):
            
            successor_index = self.graph.number_of_nodes()+i
            self.graph.add_node(successor_index)
            self.graph.node[successor_index]['state'] = successor_state
            self.graph.add_edge(1,successor_index)
            
        
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
    
    
    def drawGraph(self):
        
        pos=nx.spring_layout(self.graph)
        nx.draw(self.graph,pos,node_color='#A0CBE2',edge_color='#BB0000',width=2,with_labels=True)
        plt.show()
        
    def solve(self):
        
        '''
        Solves the Optimization problem
        '''
    
        
        