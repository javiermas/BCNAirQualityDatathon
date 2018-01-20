import random
import numpy as np
from sklearn.metrics import log_loss, mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM


class LSTM_K(object):

    def __init__(self, batch_size, seq_length, size, hidden_units,
                 num_layers, dense_units, epochs):
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.size = size
        self.hidden_units = hidden_units
        self.num_layers = num_layers
        self.dense_units = dense_units
        self.epochs = epochs

        self.model = Sequential()
        self.model.add(LSTM(
            self.hidden_units,
            input_shape=(self.seq_length, self.size)))
        self._create_dense_layers(self.num_layers, self.dense_units)
        self.model.compile(loss='mse', optimizer='adam')

    def train(self, X, Y):
        self.model.fit(X, Y, epochs=self.epochs,
                       batch_size=self.batch_size, verbose=2)

    def predict(self, X):
        return self.model.predict(X)

    def validate(self, trainX, trainY, testX, testY):
        i = 0
        losses = list()
        while i < len(testY):
            self.train(trainX, trainY)
            extra_days = random.choice(range(1, 5))
            days = (i, i+extra_days)
            i += extra_days
            test_x, test_y = testX[:i], testY[:i]
            predictions = self.predict(test_x)
            loss = mean_squared_error(test_y, predictions)
            losses.append(loss)
            print()
            print('OOS loss for t %d-%d: MSE %f' % (days[0], days[1], loss))
            print()
            self.epochs = 10
            trainX, trainY = np.vstack((trainX, test_x)),\
                np.vstack((trainY, test_y))

    def _create_dense_layers(self, num_layers, num_units):
        if isinstance(num_units, int):
            num_units = [num_units for layer in range(num_layers)]

        for layer in range(num_layers):
            self.model.add(Dense(num_units[layer]))
