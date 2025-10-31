import json
import os
import numpy as np

class CatBoostTreeModelLoader:

    def __init__(self, cb_model):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, 'model.json')
            cb_model.save_model(tmp_file, format='json')
            with open(tmp_file, encoding='utf-8') as fh:
                self.loaded_cb_model = json.load(fh)
        self.num_trees = len(self.loaded_cb_model['oblivious_trees'])
        self.max_depth = self.loaded_cb_model['model_info']['params']['tree_learner_options']['depth']

    def get_trees(self, data=None, data_missing=None):
        trees = []
        for tree_index in range(self.num_trees):
            leaf_weights = self.loaded_cb_model['oblivious_trees'][tree_index]['leaf_weights']
            leaf_weights_unraveled = [0] * (len(leaf_weights) - 1) + leaf_weights
            leaf_weights_unraveled[0] = sum(leaf_weights)
            for index in range(len(leaf_weights) - 2, 0, -1):
                leaf_weights_unraveled[index] = leaf_weights_unraveled[2 * index + 1] + leaf_weights_unraveled[2 * index + 2]
            leaf_values = self.loaded_cb_model['oblivious_trees'][tree_index]['leaf_values']
            leaf_values_unraveled = [0] * (len(leaf_values) - 1) + leaf_values
            children_left = [i * 2 + 1 for i in range(len(leaf_values) - 1)]
            children_left += [-1] * len(leaf_values)
            children_right = [i * 2 for i in range(1, len(leaf_values))]
            children_right += [-1] * len(leaf_values)
            children_default = [i * 2 + 1 for i in range(len(leaf_values) - 1)]
            children_default += [-1] * len(leaf_values)
            split_features_index = []
            borders = []
            for elem in self.loaded_cb_model['oblivious_trees'][tree_index]['splits']:
                split_type = elem.get('split_type')
                if split_type == 'FloatFeature':
                    split_feature_index = elem.get('float_feature_index')
                    borders.append(elem['border'])
                elif split_type == 'OneHotFeature':
                    split_feature_index = elem.get('cat_feature_index')
                    borders.append(elem['value'])
                else:
                    split_feature_index = elem.get('ctr_target_border_idx')
                    borders.append(elem['border'])
                split_features_index.append(split_feature_index)
            split_features_index_unraveled = []
            for counter, feature_index in enumerate(split_features_index[::-1]):
                split_features_index_unraveled += [feature_index] * 2 ** counter
            split_features_index_unraveled += [0] * len(leaf_values)
            borders_unraveled = []
            for counter, border in enumerate(borders[::-1]):
                borders_unraveled += [border] * 2 ** counter
            borders_unraveled += [0] * len(leaf_values)
            trees.append(SingleTree({'children_left': np.array(children_left), 'children_right': np.array(children_right), 'children_default': np.array(children_default), 'feature': np.array(split_features_index_unraveled), 'threshold': np.array(borders_unraveled), 'value': np.array(leaf_values_unraveled).reshape((-1, 1)), 'node_sample_weight': np.array(leaf_weights_unraveled)}, data=data, data_missing=data_missing))
        return trees