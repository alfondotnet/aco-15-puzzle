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
    
    def __init__(self, initial_states, solution_states, alpha, beta, number_of_ants, p, q0, base_attractiveness) :      
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
        self.graph = None # This is our global graph
        self.number_of_ants = number_of_ants
        self.colony = Colony(self.number_of_ants)  # We create a Colony with n Ants
        
        self.initial_tau = 1
        
        self.global_best_solution = None

    def generateNodeHash(self, state):
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
        
        pos=nx.spring_layout(self.graph)
        nx.draw(self.graph,pos,node_color='#A0CBE2',edge_color='#BB0000',width=2,with_labels=True)
        plt.show()
        

    def initial_graph_creation(self):
        
        '''
        # Initial graph creation
        Parameters: 
        none
        '''
        
        self.graph = nx.Graph()
        # Now we place final and initial nodes
            
        for s in self.initial_states:
            
            node_index = self.generateNodeHash(s)
            
            self.graph.add_node(node_index)
            self.graph.node[node_index]['node'] = ACONode(s, False, True) # Initial node
            self.graph.node[node_index]['initial'] = True
            self.graph.node[node_index]['solution'] = False
        
    def ant_placement(self):
        
        '''
        ant_placement
        places the ants equally in the "start nodes" of self.graph
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
                    initial_node_id = self.generateNodeHash(s)
                    
                    self.colony.ants[assigned_ant_id].set_start_node(initial_node_id, self.graph)
                    
        # We can make a shared random ant assignment for the rest of the cases
        
        while len(ants_id_list) > 0:
            
            assigned_ant_id = ants_id_list.pop()
            assigned_initial_state = choice(range(0,len(self.initial_states)))
            
            self.colony.ants[assigned_ant_id].set_start_node(self.generateNodeHash(self.initial_states[assigned_initial_state]), self.graph)


    def generate_ant_solutions(self):
        
        ''' generate_ant_solutions
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
        
        while True:
            # Now we tell all the ants to go find some food
            num_tasks = 0
            
            self.ant_placement()
  
            for ant in self.colony.ants:
                tasks.put(ant)
                num_tasks += 1
            
            # We wait now for all the ants to finish  
            tasks.join() 
            results_list = list()
            
            for _ in range(num_tasks):  
                results_list.append(results.get())
                
            if [r[1] for r in results_list] != [False for _ in range(len(results_list))]:
                
                # Add a poison pill for each consumer
                for _ in range(num_consumers):
                    tasks.put(None) 
                break
    
        return [r for (r,b) in results_list if b != False] 
        
    def pheromone_update(self, list_graph):
        ''' pheromone_update
            Parameters: 
            list_graph: A list of Graphs (networkx graphs)
            
            Performs both pheromone evaporation equally in the global graph and
            positive feedback on the paths of the solutions (Path on graphs) passed by argument
        '''
        # Positive feedback   
        for g in list_graph:
            for e in g.edges():
                if e in self.graph.edges():
                    # if the edge is traversed then we give some positive feedback
                    print(e)
                    print(self.graph[e[0]][e[1]])
                    
                    if 'weight' in self.graph[e[0]][e[1]].keys():
                        self.graph[e[0]][e[1]]['weight'] += self.pheromone_update_criteria(g.nodes())
                    else:
                        self.graph[e[0]][e[1]]['weight'] = self.pheromone_update_criteria(g.nodes())
        # Evaporation
        for e in self.graph.edges(data=True):
            if 'weight' in e[2].keys():
                e[2]['weight'] *= (1 - self.p)
            else:
                e[2]['weight'] = self.initial_tau * (1 - self.p)

    def update_graph(self, list_solutions):
        
        ''' update__graph
            Parameters:
            list_solutions: A list of paths returned by different ants
            A path is a list of NODES (not node indexes)
            Given a list of solutions (list of paths), updates the global graph.
            
            Return:
            Returns a list of graphs of the solutions
        '''
        list_graphs_return = list()
        
        for solution in list_solutions:
            # [[(1080243414620259090, {'node': <aconode.ACONode instance at 0x2c713b0>, 'initial': True, 'solution': False}), (16212338162585125650L, {'node': <aconode.ACONode instance at 0x2c71368>}), (17225648078743487250L, {'node': <aconode.ACONode instance at 0x2c71878>}), (17270683387822424850L, {'node': <aconode.ACONode instance at 0x2c718c0>}), (17270672049108763410L, {'node': <aconode.ACONode instance at 0x2c71908>}), (16189824631214261010L, {'node': <aconode.ACONode instance at 0x2c71950>}), (1057729883249394450, {'node': <aconode.ACONode instance at 0x2c71998>}), (14892576832299025170L, {'node': <aconode.ACONode instance at 0x2c719e0>}), (14892717567639896850L, {'node': <aconode.ACONode instance at 0x2c71a28>}), (14892717569401504530L, {'node': <aconode.ACONode instance at 0x2c71a70>}), (14892717569451835410L, {'node': <aconode.ACONode instance at 0x2c71ab8>}), (14892717569451820050L, {'node': <aconode.ACONode instance at 0x2c71b00>}), (14892717567572800530L, {'node': <aconode.ACONode instance at 0x2c71b48>}), (14892717568327775250L, {'node': <aconode.ACONode instance at 0x2c71b90>}), (14892717568422147090L, {'node': <aconode.ACONode instance at 0x2c71bd8>}), (14892716812519437330L, {'node': <aconode.ACONode instance at 0x2c71c20>}), (14847681503440499730L, {'node': <aconode.ACONode instance at 0x2c71c68>}), (13901925581692695570L, {'node': <aconode.ACONode instance at 0x2c71cb0>}), (14982772999587197970L, {'node': <aconode.ACONode instance at 0x2c71cf8>}), (14982779596556301330L, {'node': <aconode.ACONode instance at 0x2c71d40>}), (14982779595801326610L, {'node': <aconode.ACONode instance at 0x2c71d88>}), (14982779597680346130L, {'node': <aconode.ACONode instance at 0x2c71dd0>}), (14982779597680361490L, {'node': <aconode.ACONode instance at 0x2c71e18>}), (14982779597630030610L, {'node': <aconode.ACONode instance at 0x2c71e60>}), (14982779597803045650L, {'node': <aconode.ACONode instance at 0x2c71ea8>}), (14982779597804094210L, {'node': <aconode.ACONode instance at 0x2c71ef0>}), (14982779597804094240L, {'node': <aconode.ACONode instance at 0x2c71f38>}), (14982779597803766565L, {'node': <aconode.ACONode instance at 0x2c71f80>}), (14982779559149650725L, {'node': <aconode.ACONode instance at 0x2c71fc8>}), (14982778914904556325L, {'node': <aconode.ACONode instance at 0x2c72050>}), (14982772730151650085L, {'node': <aconode.ACONode instance at 0x2c72098>}), (14982784824595006245L, {'node': <aconode.ACONode instance at 0x2c720e0>}), (14982784824645337125L, {'node': <aconode.ACONode instance at 0x2c72128>}), (14982784824645321765L, {'node': <aconode.ACONode instance at 0x2c72170>}), (14982784822766302245L, {'node': <aconode.ACONode instance at 0x2c721b8>}), (14982784823521276965L, {'node': <aconode.ACONode instance at 0x2c72200>}), (14982784823588384805L, {'node': <aconode.ACONode instance at 0x2c72248>}), (14982784823588357925L, {'node': <aconode.ACONode instance at 0x2c72290>}), (14982784822783063845L, {'node': <aconode.ACONode instance at 0x2c722d8>}), (14982784823789696805L, {'node': <aconode.ACONode instance at 0x2c72320>}), (14982784823907135525L, {'node': <aconode.ACONode instance at 0x2c72368>}), (14982784823907136005L, {'node': <aconode.ACONode instance at 0x2c723b0>}), (14982784823906087445L, {'node': <aconode.ACONode instance at 0x2c723f8>}), (14982784411595518485L, {'node': <aconode.ACONode instance at 0x2c72440>}), (14982785055840612885L, {'node': <aconode.ACONode instance at 0x2c72488>}), (14982785094494728725L, {'node': <aconode.ACONode instance at 0x2c724d0>}), (14982785094488830485L, {'node': <aconode.ACONode instance at 0x2c72518>}), (14982784407304548885L, {'node': <aconode.ACONode instance at 0x2c72560>}), (14919734974594036245L, {'node': <aconode.ACONode instance at 0x2c725a8>}), (14974622595052614165L, {'node': <aconode.ACONode instance at 0x2c725f0>}), (14977155831188304405L, {'node': <aconode.ACONode instance at 0x2c72638>}), (14977154929245172245L, {'node': <aconode.ACONode instance at 0x2c72680>}), (14977155616429453845L, {'node': <aconode.ACONode instance at 0x2c726c8>}), (14977155616435352085L, {'node': <aconode.ACONode instance at 0x2c72710>}), (14977155616435679760L, {'node': <aconode.ACONode instance at 0x2c72758>}), (14977155616435679745L, {'node': <aconode.ACONode instance at 0x2c727a0>}), (14977155616435679265L, {'node': <aconode.ACONode instance at 0x2c727e8>}), (14977155616435667745L, {'node': <aconode.ACONode instance at 0x2c72830>}), (14977155615361942305L, {'node': <aconode.ACONode instance at 0x2c72878>}), (14977155617123549985L, {'node': <aconode.ACONode instance at 0x2c728c0>}), (14977155617173880865L, {'node': <aconode.ACONode instance at 0x2c72908>}), (14977155617173865505L, {'node': <aconode.ACONode instance at 0x2c72950>}), (14977155615294845985L, {'node': <aconode.ACONode instance at 0x2c72998>}), (14977155616049820705L, {'node': <aconode.ACONode instance at 0x2c729e0>}), (14977155616144192545L, {'node': <aconode.ACONode instance at 0x2c72a28>}), (14977155616146289665L, {'node': <aconode.ACONode instance at 0x2c72a70>}), (14977155616146288705L, {'node': <aconode.ACONode instance at 0x2c72ab8>}), (14977155616146261825L, {'node': <aconode.ACONode instance at 0x2c72b00>}), (14977155615340967745L, {'node': <aconode.ACONode instance at 0x2c72b48>}), (14977155616850917185L, {'node': <aconode.ACONode instance at 0x2c72b90>}), (14977155616968355905L, {'node': <aconode.ACONode instance at 0x2c72bd8>}), (14977155616968344385L, {'node': <aconode.ACONode instance at 0x2c72c20>}), (14977155615357756225L, {'node': <aconode.ACONode instance at 0x2c72c68>}), (14977155617119363905L, {'node': <aconode.ACONode instance at 0x2c72cb0>}), (14977155617169694785L, {'node': <aconode.ACONode instance at 0x2c72cf8>}), (14977155617169671745L, {'node': <aconode.ACONode instance at 0x2c72d40>}), (14977155615290652225L, {'node': <aconode.ACONode instance at 0x2c72dd0>}), (14977155616045626945L, {'node': <aconode.ACONode instance at 0x2c72ea8>}), (14977155616146288705L, {'node': <aconode.ACONode instance at 0x2c72ab8>}), (14977155616146289665L, {'node': <aconode.ACONode instance at 0x2c72a70>}), (14977155616144192545L, {'node': <aconode.ACONode instance at 0x2c72a28>}), (14977155616049820705L, {'node': <aconode.ACONode instance at 0x2c729e0>}), (14977155615294845985L, {'node': <aconode.ACONode instance at 0x2c72998>}), (14977155617173865505L, {'node': <aconode.ACONode instance at 0x2c72950>}), (14977155617173880865L, {'node': <aconode.ACONode instance at 0x2c72908>}), (14977155617123549985L, {'node': <aconode.ACONode instance at 0x2c728c0>}), (14977155615361942305L, {'node': <aconode.ACONode instance at 0x2c72878>}), (14977155616435667745L, {'node': <aconode.ACONode instance at 0x2c72830>}), (14977155616435679265L, {'node': <aconode.ACONode instance at 0x2c727e8>}), (14977155616435679745L, {'node': <aconode.ACONode instance at 0x2c727a0>}), (14977155616429388385L, {'node': <aconode.ACONode instance at 0x2c74368>}), (14977154929245106785L, {'node': <aconode.ACONode instance at 0x2c74488>}), (14977155831188238945L, {'node': <aconode.ACONode instance at 0x2c745a8>}), (14974622595052548705L, {'node': <aconode.ACONode instance at 0x2c746c8>}), (14919734974593970785L, {'node': <aconode.ACONode instance at 0x2c747e8>}), (14982784407304483425L, {'node': <aconode.ACONode instance at 0x2c74908>}), (14982785094488765025L, {'node': <aconode.ACONode instance at 0x2c74a28>}), (14982785094495056385L, {'node': <aconode.ACONode instance at 0x2c74b48>}), (14982785094495055905L, {'node': <aconode.ACONode instance at 0x2c74c68>}), (14982785094495044385L, {'node': <aconode.ACONode instance at 0x2c74d88>}), (14982785093421318945L, {'node': <aconode.ACONode instance at 0x2c74ea8>}), (14982644358080447265L, {'node': <aconode.ACONode instance at 0x2c74fc8>}), (1147797409030816545, {'node': <aconode.ACONode instance at 0x2c77128>}), (1147797409030816545, {'node': <aconode.ACONode instance at 0x2c77128>})]]

            g = nx.Graph()
            g.add_nodes_from(solution)
            g.add_path([s[0] for s in solution])

            self.graph = nx.compose(self.graph, g) # self.graph edges have preference over g
            list_graphs_return.append(g)
        
        return list_graphs_return
        
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
            solutions = self.generate_ant_solutions()
            print("\t Found "+ str(len(solutions)) + " solutions")
            
            print("Updating graph")
            sub_graphs = self.update_graph(solutions)
            print("Updating pheromone...")  
            self.pheromone_update(sub_graphs)
            for sol in solutions:    
                
                print("\t Solution of value: "+ str(self.objective_function(sol)))
                
                # We see if any of our solutions is better than the best so far
                if self.objective_function(sol) < self.objective_function(self.global_best_solution):
                    self.global_best_solution = sol
                    print("\t Global solution improved!")
                    
              
            