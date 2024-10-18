
# currently not used

from ML_model import LSTMModel

def make_prediction(data):
    """
    Use the LSTM model to make predictions based on historical data.
    """
    lstm = LSTMModel(table_name='BTCUSDT_1m')
    lstm.load_model()

    # Assume the data is preprocessed (you can adapt this as needed).
    # Here we mock the latest data as input for prediction.
    X_test = lstm.preprocess_data(data)
    predictions = lstm.predict(X_test)

    # Return the predicted value (the latest prediction)
    return predictions[-1]  # Returning the latest prediction
