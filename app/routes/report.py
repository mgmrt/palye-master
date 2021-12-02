from flask import Blueprint, render_template, jsonify, Response
from flask_login import login_required

from app.models.task import Task, Leaflet, Line
from app.models.enums import Status
from app.forms.count import LeafletForm
from app.services.report import ReportService

report = Blueprint("report", __name__, url_prefix="/report")


@report.route("/")
@login_required
def index():
    tasks = Task.query.filter(Task.status != Status.deleted).all()
    return render_template("views/report/index.html", title="Sayım Raporları", tasks=tasks)


@report.route("/task/detail/<int:tid>")
@login_required
def task_detail(tid):
    task = Task.query.filter(Task.status != Status.deleted).filter_by(id=tid).first_or_404()
    leaflets = Leaflet.query.filter(Leaflet.line.has(Line.task_id == task.id)).all()
    return render_template(
        "views/report/task_detail.html",
        title="Rapor: {}".format(task.title),
        leaflets=leaflets,
        task=task,
    )


@report.route("/leaflet/detail/<int:lid>")
@login_required
def leaflet_detail(lid):
    form = LeafletForm()
    the_leaflet = Leaflet.query.filter_by(id=lid).first_or_404()

    form.plate.data = the_leaflet.plate
    form.time_hour.data = str(the_leaflet.departure_time.hour)
    form.time_minute.data = str(the_leaflet.departure_time.minute)
    form.number.data = the_leaflet.number
    form.direction.data = the_leaflet.direction.name

    return render_template(
        "views/report/leaflet_detail.html",
        title="Föy Detay",
        form=form,
        leaflet=the_leaflet,
    )


@report.route("/line/index/<int:tid>")
@login_required
def line_index(tid):
    task = Task.query.filter(Task.status != Status.deleted).filter_by(id=tid).first_or_404()

    return render_template(
        "views/report/line_index.html",
        title="Durak Bazlı Rapor",
        task=task,
    )


@report.route("/export/<int:tid>/one")
def export_one(tid):
    """
    Bu fonksiyon "Sayılan Sefer Sayısı" raporunu oluşturur.
    Sayılan Sefer Sayısı: Oluşturulan Toplam Föy
    Sayılan Sefer Oranı: (Günlük Sefer Sayısı / 100) * Oluşturulan Toplam Föy
    """
    the_task = Task.query.filter_by(id=tid).first_or_404()
    service = ReportService()
    data = []

    for the_line in the_task.lines:
        the_leaflets = the_line.leaflets
        data.append(
            {
                "Güzergah (Hat)": "{0} - {1}".format(the_line.title, the_line.code),
                "Sayılan Sefer Sayısı:": len(the_leaflets),
                "Sayılan Sefer Oranı": (the_line.number_of_daily_expeditions / 100) * len(the_leaflets)
            }
        )
    response = service.create_excel_file(data)

    headers = {
        'Content-Disposition': 'attachment; filename=sayilan_sefer_sayisi.xlsx',
        'Content-type': 'application/vnd.ms-excel'
    }

    return Response(response, mimetype='application/vnd.ms-excel', headers=headers)


@report.route("/export/<int:tid>/two")
def export_two(tid):
    """
    Bu fonksiyon "Toplam Yolcu" raporunu oluşturur.
    Sefer Başına Ortalama Yolcu: Hatta Toplam Giren Yolcu / Sefer Sayısı
    Tüm Gün Toplam Sefer Sayısı: Günlük Sefer Sayısı
    Tüm Gün Toplam Yolcu: Sefer Başına Ortalama Yolcu * Tüm Gün Toplam Sefer Sayısı
    """
    the_task = Task.query.filter_by(id=tid).first_or_404()
    data = []
    service = ReportService()

    for the_line in the_task.lines:
        total_passenger = the_line.get_total_passenger().total_entry
        average_passenger = (total_passenger or 0) / the_line.number_of_daily_expeditions
        data.append(
            {
                "Güzergah (Hat)": "{0} - {1}".format(the_line.code, the_line.title),
                "Sefer Başına Ortalama Yolcu:": average_passenger,
                "Tüm Gün Toplam Sefer Sayısı": the_line.number_of_daily_expeditions,
                "Tüm Gün Toplam Yolcu:": total_passenger,
            }
        )
    response = service.create_excel_file(data)

    headers = {
        'Content-Disposition': 'attachment; filename=toplam_yolcu.xlsx',
        'Content-type': 'application/vnd.ms-excel'
    }
    return Response(response, mimetype='application/vnd.ms-excel', headers=headers)


