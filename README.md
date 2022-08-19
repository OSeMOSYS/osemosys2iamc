# osemosys2iamc

Convert OSeMOSYS results to IAMC format

## Install from Github repository

It is currently necessary to install the OpenEntrance dependency as an editable installation.
See [issue](https://github.com/openENTRANCE/openentrance/issues/202)

    pip install -e git+https://github.com/openENTRANCE/openentrance.git@main#egg=openentrance
    pip install git+https://github.com/osemosys/osemosys2iamc@main#egg=osemosys2iamc

## Run the demo

    osemosys2iamc results config.yaml  test.csv iamc.xlsx

Check out the IAMC formatted results in `test.csv` and plots `emissions.csv`

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

Write a configuration file in YAML format. A simple configuration file with one result variable looks like this:

    model: OSeMBE v1.0.0
    scenario: DIAG-C400-lin-ResidualFossil
    region: ['Austria']
    results:
    - iamc_variable: 'Carbon Capture|Biomass'
    tech_emi: ['(?=^.{2}(BM))^.{4}(CS)']
    emissions: [CO2]
    unit: kt CO2/yr
    transform: abs
    osemosys_param: AnnualTechnologyEmissions

The first section of the configuration file with the keys `model`, `scenario`, and `region` are used to define the metadata for
the IAMC template.

The second section `results:` is where you describe each of the IAMC variables and provide instructions to osemosys2iamc on how
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

`^.{2}(WI)` match rows with exactly two characters followed by `WI`

`(?=^.{2}(HF))^((?!00).)*$` match rows with `HF` in 3rd and 4th position which do not include `00`

`(?=^.{2}(NG))^((?!(00)|(CS)).)*$` match rows with `NG` in 3rd and 4th position that do not include `00` or `CS`

`^.{6}(I0)` match rows which contain exactly 6 characters followed by `IO` in the 7th and 8th position

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
