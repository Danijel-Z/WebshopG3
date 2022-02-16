from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Email, DataRequired, ValidationError, Length
from models import Newsletter


class NewsLetterForm(FlaskForm):
    email = StringField("Newsletter", validators=[
                        Email(), DataRequired("Please enter an email.")])

    def validate_email(self, email):
        findExistingSubscriber = Newsletter.query.filter(
            Newsletter.email == email.data).first()

        if findExistingSubscriber:
            raise ValidationError('Du är redan prenumerant.')

class SkapaNewsletterForm(FlaskForm):
    
    rubrik = StringField("Rubrik", validators=[DataRequired(), Length(max=100, message= "Rubriken får inte vara mer än 100 tecken.")])
    underRubrik = StringField("Underrubrik", validators = [Length(max=100, message= "Underrubriken får inte vara mer än 100 tecken.")])
    innehall = TextAreaField("Innehåll", validators=[DataRequired()])
    
    submit = SubmitField("Skapa")

