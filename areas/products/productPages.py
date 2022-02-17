from flask import Blueprint, render_template, flash, redirect,url_for, request
from flask_login import current_user
from .services import getCategory, getTrendingCategories, getProduct, getTrendingProducts,checkIfNewsletterSubscribed
from models import db, Subscriber
from forms import SubscriberForm


productBluePrint = Blueprint('product', __name__)




@productBluePrint.route('/', methods = ["POST", "GET"])
def index() -> str:
    ##### Start Danijels kod #####
    form = SubscriberForm()
    NewsletterPage = True
    
    if form.validate_on_submit():
        newSubscriber = Subscriber()
        newSubscriber.email = form.email.data
        db.session.add(newSubscriber)
        db.session.commit()

        flash("Tack! Du är nu prenumenerat!")
        return redirect(url_for("product.index"))
    
    inputedEmail = request.form.get("email", "")
    
    if current_user.is_authenticated:
        subscribed = checkIfNewsletterSubscribed(current_user.email)
    else:
        subscribed = False

    ##### Slut av Danijels kod #####

    trendingCategories = []
    trendingCategories = getTrendingCategories()
    trendingProducts = getTrendingProducts()

    return render_template('products/index.html', trendingCategories=trendingCategories,
        products=trendingProducts, form = form, inputedEmail = inputedEmail, NewsletterPage= NewsletterPage, subscribed= subscribed)


@productBluePrint.route('/category/<id>')
def category(id) -> str:
    category = getCategory(id)
    return render_template('products/category.html',category=category)

@productBluePrint.route('/product/<id>')
def product(id) -> str:
    product = getProduct(id)
    return render_template('products/product.html',product=product)




