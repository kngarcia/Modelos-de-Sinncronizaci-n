import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from models import kuramoto_model_vectorized, winfree_model_vectorized, order_parameter

class TestModels(unittest.TestCase):
    def setUp(self):
        self.N = 10
        self.phases = np.random.uniform(0, 2*np.pi, self.N)
        self.omega = np.ones(self.N)
        self.K = 1.0
        self.dt = 0.01
    
    def test_order_parameter_range(self):
        R = order_parameter(self.phases)
        self.assertTrue(0 <= R <= 1)
    
    def test_kuramoto_shape(self):
        new_phases = kuramoto_model_vectorized(self.phases, self.omega, self.K, self.dt)
        self.assertEqual(new_phases.shape, self.phases.shape)
    
    def test_winfree_shape(self):
        new_phases = winfree_model_vectorized(self.phases, self.omega, self.K, self.dt)
        self.assertEqual(new_phases.shape, self.phases.shape)

if __name__ == '__main__':
    unittest.main()