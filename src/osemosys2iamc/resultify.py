"""Create an IAMC dataset from a package of OSeMOSYS results

Run the command::

    python resultify.py <input_path> <results_path> <config_path> <output_path>"

where:

    ``input_path`` is the path to the folder of CSV files containing input files
    ``results_path`` is the path to the folder of CSV files holding OSeMOSYS results
    ``config_path`` is the path to the ``config.yaml`` file containing the results mapping
    ``output_path`` is the path to the csv file written out in IAMC format

"""
import functools
from multiprocessing.sharedctypes import Value
from sqlite3 import DatabaseError
import pandas as pd
import pyam
from openentrance import iso_mapping
import sys
import os
from typing import List, Dict, Optional
from yaml import load, SafeLoader
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def read_file(filename) -> pd.DataFrame:

    df = pd.read_csv(filename)

    return df

def filter_regex(df: pd.DataFrame, patterns: List[str], column: str) -> pd.DataFrame:
    """Generic filtering of rows based on columns that match a list of patterns

    This function returns the rows where the values in a ``column`` match the
    list of regular expression ``patterns``
    """
    masks = [df[column].str.match(p) for p in patterns]
    return pd.concat([df[mask] for mask in masks])

def filter_fuels(df: pd.DataFrame, fuels: List[str]) -> pd.DataFrame:
    """Returns rows which match list of regex patterns in ``technologies``

    Parameters
    ----------
    df: pd.DataFrame
        The input data
    fuels: List[str]
        List of regex patterns
    """
    return filter_regex(df, fuels, 'FUEL')

def filter_technologies(df: pd.DataFrame, technologies: List[str]) -> pd.DataFrame:
    """Returns rows which match list of regex patterns in ``technologies``

    Parameters
    ----------
    df: pd.DataFrame
        The input data
    technologies: List[str]
        List of regex patterns
    """
    return filter_regex(df, technologies, 'TECHNOLOGY')

def filter_technology_fuel(df: pd.DataFrame, technologies: List, fuels: List) -> pd.DataFrame:
    """Return rows which match ``technologies`` and ``fuels``
    """
    df = filter_technologies(df, technologies)
    df = filter_fuels(df, fuels)

    df = df.groupby(by=['REGION','YEAR'], as_index=False)["VALUE"].sum()
    return df[df.VALUE != 0]

def filter_emission_tech(df: pd.DataFrame, emission: List[str], technologies: Optional[List[str]]=None) -> pd.DataFrame:
    """Return annual emissions or captured emissions by one or several technologies.

    Parameters
    ----------
    df: pd.DataFrame
    emission: List[str]
        List of regex patterns
    technologies: List[str], default=None
        List of regex patterns

    Returns
    -------
    pandas.DataFrame
    """

    df['REGION'] = df['TECHNOLOGY'].str[:2]
    df = filter_regex(df, emission, 'EMISSION')

    if technologies:
    # Create a list of masks, one for each row that matches the pattern listed in ``tech``
        df = filter_technologies(df, technologies)

    df = df.groupby(by=['REGION','YEAR'], as_index=False)["VALUE"].sum()
    return df[df.VALUE != 0]

def filter_capacity(df: pd.DataFrame, technologies: List[str]) -> pd.DataFrame:
    """Return aggregated rows filtered on technology column.

    Parameters
    ----------
    df: pd.DataFrame
        The input data
    technologies: List[str]
        List of regex patterns

    Returns
    -------
    pandas.DataFrame
    """
    df['REGION'] = df['TECHNOLOGY'].str[:2]
    df = filter_technologies(df, technologies)

    df = df.groupby(by=['REGION','YEAR'], as_index=False)["VALUE"].sum()
    return df[df.VALUE != 0]

def filter_final_energy(df: pd.DataFrame, fuels: List) -> pd.DataFrame:
    """Return dataframe that indicate the final energy demand/use per country and year.
    """
    for f in fuels:
        if len(f)!=2:
            print("Fuel %s from config.yaml doesn't comply with expected format." % f)
            exit(1)

    df['REGION'] = df['FUEL'].str[:2]

    df['FUEL'] = df['FUEL'].str[2:]
    df_f = filter_fuels(df, fuels)

    df = df_f.groupby(by=['REGION','YEAR'], as_index=False)["VALUE"].sum()
    return df[df.VALUE != 0]

