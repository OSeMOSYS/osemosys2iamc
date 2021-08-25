import pandas as pd
import pyam
import sys
import os
from typing import List, Dict, Union
from yaml import load, SafeLoader
import matplotlib.pyplot as plt


def read_file(filename) -> pd.DataFrame:

    df = pd.read_csv(filename)

    return df

def filter_fuel(df: pd.DataFrame, technologies: List, fuels: List) -> pd.DataFrame:

    mask = df.TECHNOLOGY.isin(technologies)
    fuel_mask = df.FUEL.isin(fuels)

    return df[mask & fuel_mask]

def filter_emission(df: pd.DataFrame, emission: List) -> pd.DataFrame:
    """Extracts just rows which match contents of ``emission`` and fill region name from technology column
    """

    mask = df.EMISSION.isin(emission)

    df['REGION'] = df['TECHNOLOGY'].str[0:2]
    df = df.drop(columns='TECHNOLOGY')

    return df[mask]

def extract_results(df: pd.DataFrame, technologies: List) -> pd.DataFrame:

    mask = df.TECHNOLOGY.isin(technologies)

    return df[mask]

def aggregate_results(data: pd.DataFrame):
    """Sums rows while grouping regions and years
    """

    return data.groupby(by=['REGION', 'YEAR']).sum()

def make_iamc(data: pd.DataFrame,
              iam_model: str,
              iam_scenario: str,
              iam_variable: str,
              iam_unit: str
              ) -> pyam.IamDataFrame:
    """Creates an IAM Dataframe from raw data

    Arguments
    ---------
    data: pd.DataFrame
        Contains columns for region, year and value
    iam_model: str
        The model name to insert into the IAMC dataframe
    iam_scenario: str
        The scenario name to insert into the IAMC dataframe
    iam_variable: str
        The IAMC variable name to insert into the IAMC dataframe
    iam_unit: str
        The unit to insert into the IAMC dataframe

    """
    data = data.reset_index()
    data = data.rename(columns={
        'REGION': 'region',
        'YEAR': 'year'
    })
    # Add required columns
    data['model'] = iam_model
    data['scenario'] = iam_scenario
    data['variable'] = iam_variable
    data['unit'] = iam_unit

    iamc = pyam.IamDataFrame(data)
    return iamc

def load_config(filepath: str) -> Dict:
    """Reads the configuration file
    """
    with open(filepath, 'r') as configfile:
        config = load(configfile, Loader=SafeLoader)
    return config

def make_plots(df, model, scenario):
    """Creates standard plots
    """

    args = dict(model=model, scenario=scenario)
    print(args)

    # Plot primary energy
    fig, ax = plt.subplots()
    pe = df.filter(**args, variable='Primary Energy|*', region='World')
    if pe:
        pe.plot.bar(ax=ax, stacked=True, title='Primary energy mix')
        plt.legend(loc=1)
        plt.tight_layout()
        fig.savefig('primary_energy.pdf', bbox_inches='tight', transparent=True, pad_inches=0)

    # Create generation capacity plot
    fig, ax = plt.subplots()
    cap = df.filter(**args, variable='Capacity|*', region='World')
    if cap:
        cap.plot.bar(ax=ax, stacked=True, title='Generation Capacity')
        plt.legend(loc=1)
        plt.tight_layout()
        fig.savefig('capacity.pdf', bbox_inches='tight', transparent=True, pad_inches=0)

    # Create emissions plot
    emi = df.filter(**args, variable="Emissions|CO2*").filter(region="World", keep=False)
    print(emi)
    if emi:
        fig, ax = plt.subplots()
        emi.plot.bar(ax=ax,
            bars="region", stacked=True, title="CO2 emissions by region", cmap="tab20"
            )
        plt.legend(loc=1)
        fig.savefig('emission.pdf', bbox_inches='tight', transparent=True, pad_inches=0)



def main(config: Dict) -> pyam.IamDataFrame:
    """
    """
    blob = []
    for result in config['results']:

        inpathname = os.path.join(results_path, result['osemosys_param'] + '.csv')
        results = read_file(inpathname)

        try:
            technologies = result['technology']
        except KeyError:
            pass
        unit = result['unit']
        if 'fuel' in result.keys():
            fuels = result['fuel']
            data = filter_fuel(results, technologies, fuels)
        elif 'emission' in result.keys():
            emission = result['emission']
            data = filter_emission(results, emission)
        else:
            data = extract_results(results, technologies)
        aggregated = aggregate_results(data)

        iamc = make_iamc(aggregated, config['model'], config['scenario'], result['iamc_variable'], unit)
        blob.append(iamc)

    all_data = pyam.concat(blob)
    return all_data

if __name__ == "__main__":

    args = sys.argv[1:]

    if len(args) != 3:
        print("Usage: python resultify.py <results_path> <config_path> <output_path>")
        exit(1)

    results_path = args[0]
    configpath = args[1]
    outpath = args[2]

    config = load_config(configpath)

    all_data = main(config)
    all_data.to_csv(outpath)

    model = config['model']
    scenario = config['scenario']
    make_plots(all_data, model, scenario)
