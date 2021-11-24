# -*- coding: utf-8 -*- 
import os
import pickle
import logging 
from datetime import datetime
from random import randint

# Tensorflow
from tensorflow.keras.models import load_model

# Flask
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_apispec.extension import FlaskApiSpec
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from werkzeug.exceptions import HTTPException

# Own Libraries
from .utils.schemas import HealthSchema, GetLyrics, PostLyrics
from .utils.generate_lyrics import GenerateLyric
from .utils.constants import FLASK_ENV, VERSION, PROJECT


app = Flask(__name__)
api = Api(app)  # Flask restful wraps Flask app around it.
cors = CORS(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Lyric Generator',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0',
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)
try:
    tokenizer_variables = {}
    tokenizer_variables['model'] = load_model(os.path.abspath('src/song_lyrics_generator.h5'))
    logging.info("Model loaded")
    with open(os.path.abspath('src/tokenizer_data.pkl'), 'rb') as f:
        data = pickle.load(f)
        tokenizer_variables['tokenizer'] = data['tokenizer']
        tokenizer_variables['max_len'] = data['max_sequence_len']
    logging.info("API configuration is ready.")
except Exception as e:
    logging.error(f'Failed to load model:{str(e)}')

# Endpoints
class Lyrics(MethodResource, Resource):
    """
    Main API class to call the endpoint to generate Lyrics
    get:
        gets constants to check if the api is uploaded correctly
    post:
        post the required fields to generate a lyric
    """
    @doc(description='Health-check to see the status of the API.', tags=['Lyric Generator Status'])
    @marshal_with(HealthSchema)
    def get(self):
        """
        Get method to call configurations of the API
        """
        logging.info("Getting status of the API.")
        return {
            'project': PROJECT,
            'version': VERSION,
            'environment': FLASK_ENV,
            'date': datetime.now(),
        }

    @doc(description='Send input to generate Lyric', tags=['Generate Lyric'])
    @use_kwargs(GetLyrics, location='json')
    @marshal_with(PostLyrics)
    def post(self,**kwargs):
        """
        Generate a Lyric with two kwargs readed in json
        go to schemas.py to see more of this fields.
        """
        logging.info(f'Posting: {kwargs}')
        response = {}
        lyrics = GenerateLyric(tokenizer_variables, kwargs)
        response['title'] = lyrics.complete_this_song(randint(2,5), first_verse=True)
        response['verse_1'] = lyrics.complete_this_song(randint(40,60), first_verse=True)
        response['chorus'] = lyrics.complete_this_song(randint(30,50))    
        for medium in range(2,4): 
            response['verse_'+str(medium)] = lyrics.complete_this_song(randint(40,60))
        return jsonify(response)



# Add Endpoints
api.add_resource(Lyrics, '/lyrics')

# Add Swagger Documentation
docs.register(Lyrics)


# Handling of 404 errors.
@app.errorhandler(404)
def page_not_found(e):
    logging.info(f'Resource not found')
    return jsonify({"error": "resource not found", "code": "404"}), 404


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
        logging.warning(f'Posting: {code}')

    return jsonify(error=str(e)), code


# We run the Flask application and, if it is running in a development environment,
# we run the application in debug mode.
# to run only ```FLASK_ENV=test FLASK_APP=src.app python -m flask run --host=0.0.0.0 --port=80```
app.run(debug=FLASK_ENV == 'development', host='0.0.0.0')
