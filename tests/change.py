import json

map_paths = [
    "data/maps/test_maps/test_map_1.json",
    "data/maps/test_maps/test_map_2.json",
    "data/maps/test_maps/test_map_3.json",
    "data/maps/test_maps/test_map_4.json",
    "data/maps/test_maps/test_map_5.json"
]

replace = {
    "2.0.00": "2.1.00",
    "0.2.00": "2.0.00",
    "0.3.00": "0.2.00",
    "1.0.01": "1.1.00",
    "1.0.02": "1.2.00",
    "1.0.03": "1.3.00",
    "1.0.04": "1.4.00",
    "1.0.05": "1.5.00",
    "1.1.00": "1.2.00",
    "1.1.01": "1.3.00",
    "1.1.02": "1.4.00",
    "1.2.00": "1.6.00"
}

for map_path in map_paths:
    with open(map_path, "r") as file:
        previous_map_data = json.load(file)
        
    if "map" not in previous_map_data:
        previous_map_data["map"] = []
    
    map_arr = previous_map_data["map"]

    for j, row in enumerate(map_arr):
        for i, val in enumerate(row):
            if type(val) == list:
                map_arr[j][i] = [replace[val[x].split(":")[0]]+":"+val[x].split(":")[1] if val[x].split(":")[0] in replace else val[x] for x in range(len(val))]
                continue
            if val.split(":")[0] in replace:
                map_arr[j][i] = replace[val.split(":")[0]]+":"+val.split(":")[1]

    previous_map_data["map"] = map_arr

    with open(map_path, 'w') as file:
        json.dump(previous_map_data, file, indent=4)