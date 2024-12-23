import networkx as nx
from networkx.algorithms.clique import enumerate_all_cliques


def load_data():
    G = nx.Graph()
    with open("input", "r") as f:
        G.add_edges_from(tuple(l.strip().split("-")) for l in f)

    return G


def using_networkx():
    G = load_data()

    three_cliques_with_t = 0
    for clique in enumerate_all_cliques(G):
        if len(clique) != 3:
            continue
        if any(n[0] == "t" for n in clique):
            three_cliques_with_t += 1

    print(f"Numer of 3-cliques containing a t-node: {three_cliques_with_t}")
    # The final value of clique at the end of the loop will be the largest clique
    # in the graph - the problem wording implies there is only one clique of this
    # size
    print(f"Password (members of largest clique): {','.join(sorted(clique))}")


if __name__ == "__main__":
    using_networkx()
