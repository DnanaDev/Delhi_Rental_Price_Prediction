from flask import Flask, render_template, request, jsonify, url_for
from Models.predict import predict_rent, percentile_scores, load_data

# Master Variable through which everything is done

app = Flask(__name__, static_folder='static')

# Dataset to calculate descriptive stats about prediction.

data = load_data()


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
        stats = percentile_scores(data, params['predicted_rent'], params['suburb_name'], params['locality_name'])

        # shallow merging dictionaries
        params = {**params, ** stats}

        if params['predicted_rent']:
            return jsonify(results=params)

    return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=False)
