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
safety_coefficient = 5

def rand_degree(centrality, num_seeds, num_players):
    pool = centrality[:num_seeds * num_players + 1]
    result = []
    while len(result) < num_seeds:
        c = random.choice(centrality)
        if c[0] not in result:
            result.append(str(c[0]))
    return result


if __name__ == "__main__":
    filename = sys.argv[1]
    graph = json.loads(open(filename).read())
    num_players = int(filename.split('.')[0])
    num_seeds = int(filename.split('.')[1])

    competition_factor = 64 / num_players
    stair_width = num_players / 8.0

    # Calculate centrality
    centrality = []
    v = len(graph)
    for i in range(v):
        centrality.append([i, len(graph[str(i)])])

    c_sorted = sorted(centrality, key=itemgetter(1), reverse=True)

    dic = {}
    for i in range(num_players - 1):
        dic["deg" + str(i)] = rand_degree(centrality, num_seeds, num_players)
                
    # Randomly choose a number of seeds from the topList and output to file
    seeds_start = (num_players * num_seeds) / competition_factor + 1
    seeds = []
    while len(seeds) < num_seeds:
        seeds_end = seeds_start + int(stair_width * num_seeds)

        stair = [str(c_sorted[i][0]) for i in range(seeds_start, seeds_end)]
        random.shuffle(stair)
        seeds += stair[:(num_seeds / safety_coefficient)]
        seeds_start = seeds_end

    dic["many"] = seeds

    # Print the idea number of nodes this strategy can capture
    print sim.run(graph, dic)
    print (len(graph))

    f = open(filename[:-4] + 'sol', 'w')
    for s in seeds:
        f.write(str(s) + '\n')
    f.close()
