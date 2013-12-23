import networkx as nx
from aconode import ACONode

class Ant(object):
    
    def __init__(self, ant_id):
        
        ''' Ant class
        This class is to be run as a multiprocessing Task
        Id: numerical identifier. starts from 0
        startNode: numerical identifier of the start node
        currentNode: numerical identifier of the current node
        '''
        
        self.id = ant_id
        self.start_node_id = None # This is assigned on the start function of ACOProblem
        self.current_node_id = None # This is assigned on the start function of ACOProblem
        self.solution_nodes_id = list() # This is assigned on the start function of ACOProblem
        
        
        self.graph = None # Each ant creates it's own graph at first in setStartNode
        
        self.probability_table = dict() # Probability table for each node that this ant has visited

        self.puzzle = None # It's going to be passed by Puzzle in the __init__ so the ant knows
        # How to expand the graph and so on
        
    
    def setStartNode(self, startNode):
        
        self.startNode = startNode
        self.currentNode = startNode
        self.graph = nx.Graph()
        self.graph.add_node(self.puzzle.generateNodeHash(startNode))
        
        
    def __str__(self):
        
        return "[ Ant no:"+ str(self.id) + ", Start node:"+ str(self.start_node_id)+", Current node: "+ str(self.current_node_id) +" ]"

        
    def __call__(self):
        
        if self.puzzle == None:
            
            raise Exception ("You have to pass an instance of your puzzle to every ant of the colony first!")
    
        ''' __call__ (lookForFood)
            Method to be called by Consumer in a multiprocessing Queue
            Parameters:
            none
            
            The ant looks for a solution of the ACOProblem and when it does find one, 
            return to it's house, giving a positive feedback (depositing pheromone)
            on the path
        '''
        
        
    def expandNodes(self, node_indexes_to_expand):
        
        ''' expandNode
            Parameters:
            node_index: Indexes of nodes to expand
            
            Expands some nodes. (creates successor nodes
            and add edges from/to their parents and them).
        '''
        
        for n in node_indexes_to_expand:
            
            node_to_expand = self.graph.node[n]['node']
            
            successors = self.puzzle.successors(node_to_expand.state)

            for s in successors:
                
                successor_index = self.graph.number_of_nodes()
          
                self.graph.add_node(successor_index)
                self.graph.node[successor_index]['node'] = ACONode(s)
                self.graph.add_edge(n,successor_index, weight=self.initial_tau)    
                
        
        
        