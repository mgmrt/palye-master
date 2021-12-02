from datetime import datetime

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from app.models.task import Task, Assignment, Line, Leaflet, Entry, Station
from app.forms.count import LeafletForm, EntryForm, EntryWithOutStationForm

count = Blueprint("count", __name__, url_prefix="/count")


@count.route("/")
@login_required
def index():
    return render_template("views/count/task_detail.html", title="Sayım Falan Filan")


@count.route("/task/detail/<int:tid>")
@login_required
def task_detail(tid):
    the_task = Task.query.filter_by(
        id=tid
    ).filter(
        Task.assignments.any(Assignment.user_id == current_user.id)
    ).first_or_404()

    return render_template(
        "views/count/task_detail.html",
        title="Hatlar: {}".format(the_task.title),
        task=the_task,
    )


@count.route("/line/detail/<int:lid>", methods=["GET", "POST"])
@login_required
def line_detail(lid):
    form = LeafletForm()
    the_line = Line.query.filter_by(id=lid).first_or_404()

    if form.validate_on_submit():
        time = datetime.strptime(
            "{hour}:{minute}".format(
                hour=form.time_hour.data, minute=form.time_minute.data
            ),
            '%H:%M'
        ).time()

        leaflet = Leaflet()
        leaflet.task = the_line.task
        leaflet.line = the_line
        leaflet.user = current_user
        leaflet.plate = form.plate.data
        leaflet.departure_time = time
        leaflet.number = form.number.data
        leaflet.direction = form.direction.data
        leaflet.save()

        return redirect(url_for("count.counting", lid=leaflet.id))

    return render_template(
        "views/count/line_detail.html",
        title="Hat Yönetimi: {}".format(the_line.task.title),
        form=form,
        line=the_line,
    )


@count.route("/leaflet/detail/<int:lid>", methods=["GET", "POST"])
@login_required
def leaflet_detail(lid):
    form = LeafletForm()
    the_leaflet = Leaflet.query.filter_by(id=lid).first_or_404()

    if the_leaflet.is_completed:
        flash("Bu Föy Kapatılmış, Güncellenemez!", "warning")

    if form.validate_on_submit():
        if the_leaflet.is_completed:
            flash("Bu Föy Kapatıldığı İçin Güncellenemez!", "danger")
        else:
            flash("Föy Başarıyla Güncellendi", "success")

    form.plate.data = the_leaflet.plate
    form.time_hour.data = str(the_leaflet.departure_time.hour)
    form.time_minute.data = str(the_leaflet.departure_time.minute)
    form.number.data = the_leaflet.number
    form.direction.data = the_leaflet.direction.name

    return render_template(
        "views/count/leaflet_detail.html",
        title="Föy Detay",
        form=form,
        leaflet=the_leaflet,
    )


@count.route("/leaflet/detail/<int:lid>/close")
@login_required
def leaflet_close(lid):
    the_leaflet = Leaflet.query.filter_by(id=lid).first_or_404()
    the_leaflet.is_completed = True
    the_leaflet.save()
    flash("Föy Başarıyla Kilitlendi", "success")
    return redirect(url_for("count.leaflet_detail", lid=the_leaflet.id))


@count.route("/counting/<int:lid>", methods=["GET", "POST"])
@login_required
def counting(lid):
    form = EntryForm()
    the_leaflet = Leaflet.query.filter_by(id=lid).first_or_404()
    stations = Station.query.filter_by(
        line=the_leaflet.line
    ).filter_by(
        direction=the_leaflet.direction
    ).all()

    if form.validate_on_submit():
        the_station = Station.query.filter_by(id=form.station_id.data).first()
        new_entry = Entry()
        new_entry.leaflet = the_leaflet
        new_entry.station = the_station
        new_entry.station_name = the_station.title
        new_entry.entry = form.entry.data
        new_entry.exit = form.exit.data
        new_entry.save()

        return redirect(url_for("count.counting", lid=lid))

    get_last_entry = Entry.query.filter_by(
        leaflet=the_leaflet
    ).filter(
        Entry.station_id != None  # noqa
    ).order_by(
        Entry.created_at.desc()
    ).first()

    if get_last_entry:
        get_station = Station.query.filter_by(
            line=the_leaflet.line
        ).filter_by(
            direction=the_leaflet.direction
        ).filter_by(
            number=get_last_entry.station.number + 1
        ).first()

        if not get_station:
            the_leaflet.is_completed = True
            if not the_leaflet.finish_time:
                the_leaflet.finish_time = datetime.now()

            the_leaflet.save()
            flash("Sayım Tamamlandı ve Kapatıldı.", "success")

            return redirect(url_for("count.leaflet_detail", lid=the_leaflet.id))
    else:
        get_station = Station.query.filter_by(
            line=the_leaflet.line
        ).filter_by(
            direction=the_leaflet.direction
        ).filter_by(
            number=1
        ).first()

    form.station_name.data = "{} ({}. Durak)".format(get_station.title, get_station.number)
    form.station_id.data = get_station.id

    return render_template(
        "views/count/counting.html",
        title="Durak: {}".format(get_station.title),
        form=form,
        leaflet=the_leaflet,
        station=get_station,
        stations=stations,
    )


@count.route("/counting_without_station/<int:lid>", methods=["GET", "POST"])
@login_required
def counting_without_station(lid):
    form = EntryWithOutStationForm()
    the_leaflet = Leaflet.query.filter_by(id=lid).first_or_404()

    if form.validate_on_submit():
        new_entry = Entry()
        new_entry.leaflet = the_leaflet
        new_entry.station_name = form.station_name.data
        new_entry.entry = form.entry.data
        new_entry.exit = form.exit.data
        new_entry.save()

        return redirect(url_for("count.counting", lid=lid))

    return render_template(
        "views/count/counting_without_station.html",
        title="Ekstra Durak Ekle",
        form=form,
        leaflet=the_leaflet,
    )


@count.route("/entry/detail/<int:eid>", methods=["GET", "POST"])
@login_required
def entry_detail(eid):
    form = EntryWithOutStationForm()
    the_entry = Entry.query.filter_by(id=eid).filter(Entry.leaflet.has(Leaflet.user_id == current_user.id)).first_or_404()

    if the_entry.leaflet.is_completed:
        flash("Bu Föy Kapatılmış, Düzenlenemez", "danger")
        return redirect(url_for("count.leaflet_detail", lid=the_entry.leaflet.id))

    if form.validate_on_submit():
        the_entry.entry = form.entry.data
        the_entry.exit = form.exit.data
        the_entry.save()

        flash("Giriş Güncellendi", "success")

    form.entry.data = the_entry.entry
    form.exit.data = the_entry.exit
    form.station_name.data = the_entry.station_name

    return render_template(
        "views/count/entry_detail.html",
        title="Girdi Detay",
        form=form,
        entry=the_entry,
    )


@count.route("/entry/get_entry/<int:lid>/<int:ssn>")
@login_required
def entry_get(lid, ssn):
    the_entry = Entry.query.filter_by(leaflet_id=lid).filter(Entry.station.has(Station.number == ssn)).first()

    if the_entry:
        return redirect(url_for("count.entry_detail", eid=the_entry.id))

    flash("Girdi Bulunamadı", "danger")
    return redirect(url_for("count.leaflet_detail", lid=lid))