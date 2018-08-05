import string
from typing import Optional
import random
from torpydo import asciiart, TerminationRequested
from torpydo.ships import PlayField, Point, Ship, Orientation
from termcolor import colored
import time

class BaseUI(object):
    def __init__(self, play_field: PlayField):
        self.play_field = play_field

    def draw_board(self, turn_number: int, player, ship_list):
        pass

    def draw_damage(self, shooter, shot: Point, hit: bool, sunk_ship: Optional[Ship]):
        pass

    def draw_victory(self, turn_number: int, victor, loser):
        pass

    def get_player_shot(self, player) -> Point:
        pass

    def draw_game_started(self, player_1, player_2):
        pass

    def draw_game_stopped(self, player_1, player_2):
        pass

    @staticmethod
    def point_to_col_row(point: Point):
        """
        Converts a point such as `Point(1, 3)` to the corresponding col_row such as `'B4'`.
        """
        return "".join([string.ascii_uppercase[point.x], str(point.y + 1)])

    def col_row_to_point(self, input_str):
        """
        Converts a col_row such as `'D1'` to the corresponding point such as `Point(5, 0)`.
        """
        try:
            letter = input_str[0].upper()
            x = string.ascii_uppercase.index(letter)
            y = int(input_str[1:]) - 1
            p = Point(x, y)
            if self.play_field.is_valid_coordinate(p):
                return p
        except IndexError:
            pass
        except ValueError:
            pass
        return None


