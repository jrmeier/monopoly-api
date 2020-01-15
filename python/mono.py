import random
import json
import datetime
from copy import deepcopy
import os
from helpers import get_dot_notation as d


def add_player(state):
    new_state = deepcopy(state)
    name = input("Name: ")
    tokens = [
        "dog",
        "car",
        "wheelbarrow",
        "battleship",
        "tophat",
        "shoe"
    ]
    # token = input("Token: ")
    token = None
    if not token:
        token = random.choice(tokens)

    player = {
        "name": name,
        "token": token,
        "balance": 1500,
        "pos": 0,
    }
    new_state['players'].append(player)
    return new_state

def start(state):
    new_state = deepcopy(state)
    new_state['has_started'] = True
    new_state['current']['player'] = new_state['players'].pop(0)

    return new_state

def roll(state):
    new_state = deepcopy(state)
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    is_double = True if die1 == die2 else False

    new_state['current']['roll'] = {
        'has_rolled': True,
        "die1": die1,
        "die2": die2,
        "is_double": is_double,
        "double_count": new_state['current']['roll']['double_count']+1 if is_double else 0
    }

    new_state['messages'].append(f"{new_state['current']['player']['name']} rolled a {die1+die2}.")

    new_state['next_actions'].append("new_position")
    
    return new_state

def new_position(state):
    """
    Get information about this square
    """
    new_state = deepcopy(state)
    pos = new_state['current']['player']['pos']
    roll = new_state['current']['roll']

    new_position = roll['die1']+roll['die2'] + pos

    if new_position > 40:
        new_position = new_position - 40
        
    prop = new_state['board'][new_position]

    new_state['messages'].append(f"{new_state['current']['player']['name']} is now on {prop['name']}.")

    if not prop.get('owner'):
        if not prop.get('special'):
            prop['is_for_sale'] = True
            new_state['messages'].append(f"This property is for sale for a price of ${prop['price']}.")
    else:
        owner = prop.get('owner')
    
        if owner == new_state['current']['player']['token']:
            new_state['messages'].append("They own this property.")
        else:
            new_state['messages'].append(f"This property is owned by {prop['owner']}.")
            if prop.get('mortgaged'):
                new_state['messages'].append(f"It's mortgaged, so there is no rent charge.")
            else:
                new_state['next_actions'].append('pay_rent')

    new_state['current']['player']['pos'] = new_position

    return new_state

def determine_rent(state):
    """
    sets the current_rent on each property on the board
    """
    new_board = deepcopy(state['board'])

    total_in_group = 0
    total_owned = 0

    for prop in new_board:
        total_in_group = len([i for i, x in enumerate(new_board) if (x.get('group') and x.get('group') == prop.get("group"))])
        total_owned = len([i for i, x in enumerate(new_board) if (x.get('owner') and x.get('owner') == prop.get("owner"))])
        has_monopoly = True if (total_owned and total_owned == total_in_group) else False
        upgrades = 0 if not prop.get('upgrades') else prop.get('upgrades')

        rent_list = prop.get('rent', [])

        if not rent_list:
            prop['current_rent'] = 0

        if not has_monopoly and rent_list: # do something special for RR and utils
            prop['current_rent'] = rent_list[0]
    
        if has_monopoly and rent_list:
            if not upgrades:
                prop['current_rent'] = rent_list[1]
            if upgrades:
                prop['current_rent'] = rent_list[upgrades+1]
    
    state['board'] = new_board
    return state


def buy(state):
    new_state = deepcopy(state)
    
    board = new_state['board']
    player = new_state['current']['player']
    prop = board[player['pos']]

        
    # must have enough money
    if player['balance'] >= prop['price']:
        prop['owner'] = player['token']
        player['balance'] = player['balance'] - prop['price']
        new_state['messages'].append(f"You have bought this property for ${prop['price']}")
        new_state['next_actions'].append("determine_rent")
    else:
        new_state['messages'].append("You don't have enough money!")
    
    new_state['current']['player'] = player
    new_state['board'][player['pos']] = prop

    return new_state

def end_turn(state):
    # update the player
    new_state = deepcopy(state)
    new_state['messages'].append(f"{new_state['current']['player']['name']}'s turn has ended.")
    new_state['players'].append(new_state['current']['player'])
    new_state['current']['roll']['has_rolled'] = False
    new_state['current']['player'] = new_state['players'].pop(0)
    
    new_state['messages'].append(f"It is now {new_state['current']['player']['name']}'s turn.")
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
        board = new_state['board']
        player = new_state['current']['player']
        prop = board[player["pos"]]
        
        if state['current']['roll']['double_count'] < 3 and not state['current']['roll']['has_rolled']:
            actions.append("roll")

        # print("prop: ",prop)
        # print("player: ", player)
        # if state['current']['property']['is_for_sale'] and not d(state, 'current.property.owner'):
        # if state['board'][['current']['player']['pos']]:
        if not prop.get('owner') and not prop.get('special'):
            actions.append("buy")
        # if board['']
        # if prop['']
        # print(state['board'])
        # if state['board
        # actions.append("buy")

    #should always be at the end
    if d(state, 'current.roll.has_rolled'):
        actions.append('end_turn')


    new_state['actions'] = actions

    return new_state


def play():
    # check the game state for available actions
    date_string =datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    game_filename = f"../games/{date_string}.json"
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

        for na in state['next_actions']:
            state = eval(na)(state)
            state = update_actions(state)
            # for m in state['messages']:
            #     print(m)

        
        for m in state['messages']:
            print(m)

        state['next_actions'] = []
        state['messages'] = []

        with open(game_filename,'w') as game_file:
            game_file.write(json.dumps(state, indent=3))



if __name__ == "__main__":
    play()