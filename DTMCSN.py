# -*- coding: utf-8 -*-
# author: Yu Fu, Louise A. Dennis
# Update version used for large network(>99/use Networkx)

import tkinter as tk
from tkinter import ttk
import operator
from random import choice
import random
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


def generate_graph(nodes, edges, seed):
    G = nx.random_graphs.barabasi_albert_graph(nodes, edges, seed)
    # pos = nx.spring_layout(G)  # layout style of the graph
    # nx.draw(G, pos, with_labels=False, node_size=30, node_color='blue')
    # Show the graph of the network(structure)
    # plt.show()
    return G

def Threshold_Model(nodes, graph, probability_indifferent, prob_idea, messages, runs, sim_diff):

    threshold = 2

    # Setup and initialize infected connections count array
    infected_connections_count = []
    for node in range(nodes):
        infected_connections_count.append(0)

    # Generate seeds, make sure there are no duplicates
    seeds = 3
    infected_nodes = []
    while len(infected_nodes) < seeds:
        seed = random.randint(0, nodes - 1)
        if seed not in infected_nodes:
            infected_nodes.append(seed)

    # Iterate through initial seeds and establish a first infection round
    for seed in infected_nodes:
        for neighbour in graph.neighbors(seed):
            infected_connections_count[neighbour] += 1

    print("Starting with " + str(seeds) + " seeds, ( " + str(infected_nodes) + " )threshold is " + str(threshold))
    # Iteratively infect nodes that cross a set threshold
    for i in range(10):
        new_infected_nodes = []
        for elem in enumerate(infected_connections_count):
            # elem is a tuple (index, number_of_infected_connections)
            if elem[1] >= threshold and elem[0] not in infected_nodes:
                # Probabilistic extension
                total_neighbours = len([item for item in graph.neighbors(elem[0])])
                infected_neighbours = elem[1]
                infection_probability = infected_neighbours / total_neighbours
                outcome = infect_or_not_infect(infection_probability)

                if outcome:
                    new_infected_nodes.append(elem[0])
                    infected_nodes.append(elem[0])

        print("ROUND " + str(i) + ": !!! NEW INFECTED NODES: " + str(new_infected_nodes))
        for node in new_infected_nodes:
            for neighbour in graph.neighbors(node):
                infected_connections_count[neighbour] += 1

    print("connections_count array: " + str(infected_connections_count))
    print("infected nodes: " + str(infected_nodes))

    return 0


def infect_or_not_infect(probability):
    outcomes = [0, 1]
    outcome = random.choices(outcomes, weights=(1 - probability, probability), k=1)
    if outcome == [1]:
        return True
    return False

def Infection_Model(nodes, graph, probability_indifferent, prob_idea, messages, runs, sim_diff):

     # G = generate_graph(nodes, edges, graph_seed)

    edges = list(graph.edges())
    # print("Edges: ", edges)

    connections = {}

    for node in range(nodes):
        connections[node] = len(list(graph.neighbors(node)))

    sortedConnections = sorted(connections.items(), key=operator.itemgetter(1))

    if (sim_diff == 0):
        # print("A")
        # seed connections: many is top 0.25, few is the last 0.25
        ManyNumber = FewNumber = int(float(nodes) * 0.25)

        FewList = sortedConnections[:FewNumber]
        ManyList = sortedConnections[-ManyNumber:]
 
        # First we generate some stats for `gets there first'
        idea_init = choice(ManyList)[0]
        antiidea_init = choice(FewList)[0]
    else:
        # print("B")
        idea_index = random.randrange(nodes)
      
        less_greater = random.randint(0, 1)
      
        if (less_greater == 0):
            anti_idea_index = random.randint(idea_index - int(float(nodes) * 0.1), idea_index - 1)
            if (anti_idea_index < 0 or anti_idea_index > len(sortedConnections) - 1):
                anti_idea_index = random.randint(idea_index + 1, idea_index + int(float(nodes) * 0.1))
                
        else:
            anti_idea_index = random.randint(idea_index + 1, idea_index + int(float(nodes) * 0.1))
            if (anti_idea_index < 0 or anti_idea_index > len(sortedConnections) - 1):
                 anti_idea_index = random.randint(idea_index - int(float(nodes) * 0.1), idea_index - 1)

          
        idea_init = sortedConnections[idea_index][0]
        antiidea_init = sortedConnections[anti_idea_index][0]

    # print ("idea: " + str(len(list(graph.neighbors(idea_init)))) + " anti idea: " + str(len(list(graph.neighbors(antiidea_init)))))
    total = 0
    for i in range(runs):
        agree = model_results(nodes,probability_indifferent, prob_idea,idea_init,antiidea_init,messages,graph)
        total = agree + total
        
    AgreePercent = float( (total * 100) / (runs * nodes))
    # print ("Expected Agreement: ", AgreePercent)
    return AgreePercent
    
    
    
