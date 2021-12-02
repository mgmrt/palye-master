from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class ProfileEditForm(FlaskForm):
    username = StringField(
        "Kullanıcı Adı",
        validators=[DataRequired(), Length(min=3, max=20)],
        render_kw={"placeholder": "Kullanıcı Adınız", "autofocus": True}
    )
    password = PasswordField(
        "Yeni Şifre",
        validators=[Optional(), Length(min=6, max=20)],
        render_kw={"placeholder": "Değiştirmek İstemezseniz Boş Bırakın"}
    )
    first_name = StringField(
        "Ad",
        validators=[Optional(), Length(min=3, max=15)],
        render_kw={"placeholder": "Adınız"}
    )
    last_name = StringField(
        "Soyad",
        validators=[Optional(), Length(min=3, max=15)],
        render_kw={"placeholder": "Soyadınız"}
    )
    phone_number = StringField(
        "Telefon Numarası",
        validators=[Optional(), Length(max=15)],
        render_kw={"placeholder": "Telefon Numaranız"}
    )
    note = TextAreaField("Not")
    submit = SubmitField("Bilgileri Kaydet")