@report.route("/export/<int:tid>/three")
def export_three(tid):
    """
    Bu fonksiyon "Sefer Başına Ortalama Yolcu" raporunu oluşturur.
    Sayılan Toplam Yolcu: Gidiş + Dönüş
    Sayım Sayısı: Gidiş + Dönüş
    Sefer Başına Ortalama Yolcu Gidiş, Dönüş Toplam
    """
    the_task = Task.query.filter_by(id=tid).first_or_404()
    service = ReportService()
    data = []

    for the_line in the_task.lines:
        total_forward_passanger = the_line.get_total_passenger(direction="forward").total_entry
        total_backward_passanger = the_line.get_total_passenger(direction="backward").total_entry
        total_forward_leaflet = the_line.get_total_leaflet(direction="forward").total_leaflet
        total_backward_leaflet = the_line.get_total_leaflet(direction="backward").total_leaflet

        data.append(
            {
                "Güzergah (Hat)": "{0} - {1}".format(the_line.code, the_line.title),
                "Sayılan Toplam Yolcu": {
                    "Gidiş": total_forward_passanger or 0,
                    "Dönüş": total_backward_passanger or 0
                },
                "Sayım Sayısı": {
                    "Gidiş": total_forward_leaflet or 0,
                    "Dönüş": total_backward_leaflet or 0,
                },
                "Sefer Başına Ortalama Yolcu": {
                    "Gidiş": (total_forward_passanger or 1) / (total_forward_leaflet or 1),
                    "Dönüş": (total_backward_passanger or 1) / (total_backward_leaflet or 1),
                }
            }
        )
    response = service.create_excel_file(data)

    headers = {
        'Content-Disposition': 'attachment; filename=sefer_basina_ortalama_yolcu.xlsx',
        'Content-type': 'application/vnd.ms-excel'
    }
    return Response(response, mimetype='application/vnd.ms-excel', headers=headers)


@report.route("/export/<int:tid>/five")
def export_five(tid):
    """
    Bu fonksiyon "Araç Başına Ortalama Yolcu" raporunu oluşturur.
    Toplam Çalışan Araç Sayısı: Toplam Araç Sayısı
    Tüm Gün Toplam Yolcu: Tüm Gün Toplam Yolcu
    Tüm Gün Araç Başına Yolcu: Tüm Gün Toplam Yolcu / Toplam Çalışan Araç Sayısı
    """
    the_task = Task.query.filter_by(id=tid).first_or_404()
    data = []
    service = ReportService()

    for the_line in the_task.lines:
        total_passenger = the_line.get_total_passenger().total_entry
        data.append(
            {
                "Güzergah (Hat)": "{0} - {1}".format(the_line.code, the_line.title),
                "Toplam Çalışan Araç Sayısı:": the_line.number_of_total_vehicles,
                "Tüm Gün Toplam Yolcu": total_passenger,
                "Tüm Gün Araç Başına Yolcu:": (total_passenger or 0) / the_line.number_of_total_vehicles,
            }
        )
    response = service.create_excel_file(data)

    headers = {
        'Content-Disposition': 'attachment; filename=arac_basina_ortalama_yolcu.xlsx',
        'Content-type': 'application/vnd.ms-excel'
    }
    return Response(response, mimetype='application/vnd.ms-excel', headers=headers)


