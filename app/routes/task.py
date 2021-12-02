from datetime import datetime

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from pandas import read_excel

from app.models.user import User
from app.models.task import Task, Assignment, Line, Station, Leaflet, Entry
from app.models.enums import Status
from app.models.user import UserRole
from app.forms.task import (
    TaskForm,
    AssignmentForm,
    LineForm,
    StationCreateManuelForm,
    StationCreateExcelForm,
    LeafletForm,
    LeafletDeleteForm,
    EntryForm,
)

task = Blueprint("task", __name__, url_prefix="/task")


@task.route("/")
@task.route("/index", methods=["GET", "POST"])
@login_required
def task_index():
    form = TaskForm()
    tasks = Task.query.filter(Task.status != Status.deleted).all()

    if form.validate_on_submit():
        new_task = Task()
        new_task.title = form.title.data
        new_task.date = form.date.data
        new_task.note = form.note.data
        new_task.status = form.status.data
        new_task.save()

        flash("Sayım Başarıyla Oluşturuldu", "success")

        return redirect(url_for("task.task_detail", tid=new_task.id))

    return render_template("views/task/task_index.html", title="Sayım Yönetimi", form=form, tasks=tasks)


@task.route("/detail/<int:tid>", methods=["GET", "POST"])
@login_required
def task_detail(tid):
    form = TaskForm()
    the_task = Task.query.filter_by(id=tid).first_or_404()

    if form.validate_on_submit():
        the_task.title = form.title.data
        the_task.date = form.date.data
        the_task.note = form.note.data
        the_task.status = form.status.data
        the_task.save()

        flash("Sayım Başarıyla Güncellendi", "success")

    form.title.data = the_task.title
    form.date.data = the_task.date
    form.note.data = the_task.note
    form.status.data = the_task.status.name

    return render_template(
        "views/task/task_detail.html",
        title="Sayım Yönetimi: {}".format(the_task.title),
        form=form,
        task=the_task
    )


@task.route("/detail/<int:tid>/users", methods=["GET", "POST"])
@login_required
def user_index(tid):
    the_task = Task.query.filter_by(id=tid).first_or_404()
    user = User.query.filter_by(role=UserRole.staff).filter_by(status=Status.active).all()
    form = AssignmentForm()

    form.user.choices = [(i.id, i.full_name) for i in user]

    if form.validate_on_submit():
        assignment_check = Assignment.query.filter_by(user_id=form.user.data).filter_by(task_id=the_task.id).first()

        if assignment_check:
            flash("Kullanıcı Zaten Bu Sayıma Atanmış", "danger")
        else:
            assignment = Assignment()
            assignment.task = the_task
            assignment.user_id = int(form.user.data)
            assignment.save()
            flash("Kullanıcı Sayıma Atandı", "success")

    return render_template(
        "views/task/user_index.html",
        title="Kullanıcılar: {}".format(the_task.title),
        form=form,
        task=the_task,
    )


@task.route("/detail/<int:tid>/users/<int:uid>/delete", methods=["GET"])
@login_required
def user_delete(tid, uid):
    assignment_check = Assignment.query.filter_by(user_id=uid).filter_by(task_id=tid).first()

    if assignment_check:
        assignment_check.destroy()
        flash("Kullanıcı Sayımdan Çıkartıldı", "success")
    else:
        flash("Kullanıcı Zaten Sayımda Değil yada Olası Farklı Problemler", "danger")

    return redirect(url_for("task.user_index", tid=tid))


@task.route("/line/create/<int:tid>", methods=["GET", "POST"])
@login_required
def line_create(tid):
    form = LineForm()
    the_task = Task.query.filter_by(id=tid).first_or_404()

    if form.validate_on_submit():
        new_line = Line()
        new_line.task = the_task
        new_line.title = form.title.data
        new_line.code = form.code.data
        new_line.number_of_daily_expeditions = form.number_of_daily_expeditions.data
        new_line.number_of_daily_vehicles = form.number_of_daily_vehicles.data
        new_line.number_of_total_vehicles = form.number_of_total_vehicles.data
        new_line.average_distance = form.average_distance.data
        new_line.average_time_of_expeditions = form.average_time_of_expeditions.data
        new_line.frequency_of_expeditions = form.frequency_of_expeditions.data
        new_line.save()

        flash("Hat Başarıyla Oluşturuldu", "success")
        return redirect(url_for("task.line_detail", lid=new_line.id))

    return render_template(
        "views/task/line_create.html",
        title="Hat Oluştur: {}".format(the_task.title),
        form=form,
        task=the_task,
    )


