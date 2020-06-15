"""API for model
predict function that loads trained model and receives input from app and returns the prediction for monthly rent.
Examples:
predict_rent(3000, 'Apartment', 'Delhi South', 'Safdarjung Enclave', (28.560871, 77.190473))
"""
import joblib
import pandas as pd
from geopy.distance import geodesic
from pathlib import Path

if __name__ == "__main__":
    rent_model = joblib.load('Model_random_forest.pkl')
    columns = joblib.load('columns.pkl')
    scale = joblib.load('Fit_Standard_scalar.pkl')
else:
    rent_model = joblib.load(str(Path.cwd()) + '/Models/Model_random_forest.pkl')
    columns = joblib.load(str(Path.cwd()) + '/Models/columns.pkl')
    scale = joblib.load(str(Path.cwd()) + '/Models/Fit_Standard_scalar.pkl')


def predict_rent(size, property_type, suburb_name, locality_name, coordinates):
    """
    Takes in the details of the Listing/requirement and predicts the rent.
    :param suburb_name: str, the region of delhi where the house belongs.
    :param size: Integer, size of house in square feet.
    :param property_type: str, type of property.
    :param locality_name: str, name of locality.
    :param coordinates: list of string of latitude and longitude, co-ordinates of the house for which rent is to be predicted.
    :return: The predicted price of the listing.
    """
    try:
        assert type(size) is int
        assert type(property_type) is str
        assert type(locality_name) is str
        assert type(suburb_name) is str
        assert type(coordinates[0]) is str
        assert type(coordinates[1]) is str

        # Creating New Dataframe with existing columns
        predict = pd.DataFrame(columns=columns, index=[0])
        predict.fillna(0, inplace=True)

        # Calculating Distance from co-ord to NDLS Station
        dist_ndls = geodesic(str(coordinates[0]) + ',' + str(coordinates[1]), str(28.6417) + ',' + str(77.2207)).km
        predict['NDRLW_dist_km'] = dist_ndls

        # inserting simple input.
        predict['size_sq_ft'] = size

        # Inserting one-hot encoded Inputs
        predict['pT__' + property_type] = 1
        predict['lN__' + locality_name] = 1
        predict['sN__' + suburb_name] = 1
        # Scaling input for predictions
        scaled_input = scale.transform(predict)

        # Final Predictions
        price_pred = rent_model.predict(scaled_input)

        return price_pred[0]
    except AssertionError:
        print('Invalid Input Format')
    except ValueError:
        print('Input out of scope of Model')
