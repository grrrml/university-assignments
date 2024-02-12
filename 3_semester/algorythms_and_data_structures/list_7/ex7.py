from queue import Queue


def solve_using_bfs():
    """This code implements a breadth-first search (BFS) algorithm to solve
    a problem involving two water jugs, one with a capacity of 3 liters and 
    the other with a capacity of 4 liters. The goal is to measure out exactly
    2 liters of water using these two jugs.

    Returns:
        list: the path to solution
    """
    goal = 2
    queue = Queue()
    queue.put([(0, 0)])
    visited = list()
    while not queue.empty():
        path = queue.get()
        state = path[-1]
        if state not in visited:
            if state[0] == goal or state[1] == goal:
                return path
            visited.append(state)
            three = state[0]
            four = state[1]
            # Fill up 3l cannister
            if three < 3:
                new_path = path + [(3, four)]
                queue.put(new_path)
            # Fill up 4l cannister
            if four < 4:
                new_path = path + [(three, 4)]
                queue.put(new_path)
            # Drain 3l cannister
            if three > 0:
                new_path = path + [(0, four)]
                queue.put(new_path)
            # Drain 4l cannister
            if four > 0:
                new_path = path + [(three, 0)]
                queue.put(new_path)
            # 3l cannister -> 4l cannister
            if three > 0 and four < 4:
                new_path = path + [
                    (three - min(three, 4 - four), four + min(three, 4 - four))
                ]
                queue.put(new_path)
            # 4l cannister -> 3l cannister
            if four > 0 and three < 3:
                new_path = path + [
                    (three + min(four, 3 - three), four - min(four, 3 - three))
                ]
                queue.put(new_path)
    return None


if __name__ == "__main__":
    print(solve_using_bfs())
