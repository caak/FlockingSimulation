from world import World
import world_configs
from data_analyzer import DataAnalyzer
from bird import Bird

width = 1200
height = 900

good_count = 50
bad_count = 10
bird_count = good_count + bad_count


for simulation in range(1, 11):
    w = world_configs.Circle(width, height, good_count, bad_count, simulation)

    charter = DataAnalyzer(width, 10, 100, good_count, bad_count)


    for i in range(0, 1000):
        w.update(10)
        charter.track(w)
    P = charter.TP + charter.FN
    N = charter.TN + charter.FP
    print(simulation, charter.TP / P, charter.FN / N, charter.TP, charter.FP, charter.TN, charter.FN)

