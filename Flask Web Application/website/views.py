from flask import Blueprint, render_template, request, jsonify
from website.price_predictor import predict_stock_price

views = Blueprint('views', __name__)

@views.route('/') #URl to get to the home page (Decorator)
def home(): #will run when we go to '/' root
    return render_template("home.html")

@views.route('/stock', methods=['POST'])
def stock():
    ticker = request.form['ticker']
    return render_template('stock.html', ticker=ticker)

@views.route('/get_stock_price/<ticker>') #the ticker is sent through <ticker> with the url call
def get_stock_price(ticker):
    price = predict_stock_price(ticker)
    return jsonify({'price': price})
