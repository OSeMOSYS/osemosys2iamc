import pandas as pd
import os
import pytest
from .resultify import filter_fuel, filter_emission, filter_primary_energy, filter_final_energy


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
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['^.{6}(I0)','^.{6}(X0)','^.{2}(HY)','^.{2}(OC)','^.{2}(SO)','^.{2}(WI)']
        actual = filter_primary_energy(input_data, technologies)

        data = [
            ['AT', 2015, 26.324108350683794],
            ['AT', 2016, 26.324108350683794],
            ['AT', 2017, 26.324108350683794],
            ['AT', 2018, 26.324108350683787],
            ['AT', 2019, 26.324108350683794],
            ['CH', 2047, 69.9750212433476],
            ['CH', 2048, 91.45662886581975],
            ['CH', 2049, 76.86770297185006],
            ['CH', 2050, 70.86078033897608],
            ['CH', 2051, 53.88447040760964],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)
    
    def test_filter_final_energy(self):
        filepath = os.path.join("tests","fixtures","Demand.csv")
        input_data = pd.read_csv(filepath)

        fuels = ['E2']
        actual = filter_final_energy(input_data, fuels)

        data = [
            ['AT',2015,227.5944502],
            ['BE',2016,296.0570016],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_fuels_format_wrong(self):
        filepath = os.path.join("tests","fixtures","Demand.csv")
        input_data = pd.read_csv(filepath)
        fuels = ['ELE']
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            filter_final_energy(input_data, fuels)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1