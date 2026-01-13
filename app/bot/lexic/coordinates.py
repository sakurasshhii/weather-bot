import pandas as pd


__all__ = ['coordinates', 'city_names']

with open(fr'app\bot\lexic\coordinates.txt', encoding='utf-8') as f:
    head = f.readline().split()
    data = [line.split() for line in f.readlines()]
    d = {
        ' '.join(line[:-3]): (float(line[-3]), float(line[-2]))
        for line in data
    }
    
    coordinates = pd.DataFrame(d, index=("latitude", "longitude"))
    city_names = tuple(d.keys())
