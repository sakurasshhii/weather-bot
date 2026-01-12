import pandas as pd


with open(fr'app\bot\lexic\coordinates.txt', encoding='utf-8') as f:
    head = f.readline().split()
    data = [line.split() for line in f.readlines()]
    d = {' '.join(line[:-3]): (float(line[-3]), float(line[-2])) for line in data}
    d = pd.DataFrame(d, index=("latitude", "longitude"))
    
    coordinates = d.transpose()