import mapbox_api as mb
import pandas as pd
import re


def refine(location):
	tokens = location.split(',')
	for x in range(len(tokens)):
		if re.search(r"\d\d\d\d\d\d", tokens[x]): return ''.join([tokens[y] for y in range(x - 2, x + 1)])

df_ngos = pd.ExcelFile('data/dataset.xlsx').parse('Sheet1')
df_class = pd.ExcelFile('data/dataset.xlsx').parse('Sheet2')

df_ngos['address'] = df_ngos['location'].apply(lambda x:refine(x))
df_ngos['coordinates'] = df_ngos['address'].apply(lambda x:mb.get_coordinates(x))
df_ngos['class'] = df_ngos['class'].apply(lambda x:list(map(int,str(x).split(','))))

df_temp = pd.DataFrame(df_ngos.coordinates.tolist(), columns=['latitude', 'longitude'])
df_temp.index += 1
df_ngos['latitude'] = df_temp.loc[:,'latitude']
df_ngos['longitude'] = df_temp.loc[:,'longitude']
df_ngos = df_ngos.drop('location', axis=1)
df_ngos = df_ngos.drop('coordinates', axis=1)
df_ngos = df_ngos.set_index('id')
df_class = df_class.set_index('id')

df_ngos.to_csv('data/processed_ngo_dataset.csv')
df_class.to_csv('data/ngo_class.csv')
