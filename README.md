# osemosys2iamc

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7473185.svg)](https://doi.org/10.5281/zenodo.7473185)

Use this Python package to convert OSeMOSYS results to the IAMC format

## Acknowledgements

This work was financially supported by:

- The [European Climate and Energy Modelling Forum (ECEMF)](https://doi.org/10.3030/101022622) has received funding from the European Union’s Horizon 2020 Research and Innovation programme under the grant agreement No 101022622
- The [IAM COMPACT](https://doi.org/10.3030/101056306) project has received funding from the European Union’s HORIZON EUROPE Research and Innovation Programme under grant agreement No 101056306

<img
  src="docs/images/ecemf.png"
  alt="European Climate and Energy Modelling Forum Logo"
  style="display: inline-block; margin: 100 auto; height: 100px"><img
  src="docs/images/iamcompact.png"
  alt="IAM COMPACT Logo"
  style="display: inline-block; margin: 100 auto; height: 100px">

## Install from Python Packaging Index (PyPI)

    pip install osemosys2iamc

## Run the package

    $ osemosys2iamc --help
    osemosys2iamc <inputs_path> <results_path> <config_path> <output_path>

`inputs_path`: Path to a folder of csv files (OSeMOSYS inputs). File names should correspond to OSeMOSYS parameter names.
`results_path`: Path to a folder of csv files (OSeMOSYS results). File names should correspond to OSeMOSYS variable names.
`config_path`: Path to the configuration file (see below)
`output_path`: Path to the .xlsx file you wish to write out

## The IAMC format

The IAMC format was developed by the [Integrated Assessment Modeling Consortium (IAMC)](https://www.iamconsortium.org/)
and is used in many model comparison projects at the global and national level.
It can be used for integrated-assessment models, energy-systems scenarios
and analysis of specific sectors like transport, industry or buildings.

The format is a tabular structure with the columns *model*, *scenario*, *region*,
*variable*, *unit*, and a time domain. Each project defines "codelists"
to be used across modelling teams for comparison and analysis of results.

The most recent high-profile application of the IAMC format is the [AR6 Scenario Explorer](https://data.ece.iiasa.ac.at/ar6)
hosting the scenario ensemble supporting the quantitative assessment
in the contribution by Working Group III to the IPCC's Sixth Assessment Report (AR6).

Please refer to the Horizon 2020 project [openENTRANCE](https://github.com/openENTRANCE/openentrance#data-format-structure)
for more information about the format and its usage in that project.

## Writing a configuration file

Write a configuration file in YAML format. A simple configuration file with two result variables looks like this:

```yaml
model: OSeMBE v1.0.0
scenario: DIAG-C400-lin-ResidualFossil
region: iso2_x, iso3_x, from_csv, or a name of a country/region [substitute x with start, end, or a positive number]
results:
- iamc_variable: 'Carbon Capture|Biomass'
  tech_emi: ['(?=^.{2}(BM))^.{4}(CS)']
  emissions: [CO2]
  unit: kt CO2/yr
  transform: abs
  osemosys_param: AnnualTechnologyEmission
- iamc_variable: 'Capital Investment'
  capacity: ['^.*$']
  unit: MUSD
  osemosys_param: CapitalInvestment
```

The first section of the configuration file with the keys `model`, `scenario`, and `region` are used to define the metadata for
the IAMC template.

`model` and `scenario` are user-defined, taking any word or phrase and having no set format. `region` may be defined using 4 methods:

* `iso2_x` - using the ISO 3166-1 alpha-2 country codes located in the names of technologies/fuels/emissions (depending on the file) at the location given by the user.\*
* `iso3_x` - using the ISO 3166-1 alpha-3 country codes located in the names of technologies/fuels/emissions (depending on the file) at the location given by the user.\*
* `from_csv` - using the region as defined in the REGION column of the CSV file
* Any other word or phrase the user defines (other than an invalid iso option) will be used as the region for all variables. eg. Austria, Nepal, Ethiopia, Guyana, etc.

The `x` in the above ISO options is to be replaced by:
* `start`, if the codes are at the beginning of the names
* `end`, if the codes are at the end of the names, or
* a positive number indicating the position of the first letter of the code in the name. eg. iso2_5 will target the 'GH' in 'POWRGHSOL'

The second section, `results`, is where you describe each of the IAMC variables and provide instructions to osemosys2iamc on how
to compute the values.

`iamc_variable` - this should match one of the IAMC variable names
`unit` - provide the units of the OSeMOSYS results
`transform` - only `abs` is currently available. This returns the absolute value of the results
`osemosys_param` - provide the name of the result file from which the script should extract the result data

One or more of the following filter keys. These filter the
results by one or more columns found in OSeMOSYS results.
Following the fitering, the remaining columns except region
 and year are discarded and rows are summed.

`tech_emi` - filter the results by TECHNOLOGY and EMISSION columns using the provide regular expression and an `emissions` entry
`emissions` - a list of emissions to filter the results by the EMISSION column
`fuel` - filter by the FUEL column
`capacity` - filter the TECHNOLOGY column
`primary_technology` - filter the TECHNOLOGY column (can be replaced by `capacity` key)
`excluded_prod_tech` - filter the TECHNOLOGY column (can be replaced by `capacity` key)
`el_prod_technology` - filter the TECHNOLOGY column (can be replaced by `capacity` key)
`demand` - filters by the FUEL column (final energy)

The value for each of these keys is a list of regular expressions. These regular expressions are used to filter the rows of data in the chosen column to those that match the
regular expression.

Writing regular expressions can be tricky, but there are [useful tools](https://regexr.com/) to help.
Below we provide some examples:

`^.{2}(WI)` match rows with any two characters followed by `WI`

`(?=^.{2}(HF))^((?!00).)*$` match rows with `HF` in 3rd and 4th position which do not include `00`

`(?=^.{2}(NG))^((?!(00)|(CS)).)*$` match rows with `NG` in 3rd and 4th position that do not include `00` or `CS`

`^.{6}(I0)` match rows which contain any 6 characters followed by `IO` in the 7th and 8th position

Putting this together, the following entry extracts results from the result file `ProductionByTechnologyAnnual.csv`, filters out the rows
by matching values in the TECHNOLOGY column with a list of 6 regular expressions (this is an OR operation)
and assigns the unit `PJ/yr` and adds the aggregated (summing over region and year) total under `Primary Energy` in the IAMC template format.

    - iamc_variable: 'Primary Energy'
      primary_technology: ['^.{6}(I0)','^.{6}(X0)','^.{2}(HY)','^.{2}(OC)','^.{2}(SO)','^.{2}(WI)']
      unit: PJ/yr
      osemosys_param: ProductionByTechnologyAnnual

## List of relevant IAMC variables for OSeMOSYS

### Primary Energy

Level | Commodity
---|---
Primary Energy
Primary Energy|Biomass
Primary Energy|Coal
Primary Energy|Fossil
Primary Energy|Gas
Primary Energy|Geothermal
Primary Energy|Hydro
Primary Energy|Non-Biomass Renewables
Primary Energy|Nuclear
Primary Energy|Ocean
Primary Energy|Oil
Primary Energy|Other
Primary Energy|Secondary Energy Trade
Primary Energy|Solar
Primary Energy|Wind

# Priority Variables

Level | Commodity | Fuel
---|---|---
Secondary Energy|Electricity|Coal, w/ and w/o CCS
Secondary Energy|Liquids|Coal
Secondary Energy|Gases|Coal
Secondary Energy|Solids|Coal
Secondary Energy|hydrogen|Coal, w/ and w/o CCS

Level | Commodity | Fuel
---|---|---
Final Energy|Solids|Coal
Final Energy|Industry|Solids|Coal
Final Energy|Residential and Commercial|Solids|Coal
Final Energy|Other Sector|Solids|Coal

Level | Commodity | Sector | Sector | Sector
---|---|---|---|---
Emissions|CO2|Energy and Industrial Processes
Emissions|CO2|Energy|Supply
Emissions|CO2|Energy|Supply|Electricity
Emissions|CO2|Energy|Supply|Other Sector
Emissions|CO2|Energy|Demand
Emissions|CO2|Energy|Demand|Industry
Emissions|CO2|Energy|Demand|Residential and Commercial
Emissions|CO2|Energy|Demand|Transportation
Emissions|CO2|Energy|Demand|Agriculture
Emissions|CO2|Energy|Demand|Other Sector
Emissions|CO2|Industrial Processes
Emissions|CO2|AFOLU

Level | Commodity | Technology | Type
---|---|---|---
Capacity|Electricity|Solar|PV
Capacity|Electricity|Solar|CSP
Capacity|Electricity|Wind
Capacity|Electricity|Wind|Offshore
Capacity|Electricity|Wind|Onshore
Carbon Sequestration|CCS
Carbon Sequestration|CCS|Biomass
Carbon Sequestration|CCS|Fossil
Carbon Sequestration|Direct Air Capture
Emissions|N2O
Emissions|CH4
