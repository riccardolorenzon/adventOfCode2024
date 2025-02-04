import sys
from collections import defaultdict
import networkx as nx


def common_connected_nodes(
    connected_nodes: list[str], other_connected_nodes: list[str]
):
    for node in connected_nodes:
        if node in other_connected_nodes:
            yield node


def read_input() -> list[tuple[str, str]]:
    res = []
    with open(sys.argv[1]) as f:
        while line := f.readline().strip():
            n1, n2 = line.split("-")
            res.append((n1, n2))
    return res


def map_nodes() -> dict:
    lan_nodes = defaultdict(list)
    for node_1, node_2 in read_input():
        lan_nodes[node_1].append(node_2)
        lan_nodes[node_2].append(node_1)
    return lan_nodes


def get_ternary_sets(lan_nodes: dict[str, list]):
    ternary_sets = set()
    for node, connected_nodes in lan_nodes.items():
        for connected_node in connected_nodes:
            for common_node in common_connected_nodes(
                connected_nodes, lan_nodes[connected_node]
            ):
                ternary_sets.add(tuple(sorted([node, connected_node, common_node])))
    return ternary_sets


def find_longest_clique():
    G = nx.Graph()
    for node_1, node_2 in read_input():
        G.add_nodes_from([node_1, node_2])
        G.add_edge(node_1, node_2)
    print(",".join(sorted(max(list(nx.find_cliques(G)), key=lambda x: len(x)))))


if __name__ == "__main__":
    lan_nodes = map_nodes()
    print(
        len(
            [
                t
                for t in get_ternary_sets(lan_nodes)
                if "t" in [t[0][0], t[1][0], t[2][0]]
            ]
        )
    )
    find_longest_clique()
