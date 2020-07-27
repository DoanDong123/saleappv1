from flask import render_template, request, redirect, url_for
from saleapp import app
from saleapp import dao


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



@app.route("/products/<int:category_id>")
def product_list_by_cate(category_id):
    return render_template("product-list.html", products=dao.read_products_by_cate_id(cate_id=category_id))



if __name__ == "__main__":
    app.run(debug=True)