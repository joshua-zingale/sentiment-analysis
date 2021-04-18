import tensorflow.keras as keras
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras import Input
from embedding import get_word_embedding, embed_strings
import numpy as np
import random

class StringModel():
    '''
    A class which wrappes around a keras model, auto embedding inputs before they are fed into the model.
    '''
    def __init__(self, model = None, embedding: dict = None):
        '''
        Creates the model. To load a previous StringModel, first instantiate object and then use self.load.
        :param model: The Keras model which will drive the ML and NN functionality of this object. The input_shape of the model should be (None, max_words, vector_dim...) where 'max_words' is the maximum number of embeddings per input and vector_dim is the dimension of each embedding.
        :param embedding: The dictionary used to convert words to numerical vectors. If None, its default, the default embedding is used.
        '''
        if model != None:
            self.input_shape = model.input_shape

            # Max Words
            self.max_words = model.input_shape[1]

        # Embedding
        # If no embedding is specified, try to load default embedding
        if embedding == None:
            self.embedding = get_word_embedding(vocab_size=100000)

        else:
            self.embedding = embedding


        # There has got to be a better way of doing this
        # Raising exception if the embedding shape is different from the model's input shape
        for _, value in self.embedding.items():
            embedding_shape = np.shape(value)
            
            if model != None and embedding_shape != self.input_shape[2:]:
                raise Exception("Input shape of model", self.input_shape, "is not compatible with embedding shape", embedding_shape,"Model should have input shape of", (None, "#") + embedding_shape)

            break


        self.model = model
        

        

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

        self.input_shape = self.model.input_shape

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
    
