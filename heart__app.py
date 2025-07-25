# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import joblib

# load dataset
df = pd.read_csv('./heart_failure_clinical_records_dataset.csv')

# split X and Y
X = df.drop('DEATH_EVENT', axis=1)
Y = df['DEATH_EVENT']

# train-test split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# define MLP model
model = Sequential([
    Dense(32, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# train the model
history = model.fit(X_train_scaled, Y_train, epochs=50, batch_size=16, validation_split=0.2)

# evaluate
loss, acc = model.evaluate(X_test_scaled, Y_test)
print("Test accuracy:", acc)

# optionally save model and scaler
model.save('heart_mlp_model.h5')
joblib.dump(scaler, 'scaler.pkl')
