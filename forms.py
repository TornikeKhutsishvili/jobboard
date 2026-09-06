from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User
from categories import CATEGORIES


class RegistrationForm(FlaskForm):
    username = StringField('სახელი', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('ელფოსტა', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('პაროლი', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('გაიმეორეთ პაროლი', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('რეგისტრაცია')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('ეს სახელი უკვე გამოიყენება.')

        if len(username.data) < 2 or len(username.data) > 30:
            raise ValidationError('სახელი უნდა იყოს 2-30 სიმბოლოს შორის.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()

        if user:
            raise ValidationError('ეს ელფოსტა უკვე გამოიყენება.')


class LoginForm(FlaskForm):
    email = StringField('ელფოსტა', validators=[DataRequired(), Email()])
    password = PasswordField('პაროლი', validators=[DataRequired()])
    remember = BooleanField('დამახსოვრება')
    submit = SubmitField('შესვლა')


class JobForm(FlaskForm):
    title = StringField('ვაკანსიის სათაური', validators=[DataRequired(), Length(min=3, max=120)])
    summary = TextAreaField('მოკლე აღწერა', validators=[DataRequired(), Length(min=10, max=280)])
    description = TextAreaField('სრული აღწერა', validators=[DataRequired(), Length(min=20)])
    company = StringField('კომპანია', validators=[DataRequired(), Length(max=120)])
    salary = StringField('ხელფასი', validators=[DataRequired(), Length(max=80)])
    location = StringField('ლოკაცია', validators=[DataRequired(), Length(max=120)])
    category = SelectField('კატეგორია', choices=CATEGORIES, validators=[DataRequired()])
    submit = SubmitField('შენახვა')


class ProfileForm(FlaskForm):
    username = StringField('სახელი', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('ელფოსტა', validators=[DataRequired(), Email(), Length(max=120)])
    image = FileField('პროფილის ფოტო',
                validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'მხოლოდ სურათის ფაილი.')]
            )
    submit = SubmitField('პროფილის განახლება')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            if username.data != self.original_username and user:
                raise ValidationError('ეს სახელი უკვე გამოიყენება.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()

        if user:
            if email.data.lower() != self.original_email and user:
                raise ValidationError('ეს ელფოსტა უკვე გამოიყენება.')