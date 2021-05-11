from flask import Flask,jsonify,request,render_template
from database import Database

db = Database()

app = Flask(__name__)

@app.route("/register", methods=["GET"])
def get_register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def post_register():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    db.query(f"insert into user (name, email, password) values('{name}', '{email}', '{password}')")

    return "user registered successfully"

@app.route("/login", methods=["GET"])
def get_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def post_login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = db.select_records(f"select id, name from user where email = '{email}' and password = '{password}'")
    if len(user) == 0:
        return "Login Failed"
    else:
        return render_template("home.html")


@app.route("/product", methods=["GET"])
def get_products():
    result = db.select_records("select id, title, description, price, category from product")
    products = []
    for (id, title, description, price, category) in result:
        products.append({
            "id":id,
            "title":title,
            "description":description,
            "price":price,
            "category":category
        })

    return jsonify(products)

app.run(debug=True)

