import unittest
from torpydo import ships
from torpydo.battleship import Player, BATTLEFIELD_COLUMNS, BATTLEFIELD_ROWS, ComputerPlayer, Shot
from torpydo.ships import Point, PlayField, Fleet
from torpydo.user_interface import AsciiUI

class TestPlayField(unittest.TestCase):
    def setUp(self):
        self.playField = ships.PlayField(10, 10)

    def test_is_valid_coordinate(self):
        self.assertTrue(self.playField.is_valid_coordinate(Point(1, 2)))

    def test_is_valid_coordinate2(self):
        self.assertFalse(self.playField.is_valid_coordinate(Point(11, 2)))

    def test_get_random_position(self):
        self.assertTrue(self.playField.get_random_position().x < 10 and self.playField.get_random_position().y < 10)

    def test_get_random_position2(self):
        self.assertFalse(self.playField.get_random_position().x > 10)