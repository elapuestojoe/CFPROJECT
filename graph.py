from random import choice, randrange
import networkx as nx
import matplotlib.pyplot as plt

colorNodes = ["red", "green", "orange", "yellow", "gray", "blue", "purple", "orange", "green", "cyan"]
options = [0,1,2,3,4,5,6,7,8,9]

G=nx.Graph()
for i in range(10):
	G.add_node(str(i))

G.add_edge("2", "0", color=colorNodes[2], weight=5)
G.add_edge("6", "7", color=colorNodes[6], weight=9)
G.add_edge("7", "1", color=colorNodes[7], weight=11)
G.add_edge("3", "4", color=colorNodes[3], weight=12)
G.add_edge("5", "7", color=colorNodes[5], weight=13)
G.add_edge("7", "9", color=colorNodes[7], weight=15)
G.add_edge("4", "1", color=colorNodes[4], weight=17)
G.add_edge("6", "8", color=colorNodes[6], weight=23)
G.add_edge("9", "2", color=colorNodes[9], weight=25)

color_map = []
for node in G:
	color_map.append(colorNodes[int(node)])
edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]
pos = nx.shell_layout(G)

labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_labels(G,pos)
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels, label_pos=0.25)
nx.draw(G, pos, node_color = color_map, with_labels=True)
plt.show()
