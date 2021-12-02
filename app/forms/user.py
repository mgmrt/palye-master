from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional


class UserCreateForm(FlaskForm):
    username = StringField(
        "Kullanıcı Adı",
        validators=[DataRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Kullanıcı Adını Giriniz", "autofocus": True}
    )
    password = PasswordField(
        "Kullanıcı Şifresi",
        validators=[DataRequired(), Length(min=6, max=20)],
        render_kw={"placeholder": "Kullanıcı Şifresini Giriniz"}
    )
    first_name = StringField(
        "Adı",
        validators=[Optional(), Length(min=3, max=15)],
        render_kw={"placeholder": "Adını Giriniz"}
    )
    last_name = StringField(
        "Soyadı",
        validators=[Optional(), Length(min=3, max=15)],
        render_kw={"placeholder": "Soyadını Giriniz"}
    )
    phone_number = StringField(
        "Telefon Numarası",
        validators=[Optional(), Length(max=15)],
        render_kw={"placeholder": "Telefon Numarasını Giriniz"}
    )
    status = SelectField(
        "Kullanıcı Durumu",
        choices=[("active", "Aktif"), ("passive", "Pasif")],
        validators=[DataRequired()]
    )
    role = SelectField(
        "Kullanıcı Rolü",
        choices=[ ("staff", "Personel"), ("admin", "Admin")],
        validators=[DataRequired()]
    )
    note = TextAreaField("Not")
    submit = SubmitField("Kullanıcı Oluştur")


class UserUpdateForm(UserCreateForm):
    password = PasswordField(
        "Kullanıcı Şifresi",
        validators=[Optional(), Length(min=6, max=20)],
        render_kw={"placeholder": "Değiştirmek İstemiyorsanız Boş Bırakın"}
    )
    status = SelectField(
        "Kullanıcı Durumu",
        choices=[("active", "Aktif"), ("passive", "Pasif"), ("deleted", "Silinmiş")],
        validators=[DataRequired()]
    )
    submit = SubmitField("Kullanıcı Güncelle")
