#!/usr/bin/env python

import sys
import json
import random
import sim
from operator import itemgetter

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
    seeds_cheat = [str(c_sorted[i][0]) for i in range(num_seeds+2)]
    random.shuffle(seeds_cheat)
    seeds_cheat = seeds_cheat[:num_seeds]

    print sim.run(graph, {"deg":seeds_deg, "cheat":seeds_cheat})

    f = open(filename[:-4] + 'sol', 'w')
    for s in seeds_cheat:
        f.write(str(s) + '\n')
    f.close()