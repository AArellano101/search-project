import math
import random

# used for testing
def grid():
    return [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def neighboursOf(node, grid, shuffle=True):
    neighbours = []
    
    # left
    if node[1] != 0:
        if grid[node[0]][node[1] - 1] != 1:
            neighbours.append((node[0], node[1] - 1))
    
    # top
    if node[0] != 0:
        if grid[node[0] - 1][node[1]] != 1:
            neighbours.append((node[0] - 1, node[1]))
                
    # right
    if node[1] != len(grid) - 1:
        if grid[node[0]][node[1] + 1] != 1:
            neighbours.append((node[0], node[1] + 1))
            
    # bottom
    if node[0] != len(grid) - 1:
        if grid[node[0] + 1][node[1]] != 1:
            neighbours.append((node[0] + 1, node[1]))
    
    if shuffle:
        random.shuffle(neighbours)

    return neighbours

def neighboursOfDiagonals(node, grid, shuffle=True):
    neighbours = []
    
    # left
    if node[1] != 0:
        if grid[node[0]][node[1] - 1] != 1:
            neighbours.append((node[0], node[1] - 1))
    
    # top
    if node[0] != 0:
        if grid[node[0] - 1][node[1]] != 1:
            neighbours.append((node[0] - 1, node[1]))
                
    # right
    if node[1] != len(grid) - 1:
        if grid[node[0]][node[1] + 1] != 1:
            neighbours.append((node[0], node[1] + 1))
            
    # bottom
    if node[0] != len(grid) - 1:
        if grid[node[0] + 1][node[1]] != 1:
            neighbours.append((node[0] + 1, node[1]))

    # bottom-left diagonal      
    if node[0] != len(grid) - 1 and node[1] != 0:
        if grid[node[0] + 1][node[1] - 1] != 1:
            if grid[node[0] + 1][node[1]] != 1 and grid[node[0]][node[1] - 1] != 1:
                neighbours.append((node[0] + 1, node[1] - 1))
    
    # top-left diagonal  
    if node[0] != 0 and node[1] != 0:
        if grid[node[0] - 1][node[1] - 1] != 1:
            if grid[node[0] - 1][node[1]] != 1 and grid[node[0]][node[1] - 1] != 1:
                neighbours.append((node[0] - 1, node[1] - 1))
    
    # top-right diagonal
    if node[0] != 0 and node[1] != len(grid) - 1:
        if grid[node[0] - 1][node[1] + 1] != 1:
            if grid[node[0] - 1][node[1]] != 1 and grid[node[0]][node[1] + 1] != 1:
                neighbours.append((node[0] - 1, node[1] + 1))
    
    # bottom-right diagonal      
    if node[0] != len(grid) - 1 and node[1] != len(grid) - 1:
        if grid[node[0] + 1][node[1] + 1] != 1:
            if grid[node[0] + 1][node[1]] != 1 and grid[node[0]][node[1] + 1] != 1:
                neighbours.append((node[0] + 1, node[1] + 1))

    if shuffle:
        random.shuffle(neighbours)

    return neighbours


def distance(node1, node2):
    x = node2[0] - node1[0]
    y = node2[1] - node1[1]
    return math.sqrt(x**2+y**2)

def pathCost(path, pType, grid, goal=()):
    if pType == "path_length":
        return len(path)
    if pType == "path_consistency":
        consistency = 0
        direction = None

        for nodeNum in range(len(path)):
            if (path[nodeNum] != path[-1]):
                deltaX = path[nodeNum+1][0]-path[nodeNum][0]
                deltaY = path[nodeNum+1][1]-path[nodeNum][1]
                curDirection = str(deltaX) + str(deltaY)
                if (direction != curDirection):
                    consistency += 1
                direction = curDirection
        return consistency
    if pType == "min_walls":
        wScore = 0

        for node in path:
            wScore += 8 - len(neighboursOfDiagonals(node, grid))

        return wScore
    
    if pType == "a_star":
        return len(path) + distance(path[0], goal)

    return 1


def breadth(grid, start, goal):
    queue = [start]
    visited = [start]

    while queue:
        x = queue.pop(0)

        for neighbour in neighboursOf(x, grid):
            if neighbour not in visited and neighbour not in queue:
                visited.append(neighbour)
                queue.append(neighbour)

                if neighbour == goal:
                    return visited, True

    return visited, False


def depth(grid, start, goal):
    queue = [start]
    visited = [start]

    while queue:
        x = queue.pop(-1)

        for neighbour in neighboursOf(x, grid, False):
            if neighbour not in visited and neighbour not in queue:
                visited.append(neighbour)
                queue.append(neighbour)

                if neighbour == goal:
                    return visited, True

    return visited, False


def uniformCostSearch(grid, start, goal, pType):
    queue = {start: True}
    visited = []
    paths = {start: [start]}
    first = True

    while True in list(queue.values()):
        minPathCost = math.inf

        if not first:
            for node in paths:
                if node != start and queue[node]:
                    if pathCost(paths[node], pType, grid) < minPathCost :
                        minNode = node
                        minPathCost = pathCost(paths[node], pType, grid)
        else:
            minNode = start

        x = minNode
        queue[minNode] = False
        if (minNode not in visited):
            visited.append(minNode)

        for neighbour in neighboursOfDiagonals(x, grid, False):
            newPath = paths[x] + [neighbour]

            if neighbour in visited or neighbour in queue:
                if pathCost(newPath, pType, grid) < pathCost(paths[neighbour], pType, grid):
                    paths[neighbour] = newPath
                    queue[neighbour] = True
            else:
                paths[neighbour] = newPath
                visited.append(neighbour)
                queue[neighbour] = True

        queue[start] = False
        first = False
    return visited, paths[goal], True


def greedy(grid, start, goal):
    queue = [start]
    visited = []
    distances = [distance(start, goal)]

    while queue:
        x = queue.pop(distances.index(min(distances)))
        visited.append(x)
        distances.remove(min(distances))

        for neighbour in neighboursOf(x, grid):
            if neighbour not in visited and neighbour not in queue:
                queue.append(neighbour)
                distances.append(distance(neighbour, goal))

                if neighbour == goal:
                    visited.append(neighbour)
                    return visited, True

    return visited, False

def aStarSearch(grid, start, goal):
    queue = {start: True}
    visited = []
    paths = {start: [start]}
    first = True

    while True in list(queue.values()):
        minPathHeuristic = math.inf

        if not first:
            for node in paths:
                if node != start and queue[node]:
                    if pathCost(paths[node], "a_star", grid, goal) < minPathHeuristic:
                        minNode = node
                        minPathHeuristic = pathCost(paths[node], "a_star", grid, goal)
        else:
            minNode = start

        x = minNode
        queue[minNode] = False
        if (minNode not in visited):
            visited.append(minNode)

        for neighbour in neighboursOfDiagonals(x, grid, False):
            newPath = paths[x] + [neighbour]

            if neighbour in visited or neighbour in queue:
                if pathCost(newPath, "a_star", grid, goal) < pathCost(paths[neighbour], "a_star", grid, goal):
                    paths[neighbour] = newPath
                    queue[neighbour] = True
            else:
                paths[neighbour] = newPath
                visited.append(neighbour)
                queue[neighbour] = True

        queue[start] = False
        first = False
    return visited, paths[goal], True

def randomSearch(grid, goal):
    visited = []
    x = 0
    y = 0

    while True:
        x = random.randint(0, len(grid[0]) - 1)
        y = random.randint(0, len(grid) - 1)

        if grid[y][x] != 1:
            visited.append((y,x))
            if (y,x) == goal:
                return visited, True
    
