# ML_model.py
import numpy as np
import pandas as pd
import config

from keras.models import Sequential
from keras.layers import LSTM, Dense
import os

class LSTMModel:
    def __init__(self, time_frame=config.CANDLESTICK_DURATION, model_name=config.MODEL_NAME):
        self.time_frame = time_frame
        self.model_name = model_name
        self.model = None
        self.model_path = f'{self.model_name}_{self.time_frame}.h5'
        self.min_val = None
        self.max_val = None

    def custom_normalize(self, data):
        """
        Custom function to normalize data between 0 and 1.
        :param data: Numpy array of closing prices
        :return: Scaled data, min and max values (for inverse scaling)
        """
        self.min_val = np.min(data)
        self.max_val = np.max(data)
        return (data - self.min_val) / (self.max_val - self.min_val)

    def custom_inverse_normalize(self, data):
        """
        Custom function to inverse the normalization process.
        :param data: Scaled data
        :return: Original data values before scaling
        """
        return data * (self.max_val - self.min_val) + self.min_val

    def prepare_data(self, data, lookback=config.LOOKBACK_PERIOD):
        """
        Prepare the data for LSTM. Scale the data and split it into sequences.
        :param data: Historical data (OHLC)
        :param lookback: Number of previous data points to consider for prediction
        """
        closing_prices = data['close'].values
        scaled_data = self.custom_normalize(closing_prices)
        
        X, y = [], []
        for i in range(lookback, len(scaled_data)):
            X.append(scaled_data[i - lookback:i])
            y.append(scaled_data[i])
        return np.array(X), np.array(y)

    def build_model(self, input_shape):
        """
        Build the LSTM model architecture.
        :param input_shape: Shape of the input data
        """
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
        model.add(LSTM(50))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def train(self, X_train, y_train, epochs=config.LSTM_EPOCHS, batch_size=config.LSTM_BATCH_SIZE):
        """
        Train the LSTM model.
        :param X_train: Training features
        :param y_train: Training labels
        :param epochs: Number of training epochs
        :param batch_size: Batch size for training
        """
        if self.model is None:
            self.model = self.build_model((X_train.shape[1], 1))
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)

    def save_model(self):
        """
        Save the trained LSTM model to a file.
        """
        if self.model is not None:
            self.model.save(self.model_path)
            print(f"Model saved to {self.model_path}")

    def load_model(self):
        """
        Load an existing model if available.
        """
        if os.path.exists(self.model_path):
            from keras.models import load_model
            self.model = load_model(self.model_path)
            print(f"Model loaded from {self.model_path}")
        else:
            print(f"No existing model found at {self.model_path}")

    def run(self):
        """
        Run the entire LSTM prediction process.
        """
        # Assuming `data` is fetched from the database (you can modify this)
        db = Database(db_name=config.DATABASE_NAME)
        table_name = f'{config.TRADING_SYMBOL}_{self.time_frame}'
        raw_data = db.fetch_data(table_name)
        db.close()

        if raw_data:
            df = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            X, y = self.prepare_data(df)
            X = np.reshape(X, (X.shape[0], X.shape[1], 1))  # Reshape for LSTM

            # Train the model or load an existing one
            self.load_model() if os.path.exists(self.model_path) else self.train(X, y)
            self.save_model()

            # Predict (this part can be extended for actual prediction)
            predictions = self.model.predict(X)

            # Inverse scaling of predictions
            predictions = self.custom_inverse_normalize(predictions)
            print(predictions)
