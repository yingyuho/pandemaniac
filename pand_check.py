#!/usr/bin/env python

###############################################################################
# Naive Implementation:                                                       #
# Randomly choose num_seeds of nodes out of top num_seeds * num_player nodes  #
# with the largest degree.                                                    #
###############################################################################
import sys
import json
import random
import sim
from operator import itemgetter
from math import sqrt

N = 100 # Maxmimum number of iterations we are doing to find the top nodes

if __name__ == "__main__":
    filename = sys.argv[1]
    graph = json.loads(open(filename).read())
    num_players = int(filename.split('.')[0])
    num_seeds = int(filename.split('.')[1])

    # Calculate centrality
    centrality = []
    v = len(graph)
    print "Number of nodes: " + str(v)
    for i in range(v):
        centrality.append([i, len(graph[str(i)])])

    c_sorted = sorted(centrality, key=itemgetter(1), reverse=True)
    seeds_deg = [str(c_sorted[i][0]) for i in range(num_seeds)]
    low_degs = 0
    low_nodes = []
    centrality_2 = []
    for i in range(v):
        l = 0 #len(graph[str(i)])
        # print('g')
        # print(graph[str(i)])
        # print('s')
        # print(seeds_deg)
        for n in set(graph[str(i)]) & set(seeds_deg):
            l += len(graph[n])
        
        if l > 0:
            # print([i,l])
            centrality_2.append([i, l])
        if l < 3:
            low_degs += 1
            low_nodes.append(i)

    print "Number of low-degree nodes: " + str(low_degs)
    print "Low degree percentage: " + str(float(low_degs) / v * 100) + "%"

    c_sorted_2 = sorted(centrality_2, key=itemgetter(1), reverse=True)
    # print(centrality_2)
    # print(c_sorted_2[:num_seeds])

    seeds_deg_2 = [str(c_sorted_2[i][0]) for i in range(num_seeds)]

    # seeds_highest_deg = []

    # i = 0
    # for s in seeds_deg:
    #     seeds_highest_deg.append(s)
    #     i += 1
    #     if i >= num_seeds:
    #         break
    #     nb = graph[str(s)]
    #     # nb_of_nb = dict()
    #     # for n in nb:
    #         # nb_of_nb[n] = [x for x in graph[n] if x in nb]
    #     nb.sort(key=lambda x:centrality_2[int(x)][1], reverse=True)
    #     for n in nb:
    #         if n not in seeds_highest_deg:
    #             seeds_highest_deg.append(str(n))
    #             i += 1
    #             if i >= num_seeds:
    #                 break
    #     if i >= num_seeds:
    #         break

    # Select the top num_seeds * num_players node 
    topList = []
    pivot = centrality[0][1]
    done = False
    wanted = num_seeds * num_players / 5
    for i in range(N):
        curtop = []
        curbot = []
        for c in centrality:
            if c[1] > pivot:
                curtop.append(c)
            else:
                curbot.append(c)
        if len(curtop) > wanted:
            centrality = curtop[:]
        elif len(curtop) < wanted:
            wanted -= len(curtop)
            topList += curtop
            centrality = curbot[:]
        else:
            topList += curtop[:]
            break
        pivot = random.choice(centrality)[1]    

    topnodes = []
    for c in topList:
        topnodes.append(c[0])
            
    attacher = 0   
    attachers = []
    for lnode in low_nodes:
        for neighb in graph[str(lnode)]:
            if int(neighb) in topnodes:
                attacher += 1
                low_nodes.remove(lnode)
                attachers.append(lnode)
                break

    indatt = 0
    for lnode in low_nodes:
        for neighb in graph[str(lnode)]:
            if (int(neighb)) in attachers:
                indatt += 1
                break
    attacher += indatt
    print "Number of low-degree attachers: " + str(attacher)
    print "Attacher percentage: " + str(float(attacher) / v * 100) + "%"