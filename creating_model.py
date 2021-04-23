import models
import tensorflow.keras as keras
import numpy as np
import json
import time


with open('data/26064_yelp_reviews.json','r') as file:
    data = json.load(file)

x = np.array([datum['Review'] for datum in data])

y = np.array([1 if datum['Rating'] == 5 else 0 for datum in data])

inputs = keras.layers.Input(shape= (80,50))

t = keras.layers.LSTM(64, return_sequences = True)(inputs)

t = keras.layers.Dropout(0.2)(t)

t = keras.layers.LSTM(32, return_sequences = True)(t)

t = keras.layers.Dropout(0.2)(t)

t = keras.layers.LSTM(16, return_sequences = True)(t)

t = keras.layers.Dropout(0.2)(t)

t = keras.layers.LSTM(8, return_sequences = False)(t)

t = keras.layers.Dropout(0.2)(t)

t = keras.layers.Dense(1, activation='sigmoid')(t)


model = keras.Model(inputs, t)

model.compile(loss='binary_crossentropy', optimizer = 'adam', metrics=['accuracy'])#, 'Recall', 'Precision'])#, keras.metrics.Precision(thresholds=0.75,name='Precision75'), keras.metrics.Recall(thresholds=0.75,name='Recall75')])


sentiment_model = models.StringModel(model)

while True:
    sentiment_model.train(x[:-1000], y[:-1000])

    sentiment_model.evaluate(x[-1000:], y[-1000:])
    
    if input("Another epoch? (y/n)") == 'n':
        break



if input("Save model? (y/n): ") == 'y':
    name = 'SM' + str(time.time()).replace('.', '-')

    sentiment_model.save('models/' + name)

