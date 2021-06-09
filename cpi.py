# -*- coding: utf-8 -*-

# Input consensus estimates:

# Current month consensus estimates:

rpt_list = ["Headline CPI", "Annualized CPI", "Core CPI (ex. food and energy)", "Annualized Core"]
estimate = [0.4, 4.6, 0.4, 3.3]

# No revisions for CPI, right???  -- prior_unrevised = [0.8, 4.2, 0.9, 3.0]

"""# Code: API pull from BLS, tables, print statements"""

import pandas as pd
import numpy as np
import requests

def rpt(report_series, report_name):
  print(report_name)
  print()
  base_url = 'https://api.bls.gov/publicAPI/v1/timeseries/data/'
  series = {'id':report_series,
          'name':report_name}
  data_url = '{}{}'.format(base_url,series['id'])
  print(data_url)
  raw_data = requests.get(data_url).json()
  print('Status: ' + raw_data['status'])
  print("")
  data = raw_data["Results"]["series"][0]["data"]
  data = pd.DataFrame(data).drop(["footnotes"], axis = 1)
  data["period"] = data["period"].map(lambda x: x.lstrip("M"))
  data["value"] = pd.to_numeric(data["value"])
  data["CPI"] = np.round(data["value"].pct_change(periods = -1) * 100, 1)
  data["m/m_chg"] = data["CPI"].diff(periods = -1)
  data["CPI annualized"] = np.round(data["value"].pct_change(periods = -12) * 100, 1)
  data["y/y_chg"] = data["CPI annualized"].diff(periods = -1)
  data["m/m vs prior"] = np.where(data["m/m_chg"] == 0, "unchanged", np.where(data["m/m_chg"] > 0, "up", "down"))
  data["y/y vs prior"] = np.where(data["y/y_chg"] == 0, "unchanged", np.where(data["y/y_chg"] > 0, "up", "down"))
  #data = data[0:13]
  return data

headline = rpt("CUSR0000SA0", "All items in U.S. city average, all urban consumers, seasonally adjusted")
core = rpt("CUSR0000SA0L1E", "All items less food and energy in U.S. city average, all urban consumers, seasonally adjusted")

m = [headline["periodName"][0], headline["periodName"][0], core["periodName"][0], core["periodName"][0]]
y = [headline["year"][0], headline["year"][0], core["year"][0], core["year"][0]]
current_month = [headline["CPI"][0], headline["CPI annualized"][0], core["CPI"][0], core["CPI annualized"][0]]

df2 = pd.DataFrame(zip(y, m, rpt_list, current_month, estimate), columns=["year", "month", "report", "CPI", "estimate"])

df2["vs_consensus"] = np.where(df2["estimate"] == df2["CPI"], "in line with", np.where(df2["CPI"] > df2["estimate"], "beat", "missed"))
df2["prior_month"] = [headline["periodName"][1], headline["periodName"][1], core["periodName"][1], core["periodName"][1]]
df2["prior"] = [headline["CPI"][1], headline["CPI annualized"][1], core["CPI"][1], core["CPI annualized"][1]]
df2["rose/fell"] = np.where(df2["CPI"] == df2["prior"], "unchanged from", np.where(df2["CPI"] > df2["prior"], "up from", "down from"))

# Use this instead if monthly revisions are needed:
# df2 = pd.DataFrame(zip(y, m, rpt_list, current_month, prior_unrevised, estimate), columns=["year", "month", "report", "CPI", "prior_unrevised", "estimate"])

# Print statements

def print_statements():
  for i in range(0,len(df2)):
    print("{} {} of {}% {} consensus estimates of {}%, {} {} {}% print".format(
      df2["month"][i],
      df2["report"][i],
      df2["CPI"][i],
      df2["vs_consensus"][i],
      df2["estimate"][i],
      df2["rose/fell"][i],
      df2["prior_month"][i],
      df2["prior"][i]))

"""# Current report

Note: Since CPI formula was changed in Jan-19, we can't get annualized comparisons from before Jan-21
"""

print_statements()

df2 # Table for just this month's data

headline

core

# Table of each of the components, sorted from high to low?
tables = pd.read_excel("https://www.bls.gov/cpi/tables/supplemental-files/cpi-u-202104.xlsx")
tables = pd.DataFrame(tables)

tables
