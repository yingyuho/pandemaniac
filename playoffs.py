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
                
    # Randomly choose a number of seeds from the topList and output to file
    seeds_start = (num_players * num_seeds) / 8
    seeds_end = seeds_start + (2 * num_seeds)
    print([seeds_start,seeds_end])

    seeds = [str(c_sorted[i][0]) for i in range(seeds_start, seeds_end)]
    random.shuffle(seeds)
    seeds = seeds[:num_seeds]

    print(seeds_deg)
    print(seeds)

    # Print the idea number of nodes this strategy can capture
    print sim.run(graph, {"many":seeds, "deg":seeds_deg})

    f = open(filename[:-4] + 'sol', 'w')
    for s in seeds:
        f.write(str(s) + '\n')
    f.close()
