import time
from collections import defaultdict
from itertools import combinations


def load_data():
    with open("input", "r") as f:
        edges = [tuple(sorted(l.strip().split("-"))) for l in f]

    neighbours = defaultdict(set)
    for a, b in edges:
        neighbours[a].add(b)
        neighbours[b].add(a)

    return neighbours


def lan_party():
    neighbours = load_data()
    all_cliques = set()
    t_cliques = set()
    for n1, nbr in neighbours.items():
        for n2, n3 in combinations(nbr, 2):
            if n2 in neighbours[n3]:
                clique = tuple(sorted((n1, n2, n3)))
                all_cliques.add(clique)
                if any(n[0] == "t" for n in clique):
                    t_cliques.add(clique)

    print(f"Total number of 3-cliques: {len(all_cliques)}")
    print(f"Number of 3-cliques that contain a t node: {len(t_cliques)}")

    # now repeatedly attempt to extend each n-clique to one or more n+1 cliques.
    # This naive algorithm is probably exponential in the number of nodes, it takes
    # >10s to run on a MacBook Pro
    start = time.perf_counter()
    last_cliques = all_cliques
    while True:
        new_cliques = set()
        for clique in last_cliques:
            for node in clique:
                for nbr in neighbours[node]:
                    # Without the nbr > clique[-1] test this takes ~11s, with it ~2s.
                    # This is a safe optimization because extending the k-clique
                    # {n_1, ... n_k} with a node m whose label is < n_k produces the
                    # same k+1-clique result as starting with the k-clique
                    # {n_1, ... n_k-1} U {m}  and extending that with n_k - any
                    # possibilities including such a nbr will be covered by another
                    # iteration of the outermost for loop.
                    if nbr > clique[-1] and all(n in neighbours[nbr] for n in clique):
                        new_cliques.add(tuple(sorted((nbr, *clique))))
        if new_cliques:
            last_cliques = new_cliques
        else:
            break

    end = time.perf_counter()

    # at this point, last_cliques only contains cliques of maximum size
    final_clique = next(iter(last_cliques))
    print(f"Max clique size: {len(final_clique)}")
    print(f"Number of cliques of this size: {len(last_cliques)}")
    print(f"Time taken: {end - start:.2f} sec")
    print(",".join(final_clique))


if __name__ == "__main__":
    lan_party()