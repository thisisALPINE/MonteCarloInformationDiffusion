# -*- coding: utf-8 -*-
# author: Yu Fu, Louise A. Dennis
# Update version used for large network(>99/use Networkx)

import tkinter as tk
from tkinter import ttk
import operator
from random import choice
# -*- coding: utf-8 -*-
# author: Yu Fu, Louise A. Dennis
# Update version used for large network(>99/use Networkx)

from DTMCSN import Infection_Model, generate_graph
import sys
import random
import time
    
arguments = sys.argv

nodes = int(arguments[1])
experiment = int(arguments[2])

runs = 100
prob1 = 0.5
prob2 = 0.5

seed_list = [608, 22399, 30799, 45619, 86914, 88199, 95479, 97124, 102228, 110381, 123191]
# seed_list = [608, 22399, 30799, 45619, 86914, 88199, 95479, 97124, 102228, 110381, 123191, 128066, 136198, 138622, 144029, 145665, 150140, 155098, 160442, 167664, 174155, 178254, 182472, 205539, 207874, 211275, 242730, 253936, 273295, 277832, 283560, 283621, 287753, 293983, 342667, 368661, 388498, 398682, 399457, 401114, 405783, 411091, 414681, 419865, 425440, 436392, 437673, 445677, 463650, 466866, 466979, 480885, 490791, 493598, 512922, 515091, 515872, 520311, 523216, 523537, 535565, 540857, 540884, 543581, 558932, 560267, 570716, 582510, 614492, 629770, 632541, 672255, 689666, 706116, 708028, 712723, 741788, 746230, 810533, 812966, 813561, 816066, 825575, 831753, 832583, 849195, 861630, 866382, 888709, 888810, 917493, 925522, 936628, 938122, 955047, 972166, 974518, 976014, 991753, 993612]
# seed_list = [1]

edges = 3

i = 1
graphanalysistime = 0
graphgentime = 0
for seed in seed_list:
    start = time.time()
    G = generate_graph(nodes, edges, seed)
    end = time.time()
    graphgentime = graphgentime + (end - start)
    random.seed(seed)
    m = 0
    print("\nWorking on Graph " + str(i), end = " ")
    start = time.time()
    vd  = Infection_Model(nodes, G, prob1, prob2, (m + 1)*nodes, runs, experiment)
    end = time.time()
    graphanalysistime = graphanalysistime + (end - start)
    i = i + 1
    
averagetime = graphgentime/(i - 1)
print("\nGraph Generation Average Time: ", end="")
print(averagetime)
averagetime = graphanalysistime/(i - 1)
print("\nGraph Analysis Average Time: ", end="")
print(averagetime)

    
