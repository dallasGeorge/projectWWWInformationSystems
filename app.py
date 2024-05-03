# BEGIN CODE HERE
from flask import Flask,request,jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT
from selenium import webdriver
# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])


@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE
    name = request.args.get("name", "")
    products = list(mongo.db.products.find({"$text": {"$search": name}}).sort("price", -1))
    result = [{"id": str(product["_id"]), "name": product["name"], "production_Year": product["production_Year"],
               "price": product["price"], "color": product["color"], "size": product["size"]} for product in products]
    return jsonify(result)
    #return ""
    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    content = request.json
    if (mongo.db.products.find_one({"name": content["name"]})):
        mongo.db.products.update_one({"name": content["name"]}, {"$set": content})
    else:
        mongo.db.products.insert_one(content)

    return ""
    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE
    return ""
    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
   
  #  driver = webdriver.Chrome('C:/Users/30694/Documents/ch/chromedriver.exe')
  ###  driver.get("https://qa.auth.gr/el/x/studyguide/600000438/current")
  #  print(driver.page_source)
  #  driver.quit()
    return ""
    # END CODE HERE
