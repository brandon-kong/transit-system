from util.normalize import normalize_string as _

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
 
    while queue:
        (distance, path) = heapq.heappop(queue)
        vertex = path[-1]

        if distance <= shortest_distances.get(vertex, float('inf')):
            if vertex == end:
                print(f"Total distance: {shortest_distances[end]}km")
                return path
            
            for edge in graph[vertex]:
                total_distance = distance + edge['weight']
                adjacent = edge['id']

                # If the total distance to adjacent vertex is shorter than any previously recorded distance, we update it
                if total_distance < shortest_distances.get(adjacent, float('inf')):
                    heapq.heappush(queue, (total_distance, path + [adjacent]))
                    shortest_distances[adjacent] = total_distance

    return None


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance