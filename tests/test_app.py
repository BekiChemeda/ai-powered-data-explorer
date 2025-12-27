import unittest
import pandas as pd
import os
from app.services.dataset import Dataset
from app.services.profiler import Profiler
from app.services.visualizer import Visualizer

class TestDataServices(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Create a dummy CSV file for testing
        cls.test_file = "test_data.csv"
        df = pd.DataFrame({
            "A": [1, 2, 3, 4, 5],
            "B": ["x", "y", "x", "y", "z"],
            "C": [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        df.to_csv(cls.test_file, index=False)

    @classmethod
    def tearDownClass(cls):
        # Clean up
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)

    def test_dataset_load(self):
        dataset = Dataset(self.test_file)
        df = dataset.load()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 5)
        self.assertEqual(list(df.columns), ["A", "B", "C"])

    def test_profiler(self):
        dataset = Dataset(self.test_file)
        dataset.load()
        profiler = Profiler(dataset)
        profile = profiler.get_profile()
        
        self.assertIn("columns", profile)
        self.assertIn("missing_values", profile)
        self.assertEqual(profile["missing_values"]["A"], 0)
        self.assertEqual(profile["unique_counts"]["B"], 3)
        self.assertEqual(profile["column_types"]["A"], "numeric")

    def test_visualizer_histogram(self):
        dataset = Dataset(self.test_file)
        dataset.load()
        visualizer = Visualizer(dataset)
        
        # Test histogram generation
        base64_img = visualizer.generate_histogram("A")
        self.assertIsInstance(base64_img, str)
        self.assertTrue(len(base64_img) > 0)

    def test_visualizer_invalid_column(self):
        dataset = Dataset(self.test_file)
        dataset.load()
        visualizer = Visualizer(dataset)
        
        with self.assertRaises(ValueError):
            visualizer.generate_histogram("Z")

if __name__ == '__main__':
    unittest.main()
