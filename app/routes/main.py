from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from app.models.task import Task, Assignment, Leaflet
from app.models.enums import Status
from app.models.enums.user import UserRole

main = Blueprint("main", __name__, url_prefix="/")


@main.route("/")
@main.route("/index")
@login_required
def index():
    if current_user.role == UserRole.admin:
        return redirect(url_for("main.index_admin"))

    return redirect(url_for("main.index_staff"))


@main.route("/index/admin")
@login_required
def index_admin():
    return render_template("views/main/index_admin.html", title="Admin Ana Sayfa")


@main.route("/index/staff")
@login_required
def index_staff():
    tasks = Task.query.filter_by(
        status=Status.active
    ).filter(
        Task.assignments.any(Assignment.user_id == current_user.id)
    ).order_by(Task.date.asc()).all()
    leaflets = Leaflet.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Leaflet.created_at.desc()
    ).filter(
        Leaflet.task.has(Task.status == Status.active)
    ).order_by(
        Leaflet.created_at.desc()
    ).limit(10)
    return render_template("views/main/index_staff.html", title="Personel Ana Sayfa", tasks=tasks, leaflets=leaflets)
