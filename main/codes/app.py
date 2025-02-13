from flask import Flask, render_template, jsonify
import pandas as pd


app = Flask(__name__)

main_page_currency_table = pd.read_csv("..\codes\data\datasets\main_page_table\main_page_currency_table.csv")
currency_indicators_table = pd.read_csv("..\codes\data\datasets\currency_specific_indicators\currency_indicators_table.csv")


@app.route("/api/currency-table", methods=["GET"])
def get_currency_table():
    
    return jsonify({
        "main_page_currency_table" : main_page_currency_table.to_dict(orient='records'),
        "currency_indicators_table" : currency_indicators_table.to_dict(orient='records'),
    })

@app.route('/api/currency/<currency>', methods=["GET"])
def get_single_currency(currency):
    row = currency_indicators_table.loc[currency_indicators_table["Currency"] == currency]
    if row.empty:
        return jsonify({"error": "Currency not found"}), 404
    return jsonify(row.to_dict())


@app.route("/<currency>")
def currency_details(currency):
    currency_row = main_page_currency_table.loc[main_page_currency_table["Currency"] == currency]
    # jsonified_currency_row = jsonify(currency_row.to_dict())
    return render_template("currency-page.html", currency_name=" ",
            currency_value=" ")


@app.route("/")
def home_page():
    return render_template("main-page.html")




if __name__ == '__main__':
    app.run(debug=True)
