from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, Optional, NumberRange


class LeafletForm(FlaskForm):
    plate = StringField(
        "Araç Plakası",
        validators=[DataRequired(), Length(max=250)],
        render_kw={"placeholder": "Araç Plakasını Giriniz", "autofocus": True}
    )
    time_hour = SelectField(
        "Föy Başlangıç Saati (Saat)",
        validators=[DataRequired()],
        choices=[(i, i) for i in range(0, 24)],
    )
    time_minute = SelectField(
        "Föy Başlangıç Saati (Dakika)",
        validators=[DataRequired()],
        choices=[(i, i) for i in range(0, 60)],
    )
    number = IntegerField(
        "Föy Numarası",
        validators=[DataRequired()],
        render_kw={"placeholder": "Föy Numarasını Giriniz"}
    )
    direction = SelectField(
        "Durak Yönü",
        choices=[("forward", "Gidiş"), ("backward", "Dönüş")],
        validators=[DataRequired()]
    )
    submit = SubmitField("Bilgileri Kaydet")


class EntryForm(FlaskForm):
    station_name = StringField(
        "Durak İsmi",
        validators=[Optional(), Length(max=250)],
        render_kw={"placeholder": "Durak Adını Giriniz", "disabled": True}
    )
    station_id = HiddenField(
        "Durak ID",
        validators=[DataRequired(), Length(max=250)]
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
    add_station = BooleanField(
        "Yeni Durak Ekle"
    )
    submit = SubmitField("Bilgileri Kaydet")


class EntryWithOutStationForm(FlaskForm):
    station_name = StringField(
        "Durak İsmi",
        validators=[Optional(), Length(max=250)],
        render_kw={"placeholder": "Durak Adını Giriniz", "autofocus": True}
    )
    entry = IntegerField(
        "Binen Yolcu",
        validators=[Optional(), NumberRange(0, 100)],
        render_kw={"placeholder": "Binen Yolcu Sayısı"}
    )
    exit = IntegerField(
        "İnen Yolcu",
        validators=[Optional(), NumberRange(0, 100)],
        render_kw={"placeholder": "İnen Yolcu Sayısı"}
    )
    submit = SubmitField("Bilgileri Kaydet")
