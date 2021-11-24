from ..utils.constants import MODEL_PATH
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from numpy import array
from pandas import read_csv
from tensorflow.keras.utils import to_categorical
import pickle
import os


class ModelGeneration:
    def __init__(self):
        self.df = read_csv(os.path.abspath('pop_model.csv'))
        self.model = load_model(os.path.abspath('song_lyrics_generator.h5'))

    def create_tokenization_from_model(self):
        self.tokenizer = Tokenizer()
        self.tokenizer.fit_on_texts(self.df['Lyric'].astype(str).str.lower())
        self.total_words = len(self.tokenizer.word_index)+1
        self.tokenized_sentences = self.tokenizer.texts_to_sequences(self.df['Lyric'].astype(str))
        self.tokenized_sentences[0]
        self.input_sequences = list()
        for i in self.tokenized_sentences:
            for t in range(1, len(i)):
                self.n_gram_sequence = i[:t+1]
                self.input_sequences.append(self.n_gram_sequence)
        self.max_sequence_len = max([len(x) for x in self.input_sequences])
        self.input_sequences = array(pad_sequences(self.input_sequences, maxlen=self.max_sequence_len, padding='pre'))
        # Create predictors and label
        self.x, self.labels = self.input_sequences[:,:-1],self.input_sequences[:,-1]
        self.y = to_categorical(self.labels, num_classes=self.total_words)
        self.save_pickled_model()
        print("Modelo Guardado")
        return self

    def save_pickled_model(self):
        with open('tokenizer_data.pkl', 'wb') as handle:
            pickle.dump(
                {
                    'tokenizer': self.tokenizer,
                    'total_words':self.total_words,
                    'max_sequence_len':self.max_sequence_len
                }, handle)


ModelGeneration().create_tokenization_from_model()