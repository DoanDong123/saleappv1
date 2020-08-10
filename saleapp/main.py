from flask import render_template, session, request, redirect, url_for, jsonify
from saleapp import app
from saleapp import dao
from saleapp import decorator
from functools import wraps


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/products")
def product_list():
    keyword = request.args["keyword"] if request.args.get("keyword") else None

    from_price = float(request.args["from_price"]) if request.args.get("from_price") else None

    to_price = float(request.args["to_price"]) if request.args.get("to_price") else None

    return render_template("product-list.html", products=dao.read_products(keyword=keyword,
                                                                           from_price=from_price,
                                                                           to_price=to_price))


@app.route("/products/add", methods=["get", "post"])
@decorator.login_required
def product_add():
    err_msg = None
    if request.method.lower() == "post":
        if request.args.get("product_id"): # Update
            d = dict(request.form.copy())
            d["product_id"] = int(request.args["product_id"])
            if dao.update_product(**d):
                return redirect(url_for('product_list'))
            else:
                err_msg = "Somthing wrong"
        else: # ADD
            if dao.add_products(**dict(request.form)):
                return redirect(url_for('product_list'))
            else:
                err_msg = "Somthing wrong"

    categories = dao.read_categories()

    product = None
    if request.args["product_id"]:

        product = dao.read_product_by_id(int(request.args["product_id"]))

    return render_template("product-add.html", categories=categories, product=product, err_msg=err_msg)

@app.route("/api/pro/<int:product_id>", methods=["delete"])
def del_product(product_id):
    if dao.delete_product(product_id=product_id):
        return jsonify({"status": 200, "product_id": product_id})

    return jsonify({"status": 500, "error_message": "Something Wrong !!!!"})

@app.route("/products/<int:category_id>")
def product_list_by_cate(category_id):
    return render_template("product-list.html", products=dao.read_products_by_cate_id(cate_id=category_id))


@app.route("/login", methods=["get", "post"])
def login():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.check_login(username=username, password=password)
        if user:
            # Login Thanh cong
            session["user"] = user
            if "next" in request.args:
                return redirect(request.args["next"])
            return redirect(url_for('index'))
        else:
            err_msg = "Something Wrong"
    return render_template("login.html", err_msg=err_msg)


@app.route("/logout")
def logout():
    if "user" in session:
        session["user"] = None

    return redirect(url_for('index'))


@app.route("/register", methods=["get", "post"])
def register():
    if session.get("user"):
        return redirect(request.url)

    err_msg = ""
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password.strip() != confirm.strip():
            err_msg = "Mat khau ko khop"
        else:
            if dao.add_user(name=name, username=username, password=password):
                return redirect(url_for("login"))
            else:
                err_msg = "Something Wrong !!!"

    return render_template("register.html", err_msg=err_msg)


if __name__ == "__main__":
    app.run(debug=True)