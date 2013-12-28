import networkx as nx
import matplotlib.pyplot as plt
import multiprocessing
from aconode import ACONode
from colony import Colony
from random import choice
from consumer import Consumer

'''
acoproblem.py

@Author: Alfonso Perez-Embid (Twitter: @fonsurfing)

'''


class ACOProblem(object):
      
    '''Generic class for a generic ACOProblem'''
    
    def __init__(self, initialStates, solutionStates, alpha, beta, number_of_ants, p, q0) :      
        '''
        Receives a list of initialStates and solutionStates
        To implement:
        Initialize a new ACOProblem 
        '''
        self.initialStates = initialStates
        self.solutionStates = solutionStates
        self.alpha = alpha
        self.beta = beta
        self.p = p # Evaporation rate
        self.q0 = q0 # Parameter of the problem. Indicates the tendency of the ants of exploring or following another ants
        self.graph = None
        self.number_of_ants = number_of_ants
        self.colony = Colony(number_of_ants)  # We create a Colony with n Ants
        
        self.initial_tau = 1
        self.globalSolution = None
        

    def generateNodeHash(self, state):
        raise NotImplementedError()
        '''
        To override:
        Based on the state, we generate an unique integer hash, so we can identify uniquely
        each node of the graph
        '''
        
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
    
    
    def draw_graph(self):
        
        pos=nx.spring_layout(self.graph)
        nx.draw(self.graph,pos,node_color='#A0CBE2',edge_color='#BB0000',width=2,with_labels=True)
        plt.show()
        
    def start(self):
        
        '''
        Starts the problem
        (Creates initial sub-graph,
        places the ants equally in the "start nodes"
        and the rest randomly
        )
        '''
        
        # ========================================
        # Initial Sub-Graph creation
        # ======================================== 
        
        self.graph = nx.Graph()
        
        # Now we place final and initial nodes
                
#         for s in self.solutionStates:
#             
#             node_index = self.generateNodeHash(s)
#             
#             self.graph.add_node(node_index)   
#             self.graph.node[node_index]['node'] = ACONode(s, True) # Solution node
#             self.graph.node[node_index]['solution'] = True
#             self.graph.node[node_index]['initial'] = False
            
            # Pass this node to every ant
#             
#             for ant in self.colony.ants:   
#                 ant.solution_nodes_id.append(node_index)
            
        for s in self.initialStates:
            
            node_index = self.generateNodeHash(s)
            
            self.graph.add_node(node_index)
            self.graph.node[node_index]['node'] = ACONode(s, False, True) # Initial node
            self.graph.node[node_index]['initial'] = True
            self.graph.node[node_index]['solution'] = False
         
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
                    initial_node_id = self.generateNodeHash(s)
                    
                    self.colony.ants[assigned_ant_id].set_start_node(initial_node_id, self.graph)
                    
        # We can make a shared random ant assignment for the rest of the cases
        
        while len(ants_id_list) > 0:
            
            assigned_ant_id = ants_id_list.pop()
            assigned_initial_state = choice(range(0,len(self.initialStates)))
            
            self.colony.ants[assigned_ant_id].set_start_node(assigned_initial_state, self.graph)


    def generateAntSolutions(self):
        
        ''' generateAntSolutions
            Parameters:
            none
            
            Generates different Ant Solutions by executing the respective methods in different
            processes and letting the SO scheduler do the work
        '''
        
        tasks = multiprocessing.JoinableQueue()
        results = multiprocessing.Queue()      
        
        # Start consumers
        
        num_consumers = multiprocessing.cpu_count() * 2
        consumers = [ Consumer(tasks, results) for _ in range(num_consumers) ]  
        
        for w in consumers:
            w.start()
        
        # Now we tell all the ants to go find some food
        
        num_tasks = 0
        
        for ant in self.colony.ants:
            tasks.put(ant)
            num_tasks += 1
        
        # Add a poison pill for each consumer
    
        for _ in range(num_consumers):
            tasks.put(None)
        
        # We wait now for all the ants to finish
        
        tasks.join() 
        results_list = list()
        
        for _ in range(num_tasks):
        
            results_list.append(results.get())
            
        return results_list
        
        
            
    def pheromoneUpdate(self):
        
        ''' pheromoneUpdate
            Parameters:
            none
            
            Update the pheromone on all edges
        '''


    def run(self):
        
        '''
            Parameters:
            none
            
            This is the ACO Algorithm itself
            
        '''
            
        if self.graph == None: 
            raise Exception("The problem must be started first!")
        
        
        while not(self.endCondition()):
        
            solutions = self.generateAntSolutions()
            self.pheromoneUpdate()