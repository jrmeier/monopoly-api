import random
import json
import uuid
from copy import deepcopy
from helpers import get_dot_notation as d


# def is_for_sale(state):
#     new_state = deepcopy(state)
#     prop = new_state['current']['property']
    
#     # must not be marked by an owner
#     # and must not be mortgaged
#     # and include houses/

#     if not prop.get('owner') and not prop.get('special'):
#         prop['is_for_sale'] = True
#         new_state['messages'].append(f"This property is for sale for a price of ${prop['price']}.")
#     else:
#         prop['is_for_sale'] = False
    

#     new_state['current']['property'] = prop
    
    # return new_state

def buy(state):
    new_state = deepcopy(state)
    
    board = new_state['board']
    player = new_state['current']['player']
    prop = board[player['pos']]

    # must have enough money
    if player['balance'] >= prop['price']:
        prop['owner'] = player['id']
        player['balance'] = player['balance'] - prop['price']
        new_state['messages'].append(f"You have bought this property for ${prop['price']}")
        # update the property and rent prices
        determine_rent(state)
    
    else:
        new_state['messages'].append("You don't have enough money!")
    
    new_state['current']['player'] = player
    new_state['board'][player['pos']] = prop

    return new_state


def determine_rent(state):
    
    total_in_group = 0
    total_owned = 0

    for p in board:
        if p['group'] == prop['group']:
            total_in_group += 1
             if p.get('owner') == prop['owner']:
                 total_owned += 1
    
    has_monopoly = True if total_owned == total_owned else False

    if has_monopoly and
    


    
    total_owned = 0
    for g in group:
        if g.get('owner', None) == prop['ower']



def new_position(state):
    """
    Get board position and information about that position
    Also pay rent
    """
    new_state = deepcopy(state)
    pos = new_state['current']['player']['pos']
    roll = new_state['current']['roll']

    new_position = roll['die1']+roll['die2'] + pos
    prop = new_state['board'][new_position]


    new_state['messages'].append(f"{new_state['current']['player']['name']} is now on {prop['name']}.")

    if not prop.get('owner'):
        if not prop.get('special'):
            prop['is_for_sale'] = True
            new_state['messages'].append(f"This property is for sale for a price of ${prop['price']}.")
    else:
        # pay the rent, it should be figured at the purchase!





    new_state['current']['player']['pos'] = new_position
    # new_state['board'][pos] = prop
    return new_state

def roll(state):
    new_state = deepcopy(state)
    die1 = random.randint(0, 6)
    die2 = random.randint(0, 6)
    is_double = True if die1 == die2 else False

    new_state['current']['roll'] = {
        'has_rolled': True,
        "die1": die1,
        "die2": die2,
        "is_double": is_double,
        "double_count": new_state['current']['roll']['double_count']+1 if is_double else 0
    }

    new_state['messages'].append(f"{new_state['current']['player']['name']} rolled a {die1+die2}.")
    
    return new_position(new_state)


def add_player(state):
    new_state = deepcopy(state)
    name = input("Name: ")
    
    player = {
        "name": name,
        "id": str(uuid.uuid4()),
        "balance": 1500,
        "pos": 0,
        "properties": []
    }
    new_state['players'].append(player)
    return new_state

def start(state):
    new_state = deepcopy(state)
    new_state['has_started'] = True
    new_state['current']['player'] = new_state['players'].pop(0)

    return new_state

def end_turn(state):
    # update the player
    new_state = deepcopy(state)
    new_state['messages'].append(f"{new_state['current']['player']['name']}'s turn as ended.")
    new_state['players'].append(new_state['current']['player'])
    new_state['current']['roll']['has_rolled'] = False
    new_state['current']['player'] = new_state['players'].pop(0)
    
    new_state['messages'].append(f" It is now {new_state['current']['player']['name']}'s turn.")
    return new_state

def game(state):
    new_state = deepcopy(state)
    new_state['messages'].append(json.dumps(new_state['current'], indent=1))
    return new_state

def update_actions(state):
    """ updates the available actions """
    new_state = deepcopy(state)
    actions = ["quit","game"]
    # starting and adding players



    if len(state["players"]) >= 1 and not state["has_started"]:
        actions.append("start")
    
    if not state['has_started']:
        actions.append('add_player')

    # first roll of the game
    if state['has_started']:
        if state['current']['roll']['double_count'] < 3 and not state['current']['roll']['has_rolled']:
            actions.append("roll")

        if state['current']['property']['is_for_sale'] and not d(state, 'current.property.owner'):
            actions.append("buy")

    #should always be at the end
    if d(state, 'current.roll.has_rolled'):
        actions.append('end_turn')


    new_state['actions'] = actions

    return new_state


def play():
    # check the game state for available actions

    with open("../assets/state.json","r") as state_file:
        state = json.load(state_file)
    
    with open("../assets/board.json",'r') as board_file:
        state['board'] = json.load(board_file)

    player_action = ""
    while player_action != "quit":
        print("\nActions:")
        for action in state['actions']:
            print(f"\t{action}")
        
        player_action = input("")

        if player_action not in state['actions']:
            state['messages'].append('Action not available.')
        
        else:
            state = eval(player_action)(state)
            state = update_actions(state)

        for m in state['messages']:
            print(m)     
        
        state['messages'] = []

if __name__ == "__main__":
    play()