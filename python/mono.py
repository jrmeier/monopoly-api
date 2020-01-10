import random
import json
import uuid

def d(obj, dot_string):
    if not dot_string:
        return
    dot_split = dot_string.split(".",1)
    if len(dot_split) <= 1:
        try:
            return obj[dot_split.pop()]
        except KeyError:
            return None

    if obj.get(dot_split[0]):
        new_obj = obj[dot_split[0]]
        new_dot_string = dot_split[1:].pop()
        return d(new_obj, new_dot_string)

    return None

def is_for_sale(state):
    prop = state['current']['property']
    
    # must not be marked by an owner
    # and must not be mortgaged
    # and include houses/

    if not prop.get('owner') and not prop.get('special'):
        prop['is_for_sale'] = True
        state['messages'].append(f"This property is for sale for a price of ${prop['price']}.")
    else:
        prop['is_for_sale'] = False
    

    state['current']['property']= prop
    
    return state

def buy(state):
    player = state['current']['player']
    prop = state['current']['property']

    # must have enough money
    if player['balance'] >= prop['price']:
        prop['owner'] = player['id']
        player['balance'] = player['balance'] - prop['price']
        state['messages'].append(f"You have bought this property for ${prop['price']}")
    
    else:
        state['messages'].append("You don't have enough money!")
    
    state['current']['player'] = player
    state['current']['property'] = prop

    return state

def get_current_property(state):
    # prop = state['current']['property']
    prop = state['board'][player['pos']]

    if not prop.get('owner') and not prop.get('special'):
        prop['is_for_sale'] = True
        state['messages'].append(f"This property is for sale for a price of ${prop['price']}.")
    else:
        prop['is_for_sale'] = False
    

    state['current']['property']= prop
    
    player = state['current']['player']

    state['current']['property'] = state['board'][player['pos']]
    

    return state

def pay_rent(state):
    # determine how much
    # determine if they can pay

    return
    

def new_position(state):
    pos = state['current']['player']['pos']
    roll = state['current']['roll']

    new_position = roll['die1']+roll['die2'] + pos

    state['current']['player']['pos'] = new_position

    state = get_current_property(state)
    state['messages'].append(f"They are now on {state['current']['property']['name']}")
    
    if d(state, 'current.property.is_for_sale'):
        state['messages'].append("It is for sale.")
    

    
    # should pay rent    
    return state

def roll(state):
    die1 = random.randint(0, 6)
    die2 = random.randint(0, 6)
    is_double = True if die1 == die2 else False

    state['current']['roll'] = {
        'has_rolled': True,
        "die1": die1,
        "die2": die2,
        "is_double": is_double,
        "double_count": state['current']['roll']['double_count']+1 if is_double else 0
    }

    state['messages'].append(f"{state['current']['player']['name']} rolled a {die1+die2}.")
    return new_position(state)


def add_player(state):
    name = input("Name: ")
    
    player = {
        "name": name,
        "id": str(uuid.uuid4()),
        "balance": 1500,
        "pos": 0,
        "properties": []
    }
    state['players'].append(player)
    return state

def start(state):
    state['has_started'] = True
    state['current']['player'] = state['players'].pop(0)

    return state

def end_turn(state):
    # update the player
    state['messages'].append(f"{state['current']['player']['name']}'s turn as ended.")
    state['players'].append(state['current']['player'])
    state['current']['roll']['has_rolled'] = False
    state['current']['player'] = state['players'].pop(0)
    
    state['messages'].append(f" It is now {state['current']['player']['name']}'s turn.")
    return state

def game(state):
    state['messages'].append(json.dumps(state['current'], indent=1))
    return state

def update_actions(state):
    """ updates the available actions """
    
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

    state['actions'] = actions
    
    return state


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