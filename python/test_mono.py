import unittest
from mono import is_for_sale, buy

class TestGameActions(unittest.TestCase):
    
    def test_is_for_sale_true_1(self):
        state = {
            "current": {
                "property": {
                    "owner": None,
                    "mortgaged": False,
                    "special": False,
                    "price": 100
                }
            },
            "messages": []
        }

        res = is_for_sale(state)
        # print(res)
        msgs = ["This property is for sale for a price of $100."]
        self.assertEqual(msgs, res['messages'])
        self.assertTrue(res['current']['property']['is_for_sale'])

    def test_is_for_sale_false_2(self):
        state = {
            "current": {
                "property": {
                    "owner": "q23123123-1231",
                    "special": False,
                    "price": 400
                }
            },
            "messages": []
        }

        res = is_for_sale(state)
        msgs = ["This property is for sale for a price of $400."]
        self.assertEqual(msgs, res['messages'])
        self.assertFalse(res['current']['property']['is_for_sale'])
    
    def test_is_for_sale_false_2(self):
        state = {
            "current": {
                "property": {
                    "owner": False,
                    "special": "nope"
                }
            }
        }

        res = is_for_sale(state)

        self.assertFalse(res['current']['property']['is_for_sale'])
    
    # buy
    def get_current_property(self):
        state = {
            "current": {
                "player": {
                    "pos": 12
                }
            },
            "board": [
                
            ]
        }


if __name__ == '__main__':
    unittest.main()