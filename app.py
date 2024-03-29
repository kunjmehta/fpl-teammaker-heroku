import streamlit as st
import pandas as pd
from fpl import predict_team, get_overview_data, extract_player_roster, \
extract_teams_data, extract_player_types
import matplotlib.pyplot as plt
import numpy as np

pd.options.display.float_format = "{:,.2f}".format

def get_team_limit(max_players_from_team):
	max_players_from_team['ARS'] = int(st.text_input('ARS:', 3))
	max_players_from_team['AVL'] = int(st.text_input('AVL:', 3))
	max_players_from_team['BOU'] = int(st.text_input('BOU:', 3))
	max_players_from_team['BRE'] = int(st.text_input('BRE:', 3))
	max_players_from_team['BHA'] = int(st.text_input('BHA:', 3))
	max_players_from_team['BUR'] = int(st.text_input('BUR:', 3))
	max_players_from_team['CHE'] = int(st.text_input('CHE:', 3))
	max_players_from_team['CRY'] = int(st.text_input('CRY:', 3))
	max_players_from_team['EVE'] = int(st.text_input('EVE:', 3))
	max_players_from_team['FUL'] = int(st.text_input('FUL:', 3))
	max_players_from_team['LIV'] = int(st.text_input('LIV:', 3))
	max_players_from_team['LUT'] = int(st.text_input('LUT:', 3))
	max_players_from_team['MCI'] = int(st.text_input('MCI:', 3))
	max_players_from_team['MUN'] = int(st.text_input('MUN:', 3))
	max_players_from_team['NEW'] = int(st.text_input('NEW:', 3))
	max_players_from_team['NFO'] = int(st.text_input('NFO:', 3))
	max_players_from_team['SHU'] = int(st.text_input('SHU:', 3))
	max_players_from_team['TOT'] = int(st.text_input('TOT:', 3))
	max_players_from_team['WHU'] = int(st.text_input('WHU:', 3))
	max_players_from_team['WOL'] = int(st.text_input('WOL:', 3))

	return max_players_from_team


st.markdown("<h1 style='text-align: center;'>Welcome to FPL TeamMaker</h1>", \
			unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Use Data Science to build your \
			team and win!</h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>Updated player data for the 2023-24 season</h5>", unsafe_allow_html=True)

transfer = False
wildcard = False
gw = 1
budget = 1000
old_data_weight = 0.4
new_data_weight = 0.6
form_weight = 0.5
max_players_from_team = {}
current_team = []
num_transfers = 1


gw = int(st.text_input('Enter the Gameweek you want to make team for:', '1'))
if gw == 1:
	st.write('Starting below, please provide how many players you want from each team.\
		Use this in cases when a particular team does not have a fixture for the week.')
	max_players_from_team = get_team_limit(max_players_from_team)

elif gw > 1 and gw <= 4:
	transfer_or_wildcard = st.radio('Select your mode of team making:', ('Transfer',\
								'New Team / Wildcard'))
	if transfer_or_wildcard == 'Transfer':
		transfer = True
	else:
		wildcard = True

	old_data_weight = float(st.text_input('Enter the weight you want to give to last \
								season\'s  data (0-1.0):', 0.4))
	new_data_weight = float(st.text_input('Enter the weight you want to give to current \
								season\'s  data (0-1.0):', 0.6))
	form_weight = float(st.text_input('Enter the weight you want to give to player form \
							(0-1.0):', 0.5))
	budget = float(st.text_input('Enter your budget x 10 (For transfers, enter \
								 the leftover budget using current team):', 1000))

	if transfer:
		num_transfers = int(st.text_input('Enter the number of transfers to be made:', 1))
		overview_data_json = get_overview_data()
		teams_df = extract_teams_data(overview_data_json)
		player_types_df = extract_player_types(overview_data_json)
		player_df = extract_player_roster(overview_data_json, player_types_df, teams_df)
		player_df = player_df[['code', 'first_name', 'second_name', 'team_code']]
		player_df['name'] = player_df['first_name'] + ' ' + player_df['second_name']
		players = st.write('Please select players you have in your team.', \
								 player_df[['code', 'name', 'team_code']])
		try:
			current_team = st.multiselect('', player_df['name'])
			current_team = [int(player_df.iloc[player_df.index[player_df['name'] == n]]['code']) for n in current_team]
		except:
			st.error('Please enter an input above')

	else:
		st.write('Starting below, please provide how many players you want from each team.\
		Use this in cases when a particular team does not have a fixture for the week.')
		max_players_from_team = get_team_limit(max_players_from_team)

elif gw > 4 and gw <=38:
	transfer_or_wildcard = st.radio('Select your mode of team making:', ('Transfer',\
								'New Team / Wildcard'))
	if transfer_or_wildcard == 'Transfer':
		transfer = True
	else:
		wildcard = True


	form_weight = float(st.text_input('Enter the weight you want to give to player form \
							(0-1.0):', 0.5))
	budget = float(st.text_input('Enter your budget x 10 (For transfers, enter \
								 the leftover budget using current team):', 1000))

	if transfer:
		num_transfers = int(st.text_input('Enter the number of transfers to be made:', 1))
		overview_data_json = get_overview_data()
		teams_df = extract_teams_data(overview_data_json)
		player_types_df = extract_player_types(overview_data_json)
		player_df = extract_player_roster(overview_data_json, player_types_df, teams_df)
		player_df = player_df[['code', 'first_name', 'second_name', 'team_code']]
		player_df['name'] = player_df['first_name'] + ' ' + player_df['second_name']
		players = st.write('Please select players you have in your team.', \
								 player_df[['code', 'name', 'team_code']])
		
		try:
			current_team = st.multiselect('', player_df['name'])
			current_team = [int(player_df.iloc[player_df.index[player_df['name'] == n]]['code']) for n in current_team]
		except:
			st.error('Please enter an input above')

	else:
		st.write('Starting below, please provide how many players you want from each team.\
		Use this in cases when a particular team does not have a fixture for the week.')
		max_players_from_team = get_team_limit(max_players_from_team)

if st.button('Get Team'):

	if gw > 38:
		st.error('Enter correct GW')

	team, points, cost = predict_team(transfer, wildcard, gw, budget, old_data_weight, \
				 new_data_weight, form_weight, max_players_from_team, \
				 current_team, num_transfers)
	team['Cost'] /= 10
	team = team.rename(columns = {"First": "First Name", "Second": "Second Name"})
	if len(team) > 0:
		st.write(team)
		st.write('Total points of whole team:', points)
		st.write('Cost of the team:', cost)
	else:
		st.info('Please use this feature after GW4 has completed')
