import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from topology import Topology
import calendar
import time


if __name__ == '__main__':

    # G = nx.DiGraph()
    N = 16
    nodes = range(N)
    np.random.seed(5)
    t = Topology()
    # bb = nx.edge_betweenness_centrality(G, normalized=False)
    # nx.set_edge_attributes(G, 'weight', bb)
    # nx.set_edge_attributes(G, 'capacity', bb)

    T_matrix = t.createTrafficMatrix(0.5,1.5,N)
    G = t.createManhattanTopology(N)


    remaining_node = 4*np.ones(N)
    rem = 4*np.ones(N)
    taken = 4*np.zeros(N)
    tk = 4*np.zeros(N)
    tsd_copy = T_matrix.copy()


    #creation of the real manahttan with a greedy algorithm
    for n in nodes:

        if n == 0:
            i,j = t.findMaxAndRemove(tsd_copy,N)
            G.node[0]['node'] = i
            G.node[1]['node'] = j
            G.edge[0][1]['weight'] = T_matrix[i][j] + T_matrix[j][i]
            remaining_node[i]-=1
            remaining_node[j] -=1
            taken[i] = 1
            taken[j] = 1

            #todo elimina
            tk[0] = 1
            rem[0] -= 1
            rem[1] -= 1
            tk[1] = 1
            #todo finqua
            for s,d in G.edges(0):
                if (s,d) != (0,1):
                    argmax,max = t.findMaxForRowAndRemove(tsd_copy,i)
                    G.node[d]['node'] = argmax
                    G.edge[s][d]['weight'] = T_matrix[i][argmax] + T_matrix[argmax][i]
                    remaining_node[i] -= 1
                    remaining_node[argmax] -= 1
                    taken[argmax] = 1
                    tk[d] = 1
                    rem[s] -= 1
                    rem[d] -= 1
        else:
            for s, d in G.edges(n):

                if len(G.edge[s][d])== 0 and rem[s]>0:
                        avail = rem[s]
                        while avail == rem[s]:
                            if tk[d] == 1 and tk[s]== 1 and len(G.edge[s][d]) == 0:
                                G.edge[s][d]['weight'] = T_matrix[G.node[s]['node']][G.node[d]['node']] + T_matrix[G.node[d]['node']][G.node[s]['node']]
                                rem[s] -= 1
                                rem[d] -= 1
                                break
                            argmax,max = t.findMaxForRowAndRemove(tsd_copy,G.node[n]['node'])
                            #if remaining_node[argmax] > 0 and taken[argmax]== 0:
                            if (rem[d] > 0 and tk[d] == 0 and taken[argmax] == 0):
                                G.node[d]['node'] = argmax
                                G.edge[s][d]['weight'] = T_matrix[G.node[n]['node']][argmax] + T_matrix[argmax][G.node[n]['node']]
                                remaining_node[G.node[n]['node']] -= 1
                                remaining_node[argmax] -= 1
                                taken[argmax] = 1
                                rem[s] -= 1
                                rem[d] -= 1
                                tk[d] = 1

    #print of the new manahttan matrix
    t.printManahttan(G)

    #routing traffic towards the topology
    t.routingManahttan(G,T_matrix,N)

    #search for f_max
    f_max =  t.fmax(G)

    print f_max

    nx.draw_networkx(G, arrows=True, with_labels=True)

    plt.title('fmax = ' + str(f_max[0]))
    plt.show()

    #implementation of the simulated annealing
    G_first = G.copy()
    fMax = f_max[0]
    for i in range(200):
        print '-----------------'
        T = calendar.timegm(time.gmtime())
        print ('Prima dello swapping')
        t.printManahttan(G_first)
        sA = t.simulatedAnnealing(T_matrix,G_first,N)
        print 'Dopo lo swapping'
        t.printManahttan(sA[1])
        if sA[0] < fMax:
            G_first = sA[1]
            print 'Solution accepted   fmax-> ',sA[0]
            accepted = True
            fMax = sA[0]

        else:
            tsh = np.random.uniform(0,1)
            p = np.exp(-i/T)
            if p > tsh:
                G_first = sA[1]
                print 'Solution accepted for p  fmax->',sA[0]
                accepted = True
                fMax = sA[0]

            else:
                accepted = False
                print 'Solution not accepted'


    print f_max[0] , fMax








