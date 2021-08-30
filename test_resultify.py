import pandas as pd
import os
from .resultify import filter_fuel, filter_emission, filter_primary_energy


class TestEmissions:

    def test_filter_emission(self):

        filepath = os.path.join("tests", 'fixtures', "AnnualTechnologyEmissions.csv")
        input_data = pd.read_csv(filepath)

        emission = ['CO2']
        actual = filter_emission(input_data, emission)

        data = [
            ['AT', 'CO2', 2030, 3043.14883455963],
            ['AT', 'CO2', 2031, 2189.064680841067],
            ['AT', 'CO2', 2032, 2315.8212665203155],
            ["BG", 'CO2', 2030, 11096.55693088164],
            ["BG", 'CO2', 2031, 11069.257140908643],
            ["BG", 'CO2', 2032, 11041.957354265856],
        ]

        expected = pd.DataFrame(data=data, columns=['REGION', 'EMISSION', 'YEAR', 'VALUE'])

        index = ['REGION', 'EMISSION', 'YEAR']

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

class TestFilter:

    def test_filter_fuel(self):
        filepath = os.path.join("tests", 'fixtures', "UseByTechnology.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['ALUPLANT']
        fuels = ['C1_P_HCO']
        actual = filter_fuel(input_data, technologies, fuels)

        data = [
            ['Globe', 'ID', 'ALUPLANT', 'C1_P_HCO', 2010, 0.399179303],
            ['Globe', 'ID', 'ALUPLANT', 'C1_P_HCO', 2011, 0.397804018],
            ['Globe', 'ID', 'ALUPLANT', 'C1_P_HCO', 2012, 0.390495285],
            ['Globe', 'IN', 'ALUPLANT', 'C1_P_HCO', 2010, 0.399179303],
            ['Globe', 'IN', 'ALUPLANT', 'C1_P_HCO', 2011, 0.397804018],
            ['Globe', 'IN', 'ALUPLANT', 'C1_P_HCO', 2012, 0.390495285],
            ['Globe', 'IP', 'ALUPLANT', 'C1_P_HCO', 2010, 0.029739228],
            ['Globe', 'IP', 'ALUPLANT', 'C1_P_HCO', 2011, 0.029739228],
            ['Globe', 'IP', 'ALUPLANT', 'C1_P_HCO', 2012, 0.07106111],
        ]

        expected = pd.DataFrame(data=data, columns=['REGION', 'TIMESLICE', 'TECHNOLOGY', 'FUEL', 'YEAR', 'VALUE'])

        index = ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'FUEL', 'YEAR']

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)
    
class TestEnergy:

    def test_filter_primary_energy(self):
        filepath = os.path.join("test","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['******I**']
        actual = filter_primary_energy(input_data, technologies)

        data = [
            [],
            []
        ]