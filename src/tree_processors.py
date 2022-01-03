from functools import reduce


reduce_lists = lambda acc, level: (acc + level['leaves']) if 'leaves' in level else acc


def generate_key(name):
    return name.strip().lower().replace(' ', '_')


def preprocess_tree(t, data, key_prepend='', current_level=1):
    key = generate_key(t['name'])
    if key_prepend:
        key = key_prepend + '-' + key
    t['color'] = data['color']
    t['key'] = key
    t['level'] = current_level
    t['weight'] = 1
    next_level = current_level + 1
    if 'leaves' in t:
        for leaf in t['leaves']:
            preprocess_tree(leaf, data, key, next_level)
    return t


def are_keys_equal(k1, k2):
    if k1 == k2:
        return True

    parts1, parts2 = k1.split('-'), k2.split('-')
    for p1, p2 in zip(parts1, parts2):
        if p1 == '' or p2 == '':
            continue
        if p1 != p2:
            return False
    return True


def _merge_levels(*levels):
    if len(levels) == 0:
        raise Exception("Nothing to merge")
    if len(levels) == 1:
        return levels[0]

    return {
        **levels[0],
        'color': 'black',
        'weight': sum([level['weight'] for level in levels]),
        'leaves': reduce(reduce_lists, levels, [])
    }


def _extract_leaves(nodes):
    return [node['leaves'] if 'leaves' in node else [] for node in nodes]


def merge_levels(*node_lists):
    nodes_all = reduce(lambda acc, nl: acc + nl, node_lists, [])
    keys = set([n['key'] for n in nodes_all])
    result = []
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

