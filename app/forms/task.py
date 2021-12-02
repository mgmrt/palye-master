from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    DateField,
    TextAreaField,
    SelectField,
    IntegerField,
    FileField,
    PasswordField,
)
from wtforms.validators import DataRequired, Length, Optional, NumberRange


class TaskForm(FlaskForm):
    title = StringField(
        "Sayım Adı",
        validators=[DataRequired(), Length(min=4, max=250)],
        render_kw={"placeholder": "Sayım Adını Giriniz", "autofocus": True}
    )
    date = DateField(
        "Sayım Tarihi",
        validators=[DataRequired()],
        render_kw={"placeholder": "Sayım Tarihini Giriniz"}
    )
    note = TextAreaField("Not / Açıklama")
    status = SelectField(
        "Sayım Durumu",
        choices=[("active", "Aktif"), ("passive", "Pasif"), ("deleted", "Silinmiş")],
        validators=[DataRequired()]
    )
    submit = SubmitField("Bilgileri Kaydet")


class AssignmentForm(FlaskForm):
    user = SelectField("Atanacak Kullanıcı", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Kullanıcıyı Ata")


class LineForm(FlaskForm):
    title = StringField(
        "Hat Adı",
        validators=[DataRequired(), Length(min=4, max=250)],
        render_kw={"placeholder": "Hat Adını Giriniz", "autofocus": True}
    )
    code = StringField(
        "Hat Kodu",
        validators=[Optional(), Length(max=250)],
        render_kw={"placeholder": "Hat Kodunu Giriniz"}
    )
    number_of_daily_expeditions = IntegerField(
        "Günlük Sefer Sayısı",
        validators=[Optional()],
        render_kw={"placeholder": "Günlük Sefer Sayısını Giriniz"}
    )
    number_of_daily_vehicles = IntegerField(
        "Günlük Araç Sayısı",
        validators=[Optional()],
        render_kw={"placeholder": "Günlük Araç Sayısını Giriniz"}
    )
    number_of_total_vehicles = IntegerField(
        "Toplam Araç sayısı",
        validators=[Optional()],
        render_kw={"placeholder": "Toplam Araç Sayısını Giriniz"}
    )
    average_distance = IntegerField(
        "Ortalama Mesafe (KM)",
        validators=[Optional()],
        render_kw={"placeholder": "Ortalama Mesafe Giriniz (KM)"}
    )
    average_time_of_expeditions = IntegerField(
        "Ortalama Sefer Süresi (DK)",
        validators=[Optional()],
        render_kw={"placeholder": "Ortalama Sefer Süresi Giriniz (DK)"}
    )
    frequency_of_expeditions = IntegerField(
        "Sefer Aralığı (DK)",
        validators=[Optional()],
        render_kw={"placeholder": "Sefer Aralığı Giriniz (DK)"}
    )
    submit = SubmitField("Bilgileri Kaydet")


class StationCreateManuelForm(FlaskForm):
    title = StringField(
        "Durak Adı",
        validators=[DataRequired(), Length(max=250)],
        render_kw={"placeholder": "Durak Adını Giriniz", "autofocus": True}
    )
    number = IntegerField(
        "Durak Sırası",
        validators=[DataRequired()],
        render_kw={"placeholder": "Durak Sırasını Giriniz"}
    )
    direction = SelectField(
        "Durak Yönü",
        choices=[("forward", "Gidiş"), ("backward", "Dönüş")],
        validators=[DataRequired()]
    )
    latitude = StringField(
        "Enlem",
        validators=[Optional(), Length(max=250)],
        render_kw={"placeholder": "Enlemi Giriniz"}
    )
    longitude = StringField(
        "Boylam",
        validators=[Optional(), Length(max=250)],
        render_kw={"placeholder": "Boylamı Giriniz"}
    )
    submit = SubmitField("Bilgileri Kaydet")


class StationCreateExcelForm(FlaskForm):
    file = FileField("Excel Dosyası", validators=[DataRequired()])
    direction = SelectField(
        "Durak Yönü",
        choices=[("forward", "Gidiş"), ("backward", "Dönüş")],
        validators=[DataRequired()]
    )
    submit = SubmitField("Durakları Oluştur")


class LeafletForm(FlaskForm):
    plate = StringField(
        "Araç Plakası",
        validators=[DataRequired(), Length(max=250)],
        render_kw={"placeholder": "Araç Plakasını Giriniz", "autofocus": True}
    )
    time_hour = SelectField(
        "Sefer Başlangıç Saati (Saat)",
        validators=[DataRequired()],
        choices=[(i, i) for i in range(0, 24)],
    )
    time_minute = SelectField(
        "Sefer Başlangıç Saati (Dakika)",
        validators=[DataRequired()],
        choices=[(i, i) for i in range(0, 60)],
    )
    time_hour_finish = SelectField(
        "Sefer Bitiş Saati (Saat)",
        validators=[Optional()],
        choices=[(i, i) for i in range(0, 24)],
    )
    time_minute_finish = SelectField(
        "Sefer Bitiş Saati (Dakika)",
        validators=[Optional()],
        choices=[(i, i) for i in range(0, 60)],
    )
    number = IntegerField(
        "Föy Numarası",
        validators=[DataRequired()],
        render_kw={"placeholder": "Föy Numarasını Giriniz"}
    )
    """
    direction = SelectField(
        "Durak Yönü",
        choices=[("forward", "Gidiş"), ("backward", "Dönüş")],
        validators=[DataRequired()]
    )
    """
    is_completed = SelectField(
        "Föy Durumu",
        choices=[("0", "Tamamlanmadı"), ("1", "Tamamlandı")],
        validators=[DataRequired()]
    )
    submit = SubmitField("Bilgileri Kaydet")


class LeafletDeleteForm(FlaskForm):
    password = PasswordField(
        "Şifreniz",
        validators=[DataRequired(), Length(max=250)],
        render_kw={"placeholder": "İşlemi Onaylamak İçin Şifrenizi Giriniz", "autofocus": True}
    )
    submit = SubmitField("Onay")


class EntryForm(FlaskForm):
    station_name = StringField(
        "Durak İsmi",
        validators=[Optional(), Length(max=250)],
        render_kw={"placeholder": "Durak Adını Giriniz", "disabled": True}
    )
    entry = IntegerField(
        "Binen Yolcu",
        validators=[Optional(), NumberRange(0, 100)],
        render_kw={"placeholder": "Binen Yolcu Sayısı", "autofocus": True}
    )
    exit = IntegerField(
        "İnen Yolcu",
        validators=[Optional(), NumberRange(0, 100)],
        render_kw={"placeholder": "İnen Yolcu Sayısı"}
    )
    submit = SubmitField("Bilgileri Kaydet")

