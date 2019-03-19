from keras import models
from keras.models import Sequential
from keras.layers import Dense, Activation
from krs.test import makedata as md

batch_size = 128
n_epochs = 1

nx = 94
n1 = 256
n2 = 64
n3 = 11

data = md.Data()

model = models.load_model('nn')

predict = model.predict(data.x)

for i in range(len(predict)):
    print(data.cycle[i], predict[i])
