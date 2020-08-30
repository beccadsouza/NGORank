import pandas as pd
import random as rd
import ast
import os

"""
	attribute	optimize	weight
	------------------------------
	distance	min			neg
	impact		max			pos
	intersect	max			pos
	establish	max			pos
	response	min			neg
	public op	max			pos
	officetime	min			neg			[if volunteer]

"""

def c():
	os.system('clear')

def p(ngo,user):
	# print(ngo['id'],user['id'])
	distance = ((user['latitude']-ngo['latitude'])**2 + (user['longitude']-ngo['longitude'])**2)**0.5 if [None,None] != [ngo['latitude'],ngo['longitude']] else 1000
	impact = ngo['public_impact'].item()
	class_intersect = len(set(user['preferences']).intersection(set(ngo['class'])))
	establishment_time = 2019 - ngo['establishment_time'].item()
	response_time = int(ngo['response_time']) if 'Nan' != ngo['response_time'] else 100
	public_opinion = ngo['public_opinion'].item()
	office_time = ngo['office_end'].item() - ngo['office_start'].item() if user['stakeholder_type'] == '0' else 0
	return -distance + impact + class_intersect + establishment_time - response_time + public_opinion - office_time

def comparison(ngo1_id,ngo2_id,user_id):
	ngo1 = df_ngos[df_ngos['id'] == ngo1_id].iloc[0]
	ngo2 = df_ngos[df_ngos['id'] == ngo2_id].iloc[0]
	usr = df_users[df_users['id'] == user_id].iloc[0]
	return 1 if p(ngo1,usr) > p(ngo2,usr) else -1

df_ngos = pd.read_csv('data/processed_ngo_dataset.csv')
df_class = pd.read_csv('data/ngo_class.csv')
df_ngos.fillna(0, inplace=True)
df_ngos['class'] = df_ngos['class'].apply(lambda x:ast.literal_eval(x))

stakeholder_types = [0, 1, 2]
users = {
	'id': [1],
	'name': ['Rebecca Dsouza'],
	'age': [20],
	'stakeholder_type': [0],
	'preferences': [[5, 9, 10, 26]],
	'latitude':[72.84056],
	'longitude':[19.05444],
}

for _ in range(2,101):
	users['id'].append(_)
	users['name'].append('John Doe')
	users['age'].append(rd.randint(15, 70))
	users['stakeholder_type'].append(rd.randint(0, 2))
	users['preferences'].append([rd.randint(0, 43) for __ in range(rd.randint(2, 5))])
	users['latitude'].append(rd.uniform(72,77))
	users['longitude'].append(rd.uniform(18,19.5))

df_users = pd.DataFrame(users)

data = {
	'user_id': [],
	'ngo1_id': [],
	'ngo2_id': [],
	'phi': [],
}

for _,df_user in df_users.iterrows():
	temp = []
	for __,df_ngo in df_ngos.iterrows():
		if len(set(df_user['preferences']).intersection(set(df_ngo['class']))) > 0:
			temp.append(df_ngo['id'])
	for i,id1 in enumerate(temp,0):
		for j,id2 in enumerate(temp[i+1:],0):
			data['user_id'].append(df_user['id'])
			data['ngo1_id'].append(id1)
			data['ngo2_id'].append(id2)
			data['phi'].append(comparison(id1,id2,df_user['id']))

df_data = pd.DataFrame(data)

model_data = {
	'user_id':[],
	'user_age':[],
	'user_stakeholder_type':[],
	# 'user_preferences':[],
	'user_latitude':[],
	'user_longitude':[],
	'ngo1_id':[],
	# 'ngo1_class':[],
	'ngo1_public_opinion':[],
	'ngo1_response_time':[],
	'ngo1_establishment_time':[],
	'ngo1_office_start': [],
	'ngo1_office_end': [],
	'ngo1_public_impact': [],
	'ngo1_latitude': [],
	'ngo1_longitude':[],
	'ngo2_id':[],
	# 'ngo2_class':[],
	'ngo2_public_opinion':[],
	'ngo2_response_time':[],
	'ngo2_establishment_time':[],
	'ngo2_office_start': [],
	'ngo2_office_end': [],
	'ngo2_public_impact': [],
	'ngo2_latitude': [],
	'ngo2_longitude':[],
	'phi':[],
}

for __,_ in df_data.iterrows():
	u = df_users[df_users['id'] == _['user_id']].iloc[0]
	n1 = df_ngos[df_ngos['id'] == _['ngo1_id']].iloc[0]
	n2 = df_ngos[df_ngos['id'] == _['ngo2_id']].iloc[0]
	model_data['user_id'].append(u['id'])
	model_data['user_age'].append(u['age'])
	# model_data['user_preferences'].append(u['preferences'])
	model_data['user_stakeholder_type'].append(u['stakeholder_type'])
	model_data['user_latitude'].append(u['latitude'])
	model_data['user_longitude'].append(u['longitude'])

	model_data['ngo1_id'].append(n1['id'])
	# model_data['ngo1_class'].append(n1['class'])
	model_data['ngo1_public_opinion'].append(n1['public_opinion'])
	model_data['ngo1_response_time'].append(n1['response_time'])
	model_data['ngo1_establishment_time'].append(n1['establishment_time'])
	model_data['ngo1_office_start'].append	(n1['office_start'])
	model_data['ngo1_office_end'].append(n1['office_end'])
	model_data['ngo1_public_impact'].append(n1['public_impact'])
	model_data['ngo1_latitude'].append(n1['latitude'])
	model_data['ngo1_longitude'].append(n1['longitude'])

	model_data['ngo2_id'].append(n2['id'])
	# model_data['ngo2_class'].append(n2['class'])
	model_data['ngo2_public_opinion'].append(n2['public_opinion'])
	model_data['ngo2_response_time'].append(n2['response_time'])
	model_data['ngo2_establishment_time'].append(n2['establishment_time'])
	model_data['ngo2_office_start'].append(n2['office_start'])
	model_data['ngo2_office_end'].append(n2['office_end'])
	model_data['ngo2_public_impact'].append(n2['public_impact'])
	model_data['ngo2_latitude'].append(n2['latitude'])
	model_data['ngo2_longitude'].append(n2['longitude'])
	model_data['phi'].append(_['phi'])

df_model_data = pd.DataFrame(model_data)

df_model_data.to_csv('data/pair_dataset.csv')