def calculate_trade(results: dict, techs: List) -> pd.DataFrame:
    """Return dataframe with the net exports of a commodity
    """

    exports = filter_capacity(results['UseByTechnology'], techs).set_index(['REGION', 'YEAR'])
    imports = filter_capacity(results['ProductionByTechnologyAnnual'], techs).set_index(['REGION', 'YEAR'])
    df = exports.subtract(imports, fill_value=0)

    return df.reset_index()

def extract_results(df: pd.DataFrame, technologies: List) -> pd.DataFrame:
    """Return rows which match ``technologies``
    """

    mask = df.TECHNOLOGY.isin(technologies)

    return df[mask]


def load_config(filepath: str) -> Dict:
    """Reads the configuration file

    Arguments
    ---------
    filepath : str
        The path to the config file
    """
    with open(filepath, 'r') as configfile:
        config = load(configfile, Loader=SafeLoader)
    return config

def make_plots(df: pyam.IamDataFrame, model: str, scenario: str, regions: List[str]):
    """Creates standard plots

    Arguments
    ---------
    model: str
    scenario: str
    """

    # df = all_data #for testing
    # model = config['model'] #for testing
    # scenario = config['scenario'] #for testing
    # regions = config['region']#for testing

    args = dict(model=model, scenario=scenario)
    print(args, regions)

    fig, ax = plt.subplots()

    assert isinstance(regions, list)

    for region in regions:
        assert isinstance(region, str)
        print(f"Plotting {region}")
        # Plot primary energy
        data = df.filter(**args, variable='Primary Energy|*', region=region) # type: pyam.IamDataFrame
        if data:
            print(data)
            locator = mdates.AutoDateLocator(minticks=10)
            #locator.intervald['YEARLY'] = [10]
            data.plot.bar(ax=ax, stacked=True, title='Primary energy mix %s' % region)
            plt.legend(bbox_to_anchor=(0.,-0.5), loc='upper left')
            plt.tight_layout()
            ax.xaxis.set_major_locator(locator)
            fig.savefig('primary_energy_%s.pdf' % region, bbox_inches='tight', transparent=True, pad_inches=0)
            plt.clf()
        # Plot secondary energy (electricity generation)
        se = df.filter(**args, variable='Secondary Energy|Electricity|*', region=region)
        if se:
            locator = mdates.AutoDateLocator(minticks=10)
            #locator.intervald['YEARLY'] = [10]
            pe.plot.bar(ax=ax, stacked=True, title='Power generation mix %s' % region)
            plt.legend(bbox_to_anchor=(0.,-0.5), loc='upper left')
            plt.tight_layout()
            ax.xaxis.set_major_locator(locator)
            fig.savefig('electricity_generation_%s.pdf' % region, bbox_inches='tight', transparent=True, pad_inches=0)
            plt.clf()
        # Create generation capacity plot
        cap = df.filter(**args, variable='Capacity|Electricity|*', region=region)
        if cap:
            cap.plot.bar(ax=ax, stacked=True, title='Generation Capacity %s' % region)
            plt.legend(bbox_to_anchor=(0.,-0.25),loc='upper left')
            plt.tight_layout()
            fig.savefig('capacity_%s.pdf' % region, bbox_inches='tight', transparent=True, pad_inches=0)
            plt.clf()

    # Create emissions plot
    emi = df.filter(**args, variable="Emissions|CO2*").filter(region="World", keep=False)
    # print(emi)
    if emi:
        emi.plot.bar(ax=ax,
            bars="region", stacked=True, title="CO2 emissions by region", cmap="tab20"
            )
        plt.legend(bbox_to_anchor=(1.,1.05),loc='upper left', ncol=2)
        fig.savefig('emission.pdf', bbox_inches='tight', transparent=True, pad_inches=0)
        plt.clf()


