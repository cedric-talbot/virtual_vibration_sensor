from iotile.fixture.device_fixture import per_test_device
from typedargs.exceptions import ArgumentError
import pytest

def test_set_min_and_max_correctly_sets_the_values() :
	""" get_min_and_max should return the values passed to set_min_and_max
	"""
	hw = per_test_device(port='virtual:./vibration_device/vibration_device.py', device_id=1).next()
	con = hw.controller()
	con.set_min_and_max(1,3)
	values = con.get_min_and_max()
	assert values == (1,3)

	con.set_min_and_max(7,7)
	values = con.get_min_and_max()
	assert values == (7,7)

	con.set_min_and_max(7352, 8242)
	values = con.get_min_and_max()
	assert values == (7352,8242)


def test_both_values_must_be_positive() :
	""" set_min_and_max should return an error when called with a negative value
	"""
	hw = per_test_device(port='virtual:./vibration_device/vibration_device.py', device_id=1).next()
	con = hw.controller()
	con.set_min_and_max(1,5)

	with pytest.raises(ArgumentError) :
		con.set_min_and_max(-5,-2)
	values = con.get_min_and_max()
	#min_value and max_value should not have changed
	assert values == (1,5)

	with pytest.raises(ArgumentError) :
		con.set_min_and_max(18,-37)
	values = con.get_min_and_max()
	assert values == (1,5)

	with pytest.raises(ArgumentError) :
		con.set_min_and_max(-1438,4239)
	values = con.get_min_and_max()
	assert values == (1,5)


def test_min_value_cant_be_greater_than_max_value() :
	""" set_min_and_max should return an error when called with a min_value greater
	than max_value
	"""
	hw = per_test_device(port='virtual:./vibration_device/vibration_device.py', device_id=1).next()
	con = hw.controller()
	con.set_min_and_max(2,8)

	with pytest.raises(ArgumentError) :
		con.set_min_and_max(9,7)
	values = con.get_min_and_max()
	#min_value and max_value should not have changed
	assert values == (2,8)

	with pytest.raises(ArgumentError) :
		con.set_min_and_max(5426,2345)
	values = con.get_min_and_max()
	assert values == (2,8)

	with pytest.raises(ArgumentError) :
		con.set_min_and_max(995,522)
	values = con.get_min_and_max()
	assert values == (2,8)


def test_get_vibration_returns_a_value_between_min_value_and_max_value() :
	""" get_vibration should return a value between min_value and max_value
	"""
	hw = per_test_device(port='virtual:./vibration_device/vibration_device.py', device_id=1).next()
	con = hw.controller()
	con.set_min_and_max(5,32)
	for i in range(10) :
		vibration = con.get_vibration()
		assert (5 <= vibration and vibration <= 32)

	con.set_min_and_max(52,67)
	for i in range(10) :
		vibration = con.get_vibration()
		assert (52 <= vibration and vibration <= 67)

	con.set_min_and_max(125,4743)
	for i in range(10) :
		vibration = con.get_vibration()
		assert (125 <= vibration and vibration <= 4743)