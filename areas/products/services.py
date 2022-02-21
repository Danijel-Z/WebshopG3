
from models import Category, Product, Newsletter

def getTrendingCategories():
    return Category.query.order_by(Category.CategoryID.desc()).paginate(1,4,False).items

def getCategory(id):
    return Category.query.filter(Category.CategoryID ==id).first()

def getProduct(id):
    return Product.query.filter(Product.ProductID ==id).first()

def getTrendingProducts():
    return Product.query.order_by(Product.ProductID.desc()).paginate(1,8,False).items

def merge_dicts(dict1,dict2):
    if isinstance(dict1, dict) and isinstance(dict2, dict):
            key = list(dict2)[0]
            if key in dict1.keys():
                dict1[key]["quantity"] += 1
                return dict1
            else:
                return dict(list(dict1.items()) + list(dict2.items()))

def checkIfNewsletterSubscribed(email:str)-> bool:
    subscribed = Newsletter.query.filter(Newsletter.email == email).first()
    return True if subscribed else False

def cart_grandtotal(dict:dict):
    grandtotal = 0
    for key, product in dict.items():
        subtotal = float(product["price"]) * int(product["quantity"])
        grandtotal = grandtotal + subtotal
    return grandtotal
