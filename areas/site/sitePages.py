from this import d
from flask import Blueprint, flash, redirect, render_template, request, url_for
from models import Subscriber, db, Newsletter
from forms import SkapaNewsletterForm
from flask_user import roles_required, current_user

siteBluePrint = Blueprint('site', __name__)

@siteBluePrint.route('/contact')
def contact() -> str:
     return render_template('site/contact.html')

@siteBluePrint.route('/terms')
def terms() -> str:
     return render_template('site/terms.html')

@siteBluePrint.route('/about')
def about() -> str:
     return render_template('site/about.html')


@siteBluePrint.route('/newsletter', methods= ["GET", "POST"])
def newsletter() -> str:
     listWithNewsletters = Newsletter.query.all()
     return render_template('site/newsletter.html', listWithNewsletters = listWithNewsletters)

@siteBluePrint.route('/newsletter/<int:id>', methods = ["GET", "POST"])
def send_newsletter(id):
     foundNewsletter = Newsletter.query.get(id)
     
     if foundNewsletter:

          subscribers = Subscriber.query.all()
          
          for subscriber in subscribers:
               subscriber.newsletters.append(foundNewsletter)
          
          db.session.commit()
          
          flash("Newsletter has been sended to subscribers succesfully!")
          return redirect(url_for('site.newsletter'))

     flash("Something went wrong.")
     return redirect(url_for('site.newsletter'))


@siteBluePrint.route('/newsletter/ny', methods= ["GET", "POST"])
@roles_required("Admin") 
def skapa_newsletter() -> str:
     form = SkapaNewsletterForm()
     if form.validate_on_submit():
          new_newsletter = Newsletter()
          new_newsletter.rubrik = form.rubrik.data
          new_newsletter.underRubrik = form.underRubrik.data
          new_newsletter.innehall = form.innehall.data
          new_newsletter.user_id = current_user.id
          
          db.session.add(new_newsletter)
          db.session.commit()

          flash("Din newsletter har skapats!")
          return redirect(url_for('site.newsletter'))
     return render_template('site/skapaNewsletter.html', form = form)
