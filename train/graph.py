# Create the graph representation of the Chicago train system

from util.normalize import normalize_string as _
from .pathfinding import ( calculate_distance)
import json

weight_factor = 2.34
cost_factor = 1.5
transfer_factor = 5

class TrainGraph:
    stations = []

    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_station(self, station):
        self.stations.append(station)

    def add_edge(self, vertex, vertex2):
        if vertex not in self.graph:
            self.graph[vertex] = []

        distance = self.get_distance(vertex, vertex2) or 1
        sameLine = False
        cost = 0

        station1 = self.get_station_by_id(vertex)
        station2 = self.get_station_by_id(vertex2)

        if station1 is None:
            return
        
        if station2 is None:
            return
        
        if station1['line'] == station2['line']:
            sameLine = True

        for edge in station1['connections']:
            if edge['station_id'] == vertex2:
                cost = edge['cost']
                break

        weight = self.calculate_weight(distance, cost, sameLine)
        
        self.graph[vertex].append({'id': vertex2, 'weight': weight, 'isTransfer': not sameLine})

    def get_graph(self):
        return self.graph

    def get_vertex(self, vertex):
        if vertex in self.graph:
            return self.graph[vertex]
        else:
            return None

    def get_vertices(self):
        return self.graph.keys()

    def get_edges(self):
        edges = []
        for vertex in self.graph:
            for edge in self.graph[vertex]:
                edges.append((vertex, edge))
        return edges

    def get_num_vertices(self):
        return len(self.graph)

    def get_num_edges(self):
        return len(self.get_edges())
    
    def get_station(self, station_name, line=None):
        # O(n) search for station

        station_name = _(station_name)
        line = _(line) if line is not None else None

        for station in self.stations:
            if line is not None:
                if _(station['name']) == station_name and _(station['line']) == line:
                    return station
            else:
                if _(station['name']) == station_name:
                    return station
        return None
    
    def get_station_by_id(self, station_id: int):
        for station in self.stations:
            if station['id'] == station_id:
                return station
        return None
    
    def get_distance(self, station1, station2):
        station1 = self.get_station_by_id(station1)
        station2 = self.get_station_by_id(station2)

        if station1 is None or station2 is None:
            return None

        station1_coordinates = station1['geometry']['coordinates']
        station2_coordinates = station2['geometry']['coordinates']

        if not all(isinstance(coord, (int, float)) for coord in station1_coordinates):
            print(f"Invalid coordinates for station {station1['name']}: {station1_coordinates}")
            return None

        if not all(isinstance(coord, (int, float)) for coord in station2_coordinates):
            print(f"Invalid coordinates for station {station2['name']}: {station2_coordinates}")
            return None
    
        lon1, lat1 = station1_coordinates[0], station1_coordinates[1]
        lon2, lat2 = station2_coordinates[0], station2_coordinates[1]

        dist = calculate_distance(lat1, lon1, lat2, lon2)

        return dist
    
    def calculate_weight(self, distance, cost, sameLine):
        transfer_penalty = 0 if sameLine else 100
        weight = distance * weight_factor + cost * cost_factor + transfer_penalty * transfer_factor
        return weight
    
    def station_id_list_to_english(self, station_id_list):
        station_list = []
        prev_station = None

        for station_id in station_id_list:
            station = self.get_station_by_id(station_id)

            if station is None:
                continue

            if (prev_station is not None):
                if (prev_station['line'] != station['line']):
                    station_list.append(f"Transfer to {station['line']} line")
            
            station_list.append(station['name'])
            prev_station = station

        return station_list


    def __str__(self):
        return str(self.graph)

    def __iter__(self):
        return iter(self.graph)

    def __contains__(self, vertex):
        return vertex in self.graph
    
    def __getitem__(self, vertex):
        return self.get_vertex(vertex)

    def __len__(self):
        return self.get_num_vertices()

    def __eq__(self, other):
        return self.graph == other.graph

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):
        return str(self.graph)
    
    def __hash__(self):
        return hash(str(self.graph))
    
    def __copy__(self):
        return self.graph.copy()
    

def load_graph(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

        if (data is None):
            raise ValueError('Invalid JSON data: no stations found')
    
    if ('stations' not in data):
        raise ValueError('Invalid JSON data: no stations found')
    
    graph = TrainGraph()

    # initialize vertices first
    for station in data['stations']:
        if (station.get('status') == 'closed'):
            continue
        graph.add_vertex(station['id'])
        graph.add_station(station)

    # then initialize edges
    for station in data['stations']:
        for edge in station['connections']:
            if edge.get('status') == 'closed':
                continue
            else:
                graph.add_edge(station['id'], edge['station_id'])

    return graph

def save_graph(graph, filename):
    with open(filename, 'w') as f:
        json.dump(graph, f)