def main(config: Dict, inputs_path: str, results_path: str) -> pyam.IamDataFrame:
    """Create the IAM data frame from results

    Loops over each entry in the configuration file, extracts the data from
    the relevant result file and puts this into the IAMC data format

    Arguments
    ---------
    config : dict
        The configuration dictionary
    inputs_path: str
        Path to a folder of csv files (OSeMOSYS inputs)
    results_path: str
        Path to a folder of csv files (OSeMOSYS results)
    """
    blob = []
    try:
        for input in config['inputs']:

            inpathname = os.path.join(inputs_path, input['osemosys_param'] + '.csv')
            inputs = read_file(inpathname)

            unit = input['unit']

            technologies = input['variable_cost']
            data = filter_capacity(inputs, technologies)

            if not data.empty:
                data = data.rename(columns={'REGION': 'region',
                                            'YEAR': 'year',
                                            'VALUE': 'value'})
                iamc = pyam.IamDataFrame(
                    data,
                    model=config['model'],
                    scenario=config['scenario'],
                    variable=input['iamc_variable'],
                    unit=unit)
                blob.append(iamc)
    except KeyError:
        pass

    try:
        for result in config['results']:

            if type(result['osemosys_param']) == str:
                path_name = os.path.join(results_path, result['osemosys_param'] + '.csv')
                results = read_file(path_name)

                try:
                    technologies = result['technology']
                except KeyError:
                    pass
                unit = result['unit']
                if 'fuel' in result.keys():
                    fuels = result['fuel']
                    data = filter_technology_fuel(results, technologies, fuels)
                elif 'emissions' in result.keys():
                    if 'tech_emi' in result.keys():
                        emission = result['emissions']
                        technologies = result['tech_emi']
                        data = filter_emission_tech(results, emission, technologies)
                    else:
                        emission = result['emissions']
                        data = filter_emission_tech(results, emission)
                elif 'capacity' in result.keys():
                    technologies = result['capacity']
                    data = filter_capacity(results, technologies)
                elif 'primary_technology' in result.keys():
                    technologies = result['primary_technology']
                    data = filter_capacity(results, technologies)
                elif 'excluded_prod_tech' in result.keys():
                    technologies = result['excluded_prod_tech']
                    data = filter_capacity(results, technologies)
                elif 'el_prod_technology' in result.keys():
                    technologies = result['el_prod_technology']
                    data = filter_capacity(results, technologies)
                elif 'demand' in result.keys():
                    demands = result['demand']
                    data = filter_final_energy(results, demands)
                else:
                    data = extract_results(results, technologies)

            else:
                results = {}
                for p in result['osemosys_param']:
                    path_name = os.path.join(results_path, p + '.csv')
                    results[p] = read_file(path_name)
                if 'trade_tech' in result.keys():
                    technologies = result['trade_tech']
                    data = calculate_trade(results, technologies)

            if 'transform' in result.keys():
                if result['transform'] == 'abs':
                    data['VALUE'] = data['VALUE'].abs()
                else:
                    pass

            if not data.empty:
                data = data.rename(columns={'REGION': 'region',
                                            'YEAR': 'year',
                                            'VALUE': 'value'})
                # print(data)
                iamc = pyam.IamDataFrame(
                    data,
                    model=config['model'],
                    scenario=config['scenario'],
                    variable=result['iamc_variable'],
                    unit=unit)
                blob.append(iamc)
    except KeyError:
        pass

    all_data = pyam.concat(blob)

    all_data = all_data.convert_unit('PJ/yr', to='EJ/yr')
    all_data = all_data.convert_unit('ktCO2/yr', to='Mt CO2/yr', factor=0.001)
    all_data = all_data.convert_unit('MEUR_2015/PJ', to='EUR_2020/GJ', factor=1.05)
    all_data = all_data.convert_unit('kt CO2/yr', to='Mt CO2/yr')

    if iso_mapping is not None:
        data = all_data.timeseries()
        data.index = data.index.set_levels(data.index.levels[2].map(iso_mapping), level=2)
        all_data = pyam.IamDataFrame(data)
    else:
        msg = "Please ensure that the openentrance package is installed as an editable library " \
              "See https://github.com/openENTRANCE/openentrance/issues/202"
        raise ValueError(msg)

    all_data = pyam.IamDataFrame(all_data)
    return all_data


def aggregate(func):
    """Decorator for filters which returns the aggregated data

    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the dataframe from the filter
        data = func(*args, **kwargs)
        # Apply the aggregation
        data = data.groupby(by=['REGION', 'YEAR']).sum()
        # Make the IAMDataFrame
        return pyam.IamDataFrame(
            data,
            model=iam_model,
            scenario=iam_scenario,
            variable=iam_variable,
            unit=iam_unit)
    return wrapper

def entry_point():

    args = sys.argv[1:]

    if len(args) != 4:
        print("Usage: osemosys2iamc <inputs_path> <results_path> <config_path> <output_path>")
        exit(1)

    inputs_path = args[0]
    results_path = args[1]
    configpath = args[2]
    outpath = args[3]

    config = load_config(configpath)

    all_data = main(config, inputs_path, results_path)

    model = config['model']
    scenario = config['scenario']
    regions = config['region']

    # Plotting fail reported in [issue 25](https://github.com/OSeMOSYS/osemosys2iamc/issues/25)
    # make_plots(all_data, model, scenario, regions)

    all_data.to_excel(outpath, sheet_name='data')


if __name__ == "__main__":

    entry_point()
