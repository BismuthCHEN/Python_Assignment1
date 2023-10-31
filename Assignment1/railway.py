import matplotlib.pyplot as plt
import math
import numpy as np

def fare_price(distance, different_regions, hubs_in_dest_region):
    #raise NotImplementedError
    return 1 + distance * math.exp(1) ** (- distance / 100) * (1 + different_regions * hubs_in_dest_region / 10)



class Station:
    def __init__(self, name, region, crs, lati, longi, hub):

        # check input type
        if isinstance(name, str) != True or isinstance(region, str) != True or isinstance(crs, str) != True:
            print("Type error for name or region or crs")
            raise NotImplementedError
        #if lati.isdecimal() != True or longi.isdecimal() != True:
            #raise NotImplementedError
        if hub == 1:
            self.hub = True
        elif hub == 0:
            self.hub = False
        elif isinstance(hub, bool) != True:
            print("Type error for hub")
            raise NotImplementedError
        else:
            self.hub = hub
        
        # check number of latitue and longitude
        if lati > 90 or lati < -90:
            print("Length error for latitude")
            raise NotImplementedError
        if longi > 180 or longi < -180:
            print("Length error for longitude")
            raise NotImplementedError
        
        # check crs
        if crs.isupper() != True or len(crs) != 3 or crs.isalpha() != True:
            print("Input error for crs")
            raise NotImplementedError

        self.name = name
        self.region = region
        self.crs = crs
        self.lat = lati
        self.lon = longi
        #self.hub = hub

    def distance_to(self, target_station):
        fy_1 = np.radians(target_station.lat)
        fy_2 = np.radians(self.lat)
        theta_1 = np.radians(target_station.lon)
        theta_2 = np.radians(self.lon)

        # seperate calculation into 2 parts so its easy to understand
        part_1 = np.sin((fy_2 - fy_1) / 2) ** 2
        part_2 = np.cos(fy_1) * np.cos(fy_2) * np.sin((theta_2 - theta_1) / 2) ** 2

        dist = 2 * 6371 * np.arcsin(np.sqrt(part_1 + part_2))
        return dist

    # return sepefic information of one station
    def __str__(self):
        if self.hub == True:
            return f"Station({self.crs}-{self.name}/{self.region}-hub)"
        else:
            return f"Station({self.crs}-{self.name}/{self.region})"
        
    def __eq__(self, other):
        if self.crs == other.crs:
            return True
        else:
            return False


