import pytest
from railway import Station, RailNetwork
from utilities import read_rail_network


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
#["Edinburgh Park", "Scotland", "EDP", 55.927615, -3.307829, False]
#name, region, crs, lati, longi, hub
def test_StationTypeError(name, region, crs, lati, longi, hub, expected, errorType):
    with pytest.raises(errorType) as e:
        Station(name, region, crs, lati, longi, hub)
    exec_msg = e.value.args[0]
    assert exec_msg == expected