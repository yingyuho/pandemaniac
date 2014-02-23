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
    for i in range(v):
        centrality.append([i, len(graph[str(i)])])

    c_sorted = sorted(centrality, key=itemgetter(1), reverse=True)
    seeds_deg = [str(c_sorted[i][0]) for i in range(num_seeds)]

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

    # print(seeds_deg)
    # print(seeds_deg_2)

    # for x in set(seeds_deg) & set(seeds_deg_2):
    #     seeds_deg_2.remove(x)    

    # num_seeds_supp = max(0, min(num_seeds // 5, len(seeds_deg_2)))

    # seeds_deg_supp.extend(seeds_deg_2[:num_seeds_supp])

    num_seeds_supp = max(num_seeds // 10, 1)
    seeds_deg_supp = seeds_deg[:-num_seeds_supp]
    for i in seeds_deg[:num_seeds_supp]:
        common = []
        for j in range(v):
            if int(i) == j:
                continue
            common.append([j, len(set(graph[i]) & set(graph[str(j)]))])
        common.sort(key=itemgetter(1), reverse=True)
        for c in common:
            k = str(c[0])
            if k not in seeds_deg_supp:
                seeds_deg_supp.append(k)
                break

    # seeds_deg_supp.extend(seeds_deg_2[:num_seeds_supp])


    # print(seeds_deg_supp)

    # print(seeds_highest_deg)

    # Print the idea number of nodes this strategy can capture    
    print sim.run(graph, {"many":seeds, "deg":seeds_deg})
    print sim.run(graph, {"deg":seeds_deg, "two":seeds_deg_supp})


    # print(seeds_deg_supp)

    if num_players == 2:
        seeds = seeds_deg_supp


    f = open(filename[:-4] + 'sol', 'w')
    for s in seeds:
        f.write(str(s) + '\n')
    f.close()