@task.route("/line/detail/<int:lid>", methods=["GET", "POST"])
@login_required
def line_detail(lid):
    the_line = Line.query.filter_by(id=lid).first_or_404()
    form = LineForm()

    if form.validate_on_submit():
        the_line.title = form.title.data  # noqa
        the_line.code = form.code.data
        the_line.number_of_daily_expeditions = form.number_of_daily_expeditions.data
        the_line.number_of_daily_vehicles = form.number_of_daily_vehicles.data
        the_line.number_of_total_vehicles = form.number_of_total_vehicles.data
        the_line.average_distance = form.average_distance.data
        the_line.average_time_of_expeditions = form.average_time_of_expeditions.data
        the_line.frequency_of_expeditions = form.frequency_of_expeditions.data
        the_line.save()
        flash("Hat Başarıyla Güncellendi", "success")

    form.title.data = the_line.title  # noqa
    form.code.data = the_line.code
    form.number_of_daily_expeditions.data = the_line.number_of_daily_expeditions
    form.number_of_daily_vehicles.data = the_line.number_of_daily_vehicles
    form.number_of_total_vehicles.data = the_line.number_of_total_vehicles
    form.average_distance.data = the_line.average_distance
    form.average_time_of_expeditions.data = the_line.average_time_of_expeditions
    form.frequency_of_expeditions.data = the_line.frequency_of_expeditions

    return render_template(
        "views/task/line_detail.html",
        title="Hat Yönetimi: {}".format(the_line.title),
        form=form,
        line=the_line,
    )


@task.route("/leaflet/detail/<int:lid>", methods=["GET", "POST"])
@login_required
def leaflet_detail(lid):
    form = LeafletForm()
    the_leaflet = Leaflet.query.filter_by(id=lid).first_or_404()

    if form.validate_on_submit():
        time = datetime.strptime(
            "{hour}:{minute}".format(
                hour=form.time_hour.data, minute=form.time_minute.data
            ),
            '%H:%M'
        ).time()
        if not str(form.time_hour_finish.data) == "0":
            time_finish = datetime.strptime(
                "{hour}:{minute}".format(
                    hour=form.time_hour_finish.data, minute=form.time_minute_finish.data
                ),
                '%H:%M'
            ).time()
            the_leaflet.finish_time = time_finish

        the_leaflet.plate = form.plate.data
        the_leaflet.departure_time = time
        the_leaflet.number = form.number.data
        the_leaflet.is_completed = bool(int(form.is_completed.data))
        the_leaflet.save()

        flash("Föy Güncellendi", "success")

    form.plate.data = the_leaflet.plate
    form.time_hour.data = str(the_leaflet.departure_time.hour)
    form.time_minute.data = str(the_leaflet.departure_time.minute)
    if the_leaflet.finish_time:
        form.time_hour_finish.data = str(the_leaflet.finish_time.hour)
        form.time_minute_finish.data = str(the_leaflet.finish_time.minute)
    form.number.data = the_leaflet.number
    form.is_completed.data = str(int(the_leaflet.is_completed))

    return render_template(
        "views/task/leaflet_detail.html",
        title="Föy Detay",
        form=form,
        leaflet=the_leaflet,
    )


@task.route("/leaflet/detail/<int:lid>/delete", methods=["GET", "POST"])
@login_required
def leaflet_delete(lid):
    form = LeafletDeleteForm()
    the_leaflet = Leaflet.query.filter_by(id=lid).first_or_404()

    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            flash("Föy Başarıyla Silindi", "success")
            for entry in the_leaflet.entries:
                entry.destroy()

            line_id = the_leaflet.line.id
            the_leaflet.destroy()

            return redirect(url_for("task.line_detail", lid=line_id))
        else:
            flash("Şifrenizi Doğru Girmediniz", "danger")
            return redirect(url_for("task.leaflet_delete", lid=the_leaflet.line.id))

    return render_template(
        "views/task/leaflet_delete.html",
        title="Föy Silme Onay",
        form=form,
        leaflet=the_leaflet,
    )


