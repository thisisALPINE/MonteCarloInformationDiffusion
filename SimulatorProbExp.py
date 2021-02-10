# -*- coding: utf-8 -*-
# author: Yu Fu, Louise A. Dennis
# Update version used for large network(>99/use Networkx)

from DTMCSN import Infection_Model, generate_graph
import sys
import random


arguments = sys.argv

nodes = int(arguments[1])
filename = arguments[2]

raw_filename = "raw_" + filename
multiples = 5

file_path = 'results/' + filename
raw_file_path = 'results/' + raw_filename
runs = 1000
probability = 0.5
prob_list = [0.1, 0.2, 0.3, 0.4, 0.5]

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
fr.write("# Graph \t Probability \t Different initial \t Similar Initial\n")

i = 1;
for seed in seed_list:
    print("\nGenerating Graph " + str(i), end = " ")
    G = generate_graph(nodes, edges, seed)
    random.seed(seed)
    m = 3
    print("\nWorking on Graph " + str(i), end = " ")
    n = 0
    for prob2 in prob_list:
        fr.write(str(i))
        fr.write("\t")
    
        fr.write(str(prob2))
        fr.write("\t")
        experiment = 0
        vd  = Infection_Model(nodes, G, probability, prob2, (m + 1)*nodes, runs, experiment)
        pn_diff[n].append(vd)
        fr.write(str(vd))
        fr.write("\t")
        experiment = 1
        vs  = Infection_Model(nodes, G, probability, prob2, (m + 1)*nodes, runs, experiment)
        pn_sim[n].append(vs)
        fr.write(str(vs))
        fr.write("\n")
        n = n + 1
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
f.write("# Prob \t Different initial \t Similar Initial \t y_high_diff \t y_low_diff \t y_high_sim \t y_low_sim \n")
while n < multiples:
    f.write(str(prob_list[n]))
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
