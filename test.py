import unittest
from unittest.mock import patch, mock_open
from train.graph import load_graph

class TestTrainGraph(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='{"1": {"name": "Station1", "connections": [{"id": 2, "cost": 1}]}, "2": {"name": "Station2", "connections": [{"id": 1, "cost": 1}]}}')
    def test_load_graph(self, mock_file):
        graph = load_graph('data/chicago_train.json')
        self.assertGreater(len(graph), 0)

    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    def test_load_graph_no_stations(self, mock_file):
        with self.assertRaisesRegex(ValueError, 'Invalid JSON data: no stations found'):
            load_graph('dummy_file.json')

if __name__ == '__main__':
    unittest.main()