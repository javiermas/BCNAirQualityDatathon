def tt_split(data, train_size, target_cols):
    trainX, testX = data[:train_size].drop(target_cols, axis=1).values, data[train_size:].drop(target_cols, axis=1).values
    trainY, testY = data[target_cols][:train_size].values, data[target_cols][train_size:].values
    return trainX.reshape([-1,trainX.shape[1]]), testX.reshape([-1,trainX.shape[1]]), trainY, testY

def reshape_to_keras(data, seq_length):
    data = data.reshape([-1, seq_length, data.shape[1]])
    return data
