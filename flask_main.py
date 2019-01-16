import logging
import flask  # Web server tool.
from flask import g
# from mongoevents import *  # Mongo code
import csv  # this is for backup function
import datetime  # This is for backup function

# model related packages
import os
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise import dump
from surprise import KNNBaseline
from surprise import accuracy
from surprise.model_selection import train_test_split
import pandas as pd
from io import StringIO
import json

####
# App globals:
###

app = flask.Flask(__name__)
app.secret_key = 'secret'

PORT = 8000

TRAINED_MODEL = './models/100k/trained_model'
MOVIES_DATA = './models/100k/movies.csv'
MOVIES_LINKS = './models/100k/links.csv'
MOVIES_DETAILS = './models/100k/movies_details.csv'


###
# Pages
###

# Main index page
@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    # return flask.render_template('index.html')
    return app.send_static_file('index.html')  # provide index page for front end


# Error page(s)
@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('page_not_found.html',
                                 badurl=flask.request.base_url,
                                 linkback=flask.url_for("index")), 404


def get_neighbors(algo, iids, k):
        if algo.sim_options['user_based']:
            all_instances = algo.trainset.all_users
        else:
            all_instances = algo.trainset.all_items
        others = dict()
        for iid in iids:
            for x in all_instances():
                if x not in iids:
                    sim = algo.sim[iid, x]
                    if x not in others:
                        others[x] = sim
                    elif sim > others[x]:
                        others[x] = sim

        others = sorted(others.items(), key=lambda tple: tple[1], reverse=True)
        k_nearest_neighbors = [j for (j, _) in others[:k]]

        return k_nearest_neighbors

def movies_info_list(df):
    di = df.to_dict(orient='records')
    return json.dumps(di)


@app.route('/_autocomplete')
def autocomplete():
    # get a query of partial string of a movie title, and returns titles that contains the string
    q = flask.request.args.get("q", type=str)
    if q == None:
        return flask.jsonify(status=403, erorr="must provide a string")

    matched = movies_info[movies_info['title'].str.contains(q, case=False) == True][:8]
    # matched['movie_id'] = matched['movie_id'].apply(lambda id: algo.trainset.to_inner_iid(id))
    return flask.jsonify(status=200, data=movies_info_list(matched))

@app.route("/_predict")
def predict():
    req = flask.request.args.getlist("movie_id")
    inner_movie_ids = []
    for mid in req:
        try:
            movie_id = algo.trainset.to_inner_iid(mid)
            inner_movie_ids.append(movie_id)
        except ValueError:
            return flask.jsonify(status=403, erorr="no movie found with id: " + mid) 
    
    if len(inner_movie_ids) == 0 or len(inner_movie_ids) > 4:
        return flask.jsonify(status=403, erorr="one to four movie ids must be provided")

    app.logger.debug("User requested movies: " + ','.join(str(v) for v in inner_movie_ids))
    recommended_movies_ids = get_neighbors(algo, inner_movie_ids, k=20)
    rm_raw_ids = [algo.trainset.to_raw_iid(inner_id) for inner_id in recommended_movies_ids]
    # get the movies information from the dataset
    recommended_movies = movies_info[movies_info['movie_id'].isin(rm_raw_ids) == True]

    return flask.jsonify(status=200, data=movies_info_list(recommended_movies))


if __name__ == "__main__":
    app.debug = True
    app.logger.setLevel(logging.DEBUG)

    # get the movies data and model
    app.logger.debug("Getting the movies data...")
    movies_info = pd.read_csv(MOVIES_DETAILS, dtype='str')
    app.logger.debug("Total movies: " + str(movies_info.shape[0]))

    app.logger.debug("Getting the trained model file...")
    _, algo = dump.load(TRAINED_MODEL)

    app.run(port=PORT, host="localhost")
