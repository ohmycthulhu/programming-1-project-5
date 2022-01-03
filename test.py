from src.tree_processors import *
from json import load, dump
import matplotlib.pyplot as plt
import pydot


with open('meta/student01.json') as file:
    data = load(file)
    t1 = data['map']['root']
    for leaf in t1['leaves']:
        preprocess_tree(leaf, data)


with open('meta/student03.json') as file:
    data = load(file)
    t2 = data['map']['root']
    for leaf in t2['leaves']:
        preprocess_tree(leaf, data)


result_tree = merge_trees(t1, t2, name='OOP')

print('It worked!')

with open('tmp/result.json', 'w') as file:
    dump(result_tree, file)


graph = pydot.Dot(graph_type="digraph", rankdir="LR")

current_level = [result_tree]
while len(current_level) > 0:
    next_level = []
    for level in current_level:
        for leaf in level['leaves']:
            graph.add_node(
                pydot.Node(
                    leaf['name'],
                    color=leaf['color'],
                    width=0.5*leaf['weight'],
                    penwidth=leaf['weight'],
                )
            )
            graph.add_edge(
                pydot.Edge(
                    level['name'],
                    leaf['name'],
                    color=leaf['color'],
                    width=0.5*leaf['weight'],
                    penwidth=leaf['weight'],
                )
            )
        next_level += level['leaves']
    current_level = next_level

graph.write_png('tmp/result.png')
