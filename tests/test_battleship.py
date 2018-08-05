# Run with python3 -m unittest test_battleship.py
import unittest
from torpydo import ships
from torpydo.battleship import Player, BATTLEFIELD_COLUMNS, BATTLEFIELD_ROWS, ComputerPlayer, Shot, start_game
from torpydo.ships import Point, PlayField, Fleet
from torpydo.user_interface import AsciiUI


class TestShip(unittest.TestCase):
    def setUp(self):
        self.ship = ships.Ship("TestShip", 4, "White")
        play_field = PlayField(BATTLEFIELD_COLUMNS, BATTLEFIELD_ROWS)

        self.ui = AsciiUI(play_field)
        self.playField = ships.PlayField(10, 10)

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

    def test_computer_draw_damage(self):
        hit, sunk_ship = self.player.receive_fire(Point(1,2))
        self.computer.record_shot(Point(1,2), hit)
        self.assertTrue(
            (self.ui.draw_damage(self.computer, Point(1,2), hit, sunk_ship) and  ("Guessin' Gustavo fired at B3 and missed!")) or
             (self.ui.draw_damage(self.computer, Point(1, 2), hit, sunk_ship) and (
                 "Guessin' Gustavo fired at B3 and Hit!")))

    def test_player_draw_damage(self):
        hit, sunk_ship = self.computer.receive_fire(Point(1,2))
        self.player.record_shot(Point(1,2), hit)
        self.assertTrue(
            (self.ui.draw_damage(self.player, Point(1,2), hit, sunk_ship) and  ("Hawk-eyed Human fired at B3 and missed!")) or
             (self.ui.draw_damage(self.player, Point(1, 2), hit, sunk_ship) and (
                 "Hawk-eyed Human fired at B3 and Hit!")))

    def test_player_get_shot(self):
        self.player.record_shot(Point(1,2), None)
        self.assertTrue(self.player.get_shot_at(Point(1,2)))

    def test_computer_get_shot(self):
        self.assertTrue(self.computer.get_computer_shot())

    def test_player_available_ships(self):
        self.assertTrue(self.player.available_ships())



    # def test_get_computer_shot(self):



if '__main__' == __name__:
    unittest.main()


# test comment hi
