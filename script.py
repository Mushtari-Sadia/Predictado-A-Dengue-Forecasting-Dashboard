import urllib.request
import json
import os
import ssl
import pandas as pd

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script

input_df = pd.read_csv('D:\OneDrive\OneDrive - BUET\OneDrive\MVH\DengueDashboard\\train_test_datasets\\test.csv')

# print(input_df.index)
input_df = input_df
forecasts = []
for i,row in input_df.iterrows():
  # print(row['Temperature'])
  data =  {
    "Inputs": {
      "data": [
        {
          "Date": str(row['Date']),
          "Temperature": row['Temperature'],
          "Precipitation": row['Precipitation'],
          "City": row['City']
        }
      ]
    },
    "GlobalParameters": {
      "quantiles": [
        0.025,
        0.975
      ]
    }
  }

  body = str.encode(json.dumps(data))

  url = 'http://9fa22fe3-0e2f-44f9-9a3e-c0bfd6eccbfa.eastus2.azurecontainer.io/score'
  api_key = 'w63iNYH0gR1eok8Kojx7bw6JqW4yYopo' # Replace this with the API key for the web service

  # The azureml-model-deployment header will force the request to go to a specific deployment.
  # Remove this header to have the request observe the endpoint traffic rules
  headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

  req = urllib.request.Request(url, body, headers)

  try:
      response = urllib.request.urlopen(req)

      result = response.read()
      # print(result.decode())
      # print(type(json.loads(result.decode('utf-8'))))
      # df = pd.DataFrame.from_dict(json.loads(result.decode('utf-8')))
      forecasts.append(json.loads(result.decode('utf-8'))['Results']['forecast'][0])
      # dfs.append(df)
      # print(forecasts[-1])

  except urllib.error.HTTPError as error:
      print("The request failed with status code: " + str(error.code))

      # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
      print(error.info())
      print(error.read().decode("utf8", 'ignore'))

input_df['Value'] = forecasts
print(input_df_2)