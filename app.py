from flask import Flask, render_template, request
from Models.predict import predict_rent, columns

# Master Variable through which everything is done

app = Flask(__name__, static_url_path='/Static')

# Features that are to be input by the user passed, these are strings which will be used as identifiers

features = ["size", "property_type", "suburb_name", "locality_name"]
locality_names_list = [x.split('__')[1] for x in columns[12:]]


# Routes for different parts of the site

@app.route('/')
def hello():
    # Passing Python Variables to HTML using flask jinja template

    return render_template('index.html', input_features=features, ln_list=locality_names_list)


@app.route('/submit', methods=['POST'])
def input_data():
    if request.method == 'POST':
        print(request.form)
        # Form here is a dictionary that contains the variables, with name as the key.
        size = int(request.form['size'])
        property_type = str(request.form['property_type'])
        suburb_name = str(request.form['suburb_name'])
        locality_name = str(request.form['locality_name'])
        # final Predictions, calling the model
        predicted_rent = predict_rent(size, property_type, suburb_name, locality_name)
    return render_template('result.html', monthly_rent=int(predicted_rent))


if __name__ == '__main__':
    app.run(debug=True)
