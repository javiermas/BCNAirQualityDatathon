import random
import time
import keras
import numpy as np
from sklearn.metrics import log_loss, mean_squared_error
from matplotlib import pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM


class LSTM_K(object):

    def __init__(self, batch_size, seq_length, size, hidden_units,
                 num_layers, dense_units, epochs, learning_rate, epochs_after=10):
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.size = size
        self.hidden_units = hidden_units
        self.num_layers = num_layers
        self.dense_units = dense_units
        self.epochs = epochs
        self.epochs_after = epochs_after

        self.model = Sequential()
        self.model.add(LSTM(
            self.hidden_units,
            input_shape=(self.seq_length, self.size)))
        self._create_dense_layers(self.num_layers, self.dense_units)
        optim = keras.optimizers.RMSprop(lr=learning_rate)
        self.model.compile(loss='mse', optimizer=optim)

    def train(self, X, Y, test_X, test_Y):
        if test_X is not None:
            self.model.fit(X, Y, epochs=self.epochs, batch_size=self.batch_size,
                           verbose=1, validation_data=(test_X, test_Y))
        else:
            self.model.fit(X, Y, epochs=self.epochs, batch_size=self.batch_size,
                           verbose=1)

    def predict(self, X):
        return self.model.predict(X)

    def validate(self, trainX, trainY, testX, testY):
        i = 0
        predictions_cum = list()
        mse_losses = list()
        log_losses = list()
        while i < len(testY):
            extra_days = random.choice(range(1, 5))
            days = (i, i+extra_days)
            i += extra_days
            test_x, test_y = testX[days[0]:days[1]], testY[days[0]:days[1]]
            self.train(trainX, trainY, test_x, test_y)
            predictions = self.predict(test_x)
            mse_loss = mean_squared_error(test_y, predictions)
            l_loss = log_loss((test_y > 100)*1, (predictions > 100)*1)
            for pred in predictions:
                predictions_cum.append(pred)
            mse_losses.append(mse_loss)
            log_losses.append(l_loss)
            print()
            print('OOS loss for t %d-%d: MSE %f - log_loss %f' %\
                (days[0], days[1], mse_loss, l_loss))
            print()
            self.epochs = self.epochs_after
            trainX, trainY = np.vstack((trainX, test_x)),\
                np.vstack((trainY, test_y))
        print 'Predictions', predictions_cum
        print 'Test', testY
        '''        
        plt.plot(predictions_cum)
        plt.plot(testY)
        plt.savefig('../../references/'+'predictions'+str(time.time())+'.pdf')
        plt.plot(mse_losses)
        plt.savefig('../../references/'+'mse'+str(time.time())+'.pdf')
        plt.plot(log_losses)
        plt.savefig('../../references/'+'log_loss'+str(time.time())+'.pdf')
        '''
        return np.mean(mse_losses), np.mean(log_losses)

    def _create_dense_layers(self, num_layers, num_units):
        if isinstance(num_units, int):
            num_units = [num_units for layer in range(num_layers)]

        for layer in range(num_layers):
            self.model.add(Dense(num_units[layer]))
