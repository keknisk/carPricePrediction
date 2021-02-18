from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('CarPricePredictionModel.pkl', 'rb'))


@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()


# km driven    first    1
# fuel    second
# owner     third
# mileage     fourth
# engine      fifth
# seats       sixth
# years_old      seventh
# seller_type    eighth
# transmission_Manual     ninth


@app.route("/predict", methods=['POST'])
def predict():
    # global Seller_Type_trustmarkDeal
    if request.method == 'POST':
        km_driven = int(request.form['km_driven'])
        fuel = int(request.form['fuel'])
        owner = int(request.form['owner'])
        mileage = float(request.form['mileage'])
        engine = float(request.form['engine'])
        seats = int(request.form['seats'])
        age = int(request.form['Years_old'])
        seller_Type = request.form['seller_type']
        if seller_Type == 'Individual':
            seller_Type_Individual = 1
            seller_Type_trustmarkDealer = 0
        elif seller_Type == 'Trustmark Dealer':
            seller_Type_Individual = 0
            seller_Type_trustmarkDealer = 1
        else:
            seller_Type_Individual = 0
            seller_Type_trustmarkDealer = 0
        transmission = request.form['transmission_Manual']
        if transmission == 'manual':
            transmission_Manual = 1
        else:
            transmission_Manual = 0

        prediction = model.predict([[km_driven, fuel, owner, mileage, engine, seats, age, seller_Type_Individual,
                                     seller_Type_trustmarkDealer, transmission_Manual]])
        output = round(prediction[0], 2)
        if output < 0:
            return render_template('index.html', prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html', prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)