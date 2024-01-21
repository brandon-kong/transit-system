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

    actual_distances = {start: 0}
    shortest_distances = {start: 0}
    total_distance = 0

    # safety penalties
    safety_penalties = calculate_safety_penalties('data/user_reports.json', graph.stations)
    station_penalty = 6
    transfer_penalty = 18
 
    while queue:
        (distance, path) = heapq.heappop(queue)
        vertex = path[-1]

        if distance <= shortest_distances.get(vertex, float('inf')):
            if vertex == end:
                print(f"Total distance: {actual_distances[end]}km")
                print(f"Total stops: {len(path)}")
                print(f"Total transfers: {len(path) - 1}")
                print(f"Total safety penalties: {sum(safety_penalties.get(station, 0) for station in path)}")
                print(f"Total weight: {distance}")
                
                return path
            
            for edge in graph[vertex]:
                
                actual_distance = actual_distances[vertex] + edge['distance']
                total_distance = distance + edge['weight'] + station_penalty + safety_penalties.get(vertex, 0)
                adjacent = edge['id']

                # If the adjacent vertex is on a different line, we add a transfer penalty
            
                if (edge['isTransfer'] and adjacent != end):
                    total_distance += transfer_penalty

                # If the total distance to adjacent vertex is shorter than any previously recorded distance, we update it
                if total_distance < shortest_distances.get(adjacent, float('inf')):
                    heapq.heappush(queue, (total_distance, path + [adjacent]))
                    shortest_distances[adjacent] = total_distance
                    actual_distances[adjacent] = actual_distance

    return None
