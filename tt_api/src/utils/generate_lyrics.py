import requests
import random
import logging
from datetime import datetime
from numpy import argmax
from tensorflow.keras.preprocessing.sequence import pad_sequences


class GenerateLyric(object):
    """
    Class dedicated to generate new lyrics, only receives
    """
    def __init__(self, tokenizer_variables, kwargs):
        try:
            self.model = tokenizer_variables['model']
            self.tokenizer = tokenizer_variables['tokenizer']
            self.max_len = tokenizer_variables['max_len']
            self.seed_text, self.percentage = kwargs["lyric_input"], kwargs["percentage"]
            logging.info(f'Receiving {self.seed_text, self.percentage}')
        except Exception as e:
            logging.error(f'Unexpected error {str(e)}')

    def generate_rhyme(self, first_verse):
        try:
            if first_verse is False:
                link = f'https://api.datamuse.com/words?rel_rhy={self.seed_text}'
                rhyme = requests.get(link).json()
                if rhyme is not None:
                    try:
                        random.seed(str(datetime.now()))
                        rhyme = random.choice(rhyme)
                        seed_text = rhyme['word']
                    except IndexError:
                        seed_text = self.seed_text
            else:
                seed_text = self.seed_text
            return seed_text
        except Exception as e:
            logging.error(f'Error processing {self.seed_text}: {str(e)}')
            seed_text = self.seed_text
        
    def complete_this_song(self, next_words, first_verse=False):
        logging.info(f'Generating song.')
        try:
            seed_text = self.generate_rhyme(first_verse)
            for _ in range(next_words):
                token_list = self.tokenizer.texts_to_sequences([seed_text])[0]
                token_list = pad_sequences([token_list], maxlen=self.max_len-1, padding='pre')
                predicted = argmax(self.model.predict(token_list, verbose=0), axis=-1)
                output_word = ""
                for word, index in self.tokenizer.word_index.items():
                    if index == predicted:
                        output_word = word
                        break
                seed_text += " " + output_word
        except AttributeError:        
            seed_text = f'Cannot process {self.seed_text} try with a different word.'
            logging.error(f'Error processing {self.seed_text}: AttributeError')

        return seed_text, self.percentage