def model_results(nodes, prob1, prob2, idea, anti, messages, G):
    state = ["agree", "disagree", "indifferent"]
    dict = DTMC_Transition(nodes, prob1, prob2, idea, anti, messages, G)
    agree = 0
    disagree = 0
    for key, value in dict.items():
        if dict[key] == state[0]:
            agree += 1
        if dict[key] == state[1]:
            disagree +=1
            
    return agree
                        
    # print("Agree: ", agree)
    # print("Disagree: ", disagree)




def DTMC_Transition(nodes,prob1, prob2,idea,antiIdea,messages, G):
    edges = G.edges

    # probability of infection
    probability1=float(prob1)
    probability2=float(prob2)

    # state: agree, disagree, indifferent
    state = ["agree", "disagree", "indifferent"]


    ######################################################################################
    # construct a dictionary to store the state of each node (key: node name; value: state)
    dict={}
    # initially set all nodes' state indifferent
    for n in range(int(nodes)):
        dict[n]=state[2]

    InfectedNodes = [] # store all infected nodes and update in time
    # set two seeds' state: agree or disagree
    if idea!=None:
        dict[idea]=state[0]
        InfectedNodes.append(idea)
    if antiIdea!=None:
        dict[antiIdea]=state[1]
        InfectedNodes.append(antiIdea)
        
    m = 0 # messages
    # the number of loops equals to the simulation time? equal to message number?
    # print ("starting run")
    while(m < messages):
        # select one infected node at random(PRISM work model)
        Random_Infected_Node = choice(InfectedNodes)
 
        # Find the connection of the node and transform the idea based on the probability
        #print("Random_Infected_node: ",Random_Infected_Node)
        # connectednodes=find_connected_nodes(Random_Infected_Node,edges)
        #print("Connected nodes: ",connectednodes)
        # The state of the random selected infected node: agree or anti
        x_state = dict[Random_Infected_Node]

        # The state of each connected nodes: initialized is indifferent
        for n in G.neighbors(Random_Infected_Node):
            n_state = dict[n]

            # for the connected node n, update the opinions of it according to the relevant probabilities
            if (x_state != n_state):
                x = random.uniform(0,1)
                if (n_state == "indifferent" and x < probability1):
                    dict[n]=x_state
                    InfectedNodes.append(n)
                elif (x < probability2):
                    # print(probability2)
                    dict[n]=x_state

            # print(dict)
        m += 1
    return dict

def output_graph(FewList, AverageList, ManyList, numberOfNodes, probability_value, edges, number_Of_SimulationTimes):
    FewideaConnection = FewList  # few connection
    FewantiIdeaConnection = FewList  # few connection

    AverageideaConnection=AverageList # average connection
    AverageantiIdeaConnection=AverageList # average connection

    ManyideaConnection=ManyList # many connection
    #antiIdeaConnection=[('1', 2), ('3', 2)] # few connection

    print('FewideaConnection: ',FewideaConnection)
    print("FewantiIdeaConnection: ", FewantiIdeaConnection)
    print("AverageideaConnection: ", AverageideaConnection)
    print("AverageantiIdeaConnection", AverageantiIdeaConnection)
    print("ManyideaConnection", ManyideaConnection)


    messages = []
    ExpectedInfection_few = []
    ExpectedInfection_average = []
    ExpectedInfection_manyAndfew = []
    i = 0
    message = int(numberOfNodes) *4
    # when there are 10 nodes the number of messages is 40, so quadruple here
    while i <= message:
        messages.append(i)

        y1 = statistics(i, FewideaConnection, FewantiIdeaConnection, numberOfNodes, probability_value, edges, number_Of_SimulationTimes)
        ExpectedInfection_few.append(y1)

        y2 = statistics(i, AverageideaConnection, AverageantiIdeaConnection, numberOfNodes, probability_value, edges, number_Of_SimulationTimes)
        ExpectedInfection_average.append(y2)

        y3 = statistics(i, ManyideaConnection, FewantiIdeaConnection, numberOfNodes, probability_value, edges, number_Of_SimulationTimes)
        ExpectedInfection_manyAndfew.append(y3)

        i = i + int(message/10)    # this is the interval between data points on the curve (10 nodes -> 2 interval)

        print(messages)
        print(ExpectedInfection_few)
        print(ExpectedInfection_average)
        print(ExpectedInfection_manyAndfew)



    plt.plot(messages, ExpectedInfection_few, color='blue', label='initial agent have few connections', marker='o',
             markersize='3', linestyle='-')
    plt.plot(messages, ExpectedInfection_average, color='green', label='initial agent have average connections', marker='s',
             markersize='3', linestyle='-')
    plt.plot(messages, ExpectedInfection_manyAndfew, color='red', label='initial agent have many and few connections', marker='v',
             markersize='3', linestyle='-')



    x_ticks = np.arange(0, message + 2, int(message/10))
    y_ticks = np.arange(0.0, max(ExpectedInfection_manyAndfew) + 0.5, int(max(ExpectedInfection_manyAndfew) + 0.5)/10)
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)


    plt.legend()
    plt.grid()
    plt.xlabel('messages')
    plt.ylabel('Expected Infection')
    plt.show()
    
    
