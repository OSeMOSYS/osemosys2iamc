# osemosys2iamc

Convert OSeMOSYS results to IAMC format

## Run the demo

    python resultify.py results config.yaml  test.csv

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

## Usage for OSeMOSYS

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
