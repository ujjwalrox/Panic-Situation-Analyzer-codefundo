from keras.models import load_model
import numpy as np
from collections import Counter


def predict(data):
    results = list()
    data = np.vstack(data)
    model = load_model('disaster_model.h5')
    predictions = model.predict(data)
    for prediction in predictions:
        prediction = list(prediction)
        probability = max(prediction)
        disaster = prediction.index(probability)
        if disaster == 0:
            results.append('typhoon')
        elif disaster == 1:
            results.append('earthquake')
        elif disaster == 2:
            results.append('winter_storm')
        elif disaster == 3:
            results.append('thunderstorm')
        elif disaster == 4:
            results.append('wildfire')

    dis = Counter(results)
    return dis.most_common(1)[0][0]