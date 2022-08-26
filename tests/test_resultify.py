from datetime import date
import pandas as pd
import os
import pytest
from osemosys2iamc.resultify import (filter_fuel,
                                     filter_emission_tech,
                                     filter_final_energy,
                                     filter_capacity,
                                     calculate_trade)


class TestTrade:

    def test_trade(self):

        use = [
            ['REGION1','ID','ATBM00X00','ATBM', 2014, 5.0],
            ['REGION1','ID','ATBM00X00','ATBM', 2015, 5.0],
            ]

        production = [
            ['REGION1','ATBM00X00','ATBM', 2015, 10.0],
            ['REGION1','ATBM00X00','ATBM', 2016, 10.0],
        ]

        results = {
            'UseByTechnology': pd.DataFrame(
                data = use,
                columns = ['REGION','TIMESLICE','TECHNOLOGY','FUEL','YEAR','VALUE']
            ),
            'ProductionByTechnologyAnnual': pd.DataFrame(
                data = production,
                columns=['REGION','TECHNOLOGY','FUEL','YEAR','VALUE'])
        }

        techs = ['ATBM00X00']

        actual = calculate_trade(results, techs)

        expected_data = [
            ['AT',2014,  5.0],
            ['AT',2015, -5.0],
            ['AT',2016, -10.0],
        ]

        expected = pd.DataFrame(expected_data, columns=['REGION', 'YEAR', 'VALUE'])
        pd.testing.assert_frame_equal(actual, expected)


class TestEmissions:

    def test_filter_emission(self):

        filepath = os.path.join("tests", 'fixtures', "AnnualTechnologyEmissions.csv")
        input_data = pd.read_csv(filepath)

        emission = ['CO2']
        actual = filter_emission_tech(input_data, emission)

        data = [
            ["AT", 2026, -6244.862561],
            ["AT", 2027, -6529.532083],
            ["AT", 2030,  3043.148835],
            ["AT", 2031,  2189.064681],
            ["AT", 2032,  2315.821267],
            ["BE", 2026, -2244.982800],
            ["BE", 2027, -6746.886437],
            ["BG", 2030, 11096.556931],
            ["BG", 2031, 11069.257141],
            ["BG", 2032, 11041.957354]
        ]

        expected = pd.DataFrame(
            data=data,
            columns=['REGION', 'YEAR', 'VALUE'])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_tech_emission(self):

        filepath = os.path.join("tests", 'fixtures', "AnnualTechnologyEmissions.csv")
        input_data = pd.read_csv(filepath)

        tech = ['(?=^.{2}(BM))^.{4}(CS)']
        emission = ['CO2']
        actual = filter_emission_tech(input_data, emission, tech)

        data = [
            ['AT', 2026, -7573.069442598169],
            ['AT', 2027, -7766.777427515737],
            ['BE', 2026, -2244.98280006968],
            ['BE', 2027, -6746.886436926597],
        ]

        expected = pd.DataFrame(
            data=data,
            columns=['REGION', 'YEAR', 'VALUE'])
        print(actual)
        print(expected)
        pd.testing.assert_frame_equal(actual, expected)

