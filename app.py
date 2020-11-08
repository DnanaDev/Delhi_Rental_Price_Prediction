from flask import Flask, render_template, request, jsonify
from Models.predict import predict_rent, columns, create_input, percentile_scores
import pandas as pd

# Master Variable through which everything is done

app = Flask(__name__, static_url_path='/Static')

# Dataset to calculate descriptive stats about prediction.

#data = pd.read_csv('Data/')
# Routes for different parts of the site

@app.route('/')
def homepage():
    # Passing Python Variables to HTML using flask jinja template

    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])
def input_data():
    params = {}
    if request.method == 'POST':
        # Form here is a dictionary that contains the variables, with name as the key.
        params['size'] = int(request.form['size'])
        params['property_type'] = str(request.form['property_type'])
        params['suburb_name'] = str(request.form['suburb_name'])
        params['locality_name'] = str(request.form['locality_name'])
        # final Predictions, calling the model
        params['predicted_rent'] = int(predict_rent(params['size'], params['property_type'],
                                                    params['suburb_name'], params['locality_name']))

        # calculate descriptive stats about prediction

        if params['predicted_rent']:
            return jsonify(predicted_rent=params)

    return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True)
