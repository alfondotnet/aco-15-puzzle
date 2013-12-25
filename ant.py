import networkx as nx
from aconode import ACONode
import random
import math
import sys
import matplotlib.pyplot as plt

'''
ant.py

@Author: Alfonso Perez-Embid (Twitter: @fonsurfing)

'''


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
        
        self.list_of_visited_nodes_id = list() # This is a list of visited nodes that each ant keeps (Tabu list)

        # This may be cleared after a period of time (iterations)
        # TODO
        #self.length_of_ant_memory = ...
        
        
        self.decision_tables = dict() # Decision tables for different nodes
        
        self.working_memory = list() # This is a list of edges

        self.aco_specific_problem = None # It's going to be passed by the specific aco problem in the __init__ so the ant knows
        # How to expand the graph, the parameters of the problem and so on
 
        self.graph = None # The initial subgraph is passed from ACOProblem to the set_start_node method
    
    def set_start_node(self, start_node_id, graph):

        self.start_node_id = start_node_id
        self.current_node_id = start_node_id

        self.graph = graph

        
    def __str__(self):
        
        ant_to_string = "[ Ant no:"+ str(self.id) + ", Start node: "+ str(self.start_node_id)
        ant_to_string += ", Current node: " + str(self.current_node_id) +" ]"
        ant_to_string += " Solution nodes list: "+ str(self.solution_nodes_id)

        return ant_to_string

    def __call__(self):
        
        # We have to re-seed our RNG in order to give different results on 
        # differents tasks
        random.seed()
        
        
        if self.aco_specific_problem == None:
            
            raise Exception ("You have to pass an instance of your specific ACO problem to every ant of the colony first!")
    
        ''' __call__ (lookForFood)
            Method to be called by Consumer in a multiprocessing Queue
            Parameters:
            none
            
            Return: True?  TODO.
            
            The ant looks for a solution of the ACOProblem and when it does find one, 
            return to it's house, giving a positive feedback (depositing pheromone)
            on the path
        '''
        
        while self.current_node_id not in self.solution_nodes_id:
            
            self.expand_node(self.current_node_id)
            
            
        return True
    
    def expand_node(self, node_index_to_expand):
        
        ''' expand_node
            Parameters:
            node_index_to_expand: Index of node to expand
            
            Expands a node. (creates successor nodes
            and add edges from/to their parents and them).
        '''
             
        node_to_expand = self.graph.node[node_index_to_expand]['node']
        
        successors = self.aco_specific_problem.successors(node_to_expand.state)

        for s in successors:
            
            successor_index = self.aco_specific_problem.generateNodeHash(s)
            
            self.graph.add_node(successor_index)
            self.graph.node[successor_index]['node'] = ACONode(s)
            self.graph.add_edge(node_index_to_expand,successor_index, weight=self.aco_specific_problem.initial_tau)    
            

    def move_ant(self, node_index):
        ''' move_ant
        
            Parameters:
            node_index
            
            Moves the ant.
            This is called only by move_to_another_node, because that method has to check
            first for efficiency that the node where the ant is going has not been visited already
        '''
        
        self.current_node_id = node_index
        self.list_of_visited_nodes_id.append(node_index)
    
    def decision_table(self, node_index):
        
        ''' decision table
            (a sub ij)
            
            Parameters:
            node_index
        
            Returns:
            Dictionary (Key: Node, Value: Value of aij associated with that node)
            
            Given the index of a node, calculates and/or returns the decision table for the node.

        '''
        
        # We first check if the node has already a decision table and return it instead
        # Otherwise we calculate it, update it and return it
        
        if node_index in self.decision_tables:
            return self.decision_tables[node_index]
        
        decision_table = dict() # This is going to be the dictonary of the decision table
        edges_to_consider = self.graph.edges(self.current_node_id, data=True)
        
        edges_not_in_working_memory = [e for e in edges_to_consider if e not in self.working_memory]
        
        # This is the denominator of the aij formulae
        
        summatory_denominator = 0
        
        for e in edges_not_in_working_memory:
        
            next_state = self.graph.node[e[1]]['node'].state
            
            ph = e[-1]['weight']
            
            if self.aco_specific_problem.calculate_cost(next_state) != 0:
                nil = 1.0 / self.aco_specific_problem.calculate_cost(next_state)
            else:
                nil = sys.float_info.max
            
            summatory_denominator += math.pow(ph,self.aco_specific_problem.alpha) * math.pow(nil,self.aco_specific_problem.beta)
        
        # And now that we have calculated the denominator, we calculate each
        # a sub ij
            
        for edge in edges_to_consider:
            
            next_state = self.graph.node[edge[1]]['node'].state
            pheromone = edge[-1]['weight'] # tau i,j

            # inverse of the cost of this potential new state
            # We check if the cost is 0 (hopefully) solution to avoid division by zero
            if self.aco_specific_problem.calculate_cost(next_state) != 0:
                nij = 1.0 / self.aco_specific_problem.calculate_cost(next_state)
            else:
                nij = sys.maxint
                
            # This is the formulae for aij
            aij = math.pow(pheromone,self.aco_specific_problem.alpha) * math.pow(nij,self.aco_specific_problem.beta)
            # Now we normalize for the edges that the and hasnt visited in its
            # working memory (can be configurated)
            aij /= summatory_denominator 
            

            decision_table[edge[1]] = aij

        self.decision_tables[node_index] = decision_table
        
        return decision_table
        
    def move_to_another_node(self):
        
        ''' move_to_another_node
            (Rule of transition)
            Parameters: 
            none
        
            Here the ant will decide where to move, based on the following rule of transition:
            
            (Given q, a random number in [0,1]
            and q0, a parameter of the problem:)
            
            if q <= q0 : The ant moves to the edge with more pheromone
            if q > q0  : The ant moves a randomly-chosen edge in proportion with its
            efficacy (eg. Heuristic)
        
        '''
        
        q = random.random()


        if q <= self.aco_specific_problem.q0:
            
            edges_to_consider = self.graph.edges(self.current_node_id, data=True)
            # Now we sort the list of edges to consider
            # The edge we will take then would the last in the sorted list
            edges_to_consider_sorted = sorted(edges_to_consider, key=lambda (source,target,data): data['weight'])
            # example: [(17134975606245761055L, 17136101506152603675L, {'weight': 0.4939538810147658}), (17134975606245761055L, 18287897110852608030L, {'weight': 0.759895474826771})]
            node_to_go = edges_to_consider_sorted[-1][1]
            # We move instantly
            self.move_ant(node_to_go)
        
        else:
            
            a = 1
            
    def draw_graph(self):
        
        pos=nx.spring_layout(self.graph)
        nx.draw(self.graph,pos,node_color='#A0CBE2',edge_color='#BB0000',width=2,with_labels=True)
        plt.show()