from .instance import TSPInstance


def nearest_neighbour_tour(instance: TSPInstance) -> list[int]:
    """Return a closed nearest-neighbour tour starting at city zero."""
    if instance.n_cities == 0:
        raise ValueError("cannot construct a tour for an instance with no cities")

    distances = instance.distance_matrix()
    unvisited = set(range(1, instance.n_cities))
    tour = [0]
    current = 0
    while unvisited:
        next_city = min(unvisited, key=lambda city: (distances[current, city], city))
        tour.append(next_city)
        unvisited.remove(next_city)
        current = next_city
    tour.append(0)
    return tour
