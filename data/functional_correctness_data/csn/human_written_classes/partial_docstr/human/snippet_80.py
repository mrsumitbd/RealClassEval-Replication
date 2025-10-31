from collections import defaultdict
import numpy as np
import copy

class TrieMinimizer:

    def __init__(self):
        pass

    def minimize(self, trie, dict_storage=False, make_cashed=False, make_numpied=False, precompute_symbols=None, allow_spaces=False, return_groups=False):
        N = len(trie)
        if N == 0:
            raise ValueError('Trie should be non-empty')
        node_classes = np.full(shape=(N,), fill_value=-1, dtype=int)
        order = self.generate_postorder(trie)
        index = order[0]
        node_classes[index] = 0
        class_representatives = [index]
        node_key = ((), (), trie.is_final(index))
        classes, class_keys = ({node_key: 0}, [node_key])
        curr_index = 1
        for index in order[1:]:
            letter_indexes = tuple(trie._get_letters(index, return_indexes=True))
            children = trie._get_children(index)
            children_classes = tuple((node_classes[i] for i in children))
            key = (letter_indexes, children_classes, trie.is_final(index))
            key_class = classes.get(key, None)
            if key_class is not None:
                node_classes[index] = key_class
            else:
                class_keys.append(key)
                classes[key] = node_classes[index] = curr_index
                class_representatives.append(curr_index)
                curr_index += 1
        compressed = Trie(trie.alphabet, is_numpied=make_numpied, dict_storage=dict_storage, allow_spaces=allow_spaces, precompute_symbols=precompute_symbols)
        L = len(classes)
        new_final = [elem[2] for elem in class_keys[::-1]]
        if dict_storage:
            new_graph = [defaultdict(int) for _ in range(L)]
        elif make_numpied:
            new_graph = np.full(shape=(L, len(trie.alphabet)), fill_value=Trie.NO_NODE, dtype=int)
            new_final = np.array(new_final, dtype=bool)
        else:
            new_graph = [[Trie.NO_NODE for a in trie.alphabet] for i in range(L)]
        for (indexes, children, final), class_index in sorted(classes.items(), key=lambda x: x[1]):
            row = new_graph[L - class_index - 1]
            for i, child_index in zip(indexes, children):
                row[i] = L - child_index - 1
        compressed.graph = new_graph
        compressed.root = L - node_classes[trie.root] - 1
        compressed.final = new_final
        compressed.nodes_number = L
        compressed.data = [None] * L
        if make_cashed:
            compressed.make_cashed()
        if precompute_symbols is not None:
            if trie.is_terminated and trie.precompute_symbols and (trie.allow_spaces == allow_spaces):
                for i, node_index in enumerate(class_representatives[::-1]):
                    compressed.data[i] = copy.copy(trie.data[node_index])
            else:
                precompute_future_symbols(compressed, precompute_symbols, allow_spaces)
        if return_groups:
            node_classes = [L - i - 1 for i in node_classes]
            return (compressed, node_classes)
        else:
            return compressed

    def generate_postorder(self, trie):
        """
        Обратная топологическая сортировка
        """
        order, stack = ([], [])
        stack.append(trie.root)
        colors = ['white'] * len(trie)
        while len(stack) > 0:
            index = stack[-1]
            color = colors[index]
            if color == 'white':
                colors[index] = 'grey'
                for child in trie._get_children(index):
                    if child != Trie.NO_NODE and colors[child] == 'white':
                        stack.append(child)
            else:
                if color == 'grey':
                    colors[index] = 'black'
                    order.append(index)
                stack = stack[:-1]
        return order