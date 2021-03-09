import pandas as pd
import os
from .resultify import filter_fuel

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