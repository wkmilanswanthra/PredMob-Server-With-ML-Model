import flask
import os
import csv
import json
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = pickle.load(open('model.pkl', 'rb'))


def write_to_file(data):
    filename = 'new_players.csv'
    fields = [
        "Name",
        "Nickname",
        "Gender",
        "Date_of_birth",
        "Weight",
        "Height",
        "Team",
        "Shirt_number",
        "Position",
        "Aerial_duels_won",
        "Appearances",
        "Assists_intentional",
        "Attempts_from_set_pieces",
        "Blocks",
        "Catches",
        "Clean_sheets",
        "Duels_won",
        "Goals",
        "Goals_conceded",
        "Interceptions",
        "Key_passes_attempt_assists",
        "Offsides",
        "Open_play_passes",
        "Penalties_saved",
        "Red_cards_2nd_yellow",
        "Saves_made",
        "Shots_on_target_inc_goals",
        "Straight_red_cards",
        "Successful_crosses_open_play",
        "Successful_dribbles",
        "Successful_long_passes",
        "Successful_passes_opposition_half",
        "Successful_passes_own_half",
        "Successful_short_passes",
        "Total_clearances",
        "Total_fouls_conceded",
        "Total_losses_of_possession",
        "Total_passes",
        "Total_tackles",
        "Total_touches_in_opposition_box",
        "Unsuccessful_dribbles",
        "Unsuccessful_long_passes",
        "Unsuccessful_short_passes",
        "Yellow_cards",
        "gender"
    ]

    file_exists = os.path.isfile(filename)

    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

    except IOError:
        print("I/O error")


@app.route('/predict', methods=['POST'])
def predict():
    input_values = [0 if k == "gender" and v.lower() == "male" else 1 if k == "gender" and v.lower() == "female" else float(
        v) for k, v in request.json.items() if k not in ["Name", "Nickname", "Gender", "Date_of_birth", "Weight", "Height", "Team", "Shirt_number", "Position"]]
    write_to_file(request.json)

    stat_cols = ['aerial_duels_won', 'appearances', 'assists_intentional', 'attempts_from_set_pieces', 'blocks',
                 'catches', 'clean_sheets', 'duels_won', 'goals', 'goals_conceded', 'interceptions',
                 'key_passes_attempt_assists', 'offsides', 'open_play_passes', 'penalties_saved',
                 'red_cards_2nd_yellow', 'saves_made', 'shots_on_target_inc_goals', 'straight_red_cards',
                 'successful_crosses_open_play', 'successful_dribbles', 'successful_long_passes',
                 'successful_passes_opposition_half', 'successful_passes_own_half', 'successful_short_passes',
                 'total_clearances', 'total_fouls_conceded', 'total_losses_of_possession', 'total_passes',
                 'total_tackles', 'total_touches_in_opposition_box', 'unsuccessful_dribbles',
                 'unsuccessful_long_passes', 'unsuccessful_short_passes', 'yellow_cards', 'gender']

    input_dict = dict(zip(stat_cols, input_values))

    input_df = pd.DataFrame([input_dict])

    missing_cols = set(stat_cols) - set(input_df.columns)
    for col in missing_cols:
        input_df[col] = 0

    input_df = input_df[stat_cols]

    input_df = np.squeeze(input_df, axis=0)

    prediction = model.predict([input_df])[0]

    return jsonify({'prediction': prediction})


