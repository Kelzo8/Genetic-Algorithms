
from graphviz import Digraph


def visualise_tree(tree, filename="gp_tree"):
    """Visualise a GP expression tree using Graphviz."""

    graph = Digraph(format="png")

    graph.attr(
        rankdir="TB",
        nodesep="0.5",
        ranksep="0.7"
    )

    graph.attr(
        "node",
        shape="box",
        style="rounded,filled",
        fontname="Arial"
    )

    node_count = 0

    def add_node(subtree):
        nonlocal node_count

        current_id = str(node_count)
        node_count += 1

        if isinstance(subtree, tuple):
            label = subtree[0]
            graph.node(
                current_id,
                label=str(label),
                fillcolor="lightblue"
            )

            for child in subtree[1:]:
                child_id = add_node(child)
                graph.edge(current_id, child_id)

        else:
            graph.node(
                current_id,
                label=str(subtree),
                fillcolor="lightyellow"
            )

        return current_id

    add_node(tree)

    graph.render(filename, cleanup=True, view=True)

    return graph
