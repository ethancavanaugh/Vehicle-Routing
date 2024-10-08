from datetime import *
from Package import *
from RouteFinder import RouteFinder


class Truck:
    AVG_SPEED_MPH = 18

    # Takes a list of package objects and applies the two-opt algorithm at the time of initialization
    def __init__(self, truck_id: int, packages: list[Package], route_finder: RouteFinder):
        self.truck_id = truck_id
        self.route_finder = route_finder
        self.packages = route_finder.two_opt_tour(packages)
        self.total_distance = 0

    # Deliver all packages, updating their statuses and recording departure/delivery times
    def deliver_packages(self, departure_time: datetime):
        for p in self.packages:
            p.status = PackageStatus.EN_ROUTE
            p.truck_id = self.truck_id
            p.departure_time = departure_time

        # Update the time and status for each package that is delivered
        cur_time = departure_time
        for i in range(1, len(self.packages) - 1):
            package = self.packages[i]
            dist = self.__distance_between(self.packages[i - 1], self.packages[i])
            transit_time = timedelta(hours=(dist / self.AVG_SPEED_MPH))

            self.total_distance += dist
            cur_time += transit_time
            package.status = PackageStatus.DELIVERED
            package.delivered_time = cur_time

        # Return to hub
        return_dist = self.__distance_between(self.packages[-2], self.packages[-1])
        self.total_distance += return_dist
        cur_time += timedelta(hours=(return_dist / self.AVG_SPEED_MPH))
        print("Truck " + str(self.truck_id) + " completed all deliveries and returned to the hub at " + str(cur_time))

    # Return the distance between two packages' delivery addresses
    def __distance_between(self, pkg1, pkg2):
        return (self.route_finder.distance_table[self.route_finder.addr_index_map[pkg1.address]]
                                                [self.route_finder.addr_index_map[pkg2.address]])
