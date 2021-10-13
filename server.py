from mock_data import mock_data
import json
from flask import Flask, render_template, abort, request
from flask_cors import CORS
from config import db, parse_json

app = Flask(__name__)
CORS(app)

# put the dict here.
me = {
    "name" :"Andrew",
    "last" : "Singo",
    "email" : "test@email.com",
    "age" : 32,
    "hobbies" : [],
    "address" : {
        "street" : "main st",
        "number" : "100"
    }

}

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    # return full name.
    return f"{me['name']} {me['last']}"

@app.route("/about/email")
def email_info():
    return f"{me['email']}"

@app.route("/about/address")
def address_info():
    address = me ['address']
    return f"{address['number']} {address['street']}"


#### API Methods

@app.route("/api/catalog", methods=["GET"])
def get_catalog():
    # read products from database and return it
    cursor = db.products.find({}) # get all records/documents (if not specified)
    catalog = []
    for prod in cursor:
        catalog.append(prod)
    
    # list comprehensions
    # catalog = [prod for prod in cursor]
    
    return parse_json(mock_data)
    
    # return "OK"
    # print(request.headers)
    

@app.route("/api/catalog", methods=["POST"])
def save_product():
    product = request.get_json()
    
    if not "price" in product or product["price"] <= 0:
        abort(400, "Price required and must be greater than zero")

    if not "title" in product or len(product["title"]) < 5:
        abort(400, "Title is required and should be at least 5 chars long")

        # save product into the DB
        # MONGODB add a _id with a unique value
        db.product.insert_one(product)
        return parse_json(product)

    mock_data.append(product)
    product["_id"] = len(product["title"])
    return parse_json(product)   


@app.route("/api/categories")
def get_categories():
    # return a list with the uique categories [string, string]

    cursor = db.products.find({})
    categories = []
    for product in mock_data:
        cat = product["category"]

        if cat not in categories:
            categories.append(cat)
    
    return parse_json(categories)

@app.route("/api/product/<id>")
def get_by_id(id):
    # find the porduct with such id
    # return the product as json string
    
    # found = False
    # for prod in mock_data:
    #     if prod["_id"] == id:
    #         found = True
    #         return parse_json(prod)

    product = db.products.find_one({"_id": id})
    if not found:       
        abort(404)

    return parse_json(product)    


@app.route("/api/catalog/<cat>")
def get_by_category(cat):

    cursor = db.products.find({"category": cat})  
    prods = []
    for prod in cursor:
        prods.append(prod)

    # prods = []
    # for prod in mock_data:
    #     if prod["category"].lower() == cat.lower():
    #         prods.append(prod)
  
    return parse_json(prods)

@app.route("/api/cheapest") 
def get_cheapest():

    cursor = db.products.find({})
    cheapest = cursor[0]
    for prod in cursor:
        if prod ["price"] < cheapest["price"]:
            cheapest = prod

    return parse_json(cheapest)


@app.route("/api/couponCode", methods=["POST"])
def save_coupon():       
    coupon = request.get_json()

    if not "code" in coupon or len( coupon["code"] ) < 5:
        abort(400, "Code is required and must be at least 5 chars long")

    if not "discount" in coupon or coupon["discount"] <= 0:
        abort(400, "Discount is required and shoule be greater than zero")    

    db.couponCodes.insert_one(coupon)
    return parse_json(coupon)

@app.route("/api/couponCode")
def get_coupons():
    cursor = db.couponCodes.find({})
    codes = []
    for code in cursor:
        codes.append(codes)

    return parse_json(codes)



@app.route("/api/test/loadData")
def load_data():


    return "Data already loaded"

    # load every product in mock_data into the database
    for prod in mock_data:
         db.products.insert_one(prod)
    return "Data Loaded"

app.run(debug = True)
