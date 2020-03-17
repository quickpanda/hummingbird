"""
Tests scikit-RandomForestClassifier converter.
"""
import unittest
import warnings

import numpy as np
import torch
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, ExtraTreesClassifier

from hummingbird import convert_sklearn
from hummingbird.common.data_types import Float32TensorType
from sklearn.tree import DecisionTreeClassifier


class TestSklearnRandomForestConverter(unittest.TestCase):

    def _run_random_forest_classifier_converter(self, depths, num_classes):
        for max_depth in depths:
            model = RandomForestClassifier(n_estimators=10, max_depth=max_depth)
            X = np.random.rand(100, 200)
            X = np.array(X, dtype=np.float32)
            y = np.random.randint(num_classes, size=100)

            model.fit(X, y)
            pytorch_model = convert_sklearn(
                model,
                [("input", Float32TensorType([1, 20]))]
            )
            self.assertTrue(pytorch_model is not None)
            self.assertTrue(np.allclose(model.predict_proba(
                X), pytorch_model(torch.from_numpy(X))[1].data.numpy()))

    # binary
    def test_random_forest_classifier_binary_converter(self):
        self._run_random_forest_classifier_converter([1, 3, 8, 10, 12, None], 2)

    # multi
    def test_random_forest_classifier_multi_converter(self):
        self._run_random_forest_classifier_converter([1, 3, 8, 10, 12, None], 3)

    def test_random_forest_regressor_converter(self):
        for max_depth in [1, 3, 8, 10, 12, None]:
            model = RandomForestRegressor(n_estimators=10, max_depth=max_depth)
            X = np.random.rand(100, 200)
            X = np.array(X, dtype=np.float32)
            y = np.random.randint(3, size=100)

            model.fit(X, y)
            pytorch_model = convert_sklearn(
                model,
                [("input", Float32TensorType([1, 20]))]
            )
            self.assertTrue(pytorch_model is not None)
            self.assertTrue(np.allclose(model.predict(X), pytorch_model(
                torch.from_numpy(X)).view(-1).numpy()))

    def test_decision_tree_classifier_converter(self):
        for max_depth in [1, 3, 8, 10, 12, None]:
            model = DecisionTreeClassifier(max_depth=max_depth)
            X = np.random.rand(100, 200)
            X = np.array(X, dtype=np.float32)
            y = np.random.randint(3, size=100)

            model.fit(X, y)
            pytorch_model = convert_sklearn(
                model,
                [("input", Float32TensorType([1, 20]))]
            )
            self.assertTrue(pytorch_model is not None)
            self.assertTrue(np.allclose(model.predict_proba(
                X), pytorch_model(torch.from_numpy(X))[1].data.numpy()))

    def test_extra_trees_classifier_converter(self):
        warnings.filterwarnings("ignore")
        for max_depth in [1, 3, 8, 10, 12, None]:
            model = ExtraTreesClassifier(n_estimators=10, max_depth=max_depth)
            X = np.random.rand(100, 200)
            X = np.array(X, dtype=np.float32)
            y = np.random.randint(3, size=100)

            model.fit(X, y)
            pytorch_model = convert_sklearn(
                model,
                [("input", Float32TensorType([1, 20]))]
            )
            self.assertTrue(pytorch_model is not None)
            self.assertTrue(np.allclose(model.predict_proba(
                X), pytorch_model(torch.from_numpy(X))[1].data.numpy()))


if __name__ == "__main__":
    unittest.main()
