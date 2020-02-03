import requests
import pandas as pd


def get_dataframe(freq='daily', ticker='AMZN', api_key='FZQ417BECKZH7480', size='full'):
	if 'daily' in freq:
		freq = 'TIME_SERIES_DAILY'
	elif 'intra' in freq:
		freq = 'TIME_SERIES_INTRADAY'
	elif 'weekly' in freq:
		freq = 'TIME_SERIES_WEEKLY'

	site = 'https://www.alphavantage.co'
	url = f'{site}/query?function={freq}&symbol={ticker}&apikey={api_key}&outputsize={size}&datatype=pandas'
	response = requests.get(url)

	json_response = response.json()
	meta_data, data = json_response['Meta Data'], json_response['Time Series (Daily)']
	print(meta_data)

	dataframe = pd.DataFrame.from_dict(data, orient='index', dtype='float')
	dataframe.reset_index(level=0, inplace=True)
	dataframe.index.name = 'index'
	dataframe['index'] = pd.to_datetime(dataframe['index'])
	dataframe['5. volume'] = dataframe['5. volume'].astype(int)
	dataframe.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

	return dataframe, meta_data
