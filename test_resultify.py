import pandas as pd
import os
import pytest
from .resultify import filter_fuel, filter_emission, filter_primary_energy, filter_final_energy, filter_capacity


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
            ['BE', 2016, 141.0],
            ['BG', 2015, 1.423512],
            ['CH', 2047, 69.9750212433476],
            ['CH', 2048, 91.45662886581975],
            ['CH', 2049, 76.86770297185006],
            ['CH', 2050, 70.86078033897608],
            ['CH', 2051, 53.88447040760964],
            ['CZ', 2015, 329.5950809],
            ['DK', 2015, 0.0031536],
            ['EE', 2015, 28.512108],
            ['ES', 2015, 26.75595496],
            ['FI', 2015, 0.296581102],
            ['FR', 2015, 72.25974846],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_primary_bm(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['(?=^.{2}(BM))^.{4}(00)','(?=^.{2}(WS))^.{4}(00)']
        actual = filter_primary_energy(input_data, technologies)

        data = [
            ['AT',2015,26.324108350683794],
            ['AT',2016,26.324108350683794],
            ['AT',2017,26.324108350683794],
            ['AT',2018,26.324108350683787],
            ['AT',2019,26.324108350683794],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_primary_co(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['(?=^.{2}(CO))^.{4}(00)']
        actual = filter_primary_energy(input_data, technologies)

        data = [
            ['CH',2047,69.9750212433476],
            ['CH',2048,91.45662886581975],
            ['CH',2049,76.86770297185006],
            ['CH',2050,70.86078033897608],
            ['CH',2051,53.88447040760964],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)
    
    def test_filter_primary_ng(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['(?=^.{2}(NG))^.{4}(00)']
        actual = filter_primary_energy(input_data, technologies)

        data = [
            ['BE',2016,141.0],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_primary_go(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['(?=^.{2}(GO))^.{4}(00)']
        actual = filter_primary_energy(input_data, technologies)

        data = [
            ['BG',2015,1.423512],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_primary_hy(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['^.{2}(HY)']
        actual = filter_primary_energy(input_data, technologies)

        data = [
            ['CZ',2015,3.3637616987287244],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_primary_nu(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['^.{2}(UR)']
        actual = filter_primary_energy(input_data, technologies)

        data = [
            ['CZ',2015,326.2313192401038],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_primary_oc(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['^.{2}(OC)']
        actual = filter_primary_energy(input_data, technologies)

        data = [
            ['DK',2015,0.0031536000000000003],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_primary_oi(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['(?=^.{2}(OI))^.{4}(00)','(?=^.{2}(HF))^.{4}(00)']
        actual = filter_primary_energy(input_data, technologies)

        data = [
            ['EE',2015,28.512107999999998],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_primary_so(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['^.{2}(SO)']
        actual = filter_primary_energy(input_data, technologies)

        data = [
            ['ES',2015,26.75595496070811],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_primary_wi(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['^.{2}(WI)']
        actual = filter_primary_energy(input_data, technologies)

        data = [
            ['FI', 2015, 0.29658110158442175],
            ['FR', 2015, 72.25974845531343]
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

class TestCapacity:

    def test_filter_inst_capacity(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['^((?!(EL)|(00)).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['AT',2015,0.446776],
            ['BE',2016,0.184866],
            ['BG',2015,4.141],
            ['CH',2026,0.004563975391582646],
            ['CY',2015,0.3904880555817921],
            ['CZ',2015,0.299709],
            ['DE',2015,9.62143],
            ['DK',2015,0.0005],
            ['EE',2015,0.006],
            ['ES',2015,7.7308],
            ['FI',2015,0.0263],
            ['FR',2015,0.47835],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)
    
    def test_filter_inst_capacity_bio(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['(?=^.{2}(BF))^((?!00).)*$','(?=^.{2}(BM))^((?!00).)*$', '(?=^.{2}(WS))^((?!00).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['AT',2015,0.446776],
            ['BE',2016,0.184866],
            ['FR', 2015, 0.47835],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_inst_capacity_coal(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['(?=^.{2}(CO))^((?!00).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['BG',2015,4.141],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_inst_capacity_gas(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['(?=^.{2}(NG))^((?!00).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['DE',2015,9.62143],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_inst_capacity_geo(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['(?=^.{2}(GO))^((?!00).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['CH',2026,0.004563975391582646],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_inst_capacity_hydro(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['^.{2}(HY)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['CZ',2015,0.299709],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_inst_capacity_nuclear(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['^.{2}(NU)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['ES',2015,7.7308],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_inst_capacity_ocean(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['^.{2}(OC)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['DK',2015,0.0005],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_inst_capacity_oil(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['(?=^.{2}(HF))^((?!00).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['CY',2015,0.3904880555817921],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_inst_capacity_solar(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['^.{2}(SO)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['EE',2015,0.006],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)

    def test_filter_inst_capacity_wi_offshore(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['(?=^.{2}(WI))^.{4}(OF)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['FI',2015,0.0263],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        index = ["REGION", "YEAR"]

        pd.testing.assert_frame_equal(actual.set_index(index), expected.set_index(index), check_index_type=False)