@app.route('/data')
def get_data():
    goalkeepers_file = pd.read_csv('goalkeepers.csv')
    midfielders_file = pd.read_csv('mmidfielders.csv')
    forwards_file = pd.read_csv('forwards.csv')
    defenders_file = pd.read_csv('defenders.csv')

    goalkeepers_file = goalkeepers_file.fillna(value='NaN')
    midfielders_file = midfielders_file.fillna(value='NaN')
    forwards_file = forwards_file.fillna(value='NaN')
    defenders_file = defenders_file.fillna(value='NaN')

    all_players_df = pd.concat(
        [goalkeepers_file, midfielders_file, forwards_file, defenders_file])

    goalkeepers_df = all_players_df[all_players_df['predicted_position'] == 'Goalkeeper']
    midfielders_df = all_players_df[all_players_df['predicted_position'] == 'Midfielder']
    forwards_df = all_players_df[all_players_df['predicted_position'] == 'Forward']
    defenders_df = all_players_df[all_players_df['predicted_position'] == 'Defender']

    goalkeepers_df = goalkeepers_df.sort_values(by='score', ascending=False)
    midfielders_df = midfielders_df.sort_values(by='score', ascending=False)
    forwards_df = forwards_df.sort_values(by='score', ascending=False)
    defenders_df = defenders_df.sort_values(by='score', ascending=False)

    goalkeepers = goalkeepers_df.head(6).to_dict(orient='records')
    midfielders = midfielders_df.head(6).to_dict(orient='records')
    forwards = forwards_df.head(6).to_dict(orient='records')
    defenders = defenders_df.head(6).to_dict(orient='records')
    return jsonify(
        {'defenders': defenders,
         'forwards': forwards,
         'goalkeepers': goalkeepers,
         'midfielders': midfielders,
         })


@app.route('/altdata')
def get_altdata():
    goalkeepers_file = pd.read_csv('goalkeepers.csv')
    midfielders_file = pd.read_csv('mmidfielders.csv')
    forwards_file = pd.read_csv('forwards.csv')
    defenders_file = pd.read_csv('defenders.csv')

    goalkeepers_file = goalkeepers_file.fillna(value='NaN')
    midfielders_file = midfielders_file.fillna(value='NaN')
    forwards_file = forwards_file.fillna(value='NaN')
    defenders_file = defenders_file.fillna(value='NaN')

    goalkeepers = pd.DataFrame()
    midfielders = pd.DataFrame()
    forwards = pd.DataFrame()
    defenders = pd.DataFrame()

    for x in [goalkeepers_file, midfielders_file, forwards_file, defenders_file]:
        goalkeepers = pd.concat(
            [goalkeepers, x[x['position'] == 'Goalkeeper']])
        midfielders = pd.concat(
            [midfielders, x[x["position"] == "Midfielder"]])
        forwards = pd.concat([forwards, x[x["position"] == "Forward"]])
        defenders = pd.concat([defenders, x[x["position"] == "Defender"]])

    print(len(goalkeepers))

    goalkeepers_df = goalkeepers.sort_values(by='score', ascending=False)
    midfielders_df = midfielders.sort_values(by='score', ascending=False)
    forwards_df = forwards.sort_values(by='score', ascending=False)
    defenders_df = defenders.sort_values(by='score', ascending=False)

    top_goalkeepers = goalkeepers_df.head(6).to_dict(orient='records')
    bottom_goalkeepers = goalkeepers_df.tail(8).to_dict(orient='records')
    top_midfielders = midfielders_df.head(6).to_dict(orient='records')
    bottom_midfielders = midfielders_df.tail(8).to_dict(orient='records')
    top_forwards = forwards_df.head(6).to_dict(orient='records')
    bottom_forwards = forwards_df.tail(8).to_dict(orient='records')
    top_defenders = defenders_df.head(6).to_dict(orient='records')
    bottom_defenders = defenders_df.tail(8).to_dict(orient='records')
    return jsonify(
        {'defenders':
            {
                'top': top_defenders,
                'bottom': bottom_defenders
            },
         'forwards':
         {
                'top': top_forwards,
                'bottom': bottom_forwards
            },
         'goalkeepers':
         {
                'top': top_goalkeepers,
                'bottom': bottom_goalkeepers
            },
         'midfielders':
         {
                'top': top_midfielders,
                'bottom': bottom_midfielders
            }
         })


@app.route('/comparison')
def get_comparison():
    players = []
    files = ['defenders.csv', 'forwards.csv',
             'goalkeepers.csv', 'mmidfielders.csv']
    for file in files:
        df = pd.read_csv(file)
        df = df.fillna(value='NaN')
        df = df[['name', 'position', 'date_of_birth', 'weight',
                 'goals', 'height', 'photo', 'team', 'shirt_number']]
        df = df.to_dict(orient='records')
        players.append(df)
    return jsonify({'players': players})


if __name__ == '__main__':
    app.run(debug=True)
