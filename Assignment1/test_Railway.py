import pytest
from railway import Station, RailNetwork
from utilities import read_rail_network
from pathlib import Path

# create test set for RailNetwork`s test
network_csv = Path("uk_stations.csv")
rail_network = read_rail_network(network_csv)


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


def test_StationFunctions():
    # test distance_to() function
    st1 = Station("Edinburgh Park", "Scotland", "EDP", 55.927615, -3.307829, 0)
    st2 = Station("Aberdeen", "Scotland", "ABD", 57.143127, -2.097464, 1) 
    st3 = Station("Station3", "Scotland", "TES", 55.927615, -3.307829, 1) 
    
    # distance between station1 and station2 is about 154.19
    assert round(st1.distance_to(st2), 2) == 154.19
    # distance between station1 and station3 is 0
    assert st1.distance_to(st3) == 0


def test_RailNetworkFunctions():
    # test unique crs in the Network
    st1 = Station("Edinburgh Park", "Scotland", "EDP", 55.927615, -3.307829, 0)
    st2 = Station("Aberdeen", "Scotland", "EDP", 57.143127, -2.097464, 1)
    with pytest.raises(IOError) as e:
        RailNetwork([st1, st2])
    exec_msg = e.value.args[0]
    assert exec_msg == f"Input error: two stations with same crs: {st1.crs}."

    # test regions() function
    assert set(rail_network.regions) == set(['East of England', 'North West', 'London', 'Scotland', 
                                    'South West', 'West Midlands', 'Yorkshire and The Humber', 
                                    'North East', 'East Midlands', 'South East', 'Wales'])
    
    # test n_stations() function
    assert rail_network.n_stations == 2395

    # test return information

    # test hub_stations() function
    assert len(rail_network.hub_stations()) == 41
    assert len(rail_network.hub_stations("North West")) == 3
    receve_list = []  # transfer Station class into string
    for i in rail_network.hub_stations("North West"):
        receve_list.append(str(i))
    assert set(receve_list) == set(['Station(CAR-Carlisle/North West-hub)', 
                                    'Station(LIV-Liverpool Lime Street/North West-hub)', 
                                    'Station(MAN-Manchester Piccadilly/North West-hub)'])



    # test closest_hub() function

    # test journey_planner() function

    # test journey_fare() function

    # test plot_fare_to() function

