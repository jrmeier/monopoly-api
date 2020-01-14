import unittest
import builtins
from unittest.mock import patch
import mono
import json
    
class TestGameActions(unittest.TestCase):
    @patch('builtins.input')
    def test_add_player(self, mock_input):
        mock_input.return_value = "Bob"

        mock_state = {
            "players": [],
        }
        res = mono.add_player(mock_state)

        self.assertEqual(res['players'][0]['name'],'Bob')
        self.assertEqual(res['players'][0]['pos'],0)
        self.assertEqual(type(res['players'][0]['token']), str)
        self.assertEqual(res['players'][0]['balance'], 1500),
    
    def test_start(self):
        mock_state = {
            "has_started": False,
            "current": {},
            "players": [
                {"name": "Bobby"},
                {"name": "Rossy"}
            ]
        }
        res = mono.start(mock_state)

        self.assertEqual(res['current']['player'], {'name': 'Bobby'})
        self.assertEqual(res['players'], [{'name': 'Rossy'}])
    
    def test_roll_first(self):
        mock_state = {
            "current": {
                "player": {
                    "name": "Bob",
                    "pos": 0
                },
                "roll": {
                    "has_rolled": False,
                    "die1": 0,
                    "die2": 0,
                    "is_double": False,
                    "double_count": 0
                }
            },
            "messages": [],
            "next_actions": []
        }
        res = mono.roll(mock_state)

        self.assertEqual(res['next_actions'],['new_position'])
        self.assertTrue(res['current']['roll']['has_rolled'])
        self.assertEqual(type(res['current']['roll']['die1']),int)
        self.assertEqual(type(res['current']['roll']['die2']),int)
        self.assertEqual(1, len(res['messages']))
        
        # is a double
        is_double = res['current']['roll']['die1'] == res['current']['roll']['die2']
        self.assertEqual(is_double,res['current']['roll']['is_double'])

    def test_new_position_no_owner(self):
        mock_state = {
            "current": {
                "player": {
                    "name": "Jim",
                    "pos": 0,
                    "token": "car"
                },
                "roll": {
                    "die1": 1,
                    "die2": 2,
                }
            },
            "messages": [],
            "board": [
                {},
                {},
                {},
                {
                    "price": 100,
                    "name": "Happy Trees"
                }
            ],
            "next_actions": []
        }

        res = mono.new_position(mock_state)

        self.assertEqual(res['current']['player']['pos'], 3)
        self.assertTrue(res['board'][3]['is_for_sale'])
        self.assertEqual(res['next_actions'], [])

    def test_new_position_with_owner(self):
        mock_state = {
            "current": {
                "player": {
                    "name": "Jim",
                    "pos": 0,
                    "token": "car"
                },
                "roll": {
                    "die1": 1,
                    "die2": 2,
                }
            },
            "messages": [],
            "board": [
                {},
                {},
                {},
                {
                    "price": 100,
                    "name": "Happy Trees",
                    "owner": "mock_token"
                }
            ],
            "next_actions": []
        }
        res = mono.new_position(mock_state)

        self.assertEqual(res['next_actions'], ['pay_rent'])
        self.assertEqual(res['board'][3]['owner'], "mock_token")
        self.assertEqual(res['messages'][1], "This property is owned by mock_token.")

    def test_new_position_with_own_property(self):
        mock_state = {
            "current": {
                "player": {
                    "name": "Jim",
                    "token": "car",
                    "pos": 0,
                    "balance": 900
                },
                "roll": {
                    "die1": 1,
                    "die2": 2,
                }
            },
            "messages": [],
            "board": [
                {},
                {},
                {},
                {
                    "price": 100,
                    "name": "Happy Trees",
                    "owner": "car"
                }
            ],
            "next_actions": []
        }
        res = mono.new_position(mock_state)

        self.assertEqual(len(res['messages']), 2)
        self.assertEqual(res['current']['player']['balance'], 900)
        self.assertEqual(res['next_actions'], [])
    
    def test_new_position_with_mortaged_property(self):
        mock_state = {
            "current": {
                "player": {
                    "name": "Jim",
                    "token": "car",
                    "pos": 0,
                    "balance": 900
                },
                "roll": {
                    "die1": 1,
                    "die2": 1,
                }
            },
            "messages": [],
            "board": [
                {},
                {},
                {
                    "price": 100,
                    "name": "Happy Trees",
                    "owner": "mock_token",
                    "mortgaged": True
                },
                {}
            ],
            "next_actions": []
        }
        res = mono.new_position(mock_state)

        self.assertEqual(len(res['messages']), 3)
        self.assertEqual(res['next_actions'], [])
    
    def test_determine_rent(self):
        mock_board = [
            {
                "special": "fake_special"
            },
            {
                "special": "fake_special",
            },
            {
                "name": "Happy Trees",
                "loc": 2,
                "price": 100,
                "mortgage": 30,
                "owner": "dog",
                "building": 50,
                "group": 1,
                "rent": [
                    2,
                    4,
                    10,
                    30,
                    90,
                    160,
                    250
                ]
            },
            {
                "name": "Happy Clouds",
                "loc": 3,
                "price": 100,
                "mortgage": 30,
                "owner": "cat",
                "building": 50,
                "group": 1,
                "rent": [
                    2,
                    4,
                    10,
                    30,
                    90,
                    160,
                    250
                ]
            },
        ]

        board = mono.determine_rent(mock_board)
        self.assertEqual(board[3]['current_rent'], 2)

    def test_determine_rent_1(self):
        mock_state = [
                {},
                {},
                {
                    "name": "Happy Trees",
                    "loc": 2,
                    "price": 100,
                    "mortgage": 30,
                    "building": 50,
                    "owner": "cat",
                    "group": 1,
                    "rent": [
                        2,
                        4,
                        10,
                        30,
                        90,
                        160,
                        250
                    ]
                },
                {
                    "name": "Happy Clouds",
                    "loc": 3,
                    "price": 100,
                    "mortgage": 30,
                    "building": 50,
                    "owner": "cat",
                    "group": 1,
                    "rent": [
                        2,
                        4,
                        10,
                        30,
                        90,
                        160,
                        250
                    ]
                },
            ]
        board = mono.determine_rent(mock_state)
        # print(json.dumps(board, indent=3))
        self.assertEqual(board[3]['current_rent'], 4)

    def test_determine_rent_2(self):
        mock_state = [
                {},
                {},
                {
                    "name": "Happy Trees",
                    "loc": 2,
                    "price": 100,
                    "owner": "car",
                    "mortgage": 30,
                    "building": 50,
                    "group": 1,
                    "rent": [
                        2,
                        4,
                        10,
                        30,
                        90,
                        160,
                        250
                    ]
                },
                  {
                    "name": "Happy Clouds",
                    "loc": 3,
                    "price": 100,
                    "owner": "mock_token",
                    "mortgage": 30,
                    "building": 50,
                    "group": 1,
                    "rent": [
                        2,
                        4,
                        10,
                        30,
                        90,
                        160,
                        250
                    ]
                },
            ]
        board = mono.determine_rent(mock_state)
        self.assertEqual(board[2]['current_rent'], 2)

    def test_determine_rent_monopoly(self):
            mock_board = [
                {},
                {},
                {
                    "name": "Happy Trees",
                    "loc": 2,
                    "price": 100,
                    "owner": "car",
                    "mortgage": 30,
                    "building": 50,
                    "group": 1,
                    "rent": [
                        2,
                        4,
                        10,
                        30,
                        90,
                        160,
                        250
                    ]
                },
                {
                    "name": "Happy Clouds",
                    "loc": 3,
                    "price": 100,
                    "owner": "car",
                    "mortgage": 30,
                    "building": 50,
                    "group": 1,
                    "rent": [
                        2,
                        4,
                        10,
                        30,
                        90,
                        160,
                        250
                    ]
                },
                {}
            ]
            board = mono.determine_rent(mock_board)
            self.assertEqual(board[3]['current_rent'], 4)
    
    def test_determine_rent_upgrades(self):
        mock_board = [
                {},
                {},
                {
                    "name": "Happy Trees",
                    "loc": 2,
                    "price": 100,
                    "owner": "mock_token",
                    "mortgage": 30,
                    "building": 50,
                    "upgrades": 1,
                    "group": 1,
                    "rent": [
                        2,
                        4,
                        10,
                        30,
                        90,
                        160,
                        250
                    ]
                },
                {
                    "name": "Happy Clouds",
                    "loc": 3,
                    "price": 100,
                    "owner": "mock_token",
                    "mortgage": 30,
                    "building": 50,
                    "upgrades": 1,
                    "group": 1,
                    "rent": [
                        2,
                        4,
                        10,
                        30,
                        90,
                        160,
                        250
                    ]
                },
                {}
            ]
        board = mono.determine_rent(mock_board)
        self.assertEqual(board[3]['current_rent'], 10)

    def test_determine_rent_upgrades_max(self):
        mock_board = [
                {},
                {},
                {
                    "name": "Happy Trees",
                    "loc": 2,
                    "price": 100,
                    "owner": "mock_token",
                    "mortgage": 30,
                    "building": 50,
                    "upgrades": 5,
                    "group": 1,
                    "rent": [
                        2,
                        4,
                        10,
                        30,
                        90,
                        160,
                        250
                    ]
                },
                {
                    "name": "Happy Clouds",
                    "loc": 3,
                    "price": 100,
                    "owner": "mock_token",
                    "mortgage": 30,
                    "building": 50,
                    "upgrades": 5,
                    "group": 1,
                    "rent": [
                        2,
                        4,
                        10,
                        30,
                        90,
                        160,
                        450
                    ]
                },
                {}
            ]
        board = mono.determine_rent(mock_board)
        self.assertEqual(board[2]['current_rent'], 250)

if __name__ == '__main__':
    unittest.main()