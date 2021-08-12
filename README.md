# CPI

## Monthly CPI data from Bureau of Labor Statistics (BLS)
[Bureau of Labor Statistics - Consumer Price Index](https://www.bls.gov/cpi)

Update - August 11, 2021
- Modularize code to pull BLS data more broadly

Update - June 11, 2021
- Correctly pulls annualized data (which is non-seasonally adjusted y/y)
- Added current month's subcomponents

Update - June 9, 2021
- Adds table to compare estimates (added manually) to latest month's data
- Pulls data from monthly CPI report from BLS API
- Tables of Headline CPI and Core (ex. food and energy) CPI
- Print statements to automatically generate data releases to previous months and consensus estimates

### To-dos:
- Clean up subcomponent data table
- Filtering and sorting of subcomponent data to pull highest/lowest, biggest moves m/m
