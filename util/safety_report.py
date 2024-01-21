import json
from datetime import datetime
from util.distance import calculate_distance

def calculate_safety_penalties(safety_reports_file, stations):
    safety_reports = []

    with open(safety_reports_file, 'r') as f:
        safety_reports = json.load(f)

    severity_penalties = {
        'Low': 1,
        'Medium': 5,
        'High': 10,
        'Critical': 50
    }

    safety_penalties = {}

    for report in safety_reports:
        severity = report['severity_level']
        date_of_report = datetime.strptime(report['date_of_report'], '%Y-%m-%d')

        # If the report is older than 1 month, we don't consider it
        if (datetime.now() - date_of_report).days > 30:
            continue

        # if the station is in proximity or on the path, we add a penalty

        for station in stations:
            station_lat, station_lon = station['geometry']['coordinates'][1], station['geometry']['coordinates'][0]
            report_lat, report_lon = report['geometry']['coordinates'][1], report['geometry']['coordinates'][0]
            distance = calculate_distance(report_lat, report_lon, station_lat, station_lon)

            if distance <= 0.5:
                station_id = station['id']
                if station_id not in safety_penalties:
                    safety_penalties[station_id] = severity_penalties[severity]
                else:
                    safety_penalties[station_id] += severity_penalties[severity]

    return safety_penalties