class RailNetwork:
    def __init__(self, station_list):
        check_list = []
        self.stations = {}
        for i in station_list:
            if i.crs not in check_list:  # unique crs
                check_list.append(i.crs)
                self.stations[i.crs] = i  # add station to the dict
            else:
                print(f"Error: two stations with same crs: {i.crs}.")
                raise NotImplementedError
        self.n_stations = self.n_stations()
        self.regions = self.regions()


    def regions(self):
        region_list = []
        for i in self.stations.keys():
            region_name = self.stations[i].region
            if region_name not in region_list:  # add region if it`s not in the list
                region_list.append(region_name)
        return region_list
        #raise NotImplementedError

    def n_stations(self):
        return len(self.stations.keys())
        #raise NotImplementedError

    def hub_stations(self, region = None):
        station_list = []
        region_list = []
        if region == None:
            for i in self.stations.values():
                if i.hub == True:
                    #station_list.append(i.__str__())  ####!!!!
                    station_list.append(i)
                    region_list.append(i.region)
        else:
            for i in self.stations.values():
                if i.hub == True and i.region == region:
                    #station_list.append(i.__str__())  ####!!!!
                    station_list.append(i)
                    region_list.append(i.region)
        
        if len(region_list) == 0:
            print("Error: hub does not exist in this region")
            raise NotImplementedError
        else:
            return(station_list)

        #raise NotImplementedError

    def closest_hub(self, s):
        if s.hub == True:
            return s
        else:
            hub_list = self.hub_stations(s.region)  # throw error if hub does not exist
            closest_h = hub_list[0]
            closest_dist = s.distance_to(hub_list[0])
            for i in range(len(hub_list)):  # calculate which station is the closest hub
                if s.distance_to(hub_list[i]) <= closest_dist:
                    closest_dist = s.distance_to(hub_list[i])
                    closest_h = hub_list[i]
            return closest_h

    def journey_planner(self, start, dest):
        start_station = self.stations[start]
        dest_station = self.stations[dest]
        journey_list = []

        # may not be essential here
        if start_station.__eq__(dest_station):
            print("Warning, you cannot travel between same station!")
            raise NotImplementedError

        # check whether two crs exists
        if start not in self.stations.keys() or dest not in self.stations.keys():
            print("Error: crs does not exists")
            raise NotImplementedError
        
        if start_station.region == dest_station.region:  # two stations are in the same region
            journey_list.append(start_station)
            journey_list.append(dest_station)
        else:
            start_hub  = self.closest_hub(start_station)
            dest_hub = self.closest_hub(dest_station)
            if start_hub.crs == start:  # start station is a hub
                journey_list.append(start_hub)
            else:  # start station is not a hub
                journey_list.append(start_station)
                journey_list.append(start_hub)

            if dest_hub.crs == start:  # dest station is a hub
                journey_list.append(dest_hub)
            else:  # dest station is not a hub
                journey_list.append(dest_station)
                journey_list.append(dest_hub)
        
        return journey_list
        #raise NotImplementedError

    def journey_fare(self, start, dest, summary):
        start_station = self.stations[start]
        dest_station = self.stations[dest]
        journey_list = self.journey_planner(start, dest)
        total_fare = 0
        


        # only
        if summary:
            return self.journey_planner(start, dest)
        #only calculate the 
        else:
            return self.journey_planner(start, dest)

        #raise NotImplementedError

    def plot_fares_to(self, crs_code, save, ADDITIONAL_ARGUMENTS):
        raise NotImplementedError

    def plot_network(self, marker_size: int = 5) -> None:
        """
        A function to plot the rail network, for visualisation purposes.
        You can optionally pass a marker size (in pixels) for the plot to use.

        The method will produce a matplotlib figure showing the locations of the stations in the network, and
        attempt to use matplotlib.pyplot.show to display the figure.

        This function will not execute successfully until you have created the regions() function.
        You are NOT required to write tests nor documentation for this function.
        """
        fig, ax = plt.subplots(figsize=(5, 10))
        ax.set_xlabel("Longitude (degrees)")
        ax.set_ylabel("Latitude (degrees)")
        ax.set_title("Railway Network")

        COLOURS = ["b", "r", "g", "c", "m", "y", "k"]
        MARKERS = [".", "o", "x", "*", "+"]

        for i, r in enumerate(self.regions):
            lats = [s.lat for s in self.stations.values() if s.region == r]
            lons = [s.lon for s in self.stations.values() if s.region == r]

            colour = COLOURS[i % len(COLOURS)]
            marker = MARKERS[i % len(MARKERS)]
            ax.scatter(lons, lats, s=marker_size, c=colour, marker=marker, label=r)

        ax.legend()
        plt.tight_layout()
        plt.show()
        return

    def plot_journey(self, start: str, dest: str) -> None:
        """
        Plot the journey between the start and end stations, on top of the rail network map.
        The start and dest inputs should the strings corresponding to the CRS codes of the
        starting and destination stations, respectively.

        The method will overlay the route that your journey_planner method has found on the
        locations of the stations in your network, and draw lines to indicate the route.

        This function will not successfully execute until you have written the journey_planner method.
        You are NOT required to write tests nor documentation for this function.
        """
        # Plot railway network in the background
        network_lats = [s.lat for s in self.stations.values()]
        network_lons = [s.lon for s in self.stations.values()]

        fig, ax = plt.subplots(figsize=(5, 10))
        ax.scatter(network_lons, network_lats, s=1, c="blue", marker="x")
        ax.set_xlabel("Longitude (degrees)")
        ax.set_ylabel("Latitude (degrees)")

        # Compute the journey
        journey = self.journey_planner(start, dest)
        plot_title = f"Journey from {journey[0].name} to {journey[-1].name}"
        ax.set_title(f"Journey from {journey[0].name} to {journey[-1].name}")

        # Draw over the network with the journey
        journey_lats = [s.lat for s in journey]
        journey_lons = [s.lon for s in journey]
        ax.plot(journey_lons, journey_lats, "ro-", markersize=2)

        plt.show()
        return
