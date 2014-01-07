# coding=utf-8
import networkx as nx
#import matplotlib.pyplot as plt
import sys
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
    
    def __init__(self, initial_states, solution_states, alpha, beta, number_of_ants, p, q0, base_attractiveness, initial_tau) :      
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

    
#     def draw_graph(self):
#         
#         pos=nx.spring_layout(self.global_graph)
#         nx.draw(self.global_graph,pos,node_color='#A0CBE2',edge_color='#BB0000',width=2,with_labels=True)
#         plt.show()
        

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
        ''' generate_ant_solutions_mono
            Parameters:
            none
            
            Return:
            A list of solutions
            
            An ant MUST know the iteration she is in so it can compute the pheromone on the fly, based on all the
        '''      
        while True:
            
            self.ant_placement()
            # When at least someone has found something, we kill the rest
            while True:
                
                # STATS if exists run exists aswell

                if (len(self.global_graph)) > 2000000:
                    return False

                
                list_results_ants = list()
                # Performs one iteration in each ant
                for ant in self.colony.ants:
                    sol = ant.__iteration__()
                    list_results_ants.append(sol)
                
                if [r[1] for r in list_results_ants] != [False for _ in range(len(self.colony.ants))]:
                    break

            # We see which one is the best to give some positive feedback                 
            best_sol = sys.maxint
            best_ant = None
        
            for sol in list_results_ants:
                if sol[1] == False:
                    continue
                if len(sol[0]) < best_sol:
                    best_sol,best_ant = sol
                    
            # Global update
            
            self.colony.ants[best_ant].positive_feedback() 

            return [r for (r,b) in list_results_ants if b != False]


    
    def run(self, same_results_condition):
        
        '''
            Parameters:
            same_results_condition: Times we need to have the same result to exist.
            Means that it has considerably converged.
            
            This is the ACO Algorithm itself
            
        '''
        
        print ("ACO Problem initialized.")
        
        self.initial_graph_creation()
        
        last_value = sys.maxint
        same_value_times = 0
        first_iteration = True
        
        while not(self.end_condition()):
            
            #print("\t Generating ANT Solutions...")
            solutions = self.generate_ant_solutions_mono()

            #print("\t Found "+ str(len(solutions)) + " solutions")
            
            if solutions == False:
                return False
            
            
            for sol in solutions:
                
                if first_iteration:
                    last_value = sol
                    first_iteration = False
                
                if last_value == sol:
                    same_value_times += 1    
                else:
                    same_value_times = 0
                
                if same_value_times > same_results_condition:
                    return sol
                    
                last_value = sol
                
                print ("Solucion de "+ str(len(sol)))
                
                if self.objective_function(sol) < self.objective_function(self.global_best_solution):
                    self.global_best_solution = sol
                    #self.estimate = self.objective_function(sol)
                    print("\t Global solution improved! ", len(sol))
        return sol

            