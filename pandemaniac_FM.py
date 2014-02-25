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
def get_top_seeds(centrality):
    # Select the top num_seeds * num_players node 
    topList = []
    pivot = centrality[0][1]
    done = False
    wanted = num_seeds * num_players
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
                
    # Randomly choose a number of seeds from the topList and output to file
    seeds = []
    s = random.choice(topList)[0]
    for i in range(num_seeds):
        while str(s) in seeds:
            s = random.choice(topList)[0]
        seeds.append(str(s))  
    
    return seeds

if __name__ == "__main__":
    filename = sys.argv[1]
    graph = json.loads(open(filename).read())
    num_nodes = len(graph)
    num_players = int(filename.split('.')[0])
    num_seeds = int(filename.split('.')[1])
    
    # deg centrality
    deg_centrality = []
    v = len(graph)
    for i in range(v):
        deg_centrality.append([i, len(graph[str(i)])])

    c_sorted = sorted(deg_centrality, key=itemgetter(1), reverse=True)
    seeds_deg = [str(c_sorted[i][0]) for i in range(num_seeds)]

    # average distance centrality    
    dist = []
    # Initialize
    for i in range(num_nodes):
        dist.append([1000] * num_nodes)
    for i in range(num_nodes):
        for j in range(i, num_nodes):
            if i == j:
                dist[i][j] = 0
            elif str(i) in graph[str(j)]:
                dist[i][j] = 1
                dist[j][i] = 1
    # Use floyd-warshall algorithm to calculate the diameters
    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    sum_d = 0
    dist_centrality = []
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and dist[i][j] == 1000:
                continue
            sum_d += dist[i][j]
        dist_centrality.append([i, float(sum_d) / (num_nodes - 1)])
        sum_d = 0
       
    # Print the idea number of nodes this strategy can capture    
    for i in range(10):
        deg_seed = get_top_seeds(deg_centrality)
        dist_seed = get_top_seeds(dist_centrality)        
        print sim.run(graph, {"Degree":deg_seed, "Distance":dist_seed})

