from osemosys2iamc.resultify import main
import os
from yaml import load, SafeLoader
from pyam import IamDataFrame
from pyam.testing import assert_iamframe_equal
import pandas as pd

def test_main_input():

    config = os.path.join("tests", "fixtures", "config_input.yaml")
    inputs = os.path.join("tests", "fixtures")
    results = os.path.join("tests", "fixtures")

    with open(config, 'r') as config_file:
        config = load(config_file, Loader=SafeLoader)

    actual = main(config, inputs, results)

    data = pd.DataFrame([
        ['Austria', 'Price|Primary Energy|Biomass', 2015, 3.15],
        ['Austria', 'Price|Primary Energy|Biomass', 2016, 4.2],
        ['Belgium', 'Price|Primary Energy|Biomass', 2015, 1.785],
        ['Belgium', 'Price|Primary Energy|Biomass', 2016, 1.890],
    ], columns=['region', 'variable', 'year', 'value'])

    expected = IamDataFrame(data, model='OSeMBE v1.0.0', scenario= 'DIAG-C400-lin-ResidualFossil', unit='EUR_2020/GJ')

    assert_iamframe_equal(actual, expected)

def test_main_result():

    config = os.path.join("tests", "fixtures", "config_result.yaml")
    inputs = os.path.join("tests", "fixtures")
    results = os.path.join("tests", "fixtures")

    with open(config, 'r') as config_file:
        config = load(config_file, Loader=SafeLoader)

    actual = main(config, inputs, results)

    data = pd.DataFrame([
        ['Austria','Capacity|Electricity',2015,0.446776],
        ['Belgium','Capacity|Electricity',2016,0.184866],
        ['Bulgaria','Capacity|Electricity',2015,4.141],
        ['Switzerland','Capacity|Electricity',2026,0.004563975391582646],
        ['Cyprus','Capacity|Electricity',2015,0.3904880555817921],
        ['Czech Republic','Capacity|Electricity',2015,0.299709],
        ['Germany','Capacity|Electricity',2015,9.62143],
        ['Denmark','Capacity|Electricity',2015,0.0005],
        ['Estonia','Capacity|Electricity',2015,0.006],
        ['Spain','Capacity|Electricity',2015,7.7308],
        ['Finland','Capacity|Electricity',2015,0.0263],
        ['France','Capacity|Electricity',2015,0.47835],
    ], columns=['region', 'variable', 'year', 'value'])

    expected = IamDataFrame(data, model='OSeMBE v1.0.0', scenario= 'DIAG-C400-lin-ResidualFossil', unit='GW')

    assert_iamframe_equal(actual, expected)
