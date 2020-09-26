import smart_traffic_light
import random
import math

total_iterations = 5000
ticks_per_iter = 100
dynamic_ticks = 500000
dynamic_add_cars = 0.3


def test(weights):
    neuro = smart_traffic_light.NeuroNetwork([0, 0, 0, 0])
    neuro.weights = weights
    free_ticks = 0
    exceeded = 0
    for i in range(total_iterations):
        if i % 50 == 0:
            print("Iteration", i)
        directions = [0, 0, 0, 0]
        for j in range(4):
            directions[j] = random.randint(0, 30)
        neuro.reset_roads(directions)
        ticks = neuro.iterate_until_free(ticks_per_iter)
        free_ticks += ticks
        if sum(neuro.directions) != 0:
            exceeded += 1

    print("Total ticks:", total_iterations * ticks_per_iter)
    print("Free ticks:", free_ticks)
    print("Free / total:", free_ticks / (total_iterations * ticks_per_iter) * 100, "%")
    print("Time exceeded:", exceeded)


def test_dynamic(weights):
    neuro = smart_traffic_light.NeuroNetwork([10, 10, 10, 10])
    neuro.weights = weights
    add_whole = math.floor(dynamic_add_cars)
    add_float = dynamic_add_cars - add_whole
    additional_cars_queue = [add_whole] * (dynamic_ticks - int(dynamic_ticks * add_float)) + ([add_whole + 1] * int(dynamic_ticks * add_float))
    random.shuffle(additional_cars_queue)
    for i in range(dynamic_ticks):
        if i % 1000 == 0:
            print("Tick", i)
        if additional_cars_queue[i] > 0:
            direction = random.randint(0, 3)
            neuro.directions[direction] += add_whole
        neuro.tick()

    print("Score:", neuro.score)
    print("Total cars:", 40 + dynamic_ticks * dynamic_add_cars)
    print("Passed cars:", 40 + dynamic_ticks * dynamic_add_cars - sum(neuro.directions))
    print("Passed ratio:", (40 + dynamic_ticks * dynamic_add_cars - sum(neuro.directions)) / (40 + dynamic_ticks * dynamic_add_cars) * 100, "%")


def test_timed():
    neuro = smart_traffic_light.TimedLights([0, 0, 0, 0])
    free_ticks = 0
    exceeded = 0
    for i in range(total_iterations):
        if i % 50 == 0:
            print("Iteration", i)
        directions = [0, 0, 0, 0]
        for j in range(4):
            directions[j] = random.randint(0, 30)
        neuro.reset_roads(directions)
        ticks = neuro.iterate_until_free(ticks_per_iter)
        free_ticks += ticks
        if sum(neuro.directions) != 0:
            exceeded += 1

    print("Total ticks:", total_iterations * ticks_per_iter)
    print("Free ticks:", free_ticks)
    print("Free / total:", free_ticks / (total_iterations * ticks_per_iter) * 100, "%")
    print("Time exceeded:", exceeded)


def test_dynamic_timed():
    neuro = smart_traffic_light.TimedLights([10, 10, 10, 10])

    add_whole = math.floor(dynamic_add_cars)
    add_float = dynamic_add_cars - add_whole
    additional_cars_queue = [add_whole] * (dynamic_ticks - int(dynamic_ticks * add_float)) + (
                [add_whole + 1] * int(dynamic_ticks * add_float))
    random.shuffle(additional_cars_queue)
    for i in range(dynamic_ticks):
        if i % 1000 == 0:
            print("Tick", i)
        if additional_cars_queue[i] > 0:
            direction = random.randint(0, 3)
            neuro.directions[direction] += add_whole
        neuro.tick()

    print("Score:", neuro.score)
    print("Total cars:", 40 + dynamic_ticks * dynamic_add_cars)
    print("Passed cars:", 40 + dynamic_ticks * dynamic_add_cars - sum(neuro.directions))
    print("Passed ratio:", (40 + dynamic_ticks * dynamic_add_cars - sum(neuro.directions)) / (
                40 + dynamic_ticks * dynamic_add_cars) * 100, "%")
