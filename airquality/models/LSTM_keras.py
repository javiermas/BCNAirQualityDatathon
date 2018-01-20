from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

class LSTM(object):

    def __init__(self, batch_size, seq_length, hidden_units,
                 dense_layers, dense_units, epochs):
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.hidden_units = hidden_units
        self.dense_layers = dense_layers
        self.dense_units = dense_units
        
        self.model = Sequential()
        self.model.add(LSTM(self.hidden_units,\
            input_shape=(self.batch_size, self.seq_length)))
        self.create_dense_layers(self.num_layers, self.num_units)
        self.model.compile(loss='log_loss', optimizer='adam')

    def fit(X, Y):   
        self.model.fit(X, Y, epochs=100, batch_size=1, verbose=2)
    
    def predict(X):
        return self.model.predict(X)

    def create_dense_layers(num_layers, num_units):
        if isinstance(num_units, int):
            num_units = [num_units for layer in num_layers]

        for layer in num_layers:
            self.model.add(Dense(num_units[layer]))


