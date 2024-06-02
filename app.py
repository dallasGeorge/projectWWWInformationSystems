# BEGIN CODE HERE
from flask import Flask,request,jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import numpy as np
# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])


@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE
    name = request.args.get("name")
    products = list(mongo.db.products.find({"name": name}))
    if not products:
        products = list(mongo.db.products.find({"$text": {"$search": name}}).sort("price", -1))

    results = []
    for product in products:
        result = {
            "id": str(product["_id"]),
            "name": product["name"],
            "production_Year": product["production_Year"],
            "price": product["price"],
            "color": product["color"],
            "size": product["size"]
        }
        results.append(result)

    return jsonify(results)
    return ""
    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    colors = [1, 2, 3]
    sizes = [1, 2, 3, 4]
    content = request.json
    if content["color"] not in colors or content["size"] not in sizes:
        return jsonify({"error": "Invalid color (1 or 2 or 3) or size (1 or 2 or 3 or 4) code"}), 400
  
    if (mongo.db.products.find_one({"name": content["name"]})):
        mongo.db.products.update_one({"name": content["name"]}, {"$set": content})
    else:
        mongo.db.products.insert_one(content)

    return ""
    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE
    data = request.get_json()
    input = np.array([data["production_Year"], data["price"], data["color"], data["size"]])

    results = []
    all_products = mongo.db.products.find({})

    for product in all_products:
        pr_array = np.array([product["production_Year"], product["price"], product["color"], product["size"]])

        vec1_norm = np.linalg.norm(input)
        vec2_norm = np.linalg.norm(pr_array)

        if vec1_norm != 0 or vec2_norm != 0:
            similarity = np.dot(input / vec1_norm, pr_array / vec2_norm)
        else:
            similarity= 0

        
        if similarity > 0.7:
            results.append(product["name"])

    return jsonify(results)
    return ""
    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    semester = request.args.get('semester', type=int)
    if semester is None:
        return jsonify({"error": "did not give a valid semester integer"}), 400
    url = "https://qa.auth.gr/el/x/studyguide/600000438/current"

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    semester_element = driver.find_element(By.ID, f"exam{semester}")
    course_elements = semester_element.find_elements(By.TAG_NAME, "tr")
    course_titles = []
    for row in course_elements:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) > 1:
            course_titles.append(cols[1].text)
    return jsonify(course_titles)
    # END CODE HERE
