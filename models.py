import tensorflow.keras as keras
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras import Input
from embedding import get_word_embedding, embed_strings
import numpy as np
import random

class StringModel():
    '''
    An LSTM model which makes binary predictions based on inputed strings.
    '''
    def __init__(self, metrics = ['accuracy'], embedding = None, max_words = 40):
        '''
        Creates the model.
        :param input_shape: The shape of each input
        :param metrics: The metrics tracked by the model durring training and evaluation.
        :param embedding: The dictionary used to convert words to numerical vectors. If None, its default, the default embedding is used.
        :param max_words: The maximum number of words per string input. If max_words is not reached by a particular input, 0 vectors are appended. Any word above max_words is disgarded.
        '''
        # Max Words
        self.max_words = max_words

        # Embedding
        if embedding == None:
            self.embedding = get_word_embedding(vocab_size=100000)

        else:
            self.embedding = embedding

        # Input shape
        # There has got to be a better way of doing this
        vector_dim = 0
        for _, value in self.embedding.items():
             vector_dim = len(value)
             break

        self.input_shape = (max_words, vector_dim)

        # Build model with keras.
        p = Input(self.input_shape)
        x = LSTM(64, return_sequences = True)(p)
        x = Dropout(0.2)(x)
        x = LSTM(32, return_sequences= True)(x)
        x = Dropout(0.2)(x)
        x = LSTM(16, return_sequences= False)(x)
        x = Dense(1, activation='sigmoid')(x)
        self.model = keras.Model(p, x)
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics = metrics)

        

        

    def train(self, x, y, epochs = 1, mix_pairs= True):
        '''
        Trains the model on input data.
        :param x: The training inputs. Each input is a string.
        :param y: The training outputs. Each output is either 0 or 1.
        :param epochs: The number of training iterrations.
        :param mix: If true, input and output pairs are randomly ordered.
        '''
        if mix_pairs == True:
            x, y = __mix(x, y)
        else:
            x, y = np.array(x), np.array(y, dtype='float32')
        

        x = embed_strings(x, self.embedding, self.max_words)

        self.model.fit(x, y, epochs = epochs)


    def evaluate(self, x, y):
        '''
        Evaluate the model.
        :param x: The inputs.
        :param y: The correct outputs.
        '''
        x = embed_strings(x, self.embedding, self.max_words)
        y = np.array(y, dtype='float32')
        
        self.model.evaluate(x, y)

    def predict(self, x):
        '''
        Predicts outputs for given input strings.
        :param x: The inputs for which outputs are predicted. It is an array of strings
        :return: The predictions
        '''
        x = embed_strings(x, self.embedding, self.max_words)

        return self.model.predict(x)

    def save(self, destination):
        '''
        Saves current model.
        :param destination: The file path into which the model will be saved.
        '''
        self.model.save(destination)

    def load(self, path):
        '''
        Loads a a model from persistant storage. Currently, the embedding used with the model is not saved nor loaded, so it must be set manually. To avoid issues, always use the default embedding (do not specify one when instantiating object).
        :param path: That file path to the stored model.
        '''
        self.model = keras.models.load_model(path)

        self.max_words = self.model.input_shape[1]



def __mix(x,y):
    '''
    Randomize the order in input output pairs
    '''    
    x = list(x)

    y = list(y)

    new_x, new_y = [], []

    while len(x) > 0:
        i = random.randrange(0, len(x))

        new_x.append(x.pop(i))

        new_y.append(y.pop(i))

    return np.array(new_x), np.array(new_y)
    
