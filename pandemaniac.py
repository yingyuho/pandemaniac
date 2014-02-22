###############################################################################
# Naive Implementation:                                                       #
# Randomly choose num_seeds of nodes out of top num_seeds * num_player nodes  #
# with the largest degree.                                                    #
###############################################################################
import sys
import json
import random
import sim

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
    f = open(filename[:-4] + 'sol', 'w')
    seeds = []
    s = random.choice(topList)[0]
    for i in range(num_seeds):
	while str(s) in seeds:
	    s = random.choice(topList)[0]
	seeds.append(str(s))
	f.write(str(s) + '\n')
    f.close()
	
    # Print the idea number of nodes this strategy can capture    
    print sim.run(graph, {"strategy":seeds})

