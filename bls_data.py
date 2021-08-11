import pandas as pd
import numpy as np
import requests
import credentials

login = credentials #.py file with bls_key = 'API key here'

def bls_rpt(report_series, report_name):
  print(report_name)
  print()
  
  # URL for BLS
  base_url = 'https://api.bls.gov/publicAPI/v1/timeseries/data/'
  
  # report series
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
  data["CPI annualized"] = np.round(data["value"].pct_change(periods = -13) * 100, 1)
  data["y/y_chg"] = data["CPI annualized"].diff(periods = -1)
  data["m/m vs prior"] = np.where(data["m/m_chg"] == 0, "unchanged", np.where(data["m/m_chg"] > 0, "up", "down"))
  data["y/y vs prior"] = np.where(data["y/y_chg"] == 0, "unchanged", np.where(data["y/y_chg"] > 0, "up", "down"))
  #data = data[0:13]
  return data