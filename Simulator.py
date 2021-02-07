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
import sys

def generate_graph(nodes, edges, seed):
    G = nx.random_graphs.barabasi_albert_graph(nodes, edges, seed)
    pos = nx.spring_layout(G)  # layout style of the graph
    nx.draw(G, pos, with_labels=False, node_size=30, node_color='blue')
    # Show the graph of the network(structure)
    # plt.show()
    return G
    

def Infection_Model(nodes, graph, probability_value, messages, runs, sim_diff):

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
        agree = model_results(nodes,probability_value,idea_init,antiidea_init,messages,graph)
        total = agree + total
        
    AgreePercent = float( (total * 100) / (runs * nodes))
    # print ("Expected Agreement: ", AgreePercent)
    return AgreePercent
    
    
    
def model_results(nodes, probability, idea, anti, messages, G):
    state = ["agree", "disagree", "indifferent"]
    dict = DTMC_Transition(nodes, probability, idea, anti, messages, G)
    agree = 0
    disagree = 0
    for key, value in dict.items():
        if dict[key] == state[0]:
            agree += 1

    for key, value in dict.items():
        if dict[key] == state[1]:
            disagree +=1
            
    return agree
                        
    # print("Agree: ", agree)
    # print("Disagree: ", disagree)




def DTMC_Transition(nodes,probability_value,idea,antiIdea,messages, G):
    edges = G.edges

    # probability of infection
    probability=float(probability_value)

    # state: agree, disagree, indifferent
    state = ["agree", "disagree", "indifferent"]


    ######################################################################################
    # construct a dictionary to store the state of each node (key: node name; value: state)
    dict={}
    # initially set all nodes' state indifferent
    for n in range(int(nodes)):
        dict[n]=state[2]

    # set two seeds' state: agree or disagree
    if idea!=None:
        dict[idea]=state[0]
    if antiIdea!=None:
        dict[antiIdea]=state[1]
        
    ######################################################################################
    # construct a dictionary to store connectedness information
    
    # connected = {}
    # for n in range(int(nodes)):
    #     connectednodes = []
    #     for i in edges:
     #        if i[0] == n:
     #            connectednodes.append(i[1])
     #        if i[1] == n:
    #             connectednodes.append(i[0])
    #     connected[n] = connectednodes


    InfectedNodes = [] # store all infected nodes and update in time
    # if the state is not 'indifferent', it is infected node
    for key, value in dict.items():
        if dict[key] != state[2]:
            InfectedNodes.append(key)

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
                if (x < probability):
                    dict[n]=x_state
                    if n_state == "indifferent":
                        InfectedNodes.append(n)

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
    
    
arguments = sys.argv

nodes = int(arguments[1])
filename = arguments[2]
raw_filename = "raw_" + filename
multiples = 6

file_path = 'results/' + filename
raw_file_path = 'results/' + raw_filename
runs = 1000
probability = 0.5

seed_list = [608, 22399, 30799, 45619, 86914, 88199, 95479, 97124, 102228, 110381, 123191, 128066, 136198, 138622, 144029, 145665, 150140, 155098, 160442, 167664, 174155, 178254, 182472, 205539, 207874, 211275, 242730, 253936, 273295, 277832, 283560, 283621, 287753, 293983, 342667, 368661, 388498, 398682, 399457, 401114, 405783, 411091, 414681, 419865, 425440, 436392, 437673, 445677, 463650, 466866, 466979, 480885, 490791, 493598, 512922, 515091, 515872, 520311, 523216, 523537, 535565, 540857, 540884, 543581, 558932, 560267, 570716, 582510, 614492, 629770, 632541, 672255, 689666, 706116, 708028, 712723, 741788, 746230, 810533, 812966, 813561, 816066, 825575, 831753, 832583, 849195, 861630, 866382, 888709, 888810, 917493, 925522, 936628, 938122, 955047, 972166, 974518, 976014, 991753, 993612]
# seed_list = [1]

pn_diff = []
pn_sim = []
for i in range(multiples):
    pn_diff.append([])
    pn_sim.append([])

edges = 3

fr = open(raw_file_path, 'w')
fr.write("# Number of nodes: ")
fr.write(str(nodes))
fr.write("\n")
fr.write("# Number of edges in Barabasi graph: ")
fr.write(str(edges))
fr.write("\n")
fr.write("# Graph \t Messages \t Different initial \t Similar Initial\n")

i = 1;
for seed in seed_list:
    G = generate_graph(nodes, edges, seed)
    random.seed(seed)
    m = 0
    print("\nWorking on Graph " + str(i), end = " ")
    while m < multiples:
        fr.write(str(i))
        fr.write("\t")
    
        fr.write(str(m + 1))
        fr.write("\t")
        experiment = 0
        vd  = Infection_Model(nodes, G, probability, (m + 1)*nodes, runs, experiment)
        pn_diff[m].append(vd)
        fr.write(str(vd))
        fr.write("\t")
        experiment = 1
        vs  = Infection_Model(nodes, G, probability, (m + 1)*nodes, runs, experiment)
        pn_sim[m].append(vs)
        fr.write(str(vs))
        fr.write("\n")
        m = m + 1
    i = i + 1

fr.close()

f = open(file_path, 'w')
n = 0
f.write("# Number of nodes: ")
f.write(str(nodes))
f.write("\n")
f.write("# Number of edges in Barabasi graph: ")
f.write(str(edges))
f.write("\n")
f.write("# Messages \t Different initial \t Similar Initial \t y_high_diff \t y_low_diff \t y_high_sim \t y_low_sim \n")
while n < multiples:
    f.write(str(n  +  1))
    f.write("\t")
    pnn_diff = sum(pn_diff[n]) / len(seed_list)
    f.write(str(pnn_diff))
    f.write("\t")
    pnn_sim = sum(pn_sim[n]) / len(seed_list)
    f.write(str(pnn_sim))
    f.write("\t")
    diff_sorted = sorted(pn_diff[n])
    sim_sorted = sorted(pn_sim[n])
    low_index = int(len(seed_list)/10)
    high_index = 9*low_index
    f.write(str(diff_sorted[low_index]))
    f.write("\t")
    f.write(str(diff_sorted[high_index]))
    f.write("\t")
    f.write(str(sim_sorted[low_index]))
    f.write("\t")
    f.write(str(sim_sorted[high_index]))
    f.write("\n")
    n = n + 1
    
f.close()
