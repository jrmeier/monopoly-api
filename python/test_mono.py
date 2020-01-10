import unittest
from mono import new_position, buy

class TestGameActions(unittest.TestCase):
    def test_new_position_1(self):
        mock_state = {
            "current": {
                "player": {
                    "pos": 0,
                    "name": "Bob"
                },
                "roll": {
                    "die1": 1,
                    "die2": 2
                }
            },
            "board": [
                {
                    "name": "OG prop",
                    "price": 60
                },
                {
                    "name": "First prop",
                    "price": 60
                },
                {
                    "name": "Second prop",
                    "price": 120
                },
                {
                    "name": "Third Prop",
                    "price": 100
                }
            ],
            "messages": []
        }

        res = new_position(mock_state)
        
        self.assertEqual(3, res['current']['player']['pos'])
        self.assertEqual("Bob is now on Third Prop.", res['messages'][0])
        self.assertEqual("This property is for sale for a price of $100.",res['messages'][1])
        self.assertTrue(res['board'][3]['is_for_sale'])

    def test_new_position_2(self):
        mock_state = {
            "current": {
                "player": {
                    "pos": 0,
                    "name": "Bob"
                },
                "roll": {
                    "die1": 1,
                    "die2": 1
                }
            },
            "board": [
                {
                    "name": "OG Prop",
                    "special": "og_property"
                },
                {
                    "name": "First Prop",
                    "price": 60
                },
                {
                    "name": "Specialty Prop",
                    "special": True,
                },
                {
                    "name": "Third Prop",
                    "price": 100
                }
            ],
            "messages": []
        }

        res = new_position(mock_state)
        
        self.assertEqual(2, res['current']['player']['pos'])
        self.assertEqual("Bob is now on Specialty Prop.", res['messages'][0])
        self.assertEqual(1, len(res['messages']))
        self.assertFalse(res['board'][2]['is_for_sale'])
    

    def test_buy_1(self):
        mock_state = {
            "current": {
                "player": {
                    "pos": 1,
                    "balance": 1000
                }
            },
            "board": [
                {
                    "name": "OG Prop",
                    "special": "og_property"
                },
                {
                    "name": "Buy Me Yo",
                    "price": 100,
                }
            ],
            "messages": []
        }

        res = buy(mock_state)



if __name__ == '__main__':
    unittest.main()