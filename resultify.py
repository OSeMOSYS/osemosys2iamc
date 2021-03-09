import pandas as pd
import pyam
import sys
import os
from typing import List, Dict
from yaml import load, SafeLoader

def read_file(filename: str) -> pd.DataFrame:

    df = pd.read_csv(filename)

    return df

def filter_fuel(df: pd.DataFrame, technologies: List, fuels: List) -> pd.DataFrame:

    mask = df.TECHNOLOGY.isin(technologies)
    fuel_mask = df.FUEL.isin(fuels)

    return df[mask & fuel_mask]

def extract_results(df: pd.DataFrame, technologies: List) -> pd.DataFrame:

    mask = df.TECHNOLOGY.isin(technologies)

    return df[mask]

def aggregate_results(data: pd.DataFrame):

    return data.groupby(by=['REGION', 'YEAR']).sum()

def make_iamc(data: pd.DataFrame,
              iam_model,
              iam_scenario,
              iam_region,
              iam_variable,
              iam_unit
              ) -> pyam.IamDataFrame:
    data = data.reset_index()
    # Add required columns
    data['REGION'] = iam_region
    data = data.rename(columns={
        'REGION': 'region',
        'YEAR': 'year'
    })
    data['model'] = iam_model
    data['scenario'] = iam_scenario
    data['variable'] = iam_variable
    data['unit'] = iam_unit

    iamc = pyam.IamDataFrame(data)
    return iamc

def load_config(filepath: str) -> Dict:
    with open(filepath, 'r') as configfile:
        config = load(configfile, Loader=SafeLoader)
    return config

def main(infilename, technames: List, outfilename):

    results = read_file(infilename)

    if isinstance(technames, str):
        technologies = [x.strip() for x in technames.split(",")]
    elif isinstance(technologies, list):
        technologies = technames
    else:
        raise TypeError("Argument is not a list or string")

    data = extract_results(results, technologies)

    aggregated = aggregate_results(data)

    iamc = make_iamc(aggregated)

    iamc.to_csv(outfilename)

if __name__ == "__main__":

    args = sys.argv[1:]

    results_path = args[0]
    configpath = args[1]
    outpath = args[2]

    config = load_config(configpath)

    blob = []

    for result in config['results']:

        inpathname = os.path.join(results_path, result['osemosys_param'] + '.csv')
        results = read_file(inpathname)

        technologies = [x['name'] for x in result['technology']]
        units = [x['unit'] for x in result['technology']]
        data = extract_results(results, technologies)
        aggregated = aggregate_results(data)

        if len(set(units)) != 1:
            msg = "osemosys2iamc does not yet support technology specific units. Found {} in '{}'"
            raise ValueError(msg.format(", ".join(list(set(units))), result['iamc_variable']))

        iamc = make_iamc(aggregated, config['model'], config['scenario'], 'World', result['iamc_variable'], units[0])
        blob.append(iamc)

    pyam.concat(blob).to_csv(outpath)
