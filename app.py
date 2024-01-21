from train.graph import ( load_graph )
from train.pathfinding import ( get_closest_path )
from util.normalize import normalize_string as _
from util.input_parser import parse_input

def main():
    graph = load_graph('data/chicago_train.json')
    
    start_station, start_line = parse_input(input('Enter start station: '))

    start_station = graph.get_station(start_station, start_line)
    start_station_id = start_station['id'] if start_station is not None else None

    if start_station_id is None:
        print('Start station not found')
        return
    
    end_station, end_line = parse_input(input('Enter end station: '))

    print(end_station, end_line)
    end_station = graph.get_station(end_station, end_line)
    end_station_id = end_station['id'] if end_station is not None else None

    if end_station_id is None:
        print('End station not found')
        return
        
        
    path = get_closest_path(graph, start_station_id, end_station_id)

    if (path is None):
        print('No path found')
        return
    
    print(graph.station_id_list_to_english(path))

if __name__ == '__main__':
    main()