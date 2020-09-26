import math
import random
import copy


class RoadLane:
    cars = 0

    def __init__(self, cars=0):
        self.cars = cars


class TimedLights:
    # up, left, down, right
    directions = [0, 0, 0, 0]
    lights = [False, False, False, False]
    score = 0
    collisions = 0
    delay = 0

    def check_collisions(self) -> bool:
        if ((self.lights[0] and self.directions[0] > 0) or (self.lights[2] and self.directions[2] > 0)) and ((self.lights[1] and self.directions[1] > 0) or (self.lights[3] and self.directions[3] > 0)):
            return True
        return False

    def tick(self):
        if self.delay == 0:
            if self.lights[0]:
                self.lights = [False, True, False, True]
            else:
                self.lights = [True, False, True, False]
            self.delay = 5

        self.delay -= 1

        if self.check_collisions():
            # print("Collision detected!")
            # self.score -= 10
            self.collisions += 3

        if self.collisions == 0:
            for i in range(4):
                if self.lights[i] and self.directions[i] > 0:
                    self.directions[i] -= 1
                    self.score += 1

        if sum(self.directions) <= 4:
            self.score += 2

    def print_info(self):
        print("Score:\n", self.score)
        print("Weights:\n", self.weights)
        print("Directions:\n", self.directions)
        print("Lights:\n", self.lights)

    def iterate_until_free(self, time_limit):
        for i in range(time_limit):
            # print("====== Iteration:", i)
            # self.print_info()
            self.tick()

            if sum(self.directions) == 0:
                return time_limit - i
        return 0

    def reset_roads(self, directions):
        self.collisions = 0
        self.directions = directions
        self.starting_cars = sum(directions)
        self.lights = [False, False, False, False]

    def reset_score(self):
        self.score = 0

    def set_random_weights(self):
        for layer in range(2):
            for x in range(4):
                for y in range(4):
                    self.weights[layer][x][y] = round(random.uniform(-1, 1), 2)

    def __init__(self, directions):
        self.reset_roads(directions)
        self.reset_score()
        # up, left, down, right
        self.ih = [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]

        self.hp = [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]

        self.weights = [self.ih, self.hp]

        self.delay = 0


class NeuroNetwork:
    # up, left, down, right
    ih = [[0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]]

    hp = [[0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]]

    weights = [ih, hp]

    # up, left, down, right
    directions = [0, 0, 0, 0]
    lights = [False, False, False, False]
    score = 0
    collisions = 0

    def check_collisions(self) -> bool:
        if ((self.lights[0] and self.directions[0] > 0) or (self.lights[2] and self.directions[2] > 0)) and ((self.lights[1] and self.directions[1] > 0) or (self.lights[3] and self.directions[3] > 0)):
            return True
        return False

    def tick(self):
        neuro_out = neural_network(self.directions, self.weights)

        for i in range(4):
            self.lights[i] = neuro_out[i] > 0

        if self.check_collisions():
            # print("Collision detected!")
            # self.score -= 10
            self.collisions += 3

        if self.collisions == 0:
            for i in range(4):
                if self.lights[i] and self.directions[i] > 0:
                    self.directions[i] -= 1
                    self.score += 1

        if sum(self.directions) <= 4:
            self.score += 2

    def print_info(self):
        print("Score:\n", self.score)
        print("Weights:\n", self.weights)
        print("Directions:\n", self.directions)
        print("Lights:\n", self.lights)

    def iterate_until_free(self, time_limit):
        for i in range(time_limit):
            # print("====== Iteration:", i)
            # self.print_info()
            self.tick()

            if sum(self.directions) == 0:
                return time_limit - i
        return 0

    def reset_roads(self, directions):
        self.collisions = 0
        self.directions = directions
        self.starting_cars = sum(directions)
        self.lights = [False, False, False, False]

    def reset_score(self):
        self.score = 0

    def set_random_weights(self):
        for layer in range(2):
            for x in range(4):
                for y in range(4):
                    self.weights[layer][x][y] = round(random.uniform(-1, 1), 2)

    def __init__(self, directions):
        self.reset_roads(directions)
        self.reset_score()
        # up, left, down, right
        self.ih = [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]

        self.hp = [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]

        self.weights = [self.ih, self.hp]


