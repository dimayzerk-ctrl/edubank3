from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    DecimalField,
    SelectField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=20)]
    )

    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6)]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )

    submit = SubmitField('Login')


class TransferForm(FlaskForm):
    recipient = StringField(
        'Recipient Username',
        validators=[DataRequired()]
    )

    amount = DecimalField(
        'Amount',
        validators=[DataRequired()]
    )

    description = StringField(
        'Description'
    )

    submit = SubmitField('Transfer')


class SavingsForm(FlaskForm):
    amount = DecimalField(
        'Сумма',
        validators=[DataRequired()]
    )

    action = SelectField(
        'Действие',
        choices=[
            ('deposit', 'Пополнить'),
            ('withdraw', 'Вывести')
        ]
    )

    submit = SubmitField('Подтвердить')


class PaymentForm(FlaskForm):
    category = SelectField(
        'Категория',
        choices=[
            ('Мобильная связь', 'Мобильная связь'),
            ('Интернет', 'Интернет'),
            ('ЖКХ', 'ЖКХ'),
            ('Игры', 'Игры'),
            ('Подписки', 'Подписки')
        ]
    )

    amount = DecimalField(
        'Сумма',
        validators=[DataRequired()]
    )

    submit = SubmitField('Оплатить')
