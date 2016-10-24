"""Tests to ensure that the example simulation model fixtures are behaving


"""
import subprocess
from fixtures.water_supply import (ExampleWaterSupplySimulation,
                                   ExampleWaterSupplySimulationReservoir,
                                   process_results, raininess_oracle)
from pytest import raises


def test_water_supply_with_reservoir():
    raininess = 1
    reservoir_level = 2
    model = ExampleWaterSupplySimulationReservoir(raininess, reservoir_level)
    actual = model.simulate()
    expected = {'cost': 1.2, 'water': 3, 'reservoir level': 2}
    assert actual == expected


def test_water_supply_with_reservoir_negative_level():
    raininess = 1
    reservoir_level = -2
    with raises(ValueError, message="Reservoir level cannot be negative"):
        ExampleWaterSupplySimulationReservoir(raininess, reservoir_level)


def test_process_results():
    input_bytes = b"cost,1\nwater,1\n"
    actual = process_results(input_bytes)
    expected = {'water': 1, 'cost': 1}
    assert actual == expected


def test_raininess_oracle():
    time = [2010, 2020, 2030, 2042, 2050]
    expected = [1, 2, 3, 4, 5]

    for result in zip(time, expected):
        actual = raininess_oracle(result[0])
        assert actual == result[1]


def test_raininess_oracle_out_of_range():
    msg = "timestep 2051 is outside of the range [2010, 2050]"
    with raises(AssertionError, message=msg):
        raininess_oracle(2051)


def test_simulate_rain_cost_python():
    raininess = 1
    model = ExampleWaterSupplySimulation(raininess)
    actual = model.simulate()
    expected = {'cost': 1, 'water': 1}
    assert actual == expected


def test_simulate_rain_executable():
    raininess = 10
    model_executable = './tests/fixtures/water_supply_exec.py'
    argument = "--raininess={}".format(str(raininess))
    output = subprocess.check_output([model_executable, argument])
    results = process_results(output)
    assert results['water'] == 10
    assert results['cost'] == 1