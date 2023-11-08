import pytest
import math
from railway import Station, RailNetwork, fare_price
from utilities import read_rail_network
from pathlib import Path

# create test set for RailNetwork`s test
network_csv = Path("uk_stations.csv")
rail_network = read_rail_network(network_csv)

st1 = Station("Edinburgh Park", "Scotland", "EDP", 55.927615, -3.307829, 0)
st2 = Station("Aberdeen", "Scotland", "EDP", 57.143127, -2.097464, 1)
st3 = Station("Edinburgh Park", "Scotland", "EDP", 55.927615, -3.307829, False)
st4 = Station("Edinburgh Park", "Scotland", "EDP", 55.927615, -3.307829, 0)
st5 = Station("Aberdeen", "Scotland", "ABD", 57.143127, -2.097464, 0) 


@pytest.mark.parametrize("name, region, crs, lati, longi, hub, expected, errorType", [
    # test type of name, region and crs
    (123, "Scotland", "EDP", 55.927615, -3.307829, False, "Type error: name, region and crs should be string", TypeError), 
    ("Edinburgh Park", 456, "EDP", 55.927615, -3.307829, False, "Type error: name, region and crs should be string", TypeError), 
    ("Edinburgh Park", "Scotland", 789, 55.927615, -3.307829, False, "Type error: name, region and crs should be string", TypeError), 
    
    # test type and values of latitude and longitude
    ("Edinburgh Park", "Scotland", "EDP", 91, 0, False, "Length error: -90 < latitude < 90", ValueError), 
    ("Edinburgh Park", "Scotland", "EDP", -91, 0, False, "Length error: -90 < latitude < 90", ValueError), 
    ("Edinburgh Park", "Scotland", "EDP", 0, 181, False, "Length error: -180 < longitude < 180", ValueError), 
    ("Edinburgh Park", "Scotland", "EDP", 0, -181, False, "Length error: -180 < longitude < 180", ValueError), 
    ("Edinburgh Park", "Scotland", "EDP", "hello", 0, False, "Type error: latitude and longitude are not decimal numbers", TypeError), 
    ("Edinburgh Park", "Scotland", "EDP", 0, "world", False, "Type error: latitude and longitude are not decimal numbers", TypeError), 
    
    # test type of hub
    ("Edinburgh Park", "Scotland", "EDP", 55.927615, -3.307829, -1, "Type error: hub should be bool or 0/1", TypeError), 
    ("Edinburgh Park", "Scotland", "EDP", 55.927615, -3.307829, "True", "Type error: hub should be bool or 0/1", TypeError), 
    
    # test crs
    ("Edinburgh Park", "Scotland", "EDPG", 55.927615, -3.307829, False, "Value Error: crs should be 3-character string with upper letters", ValueError),
    ("Edinburgh Park", "Scotland", "edp", 55.927615, -3.307829, False, "Value Error: crs should be 3-character string with upper letters", ValueError)])
def test_StationTypeError(name, region, crs, lati, longi, hub, expected, errorType):
    with pytest.raises(errorType) as e:
        Station(name, region, crs, lati, longi, hub)
    exec_msg = e.value.args[0]
    assert exec_msg == expected


# test fare_price() function
def test_farePrice():
    assert fare_price(100, 10, 10) == 1 + 100 * math.exp(-1) * (1 + 10)


def test_StationFunctions():
    # test distance_to() function
    st1 = Station("Edinburgh Park", "Scotland", "EDP", 55.927615, -3.307829, 0)
    st2 = Station("Aberdeen", "Scotland", "ABD", 57.143127, -2.097464, 1) 
    st3 = Station("Station3", "Scotland", "TES", 55.927615, -3.307829, 1) 
    
    ## distance between station1 and station2 is about 154.19
    assert round(st1.distance_to(st2), 2) == 154.19
    ## distance between station1 and station3 is 0
    assert st1.distance_to(st3) == 0

# test normal functions in class RailNetwork
def test_RailNetworkFunctions():
    # test unique crs in the Network
    with pytest.raises(ValueError) as e:
        RailNetwork([st1, st2])
    exec_msg = e.value.args[0]
    assert exec_msg == f"Value error: two stations with same crs: {st1.crs}."

    # test regions() function
    assert set(rail_network.regions) == set(['East of England', 'North West', 'London', 'Scotland', 
                                    'South West', 'West Midlands', 'Yorkshire and The Humber', 
                                    'North East', 'East Midlands', 'South East', 'Wales'])
    
    # test n_stations() function
    assert rail_network.n_stations == 2395

# test hub_stations() function
def test_hubStations():
    ## test all stations in the network
    assert len(rail_network.hub_stations()) == 41

    ## test stations in North West
    assert len(rail_network.hub_stations("North West")) == 3
    receve_list = []  # transfer Station class into string
    for i in rail_network.hub_stations("North West"):
        receve_list.append(str(i))
    assert set(receve_list) == set(['Station(CAR-Carlisle/North West-hub)', 
                                    'Station(LIV-Liverpool Lime Street/North West-hub)', 
                                    'Station(MAN-Manchester Piccadilly/North West-hub)'])

# test closest_hub() function
def test_closestHub():
    ## test normal case
    assert str(rail_network.closest_hub(st3)) == "Station(STG-Stirling/Scotland-hub)"

    ## test regions with no hub station
    ## test network with no hub
    with pytest.raises(ValueError) as e:
        RailNetwork([st4, st5]).hub_stations("Scotland")
    exec_msg = e.value.args[0]
    assert exec_msg == "Error: hub does not exist in this region"

# test journey_planner() function
def test_JourneyPlanner():
    ## test start and dest are the same station
    with pytest.raises(ValueError) as e:
        RailNetwork([st4, st5]).journey_planner("EDP", "EDP")
    exec_msg = e.value.args[0]
    assert exec_msg == "Warning, you cannot travel between same station!"

    ## test crs not in the list
    with pytest.raises(ValueError) as e:
        RailNetwork([st4, st5]).journey_planner("EDP", "EFG")  # this network contains EDP and ABD
    exec_msg = e.value.args[0]
    assert exec_msg == "Value error: crs does not exists"

    ## test normal function
    assert rail_network.journey_planner("BTN", "KGX") == [rail_network.stations["BTN"], rail_network.stations["KGX"]]

# test journey_fare() function
def test_journeyFare():
    ## test money
    assert round(rail_network.journey_fare("BTN", "KGX"), 2) == round(90.38331633489044, 2)

    ## test case with summary == True
    assert rail_network.journey_fare("EDP", "BTN", summary=True) == 31.87
    assert rail_network.journey_fare("AVY", "CDF", summary=True) == 36.16

# test plot_fare_to() function
def test_plotFare():
    rail_network.plot_fares_to("KGX", save=True, bins=10)
    assert Path('./Fare_price_to_London_Kings_Cross.png').exists() == True

