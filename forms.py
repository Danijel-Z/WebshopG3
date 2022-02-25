from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Email, DataRequired, ValidationError, Length
from models import Subscriber


class SubscriberForm(FlaskForm):
    email = StringField("Newsletter", validators=[
                        Email(), DataRequired("Please enter an email.")])

    def validate_email(self, email):
        findExistingSubscriber = Subscriber.query.filter(
            Subscriber.email == email.data).first()

        if findExistingSubscriber:
            raise ValidationError('You are already a subscriber.')

class SkapaNewsletterForm(FlaskForm):
    
    rubrik = StringField("Title", validators=[DataRequired(), Length(max=100, message= "The title must not exceed 100 characters.")])
    underRubrik = StringField("Subtitle", validators = [Length(max=100, message= "The subtitle must not exceed 100 characters.")])
    innehall = TextAreaField("Content", validators=[DataRequired()])
    
    submit = SubmitField("Create")

class EditNewsletterForm(FlaskForm):
    rubrik = StringField("Title", validators=[DataRequired(), Length(max=100, message= "The title must not exceed 100 characters.")])
    underRubrik = StringField("Subtitle", validators = [Length(max=100, message= "The subtitle must not exceed 100 characters.")])
    innehall = TextAreaField("Content", validators=[DataRequired()])
    
    submit = SubmitField("Save")





