from flask import Blueprint, render_template
#from areas.products.services import getCategory, getTrendingCategories, getProduct
#from ../../ models import Category, Product



productBluePrint = Blueprint('product', __name__)




@productBluePrint.route('/')
def index() -> str:
    trendingCategories = []
#    trendingCategories = getTrendingCategories()
    return render_template('products/index.html',trendingCategories=trendingCategories)


@productBluePrint.route('/category/<id>')
def category(id) -> str:
    category = getCategory(id)
    return render_template('products/category.html',category=category)

@productBluePrint.route('/product/<id>')
def product(id) -> str:
    product = getProduct(id)
    return render_template('products/product.html',product=product)




def getTrendingCategories():
    return Category.query.order_by(Category.CategoryID.desc()).paginate(1,4,False).items

def getCategory(id):
    return Category.query.filter(Category.CategoryID ==id).first()

def getProduct(id):
    return Product.query.filter(Product.ProductID ==id).first()
