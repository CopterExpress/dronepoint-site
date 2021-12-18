import csv

def get_coords():
    coords = []
    with open('mavlink/DAS Coordinates.csv', newline='') as file:
        spamreader = csv.reader(file)
        for row in spamreader:
            coords.append([
                float(row[1][1:]),
                float(row[2][:-1]),
            ])
    return coords

def get_trail(pos: list[float], drone_pos: list[float]):
    coords: list[list[float]] = get_coords()
    closest_pos = sorted(
        coords, 
        key=lambda x: (x[0] - pos[0]) ** 2 + (x[1] - pos[1]) ** 2 
    )[0]
    closest_drone = sorted(
        coords, 
        key=lambda x: (x[0] - drone_pos[0]) ** 2 + (x[1] - drone_pos[1]) ** 2 
    )[0]
    i1 = coords.index(closest_pos)
    i2 = coords.index(closest_drone)
    if i1 < i2:
        return coords[i1:i2+1][::-1]
    else:
        return coords[i2:i1+1]