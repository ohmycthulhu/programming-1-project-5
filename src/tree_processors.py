from functools import reduce


"""
    File that holds helpers for working with trees
"""

reduce_leaves = lambda acc, level: (acc + level['leaves']) if 'leaves' in level else acc


def generate_key(name):
    """Generates new key by name"""
    return name.strip().lower().replace(' ', '_')


def preprocess_tree(t, data, key_prepend='', current_level=1):
    """Recursive function for processing each node of the tree"""
    key = generate_key(t['name'])
    # key_prepend displays the path to the node
    if key_prepend:
        key = key_prepend + '-' + key

    # Color, key, and level are saved for easy processing
    # Weight signifies the amount of merged nodes
    t['color'] = data['color']
    t['key'] = key
    t['level'] = current_level
    t['weight'] = 1
    next_level = current_level + 1

    # Preprocess also all leaves if there are any
    if 'leaves' in t:
        for leaf in t['leaves']:
            preprocess_tree(leaf, data, key, next_level)

    return t


def _merge_levels(*levels):
    if len(levels) == 0:
        raise Exception("Nothing to merge")
    if len(levels) == 1:
        return levels[0]

    return {
        **levels[0],
        # Replace the color by 'black' to show that there are many nodes merged
        'color': 'black',
        # New weight is sum of all weights
        'weight': sum([level['weight'] for level in levels]),
        # New leaves are combination of all leaves
        'leaves': reduce(reduce_leaves, levels, [])
    }


def _extract_leaves(nodes):
    return [(node['leaves'] if 'leaves' in node else []) for node in nodes]


def merge_levels(*node_lists):
    # Merge all nodes from node_lists
    nodes_all = reduce(lambda acc, nl: acc + nl, node_lists, [])

    # Get unique keys
    keys = set([n['key'] for n in nodes_all])
    result = []

    # Merge all nodes by unique keys
    for key in keys:
        nodes = [n for n in nodes_all if n['key'] == key]
        result.append(_merge_levels(*nodes))

    return result


def merge_trees(*roots, name='Result Tree', color='black'):
    initial_level = merge_levels(*_extract_leaves(roots))

    result = {
        'name': name,
        'color': color,
        'leaves': initial_level,
    }

    parents_level = initial_level
    while len(parents_level) > 0:
        # Merge all children
        current_level = merge_levels(*_extract_leaves(parents_level))

        # Distribute children
        for parent in parents_level:
            parent['leaves'] = [level for level in current_level if level['key'].startswith(parent['key'])]

        # Reassign parents
        parents_level = current_level

    return result

