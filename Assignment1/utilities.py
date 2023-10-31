import csv
from railway import Station, RailNetwork

def read_rail_network(filepath):
    all_stations = []
    with open(filepath, "r", encoding = "utf-8") as f:
        read_file = csv.reader(f)
        col_list = next(read_file)
        csv_reader = csv.DictReader(f, fieldnames = col_list)  # read first row as the key

        # read and store data
        for i in csv_reader:
            st = {}
            for k, v in i.items():
                st[k] = v
            all_stations.append(Station(st["name"], st["region"], st["crs"], 
                                        st["latitude"], st["longitude"], st["hub"]))

    return RailNetwork(all_stations)

    raise NotImplementedError



