from keras.models import Sequential
from keras.layers import Dense, Activation
from krs import makedata as md

batch_size = 128
n_epochs = 20

nx = 94
n1 = 256
n2 = 64
n3 = 11

data = md.Data()

model = Sequential()

model.add(Dense(units=n1, activation='relu', input_shape=(nx,)))
model.add(Dense(units=n2, activation='relu'))
model.add(Dense(units=n3, activation='softmax'))

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(data.x, data.y, epochs=n_epochs, batch_size=batch_size, validation_data=(data.x_t, data.y_t))
model.save('nndribl')
