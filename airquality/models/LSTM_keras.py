import random
import time
import keras
import numpy as np
from sklearn.metrics import log_loss, mean_squared_error
from matplotlib import pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Conv2D, Flatten


class LSTM_K(object):

    def __init__(self, batch_size, seq_length, size, hidden_units, num_layers,
                 dense_units, dropout, epochs, learning_rate,
                 epochs_after=10, cnn=False):
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.size = size
        self.hidden_units = hidden_units
        self.num_layers = num_layers
        self.dense_units = dense_units
        self.dropout = dropout
        self.epochs = epochs
        self.epochs_after = epochs_after
        self.model = Sequential()
        self.model.add(LSTM(
            self.hidden_units,
            input_shape=(self.seq_length, self.size)))
        self._create_dense_layers(self.num_layers, self.dense_units)
        self.model.add(Dropout(self.dropout))
        optim = keras.optimizers.RMSprop(lr=learning_rate)
        self.model.compile(loss='mse', optimizer=optim)

    def train(self, X, Y, test_X, test_Y):
        self.model.fit(X, Y, epochs=self.epochs, batch_size=self.batch_size,
                       verbose=3, validation_data=(test_X, test_Y))

    def predict(self, X, scaler=None):
        predictions = self.model.predict(X)
        if scaler is not None:
            predictions_h = predictions.reshape([-1, 1])
            predictions_h = scaler.inverse_transform(predictions_h)
            predictions = predictions_h.reshape([-1, self.dense_units])

        return predictions

    def validate(self, trainX, trainY, testX, testY, scaler):
        i = 0
        predictions_cum = list()
        labels_cum = list()
        mse_losses = list()
        log_losses = list()
        while i < len(testY):
            extra_days = random.choice(range(1, 5))
            days = (i, i+extra_days)
            i += extra_days
            test_x, test_y = testX[days[0]:days[1]], testY[days[0]:days[1]]
            self.train(trainX, trainY, test_x, test_y)
            predictions = self.predict(test_x)
            predictions_h = predictions.reshape([-1, 1])
            test_y_h = test_y.reshape([-1, 1])
            predictions_h = scaler.inverse_transform(predictions_h)
            test_y_h = scaler.inverse_transform(test_y_h)

            mse_loss = mean_squared_error(test_y_h, predictions_h)
            l_loss = log_loss((test_y_h > 100)*1, (predictions_h > 100)*1, labels=[0,1])
            predictions_h = predictions_h.reshape([-1, self.dense_units])
            predictions_cum.append(predictions_h)
            labels_cum.append(test_y_h.reshape([-1, self.dense_units]))
            mse_losses.append(mse_loss)
            log_losses.append(l_loss)
            print()
            print('OOS loss for t %d-%d: MSE %f - log_loss %f' %\
                (days[0], days[1], mse_loss, l_loss))
            print()
            self.epochs = self.epochs_after
            trainX, trainY = np.vstack((trainX, test_x)),\
                np.vstack((trainY, test_y))

        self.predictions_cum = np.vstack(predictions_cum)
        self.labels_cum = np.vstack(labels_cum)
        return np.mean(mse_losses), np.mean(log_losses)

    def _create_dense_layers(self, num_layers, num_units):
        if isinstance(num_units, int):
            num_units = [num_units for layer in range(num_layers)]

        for layer in range(num_layers):
            self.model.add(Dense(num_units[layer]))
