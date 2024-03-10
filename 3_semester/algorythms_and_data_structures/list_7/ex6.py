from queue import Queue


def safety_check(missionaries: int, cannibals: int):
    """Checks if the missionaries are safe

    Args:
        missionaries (int): the number of missionaries on the left bank of the river
        cannibals (int): the number of cannibals on the left bank of the river

    Returns:
        bool: True if missionaries are safe, False otherwise
    """
    if missionaries > 3 or cannibals > 3:
        return False
    elif missionaries < 0 or cannibals < 0:
        return False
    elif (3 - missionaries) < (3 - cannibals) and (3 - missionaries) > 0:
        return False
    elif missionaries < cannibals and missionaries > 0:
        return False
    else:
        return True


def solve_using_bfs():
    """Solves the missionaries and cannibals problem using graph BFS

    Returns:
        list: list of states
    """
    end_state = (
        0,
        0,
        1,
    )  # end state, all cannibals and missionaries on the right bank of the river
    queue = Queue()
    queue.put(
        [(3, 3, 0)]
    )  # queue of paths with the beginning state of all cannibals and missionaries on the left bank of the river
    visited = []
    while queue:
        path = queue.get()
        state = path[-1]
        if state not in visited:
            if state == end_state:
                return path
            visited.append(state)
            for n in range(3):
                for m in range(3):
                    if n + m > 0 and n + m < 3:
                        missionaries = state[0]
                        cannibals = state[1]
                        current_boat = state[2]
                        if current_boat == 0:
                            missionaries -= n
                            cannibals -= m
                            if safety_check(missionaries, cannibals):
                                new_state = (missionaries, cannibals, 1)
                                new_path = list(path)
                                new_path.append(new_state)
                                queue.put(new_path)
                        else:
                            missionaries += n
                            cannibals += m
                            if safety_check(missionaries, cannibals):
                                new_state = (missionaries, cannibals, 0)
                                new_path = list(path)
                                new_path.append(new_state)
                                queue.put(new_path)
    return None


if __name__ == "__main__":
    print(solve_using_bfs())
