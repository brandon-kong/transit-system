from train.graph import ( load_graph )
from train.pathfinding import ( get_closest_path )
from util.normalize import normalize_string as _

def main():
    graph = load_graph('data/chicago_train.json')
    
    start_station = input('Enter start station: ')

    start_station = graph.get_station(start_station)
    start_station_id = start_station['id'] if start_station is not None else None

    if start_station_id is None:
        print('Start station not found')
        return
    
    end_station = input('Enter end station: ')

    end_station = graph.get_station(end_station)
    end_station_id = end_station['id'] if end_station is not None else None

    if end_station_id is None:
        print('End station not found')
        return
        
    path = get_closest_path(graph, start_station_id, end_station_id)
    print(path)

if __name__ == '__main__':
    main()