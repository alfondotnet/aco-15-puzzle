# coding=utf-8
import networkx as nx
import matplotlib.pyplot as plt

from aconode import ACONode
from colony import Colony
from random import choice
import math

'''
acoproblem.py

@Author: Alfonso Perez-Embid (Twitter: @fonsurfing)

'''

class ACOProblem(object):
      
    '''Generic class for a generic ACOProblem'''
    
    def __init__(self, initial_states, solution_states, alpha, beta, number_of_ants, p, q0, base_attractiveness, initial_tau, initial_estimate) :      
        '''
        Receives a list of initial_states and solution_states
        To implement:
        Initialize a new ACOProblem 
        '''
        self.initial_states = initial_states
        self.solution_states = solution_states
        self.alpha = alpha
        self.beta = beta
        self.p = p # Evaporation rate
        self.q0 = q0 # Parameter of the problem. Indicates the tendency of the ants of exploring or following another ants
        self.base_attractiveness = base_attractiveness # Parameter Q
        self.global_graph = None # This is our global graph
        self.number_of_ants = number_of_ants
        self.colony = Colony(self.number_of_ants)  # We create a Colony with n Ants
        
        self.initial_tau = initial_tau
        
        self.estimate = initial_estimate
        
        self.global_best_solution = None

    def generate_node_hash(self, state):
        raise NotImplementedError()
        '''
        To override:
        Based on the state, we generate an unique integer hash, so we can identify uniquely
        each node of the graph
        '''
        
    def objective_function(self, solution):
        raise NotImplementedError()
        '''
        To implement:
        Returns the objective function image associated with a particular
        ACOProblem solution
        '''
    
    def end_condition(self):
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

            
    def pheromone_update_criteria(self, solution):
        raise NotImplementedError()
        ''' To override
            pheromone_update_criteria
            Parameters:
            none
            Given a solution
            Returns the new pheromone associated for that solution
        '''

    
    def draw_graph(self):
        
        pos=nx.spring_layout(self.global_graph)
        nx.draw(self.global_graph,pos,node_color='#A0CBE2',edge_color='#BB0000',width=2,with_labels=True)
        plt.show()
        

    def initial_graph_creation(self):
        
        '''
        # Initial graph creation
        Parameters: 
        none
        '''
        
        self.global_graph = nx.Graph()
        # Now we place final node
            
        for s in self.initial_states:
            
            node_index = self.generate_node_hash(s)
            
            self.global_graph.add_node(node_index)
            self.global_graph.node[node_index]['node'] = ACONode(s, False, True) # Initial node

        
    def ant_placement(self):
        
        '''
        ant_placement
        places the ants equally in the "start nodes" of self.global_graph
        and the rest randomly
        '''    

        # We use this criteria to place the ants:
        # If the number of ants is greater than the number of Initial Nodes,
        # then we assign numberOfAnts % len(initial_states) ants equally
        # and the rest randomly
        
        # Otherwise we assign randomly
           
        ants_id_list = [i for i in range(self.number_of_ants)]
        
        if self.number_of_ants > len(self.initial_states):
            
            # We make sure each initial node has one ant
            # We break the loop when there is no more empty initialNodes
            # We assign the rest randomly
            
            while len(ants_id_list) > 0 and (len(ants_id_list) % len(self.initial_states) == 0):
                
                for s in self.initial_states:
                    
                    assigned_ant_id = ants_id_list.pop()
                    initial_node_id = self.generate_node_hash(s)
                    
                    self.colony.ants[assigned_ant_id].set_start_node(initial_node_id, self.global_graph)
                    
        # We can make a shared random ant assignment for the rest of the cases
        
        while len(ants_id_list) > 0:
            
            assigned_ant_id = ants_id_list.pop()
            assigned_initial_state = choice(range(0,len(self.initial_states)))
            
            self.colony.ants[assigned_ant_id].set_start_node(self.generate_node_hash(self.initial_states[assigned_initial_state]), self.global_graph)



    def generate_ant_solutions_mono(self):
        
        while True:

            self.ant_placement()

            list_results_ants = list()
            
            for ant in self.colony.ants:
                sol = ant.__call__()
                list_results_ants.append(sol)

                      
            if [r[1] for r in list_results_ants] != [False for _ in range(len(self.colony.ants))]:
                #print (list_results_ants)
                return [r for (r,b) in list_results_ants if b != False]
                
    
    

    def update_graph_mono(self, list_solutions):
        
        ''' update__graph_mono
            Parameters:
            list_solutions: A list of paths returned by different ants
            A path is a list of NODES (not node indexes)
            Given a list of solutions (list of paths), updates the global graph.
            
            Return:
            Returns a list of graphs of the solutions
            
            I am going to try to do all in here
        '''

        for sol in list_solutions:
            
            positive_feedback = self.pheromone_update_criteria(sol)

            for node_index in range(len(sol)):
                
                if node_index == len(sol)-1:
                    break
                
                this_node = sol[node_index]
                next_node = sol[node_index+1]
                
                self.global_graph.add_edge(this_node[0],next_node[0]) # if exists doesnt override the data
                
                try:             
                    self.global_graph.edge[this_node[0]][next_node[0]]['weight'] += positive_feedback
                except KeyError:
                    self.global_graph.edge[this_node[0]][next_node[0]]['weight'] = positive_feedback
                

                self.global_graph.edge[this_node[0]][next_node[0]]['weight'] *= (1 - self.p)
        
                
        
        return True
    
    
    def run(self):
        
        '''
            Parameters:
            none
            
            This is the ACO Algorithm itself
            
        '''
        
        print ("ACO Problem initialized.")
        
        self.initial_graph_creation()
        
        while not(self.end_condition()):
            
            print("\t Generating ANT Solutions...")
            solutions = self.generate_ant_solutions_mono()

            print("\t Found "+ str(len(solutions)) + " solutions")
            print("Updating graphssssssss")
            
            self.update_graph_mono(solutions)

            
            for sol in solutions:    
                
                print("\t Solution of value: "+ str(self.objective_function(sol)))
                
                # We see if any of our solutions is better than the best so far
                if self.objective_function(sol) < self.objective_function(self.global_best_solution):
                    self.global_best_solution = sol
                    self.estimate = self.objective_function(sol) + math.ceil(self.objective_function(sol) / 2)
                    print("\t Global solution improved!")
                    
              
            