@task.route("/station/create/manuel/<int:lid>", methods=["GET", "POST"])
@login_required
def station_create_manuel(lid):
    form = StationCreateManuelForm()
    the_line = Line.query.filter_by(id=lid).first_or_404()

    if form.validate_on_submit():
        new_station = Station()
        new_station.line = the_line
        new_station.title = form.title.data
        new_station.number = form.number.data
        new_station.direction = form.direction.data
        new_station.latitude = form.latitude.data
        new_station.longitude = form.longitude.data
        new_station.save()

        flash("Durak Başarıyla Oluşturuldu: {}".format(new_station.title), "success")

    return render_template(
        "views/task/station_create_manuel.html",
        title="Durak Oluştur: {} -> {}".format(the_line.task.title, the_line.title),
        form=form,
        line=the_line,
    )


@task.route("/station/create/excel/<int:lid>", methods=["GET", "POST"])
@login_required
def station_create_excel(lid):
    form = StationCreateExcelForm()
    the_line = Line.query.filter_by(id=lid).first_or_404()

    if form.validate_on_submit():
        excel_file = request.files[form.file.name]
        stations = read_excel(excel_file).values.tolist()

        for station in stations:
            new_station = Station(
                line=the_line,
                number=str(station[0]),
                title=str(station[1]),
                direction=form.direction.data,
                latitude=str(station[2]),
                longitude=str(station[3]),
            )
            new_station.save()

        flash("Duraklar Başarıyla Oluşturuldu", "success")

    return render_template(
        "views/task/station_create_excel.html",
        title="Durak Oluştur: {} -> {}".format(the_line.task.title, the_line.title),
        form=form,
        line=the_line,
    )


@task.route("/station/detail/<int:sid>", methods=["GET", "POST"])
@login_required
def station_detail(sid):
    form = StationCreateManuelForm()
    the_station = Station.query.filter_by(id=sid).first_or_404()

    if form.validate_on_submit():
        the_station.title = form.title.data
        the_station.number = form.number.data
        the_station.direction = form.direction.data
        the_station.latitude = form.latitude.data
        the_station.longitude = form.longitude.data
        the_station.save()

        flash("Durak Başarıyla Güncellendi", "success")

    form.title.data = the_station.title
    form.number.data = the_station.number
    form.direction.data = the_station.direction.name
    form.latitude.data = the_station.latitude
    form.longitude.data = the_station.longitude

    return render_template(
        "views/task/station_detail.html",
        title="Durak Yönetimi: {}".format(the_station.title),
        form=form,
        station=the_station,
    )


@task.route("/station/delete/<int:sid>", methods=["GET", "POST"])
@login_required
def station_delete(sid):
    form = LeafletDeleteForm()
    the_station = Station.query.filter_by(id=sid).first_or_404()

    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            for entry in the_station.entries:
                entry.destroy()

            line_id = the_station.line.id
            the_station.destroy()

            flash("Durak Başarıyla Silindi", "success")
            return redirect(url_for("task.line_detail", lid=line_id))
        else:
            flash("Şifrenizi Doğru Girmediniz", "danger")

    return render_template(
        "views/task/station_delete.html",
        title="Durak Silme Onay",
        form=form,
        station=the_station,
    )


@task.route("/entry/detail/<int:eid>", methods=["GET", "POST"])
@login_required
def entry_detail(eid):
    form = EntryForm()
    the_entry = Entry.query.filter_by(id=eid).first_or_404()

    if form.validate_on_submit():
        the_entry.entry = form.entry.data
        the_entry.exit = form.exit.data
        the_entry.save()
        flash("Föy Kaydedildi", "success")

    form.entry.data = the_entry.entry
    form.exit.data = the_entry.exit
    form.station_name.data = the_entry.station_name

    return render_template(
        "views/task/entry_detail.html",
        title="Giriş Detay",
        form=form,
        entry=the_entry
    )
