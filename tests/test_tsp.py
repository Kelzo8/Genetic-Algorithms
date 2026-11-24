import math

import numpy as np

from GP.primitives import FUNCTIONS
from tsp.baselines import nearest_neighbour_tour
from tsp.constructor import construct_tour
from tsp.datasets import generate_uniform_map
from tsp.features import candidate_features
from tsp.fitness import make_fitness_function
from tsp.instance import TSPInstance


TERMINALS = ["D_cn", "D_in", "D_c"]
FOUR_CITIES = TSPInstance(np.array([[0, 0], [3, 0], [3, 4], [0, 4]], dtype=float))


def test_distance_matrix_is_symmetric_euclidean():
    distances = FOUR_CITIES.distance_matrix()
    np.testing.assert_allclose(distances, distances.T)
    np.testing.assert_allclose(np.diag(distances), 0.0)
    np.testing.assert_allclose(distances[0], [0.0, 3.0, 5.0, 4.0])


def test_tour_length_includes_return_to_start():
    assert FOUR_CITIES.tour_length([0, 1, 2, 3]) == 14.0
    assert FOUR_CITIES.tour_length([0, 1, 2, 3, 0]) == 14.0


def test_candidate_features_include_excluding_candidate_centroid():
    result = candidate_features(FOUR_CITIES, 0, 0, [1, 2, 3], FOUR_CITIES.distance_matrix())
    assert result[1]["D_cn"] == result[1]["D_in"] == 3.0
    assert math.isclose(result[1]["D_c"], math.sqrt(18.25))
    assert result[2]["D_cn"] == result[2]["D_in"] == 5.0
    assert result[2]["D_c"] == 2.5
    assert result[3]["D_cn"] == result[3]["D_in"] == 4.0
    assert math.isclose(result[3]["D_c"], math.sqrt(13.0))

    only_one = candidate_features(FOUR_CITIES, 2, 0, [3], FOUR_CITIES.distance_matrix())
    assert only_one[3]["D_c"] == 0.0


def test_constructed_tour_visits_each_city_once_and_closes():
    tour = construct_tour("D_cn", FOUR_CITIES, TERMINALS, FUNCTIONS)
    assert tour[0] == tour[-1] == 0
    assert sorted(tour[:-1]) == list(range(FOUR_CITIES.n_cities))


def test_nearest_neighbour_tour_and_seeded_generation_are_deterministic():
    tour = nearest_neighbour_tour(FOUR_CITIES)
    assert tour == [0, 1, 2, 3, 0]
    first = generate_uniform_map(12, seed=123)
    second = generate_uniform_map(12, seed=123)
    np.testing.assert_array_equal(first.coordinates, second.coordinates)
    assert nearest_neighbour_tour(first) == nearest_neighbour_tour(second)


def test_fitness_returns_mean_constructed_tour_length():
    fitness = make_fitness_function([FOUR_CITIES], TERMINALS, FUNCTIONS)
    assert math.isclose(fitness("D_cn"), 18.0)


def test_shorter_tour_rule_receives_lower_fitness():
    fitness = make_fitness_function([FOUR_CITIES], TERMINALS, FUNCTIONS)
    longer_rule = "D_cn"
    shorter_rule = ("neg", "D_cn")

    longer_fitness = fitness(longer_rule)
    shorter_fitness = fitness(shorter_rule)

    assert math.isclose(longer_fitness, 18.0)
    assert math.isclose(shorter_fitness, 14.0)
    assert shorter_fitness < longer_fitness


def test_fitness_returns_infinity_for_zero_mean_length():
    one_city = TSPInstance(np.array([[1.0, 2.0]]))
    fitness = make_fitness_function([one_city], TERMINALS, FUNCTIONS)
    assert math.isinf(fitness("D_cn"))