def w_sum(a, b):
    assert(len(a) == len(b))
    output = 0
    for i in range(len(a)):
        output += (a[i] * b[i])
    return output


def vect_mat_mul(vect, matrix):
    # assert(len(vect) == len(matrix))
    output = [0, 0, 0, 0]
    for i in range(len(output)):
        output[i] = w_sum(vect, matrix[i])
    return output


def neural_network(input, weights):
    hid = vect_mat_mul(input, weights[0])
    pred = vect_mat_mul(hid, weights[1])
    return pred


if __name__ == "__main__":
    # Configuration
    generations = 300
    units_per_gen = 50
    mutated_units = 30
    mutations = 1
    mut_min = -1
    mut_max = 1
    reseted_units = 3
    resets = 1
    reset_min = -2
    reset_max = 2
    training_situations = 25
    directions_shuffle_delay = 45
    max_iters = 100
    additional_cars = 1.5

    networks = []

    for i in range(units_per_gen):
        network = NeuroNetwork([0, 0, 0, 0])
        network.set_random_weights()
        networks.append(network)

    training_directions = []

    for generation in range(generations):
        print("=== Generation", generation)

        if generation % directions_shuffle_delay == 0:
            training_directions = []
            for i in range(training_situations):
                directions = [0, 0, 0, 0]
                for j in range(4):
                    directions[j] = random.randint(0, 30)
                training_directions.append(directions)
            print("Directions shuffle! New directions:", training_directions)

        # Iterating
        for i in range(units_per_gen):
            networks[i].reset_score()
            for starting_directions in training_directions:
                networks[i].reset_roads(copy.deepcopy(starting_directions))
                add_whole = math.floor(additional_cars)
                add_float = additional_cars - add_whole
                additional_cars_queue = [add_whole] * (max_iters - int(max_iters * add_float)) + (
                                        [add_whole + 1] * int(max_iters * add_float))
                random.shuffle(additional_cars_queue)
                for j in range(max_iters):
                    networks[i].tick()
                    if additional_cars_queue[i] > 0:
                        direction = random.randint(0, 3)
                        networks[i].directions[direction] += add_whole

        total_score = sum(net.score for net in networks)

        networks.sort(key=lambda net: net.score, reverse=True)

        print("Max score:", networks[0].score)
        print("Min score:", networks[units_per_gen - 1].score)
        print("Median score:", networks[int(units_per_gen / 2)].score)
        print("Average score:", total_score / units_per_gen)
        print("Best weights:", networks[0].weights)

        # Selection
        selected = []
        for i in range(int(units_per_gen / 2)):
            selected.append(networks[i])

        # Getting parents
        parents = [[], []]
        for i in range(0, units_per_gen - 1, 2):
            parents[0].append(networks[i])
            parents[1].append(networks[i+1])

        offsprings = []
        for i in range(len(parents[0])):
            offspring = copy.deepcopy(parents[0][i])
            for layer in range(2):
                for x in range(4):
                    for y in range(4):
                        if random.random() >= 0.5:
                            offspring.weights[layer][x][y] = parents[1][i].weights[layer][x][y]
            offsprings.append(offspring)

        for i in range(units_per_gen // 2, units_per_gen):
            networks[i] = offsprings[i - units_per_gen // 2]

        # Mutations
        for i in random.sample(range(0, units_per_gen - 1), mutated_units):
            n = random.randint(i, i + 1)
            for j in range(mutations):
                layer = random.randint(0, 1)
                x = random.randint(0, 3)
                y = random.randint(0, 3)
                networks[n].weights[layer][x][y] += random.uniform(mut_min, mut_max)
                networks[n].weights[layer][x][y] = round(networks[n].weights[layer][x][y], 2)

        for i in random.sample(range(0, units_per_gen - 1), reseted_units):
            n = random.randint(i, i + 1)
            for j in range(resets):
                layer = random.randint(0, 1)
                x = random.randint(0, 3)
                y = random.randint(0, 3)
                networks[n].weights[layer][x][y] = random.uniform(reset_min, reset_max)
                networks[n].weights[layer][x][y] = round(networks[n].weights[layer][x][y], 2)
