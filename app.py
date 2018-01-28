from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import mission_to_mars_scrape


app = Flask(__name__)


mongo = PyMongo(app)


@app.route('/')
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template('index.html', mars=mars_info)


@app.route('/scrape') #scrape first to get data
def scrape():
    mars_info = mongo.db.mars_info
    data = mission_to_mars_scrape.scrape()
    mars_info.update(
        {},
        data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)