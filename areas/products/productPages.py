from flask import Blueprint, render_template
from .services import getCategory, getTrendingCategories, getProduct



productBluePrint = Blueprint('product', __name__)




@productBluePrint.route('/')
def index() -> str:
    trendingCategories = []
    trendingCategories = getTrendingCategories()
    return render_template('products/index.html',trendingCategories=trendingCategories)


@productBluePrint.route('/category/<id>')
def category(id) -> str:
    category = getCategory(id)
    return render_template('products/category.html',category=category)

@productBluePrint.route('/product/<id>')
def product(id) -> str:
    product = getProduct(id)
    return render_template('products/product.html',product=product)




