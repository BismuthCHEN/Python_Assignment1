import csv

def read_rail_network(filepath):
    all_stations = []
    with open(filepath, "r", encoding = "utf-8") as f:
        read_file = csv.reader(f)
        col_list = next(read_file)
        csv_reader = csv.DictReader(f, fieldnames = col_list)
        for i in csv_reader:
            st = {}
            for k, v in i.items():
                st[k] = v
            all_stations.append(st)
    return all_stations

    raise NotImplementedError