@report.route("/export/<int:tid>/six")
def export_six(tid):
    """
    Bu fonksiyon "Birim KM'de Taşınan Yolcu" raporunu oluşturur.
    Tüm Gün Toplam Mesafe: Ortalama Mesafe.
    Tüm Gün Toplam Yolcu: Toplam Yolcu.
    Tüm Gün Birim Km'de Taşınan Yolcu: Tüm Gün Toplam Yolcu / Tüm Gün Toplam Mesafe
    """
    the_task = Task.query.filter_by(id=tid).first_or_404()
    data = []
    service = ReportService()

    for the_line in the_task.lines:
        total_passenger = the_line.get_total_passenger().total_entry
        data.append(
            {
                "Güzergah (Hat)": "{0} - {1}".format(the_line.code, the_line.title),
                "Tüm Gün Toplam Mesafe:": the_line.average_distance,
                "Tüm Gün Toplam Yolcu": total_passenger,
                "Tüm Gün Birim Km'de Taşınan Yolcu:": (total_passenger or 0) / the_line.average_distance,
            }
        )
    response = service.create_excel_file(data)

    headers = {
        'Content-Disposition': 'attachment; filename=birik_km_tasianan_yolcu.xlsx',
        'Content-type': 'application/vnd.ms-excel'
    }
    return Response(response, mimetype='application/vnd.ms-excel', headers=headers)


@report.route("/export/<int:tid>/seven")
def export_seven(tid):
    """
    Bu fonksiyon "Sayım Oranı" raporunu oluşturur.
    Sayılan Sefer Sayısı: Günlük Sefer Sayısı / Oluşturulan Toplam Föy
    Sefer Başına Ortalama Yolcu: Toplam Yolcu / Sayılan Sefer Sayısı
    Sayılan Yolcu: Toplam Yolcu
    Tüm Gün Toplam Yolcu: Sayım Oranı
    """
    the_task = Task.query.filter_by(id=tid).first_or_404()
    data = []
    service = ReportService()

    for the_line in the_task.lines:
        total_passenger = the_line.get_total_passenger().total_entry
        data.append(
            {
                "Güzergah (Hat)": "{0} - {1}".format(the_line.code, the_line.title),
                "Sayılan Sefer Sayısı:": the_line.get_total_leaflet().total_leaflet,
                "Sefer Başına Ortalama Yolcu": (total_passenger or 1) / (the_line.get_total_leaflet().total_leaflet or 1),
                "Sayılan Yolcu:": (total_passenger or 1) / (the_line.average_distance or 1),
                "Tüm Gün Toplam Yolcu": total_passenger,
                "Sayım Oranı": "{}%".format(((total_passenger or 1) / (the_line.average_distance or 1)) / (total_passenger or 1)),
            }
        )
    response = service.create_excel_file(data)

    headers = {
        'Content-Disposition': 'attachment; filename=sayim_orani.xlsx',
        'Content-type': 'application/vnd.ms-excel'
    }
    return Response(response, mimetype='application/vnd.ms-excel', headers=headers)


@report.route("/export/<int:lid>/eight")
def export_eight(lid):
    """
    Bu fonksiyon "Durak Raporu" raporunu oluşturur.
    """
    the_line = Line.query.filter_by(id=lid).first_or_404()
    data = []
    service = ReportService()

    for the_station in the_line.stations:
        data.append(
            {
                "Durak": the_station.title,
                "Toplam Binen Yolcu": the_station.get_passangers().total_entry,
            }
        )
    response = service.create_excel_file(data)

    headers = {
        'Content-Disposition': 'attachment; filename=durak_raporu.xlsx',
        'Content-type': 'application/vnd.ms-excel'
    }
    return Response(response, mimetype='application/vnd.ms-excel', headers=headers)
