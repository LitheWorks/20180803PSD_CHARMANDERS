# Run with python3 -m unittest test_battleship.py
import unittest
from torpydo import ships
from torpydo.battleship import Player, BATTLEFIELD_COLUMNS, BATTLEFIELD_ROWS, ComputerPlayer
from torpydo.ships import Point, PlayField, Fleet
from torpydo.user_interface import AsciiUI


class TestShip(unittest.TestCase):
    def setUp(self):
        self.ship = ships.Ship("TestShip", 4, "White")
        play_field = PlayField(BATTLEFIELD_COLUMNS, BATTLEFIELD_ROWS)

        self.ui = AsciiUI(play_field)

        player_fleet = Fleet.standard_fleet()
        player_fleet.random_positioning(play_field)
        self.player = Player("Hawk-eyed Human", play_field, player_fleet)
        computer_fleet = Fleet.standard_fleet()
        computer_fleet.random_positioning(play_field)
        self.ship.all_positions.add(Point(1, 2))
        self.computer = ComputerPlayer(play_field, computer_fleet)

    def test_is_at(self):
        self.assertTrue(self.ship.receive_fire(Point(1, 2)))

    def test_alive_ships(self):
        self.assertTrue(self.ship.is_alive())

    def test_tanked_ships(self):
        self.ship.receive_fire(Point(1,2))
        self.assertFalse(self.ship.is_alive())

    # def test_draw_damage(self):
    #     hit, sunk_ship = self.player_2.receive_fire(Point(1,2))
    #     self.player_1.record_shot(player_shot, hit)
    #     self.u


if '__main__' == __name__:
    unittest.main()


# test comment hi
