import numpy as np
import math


def team_properties():
    properties = dict()
    player_names = ["Ace", "Ivan", "Bojan"]
    properties['team_name'] = "ФКВардар"
    properties['player_names'] = player_names
    properties['image_name'] = 'Blue.png'  # use image resolution 153x153
    return properties


def presmetajAgol(igrac, target):
    deltaX = abs(target['x'] - igrac['x'])
    deltaY = abs(target['y'] - igrac['y'])
    alpha = np.arctan(deltaY / deltaX)
    returnAlpha = 0
    if igrac['y'] < target['y'] and igrac['x'] < target['x']:
        returnAlpha = alpha
    elif igrac['y'] < target['y'] and igrac['x'] > target['x']:
        returnAlpha = np.pi - alpha
    elif igrac['y'] > target['y'] and igrac['x'] < target['x']:
        returnAlpha = -alpha
    elif igrac['y'] > target['y'] and igrac['x'] > target['x']:
        returnAlpha = np.pi + alpha
    elif igrac['x'] > target['x'] and igrac['y'] == target['y']:
        returnAlpha = -np.pi
    elif igrac['x'] < target['x'] and igrac['y'] == target['y']:
        returnAlpha = 0
    elif igrac['y'] > target['y'] and igrac['x'] == target['x']:
        returnAlpha = np.pi / 2
    else:
        returnAlpha = -np.pi / 2
    return returnAlpha


def presmetajDistanca(igrac, target):
    return np.sqrt(pow(igrac['x'] - target['x'], 2) + pow(igrac['y'] - target['y'], 2))


Alpha = 0


def move_player_on_circle(rb, rp, d, bx, by, px, py):
    player = {'x': px, 'y': py}
    ball = {'x': bx, 'y': by}
    R = rb + rp + d
    global Alpha
    Alpha += np.pi / 18
    if py >= 460:
        x = bx + R * math.cos((np.pi - presmetajAgol(player, ball)) + Alpha)
        y = by + R * math.sin((np.pi - presmetajAgol(player, ball)) + Alpha)
    else:
        x = bx + R * math.cos((np.pi + presmetajAgol(player, ball)) + Alpha)
        y = by + R * math.sin((np.pi + presmetajAgol(player, ball)) + Alpha)

    return x, y


def odluchiShut(player, ball, their_team):
    enemy = their_team[0]
    for i in range(3):
        if enemy['x'] < their_team[i]['x']:
            enemy = their_team[i]
    print(f"py: {player['y']}, by: {ball['y']}")
    if 343 <= ball['y'] <= 578 and int(player['y']) == int(ball['y']) and int(enemy['y']) != ball['y']:
        shot_request = True
        shot_power = np.infty
    else:
        shot_request = False
        shot_power = 0
    return shot_request, shot_power


def odlukaNapagjach(ball, napagjach, your_side):
    odluka = dict()
    agol = 0
    request = True
    distanca = napagjach['radius'] + ball['radius']

    if your_side == 'left':
        optimalPosition = {'x': ball['x'] - (ball['radius'] - 1), 'y': ball['y']}
        repositionX, repositionY = move_player_on_circle(ball['radius'], napagjach['radius'], 0, ball['x'],
                                                         ball['y'], napagjach['x'], napagjach['y'])
        reposition = {'x': repositionX, 'y': repositionY}
        request = False
        force = 0
    else:
        repositionX, repositionY = move_player_on_circle(ball['radius'], napagjach['radius'], 0, ball['x'],
                                                         ball['y'], napagjach['x'], napagjach['y'])
        optimalPosition = {'x': repositionX, 'y': repositionY}
        reposition = {'x': ball['x'] + (ball['radius'] + 1), 'y': ball['y']}
        request = False
        force = np.infty

    if 0 <= int(presmetajDistanca(napagjach, ball) - distanca) <= 20:
        if napagjach['x'] > ball['x']:
            agol = presmetajAgol(napagjach, reposition)
        elif napagjach['x'] <= ball['x']:
            agol = presmetajAgol(napagjach, optimalPosition)
    else:
        agol = presmetajAgol(napagjach, ball)

    odluka['force'] = np.infty
    odluka['alpha'] = agol
    odluka['shot_request'] = request
    odluka['shot_power'] = 100
    return odluka


def odlukaCentar(their_team, your_side, player, ball):
    odluka = dict()
    force = np.infty
    agol = 0

    if your_side == 'left':
        enemy_left = their_team[0]
        enemy_right = their_team[0]
        for i in range(3):
            if presmetajDistanca(ball, their_team[i]) < presmetajDistanca(ball, enemy_left):
                enemy_left = their_team[i]
            if their_team[i]['x'] > enemy_right['x']:
                enemy_right = their_team[i]
        if ball['x'] < 1016:
            agol = presmetajAgol(player, enemy_left)
        else:
            agol = presmetajAgol(player, enemy_right)
        force = np.inf
    else:
        enemy_left = their_team[0]
        enemy_right = their_team[0]
        for i in range(3):
            if their_team[i]['x'] < enemy_left['x']:
                enemy_left = their_team[i]
            if presmetajDistanca(ball, their_team[i]) < presmetajDistanca(enemy_right, ball):
                enemy_right = their_team[i]
        if ball['x'] > 350:
            agol = presmetajAgol(player, enemy_right)
        else:
            agol = presmetajAgol(player, enemy_left)
        force = np.inf

    odluka['force'] = force
    odluka['alpha'] = agol
    odluka['shot_request'] = True
    odluka['shot_power'] = 100
    return odluka


def odlukaGolman(your_side, player, ball):
    odluka = dict()
    force = np.infty
    agol = 0

    if your_side == 'left':
        nashGol = {'x': 83, 'y': 460}
        levX, desenX = 73, 94
    else:
        nashGol = {'x': 1286, 'y': 460}
        levX, desenX = 1276, 1297

    if levX <= player['x'] <= desenX:
        if 343 <= player['y'] < ball['y'] and player['y'] <= 578:
            agol = np.pi / 2
            force = np.infty
        elif ball['y'] < player['y'] <= 578 and player['y'] >= 343:
            agol = -np.pi / 2
            force = np.infty
        else:  # player['y'] < 343 or player['y'] > 578:
            agol = presmetajAgol(player, nashGol)
            force = np.infty
    else:
        agol = presmetajAgol(player, nashGol)
        force = np.infty

    odluka['force'] = force
    odluka['alpha'] = agol
    odluka['shot_request'] = True
    odluka['shot_power'] = np.infty
    return odluka


flag = False
mid = 0
nashStriker = 0
golman = 0


def decision(our_team, their_team, ball, your_side, half, time_left, our_score, their_score):
    manager_decision = [dict(), dict(), dict()]
    global flag
    global mid
    global nashStriker
    global golman
    if not flag:
        vMax = our_team[0]['v_max']
        vMin = our_team[0]['v_max']
        for i in range(3):
            if our_team[i]['v_max'] > vMax:
                nashStriker = i
                vMax = our_team[i]['v_max']
            if our_team[i]['v_max'] < vMin:
                golman = i
                vMin = our_team[i]['v_max']
        mid = abs(3 - (golman + nashStriker))

    napagjach = our_team[nashStriker]
    centar = our_team[mid]
    golee = our_team[golman]

    for i in range(3):
        player = our_team[i]
        if player == napagjach:
            manager_decision[nashStriker] = odlukaNapagjach(ball, napagjach, your_side)
        elif player == centar:
            manager_decision[mid] = odlukaCentar(their_team, your_side, player, ball)
        elif player == golee:
            manager_decision[golman] = odlukaGolman(your_side, player, ball)
    return manager_decision
