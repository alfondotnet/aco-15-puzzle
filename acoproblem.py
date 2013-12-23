import networkx as nx
import matplotlib.pyplot as plt
from aconode import ACONode
from colony import Colony
from random import choice

class ACOProblem(object):
      
    '''Generic class for a generic ACOProblem'''
    
    def __init__(self, initialStates, solutionStates, alpha, beta, number_of_ants) :      
        '''
        Receives a list of initialStates and solutionStates
        To implement:
        Initialize a new ACOProblem 
        '''
        self.initialStates = initialStates
        self.solutionStates = solutionStates
        self.alpha = alpha
        self.beta = beta
        self.graph = None
        self.number_of_ants = number_of_ants
        self.colony = Colony(number_of_ants)  # We create a Colony with n Ants
        
        self.initial_tau = 1
        self.globalSolution = None
        
        
    def objectiveFunction(self):
        raise NotImplementedError()
        '''
        To implement:
        Returns the objective function image associated with a particular
        ACOProblem
        '''
    
    def endCondition(self):
        raise NotImplementedError()
    
        '''
        To override. 
        Checks after each iteration if the algorithm has ended
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
        
    def start(self):
        
        '''
        Starts the problem
        (Creates initial sub-graph,
        places the ants equally in the "start nodes"
        )
        '''
        
        # ========================================
        # Initial Sub-Graph creation
        # ======================================== 
        
        self.graph = nx.Graph()
        
        # Now we place final and initial nodes
        # In our particular problem, the only solution state will have 0 as index
        # Because solutionState list has only one component
        
        for i,s in enumerate(self.solutionStates):
        
            self.graph.add_node(i)   
            self.graph.node[i]['node'] = ACONode(s, True) # Solution node
            self.graph.node[i]['solution'] = True
            self.graph.node[i]['initial'] = False
            
        first_index = self.graph.number_of_nodes()
        
        for i,s in enumerate(self.initialStates):
            
            self.graph.add_node(i+first_index)
            self.graph.node[i+first_index]['node'] = ACONode(s, False, True) # Initial node
            self.graph.node[i+first_index]['initial'] = True
            self.graph.node[i+first_index]['solution'] = False
         
        # ========================================
        # Initial Ants placement
        # ========================================   
        # Now we have to place "numberOfAnts" ants equally in the StartNodes
        # We use this criteria to place the ants:
        # If the number of ants is greater than the number of Initial Nodes,
        # then we assign numberOfAnts % len(initialStates) ants equally
        # and the rest randomly
        
        # Otherwise we assign randomly
        
        ants_id_list = [i for i in range(self.number_of_ants)]
        
        if self.number_of_ants > len(self.initialStates):
            
            # We make sure each initial node has one ant
            # We break the loop when there is no more empty initialNodes
            # We assign the rest randomly
            
            while len(ants_id_list) > 0 and (len(ants_id_list) % len(self.initialStates) == 0):
                
                for s in self.initialStates:
                    
                    assigned_ant_id = ants_id_list.pop()
                    self.colony.ants[assigned_ant_id].startNode = assigned_ant_id
                    self.colony.ants[assigned_ant_id].currentNode = assigned_ant_id
                
        # We can make a shared random ant assignment for the rest of the cases
        
        while len(ants_id_list) > 0:
            
            assigned_ant_id = ants_id_list.pop()
            assigned_initial_state = choice(range(0,len(self.initialStates)))
            
            self.colony.ants[assigned_ant_id].startNode = assigned_initial_state
            self.colony.ants[assigned_ant_id].currentNode = assigned_initial_state
        

    def expandNodes(self, node_indexes_to_expand):
        
        ''' expandNode
            Parameters:
            node_index: Indexes of nodes to expand
            
            Expands some nodes
        '''
        
        for n in node_indexes_to_expand:
            
            successors = self.successors(n.state)

            for s in successors:
                
                successor_index = self.graph.number_of_nodes()+1
          
                self.graph.add_node(successor_index)
                self.graph.node[successor_index]['node'] = ACONode(s)
                self.graph.add_edge(1,successor_index, weight=self.initial_tau)
            
        

    def run(self):
            
        if self.graph == None: 
            raise("The problem must be started first!")
        
        
        while not(self.endCondition()):
        
            a="a" 