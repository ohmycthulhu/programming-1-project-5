import json
import src.tree_processors as tp
import pydot


class MindMapController:
    def __init__(self, files):
        self._files = files
        self._trees = None

    def export(self, path):
        tree = self._merged_tree()
        graph = pydot.Dot(graph_type="digraph", rankdir="LR")

        current_level = [tree]
        while len(current_level) > 0:
            next_level = []
            for level in current_level:
                self._process_level(graph, level)
                next_level += level['leaves']
            current_level = next_level

        graph.write_png(path)

    @staticmethod
    def _process_level(graph, level):
        for leaf in level['leaves']:
            graph.add_node(
                pydot.Node(
                    leaf['name'],
                    color=leaf['color'],
                    width=0.5 * leaf['weight'],
                    penwidth=leaf['weight'],
                )
            )
            graph.add_edge(
                pydot.Edge(
                    level['name'],
                    leaf['name'],
                    color=leaf['color'],
                    width=0.5 * leaf['weight'],
                    penwidth=leaf['weight'],
                )
            )

    def _merged_tree(self):
        return tp.merge_trees(*self._get_trees())

    def _get_trees(self):
        if self._trees is None:
            self._trees = [self._load_tree(p) for p in self._files]
        return self._trees

    @staticmethod
    def _load_tree(path):
        with open(path) as file:
            data = json.load(file)
            tree = data['map']['root']
            for leaf in tree['leaves']:
                tp.preprocess_tree(leaf, data)
        return tree
