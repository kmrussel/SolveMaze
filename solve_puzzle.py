
from copy import deepcopy


def solve_puzzle(Board, Source, Destination):
    """Traverses a 2zD puzzle of size MxN. Each cell in the puzzle can
    either be empty or has a barrier. Given the source and destination,
    the function determines the path that covers the minimum number of cells"""
    graph = {}
    for i in range(0, len(Board)):
        for j in range(0, len(Board[i])):
            # if the cell is not a barrier
            if Board[i][j] == '-':
                graph[(i, j)] = {}

                # up
                if i - 1 >= 0 and Board[i - 1][j] == '-':
                    graph[(i, j)][(i-1, j)] = 'U'
                # down
                if i + 1 < len(Board) and Board[i + 1][j] == '-':
                    graph[(i, j)][(i + 1, j)] = 'D'
                # left
                if j - 1 >= 0 and Board[i][j - 1] == '-':
                    graph[(i, j)][(i, j - 1)] = 'L'
                # right
                if j + 1 < len(Board[i]) and Board[i][j + 1] == '-':
                    graph[(i, j)][(i, j + 1)] = 'R'

    path = [[[Source], []]]
    index = 0

    visited = []

    if Source == Destination:
        return path[0]

    visited.append(Source)
    while index < len(path):
        current = path[index]
        last = current[0][-1]
        next_set = graph[last]

        if Destination in next_set:
            current[0].append(Destination)
            current[1].append(graph[last][Destination])
            current[1] = ''.join(current[1])
            return current[0], current[1]

        for next_node in next_set:
            if next_node not in visited:
                new_path = deepcopy(current)
                new_path[0].append(next_node)
                new_path[1].append(next_set[next_node])
                path.append(new_path)
                visited.append(next_node)
        index += 1
    return None