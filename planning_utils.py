def traverse(goal_state, prev):
    '''
    extract a plan using the result of dijkstra's algorithm
    :param goal_state: the end state
    :param prev: result of dijkstra's algorithm
    :return: a list of (state, actions) such that the first element is (start_state, a_0), and the last is
    (goal_state, None)
    '''
    result = [(goal_state, None)]

    curr_state = goal_state

    while prev[curr_state.to_string()] is not None:
        prev_state = prev[curr_state.to_string()]

        for action in prev_state.get_actions():
            if prev_state.apply_action(action) == curr_state:
                result = [(prev_state, action)] + result
                break
        curr_state = prev[curr_state.to_string()]

    return result


def print_plan(plan):
    print('plan length {}'.format(len(plan)-1))
    for current_state, action in plan:
        print(current_state.to_string())
        if action is not None:
            print('apply action {}'.format(action))
