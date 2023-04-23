import flask
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = pickle.load(open('model.pkl', 'rb'))


@app.route('/')
def home():
    return jsonify({'message': 'this works'})


@app.route('/predict', methods=['POST'])
def predict():
    input_values = [float(x) for x in request.form.values()]
    print(input_values)

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

    print(input_df)
    prediction = model.predict([input_df])[0]

    return jsonify({'prediction': prediction})


@app.route('/data')
def get_data():
    defenders = pd.read_csv('defenders.csv')
    defenders = defenders.fillna(value='NaN')
    top_defenders = defenders.head(6).to_dict(orient='records')
    bottom_defenders = defenders.tail(8).to_dict(orient='records')

    forwards = pd.read_csv('forwards.csv')
    forwards = forwards.fillna(value='NaN')
    top_forwards = forwards.head(6).to_dict(orient='records')
    bottom_forwards = forwards.tail(8).to_dict(orient='records')

    goalkeepers = pd.read_csv('goalkeepers.csv')
    goalkeepers = goalkeepers.fillna(value='NaN')
    top_goalkeepers = goalkeepers.head(6).to_dict(orient='records')
    bottom_goalkeepers = goalkeepers.tail(8).to_dict(orient='records')

    midfielders = pd.read_csv('mmidfielders.csv')
    midfielders = midfielders.fillna(value='NaN')
    top_midfielders = midfielders.head(6).to_dict(orient='records')
    bottom_midfielders = midfielders.tail(8).to_dict(orient='records')
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


if __name__ == '__main__':
    app.run(debug=True)
