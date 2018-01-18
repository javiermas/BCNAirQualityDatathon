


class TimeSeriesValidation(object):
    
    '''This class does validation for time series'''

    def __init__(self):
        self.models = None
    
    def validate(self, features, target, model, min_train, step):
        loss = []
        predictions = []
        tests = []
        for i in range(0, len(features)-min_train, step):
            f_train, f_test = features[:min_train+i],\
                    features[(min_train+i):(min_train+i+1)]
            t_train, t_test = target[:min_train+i],\
                    target[(min_train+i):(min_train+i+1)]

            print f_train.size, t_train.size
            pred = self._fit_and_predict_xgb(model, f_train, t_train, f_test)
            loss = ((pred - test)**2)
            MSE.append(loss)
            predictions.append(pred)
            tests.append(test)
            if i % 10 == 0:
                print 'Train %d - Test %d' % (len(train_Y), len(test_Y))
                print 'Loss: %f' % np.mean(MSE[-50:])

    def _fit_and_predict_xgb(self, model, f_train, t_train, f_test):
        print model
        model = model.fit(f_train, t_train)
        prediction = model.predict(f_test)[0]
        return prediction


    