class AsciiUI(BaseUI):
    SPACER = '    '

    def __init__(self, play_field: PlayField):
        super().__init__(play_field)
        self.numbers_column = f"{{:{len(str(play_field.height))}d}} "
        self.numbers_spacer = " " * (1 + len(str(play_field.height)))

    def draw_game_started(self, player_1, player_2):
        print(asciiart.ASCII_BATTLESHIP)
        print()
        fight_title = f'The battle between {player_1.name} and {player_2.name}'
        print(asciiart.ASCII_DIVIDER)
        print(fight_title)
        print(asciiart.ASCII_DIVIDER)
        print()

    def draw_board(self, turn_number: int, player, ship_list):

        if player.is_computer():
            print()
            print(colored(f"{player.name}, turn #{turn_number}", 'yellow'))
            time.sleep(1)
            print(colored(f"{player.name} is thinking...", 'yellow'))
            time.sleep(1)
            print()
        else:
            print()
            print(colored(f"{player.name}, turn #{turn_number}", 'cyan'))
            print()
            cols = string.ascii_uppercase[:self.play_field.width]
            print(self.numbers_spacer, cols, self.SPACER, self.numbers_spacer, cols, sep='')
            for y in range(self.play_field.height):
                print(self.numbers_column.format(y + 1), end='')
                for x in range(self.play_field.width):
                    shot = player.get_shot_at(Point(x, y))
                    if shot:
                        print(colored('*', 'red') if shot.hit else colored('○', 'blue'), end='')
                    else:
                        print('·', end='')
                print(self.SPACER, self.numbers_column.format(y + 1), sep='', end='')
                for x in range(self.play_field.width):
                    pos = Point(x, y)
                    oppo = pos in player.opponent_shots
                    char = colored('○', 'blue') if oppo else colored('·', 'blue')
                    for ship in player.fleet:
                        if pos in ship.all_positions:
                            char = colored('*', 'red') if oppo else colored('═', 'grey') if ship.position[1] == Orientation.HORIZONTAL else colored('║', 'grey')
                    print(char, end='')
                print()
            print()
            print('****ENEMY SHIPS****')
            for final_ship in ship_list:
                print(final_ship)


    def draw_damage(self, shooter, shot: Point, hit: bool, sunk_ship: Optional[Ship]):
        if sunk_ship:
            print(f"{shooter.name} fired at {self.point_to_col_row(shot)} and SANK a {sunk_ship.name}!")
        else:
            print()
            if shooter.is_computer():
                print(colored(f"{shooter.name} fired at {self.point_to_col_row(shot)} and {'hit' if hit else 'missed'}!",'yellow'))
            else:
                print(colored(f"{shooter.name} fired at {self.point_to_col_row(shot)} and {'hit' if hit else 'missed'}!", 'cyan'))



    def draw_victory(self, turn_number: int, victor, loser):
        print()


        winMessages = [ "You Vanquished The Evil Captain's Fleet!","You Saved Your Crew!", "You Defeated The Evil Pirates!"  ]
        lostMessages = ["All Your Base Are Belong To Us", "All Of Your Ships Have Sank! Smell Ya Later!","Time To Find A New Profession, It Doesn't Seem Like This Suits You./"]
        if isinstance(victor,str) :
            print(colored(random.choice(winMessages) + r"""
                               
                               
                                         _ 
                                        | |
 _   _  ___  _   _  __      _____  _ __ | |
| | | |/ _ \| | | | \ \ /\ / / _ \| '_ \| |
| |_| | (_) | |_| |  \ V  V / (_) | | | |_|
 \__, |\___/ \__,_|   \_/\_/ \___/|_| |_(_)
  __/ |                                    
 |___/       
 
                                    .''.
       .''.      .        *''*    :_\/_:     .
      :_\/_:   _\(/_  .:.*_\/_*   : /\ :  .'.:.'.
  .''.: /\ :    /)\   ':'* /\ *  : '..'.  -=:o:=-
 :_\/_:'.:::.  | ' *''*    * '.\'/.'_\(/_'.':'.'
 : /\ : :::::  =  *_\/_*     -= o =- /)\    '  *
  '..'  ':::' === * /\ *     .'/.\'.  ' ._____
      *        |   *..*         :       |.   |' .---"|
        *      |     _           .--'|  ||   | _|    |
        *      |  .-'|       __  |   |  |    ||      |
     .-----.   |  |' |  ||  |  | |   |  |    ||      |
 ___'       ' /"\ |  '-."".    '-'   '-.'    '`      |____
jgs~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  &                    ~-~-~-~-~-~-~-~-~-~   /|
 ejm97    )      ~-~-~-~-~-~-~-~  /|~       /_|\
        _-H-__  -~-~-~-~-~-~     /_|\    -~======-~
~-\XXXXXXXXXX/~     ~-~-~-~     /__|_\ ~-~-~-~
~-~-~-~-~-~    ~-~~-~-~-~-~    ========  ~-~-~-~                              
            
            """       ,'green'))
        elif victor.is_computer():
            print(colored(random.choice(lostMessages) + r"""
                     _                      
                    | |                     
 _   _  ___  _   _  | | ___  ___  ___       
| | | |/ _ \| | | | | |/ _ \/ __|/ _ \      
| |_| | (_) | |_| | | | (_) \__ \  __/_ _ _ 
 \__, |\___/ \__,_| |_|\___/|___/\___(_|_|_)
  __/ |                                     
 |___/                                      
            
     _.-^^---....,,--
 _--                  --_
<                        >)
|                         |
 \._                   _./
    ```--. . , ; .--'''
          | |   |
       .-=||  | |=-.
       `-=#$%&%$#=-'
          | ;  :|
 _____.,-#%&$@%#&#~,._____ 
            
            
            """






                          , 'red'))
            # print(f"{victor.name}'s mighty fleet vanquished {loser.name} in turn {turn_number}!")
        else:
            print(colored(random.choice(winMessages) + r"""
                                                     _ 
                                                    | |
             _   _  ___  _   _  __      _____  _ __ | |
            | | | |/ _ \| | | | \ \ /\ / / _ \| '_ \| |
            | |_| | (_) | |_| |  \ V  V / (_) | | | |_|
             \__, |\___/ \__,_|   \_/\_/ \___/|_| |_(_)
              __/ |                                    
             |___/       

                                                .''.
                   .''.      .        *''*    :_\/_:     .
                  :_\/_:   _\(/_  .:.*_\/_*   : /\ :  .'.:.'.
              .''.: /\ :    /)\   ':'* /\ *  : '..'.  -=:o:=-
             :_\/_:'.:::.  | ' *''*    * '.\'/.'_\(/_'.':'.'
             : /\ : :::::  =  *_\/_*     -= o =- /)\    '  *
              '..'  ':::' === * /\ *     .'/.\'.  ' ._____
                  *        |   *..*         :       |.   |' .---"|
                    *      |     _           .--'|  ||   | _|    |
                    *      |  .-'|       __  |   |  |    ||      |
                 .-----.   |  |' |  ||  |  | |   |  |    ||      |
             ___'       ' /"\ |  '-."".    '-'   '-.'    '`      |____
            jgs~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
              &                    ~-~-~-~-~-~-~-~-~-~   /|
             ejm97    )      ~-~-~-~-~-~-~-~  /|~       /_|\
                    _-H-__  -~-~-~-~-~-~     /_|\    -~======-~
            ~-\XXXXXXXXXX/~     ~-~-~-~     /__|_\ ~-~-~-~
            ~-~-~-~-~-~    ~-~~-~-~-~-~    ========  ~-~-~-~                              

                        """, 'green'))

    def draw_game_stopped(self, player_1, player_2):
        print("The game ended before either fleet was completely defeated.")
        print(f"{player_1.name} hit {player_2.name}'s ships {player_2.fleet.total_damage()} time(s).")
        print(f"{player_2.name} hit {player_1.name}'s ships {player_1.fleet.total_damage()} time(s).")

    def get_player_shot(self, player) -> Point:
        # See if we fire an automated shot
        if player.is_computer():
            return player.get_computer_shot()

        # Otherwise get a shot from user input
        print()
        print(colored("Player, it's your turn.",'cyan'))
        try:
            player_shot = None
            while player_shot is None:
                input_value = input(colored('Please enter a coordinate between {} and {} to shoot the missile, or CTRL-D to to quit: ',"blue").format(
                    AsciiUI.point_to_col_row(self.play_field.top_left),
                    AsciiUI.point_to_col_row(self.play_field.bottom_right)))

                if input_value == '1337': self.draw_victory(0, 'player' ,'machine')

                player_shot = self.col_row_to_point(input_value)
                # print(input_value + 'okk')
            print()
            return player_shot
        except EOFError:
            raise TerminationRequested()
