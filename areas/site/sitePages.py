from this import d
from flask import Blueprint, flash, redirect, render_template, request, url_for
from models import Subscriber, db, Newsletter
from forms import SkapaNewsletterForm, EditNewsletterForm
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
     return render_template('site/newsletter.html', listWithNewsletters = enumerate(listWithNewsletters) )


@siteBluePrint.route('/newsletter/<int:id>', methods = ["GET", "POST"])
@roles_required("Admin")
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

          flash("Your newsletter has been created!")
          return redirect(url_for('site.newsletter'))
     return render_template('site/skapaNewsletter.html', form = form)


@siteBluePrint.route('/newsletter/edit/<int:id>', methods= ["GET", "POST"])
@roles_required("Admin") 
def edit_newsletter(id) -> str:
     form = EditNewsletterForm()
     if form.validate_on_submit():
          newsletterToEdit = Newsletter.query.get(id)
          newsletterToEdit.rubrik = form.rubrik.data
          newsletterToEdit.underRubrik = form.underRubrik.data
          newsletterToEdit.innehall = form.innehall.data
          newsletterToEdit.user_id = current_user.id

          db.session.commit()
          flash("Your newsletter has been changed!")
          return redirect(url_for("site.edit_newsletter", id = id))
          
     elif request.method == "GET":
          editedNewsletter = Newsletter.query.get(id)
          form.rubrik.data = editedNewsletter.rubrik 
          form.underRubrik.data = editedNewsletter.underRubrik 
          form.innehall.data = editedNewsletter.innehall 
     return render_template("site/editNewsletter.html", form = form)
     
@siteBluePrint.route('/newsletter/delete/<int:id>', methods= ["POST"])
@roles_required("Admin") 
def delete_newsletter(id) -> str:
     findNewsletterToDelete = Newsletter.query.get(id)
     

     if findNewsletterToDelete:
          db.session.delete(findNewsletterToDelete)
          db.session.commit()
          flash("Newsletter has been removed.")
          return redirect(url_for("site.newsletter"))

     flash("Could not remove the newsletter, try again later.")
     return render_template("site/newsletter.html")
     


