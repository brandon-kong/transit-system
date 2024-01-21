from util.normalize import normalize_string as _
from util.safety_report import calculate_safety_penalties

import heapq
import math

def get_closest_path(graph, start: int, end: int):
    # O(n) search for closest path

    start = start
    end = end

    if start == end:
        return [start]
    
    if start not in graph:
        return None
    
    if end not in graph:
        return None
    
    queue = [(0, [start])]

    shortest_distances = {start: 0}
    total_distance = 0
    accumulated_distance = 0

    # safety penalties
    safety_penalties = calculate_safety_penalties('data/user_reports.json', graph.stations)
    station_penalty = 8
    transfer_penalty = 8
 
    while queue:
        (distance, path) = heapq.heappop(queue)
        vertex = path[-1]

        if distance <= shortest_distances.get(vertex, float('inf')):
            if vertex == end:
                print(f"Total distance: {accumulated_distance}km")
                return path
            
            for edge in graph[vertex]:
                accumulated_distance += edge['distance']
                total_distance = distance + edge['weight'] + station_penalty + safety_penalties.get(vertex, 0)
                adjacent = edge['id']

                # If the adjacent vertex is on a different line, we add a transfer penalty
            
                if (edge['isTransfer'] and adjacent != end):
                    total_distance += transfer_penalty

                # If the total distance to adjacent vertex is shorter than any previously recorded distance, we update it
                if total_distance < shortest_distances.get(adjacent, float('inf')):
                    heapq.heappush(queue, (total_distance, path + [adjacent]))
                    shortest_distances[adjacent] = total_distance

    return None
