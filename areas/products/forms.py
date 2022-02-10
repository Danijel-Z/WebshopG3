from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Email, DataRequired, ValidationError
from models import Newsletter


class NewsLetterForm(FlaskForm):
    email = StringField("Newsletter", validators=[
                        Email(), DataRequired("Please enter an email.")])

    def validate_email(self, email):
        findExistingSubscriber = Newsletter.query.filter(
            Newsletter.email == email.data).first()

        if findExistingSubscriber:
            raise ValidationError('Du är redan prenumerant.')
