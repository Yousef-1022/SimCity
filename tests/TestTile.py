import unittest
from models.Tile import Tile

class TestTile(unittest.TestCase):

    def test_tile_creation(self):
        tile = Tile(5, 10, "water", True)
        self.assertEqual(5, tile.x)
        self.assertEqual(10, tile.y)
        self.assertEqual("water", tile.type)
        self.assertEqual(True, tile.occupied)

if __name__ == '__main__':
    unittest.main()

