import csv
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def create_author_collaboration_graph(file_path, filter_author=None):
    G = nx.Graph()
    author_counts = defaultdict(int)

    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  

        collaboration_count = defaultdict(int)

        for row in reader:
            paper_title = row[0]
            authors = [author.strip() for author in row[1].split(';')]

            for author in authors:
                author_counts[author] += 1

            for i, author1 in enumerate(authors):
                for j, author2 in enumerate(authors):
                    if i < j:
                        author_pair = tuple(sorted([author1, author2]))
                        collaboration_count[author_pair] += 1

    for (author1, author2), weight in collaboration_count.items():
        G.add_edge(author1, author2, weight=weight / 20)

    if filter_author:
        if filter_author in G:
            neighbors = list(G.neighbors(filter_author))
            subgraph_nodes = [filter_author] + neighbors
            G = G.subgraph(subgraph_nodes).copy()
        else:
            print(f"Author '{filter_author}' not found in the graph.")
            return

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)  

    node_sizes = [100 + 1 * author_counts[node] for node in G.nodes()]

    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=node_sizes)
    edges = nx.draw_networkx_edges(
        G, pos, edge_color='gray',
        width=[G[u][v]['weight'] for u, v in G.edges()]
    )
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

    plt.title(f'Collaboration Network for Author "{filter_author}"' if filter_author else 'Full Collaboration Network')
    plt.show()


import sys

if len(sys.argv) > 1:
    filter_author = sys.argv[1]
else:
    filter_author = None  

file_path = 'papers_data_clean.csv'
create_author_collaboration_graph(file_path, filter_author)
