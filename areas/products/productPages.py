from flask import Blueprint, render_template, flash, redirect,url_for
from .services import getCategory, getTrendingCategories, getProduct, getTrendingProducts
from models import db, Newsletter
from .forms import NewsLetterForm


productBluePrint = Blueprint('product', __name__)




@productBluePrint.route('/', methods = ["POST", "GET"])
def index() -> str:
    form = NewsLetterForm()

    if form.validate_on_submit():
        newSubscriber = Newsletter()
        newSubscriber.email = form.email.data
        db.session.add(newSubscriber)
        db.session.commit()

        flash("Tack! Du är nu prenumenerat!")
        return redirect(url_for("product.index", inputedEmail = form.email.data, form=form))
    
    trendingCategories = []
    trendingCategories = getTrendingCategories()
    trendingProducts = getTrendingProducts()
    return render_template('products/index.html',trendingCategories=trendingCategories,
        products=trendingProducts, form= form, inputedEmail = form.email.data)


@productBluePrint.route('/category/<id>')
def category(id) -> str:
    category = getCategory(id)
    return render_template('products/category.html',category=category)

@productBluePrint.route('/product/<id>')
def product(id) -> str:
    product = getProduct(id)
    return render_template('products/product.html',product=product)




