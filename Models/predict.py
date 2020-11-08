"""API for model
predict function that loads trained model and receives input from app and returns the prediction for monthly rent.
Examples:
predict_rent(3000, 'Apartment', 'Delhi South', 'Safdarjung Enclave'
"""
import joblib
import pandas as pd
from pathlib import Path
from scipy.stats import percentileofscore

if __name__ == "__main__":
    rent_model = joblib.load('predict_pipe_prod.pkl')
    columns = joblib.load('columns.pkl')
    scale = joblib.load('Fit_Standard_scalar.pkl')
else:
    rent_model = joblib.load(str(Path.cwd()) + '/Models/predict_pipe_prod.pkl')
    columns = joblib.load(str(Path.cwd()) + '/Models/columns.pkl')
    scale = joblib.load(str(Path.cwd()) + '/Models/Fit_Standard_scalar.pkl')


def predict_rent(size, property_type, suburb_name, locality_name):
    """
    Takes in the details of the Listing/requirement and predicts the rent.
    :param suburb_name: str, the region of delhi where the house belongs.
    :param size: Integer, size of house in square feet.
    :param property_type: str, type of property.
    :param locality_name: str, name of locality.
    :return: The predicted price of the listing.
    """
    try:
        assert type(size) is int
        assert type(property_type) is str
        assert type(locality_name) is str
        assert type(suburb_name) is str

        # Creating New Dataframe with existing columns
        predict = pd.DataFrame(columns=columns, index=[0])
        predict.fillna(0, inplace=True)

        # inserting simple input.
        predict['size_sq_ft'] = size

        # Inserting one-hot encoded Inputs
        predict['pT__' + property_type] = 1
        predict['lN__' + locality_name] = 1
        predict['sN__' + suburb_name] = 1

        # Final Predictions using pipeline
        price_pred = rent_model.predict(predict)

        return price_pred[0]
    except AssertionError:
        print('Invalid Input Format')
    except ValueError:
        print('Input out of scope of Model')


def create_input(size, prop_type, local, suburb):
    predict = pd.DataFrame(columns=columns, index=[0])
    predict.fillna(0, inplace=True)

    # inserting simple input.
    predict['size_sq_ft'] = int(size)

    # Inserting one-hot encoded Inputs
    predict['pT__' + prop_type] = 1

    predict['lN__' + local] = 1

    predict['sN__' + suburb] = 1

    return predict


def percentile_scores(df, pred_rent, Suburb_Name, Locality_Name):
    scores = {}
    scores['price_local'] = round(percentileofscore(df[df['localityName'] == Locality_Name].price, pred_rent))
    scores['price_suburb'] = round(percentileofscore(df[df['suburbName'] == Suburb_Name].price, pred_rent))
    scores['price_city'] = round(percentileofscore(df.price, pred_rent))
    return scores
