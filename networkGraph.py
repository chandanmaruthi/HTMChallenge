import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph):
    # create networkx graph
    G=nx.Graph()
    # add nodes
    G.add_nodes_from(["animal","bat","cat","dog","elephant","fish","goat","horse","ink","j","k","l"])
    labels = {"animal":"animal","bat":"bat","cat":"cat","dog":"dog","elephant":"elephant","fish":"fish","goat":"goat","h":"h","i":"i","j":"j","k":"k","l":"l"}
    pos = nx.spring_layout(G)
    H=nx.relabel_nodes(G,labels)
    # add edges
    for edge in graph:
        H.add_edge(edge[0], edge[1])

    # draw graph
    nx.draw(H, node_color="red", with_labels = True, node_shape='o')

    # show graph
    plt.savefig("/home/chandan/chandan/code/simple_path.png")
    #plt.show()

# draw example
graph = [('animal', 'bat'),('animal', 'cat'),('animal','dog'),('bat','fish'),('bat','goat'),('c','h'),('c','l'),('f','k')]
draw_graph(graph)
