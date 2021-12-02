from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(
        "Kullanıcı Adı",
        validators=[DataRequired()],
        render_kw={'placeholder': 'Kullanıcı Adınızı Giriniz', "autofocus": True},
    )
    password = PasswordField(
        "Parola",
        validators=[DataRequired()],
        render_kw={"placeholder": "Parolanızı Giriniz"},
    )
    remember_me = BooleanField("Beni Hatırla")
    submit = SubmitField("Giriş Yap")
