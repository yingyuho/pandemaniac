from json import load
import matplotlib.pyplot as plt

def json_analyze(filename):
  f = open(filename, 'r')
  graph = load(f)
  data_hist(graph)
  udgraph = go_undirected(graph)
  (clavg, cl) = cluster_anal(udgraph)
  print "Average clustering coefficient is " + str(clavg)
  print "Overall clustering coefficient is " + str(cl)
  (maxd, avgd) = diameter_anal(udgraph)
  print "Diameter is " + str(maxd)
  print "Average Diameter is " + str(avgd)
  f.close()
  f = open("webgraph_params.txt", 'w')
  f.write("Average clustering coefficient is " + str(clavg) + "\n")
  f.write("Overall clustering coefficient is " + str(cl) + "\n")
  f.write("Diameter is " + str(maxd) + "\n")
  f.write("Average Diameter is " + str(avgd) + "\n")
  f.close()
  return
  
def data_hist(data):
  degree = []
  indegree = [0] * len(data)
  for node in data:
    degree.append(len(data[node]))
    for neighb in data[node]:
      indegree[int(neighb)] += 1
  h = plt.hist(degree, bins = max(degree))
  plt.savefig("webgraph_histogram.png")
  plt.clf()
  hi = plt.hist(indegree, bins = max(indegree))
  plt.savefig("webgraph_inhistogram.png")
  plt.clf()
  ccdf = []
  ccdfin = []
  r = range(max(degree) + 1)
  r.reverse()
  prev = 0
  for i in r:
    ccdf.append(prev + degree.count(i))
    prev = ccdf[-1]
  for c in range(len(ccdf)):
    ccdf[c] /= float(len(data))
  f = plt.plot(r, ccdf)
  plt.savefig("webgraph_ccdf.png")
  plt.clf()
  r2 = range(max(indegree) + 1)
  r2.reverse()
  prev = 0
  for i in r2:
    ccdfin.append(prev + indegree.count(i))
    prev = ccdfin[-1]
  for c in range(len(ccdfin)):
    ccdfin[c] /= float(len(data))
  fi = plt.plot(r2, ccdfin)
  plt.savefig("webgraph_ccdfin.png")
  plt.clf()
  return

def go_undirected(graph):
  newgraph = graph.copy()
  for v in newgraph:
    for neighb in newgraph[v]:
      if v not in graph[neighb]:
        newgraph[neighb].append(v)
  return newgraph
  
def cluster_anal(fl):
  triangles = {}
  ntriples = []
  ntriangles = []
  for friend in fl:
    n = len(fl[friend])
    if n >= 2:
      ntriples.append(n * (n - 1) / 2)
      ntriang = 0
      for frfr in fl[friend]:
        intersect = list(set(fl[frfr]) & set(fl[friend]))
        ntriang += len(intersect)
        for cofr in intersect:
          triangle = tuple(sorted([friend, frfr, cofr]))
          if triangle not in triangles:
            triangles[triangle] = 1
      ntriang = ntriang / 2
      ntriangles.append(ntriang)
  cli = []
  cl = 3 * float(len(triangles)) / sum(ntriples)
  for i in range(len(ntriples)):
    cli.append(float(ntriangles[i]) / float(ntriples[i]))
  clavg = sum(cli) / len(fl)
  return (clavg, cl)
    
def diameter_anal(graph):
  vx = len(graph)
  dis = []
  for i in range(vx):
    dis.append([0xffff] * vx)
  for v in range(vx):
    dis[v][v] = 0
    for neighb in graph[unicode(v)]:
      dis[v][int(neighb)] = 1
  for k in range(vx):
    for i in range(vx):
      for j in range(vx):
        if dis[i][k] + dis[k][j] < dis[i][j]:
          dis[i][j] = dis[i][k] + dis[k][j]
          dis[j][i] = dis[i][j]
  maxd = 0
  sumd = 0
  dc = 0
  for i in range(vx - 1):
    for j in range(i + 1, vx):
      if dis[i][j] != 0xffff:
        dc += 1
        sumd += dis[i][j]
        if dis[i][j] > maxd:
          maxd = dis[i][j]
      else:
        return (0, 0)
  avgd = float(sumd) / float(dc)
  return (maxd, avgd)
    
if __name__ == "__main__":
  json_analyze("network_stats.txt")
