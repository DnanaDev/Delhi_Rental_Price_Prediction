# Delhi Rental Price Prediction
<p>This is an end-end data science project involving all the steps of the data science pipeline, from scraping rental listings to model development and exposing the model as a Flask app on Heroku. </p>
    
1. Data Gathering and Storing - Using a custom scraper to get the data and store it in a MongoDB collection. [Scripts.](Scraper/) 
2. Data Cleaning and Wrangling [Notebook](Data_Wrangling.ipynb)
3. Anlysis and Modelling - Include Feature selection using RFE, modelling using RandomForest Regressor, XGBoost Regressor, RandomSearchCV Hyperparamter optimsation. [Notebook.](https://nbviewer.jupyter.org/github/DnanaDev/Delhi_Rental_Price_Prediction/blob/master/Rental_Price_Analysis_and_Modeling.ipynb)
4. Exposed Flask App hosted on [Heroku](https://new-delhi-rent-prediction.herokuapp.com)<br>
![Listings](complete_heatmap_2lac.jpg)

## Data Sources
1. Makaan.com