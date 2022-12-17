import os
import re
from functools import cache

graph = dict()
rates = dict()

with open(os.getcwd() + "/day16/input.txt", encoding="utf-8") as f:
    for line in f:
        valves = re.findall("([A-Z]{2})", line)
        graph[valves[0]] = valves[1:]
        rates[valves[0]] = int(re.findall("\d+", line)[0])


# Calculate min distances between all nodes
distances: dict[str, dict[str], int] = {valve: {valve: 0} for valve in graph}
for start in graph:
    stack = [start]
    while len(stack) > 0:
        curr = stack.pop(0)
        for node in graph[curr]:
            if node not in distances[start]:
                stack.append(node)
                distances[start][node] = distances[start][curr] + 1


@cache
def dfs(curr: str, opened: tuple, time_remaining: int):
    # Substract opening time
    time_remaining -= 1
    if time_remaining == 0:
        return 0

    visited = tuple(list(opened) + [curr])
    options = [
        node
        for node in graph if node not in visited
        and rates[node] > 0 and time_remaining - distances[curr][node] > 1
    ]

    scores = [0]
    for node in options:
        dist = distances[curr][node]
        scores.append(dfs(node, visited, time_remaining - dist))

    return max(scores) + rates[curr] * time_remaining


most_pressure = dfs("AA", tuple(), 31)
print(f"Most pressure that can be released: {most_pressure}")