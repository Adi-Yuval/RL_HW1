import os

from puzzle import *
from planning_utils import *
import heapq
import datetime


def a_star(puzzle):
    '''
    apply a_star to a given puzzle
    :param puzzle: the puzzle to solve
    :return: a dictionary mapping state (as strings) to the action that should be taken (also a string)
    '''

    # general remark - to obtain hashable keys, instead of using State objects as keys, use state.as_string() since
    # these are immutable.

    initial = puzzle.start_state
    goal = puzzle.goal_state

    # this is the heuristic function for of the start state
    initial_to_goal_heuristic = initial.get_manhattan_distance(goal)

    # the fringe is the queue to pop items from
    fringe = [(initial_to_goal_heuristic, initial)]
    # concluded contains states that were already resolved
    concluded = set()
    # a mapping from state (as a string) to the currently minimal distance (int).
    distances = {initial.to_string(): 0}
    # the return value of the algorithm, a mapping from a state (as a string) to the state leading to it (NOT as string)
    # that achieves the minimal distance to the starting state of puzzle.
    prev = {initial.to_string(): None}

    while len(fringe) > 0:
        # pop the first item from the fringe
        _, current = heapq.heappop(fringe)
        if current.to_string() in concluded:
            continue

        curr_dist = distances[current.to_string()]

        # if the current state is the goal state, we are done
        if current == goal:
            break

        # otherwise, add/update its neighbors in the fringe
        for action in current.get_actions():
            neighbor = current.apply_action(action)

            if neighbor.to_string() in concluded:
                continue

            heuristic = neighbor.get_manhattan_distance(goal)
            # # for section 3.2.3
            # heuristic = 0
            # for i in range(3):
            #     for j in range(3):
            #         if neighbor._array[i][j] != goal._array[i][j]:
            #             heuristic += 1

            heapq.heappush(fringe, (heuristic + curr_dist + 1, neighbor))

            if (neighbor.to_string() not in distances) or \
                    (distances[neighbor.to_string()] < curr_dist + 1):
                distances[neighbor.to_string()] = curr_dist + 1
                prev[neighbor.to_string()] = current

        concluded.add(current.to_string())

    # print("Number of nodes expanded: ", len(concluded))

    return prev


def solve(puzzle):
    # compute mapping to previous using dijkstra
    prev_mapping = a_star(puzzle)
    # extract the state-action sequence
    plan = traverse(puzzle.goal_state, prev_mapping)
    print_plan(plan)
    return plan


if __name__ == '__main__':
    # we create some start and goal states. the number of actions between them is 25 although a shorter plan of
    # length 19 exists (make sure your plan is of the same length)
    initial_state = State()
    actions = [
        'r', 'r', 'd', 'l', 'u', 'l', 'd', 'd', 'r', 'r', 'u', 'l', 'd', 'r', 'u', 'u', 'l', 'd', 'l', 'd', 'r', 'r',
        'u', 'l', 'u'
    ]
    goal_state = initial_state
    for a in actions:
        goal_state = goal_state.apply_action(a)
    puzzle = Puzzle(initial_state, goal_state)
    print('original number of actions:{}'.format(len(actions)))
    solution_start_time = datetime.datetime.now()
    solve(puzzle)
    print('time to solve {}'.format(datetime.datetime.now()-solution_start_time))

    # # for section 3.2.4:
    # initial_state = State('0 8 7' + os.linesep + '6 5 4' + os.linesep + '3 2 1')
    # goal_state = State('1 2 3' + os.linesep + '4 5 6' + os.linesep + '7 8 0')
    # puzzle = Puzzle(initial_state, goal_state)
    # solution_start_time = datetime.datetime.now()
    # solve(puzzle)
    # print('time to solve {}'.format(datetime.datetime.now()-solution_start_time))

