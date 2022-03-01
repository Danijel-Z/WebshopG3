from flask import Blueprint, render_template, flash, redirect,url_for, request, session
from flask_login import current_user
from .services import getCategory, getTrendingCategories, getProduct, getTrendingProducts, merge_dicts, checkIfNewsletterSubscribed, cart_grandtotal, getBildURL
from models import db, Subscriber, Product
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
    changedCategoryName = False
    newCategoryName = False

    if "/" in category.CategoryName:
        newCategoryName = category.CategoryName.replace("/", "-")
        changedCategoryName = True
    
    return render_template('products/category.html', category=category, changedCategoryName = changedCategoryName, newCategoryName = newCategoryName)

@productBluePrint.route('/product/<id>')
def product(id) -> str:
    product = getProduct(id)
    return render_template('products/product.html',product=product)


@productBluePrint.route('/viewcart', methods=["GET"])
def viewcart():
    if "shoppingcart" not in session:
        return redirect(request.referrer)
    cart = session["shoppingcart"]
    grandtotal = cart_grandtotal(cart)
    return render_template('products/viewcart.html', cart = cart, grandtotal = grandtotal )

@productBluePrint.route('/checkout', methods=["POST", "GET"])
def checkout():
    if "shoppingcart" not in session:
        return redirect(request.referrer)
    cart = session["shoppingcart"]
    return render_template('products/checkout.html', cart = cart )

@productBluePrint.route('/add_cart', methods=["POST", "GET"])
def add_cart():
    try:
        product_id = request.args.get("id")
        product = Product.query.get(product_id)
        changedCategoryName = request.args.get("changedCategoryName")
        CategoryName = request.args.get("CategoryName")

        BildURL = getBildURL(bool(changedCategoryName), CategoryName, product_id )

        dict_items = {product_id:{"name":product.ProductName, "price": product.UnitPrice, 
        "image": BildURL ,"quantity":1,"discount":product.Discontinued}}
        
        if "shoppingcart" in session:
            session["shoppingcart"] = merge_dicts(session["shoppingcart"],dict_items)
            return redirect(request.referrer)
        else:
            session["shoppingcart"] = dict_items 
            return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@productBluePrint.route('/updatecart/<int:code>', methods=["POST"])
def update_cart(code): 
    if request.method =="POST":
        quantity= request.form.get("quantity")
        try: 
            session.modified = True
            for key, item in session["shoppingcart"].items():
                if int(key) == code:
                    item["quantity"] = int(quantity)
                    return redirect(url_for("product.viewcart"))
        except Exception as e:
            print(e)
            return redirect(url_for("product.viewcart"))

@productBluePrint.route('/updatecart/<int:id>', methods=["POST","GET"])      
def delete_item(id):
    try:
        session.modified = True
        for key , item in session['shoppingcart'].items():
            if int(key) == id:
                session['shoppingcart'].pop(key, None)
                return redirect(request.referrer)
    except Exception as e:
        print(e)
        return redirect(url_for('product.viewcart'))


@productBluePrint.route('/wishlist', methods=["GET"])
def wishlist():
    if "wishlist" not in session:
        return redirect(request.referrer)
    wishcart = session["wishlist"]
    return render_template('products/wishlist.html', wishcart = wishcart )

@productBluePrint.route('/addwishlist', methods=["POST", "GET"])
def addwishlist():
    try:
        product_id = request.args.get("id")
        product = Product.query.get(product_id)

        changedCategoryName = request.args.get("changedCategoryName")
        CategoryName = request.args.get("CategoryName")

        BildURL = getBildURL(bool(changedCategoryName), CategoryName, product_id)

        dict_items = {product_id:{"name":product.ProductName, "price": product.UnitPrice, 
        "image": BildURL ,"quantity":1,"discount":product.Discontinued}}
        
        if "wishlist" in session:
            session["wishlist"] = merge_dicts(session["wishlist"],dict_items)
            return redirect(request.referrer)
        else:
            session["wishlist"] = dict_items 
            return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@productBluePrint.route('/delete_wish/<int:id>', methods=["POST","GET"])      
def delete_wish_item(id):
    try:
        session.modified = True
        for key , item in session['wishlist'].items():
            if int(key) == id:
                session['wishlist'].pop(key, None)
                return redirect(request.referrer)
    except Exception as e:
        print(e)
        return redirect(request.referrer)