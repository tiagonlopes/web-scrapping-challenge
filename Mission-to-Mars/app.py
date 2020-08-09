# Dependencies
from flask import Flask, render_template, redirect, jsonify
import pymongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
conn =  'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db

@app.route("/")
def index():
    mars = db.mars_db
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    mars = db.mars_db.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = db.mars_db
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)