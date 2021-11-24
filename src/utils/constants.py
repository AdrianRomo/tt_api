# encoding: utf-8

# Execution environment.
FLASK_ENV = 'test'
VERSION = '1.0.0'
PROJECT = 'lyric-generator'
MODEL_PATH = '/app/src/utils/'

# Variables for Testing
if FLASK_ENV in ['test', 'development']:
    VERSION = '1.0.0'
    PROJECT = 'lyric-generator'
    MODEL_PATH = '/app/src/utils/'