class TestFilter:

    def test_filter_fuel(self):
        filepath = os.path.join("tests", 'fixtures', "UseByTechnology.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['ALUPLANT']
        fuels = ['C1_P_HCO']
        actual = filter_fuel(input_data, technologies, fuels)

        data = [
            ["Globe",  2010,  0.828098],
            ["Globe",  2011,  0.825347],
            ["Globe",  2012,  0.852052]
        ]
        expected = pd.DataFrame(data=data,
            columns=['REGION', 'YEAR', 'VALUE'])

        print(actual, type(actual))
        print(expected, type(expected))

        pd.testing.assert_frame_equal(actual, expected)

class TestEnergy:

    def test_filter_capacity(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['^.{6}(I0)','^.{6}(X0)','^.{2}(HY)','^.{2}(OC)','^.{2}(SO)','^.{2}(WI)']
        actual = filter_capacity(input_data, technologies)

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

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_bm(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['(?=^.{2}(BM))^.{4}(00)','(?=^.{2}(WS))^.{4}(00)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['AT',2015,26.324108350683794],
            ['AT',2016,26.324108350683794],
            ['AT',2017,26.324108350683794],
            ['AT',2018,26.324108350683787],
            ['AT',2019,26.324108350683794],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_co(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['(?=^.{2}(CO))^.{4}(00)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['CH',2047,69.9750212433476],
            ['CH',2048,91.45662886581975],
            ['CH',2049,76.86770297185006],
            ['CH',2050,70.86078033897608],
            ['CH',2051,53.88447040760964],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_ng(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['(?=^.{2}(NG))^.{4}(00)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['BE',2016,141.0],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_go(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['(?=^.{2}(GO))^.{4}(00)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['BG',2015,1.423512],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])
        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_hy(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['^.{2}(HY)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['CZ',2015,3.3637616987287244],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])
        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_nu(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['^.{2}(UR)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['CZ',2015,326.2313192401038],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])
        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_oc(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['^.{2}(OC)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['DK',2015,0.0031536000000000003],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_oi(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['(?=^.{2}(OI))^.{4}(00)','(?=^.{2}(HF))^.{4}(00)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['EE',2015,28.512107999999998],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_so(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['^.{2}(SO)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['ES',2015,26.75595496070811],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_wi(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['^.{2}(WI)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['FI', 2015, 0.29658110158442175],
            ['FR', 2015, 72.25974845531343]
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_secondary_bm(self):
        filepath = os.path.join("tests","fixtures","ProductionByTechnologyAnnual.csv")
        input_data = pd.read_csv(filepath)

        technologies = ['(?=^.{2}(BF))^((?!00).)*$','(?=^.{2}(BM))^((?!00).)*$', '(?=^.{2}(WS))^((?!00).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['AT', 2042, 0.6636346353894057],
            ['AT', 2043, 1.3300518531620575],
            ['AT', 2044, 1.9992691432067637],
            ['AT', 2045, 2.6713041901899794],
            ['AT', 2046, 3.4778527409137996]
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

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

        print(actual)
        print(expected)

        pd.testing.assert_frame_equal(actual, expected)

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

        print(actual)

        print(expected)

        pd.testing.assert_frame_equal(actual, expected)

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

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_coal(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['(?=^.{2}(CO))^((?!00).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['BG',2015,4.141],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_gas(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['(?=^.{2}(NG))^((?!00).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['DE',2015,9.62143],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_geo(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['(?=^.{2}(GO))^((?!00).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['CH',2026,0.004563975391582646],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_hydro(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['^.{2}(HY)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['CZ',2015,0.299709],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_nuclear(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['^.{2}(NU)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['ES',2015,7.7308],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_ocean(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['^.{2}(OC)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['DK',2015,0.0005],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_oil(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['(?=^.{2}(HF))^((?!00).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['CY',2015,0.3904880555817921],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_solar(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['^.{2}(SO)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['EE',2015,0.006],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_wi_offshore(self):
        filepath = os.path.join("tests","fixtures","TotalCapacityAnnual.csv")
        input_data = pd.read_csv(filepath)
        technologies = ['(?=^.{2}(WI))^.{4}(OF)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['FI',2015,0.0263],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

class TestPrice:

    def test_price_bm(self):
        filepath = os.path.join("tests","fixtures","VariableCost.csv")
        input_data = pd.read_csv(filepath)
        commodity = ['(?=^.{2}(BM))^.{6}(X0)']
        actual = filter_capacity(input_data, commodity)

        data = [
            ['AT',2015,3.0],
            ['AT',2016,4.0],
            ['BE',2015,1.7],
            ['BE',2016,1.8],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        print(actual)
        print(expected)

        pd.testing.assert_frame_equal(actual, expected)
